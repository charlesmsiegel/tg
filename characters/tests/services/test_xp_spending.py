"""Tests for XP spending service."""

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.mage import Mage, PracticeRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from characters.services.xp_spending import MageXPSpendingService, XPSpendResult
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from game.models import Chronicle, ObjectType


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
