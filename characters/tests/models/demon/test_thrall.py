"""Tests for Thrall model."""

from characters.costs import get_freebie_cost
from characters.models.demon import Demon
from characters.models.demon.pact import Pact
from characters.models.demon.thrall import Thrall
from django.contrib.auth.models import User
from django.test import TestCase


class ThrallModelTests(TestCase):
    """Tests for Thrall model functionality."""

    def setUp(self):
        """Create a test user for thrall ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_default_values(self):
        """Test default values for Thrall fields."""
        self.assertEqual(self.thrall.faith_potential, 1)
        self.assertEqual(self.thrall.daily_faith_offered, 1)
        self.assertEqual(self.thrall.conviction, 1)
        self.assertEqual(self.thrall.courage, 1)
        self.assertEqual(self.thrall.conscience, 1)
        self.assertEqual(self.thrall.background_points, 5)
        self.assertEqual(self.thrall.enhancements, [])

    def test_type_and_gameline(self):
        """Test type and gameline values."""
        self.assertEqual(self.thrall.type, "thrall")
        self.assertEqual(self.thrall.gameline, "dtf")

    def test_freebie_step(self):
        """Test freebie step value."""
        self.assertEqual(self.thrall.freebie_step, 6)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.thrall.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/thrall/{self.thrall.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.thrall.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/thrall/{self.thrall.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = Thrall.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/thrall/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.thrall.get_heading(), "dtf_heading")

    def test_ordering_by_name(self):
        """Thralls should be ordered by name by default."""
        thrall_c = Thrall.objects.create(name="Charlie", owner=self.user)
        thrall_a = Thrall.objects.create(name="Alice", owner=self.user)
        thrall_b = Thrall.objects.create(name="Bob", owner=self.user)

        thralls = list(Thrall.objects.exclude(pk=self.thrall.pk))
        self.assertEqual(thralls[0], thrall_a)
        self.assertEqual(thralls[1], thrall_b)
        self.assertEqual(thralls[2], thrall_c)


class ThrallFaithPotentialTests(TestCase):
    """Tests for Faith Potential-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_add_faith_potential_increases(self):
        """add_faith_potential increases faith potential by 1."""
        initial = self.thrall.faith_potential
        result = self.thrall.add_faith_potential()
        self.assertTrue(result)
        self.assertEqual(self.thrall.faith_potential, initial + 1)

    def test_add_faith_potential_returns_false_at_max(self):
        """add_faith_potential returns False at max (5)."""
        self.thrall.faith_potential = 5
        self.thrall.save()
        result = self.thrall.add_faith_potential()
        self.assertFalse(result)
        self.assertEqual(self.thrall.faith_potential, 5)

    def test_has_faith_potential_true(self):
        """has_faith_potential returns True when >= 1."""
        self.assertTrue(self.thrall.has_faith_potential())

    def test_has_faith_potential_false(self):
        """has_faith_potential returns False when < 1."""
        self.thrall.faith_potential = 0
        self.assertFalse(self.thrall.has_faith_potential())

    def test_calculate_daily_faith_round_up(self):
        """calculate_daily_faith rounds up correctly."""
        self.thrall.faith_potential = 1
        result = self.thrall.calculate_daily_faith()
        self.assertEqual(result, 1)  # (1+1)//2 = 1

        self.thrall.faith_potential = 3
        result = self.thrall.calculate_daily_faith()
        self.assertEqual(result, 2)  # (3+1)//2 = 2

        self.thrall.faith_potential = 5
        result = self.thrall.calculate_daily_faith()
        self.assertEqual(result, 3)  # (5+1)//2 = 3


class ThrallVirtuesTests(TestCase):
    """Tests for virtue-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_has_virtues_false_with_wrong_sum(self):
        """has_virtues returns False when sum isn't 6."""
        self.thrall.conviction = 1
        self.thrall.courage = 1
        self.thrall.conscience = 1
        self.assertFalse(self.thrall.has_virtues())

    def test_has_virtues_true_with_correct_sum(self):
        """has_virtues returns True when sum is 6."""
        self.thrall.conviction = 2
        self.thrall.courage = 2
        self.thrall.conscience = 2
        self.assertTrue(self.thrall.has_virtues())


class ThrallPactTests(TestCase):
    """Tests for pact-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_get_pacts_empty(self):
        """get_pacts returns empty queryset initially."""
        pacts = self.thrall.get_pacts()
        self.assertEqual(pacts.count(), 0)

    def test_get_pacts_returns_pacts(self):
        """get_pacts returns thrall's pacts."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        pacts = self.thrall.get_pacts()
        self.assertEqual(pacts.count(), 1)
        self.assertIn(pact, pacts)

    def test_get_active_pacts(self):
        """get_active_pacts returns only active pacts."""
        pact1 = Pact.objects.create(demon=self.demon, thrall=self.thrall, active=True)
        pact2 = Pact.objects.create(demon=self.demon, thrall=self.thrall, active=False)
        active_pacts = self.thrall.get_active_pacts()
        self.assertEqual(active_pacts.count(), 1)
        self.assertIn(pact1, active_pacts)
        self.assertNotIn(pact2, active_pacts)

    def test_total_pacts_counts_active_only(self):
        """total_pacts counts only active pacts."""
        Pact.objects.create(demon=self.demon, thrall=self.thrall, active=True)
        Pact.objects.create(demon=self.demon, thrall=self.thrall, active=False)
        self.assertEqual(self.thrall.total_pacts(), 1)


class ThrallEnhancementTests(TestCase):
    """Tests for enhancement-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_add_enhancement_adds_new(self):
        """add_enhancement adds a new enhancement."""
        result = self.thrall.add_enhancement("Enhanced Strength")
        self.assertTrue(result)
        self.assertIn("Enhanced Strength", self.thrall.enhancements)

    def test_add_enhancement_returns_false_duplicate(self):
        """add_enhancement returns False for duplicate."""
        self.thrall.enhancements = ["Enhanced Strength"]
        self.thrall.save()
        result = self.thrall.add_enhancement("Enhanced Strength")
        self.assertFalse(result)

    def test_remove_enhancement_removes(self):
        """remove_enhancement removes an enhancement."""
        self.thrall.enhancements = ["Enhanced Strength", "Night Vision"]
        self.thrall.save()
        result = self.thrall.remove_enhancement("Enhanced Strength")
        self.assertTrue(result)
        self.assertNotIn("Enhanced Strength", self.thrall.enhancements)
        self.assertIn("Night Vision", self.thrall.enhancements)

    def test_remove_enhancement_returns_false_not_found(self):
        """remove_enhancement returns False if not found."""
        result = self.thrall.remove_enhancement("Not Present")
        self.assertFalse(result)


class ThrallXPTests(TestCase):
    """Tests for XP-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user, xp=100)

    def test_xp_frequencies_returns_dict(self):
        """xp_frequencies returns correct dictionary."""
        freq = self.thrall.xp_frequencies()
        self.assertIn("attribute", freq)
        self.assertIn("ability", freq)
        self.assertIn("background", freq)
        self.assertIn("willpower", freq)
        self.assertIn("faith_potential", freq)
        self.assertIn("virtue", freq)


class ThrallFreebieTests(TestCase):
    """Tests for freebie-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user, freebies=50)

    def test_freebie_frequencies_returns_dict(self):
        """freebie_frequencies returns correct dictionary."""
        freq = self.thrall.freebie_frequencies()
        self.assertIn("attribute", freq)
        self.assertIn("ability", freq)
        self.assertIn("background", freq)
        self.assertIn("willpower", freq)
        self.assertIn("meritflaw", freq)
        self.assertIn("faith_potential", freq)
        self.assertIn("virtue", freq)

    def test_freebie_costs_returns_dict(self):
        """Test centralized freebie costs for thrall traits."""
        self.assertEqual(get_freebie_cost("faith_potential"), 7)
        self.assertEqual(get_freebie_cost("virtue"), 2)

    def test_freebie_cost_faith_potential(self):
        """freebie_cost returns correct cost for faith_potential."""
        self.assertEqual(get_freebie_cost("faith_potential"), 7)

    def test_freebie_cost_virtue(self):
        """freebie_cost returns correct cost for virtue."""
        self.assertEqual(get_freebie_cost("virtue"), 2)

    def test_spend_freebies_faith_potential(self):
        """spend_freebies increases faith_potential and deducts freebies."""
        initial_fp = self.thrall.faith_potential
        initial_freebies = self.thrall.freebies
        result = self.thrall.spend_freebies("faith_potential")
        self.assertTrue(result)
        self.assertEqual(self.thrall.faith_potential, initial_fp + 1)
        self.assertEqual(self.thrall.freebies, initial_freebies - 7)

    def test_spend_freebies_faith_potential_insufficient(self):
        """spend_freebies returns False with insufficient freebies."""
        self.thrall.freebies = 1
        self.thrall.save()
        result = self.thrall.spend_freebies("faith_potential")
        self.assertFalse(result)

    def test_spend_freebies_virtue(self):
        """spend_freebies increases virtue and deducts freebies."""
        initial_conviction = self.thrall.conviction
        result = self.thrall.spend_freebies("conviction")
        self.assertTrue(result)
        self.assertEqual(self.thrall.conviction, initial_conviction + 1)


class ThrallMasterTests(TestCase):
    """Tests for master relationship."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_master_can_be_set(self):
        """Master demon can be set."""
        self.thrall.master = self.demon
        self.thrall.save()
        self.assertEqual(self.thrall.master, self.demon)

    def test_master_can_be_null(self):
        """Master demon can be null."""
        self.assertIsNone(self.thrall.master)

    def test_primary_thralls_related_name(self):
        """Test primary_thralls related name on Demon."""
        self.thrall.master = self.demon
        self.thrall.save()
        self.assertIn(self.thrall, self.demon.primary_thralls.all())
