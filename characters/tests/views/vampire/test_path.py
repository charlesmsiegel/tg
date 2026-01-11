"""Tests for Path views and templates."""

from django.test import Client, TestCase, override_settings
from django.urls import reverse

from characters.models.vampire.path import Path


# Disable caching for template assertion tests
@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class TestPathDetailView(TestCase):
    """Test Path detail view."""

    def setUp(self):
        self.client = Client()
        self.path = Path.objects.create(
            name="Path of Caine",
            requires_conviction=True,
            requires_instinct=True,
            ethics="Follow the teachings of Caine above all.",
        )
        self.url = self.path.get_absolute_url()

    def test_detail_view_public_access(self):
        """Detail view is publicly accessible (Path is reference data)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/path/detail.html")


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class TestPathListView(TestCase):
    """Test Path list view."""

    def setUp(self):
        self.client = Client()
        Path.objects.create(name="Path of Caine", requires_conviction=True, requires_instinct=True)
        Path.objects.create(
            name="Path of Death and the Soul", requires_conviction=True, requires_instinct=False
        )
        self.url = reverse("characters:vampire:list:path")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/list/path/")

    def test_list_view_status_code(self):
        """List view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/path/list.html")

    def test_list_view_contains_paths(self):
        """List view displays all paths."""
        response = self.client.get(self.url)
        self.assertContains(response, "Path of Caine")
        self.assertContains(response, "Path of Death and the Soul")


class TestPathCreateView(TestCase):
    """Test Path create view."""

    def setUp(self):
        self.client = Client()
        self.url = Path.get_creation_url()
        self.valid_data = {
            "name": "Test Path",
            "description": "A test path",
            "requires_conviction": True,
            "requires_instinct": False,
            "ethics": "Test ethics",
        }

    def test_create_url_resolves(self):
        """Create URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/create/path/")

    def test_create_view_get_status_code(self):
        """Create view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/path/form.html")

    def test_create_view_post_creates_path(self):
        """Create view POST creates a new path."""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(Path.objects.filter(name="Test Path").count(), 1)


class TestPathUpdateView(TestCase):
    """Test Path update view."""

    def setUp(self):
        self.client = Client()
        self.path = Path.objects.create(
            name="Path of Honorable Accord",
            requires_conviction=False,
            requires_instinct=True,
        )
        self.url = self.path.get_update_url()

    def test_update_url_resolves(self):
        """Update URL should resolve correctly."""
        self.assertEqual(self.url, f"/characters/vampire/update/path/{self.path.pk}/")

    def test_update_view_get_status_code(self):
        """Update view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/path/form.html")
