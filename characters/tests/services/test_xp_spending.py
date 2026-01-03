"""Tests for XP spending service."""

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.mage import Mage, PracticeRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from characters.services.xp_spending import (
    MageXPSpendingService,
    XPApplyResult,
    XPSpendingServiceFactory,
    XPSpendResult,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from game.models import Chronicle, ObjectType, XPSpendingRequest


class TestXPSpendResult(TestCase):
    """Test XPSpendResult dataclass."""

    def test_success_result(self):
        """Test successful result creation."""
        result = XPSpendResult(
            success=True,
            trait="Strength",
            cost=4,
            message="Spent 4 XP on Strength",
        )
        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.cost, 4)
        self.assertEqual(result.message, "Spent 4 XP on Strength")
        self.assertIsNone(result.error)

    def test_failure_result(self):
        """Test failure result creation."""
        result = XPSpendResult(
            success=False,
            trait="Strength",
            cost=0,
            message="",
            error="Insufficient XP",
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Insufficient XP")


class TestMageXPSpendingServiceAttributes(TestCase):
    """Test MageXPSpendingService attribute spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            strength=2,
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")

    def test_spend_on_attribute(self):
        """Test spending XP on an attribute."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.cost, 8)  # current * 4 = 2 * 4 = 8
        self.assertIn("XP", result.message)

        # Verify XP was deducted
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.xp, 42)

    def test_spend_on_attribute_insufficient_xp(self):
        """Test spending on attribute with insufficient XP."""
        self.mage.xp = 1
        self.mage.save()

        service = MageXPSpendingService(self.mage)
        result = service.spend("Attribute", self.strength)

        self.assertFalse(result.success)
        self.assertIn("Insufficient", result.error)


class TestMageXPSpendingServiceAbilities(TestCase):
    """Test MageXPSpendingService ability spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            alertness=2,
        )
        self.alertness = Ability.objects.create(name="Alertness", property_name="alertness")

    def test_spend_on_ability(self):
        """Test spending XP on an ability."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Ability", self.alertness)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Alertness")
        self.assertEqual(result.cost, 4)  # current * 2 = 2 * 2 = 4


class TestMageXPSpendingServiceBackgrounds(TestCase):
    """Test MageXPSpendingService background spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
        )
        self.resources = Background.objects.create(name="Resources", property_name="resources")
        # Create existing background rating
        self.bg_rating = BackgroundRating.objects.create(
            char=self.mage,
            bg=self.resources,
            rating=2,
            note="Family wealth",
        )

    def test_spend_on_new_background(self):
        """Test spending XP on a new background."""
        contacts = Background.objects.create(name="Contacts", property_name="contacts")
        service = MageXPSpendingService(self.mage)
        result = service.spend("New Background", contacts, note="Street informants")

        self.assertTrue(result.success)
        self.assertIn("Contacts", result.trait)
        self.assertEqual(result.cost, 5)  # new background = 5 XP

    def test_spend_on_existing_background(self):
        """Test spending XP on an existing background."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Existing Background", self.bg_rating)

        self.assertTrue(result.success)
        self.assertIn("Resources", result.trait)
        self.assertEqual(result.cost, 6)  # current * 3 = 2 * 3 = 6


class TestMageXPSpendingServiceWillpower(TestCase):
    """Test MageXPSpendingService willpower spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            willpower=5,
        )

    def test_spend_on_willpower(self):
        """Test spending XP on willpower."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Willpower", None)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Willpower")
        self.assertEqual(result.cost, 5)  # current willpower cost


class TestMageXPSpendingServiceMeritFlaw(TestCase):
    """Test MageXPSpendingService merit/flaw spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
        )
        mage_type, _ = ObjectType.objects.get_or_create(
            name="mage", defaults={"type": "char", "gameline": "mta"}
        )
        self.acute_sense = MeritFlaw.objects.create(
            name="Acute Senses",
            max_rating=3,
        )
        self.acute_sense.ratings.create(value=1)
        self.acute_sense.ratings.create(value=2)
        self.acute_sense.ratings.create(value=3)
        self.acute_sense.allowed_types.add(mage_type)

    def test_spend_on_merit_flaw(self):
        """Test spending XP on a merit/flaw."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("MeritFlaw", self.acute_sense, value=2)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Acute Senses")
        self.assertEqual(result.cost, 6)  # (2 - 0) * 3 = 6


class TestMageXPSpendingServiceSpheres(TestCase):
    """Test MageXPSpendingService sphere spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.forces = Sphere.objects.create(name="Forces", property_name="forces")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=3,
            xp=50,
            forces=1,
            affinity_sphere=self.forces,
        )

    def test_spend_on_affinity_sphere(self):
        """Test spending XP on an affinity sphere."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Sphere", self.forces)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Forces")
        # Affinity sphere cost: 7 * current = 7 * 1 = 7
        self.assertEqual(result.cost, 7)

    def test_spend_on_non_affinity_sphere(self):
        """Test spending XP on a non-affinity sphere."""
        prime = Sphere.objects.create(name="Prime", property_name="prime")
        self.mage.prime = 1
        self.mage.save()

        service = MageXPSpendingService(self.mage)
        result = service.spend("Sphere", prime)

        self.assertTrue(result.success)
        # Regular sphere cost: 8 * current = 8 * 1 = 8
        self.assertEqual(result.cost, 8)


class TestMageXPSpendingServiceTenets(TestCase):
    """Test MageXPSpendingService tenet spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.metaphysical = Tenet.objects.create(name="Everything is Data", tenet_type="met")
        self.personal = Tenet.objects.create(name="Self-Empowerment", tenet_type="per")
        self.ascension = Tenet.objects.create(
            name="Enlightenment Through Technology", tenet_type="asc"
        )
        self.other_tenet = Tenet.objects.create(name="All Is One", tenet_type="oth")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            metaphysical_tenet=self.metaphysical,
            personal_tenet=self.personal,
            ascension_tenet=self.ascension,
        )

    def test_spend_on_tenet(self):
        """Test spending XP to add a tenet."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Tenet", self.other_tenet)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "All Is One")
        self.assertEqual(result.cost, 0)  # Tenets are free

    def test_spend_on_remove_tenet(self):
        """Test spending XP to remove a tenet."""
        self.mage.other_tenets.add(self.other_tenet)
        self.mage.save()

        service = MageXPSpendingService(self.mage)
        result = service.spend("Remove Tenet", self.other_tenet)

        self.assertTrue(result.success)
        self.assertIn("Remove", result.trait)


class TestMageXPSpendingServicePractices(TestCase):
    """Test MageXPSpendingService practice spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
        )
        self.high_ritual = Practice.objects.create(name="High Ritual")
        # Create a practice rating
        PracticeRating.objects.create(
            mage=self.mage,
            practice=self.high_ritual,
            rating=1,
        )

    def test_spend_on_practice(self):
        """Test spending XP on a practice."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Practice", self.high_ritual)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "High Ritual")
        # Practice cost: 1 * current = 1 * 1 = 1
        self.assertEqual(result.cost, 1)


class TestMageXPSpendingServiceArete(TestCase):
    """Test MageXPSpendingService Arete spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=2,
            xp=50,
        )

    def test_spend_on_arete(self):
        """Test spending XP on Arete."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Arete", None)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Arete")
        # Arete cost: 8 * current = 8 * 2 = 16
        self.assertEqual(result.cost, 16)


class TestMageXPSpendingServiceResonance(TestCase):
    """Test MageXPSpendingService resonance spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
        )

    def test_spend_on_new_resonance(self):
        """Test spending XP on a new resonance."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Resonance", None, resonance="Dynamic")

        self.assertTrue(result.success)
        self.assertIn("Dynamic", result.trait)
        # New resonance cost: 5 (for rating 0)
        self.assertEqual(result.cost, 5)


class TestMageXPSpendingServiceRotePoints(TestCase):
    """Test MageXPSpendingService rote points spending."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            rote_points=0,
        )

    def test_spend_on_rote_points(self):
        """Test spending XP on rote points."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Rote Points", None)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Rote Points")
        # Rote points cost: 1 XP per point (buying 3 at a time)
        self.assertEqual(result.cost, 1)


class TestMageXPSpendingServiceUnknownCategory(TestCase):
    """Test MageXPSpendingService with unknown category."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
        )

    def test_unknown_category_returns_error(self):
        """Test that unknown category returns an error."""
        service = MageXPSpendingService(self.mage)
        result = service.spend("Unknown Category", None)

        self.assertFalse(result.success)
        self.assertIn("Unknown", result.error)


class TestXPSpendingServiceFactory(TestCase):
    """Test XPSpendingServiceFactory returns correct services."""

    def setUp(self):
        from characters.services.xp_spending import XPSpendingServiceFactory

        self.factory = XPSpendingServiceFactory
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_factory_returns_mage_service_for_mage(self):
        """Test factory returns MageXPSpendingService for mage characters."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            arete=1,
        )
        service = self.factory.get_service(mage)
        self.assertIsInstance(service, MageXPSpendingService)

    def test_factory_returns_correct_service_for_registered_types(self):
        """Test factory has all expected character types registered."""
        expected_types = [
            "human",
            "mage",
            "vampire",
            "werewolf",
            "wraith",
            "changeling",
            "demon",
            "hunter",
            "mummy",
            "sorcerer",
            "companion",
            "ghoul",
            "revenant",
            "kinfolk",
            "bastet",
            "corax",
        ]
        for char_type in expected_types:
            self.assertIn(
                char_type,
                self.factory._service_map,
                f"Character type '{char_type}' not registered in factory",
            )


class TestHandlerInheritance(TestCase):
    """Test that handler inheritance works correctly via metaclass."""

    def test_mage_service_has_human_handlers(self):
        """Test MageXPSpendingService inherits HumanXPSpendingService handlers."""
        # Human handlers that should be inherited
        human_handlers = [
            "Attribute",
            "Ability",
            "New Background",
            "Existing Background",
            "Willpower",
            "MeritFlaw",
        ]
        for handler in human_handlers:
            self.assertIn(
                handler,
                MageXPSpendingService._handlers,
                f"Handler '{handler}' not inherited by MageXPSpendingService",
            )

    def test_mage_service_has_mage_specific_handlers(self):
        """Test MageXPSpendingService has its own handlers."""
        mage_handlers = [
            "Sphere",
            "Arete",
            "Practice",
            "Tenet",
            "Remove Tenet",
            "Resonance",
            "Rote Points",
        ]
        for handler in mage_handlers:
            self.assertIn(
                handler,
                MageXPSpendingService._handlers,
                f"Handler '{handler}' not found in MageXPSpendingService",
            )

    def test_vampire_service_inherits_from_vtm_human(self):
        """Test VampireXPSpendingService inherits VtMHumanXPSpendingService handlers."""
        from characters.services.xp_spending import VampireXPSpendingService

        # VtMHuman adds Virtue handler, Vampire should inherit it
        self.assertIn("Virtue", VampireXPSpendingService._handlers)
        # Plus Vampire-specific handlers
        self.assertIn("Discipline", VampireXPSpendingService._handlers)
        self.assertIn("Morality", VampireXPSpendingService._handlers)

    def test_garou_service_has_werewolf_handlers(self):
        """Test GarouXPSpendingService has werewolf-specific handlers."""
        from characters.services.xp_spending import GarouXPSpendingService

        werewolf_handlers = ["Gift", "Rite", "Rage", "Gnosis"]
        for handler in werewolf_handlers:
            self.assertIn(
                handler,
                GarouXPSpendingService._handlers,
                f"Handler '{handler}' not found in GarouXPSpendingService",
            )

    def test_fera_services_inherit_from_garou(self):
        """Test Fera services inherit Garou handlers."""
        from characters.services.xp_spending import (
            BastetXPSpendingService,
            CoraxXPSpendingService,
            FeraXPSpendingService,
        )

        for service_class in [
            FeraXPSpendingService,
            BastetXPSpendingService,
            CoraxXPSpendingService,
        ]:
            self.assertIn(
                "Gift",
                service_class._handlers,
                f"Gift handler not inherited by {service_class.__name__}",
            )
            self.assertIn(
                "Gnosis",
                service_class._handlers,
                f"Gnosis handler not inherited by {service_class.__name__}",
            )


class TestAvailableCategories(TestCase):
    """Test available_categories property returns correct handlers."""

    def test_mage_available_categories(self):
        """Test MageXPSpendingService.available_categories returns all categories."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        mage = Mage.objects.create(
            name="Test Mage",
            owner=user,
            chronicle=chronicle,
            arete=1,
        )
        service = MageXPSpendingService(mage)
        categories = service.available_categories

        # Should include human + mage categories
        expected = [
            "Attribute",
            "Ability",
            "New Background",
            "Existing Background",
            "Willpower",
            "MeritFlaw",
            "Sphere",
            "Arete",
            "Practice",
            "Tenet",
            "Remove Tenet",
            "Resonance",
            "Rote Points",
        ]
        for cat in expected:
            self.assertIn(cat, categories, f"Category '{cat}' not in available_categories")


# =============================================================================
# APPLY/DENY TESTS
# =============================================================================


class TestXPApplyResult(TestCase):
    """Test XPApplyResult dataclass."""

    def test_success_result(self):
        """Test successful apply result creation."""
        result = XPApplyResult(
            success=True,
            trait="Strength",
            message="Approved Strength increase to 3",
        )
        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertEqual(result.message, "Approved Strength increase to 3")
        self.assertIsNone(result.error)

    def test_failure_result(self):
        """Test failure apply result creation."""
        result = XPApplyResult(
            success=False,
            trait="Unknown",
            message="",
            error="Unknown trait type",
        )
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Unknown trait type")


class TestApplyAttribute(TestCase):
    """Test applying attribute XP spending requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.approver = User.objects.create_user(
            username="approver", email="approver@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            strength=2,
        )
        self.strength = Attribute.objects.create(name="Strength", property_name="strength")

    def test_apply_attribute(self):
        """Test applying an approved attribute XP request."""
        # Create pending request
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Strength",
            trait_type="attribute",
            trait_value=3,
            cost=8,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Strength")
        self.assertIn("Approved", result.message)

        # Verify attribute was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, 3)

        # Verify request was marked approved
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved, "Approved")
        self.assertEqual(xp_request.approved_by, self.approver)
        self.assertIsNotNone(xp_request.approved_at)


class TestApplyAbility(TestCase):
    """Test applying ability XP spending requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.approver = User.objects.create_user(
            username="approver", email="approver@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            alertness=2,
        )
        self.alertness = Ability.objects.create(name="Alertness", property_name="alertness")

    def test_apply_ability(self):
        """Test applying an approved ability XP request."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Alertness",
            trait_type="ability",
            trait_value=3,
            cost=4,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Alertness")

        # Verify ability was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.alertness, 3)


class TestApplyBackground(TestCase):
    """Test applying background XP spending requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.approver = User.objects.create_user(
            username="approver", email="approver@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
        )
        self.resources = Background.objects.create(name="Resources", property_name="resources")
        self.bg_rating = BackgroundRating.objects.create(
            char=self.mage,
            bg=self.resources,
            rating=2,
            note="Family wealth",
        )

    def test_apply_existing_background(self):
        """Test applying an existing background XP request."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Resources (Family wealth)",
            trait_type="background",
            trait_value=3,
            cost=6,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertTrue(result.success)

        # Verify background rating was increased
        self.bg_rating.refresh_from_db()
        self.assertEqual(self.bg_rating.rating, 3)

    def test_apply_new_background(self):
        """Test applying a new background XP request."""
        contacts = Background.objects.create(name="Contacts", property_name="contacts")

        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Contacts (Street informants)",
            trait_type="new-background",
            trait_value=1,
            cost=5,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertTrue(result.success)

        # Verify new background was created
        new_bg = self.mage.backgrounds.filter(bg__name="Contacts").first()
        self.assertIsNotNone(new_bg)
        self.assertEqual(new_bg.rating, 1)
        self.assertEqual(new_bg.note, "Street informants")


class TestApplyWillpower(TestCase):
    """Test applying willpower XP spending requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.approver = User.objects.create_user(
            username="approver", email="approver@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
            willpower=5,
        )

    def test_apply_willpower(self):
        """Test applying a willpower XP request."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Willpower",
            trait_type="willpower",
            trait_value=6,
            cost=5,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Willpower")

        # Verify willpower was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.willpower, 6)


class TestApplySphere(TestCase):
    """Test applying sphere XP spending requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.approver = User.objects.create_user(
            username="approver", email="approver@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.forces = Sphere.objects.create(name="Forces", property_name="forces")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=3,
            xp=50,
            forces=1,
            affinity_sphere=self.forces,
        )

    def test_apply_sphere(self):
        """Test applying a sphere XP request."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Forces",
            trait_type="sphere",
            trait_value=2,
            cost=7,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Forces")

        # Verify sphere was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.forces, 2)


class TestApplyArete(TestCase):
    """Test applying arete XP spending requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.approver = User.objects.create_user(
            username="approver", email="approver@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=2,
            xp=50,
        )

    def test_apply_arete(self):
        """Test applying an arete XP request."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Arete",
            trait_type="arete",
            trait_value=3,
            cost=16,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertTrue(result.success)
        self.assertEqual(result.trait, "Arete")

        # Verify arete was increased
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.arete, 3)


class TestDenyXPRequest(TestCase):
    """Test denying XP spending requests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.denier = User.objects.create_user(
            username="denier", email="denier@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=42,  # After spending 8 XP on strength
            strength=2,
        )

    def test_deny_refunds_xp(self):
        """Test that denying a request refunds the XP cost."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Strength",
            trait_type="attribute",
            trait_value=3,
            cost=8,
            approved="Pending",
        )

        initial_xp = self.mage.xp  # 42

        service = MageXPSpendingService(self.mage)
        result = service.deny(xp_request, self.denier)

        self.assertTrue(result.success)
        self.assertIn("refunded", result.message)
        self.assertIn("8", result.message)

        # Verify XP was refunded
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.xp, initial_xp + 8)  # 42 + 8 = 50

        # Verify request was marked denied
        xp_request.refresh_from_db()
        self.assertEqual(xp_request.approved, "Denied")
        self.assertEqual(xp_request.approved_by, self.denier)
        self.assertIsNotNone(xp_request.approved_at)

    def test_deny_does_not_change_trait(self):
        """Test that denying a request does not change the trait value."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Strength",
            trait_type="attribute",
            trait_value=3,
            cost=8,
            approved="Pending",
        )

        initial_strength = self.mage.strength  # 2

        service = MageXPSpendingService(self.mage)
        service.deny(xp_request, self.denier)

        # Verify strength was NOT changed
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.strength, initial_strength)


class TestApplyUnknownTraitType(TestCase):
    """Test applying requests with unknown trait types."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.approver = User.objects.create_user(
            username="approver", email="approver@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            arete=1,
            xp=50,
        )

    def test_unknown_trait_type_returns_error(self):
        """Test that unknown trait type returns an error."""
        xp_request = XPSpendingRequest.objects.create(
            character=self.mage,
            trait_name="Unknown Trait",
            trait_type="unknown_type",
            trait_value=1,
            cost=10,
            approved="Pending",
        )

        service = MageXPSpendingService(self.mage)
        result = service.apply(xp_request, self.approver)

        self.assertFalse(result.success)
        self.assertIn("Unknown trait type", result.error)


class TestApplierInheritance(TestCase):
    """Test that applier inheritance works correctly via metaclass."""

    def test_mage_service_has_human_appliers(self):
        """Test MageXPSpendingService inherits HumanXPSpendingService appliers."""
        human_appliers = [
            "attribute",
            "ability",
            "background",
            "new-background",
            "willpower",
            "meritflaw",
        ]
        for applier_type in human_appliers:
            self.assertIn(
                applier_type,
                MageXPSpendingService._appliers,
                f"Applier '{applier_type}' not inherited by MageXPSpendingService",
            )

    def test_mage_service_has_mage_specific_appliers(self):
        """Test MageXPSpendingService has its own appliers."""
        mage_appliers = [
            "sphere",
            "arete",
            "practice",
            "tenet",
            "remove tenet",
            "resonance",
            "rotes",
        ]
        for applier_type in mage_appliers:
            self.assertIn(
                applier_type,
                MageXPSpendingService._appliers,
                f"Applier '{applier_type}' not found in MageXPSpendingService",
            )

    def test_vampire_service_inherits_appliers(self):
        """Test VampireXPSpendingService inherits appliers correctly."""
        from characters.services.xp_spending import VampireXPSpendingService

        # VtMHuman adds virtue applier
        self.assertIn("virtue", VampireXPSpendingService._appliers)
        # Plus Vampire-specific appliers
        self.assertIn("discipline", VampireXPSpendingService._appliers)
        self.assertIn("morality", VampireXPSpendingService._appliers)

    def test_garou_service_has_werewolf_appliers(self):
        """Test GarouXPSpendingService has werewolf-specific appliers."""
        from characters.services.xp_spending import GarouXPSpendingService

        werewolf_appliers = ["gift", "rite", "rage", "gnosis"]
        for applier_type in werewolf_appliers:
            self.assertIn(
                applier_type,
                GarouXPSpendingService._appliers,
                f"Applier '{applier_type}' not found in GarouXPSpendingService",
            )


class TestAvailableAppliers(TestCase):
    """Test available_appliers property returns correct appliers."""

    def test_mage_available_appliers(self):
        """Test MageXPSpendingService.available_appliers returns all appliers."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        mage = Mage.objects.create(
            name="Test Mage",
            owner=user,
            chronicle=chronicle,
            arete=1,
        )
        service = MageXPSpendingService(mage)
        appliers = service.available_appliers

        # Should include human + mage appliers
        expected = [
            "attribute",
            "ability",
            "background",
            "new-background",
            "willpower",
            "meritflaw",
            "sphere",
            "arete",
            "practice",
            "tenet",
            "remove tenet",
            "resonance",
            "rotes",
        ]
        for app in expected:
            self.assertIn(app, appliers, f"Applier '{app}' not in available_appliers")
