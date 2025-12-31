"""Tests for Treasure model."""

from django.test import TestCase
from items.models.changeling.treasure import Treasure


class TestTreasure(TestCase):
    """Test Treasure model methods."""

    def setUp(self):
        self.treasure = Treasure.objects.create(
            name="Test Treasure",
            rating=3,
            treasure_type="talisman",
            effects=[],
        )

    def test_str_with_name_and_rating(self):
        """Test __str__ returns name with star rating."""
        expected = f"{self.treasure.name} (★★★)"
        self.assertEqual(str(self.treasure), expected)

    def test_str_rating_1(self):
        """Test __str__ with rating 1."""
        treasure = Treasure.objects.create(name="One Star", rating=1, effects=[])
        self.assertEqual(str(treasure), "One Star (★)")

    def test_str_rating_5(self):
        """Test __str__ with rating 5."""
        treasure = Treasure.objects.create(name="Five Star", rating=5, effects=[])
        self.assertEqual(str(treasure), "Five Star (★★★★★)")


class TestTreasureDefaults(TestCase):
    """Test Treasure default values."""

    def test_rating_default(self):
        """Test rating defaults to 1."""
        treasure = Treasure.objects.create(name="Default Rating", effects=[])
        self.assertEqual(treasure.rating, 1)

    def test_treasure_type_default(self):
        """Test treasure_type defaults to empty string."""
        treasure = Treasure.objects.create(name="Default Type", effects=[])
        self.assertEqual(treasure.treasure_type, "")

    def test_permanence_default(self):
        """Test permanence defaults to True."""
        treasure = Treasure.objects.create(name="Default Permanence", effects=[])
        self.assertTrue(treasure.permanence)

    def test_glamour_storage_default(self):
        """Test glamour_storage defaults to 0."""
        treasure = Treasure.objects.create(name="Default Glamour", effects=[])
        self.assertEqual(treasure.glamour_storage, 0)


class TestTreasureType(TestCase):
    """Test treasure type choices."""

    def test_treasure_type_choices(self):
        """Test treasure_type can be set to valid choices."""
        valid_types = ["weapon", "armor", "talisman", "wonder", "other"]
        for ttype in valid_types:
            treasure = Treasure.objects.create(
                name=f"{ttype} treasure", treasure_type=ttype, effects=[]
            )
            self.assertEqual(treasure.treasure_type, ttype)


class TestTreasureUrls(TestCase):
    """Test URL methods for Treasure."""

    def setUp(self):
        self.treasure = Treasure.objects.create(name="URL Test Treasure", effects=[])

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.treasure.get_update_url()
        self.assertIn(str(self.treasure.id), url)
        self.assertIn("treasure", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Treasure.get_creation_url()
        self.assertIn("treasure", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.treasure.get_heading(), "ctd_heading")


class TestTreasureDetailView(TestCase):
    """Test Treasure detail view."""

    def setUp(self):
        self.treasure = Treasure.objects.create(name="Test Treasure", effects=[])
        self.url = self.treasure.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/changeling/treasure/detail.html")


class TestTreasureCreateView(TestCase):
    """Test Treasure create view."""

    def setUp(self):
        self.url = Treasure.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/changeling/treasure/form.html")


class TestTreasureUpdateView(TestCase):
    """Test Treasure update view."""

    def setUp(self):
        self.treasure = Treasure.objects.create(
            name="Test Treasure", description="Test", effects=[]
        )
        self.url = self.treasure.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/changeling/treasure/form.html")


class TestTreasureEffects(TestCase):
    """Test effects JSONField."""

    def test_effects_default(self):
        """Test effects defaults to empty list."""
        treasure = Treasure.objects.create(name="Default Effects")
        self.assertEqual(treasure.effects, [])

    def test_effects_can_be_set(self):
        """Test effects can be set to a list."""
        effects_list = ["Flight", "Invisibility", "Telekinesis"]
        treasure = Treasure.objects.create(name="With Effects", effects=effects_list)
        self.assertEqual(treasure.effects, effects_list)


class TestTreasureGlamour(TestCase):
    """Test glamour-related properties."""

    def test_glamour_storage_can_be_set(self):
        """Test glamour_storage can be set."""
        treasure = Treasure.objects.create(name="Glamour Storage", glamour_storage=25, effects=[])
        self.assertEqual(treasure.glamour_storage, 25)

    def test_glamour_affinity_default(self):
        """Test glamour_affinity defaults to empty string."""
        treasure = Treasure.objects.create(name="Default Affinity", effects=[])
        self.assertEqual(treasure.glamour_affinity, "")

    def test_glamour_affinity_can_be_set(self):
        """Test glamour_affinity can be set."""
        treasure = Treasure.objects.create(name="With Affinity", glamour_affinity="Joy", effects=[])
        self.assertEqual(treasure.glamour_affinity, "Joy")
