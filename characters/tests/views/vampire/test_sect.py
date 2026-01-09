"""Tests for VampireSect views and templates."""

from characters.models.vampire.sect import VampireSect
from django.test import Client, TestCase
from django.urls import reverse


class TestVampireSectDetailView(TestCase):
    """Test VampireSect detail view."""

    def setUp(self):
        self.client = Client()
        self.sect = VampireSect.objects.create(
            name="Camarilla",
            philosophy="The Masquerade must be preserved at all costs.",
        )
        self.url = self.sect.get_absolute_url()

    def test_detail_view_status_code(self):
        """Detail view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/sect/detail.html")


class TestVampireSectListView(TestCase):
    """Test VampireSect list view."""

    def setUp(self):
        self.client = Client()
        VampireSect.objects.create(name="Camarilla")
        VampireSect.objects.create(name="Sabbat")
        self.url = reverse("characters:vampire:list:sect")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/list/sect/")

    def test_list_view_status_code(self):
        """List view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/sect/list.html")

    def test_list_view_contains_sects(self):
        """List view displays all sects."""
        response = self.client.get(self.url)
        self.assertContains(response, "Camarilla")
        self.assertContains(response, "Sabbat")


class TestVampireSectCreateView(TestCase):
    """Test VampireSect create view."""

    def setUp(self):
        self.client = Client()
        self.url = VampireSect.get_creation_url()
        self.valid_data = {
            "name": "Test Sect",
            "description": "A test sect",
            "philosophy": "Test philosophy",
        }

    def test_create_url_resolves(self):
        """Create URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/create/sect/")

    def test_create_view_get_status_code(self):
        """Create view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/sect/form.html")

    def test_create_view_post_creates_sect(self):
        """Create view POST creates a new sect."""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(VampireSect.objects.filter(name="Test Sect").count(), 1)


class TestVampireSectUpdateView(TestCase):
    """Test VampireSect update view."""

    def setUp(self):
        self.client = Client()
        self.sect = VampireSect.objects.create(
            name="Anarch Movement",
        )
        self.url = self.sect.get_update_url()

    def test_update_url_resolves(self):
        """Update URL should resolve correctly."""
        self.assertEqual(self.url, f"/characters/vampire/update/sect/{self.sect.pk}/")

    def test_update_view_get_status_code(self):
        """Update view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/sect/form.html")


class TestVampireSectCreateViewNegativeCases(TestCase):
    """Test VampireSect create view with invalid data."""

    def setUp(self):
        self.client = Client()
        self.url = VampireSect.get_creation_url()

    def test_create_missing_name_fails(self):
        """Create view POST with missing name fails."""
        data = {"philosophy": "Test philosophy"}
        response = self.client.post(self.url, data)
        # Form should re-render with errors (200) rather than redirect (302)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VampireSect.objects.filter(philosophy="Test philosophy").count(), 0)
        # Check that name field has errors (form validation + model clean)
        self.assertTrue(response.context["form"].errors.get("name"))

    def test_create_empty_data_fails(self):
        """Create view POST with empty data fails."""
        initial_count = VampireSect.objects.count()
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VampireSect.objects.count(), initial_count)
