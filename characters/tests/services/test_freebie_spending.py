"""Tests for Freebie spending service."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.mage import Mage
from characters.models.vampire.vampire import Vampire
from characters.services.freebie_spending import (
    FreebieApplyResult,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    MageFreebieSpendingService,
    VampireFreebieSpendingService,
)
from characters.services.xp_spending import XPSpendingServiceFactory
from game.models import Chronicle, FreebieSpendingRecord


class TestFreebieSpendResult(TestCase):
    """Test FreebieSpendResult dataclass."""

    def test_success_result(self):
        """Test successful result creation."""
        result = FreebieSpendResult(
            success=True,
            trait="Strength",
            cost=5,
            message="Spent 5 freebies on Strength",
        )
        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.cost, 5)
        self.assertEqual(result.message, "Spent 5 freebies on Strength")
        self.assertIsNone(result.error)

    def test_failure_result(self):
        """Test failure result creation."""
        result = FreebieSpendResult(
            success=False,
            trait="Strength",
            cost=0,
            message="",
            error="Not enough freebies",
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Not enough freebies")


class TestFreebieApplyResult(TestCase):
    """Test FreebieApplyResult dataclass."""

    def test_success_result(self):
        """Test successful apply result creation."""
        result = FreebieApplyResult(
            success=True,
            trait="Strength",
            message="Approved Strength",
        )
        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.message, "Approved Strength")
        self.assertIsNone(result.error)


class TestFreebieSpendingServiceFactory(TestCase):
    """Test FreebieSpendingServiceFactory."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_get_mage_service(self):
        """Test factory returns correct service for Mage."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )
        service = FreebieSpendingServiceFactory.get_service(mage)
        self.assertIsInstance(service, MageFreebieSpendingService)

    def test_get_vampire_service(self):
        """Test factory returns correct service for Vampire."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            chronicle=self.chronicle,
            freebies=15,
        )
        service = FreebieSpendingServiceFactory.get_service(vampire)
        self.assertIsInstance(service, VampireFreebieSpendingService)

    def test_get_categories(self):
        """Test factory can get available categories for a character."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )
        categories = FreebieSpendingServiceFactory.get_categories_for_character(mage)
        self.assertIn("Attribute", categories)
        self.assertIn("Ability", categories)
        self.assertIn("Sphere", categories)
        self.assertIn("Arete", categories)


class TestHumanFreebieSpendingService(TestCase):
    """Test HumanFreebieSpendingService attribute and ability spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
            strength=2,
            alertness=1,
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")
        self.alertness = Ability.objects.create(name="Alertness", property_name="alertness")

    def test_spend_on_attribute(self):
        """Test spending freebies on an attribute."""
        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.cost, 5)  # Attribute cost is 5
        self.assertIn("freebies", result.message)

        # Verify attribute was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, 3)

        # Verify freebies were deducted
        self.assertEqual(self.mage.freebies, 10)

        # Verify FreebieSpendingRecord was created
        record = FreebieSpendingRecord.objects.get(character=self.mage)
        self.assertEqual(record.trait_name, "Strength")
        self.assertEqual(record.trait_type, "attribute")
        self.assertEqual(record.cost, 5)
        self.assertEqual(record.approved, "Pending")

    def test_spend_on_attribute_insufficient_freebies(self):
        """Test spending on attribute with insufficient freebies."""
        self.mage.freebies = 2
        self.mage.save()

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertFalse(result.success)
        self.assertIn("Not enough freebies", result.error)

    def test_spend_on_attribute_at_maximum(self):
        """Test spending on attribute already at maximum."""
        self.mage.strength = 5
        self.mage.save()

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertFalse(result.success)
        self.assertIn("maximum", result.error)

    def test_spend_on_ability(self):
        """Test spending freebies on an ability."""
        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Ability", self.alertness)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Alertness")
        self.assertEqual(result.cost, 2)  # Ability cost is 2

        # Verify ability was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.alertness, 2)

    def test_spend_on_willpower(self):
        """Test spending freebies on Willpower."""
        initial_willpower = self.mage.willpower

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Willpower")

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Willpower")
        self.assertEqual(result.cost, 1)  # Willpower cost is 1

        # Verify willpower was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.willpower, initial_willpower + 1)


class TestHumanFreebieSpendingBackgrounds(TestCase):
    """Test HumanFreebieSpendingService background spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )
        self.resources = Background.objects.create(name="Resources", property_name="resources")

    def test_spend_on_new_background(self):
        """Test spending freebies on a new background."""
        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("New Background", self.resources, note="Family wealth")

        self.assertTrue(result.success)
        self.assertIn("Resources", result.trait)
        self.assertIn("Family wealth", result.trait)

        # Verify background was created
        bg_rating = BackgroundRating.objects.get(char=self.mage, bg=self.resources)
        self.assertEqual(bg_rating.rating, 1)
        self.assertEqual(bg_rating.note, "Family wealth")

    def test_spend_on_existing_background(self):
        """Test spending freebies on an existing background."""
        bg_rating = BackgroundRating.objects.create(
            char=self.mage,
            bg=self.resources,
            rating=2,
            note="Inheritance",
        )

        service = HumanFreebieSpendingService(self.mage)
        result = service.spend("Existing Background", bg_rating)

        self.assertTrue(result.success)

        # Verify background was increased
        bg_rating.refresh_from_db()
        self.assertEqual(bg_rating.rating, 3)


class TestMageFreebieSpendingService(TestCase):
    """Test MageFreebieSpendingService Mage-specific spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        # Arete must be higher than current sphere for add_sphere to work
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=3,
            freebies=30,
            forces=1,
        )
        from characters.models.mage.sphere import Sphere

        self.forces = Sphere.objects.filter(name="Forces").first()
        if not self.forces:
            self.forces = Sphere.objects.create(name="Forces", property_name="forces")

    def test_spend_on_sphere(self):
        """Test spending freebies on a Sphere."""
        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Forces")
        self.assertEqual(result.cost, 7)  # Sphere cost is 7

        # Verify sphere was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.forces, 2)

    def test_inherit_human_handlers(self):
        """Test that MageFreebieSpendingService inherits human handlers."""
        service = MageFreebieSpendingService(self.mage)
        categories = service.available_categories

        # Should have human categories
        self.assertIn("Attribute", categories)
        self.assertIn("Ability", categories)
        self.assertIn("Willpower", categories)

        # Should also have Mage categories
        self.assertIn("Sphere", categories)
        self.assertIn("Arete", categories)
        self.assertIn("Resonance", categories)

    def test_avatar_freebie_adds_to_starting_quintessence(self):
        avatar, _ = Background.objects.get_or_create(
            property_name="avatar", defaults={"name": "Avatar"}
        )
        self.mage.quintessence = 4
        self.mage.save(update_fields=["quintessence"])
        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Background", avatar)
        self.assertTrue(result.success, result.error)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.avatar, 1)
        self.assertEqual(self.mage.quintessence, 5)

        rating = BackgroundRating.objects.get(char=self.mage, bg=avatar)
        result = service.spend("Background", rating)
        self.assertTrue(result.success, result.error)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.avatar, 2)
        self.assertEqual(self.mage.quintessence, 6)

    def test_denied_avatar_freebie_reverts_its_quintessence(self):
        avatar, _ = Background.objects.get_or_create(
            property_name="avatar", defaults={"name": "Avatar"}
        )
        service = MageFreebieSpendingService(self.mage)
        self.assertTrue(service.spend("Background", avatar).success)
        request = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        storyteller = User.objects.create_user("avatar_storyteller")
        self.assertTrue(service.deny(request, storyteller).success)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.avatar, 0)
        self.assertEqual(self.mage.quintessence, 0)


class TestFreebieApprovalDenial(TestCase):
    """Test freebie spending approval and denial."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.st_user = User.objects.create_user(
            username="storyteller", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
            strength=2,
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")

    def test_approve_freebie_spend(self):
        """Test approving a freebie spending request."""
        # First spend freebies to create a pending request
        service = MageFreebieSpendingService(self.mage)
        spend_result = service.spend("Attribute", self.strength)
        self.assertTrue(spend_result.success)

        # Get the pending request
        freebie_request = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")

        # Approve the request
        apply_result = service.apply(freebie_request, self.st_user)

        self.assertTrue(apply_result.success)
        self.assertIn("Approved", apply_result.message)

        # Verify request was marked approved
        freebie_request.refresh_from_db()
        self.assertEqual(freebie_request.approved, "Approved")
        self.assertEqual(freebie_request.approved_by, self.st_user)
        self.assertIsNotNone(freebie_request.approved_at)

    def test_deny_freebie_spend(self):
        """Test denying a freebie spending request reverts changes."""
        initial_strength = self.mage.strength
        initial_freebies = self.mage.freebies

        # Spend freebies
        service = MageFreebieSpendingService(self.mage)
        spend_result = service.spend("Attribute", self.strength)
        self.assertTrue(spend_result.success)

        # Verify trait increased and freebies deducted
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, initial_strength + 1)
        self.assertEqual(self.mage.freebies, initial_freebies - 5)

        # Get the pending request
        freebie_request = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")

        # Deny the request
        deny_result = service.deny(freebie_request, self.st_user)

        self.assertTrue(deny_result.success)
        self.assertIn("Denied", deny_result.message)

        # Verify trait was reverted
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, initial_strength)

        # Verify freebies were refunded
        self.assertEqual(self.mage.freebies, initial_freebies)

        # Verify request was marked denied
        freebie_request.refresh_from_db()
        self.assertEqual(freebie_request.approved, "Denied")


class TestUnknownCategory(TestCase):
    """Test handling of unknown freebie categories."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
        )

    def test_unknown_category_returns_error(self):
        """Test that spending on unknown category returns error."""
        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Invalid Category")

        self.assertFalse(result.success)
        self.assertIn("Unknown freebie category", result.error)


class TestSphereAreteFreebiValidation(TestCase):
    """Test that sphere spending respects Arete limits."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        from characters.models.mage.sphere import Sphere

        self.forces = Sphere.objects.filter(name="Forces").first()
        if not self.forces:
            self.forces = Sphere.objects.create(name="Forces", property_name="forces")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=2,  # Arete is 2
            freebies=30,
            forces=2,  # Forces is already at Arete level
        )

    def test_sphere_cannot_exceed_arete(self):
        """Test that spending freebies on a sphere that would exceed Arete fails."""
        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertFalse(result.success)
        self.assertIn("cannot exceed Arete", result.error)

        # Verify sphere was NOT increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.forces, 2)

    def test_sphere_at_arete_cannot_increase(self):
        """Test sphere exactly at Arete limit cannot be increased further."""
        # Set Forces at Arete limit
        self.mage.forces = 2
        self.mage.arete = 2
        self.mage.save()

        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertFalse(result.success)
        self.assertIn("cannot exceed Arete", result.error)

    def test_sphere_below_arete_can_increase(self):
        """Test sphere below Arete limit can be increased."""
        self.mage.forces = 1
        self.mage.arete = 3  # Arete is 3, Forces is 1
        self.mage.save()

        service = MageFreebieSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertTrue(result.success)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.forces, 2)


class TestVampireDisciplineFreebies(TestCase):
    """Every Discipline costs 7 freebies per dot, in clan or out."""

    def setUp(self):
        from characters.models.vampire.clan import VampireClan
        from characters.models.vampire.discipline import Discipline

        self.user = User.objects.create_user(username="kindred_owner")
        self.potence = Discipline.objects.create(name="Potence", property_name="potence")
        self.auspex = Discipline.objects.create(name="Auspex", property_name="auspex")
        clan = VampireClan.objects.create(name="Brujah")
        clan.disciplines.add(self.potence)
        self.vampire = Vampire.objects.create(
            name="Test Kindred", owner=self.user, clan=clan, freebies=15
        )

    def test_in_clan_and_out_of_clan_disciplines_cost_seven(self):
        service = VampireFreebieSpendingService(self.vampire)
        for discipline in (self.potence, self.auspex):
            with self.subTest(discipline=discipline.name):
                result = service.spend("Discipline", discipline)
                self.assertTrue(result.success, result.error)
                self.assertEqual(result.cost, 7)
        self.vampire.refresh_from_db()
        self.assertEqual((self.vampire.potence, self.vampire.auspex), (1, 1))
        self.assertEqual(self.vampire.freebies, 1)

    def test_ghoul_discipline_costs_seven(self):
        from characters.models.vampire.ghoul import Ghoul

        ghoul = Ghoul.objects.create(name="Test Ghoul", owner=self.user, freebies=7)
        starting_potence = ghoul.potence
        result = FreebieSpendingServiceFactory.get_service(ghoul).spend("Discipline", self.potence)
        self.assertTrue(result.success, result.error)
        self.assertEqual(result.cost, 7)
        ghoul.refresh_from_db()
        self.assertEqual((ghoul.potence, ghoul.freebies), (starting_potence + 1, 0))


class TestEveryFeraBreedSpendsFeraTraits(TestCase):
    """Every Changing Breed buys Gifts, Rage and Gnosis through the Fera services."""

    BREEDS = (
        "ajaba",
        "ananasi",
        "bastet",
        "corax",
        "grondr",
        "gurahl",
        "kitsune",
        "mokole",
        "nagah",
        "nuwisha",
        "ratkin",
        "rokea",
    )

    def test_every_breed_is_served_by_a_fera_service(self):
        from characters.services.freebie_spending import FeraFreebieSpendingService
        from characters.services.xp_spending import FeraXPSpendingService

        for breed in self.BREEDS:
            with self.subTest(breed=breed):
                self.assertTrue(
                    issubclass(
                        FreebieSpendingServiceFactory._service_map[breed],
                        FeraFreebieSpendingService,
                    )
                )
                self.assertTrue(
                    issubclass(XPSpendingServiceFactory._service_map[breed], FeraXPSpendingService)
                )

    def test_every_breed_buys_rage_with_freebies(self):
        from django.apps import apps

        user = User.objects.create_user(username="fera_owner")
        for breed in self.BREEDS:
            with self.subTest(breed=breed):
                model = next(
                    m
                    for m in apps.get_app_config("characters").get_models()
                    if getattr(m, "type", None) == breed
                )
                fera = model.objects.create(name=f"Test {breed}", owner=user, rage=1)
                result = FreebieSpendingServiceFactory.get_service(fera).spend("Rage")
                self.assertTrue(result.success, result.error)
                fera.refresh_from_db()
                self.assertEqual(fera.rage, 2)


class TestWerewolfRiteSpending(TestCase):
    """Rites land in rites_known, for Garou and Fera alike."""

    def setUp(self):
        from characters.models.werewolf.bastet import Bastet
        from characters.models.werewolf.garou import Werewolf
        from characters.models.werewolf.rite import Rite

        self.user = User.objects.create_user(username="rite_owner")
        self.rite = Rite.objects.create(name="Rite of Cleansing", level=1)
        self.characters = [
            model.objects.create(name=model.__name__, owner=self.user, xp=10)
            for model in (Werewolf, Bastet)
        ]

    def test_freebie_rite_spend_learns_the_rite(self):
        for character in self.characters:
            with self.subTest(type=character.type):
                service = FreebieSpendingServiceFactory.get_service(character)
                result = service.spend("Rite", self.rite)
                self.assertTrue(result.success, result.error)
                self.assertIn(self.rite, character.rites_known.all())

    def test_approved_xp_rite_request_learns_the_rite(self):
        from game.models import XPSpendingRequest

        for character in self.characters:
            with self.subTest(type=character.type):
                request = XPSpendingRequest.objects.create(
                    character=character,
                    trait_name=self.rite.name,
                    trait_type="rite",
                    trait_value=1,
                    cost=3,
                    approved="Pending",
                )
                service = XPSpendingServiceFactory.get_service(character)
                result = service.apply(request, self.user)
                self.assertTrue(result.success)
                self.assertIn(self.rite, character.rites_known.all())
