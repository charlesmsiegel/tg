"""Tests for VampireClan views and templates."""

from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestVampireClanDetailView(TestCase):
    """Test VampireClan detail view."""

    def setUp(self):
        self.client = Client()
        self.discipline = Discipline.objects.create(name="Dominate", property_name="dominate")
        self.clan = VampireClan.objects.create(
            name="Ventrue",
            nickname="Blue Bloods",
            weakness="Can only feed from specific mortals",
        )
        self.clan.disciplines.add(self.discipline)
        self.url = self.clan.get_absolute_url()

    def test_detail_view_status_code(self):
        """Detail view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/clan/detail.html")

    def test_detail_view_context_contains_disciplines(self):
        """Detail view context includes disciplines."""
        response = self.client.get(self.url)
        self.assertIn("disciplines", response.context)
        self.assertEqual(response.context["disciplines"], "Dominate")


class TestVampireClanListView(TestCase):
    """Test VampireClan list view."""

    def setUp(self):
        self.client = Client()
        VampireClan.objects.create(name="Brujah", nickname="Rabble")
        VampireClan.objects.create(name="Ventrue", nickname="Blue Bloods")
        self.url = reverse("characters:vampire:list:clan")

    def test_list_url_resolves(self):
        """List view URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/list/clan/")

    def test_list_view_status_code(self):
        """List view is publicly accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """List view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/clan/list.html")

    def test_list_view_contains_clans(self):
        """List view displays all clans."""
        response = self.client.get(self.url)
        self.assertContains(response, "Brujah")
        self.assertContains(response, "Ventrue")


class TestVampireClanCreateView(TestCase):
    """Test VampireClan create view."""

    def setUp(self):
        self.client = Client()
        self.url = VampireClan.get_creation_url()
        self.valid_data = {
            "name": "Test Clan",
            "description": "A test clan",
            "nickname": "Testers",
            "weakness": "Test weakness",
            "is_bloodline": False,
        }

    def test_create_url_resolves(self):
        """Create URL should resolve correctly."""
        self.assertEqual(self.url, "/characters/vampire/create/clan/")

    def test_create_view_get_status_code(self):
        """Create view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/clan/form.html")

    def test_create_view_post_creates_clan(self):
        """Create view POST creates a new clan."""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(VampireClan.objects.filter(name="Test Clan").count(), 1)


class TestVampireClanUpdateView(TestCase):
    """Test VampireClan update view."""

    def setUp(self):
        self.client = Client()
        self.clan = VampireClan.objects.create(
            name="Nosferatu",
            nickname="Sewer Rats",
        )
        self.url = self.clan.get_update_url()

    def test_update_url_resolves(self):
        """Update URL should resolve correctly."""
        self.assertEqual(self.url, f"/characters/vampire/update/clan/{self.clan.pk}/")

    def test_update_view_get_status_code(self):
        """Update view GET is accessible."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/clan/form.html")
