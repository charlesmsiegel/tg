"""Tests for Demon model."""

from characters.costs import get_freebie_cost
from characters.models.demon import Demon
from characters.models.demon.apocalyptic_form import (
    ApocalypticForm,
    ApocalypticFormTrait,
)
from characters.models.demon.demon import LoreRating
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.pact import Pact
from characters.models.demon.ritual import Ritual
from characters.models.demon.thrall import Thrall
from characters.models.demon.visage import Visage
from django.contrib.auth.models import User
from django.test import TestCase


class DemonModelTests(TestCase):
    """Tests for Demon model functionality."""

    def setUp(self):
        """Create a test user for demon ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_name_field_is_primary_identifier(self):
        """The name field should be the primary identifier (host name)."""
        demon = Demon.objects.create(
            name="John Smith",
            celestial_name="Hasmed",
            owner=self.user,
        )
        # __str__ uses the inherited name field
        self.assertEqual(str(demon), "John Smith")

    def test_celestial_name_is_separate(self):
        """Celestial name is stored separately from the name (host identity)."""
        demon = Demon.objects.create(
            name="Jane Doe",
            celestial_name="Ahrimal",
            owner=self.user,
        )
        self.assertEqual(demon.name, "Jane Doe")
        self.assertEqual(demon.celestial_name, "Ahrimal")

    def test_ordering_by_name(self):
        """Demons should be ordered by name by default."""
        # Create demons out of alphabetical order
        demon_c = Demon.objects.create(name="Charlie Brown", owner=self.user)
        demon_a = Demon.objects.create(name="Alice Smith", owner=self.user)
        demon_b = Demon.objects.create(name="Bob Jones", owner=self.user)

        # Query without explicit ordering - should use Meta.ordering
        demons = list(Demon.objects.exclude(pk=self.demon.pk))

        # Should be ordered by name alphabetically
        self.assertEqual(demons[0], demon_a)  # Alice
        self.assertEqual(demons[1], demon_b)  # Bob
        self.assertEqual(demons[2], demon_c)  # Charlie

    def test_host_name_field_removed(self):
        """The host_name field should no longer exist."""
        demon = Demon.objects.create(name="Test Demon 2", owner=self.user)
        self.assertFalse(hasattr(demon, "host_name"))

    def test_default_values(self):
        """Test default values for Demon fields."""
        self.assertEqual(self.demon.faith, 3)
        self.assertEqual(self.demon.temporary_faith, 3)
        self.assertEqual(self.demon.torment, 3)
        self.assertEqual(self.demon.temporary_torment, 0)
        self.assertEqual(self.demon.conviction, 1)
        self.assertEqual(self.demon.courage, 1)
        self.assertEqual(self.demon.conscience, 1)
        self.assertEqual(self.demon.days_until_consumption, 30)
        self.assertEqual(self.demon.age_of_fall, 0)
        self.assertEqual(self.demon.background_points, 5)
        self.assertEqual(self.demon.apocalyptic_form_points, 16)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.demon.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/demon/{self.demon.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.demon.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/demon/{self.demon.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = Demon.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/demon/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.demon.get_heading(), "dtf_heading")


class DemonHouseTests(TestCase):
    """Tests for house-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.house = DemonHouse.objects.create(
            name="Devils",
            celestial_name="Namaru",
            starting_torment=4,
        )

    def test_has_house_returns_false_initially(self):
        """has_house returns False when no house set."""
        self.assertFalse(self.demon.has_house())

    def test_has_house_returns_true_after_set(self):
        """has_house returns True after setting house."""
        self.demon.house = self.house
        self.demon.save()
        self.assertTrue(self.demon.has_house())

    def test_set_house_sets_house_and_torment(self):
        """set_house sets house and starting torment."""
        result = self.demon.set_house(self.house)
        self.assertTrue(result)
        self.assertEqual(self.demon.house, self.house)
        self.assertEqual(self.demon.torment, 4)


class DemonFactionTests(TestCase):
    """Tests for faction-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.faction = DemonFaction.objects.create(name="Cryptics")

    def test_has_faction_returns_false_initially(self):
        """has_faction returns False when no faction set."""
        self.assertFalse(self.demon.has_faction())

    def test_has_faction_returns_true_after_set(self):
        """has_faction returns True after setting faction."""
        self.demon.faction = self.faction
        self.demon.save()
        self.assertTrue(self.demon.has_faction())

    def test_set_faction_sets_faction(self):
        """set_faction sets the faction."""
        result = self.demon.set_faction(self.faction)
        self.assertTrue(result)
        self.assertEqual(self.demon.faction, self.faction)


class DemonVisageTests(TestCase):
    """Tests for visage-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.visage = Visage.objects.create(name="Bel")

    def test_has_visage_returns_false_initially(self):
        """has_visage returns False when no visage set."""
        self.assertFalse(self.demon.has_visage())

    def test_has_visage_returns_true_after_set(self):
        """has_visage returns True after setting visage."""
        self.demon.visage = self.visage
        self.demon.save()
        self.assertTrue(self.demon.has_visage())

    def test_set_visage_sets_visage(self):
        """set_visage sets the visage."""
        result = self.demon.set_visage(self.visage)
        self.assertTrue(result)
        self.assertEqual(self.demon.visage, self.visage)


class DemonFaithTests(TestCase):
    """Tests for Faith-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_add_faith_increases_faith(self):
        """add_faith increases faith by 1."""
        initial_faith = self.demon.faith
        result = self.demon.add_faith()
        self.assertTrue(result)
        self.assertEqual(self.demon.faith, initial_faith + 1)

    def test_add_faith_returns_false_at_max(self):
        """add_faith returns False when faith is at 10."""
        self.demon.faith = 10
        self.demon.save()
        result = self.demon.add_faith()
        self.assertFalse(result)
        self.assertEqual(self.demon.faith, 10)


class DemonTormentTests(TestCase):
    """Tests for Torment-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_add_torment_increases_torment(self):
        """add_torment increases torment by 1."""
        initial_torment = self.demon.torment
        result = self.demon.add_torment()
        self.assertTrue(result)
        self.assertEqual(self.demon.torment, initial_torment + 1)

    def test_add_torment_returns_false_at_max(self):
        """add_torment returns False when torment is at 10."""
        self.demon.torment = 10
        self.demon.save()
        result = self.demon.add_torment()
        self.assertFalse(result)
        self.assertEqual(self.demon.torment, 10)

    def test_reduce_torment_decreases_torment(self):
        """reduce_torment decreases torment by 1."""
        self.demon.torment = 5
        self.demon.save()
        result = self.demon.reduce_torment()
        self.assertTrue(result)
        self.assertEqual(self.demon.torment, 4)

    def test_reduce_torment_returns_false_at_min(self):
        """reduce_torment returns False when torment is at 0."""
        self.demon.torment = 0
        self.demon.save()
        result = self.demon.reduce_torment()
        self.assertFalse(result)
        self.assertEqual(self.demon.torment, 0)


class DemonVirtuesTests(TestCase):
    """Tests for virtue-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_has_virtues_false_with_wrong_sum(self):
        """has_virtues returns False when sum isn't 6."""
        self.demon.conviction = 1
        self.demon.courage = 1
        self.demon.conscience = 1
        self.assertFalse(self.demon.has_virtues())

    def test_has_virtues_true_with_correct_sum(self):
        """has_virtues returns True when sum is 6."""
        self.demon.conviction = 2
        self.demon.courage = 2
        self.demon.conscience = 2
        self.assertTrue(self.demon.has_virtues())

    def test_has_virtues_true_with_uneven_distribution(self):
        """has_virtues returns True with uneven distribution summing to 6."""
        self.demon.conviction = 3
        self.demon.courage = 2
        self.demon.conscience = 1
        self.assertTrue(self.demon.has_virtues())


class DemonLoreTests(TestCase):
    """Tests for lore-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_has_lores_false_initially(self):
        """has_lores returns False with no lores."""
        self.assertFalse(self.demon.has_lores())

    def test_has_lores_false_under_three(self):
        """has_lores returns False with less than 3 dots."""
        self.demon.lore_of_flame = 2
        self.demon.save()
        self.assertFalse(self.demon.has_lores())

    def test_has_lores_true_at_three(self):
        """has_lores returns True with 3 dots."""
        self.demon.lore_of_flame = 3
        self.demon.save()
        self.assertTrue(self.demon.has_lores())

    def test_has_lores_true_over_three(self):
        """has_lores returns True with more than 3 dots."""
        self.demon.lore_of_flame = 2
        self.demon.lore_of_the_fundament = 2
        self.demon.save()
        self.assertTrue(self.demon.has_lores())


class DemonApocalypticFormTests(TestCase):
    """Tests for apocalyptic form-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.form = ApocalypticForm.objects.create(name="Test Form")
        # Create traits
        self.low_trait1 = ApocalypticFormTrait.objects.create(name="Wings", cost=2)
        self.low_trait2 = ApocalypticFormTrait.objects.create(name="Claws", cost=2)
        self.low_trait3 = ApocalypticFormTrait.objects.create(name="Armor", cost=2)
        self.low_trait4 = ApocalypticFormTrait.objects.create(name="Speed", cost=2)
        self.high_trait1 = ApocalypticFormTrait.objects.create(name="Fire Breath", cost=2)
        self.high_trait2 = ApocalypticFormTrait.objects.create(name="Shadow Form", cost=2)
        self.high_trait3 = ApocalypticFormTrait.objects.create(name="Terror", cost=2)
        self.high_trait4 = ApocalypticFormTrait.objects.create(name="Poison", cost=2)

    def test_has_apocalyptic_form_false_initially(self):
        """has_apocalyptic_form returns False when no form."""
        self.assertFalse(self.demon.has_apocalyptic_form())

    def test_has_apocalyptic_form_false_invalid_form(self):
        """has_apocalyptic_form returns False with invalid form."""
        self.demon.apocalyptic_form = self.form
        self.demon.save()
        # Form has no traits, so invalid
        self.assertFalse(self.demon.has_apocalyptic_form())

    def test_has_apocalyptic_form_true_valid_form(self):
        """has_apocalyptic_form returns True with valid form."""
        # Add 4 low and 4 high traits
        self.form.low_torment_traits.add(
            self.low_trait1, self.low_trait2, self.low_trait3, self.low_trait4
        )
        self.form.high_torment_traits.add(
            self.high_trait1, self.high_trait2, self.high_trait3, self.high_trait4
        )
        self.demon.apocalyptic_form = self.form
        self.demon.save()
        self.assertTrue(self.demon.has_apocalyptic_form())

    def test_get_low_torment_traits_with_no_form(self):
        """get_low_torment_traits returns empty queryset with no form."""
        traits = self.demon.get_low_torment_traits()
        self.assertEqual(traits.count(), 0)

    def test_get_low_torment_traits_with_form(self):
        """get_low_torment_traits returns traits from form."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)
        self.demon.apocalyptic_form = self.form
        self.demon.save()
        traits = self.demon.get_low_torment_traits()
        self.assertEqual(traits.count(), 2)

    def test_get_high_torment_traits_with_no_form(self):
        """get_high_torment_traits returns empty queryset with no form."""
        traits = self.demon.get_high_torment_traits()
        self.assertEqual(traits.count(), 0)

    def test_get_high_torment_traits_with_form(self):
        """get_high_torment_traits returns traits from form."""
        self.form.high_torment_traits.add(self.high_trait1, self.high_trait2)
        self.demon.apocalyptic_form = self.form
        self.demon.save()
        traits = self.demon.get_high_torment_traits()
        self.assertEqual(traits.count(), 2)

    def test_apocalyptic_form_counts_with_no_form(self):
        """Count methods return 0 with no form."""
        self.assertEqual(self.demon.apocalyptic_form_low_torment_count(), 0)
        self.assertEqual(self.demon.apocalyptic_form_high_torment_count(), 0)

    def test_apocalyptic_form_counts_with_form(self):
        """Count methods return correct counts."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)
        self.form.high_torment_traits.add(self.high_trait1)
        self.demon.apocalyptic_form = self.form
        self.demon.save()
        self.assertEqual(self.demon.apocalyptic_form_low_torment_count(), 2)
        self.assertEqual(self.demon.apocalyptic_form_high_torment_count(), 1)

    def test_apocalyptic_form_points_spent_with_no_form(self):
        """Points spent returns 0 with no form."""
        self.assertEqual(self.demon.apocalyptic_form_points_spent(), 0)

    def test_apocalyptic_form_points_spent_with_form(self):
        """Points spent returns sum of trait costs."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)  # 4 points
        self.form.high_torment_traits.add(self.high_trait1)  # 2 points
        self.demon.apocalyptic_form = self.form
        self.demon.save()
        self.assertEqual(self.demon.apocalyptic_form_points_spent(), 6)

    def test_apocalyptic_form_points_remaining_with_no_form(self):
        """Points remaining returns 16 with no form."""
        self.assertEqual(self.demon.apocalyptic_form_points_remaining(), 16)

    def test_apocalyptic_form_points_remaining_with_form(self):
        """Points remaining calculated correctly."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)  # 4 points
        self.form.high_torment_traits.add(self.high_trait1)  # 2 points
        self.demon.apocalyptic_form = self.form
        self.demon.save()
        self.assertEqual(self.demon.apocalyptic_form_points_remaining(), 10)


class DemonRitualTests(TestCase):
    """Tests for ritual-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.house = DemonHouse.objects.create(
            name="Devils",
            celestial_name="Namaru",
            starting_torment=4,
        )
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user, house=self.house)
        self.lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore.houses.add(self.house)
        self.ritual = Ritual.objects.create(
            name="Binding of Fire",
            house=self.house,
            primary_lore=self.lore,
            primary_lore_rating=2,
        )

    def test_get_rituals_empty_initially(self):
        """get_rituals returns empty queryset initially."""
        rituals = self.demon.get_rituals()
        self.assertEqual(rituals.count(), 0)

    def test_get_rituals_returns_rituals(self):
        """get_rituals returns known rituals."""
        self.demon.rituals.add(self.ritual)
        rituals = self.demon.get_rituals()
        self.assertEqual(rituals.count(), 1)
        self.assertIn(self.ritual, rituals)

    def test_knows_ritual_false_initially(self):
        """knows_ritual returns False initially."""
        self.assertFalse(self.demon.knows_ritual(self.ritual))

    def test_knows_ritual_true_after_learning(self):
        """knows_ritual returns True after adding ritual."""
        self.demon.rituals.add(self.ritual)
        self.assertTrue(self.demon.knows_ritual(self.ritual))

    def test_add_ritual_adds_ritual(self):
        """add_ritual adds a ritual."""
        result = self.demon.add_ritual(self.ritual)
        self.assertTrue(result)
        self.assertIn(self.ritual, self.demon.rituals.all())

    def test_add_ritual_returns_false_for_duplicate(self):
        """add_ritual returns False if already known."""
        self.demon.rituals.add(self.ritual)
        result = self.demon.add_ritual(self.ritual)
        self.assertFalse(result)

    def test_remove_ritual_removes_ritual(self):
        """remove_ritual removes a ritual."""
        self.demon.rituals.add(self.ritual)
        result = self.demon.remove_ritual(self.ritual)
        self.assertTrue(result)
        self.assertNotIn(self.ritual, self.demon.rituals.all())

    def test_remove_ritual_returns_false_if_not_known(self):
        """remove_ritual returns False if not known."""
        result = self.demon.remove_ritual(self.ritual)
        self.assertFalse(result)

    def test_get_available_rituals_with_no_house(self):
        """get_available_rituals returns empty with no house."""
        self.demon.house = None
        self.demon.save()
        rituals = self.demon.get_available_rituals()
        self.assertEqual(rituals.count(), 0)

    def test_get_available_rituals_with_insufficient_lore(self):
        """get_available_rituals excludes rituals with insufficient lore."""
        # Demon has no flame lore, ritual requires 2
        rituals = self.demon.get_available_rituals()
        self.assertEqual(rituals.count(), 0)

    def test_get_available_rituals_with_sufficient_lore(self):
        """get_available_rituals includes rituals with sufficient lore."""
        self.demon.lore_of_flame = 3
        self.demon.save()
        rituals = self.demon.get_available_rituals()
        self.assertEqual(rituals.count(), 1)
        self.assertIn(self.ritual, rituals)

    def test_get_available_rituals_excludes_known(self):
        """get_available_rituals excludes already known rituals."""
        self.demon.lore_of_flame = 3
        self.demon.rituals.add(self.ritual)
        self.demon.save()
        rituals = self.demon.get_available_rituals()
        self.assertEqual(rituals.count(), 0)


class DemonPactTests(TestCase):
    """Tests for pact-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_get_pacts_empty_initially(self):
        """get_pacts returns empty queryset initially."""
        pacts = self.demon.get_pacts()
        self.assertEqual(pacts.count(), 0)

    def test_get_pacts_returns_pacts(self):
        """get_pacts returns demon's pacts."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        pacts = self.demon.get_pacts()
        self.assertEqual(pacts.count(), 1)
        self.assertIn(pact, pacts)

    def test_add_pact_creates_pact(self):
        """add_pact creates a new pact."""
        pact = self.demon.add_pact(
            thrall=self.thrall,
            terms="Power for service",
            faith_payment=2,
            enhancements=["Enhanced Strength"],
        )
        self.assertIsNotNone(pact)
        self.assertEqual(pact.demon, self.demon)
        self.assertEqual(pact.thrall, self.thrall)
        self.assertEqual(pact.terms, "Power for service")
        self.assertEqual(pact.faith_payment, 2)
        self.assertEqual(pact.enhancements, ["Enhanced Strength"])

    def test_add_pact_with_defaults(self):
        """add_pact creates pact with default values."""
        pact = self.demon.add_pact(thrall=self.thrall)
        self.assertEqual(pact.terms, "")
        self.assertEqual(pact.faith_payment, 0)
        self.assertEqual(pact.enhancements, [])

    def test_total_pacts_counts_active_only(self):
        """total_pacts counts only active pacts."""
        pact1 = Pact.objects.create(demon=self.demon, thrall=self.thrall, active=True)
        pact2 = Pact.objects.create(demon=self.demon, thrall=self.thrall, active=False)
        self.assertEqual(self.demon.total_pacts(), 1)


class DemonHistoryTests(TestCase):
    """Tests for history-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_has_demon_history_false_initially(self):
        """has_demon_history returns False with no history."""
        self.assertFalse(self.demon.has_demon_history())

    def test_has_demon_history_false_missing_celestial_name(self):
        """has_demon_history returns False without celestial name."""
        self.demon.age_of_fall = 5
        self.demon.save()
        self.assertFalse(self.demon.has_demon_history())

    def test_has_demon_history_false_missing_age(self):
        """has_demon_history returns False without age_of_fall."""
        self.demon.celestial_name = "Hasmed"
        self.demon.save()
        self.assertFalse(self.demon.has_demon_history())

    def test_has_demon_history_true_with_both(self):
        """has_demon_history returns True with both fields."""
        self.demon.celestial_name = "Hasmed"
        self.demon.age_of_fall = 5
        self.demon.save()
        self.assertTrue(self.demon.has_demon_history())


class DemonXPTests(TestCase):
    """Tests for XP-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user, xp=100)
        self.demon.house = self.house
        self.lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore.houses.add(self.house)
        self.demon.save()

    def test_xp_frequencies_returns_dict(self):
        """xp_frequencies returns correct dictionary."""
        freq = self.demon.xp_frequencies()
        self.assertIn("attribute", freq)
        self.assertIn("ability", freq)
        self.assertIn("background", freq)
        self.assertIn("willpower", freq)
        self.assertIn("lore", freq)
        self.assertIn("faith", freq)
        self.assertIn("virtue", freq)


class DemonFreebieTests(TestCase):
    """Tests for freebie-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user, freebies=50)
        self.demon.house = self.house
        self.lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore.houses.add(self.house)
        self.demon.save()

    def test_freebie_frequencies_returns_dict(self):
        """freebie_frequencies returns correct dictionary."""
        freq = self.demon.freebie_frequencies()
        self.assertIn("attribute", freq)
        self.assertIn("ability", freq)
        self.assertIn("background", freq)
        self.assertIn("willpower", freq)
        self.assertIn("meritflaw", freq)
        self.assertIn("lore", freq)
        self.assertIn("faith", freq)
        self.assertIn("virtue", freq)
        self.assertIn("temporary_faith", freq)

    def test_freebie_costs_returns_dict(self):
        """Test centralized freebie costs for demon traits."""
        self.assertEqual(get_freebie_cost("lore"), 7)
        self.assertEqual(get_freebie_cost("faith"), 6)
        self.assertEqual(get_freebie_cost("virtue"), 2)
        self.assertEqual(get_freebie_cost("temporary_faith"), 1)

    def test_freebie_cost_lore(self):
        """freebie_cost returns correct cost for lore."""
        self.assertEqual(get_freebie_cost("lore"), 7)

    def test_freebie_cost_faith(self):
        """freebie_cost returns correct cost for faith."""
        self.assertEqual(get_freebie_cost("faith"), 6)

    def test_freebie_cost_virtue(self):
        """freebie_cost returns correct cost for virtue."""
        self.assertEqual(get_freebie_cost("virtue"), 2)

    def test_freebie_cost_temporary_faith(self):
        """freebie_cost returns correct cost for temporary_faith."""
        self.assertEqual(get_freebie_cost("temporary_faith"), 1)

    def test_spend_freebies_faith(self):
        """spend_freebies increases faith and deducts freebies."""
        initial_faith = self.demon.faith
        initial_freebies = self.demon.freebies
        result = self.demon.spend_freebies("faith")
        self.assertTrue(result)
        self.assertEqual(self.demon.faith, initial_faith + 1)
        self.assertEqual(self.demon.freebies, initial_freebies - 6)

    def test_spend_freebies_faith_insufficient_freebies(self):
        """spend_freebies returns False with insufficient freebies."""
        self.demon.freebies = 1
        self.demon.save()
        result = self.demon.spend_freebies("faith")
        self.assertFalse(result)

    def test_spend_freebies_temporary_faith(self):
        """spend_freebies increases temporary_faith and deducts freebies."""
        initial_tf = self.demon.temporary_faith
        result = self.demon.spend_freebies("temporary_faith")
        self.assertTrue(result)
        self.assertEqual(self.demon.temporary_faith, initial_tf + 1)

    def test_spend_freebies_virtue(self):
        """spend_freebies increases virtue and deducts freebies."""
        initial_conviction = self.demon.conviction
        result = self.demon.spend_freebies("conviction")
        self.assertTrue(result)
        self.assertEqual(self.demon.conviction, initial_conviction + 1)


class LoreRatingDeleteBehaviorTests(TestCase):
    """Tests for LoreRating SET_NULL behavior when parent objects are deleted."""

    def setUp(self):
        """Create test user, demon, lore, and rating."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.lore = Lore.objects.create(
            name="Lore of the Fundament",
            property_name="fundament",
            description="Test description",
        )
        self.rating = LoreRating.objects.create(demon=self.demon, lore=self.lore, rating=3)

    def test_deleting_demon_sets_null_preserves_rating(self):
        """Deleting a Demon should set demon FK to NULL, not delete LoreRating."""
        rating_id = self.rating.id
        self.demon.delete()

        # LoreRating should still exist
        self.assertTrue(LoreRating.objects.filter(id=rating_id).exists())

        # demon FK should be NULL
        rating = LoreRating.objects.get(id=rating_id)
        self.assertIsNone(rating.demon)
        self.assertEqual(rating.lore, self.lore)
        self.assertEqual(rating.rating, 3)

    def test_deleting_lore_sets_null_preserves_rating(self):
        """Deleting a Lore should set lore FK to NULL, not delete LoreRating."""
        rating_id = self.rating.id
        self.lore.delete()

        # LoreRating should still exist
        self.assertTrue(LoreRating.objects.filter(id=rating_id).exists())

        # lore FK should be NULL
        rating = LoreRating.objects.get(id=rating_id)
        self.assertIsNone(rating.lore)
        self.assertEqual(rating.demon, self.demon)
        self.assertEqual(rating.rating, 3)

    def test_related_name_lore_ratings_on_demon(self):
        """Demon should have lore_ratings related manager."""
        self.assertIn(self.rating, self.demon.lore_ratings.all())

    def test_related_name_demon_ratings_on_lore(self):
        """Lore should have demon_ratings related manager."""
        self.assertIn(self.rating, self.lore.demon_ratings.all())

    def test_lore_rating_str(self):
        """Test LoreRating __str__ method."""
        self.assertEqual(str(self.rating), "Test Demon: Lore of the Fundament: 3")

    def test_lore_rating_str_no_demon(self):
        """Test LoreRating __str__ with no demon."""
        self.rating.demon = None
        self.rating.save()
        self.assertEqual(str(self.rating), "No Demon: Lore of the Fundament: 3")

    def test_lore_rating_str_no_lore(self):
        """Test LoreRating __str__ with no lore."""
        self.rating.lore = None
        self.rating.save()
        self.assertEqual(str(self.rating), "Test Demon: No Lore: 3")


class DemonRitualKnowledgeXPCostTests(TestCase):
    """Tests for ritual knowledge XP cost calculation."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_ritual_knowledge_xp_cost_with_no_background(self):
        """ritual_knowledge_xp_cost returns 0 with no background."""
        cost = self.demon.ritual_knowledge_xp_cost()
        self.assertEqual(cost, 0)
