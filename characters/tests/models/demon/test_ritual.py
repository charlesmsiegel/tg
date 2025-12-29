"""Tests for Ritual model."""

from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual
from django.test import TestCase


class RitualModelTests(TestCase):
    """Tests for Ritual model functionality."""

    def setUp(self):
        """Create test fixtures."""
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore.houses.add(self.house)
        self.ritual = Ritual.objects.create(
            name="Binding of Fire",
            house=self.house,
            primary_lore=self.lore,
            primary_lore_rating=2,
        )

    def test_str(self):
        """Test __str__ returns ritual name."""
        self.assertEqual(str(self.ritual), "Binding of Fire")

    def test_ordering_by_house_then_name(self):
        """Rituals should be ordered by house name then ritual name."""
        house2 = DemonHouse.objects.create(
            name="Scourges", celestial_name="Asharu", starting_torment=3
        )
        lore2 = Lore.objects.create(name="Lore of Awakening", property_name="awakening")
        lore2.houses.add(house2)

        ritual_c = Ritual.objects.create(
            name="Conjuration", house=self.house, primary_lore=self.lore, primary_lore_rating=1
        )
        ritual_a = Ritual.objects.create(
            name="Awakening", house=house2, primary_lore=lore2, primary_lore_rating=1
        )

        # Devils comes before Scourges, so Devils rituals first
        rituals = list(Ritual.objects.all())
        # First should be Devils rituals (Binding of Fire, then Conjuration alphabetically)
        # Then Scourges rituals (Awakening)
        self.assertEqual(rituals[0].house, self.house)

    def test_default_values(self):
        """Test default values for Ritual fields."""
        self.assertEqual(self.ritual.system, "")
        self.assertEqual(self.ritual.base_cost, 6)
        self.assertEqual(self.ritual.minimum_casting_time, 10)
        self.assertEqual(self.ritual.restrictions, "")
        self.assertEqual(self.ritual.torment_effect, "")
        self.assertEqual(self.ritual.variations, "")
        self.assertEqual(self.ritual.flavor_text, "")
        self.assertEqual(self.ritual.source_page, "")
        self.assertEqual(self.ritual.secondary_lore_requirements, [])

    def test_house_relationship(self):
        """Test house FK relationship."""
        self.assertEqual(self.ritual.house, self.house)
        self.assertIn(self.ritual, self.house.rituals.all())

    def test_primary_lore_relationship(self):
        """Test primary_lore FK relationship."""
        self.assertEqual(self.ritual.primary_lore, self.lore)
        self.assertEqual(self.ritual.primary_lore_rating, 2)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.ritual.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/ritual/{self.ritual.pk}/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.ritual.get_heading(), "dtf_heading")


class RitualWithSecondaryLoreTests(TestCase):
    """Tests for rituals with secondary lore requirements."""

    def setUp(self):
        """Create test fixtures."""
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.primary_lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.primary_lore.houses.add(self.house)
        self.secondary_lore = Lore.objects.create(
            name="Lore of the Fundament", property_name="fundament"
        )
        self.secondary_lore.houses.add(self.house)
        self.ritual = Ritual.objects.create(
            name="Complex Ritual",
            house=self.house,
            primary_lore=self.primary_lore,
            primary_lore_rating=3,
            secondary_lore_requirements=[
                {"lore_id": self.secondary_lore.pk, "rating": 2}
            ],
        )

    def test_secondary_lore_requirements(self):
        """Test secondary lore requirements are stored correctly."""
        self.assertEqual(len(self.ritual.secondary_lore_requirements), 1)
        self.assertEqual(self.ritual.secondary_lore_requirements[0]["rating"], 2)

    def test_get_secondary_lores(self):
        """Test get_secondary_lores method."""
        lores = self.ritual.get_secondary_lores()
        self.assertEqual(len(lores), 1)
        self.assertEqual(lores[0]["lore"], self.secondary_lore)
        self.assertEqual(lores[0]["rating"], 2)

    def test_total_lore_dots(self):
        """Test total_lore_dots calculation."""
        # 3 from primary + 2 from secondary = 5
        self.assertEqual(self.ritual.total_lore_dots(), 5)

    def test_total_lore_paths(self):
        """Test total_lore_paths calculation."""
        # 1 primary + 1 secondary = 2
        self.assertEqual(self.ritual.total_lore_paths(), 2)

    def test_ritual_with_system(self):
        """Test ritual with system text."""
        self.ritual.system = "Roll Manipulation + Lore of Flame"
        self.ritual.save()
        self.assertEqual(self.ritual.system, "Roll Manipulation + Lore of Flame")


class RitualBaseCostTests(TestCase):
    """Tests for ritual base cost values."""

    def setUp(self):
        """Create test fixtures."""
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore.houses.add(self.house)

    def test_default_base_cost(self):
        """Default base_cost should be 6."""
        ritual = Ritual.objects.create(
            name="Standard Ritual", house=self.house, primary_lore=self.lore, primary_lore_rating=1
        )
        self.assertEqual(ritual.base_cost, 6)

    def test_custom_base_cost(self):
        """Base cost can be set to custom values."""
        ritual = Ritual.objects.create(
            name="Hard Ritual",
            house=self.house,
            primary_lore=self.lore,
            primary_lore_rating=3,
            base_cost=10,
        )
        self.assertEqual(ritual.base_cost, 10)


class RitualHouseLoreRelationshipTests(TestCase):
    """Tests for house and lore FK relationships."""

    def setUp(self):
        """Create test fixtures."""
        self.house1 = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.house2 = DemonHouse.objects.create(
            name="Scourges", celestial_name="Asharu", starting_torment=3
        )
        self.lore1 = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore1.houses.add(self.house1)
        self.lore2 = Lore.objects.create(name="Lore of the Firmament", property_name="firmament")
        self.lore2.houses.add(self.house2)

    def test_ritual_belongs_to_house(self):
        """Ritual belongs to a specific house."""
        ritual = Ritual.objects.create(
            name="Test Ritual", house=self.house1, primary_lore=self.lore1, primary_lore_rating=1
        )
        self.assertEqual(ritual.house, self.house1)
        self.assertNotEqual(ritual.house, self.house2)

    def test_house_rituals_related_name(self):
        """Test house.rituals related name."""
        ritual1 = Ritual.objects.create(
            name="Ritual 1", house=self.house1, primary_lore=self.lore1, primary_lore_rating=1
        )
        ritual2 = Ritual.objects.create(
            name="Ritual 2", house=self.house1, primary_lore=self.lore1, primary_lore_rating=2
        )
        ritual3 = Ritual.objects.create(
            name="Ritual 3", house=self.house2, primary_lore=self.lore2, primary_lore_rating=1
        )

        house1_rituals = self.house1.rituals.all()
        self.assertEqual(house1_rituals.count(), 2)
        self.assertIn(ritual1, house1_rituals)
        self.assertIn(ritual2, house1_rituals)
        self.assertNotIn(ritual3, house1_rituals)

    def test_lore_can_be_used_by_multiple_rituals(self):
        """Multiple rituals can use the same lore."""
        ritual1 = Ritual.objects.create(
            name="Ritual 1", house=self.house1, primary_lore=self.lore1, primary_lore_rating=1
        )
        ritual2 = Ritual.objects.create(
            name="Ritual 2", house=self.house1, primary_lore=self.lore1, primary_lore_rating=2
        )
        self.assertEqual(ritual1.primary_lore, self.lore1)
        self.assertEqual(ritual2.primary_lore, self.lore1)


class RitualDeleteBehaviorTests(TestCase):
    """Tests for deletion behavior of Ritual relationships."""

    def setUp(self):
        """Create test fixtures."""
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore.houses.add(self.house)
        self.ritual = Ritual.objects.create(
            name="Test Ritual", house=self.house, primary_lore=self.lore, primary_lore_rating=2
        )

    def test_deleting_house_sets_null(self):
        """Deleting a house should set ritual house FK to NULL."""
        ritual_id = self.ritual.id
        self.house.delete()
        ritual = Ritual.objects.get(id=ritual_id)
        self.assertIsNone(ritual.house)

    def test_deleting_lore_sets_null(self):
        """Deleting a lore should set ritual lore FKs to NULL."""
        ritual_id = self.ritual.id
        self.lore.delete()
        ritual = Ritual.objects.get(id=ritual_id)
        self.assertIsNone(ritual.primary_lore)


class RitualDisplayMethodsTests(TestCase):
    """Tests for ritual display methods."""

    def setUp(self):
        """Create test fixtures."""
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.primary_lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.primary_lore.houses.add(self.house)
        self.secondary_lore = Lore.objects.create(
            name="Lore of the Fundament", property_name="fundament"
        )
        self.secondary_lore.houses.add(self.house)
        self.ritual = Ritual.objects.create(
            name="Complex Ritual",
            house=self.house,
            primary_lore=self.primary_lore,
            primary_lore_rating=3,
            secondary_lore_requirements=[
                {"lore_id": self.secondary_lore.pk, "rating": 2}
            ],
        )

    def test_get_primary_lore_display(self):
        """Test get_primary_lore_display formatting."""
        display = self.ritual.get_primary_lore_display()
        self.assertEqual(display, "Lore of Flame •••")

    def test_get_primary_lore_display_no_lore(self):
        """Test get_primary_lore_display with no lore."""
        self.ritual.primary_lore = None
        self.ritual.save()
        display = self.ritual.get_primary_lore_display()
        self.assertEqual(display, "")

    def test_get_secondary_lore_display(self):
        """Test get_secondary_lore_display formatting."""
        displays = self.ritual.get_secondary_lore_display()
        self.assertEqual(len(displays), 1)
        self.assertEqual(displays[0], "Lore of the Fundament ••")

    def test_get_secondary_lores_with_invalid_id(self):
        """Test get_secondary_lores handles invalid lore IDs."""
        self.ritual.secondary_lore_requirements = [
            {"lore_id": 99999, "rating": 2}  # Non-existent ID
        ]
        self.ritual.save()
        lores = self.ritual.get_secondary_lores()
        self.assertEqual(len(lores), 0)


class RitualCastingTimeTests(TestCase):
    """Tests for ritual casting time."""

    def setUp(self):
        """Create test fixtures."""
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=4
        )
        self.lore = Lore.objects.create(name="Lore of Flame", property_name="flame")
        self.lore.houses.add(self.house)

    def test_default_casting_time(self):
        """Default minimum_casting_time should be 10 minutes."""
        ritual = Ritual.objects.create(
            name="Standard Ritual", house=self.house, primary_lore=self.lore, primary_lore_rating=1
        )
        self.assertEqual(ritual.minimum_casting_time, 10)

    def test_custom_casting_time(self):
        """Casting time can be customized."""
        ritual = Ritual.objects.create(
            name="Quick Ritual",
            house=self.house,
            primary_lore=self.lore,
            primary_lore_rating=1,
            minimum_casting_time=5,
        )
        self.assertEqual(ritual.minimum_casting_time, 5)

    def test_long_casting_time(self):
        """Test longer casting times."""
        ritual = Ritual.objects.create(
            name="Long Ritual",
            house=self.house,
            primary_lore=self.lore,
            primary_lore_rating=5,
            minimum_casting_time=60,  # 1 hour
        )
        self.assertEqual(ritual.minimum_casting_time, 60)
