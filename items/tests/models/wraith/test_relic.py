"""Tests for WraithRelic model."""
from django.test import TestCase
from items.models.wraith.relic import WraithRelic


class TestWraithRelic(TestCase):
    """Test WraithRelic model methods."""

    def setUp(self):
        self.relic = WraithRelic.objects.create(
            name="Test Wraith Relic",
            level=3,
            rarity="uncommon",
        )

    def test_save_sets_background_cost_to_level(self):
        """Test save() sets background_cost equal to level."""
        relic = WraithRelic.objects.create(name="Level Test", level=4)
        self.assertEqual(relic.background_cost, 4)

    def test_set_level(self):
        """Test set_level sets level and background_cost."""
        result = self.relic.set_level(5)
        self.assertTrue(result)
        self.assertEqual(self.relic.level, 5)
        self.assertEqual(self.relic.background_cost, 5)

    def test_has_level_true(self):
        """Test has_level returns True when level > 0."""
        self.assertTrue(self.relic.has_level())

    def test_has_level_false(self):
        """Test has_level returns False when level is 0."""
        relic = WraithRelic.objects.create(name="No Level", level=0)
        self.assertFalse(relic.has_level())


class TestWraithRelicDefaults(TestCase):
    """Test WraithRelic default values."""

    def test_level_default(self):
        """Test level defaults to 1."""
        relic = WraithRelic.objects.create(name="Default Level")
        self.assertEqual(relic.level, 1)

    def test_rarity_default(self):
        """Test rarity defaults to common."""
        relic = WraithRelic.objects.create(name="Default Rarity")
        self.assertEqual(relic.rarity, "common")

    def test_pathos_cost_default(self):
        """Test pathos_cost defaults to 0."""
        relic = WraithRelic.objects.create(name="Default Pathos")
        self.assertEqual(relic.pathos_cost, 0)


class TestWraithRelicRarity(TestCase):
    """Test rarity choices."""

    def test_rarity_choices(self):
        """Test rarity can be set to valid choices."""
        valid_rarities = ["common", "uncommon", "rare", "very_rare", "legendary"]
        for rarity in valid_rarities:
            relic = WraithRelic.objects.create(name=f"{rarity} relic", rarity=rarity)
            self.assertEqual(relic.rarity, rarity)


class TestWraithRelicUrls(TestCase):
    """Test URL methods for WraithRelic."""

    def setUp(self):
        self.relic = WraithRelic.objects.create(name="URL Test Relic")

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.relic.get_update_url()
        self.assertIn(str(self.relic.id), url)
        self.assertIn("relic", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = WraithRelic.get_creation_url()
        self.assertIn("relic", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.relic.get_heading(), "wto_heading")


class TestWraithRelicDetailView(TestCase):
    """Test WraithRelic detail view."""

    def setUp(self):
        self.relic = WraithRelic.objects.create(name="Test Relic")
        self.url = self.relic.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/wraith/relic/detail.html")


class TestWraithRelicCreateView(TestCase):
    """Test WraithRelic create view."""

    def setUp(self):
        self.url = WraithRelic.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/wraith/relic/form.html")


class TestWraithRelicUpdateView(TestCase):
    """Test WraithRelic update view."""

    def setUp(self):
        self.relic = WraithRelic.objects.create(name="Test Relic", description="Test")
        self.url = self.relic.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/wraith/relic/form.html")


class TestWraithRelicProperties(TestCase):
    """Test WraithRelic specific properties."""

    def test_type_is_relic(self):
        """Test type is 'relic'."""
        relic = WraithRelic.objects.create(name="Type Test")
        self.assertEqual(relic.type, "relic")

    def test_gameline_is_wto(self):
        """Test gameline is 'wto'."""
        relic = WraithRelic.objects.create(name="Gameline Test")
        self.assertEqual(relic.gameline, "wto")
