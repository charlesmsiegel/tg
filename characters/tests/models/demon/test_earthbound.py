"""Tests for Earthbound model."""

from characters.models.demon.apocalyptic_form import (
    ApocalypticForm,
    ApocalypticFormTrait,
)
from characters.models.demon.earthbound import Earthbound
from characters.models.demon.house import DemonHouse
from characters.models.demon.visage import Visage
from django.contrib.auth.models import User
from django.test import TestCase


class EarthboundModelTests(TestCase):
    """Tests for Earthbound model functionality."""

    def setUp(self):
        """Create a test user for earthbound ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)

    def test_type(self):
        """Test type value."""
        self.assertEqual(self.earthbound.type, "earthbound")

    def test_freebie_step(self):
        """Test freebie step value."""
        self.assertEqual(self.earthbound.freebie_step, 7)

    def test_default_values(self):
        """Test default values for Earthbound fields."""
        self.assertEqual(self.earthbound.faith, 3)
        self.assertEqual(self.earthbound.temporary_faith, 10)
        self.assertEqual(self.earthbound.max_faith, 10)
        self.assertEqual(self.earthbound.torment, 6)
        self.assertEqual(self.earthbound.temporary_torment, 0)
        self.assertEqual(self.earthbound.conviction, 1)
        self.assertEqual(self.earthbound.courage, 1)
        self.assertEqual(self.earthbound.conscience, 1)
        self.assertEqual(self.earthbound.urge_flesh, 1)
        self.assertEqual(self.earthbound.urge_thought, 1)
        self.assertEqual(self.earthbound.urge_emotion, 1)
        self.assertEqual(self.earthbound.reliquary_type, "perfect")
        self.assertEqual(self.earthbound.reliquary_max_health, 10)
        self.assertEqual(self.earthbound.reliquary_current_health, 10)
        self.assertEqual(self.earthbound.reliquary_soak, 0)
        self.assertTrue(self.earthbound.can_manifest)
        self.assertEqual(self.earthbound.manifestation_range, 0)
        self.assertEqual(self.earthbound.mastery_rating, 0)
        self.assertEqual(self.earthbound.known_celestial_names, [])
        self.assertEqual(self.earthbound.known_true_names, [])

    def test_earthbound_specific_abilities_default(self):
        """Test Earthbound-specific abilities default to 0."""
        self.assertEqual(self.earthbound.indoctrination, 0)
        self.assertEqual(self.earthbound.recall, 0)
        self.assertEqual(self.earthbound.tactics, 0)
        self.assertEqual(self.earthbound.torture, 0)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.earthbound.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/earthbound/{self.earthbound.pk}/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.earthbound.get_heading(), "dtf_heading")

    def test_verbose_name(self):
        """Test verbose names."""
        self.assertEqual(Earthbound._meta.verbose_name, "Earthbound")
        self.assertEqual(Earthbound._meta.verbose_name_plural, "Earthbound")


class EarthboundReliquaryTypeTests(TestCase):
    """Tests for reliquary type choices."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)

    def test_perfect_reliquary(self):
        """Test perfect reliquary type."""
        self.earthbound.reliquary_type = "perfect"
        self.earthbound.save()
        self.assertEqual(self.earthbound.reliquary_type, "perfect")

    def test_improvised_reliquary(self):
        """Test improvised reliquary type."""
        self.earthbound.reliquary_type = "improvised"
        self.earthbound.save()
        self.assertEqual(self.earthbound.reliquary_type, "improvised")

    def test_location_reliquary(self):
        """Test location reliquary type."""
        self.earthbound.reliquary_type = "location"
        self.earthbound.save()
        self.assertEqual(self.earthbound.reliquary_type, "location")


class EarthboundFinalDamnationTests(TestCase):
    """Tests for Final Damnation (Torment 10) method."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)

    def test_is_final_damnation_false(self):
        """is_final_damnation returns False when torment < 10."""
        self.earthbound.torment = 9
        self.assertFalse(self.earthbound.is_final_damnation())

    def test_is_final_damnation_true_at_10(self):
        """is_final_damnation returns True when torment = 10."""
        self.earthbound.torment = 10
        self.assertTrue(self.earthbound.is_final_damnation())


class EarthboundFaithPerManifestationTests(TestCase):
    """Tests for Faith cost per manifestation turn."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)

    def test_improvised_costs_1(self):
        """Improvised reliquary costs 1 Faith per turn."""
        self.earthbound.reliquary_type = "improvised"
        self.earthbound.save()
        self.assertEqual(self.earthbound.get_faith_per_manifestation_turn(), 1)

    def test_perfect_costs_2(self):
        """Perfect reliquary costs 2 Faith per turn."""
        self.earthbound.reliquary_type = "perfect"
        self.earthbound.save()
        self.assertEqual(self.earthbound.get_faith_per_manifestation_turn(), 2)

    def test_location_costs_2(self):
        """Location reliquary costs 2 Faith per turn."""
        self.earthbound.reliquary_type = "location"
        self.earthbound.save()
        self.assertEqual(self.earthbound.get_faith_per_manifestation_turn(), 2)


class EarthboundMaxFaithTests(TestCase):
    """Tests for max Faith from Hoard background."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)

    def test_get_max_faith_from_hoard(self):
        """get_max_faith_from_hoard returns stored value."""
        self.earthbound.max_faith = 25
        self.earthbound.save()
        self.assertEqual(self.earthbound.get_max_faith_from_hoard(), 25)

    def test_default_max_faith(self):
        """Default max_faith is 10."""
        self.assertEqual(self.earthbound.get_max_faith_from_hoard(), 10)


class EarthboundReliquaryHealthTests(TestCase):
    """Tests for reliquary health calculations."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)

    def test_calculate_health_perfect(self):
        """Perfect reliquary health = faith."""
        self.earthbound.reliquary_type = "perfect"
        self.earthbound.faith = 5
        self.earthbound.save()
        self.assertEqual(self.earthbound.calculate_reliquary_health(), 5)

    def test_calculate_health_improvised(self):
        """Improvised reliquary health = faith."""
        self.earthbound.reliquary_type = "improvised"
        self.earthbound.faith = 4
        self.earthbound.save()
        self.assertEqual(self.earthbound.calculate_reliquary_health(), 4)

    def test_calculate_health_location(self):
        """Location reliquary health = (faith + willpower) * 2."""
        self.earthbound.reliquary_type = "location"
        self.earthbound.faith = 5
        self.earthbound.willpower = 3
        self.earthbound.save()
        self.assertEqual(self.earthbound.calculate_reliquary_health(), 16)  # (5+3)*2


class EarthboundRegenerationTests(TestCase):
    """Tests for reliquary regeneration."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)

    def test_can_regenerate_with_faith_and_damage(self):
        """can_regenerate_reliquary True with faith and damage."""
        self.earthbound.temporary_faith = 5
        self.earthbound.reliquary_current_health = 5
        self.earthbound.reliquary_max_health = 10
        self.assertTrue(self.earthbound.can_regenerate_reliquary())

    def test_cannot_regenerate_no_faith(self):
        """can_regenerate_reliquary False with no faith."""
        self.earthbound.temporary_faith = 0
        self.earthbound.reliquary_current_health = 5
        self.earthbound.reliquary_max_health = 10
        self.assertFalse(self.earthbound.can_regenerate_reliquary())

    def test_cannot_regenerate_full_health(self):
        """can_regenerate_reliquary False at full health."""
        self.earthbound.temporary_faith = 5
        self.earthbound.reliquary_current_health = 10
        self.earthbound.reliquary_max_health = 10
        self.assertFalse(self.earthbound.can_regenerate_reliquary())


class EarthboundApocalypticFormTests(TestCase):
    """Tests for apocalyptic form-related methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)
        self.form = ApocalypticForm.objects.create(name="Test Form")
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
        self.assertFalse(self.earthbound.has_apocalyptic_form())

    def test_has_apocalyptic_form_false_invalid(self):
        """has_apocalyptic_form returns False with invalid form."""
        self.earthbound.apocalyptic_form = self.form
        self.earthbound.save()
        self.assertFalse(self.earthbound.has_apocalyptic_form())

    def test_has_apocalyptic_form_true_valid(self):
        """has_apocalyptic_form returns True with valid form."""
        self.form.low_torment_traits.add(
            self.low_trait1, self.low_trait2, self.low_trait3, self.low_trait4
        )
        self.form.high_torment_traits.add(
            self.high_trait1, self.high_trait2, self.high_trait3, self.high_trait4
        )
        self.earthbound.apocalyptic_form = self.form
        self.earthbound.save()
        self.assertTrue(self.earthbound.has_apocalyptic_form())

    def test_get_low_torment_traits_no_form(self):
        """get_low_torment_traits returns empty queryset with no form."""
        traits = self.earthbound.get_low_torment_traits()
        self.assertEqual(traits.count(), 0)

    def test_get_low_torment_traits_with_form(self):
        """get_low_torment_traits returns traits from form."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)
        self.earthbound.apocalyptic_form = self.form
        self.earthbound.save()
        traits = self.earthbound.get_low_torment_traits()
        self.assertEqual(traits.count(), 2)

    def test_get_high_torment_traits_no_form(self):
        """get_high_torment_traits returns empty queryset with no form."""
        traits = self.earthbound.get_high_torment_traits()
        self.assertEqual(traits.count(), 0)

    def test_get_high_torment_traits_with_form(self):
        """get_high_torment_traits returns traits from form."""
        self.form.high_torment_traits.add(self.high_trait1, self.high_trait2)
        self.earthbound.apocalyptic_form = self.form
        self.earthbound.save()
        traits = self.earthbound.get_high_torment_traits()
        self.assertEqual(traits.count(), 2)

    def test_apocalyptic_form_counts_no_form(self):
        """Count methods return 0 with no form."""
        self.assertEqual(self.earthbound.apocalyptic_form_low_torment_count(), 0)
        self.assertEqual(self.earthbound.apocalyptic_form_high_torment_count(), 0)

    def test_apocalyptic_form_counts_with_form(self):
        """Count methods return correct counts."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)
        self.form.high_torment_traits.add(self.high_trait1)
        self.earthbound.apocalyptic_form = self.form
        self.earthbound.save()
        self.assertEqual(self.earthbound.apocalyptic_form_low_torment_count(), 2)
        self.assertEqual(self.earthbound.apocalyptic_form_high_torment_count(), 1)

    def test_apocalyptic_form_points_spent_no_form(self):
        """Points spent returns 0 with no form."""
        self.assertEqual(self.earthbound.apocalyptic_form_points_spent(), 0)

    def test_apocalyptic_form_points_spent_with_form(self):
        """Points spent returns sum of trait costs."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)  # 4 points
        self.form.high_torment_traits.add(self.high_trait1)  # 2 points
        self.earthbound.apocalyptic_form = self.form
        self.earthbound.save()
        self.assertEqual(self.earthbound.apocalyptic_form_points_spent(), 6)

    def test_apocalyptic_form_points_remaining_no_form(self):
        """Points remaining returns 16 with no form."""
        self.assertEqual(self.earthbound.apocalyptic_form_points_remaining(), 16)

    def test_apocalyptic_form_points_remaining_with_form(self):
        """Points remaining calculated correctly."""
        self.form.low_torment_traits.add(self.low_trait1, self.low_trait2)  # 4 points
        self.form.high_torment_traits.add(self.high_trait1)  # 2 points
        self.earthbound.apocalyptic_form = self.form
        self.earthbound.save()
        self.assertEqual(self.earthbound.apocalyptic_form_points_remaining(), 10)


class EarthboundHouseAndVisageTests(TestCase):
    """Tests for house and visage relationships."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.earthbound = Earthbound.objects.create(name="Test Earthbound", owner=self.user)
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.visage = Visage.objects.create(name="Bel")

    def test_house_can_be_set(self):
        """House can be set."""
        self.earthbound.house = self.house
        self.earthbound.save()
        self.assertEqual(self.earthbound.house, self.house)

    def test_house_can_be_null(self):
        """House can be null."""
        self.assertIsNone(self.earthbound.house)

    def test_visage_can_be_set(self):
        """Visage can be set."""
        self.earthbound.visage = self.visage
        self.earthbound.save()
        self.assertEqual(self.earthbound.visage, self.visage)

    def test_visage_can_be_null(self):
        """Visage can be null."""
        self.assertIsNone(self.earthbound.visage)


class EarthboundAllowedBackgroundsTests(TestCase):
    """Tests for Earthbound-specific allowed backgrounds."""

    def test_allowed_backgrounds_includes_earthbound_specific(self):
        """allowed_backgrounds includes Earthbound-specific backgrounds."""
        self.assertIn("codex", Earthbound.allowed_backgrounds)
        self.assertIn("cult", Earthbound.allowed_backgrounds)
        self.assertIn("hoard", Earthbound.allowed_backgrounds)
        self.assertIn("mastery", Earthbound.allowed_backgrounds)
        self.assertIn("thralls", Earthbound.allowed_backgrounds)
        self.assertIn("worship", Earthbound.allowed_backgrounds)

    def test_allowed_backgrounds_includes_common(self):
        """allowed_backgrounds includes common backgrounds."""
        self.assertIn("contacts", Earthbound.allowed_backgrounds)
        self.assertIn("mentor", Earthbound.allowed_backgrounds)
        self.assertIn("allies", Earthbound.allowed_backgrounds)
        self.assertIn("influence", Earthbound.allowed_backgrounds)
        self.assertIn("resources", Earthbound.allowed_backgrounds)
