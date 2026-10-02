"""Tests for Freebie spending service."""

from types import SimpleNamespace
from unittest import mock

from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.changeling.changeling import Changeling
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.statistic import Statistic
from characters.models.demon.demon import Demon
from characters.models.demon.thrall import Thrall
from characters.models.hunter.hunter import Hunter
from characters.models.mage.mage import Mage
from characters.models.mage.sphere import Sphere
from characters.models.mummy.mummy import Mummy
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from characters.models.werewolf.bastet import Bastet
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.rite import Rite
from characters.models.wraith.wraith import Wraith
from characters.services.freebie_spending import (
    FeraFreebieSpendingService,
    FreebieApplyResult,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    MageFreebieSpendingService,
    VampireFreebieSpendingService,
)
from characters.services.xp_spending import FeraXPSpendingService, XPSpendingServiceFactory
from game.models import Chronicle, FreebieSpendingRecord, XPSpendingRequest


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


class TestFreebieDenialReverts(TestCase):
    """deny() reverts exactly the recorded spend, or refuses and changes nothing."""

    def setUp(self):
        self.user = User.objects.create_user(username="denial-player")
        self.st_user = User.objects.create_user(username="denial-st")
        self.chronicle = Chronicle.objects.create(name="Denial Chronicle")
        self.mage = Mage.objects.create(
            name="Denied Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
            freebies=15,
            strength=2,
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")
        self.resources = Background.objects.create(name="Resources", property_name="resources")
        self.service = MageFreebieSpendingService(self.mage)

    def record(self, **kwargs):
        fields = {
            "character": self.mage,
            "trait_name": "Strength",
            "trait_type": "attribute",
            "trait_value": 3,
            "cost": 5,
        }
        fields.update(kwargs)
        return FreebieSpendingRecord.objects.create(**fields)

    def assert_untouched(self, record, *, freebies, strength):
        record.refresh_from_db()
        self.mage.refresh_from_db()
        self.assertEqual(record.approved, "Pending")
        self.assertIsNone(record.approved_by)
        self.assertEqual(self.mage.freebies, freebies)
        self.assertEqual(self.mage.strength, strength)

    def test_missing_catalogue_row_fails_and_changes_nothing(self):
        record = self.record(trait_name="Charisma")

        result = self.service.deny(record, self.st_user)

        self.assertFalse(result.success)
        self.assertIn("Charisma", result.error)
        self.assert_untouched(record, freebies=15, strength=2)

    def test_raising_revert_fails_and_rolls_back(self):
        record = self.record(trait_value=2)

        def partial_then_raise(freebie_request, approver, deny=False):
            self.mage.freebies += 999
            self.mage.save()
            raise RuntimeError("catalogue exploded")

        with mock.patch.object(
            MageFreebieSpendingService, "_apply_attribute", side_effect=partial_then_raise
        ):
            result = self.service.deny(record, self.st_user)

        self.assertFalse(result.success)
        self.assertEqual(result.error, "Could not revert Strength: an unexpected error was logged")
        self.assertNotIn("exploded", result.error)
        self.assert_untouched(record, freebies=15, strength=2)

    def test_validation_error_during_revert_reaches_the_storyteller(self):
        record = self.record(trait_value=2)

        def invalid_revert(freebie_request, approver, deny=False):
            raise ValidationError({"strength": ["Strength cannot drop below 2 for this clan."]})

        with mock.patch.object(
            MageFreebieSpendingService, "_apply_attribute", side_effect=invalid_revert
        ):
            result = self.service.deny(record, self.st_user)

        self.assertFalse(result.success)
        self.assertEqual(
            result.error, "Could not revert Strength: Strength cannot drop below 2 for this clan."
        )
        self.assert_untouched(record, freebies=15, strength=2)

    def test_unregistered_trait_type_fails(self):
        record = self.record(trait_type="custom")

        result = self.service.deny(record, self.st_user)

        self.assertFalse(result.success)
        self.assertIn("custom", result.error)
        self.assert_untouched(record, freebies=15, strength=2)

    def test_denial_restores_the_recorded_value(self):
        self.assertTrue(self.service.spend("Attribute", self.strength).success)
        record = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        self.assertEqual(record.trait_value, 3)

        result = self.service.deny(record, self.st_user)

        self.assertTrue(result.success, result.error)
        record.refresh_from_db()
        self.mage.refresh_from_db()
        self.assertEqual(record.approved, "Denied")
        self.assertEqual(record.approved_by, self.st_user)
        self.assertEqual(self.mage.strength, 2)
        self.assertEqual(self.mage.freebies, 15)

    def test_denial_after_a_later_raise_refuses(self):
        self.assertTrue(self.service.spend("Attribute", self.strength).success)
        first = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        self.assertTrue(self.service.spend("Attribute", self.strength).success)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, 4)

        result = self.service.deny(first, self.st_user)

        self.assertFalse(result.success)
        self.assertIn("Strength", result.error)
        self.assert_untouched(first, freebies=5, strength=4)

    def test_new_background_is_recorded_and_removed_on_denial(self):
        result = self.service.spend("New Background", self.resources, note="Family wealth")
        self.assertTrue(result.success, result.error)
        record = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        self.assertEqual(record.trait_type, "new-background")
        self.assertEqual(record.trait_value, 1)
        freebies_after_spend = Mage.objects.get(pk=self.mage.pk).freebies

        deny = self.service.deny(record, self.st_user)

        self.assertTrue(deny.success, deny.error)
        self.assertFalse(
            BackgroundRating.objects.filter(char=self.mage, bg=self.resources).exists()
        )
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.freebies, freebies_after_spend + record.cost)

    def test_existing_background_denial_decrements(self):
        rating = BackgroundRating.objects.create(char=self.mage, bg=self.resources, rating=2)
        self.assertTrue(self.service.spend("Existing Background", rating).success)
        record = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        self.assertEqual(record.trait_type, "background")
        self.assertEqual(record.trait_value, 3)

        deny = self.service.deny(record, self.st_user)

        self.assertTrue(deny.success, deny.error)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 2)

    def test_background_denial_after_a_later_raise_refuses(self):
        rating = BackgroundRating.objects.create(char=self.mage, bg=self.resources, rating=1)
        self.assertTrue(self.service.spend("Existing Background", rating).success)
        record = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        rating.refresh_from_db()
        rating.rating = 3
        rating.save()

        deny = self.service.deny(record, self.st_user)

        self.assertFalse(deny.success)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)
        record.refresh_from_db()
        self.assertEqual(record.approved, "Pending")

    def test_old_spelling_record_refuses_once_the_background_was_raised(self):
        BackgroundRating.objects.create(char=self.mage, bg=self.resources, rating=2, note="Old")
        record = self.record(
            trait_name="Resources (Old)", trait_type="background", trait_value=1, cost=1
        )

        deny = self.service.deny(record, self.st_user)

        self.assertFalse(deny.success)
        self.assertEqual(
            BackgroundRating.objects.get(char=self.mage, bg=self.resources, note="Old").rating, 2
        )
        record.refresh_from_db()
        self.assertEqual(record.approved, "Pending")

    def test_old_new_background_record_spelled_background_still_deletes(self):
        BackgroundRating.objects.create(char=self.mage, bg=self.resources, rating=1, note="Old")
        record = self.record(
            trait_name="Resources (Old)", trait_type="background", trait_value=1, cost=1
        )

        deny = self.service.deny(record, self.st_user)

        self.assertTrue(deny.success, deny.error)
        self.assertFalse(
            BackgroundRating.objects.filter(char=self.mage, bg=self.resources).exists()
        )

    def test_overlapping_spends_deny_in_reverse_order(self):
        self.assertTrue(self.service.spend("Attribute", self.strength).success)
        first = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        self.assertTrue(self.service.spend("Attribute", self.strength).success)
        second = FreebieSpendingRecord.objects.get(
            character=self.mage, approved="Pending", trait_value=4
        )

        refused = self.service.deny(first, self.st_user)
        self.assertFalse(refused.success)
        self.assertIn("later spend", refused.error)

        self.assertTrue(self.service.deny(second, self.st_user).success)
        self.assertTrue(self.service.deny(first, self.st_user).success)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, 2)
        self.assertEqual(self.mage.freebies, 15)

    def test_pool_trait_changed_since_the_spend_refuses(self):
        """A pool (Quintessence here) that moved after the spend is not reverted relative
        to its current value: the denial refuses and the storyteller corrects by hand."""
        self.mage.quintessence = 4
        self.mage.save()
        self.assertTrue(self.service.spend("Quintessence").success)
        record = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        self.assertEqual(record.trait_value, 8)
        Mage.objects.filter(pk=self.mage.pk).update(quintessence=6)
        self.mage.refresh_from_db()

        result = self.service.deny(record, self.st_user)

        self.assertFalse(result.success)
        self.assertIn("Quintessence is 6", result.error)
        record.refresh_from_db()
        self.mage.refresh_from_db()
        self.assertEqual(record.approved, "Pending")
        self.assertEqual(self.mage.quintessence, 6)

    def test_background_note_ending_in_a_parenthesis_is_found(self):
        note = "Trust fund (contested)"
        result = self.service.spend("New Background", self.resources, note=note)
        self.assertTrue(result.success, result.error)
        record = FreebieSpendingRecord.objects.get(character=self.mage, approved="Pending")
        self.assertEqual(record.trait_name, f"Resources ({note})")

        deny = self.service.deny(record, self.st_user)

        self.assertTrue(deny.success, deny.error)
        self.assertFalse(BackgroundRating.objects.filter(char=self.mage, note=note).exists())

    def test_ambiguous_catalogue_name_refuses(self):
        Attribute.objects.create(name="Strength", property_name="dexterity")
        record = self.record(trait_value=2)

        result = self.service.deny(record, self.st_user)

        self.assertFalse(result.success)
        self.assertIn("More than one", result.error)
        self.assert_untouched(record, freebies=15, strength=2)


class TestEveryColumnRevertRoundTrips(TestCase):
    """Every applier that reverts through ``_revert_column`` restores the exact value a
    spend set, so a wrong ``step`` or a missing ``mirror`` in any gameline shows up here.

    Quintessence and Pathos are excluded from the spend-then-deny cases because their
    freebie costs are fractional (0.25 and 0.5), which the integer ``cost`` column stores
    as 0; Corpus, Banality Reduction and Torment Reduction because they have no freebie
    cost entry, so the spend itself fails. Those are spend-side defects outside the
    denial fix; their reverts are covered by the hand-filed records below.
    """

    @classmethod
    def setUpTestData(cls):
        cls.player = User.objects.create_user(username="roundtrip-player")
        cls.storyteller = User.objects.create_user(username="roundtrip-st")
        cls.forces = Sphere.objects.create(name="Forces", property_name="forces")
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.chicanery = Statistic.objects.create(name="Chicanery", property_name="chicanery")
        cls.actor = Statistic.objects.create(name="Actor", property_name="actor")

    @staticmethod
    def named(name, property_name):
        return SimpleNamespace(name=name, property_name=property_name)

    def spend_cases(self):
        # (model, create kwargs, category, example, column, mirror column or None)
        return [
            (Mage, {"arete": 1}, "Arete", None, "arete", None),
            (Mage, {"arete": 1}, "Rote Points", None, "rote_points", None),
            (Mage, {"arete": 1}, "Sphere", self.forces, "forces", None),
            (Mage, {"arete": 1}, "Willpower", None, "willpower", "temporary_willpower"),
            (Vampire, {"humanity": 5}, "Humanity", None, "humanity", None),
            (Vampire, {}, "Discipline", self.potence, "potence", None),
            (Vampire, {}, "Virtue", self.named("Conscience", "conscience"), "conscience", None),
            (Werewolf, {"rage": 3, "gnosis": 3}, "Rage", None, "rage", None),
            (Werewolf, {"rage": 3, "gnosis": 3}, "Gnosis", None, "gnosis", None),
            (Werewolf, {"rage": 3, "gnosis": 3}, "Glory", None, "temporary_glory", None),
            (Werewolf, {"rage": 3, "gnosis": 3}, "Honor", None, "temporary_honor", None),
            (Werewolf, {"rage": 3, "gnosis": 3}, "Wisdom", None, "temporary_wisdom", None),
            (Mummy, {"sekhem": 3, "balance": 3}, "Sekhem", None, "sekhem", None),
            (Mummy, {"sekhem": 3, "balance": 3}, "Balance", None, "balance", None),
            (Mummy, {}, "Hekau", self.named("Alchemy", "alchemy"), "alchemy", None),
            (Changeling, {}, "Art", self.chicanery, "chicanery", None),
            (Changeling, {}, "Realm", self.actor, "actor", None),
            (Changeling, {"glamour": 3}, "Glamour", None, "glamour", "temporary_glamour"),
            (Demon, {"faith": 3}, "Faith", None, "faith", None),
            (Demon, {}, "Virtue", self.named("Conviction", "conviction"), "conviction", None),
            (Thrall, {}, "Faith Potential", None, "faith_potential", None),
            (Hunter, {}, "Virtue", self.named("Zeal", "zeal"), "zeal", None),
        ]

    def test_spend_then_deny_restores_the_column(self):
        for model, kwargs, category, example, column, mirror in self.spend_cases():
            with self.subTest(model=model.__name__, category=category):
                character = model.objects.create(
                    name=f"{model.__name__} {category}", owner=self.player, freebies=30, **kwargs
                )
                before = getattr(character, column)
                service = FreebieSpendingServiceFactory.get_service(character)

                spend = service.spend(category, example)
                self.assertTrue(spend.success, spend.error)
                character.refresh_from_db()
                self.assertNotEqual(getattr(character, column), before)
                record = FreebieSpendingRecord.objects.get(character=character, approved="Pending")

                deny = service.deny(record, self.storyteller)
                self.assertTrue(deny.success, deny.error)
                character.refresh_from_db()
                record.refresh_from_db()
                self.assertEqual(getattr(character, column), before)
                if mirror:
                    self.assertEqual(getattr(character, mirror), before)
                self.assertEqual(character.freebies, 30)
                self.assertEqual(record.approved, "Denied")

    def test_hand_filed_records_revert_by_their_step(self):
        """The +4 pools and the reductions revert ``trait_value - step``."""
        cases = [
            # (model, column, trait type, value the spend set, value before it)
            (Mage, "quintessence", "quintessence", 7, 3),
            (Mage, "rote_points", "rotes", 10, 6),
            (Wraith, "pathos", "pathos", 6, 5),
            (Wraith, "corpus", "corpus", 6, 5),
            (Changeling, "banality", "banality_reduction", 4, 5),
            (Demon, "torment", "torment_reduction", 4, 5),
        ]
        for model, column, trait_type, after, before in cases:
            with self.subTest(model=model.__name__, trait_type=trait_type):
                character = model.objects.create(
                    name=f"{model.__name__} {trait_type}",
                    owner=self.player,
                    freebies=10,
                    **{column: after},
                )
                record = FreebieSpendingRecord.objects.create(
                    character=character,
                    trait_name=trait_type,
                    trait_type=trait_type,
                    trait_value=after,
                    cost=1,
                )

                deny = FreebieSpendingServiceFactory.get_service(character).deny(
                    record, self.storyteller
                )

                self.assertTrue(deny.success, deny.error)
                character.refresh_from_db()
                self.assertEqual(getattr(character, column), before)
                self.assertEqual(character.freebies, 11)
