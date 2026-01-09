"""Tests for Discipline views and templates."""

from characters.models.vampire.discipline import Discipline
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


# URL helpers for Discipline (which extends Statistic, not Model)
def get_discipline_create_url():
    return reverse("characters:vampire:create:discipline")


def get_discipline_list_url():
    return reverse("characters:vampire:list:discipline")


class TestDisciplineDetailView(TestCase):
    """Test Discipline detail view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.discipline = Discipline.objects.create(
            name="Celerity",
            property_name="celerity",
            description="Supernatural speed and reflexes.",
        )
        self.url = self.discipline.get_absolute_url()

    def test_detail_view_requires_login(self):
        """Detail view requires authentication."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_detail_view_status_code(self):
        """Detail view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/discipline/detail.html")


class TestDisciplineListView(TestCase):
    """Test Discipline list view."""

    def setUp(self):
        self.client = Client()
        Discipline.objects.create(name="Potence", property_name="potence")
        Discipline.objects.create(name="Fortitude", property_name="fortitude")
        self.url = reverse("characters:vampire:list:discipline")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/list/discipline/")

    def test_list_view_status_code(self):
        """List view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/discipline/list.html")

    def test_list_view_contains_disciplines(self):
        """List view displays all disciplines."""
        response = self.client.get(self.url)
        self.assertContains(response, "Potence")
        self.assertContains(response, "Fortitude")


class TestDisciplineCreateView(TestCase):
    """Test Discipline create view."""

    def setUp(self):
        self.client = Client()
        self.url = get_discipline_create_url()
        self.valid_data = {
            "name": "Test Discipline",
            "property_name": "test_discipline",
        }

    def test_create_url_resolves(self):
        """Create URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/create/discipline/")

    def test_create_view_get_status_code(self):
        """Create view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/discipline/form.html")

    def test_create_view_post_creates_discipline(self):
        """Create view POST creates a new discipline."""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(Discipline.objects.filter(name="Test Discipline").count(), 1)


class TestDisciplineUpdateView(TestCase):
    """Test Discipline update view."""

    def setUp(self):
        self.client = Client()
        self.discipline = Discipline.objects.create(
            name="Obtenebration",
            property_name="obtenebration",
        )
        self.url = self.discipline.get_update_url()

    def test_update_url_resolves(self):
        """Update URL should resolve correctly."""
        self.assertEqual(self.url, f"/characters/vampire/update/discipline/{self.discipline.pk}/")

    def test_update_view_get_status_code(self):
        """Update view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/discipline/form.html")


class TestDisciplineCreateViewNegativeCases(TestCase):
    """Test Discipline create view with invalid data."""

    def setUp(self):
        self.client = Client()
        self.url = get_discipline_create_url()

    def test_create_missing_name_fails(self):
        """Create view POST with missing name fails."""
        data = {"property_name": "test_discipline"}
        response = self.client.post(self.url, data)
        # Form should re-render with errors (200) rather than redirect (302)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Discipline.objects.filter(property_name="test_discipline").count(), 0)
        # Check that name field has errors (form validation + model clean)
        self.assertTrue(response.context["form"].errors.get("name"))

    def test_create_missing_property_name_fails(self):
        """Create view POST with missing property_name fails."""
        data = {"name": "Test Discipline"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Discipline.objects.filter(name="Test Discipline").count(), 0)
        # Check that property_name field has errors
        self.assertTrue(response.context["form"].errors.get("property_name"))

    def test_create_empty_data_fails(self):
        """Create view POST with empty data fails."""
        initial_count = Discipline.objects.count()
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Discipline.objects.count(), initial_count)
