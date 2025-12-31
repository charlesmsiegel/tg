"""Tests for Talen model."""

from django.test import TestCase
from items.models.werewolf.talen import Talen


class TestTalen(TestCase):
    """Test Talen model methods."""

    def setUp(self):
        self.talen = Talen.objects.create(
            name="Test Talen",
            rank=2,
            gnosis=3,
            spirit="Fire Spirit",
        )

    def test_save_sets_background_cost_to_rank(self):
        """Test save() sets background_cost equal to rank."""
        talen = Talen.objects.create(name="Rank Test", rank=4)
        self.assertEqual(talen.background_cost, 4)

    def test_save_updates_background_cost_on_rank_change(self):
        """Test background_cost updates when rank changes."""
        self.talen.rank = 5
        self.talen.save()
        self.talen.refresh_from_db()
        self.assertEqual(self.talen.background_cost, 5)


class TestTalenDefaults(TestCase):
    """Test Talen default values."""

    def test_gnosis_default(self):
        """Test gnosis defaults to 0."""
        talen = Talen.objects.create(name="Default Gnosis")
        self.assertEqual(talen.gnosis, 0)

    def test_spirit_default(self):
        """Test spirit defaults to empty string."""
        talen = Talen.objects.create(name="Default Spirit")
        self.assertEqual(talen.spirit, "")


class TestTalenUrls(TestCase):
    """Test URL methods for Talen."""

    def setUp(self):
        self.talen = Talen.objects.create(name="URL Test Talen")

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.talen.get_update_url()
        self.assertIn(str(self.talen.id), url)
        self.assertIn("talen", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Talen.get_creation_url()
        self.assertIn("talen", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.talen.get_heading(), "wta_heading")


class TestTalenDetailView(TestCase):
    """Test Talen detail view."""

    def setUp(self):
        self.talen = Talen.objects.create(name="Test Talen")
        self.url = self.talen.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/werewolf/talen/detail.html")


class TestTalenCreateView(TestCase):
    """Test Talen create view."""

    def setUp(self):
        self.valid_data = {
            "name": "Test Talen",
            "rank": 2,
            "background_cost": 2,
            "quintessence_max": 2,
            "description": "Test",
            "gnosis": 2,
            "spirit": "Test Spirit",
        }
        self.url = Talen.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/werewolf/talen/form.html")

    def test_create_view_successful_post(self):
        """Test create view POST creates talen."""
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Talen.objects.count(), 1)


class TestTalenUpdateView(TestCase):
    """Test Talen update view."""

    def setUp(self):
        self.talen = Talen.objects.create(name="Test Talen", description="Test")
        self.valid_data = {
            "name": "Updated Talen",
            "rank": 3,
            "background_cost": 3,
            "quintessence_max": 3,
            "description": "Updated",
            "gnosis": 3,
            "spirit": "Updated Spirit",
        }
        self.url = self.talen.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/werewolf/talen/form.html")

    def test_update_view_successful_post(self):
        """Test update view POST updates talen."""
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.talen.refresh_from_db()
        self.assertEqual(self.talen.name, "Updated Talen")


class TestTalenInheritance(TestCase):
    """Test Talen inherits from Wonder correctly."""

    def test_talen_type(self):
        """Test Talen has correct type."""
        talen = Talen.objects.create(name="Type Test")
        self.assertEqual(talen.type, "talen")

    def test_talen_gameline(self):
        """Test Talen has correct gameline."""
        talen = Talen.objects.create(name="Gameline Test")
        self.assertEqual(talen.gameline, "wta")
