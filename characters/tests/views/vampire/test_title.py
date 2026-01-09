"""Tests for VampireTitle views and templates."""

from characters.models.vampire.sect import VampireSect
from characters.models.vampire.title import VampireTitle
from django.test import Client, TestCase
from django.urls import reverse


class TestVampireTitleDetailView(TestCase):
    """Test VampireTitle detail view."""

    def setUp(self):
        self.client = Client()
        self.sect = VampireSect.objects.create(name="Camarilla")
        self.title = VampireTitle.objects.create(
            name="Prince",
            sect=self.sect,
            value=7,
            is_negative=False,
            powers="Rules a domain. Final authority on local Kindred matters.",
        )
        self.url = self.title.get_absolute_url()

    def test_detail_view_status_code(self):
        """Detail view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/title/detail.html")

    def test_detail_view_context_contains_sect(self):
        """Detail view context includes sect when present."""
        response = self.client.get(self.url)
        self.assertIn("sect", response.context)
        self.assertEqual(response.context["sect"], self.sect)


class TestVampireTitleListView(TestCase):
    """Test VampireTitle list view."""

    def setUp(self):
        self.client = Client()
        VampireTitle.objects.create(name="Prince", value=7)
        VampireTitle.objects.create(name="Primogen", value=3)
        self.url = reverse("characters:vampire:list:title")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/list/title/")

    def test_list_view_status_code(self):
        """List view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/title/list.html")

    def test_list_view_contains_titles(self):
        """List view displays all titles."""
        response = self.client.get(self.url)
        self.assertContains(response, "Prince")
        self.assertContains(response, "Primogen")


class TestVampireTitleCreateView(TestCase):
    """Test VampireTitle create view."""

    def setUp(self):
        self.client = Client()
        self.url = VampireTitle.get_creation_url()
        self.valid_data = {
            "name": "Test Title",
            "description": "A test title",
            "value": 2,
            "is_negative": False,
            "powers": "Test powers",
        }

    def test_create_url_resolves(self):
        """Create URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/create/title/")

    def test_create_view_get_status_code(self):
        """Create view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/title/form.html")

    def test_create_view_post_creates_title(self):
        """Create view POST creates a new title."""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(VampireTitle.objects.filter(name="Test Title").count(), 1)


class TestVampireTitleUpdateView(TestCase):
    """Test VampireTitle update view."""

    def setUp(self):
        self.client = Client()
        self.title = VampireTitle.objects.create(
            name="Sheriff",
            value=4,
        )
        self.url = self.title.get_update_url()

    def test_update_url_resolves(self):
        """Update URL should resolve correctly."""
        self.assertEqual(self.url, f"/characters/vampire/update/title/{self.title.pk}/")

    def test_update_view_get_status_code(self):
        """Update view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/title/form.html")


class TestVampireTitleNegativeStatus(TestCase):
    """Test negative title handling in views."""

    def setUp(self):
        self.client = Client()
        self.negative_title = VampireTitle.objects.create(
            name="Autarkis",
            value=2,
            is_negative=True,
        )

    def test_negative_title_detail_displays_correctly(self):
        """Negative title detail view shows negative status."""
        response = self.client.get(self.negative_title.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Negative Title")


class TestVampireTitleCreateViewNegativeCases(TestCase):
    """Test VampireTitle create view with invalid data."""

    def setUp(self):
        self.client = Client()
        self.url = VampireTitle.get_creation_url()

    def test_create_missing_name_fails(self):
        """Create view POST with missing name fails."""
        data = {"value": 5, "is_negative": False}
        response = self.client.post(self.url, data)
        # Form should re-render with errors (200) rather than redirect (302)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VampireTitle.objects.filter(value=5).count(), 0)
        # Check that name field has errors (form validation + model clean)
        self.assertTrue(response.context["form"].errors.get("name"))

    def test_create_empty_data_fails(self):
        """Create view POST with empty data fails."""
        initial_count = VampireTitle.objects.count()
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VampireTitle.objects.count(), initial_count)

    def test_create_invalid_sect_fails(self):
        """Create view POST with invalid sect ID fails."""
        data = {
            "name": "Test Title",
            "value": 3,
            "sect": 99999,  # Non-existent ID
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VampireTitle.objects.filter(name="Test Title").count(), 0)


class TestVampireTitleDetailViewNoSect(TestCase):
    """Test VampireTitle detail view when sect is None."""

    def setUp(self):
        self.client = Client()
        self.title = VampireTitle.objects.create(
            name="Independent Title",
            value=2,
            sect=None,
        )

    def test_detail_view_handles_no_sect(self):
        """Detail view handles title without sect gracefully."""
        response = self.client.get(self.title.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # sect context variable should be None
        self.assertIsNone(response.context["sect"])
