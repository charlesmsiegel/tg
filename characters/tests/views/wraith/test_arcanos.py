"""Tests for Arcanos views.

Arcanos is a reference model (public game data) and should be accessible without login.
"""

from characters.models.wraith.arcanos import Arcanos
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse


class TestArcanosDetailView(TestCase):
    """Test ArcanosDetailView permissions and functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.arcanos = Arcanos.objects.create(
            name="Argos",
            description="The art of traveling the Tempest",
            arcanos_type="standard",
            owner=self.user,
        )

    def test_detail_view_publicly_accessible(self):
        """Test that arcanos detail view is accessible without login (reference model)."""
        response = self.client.get(self.arcanos.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        response = self.client.get(self.arcanos.get_absolute_url())
        self.assertTemplateUsed(response, "characters/wraith/arcanos/detail.html")

    def test_detail_view_shows_levels(self):
        """Test that detail view shows arcanos levels for parent."""
        level1 = Arcanos.objects.create(
            name="Enshroud",
            description="Become invisible to the living",
            arcanos_type="standard",
            level=1,
            parent_arcanos=self.arcanos,
            owner=self.user,
        )
        response = self.client.get(self.arcanos.get_absolute_url())
        self.assertIn("levels", response.context)
        self.assertIn(level1, response.context["levels"])


class TestArcanosListView(TestCase):
    """Test ArcanosListView functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.parent_arcanos = Arcanos.objects.create(
            name="Inhabit", arcanos_type="standard", description="Control machines", owner=self.user
        )
        self.child_arcanos = Arcanos.objects.create(
            name="Sense Gremlin",
            arcanos_type="standard",
            description="Sense machine spirits",
            level=1,
            parent_arcanos=self.parent_arcanos,
            owner=self.user,
        )

    def test_list_view_publicly_accessible(self):
        """Test that arcanos list view is accessible without login (reference model)."""
        url = reverse("characters:wraith:list:arcanos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_arcanoi(self):
        """Test that list view shows arcanoi."""
        url = reverse("characters:wraith:list:arcanos")
        response = self.client.get(url)
        self.assertContains(response, "Inhabit")

    def test_list_view_only_shows_parent_arcanoi(self):
        """Test that list view only shows parent arcanoi, not levels."""
        url = reverse("characters:wraith:list:arcanos")
        response = self.client.get(url)
        self.assertContains(response, "Inhabit")
        # The child should not appear in the main list
        self.assertNotContains(response, "Sense Gremlin")


class TestArcanosCreateView(TestCase):
    """Test ArcanosCreateView functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_publicly_accessible(self):
        """Test that arcanos create view is accessible without login (reference model)."""
        url = reverse("characters:wraith:create:arcanos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used."""
        url = reverse("characters:wraith:create:arcanos")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/arcanos/form.html")

    def test_create_arcanos_successfully(self):
        """Test creating an arcanos successfully."""
        url = reverse("characters:wraith:create:arcanos")
        data = {
            "name": "Keening",
            "description": "The art of ghostly communication",
            "arcanos_type": "standard",
            "level": 0,
            "pathos_cost": 0,
            "angst_cost": 0,
            "difficulty": 6,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Arcanos.objects.filter(name="Keening").exists())


class TestArcanosUpdateView(TestCase):
    """Test ArcanosUpdateView functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.arcanos = Arcanos.objects.create(
            name="Lifeweb",
            arcanos_type="standard",
            description="Art of connections",
            owner=self.user,
        )

    def test_update_view_publicly_accessible(self):
        """Test that arcanos update view is accessible without login (reference model)."""
        url = self.arcanos.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used."""
        url = self.arcanos.get_update_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/arcanos/form.html")

    def test_update_arcanos_successfully(self):
        """Test updating an arcanos successfully."""
        url = self.arcanos.get_update_url()
        data = {
            "name": "Updated Arcanos",
            "description": "Updated description",
            "arcanos_type": "dark",
            "level": 0,
            "pathos_cost": 1,
            "angst_cost": 0,
            "difficulty": 7,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.arcanos.refresh_from_db()
        self.assertEqual(self.arcanos.name, "Updated Arcanos")


class TestArcanos404Handling(TestCase):
    """Test 404 error handling for arcanos views."""

    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_arcanos_detail_returns_404_for_invalid_pk(self):
        """Test that arcanos detail returns 404 for non-existent arcanos."""
        response = self.client.get(reverse("characters:wraith:arcanos", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_arcanos_update_returns_404_for_invalid_pk(self):
        """Test that arcanos update returns 404 for non-existent arcanos."""
        response = self.client.get(
            reverse("characters:wraith:update:arcanos", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
