"""Tests for ShadowArchetype views."""

from characters.models.wraith.shadow_archetype import ShadowArchetype
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse


class TestShadowArchetypeDetailView(TestCase):
    """Test ShadowArchetypeDetailView permissions and functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.archetype = ShadowArchetype.objects.create(
            name="The Freak",
            description="An archetype of self-destruction",
            point_cost=3,
            core_function="Self-destruction through excess",
            owner=self.user,
        )

    def test_detail_view_accessible_when_logged_in(self):
        """Test that archetype detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.archetype.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.archetype.get_absolute_url())
        self.assertTemplateUsed(response, "characters/wraith/shadow_archetype/detail.html")


class TestShadowArchetypeListView(TestCase):
    """Test ShadowArchetypeListView functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        # Create archetype in setUp to avoid caching issues
        self.archetype = ShadowArchetype.objects.create(
            name="The Pusher", point_cost=2, owner=self.user
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that archetype list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:list:shadow_archetype")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_archetypes(self):
        """Test that list view shows archetypes."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:list:shadow_archetype")
        response = self.client.get(url)
        self.assertContains(response, "The Pusher")


class TestShadowArchetypeCreateView(TestCase):
    """Test ShadowArchetypeCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible(self):
        """Test that archetype create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:shadow_archetype")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:shadow_archetype")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/shadow_archetype/form.html")

    def test_create_archetype_successfully(self):
        """Test creating an archetype successfully."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:shadow_archetype")
        data = {
            "name": "The Martyr",
            "description": "An archetype of sacrifice",
            "point_cost": 4,
            "core_function": "Self-sacrifice for others' suffering",
            "modus_operandi": "",
            "dominance_behavior": "",
            "effect_on_psyche": "",
            "strengths": "",
            "weaknesses": "",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ShadowArchetype.objects.filter(name="The Martyr").exists())


class TestShadowArchetypeUpdateView(TestCase):
    """Test ShadowArchetypeUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.archetype = ShadowArchetype.objects.create(
            name="The Director", point_cost=2, owner=self.user
        )

    def test_update_view_accessible(self):
        """Test that archetype update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.archetype.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = self.archetype.get_update_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/shadow_archetype/form.html")

    def test_update_archetype_successfully(self):
        """Test updating an archetype successfully."""
        self.client.login(username="user", password="password")
        url = self.archetype.get_update_url()
        data = {
            "name": "Updated Archetype",
            "description": "Updated description",
            "point_cost": 5,
            "core_function": "Updated function",
            "modus_operandi": "Updated",
            "dominance_behavior": "Updated",
            "effect_on_psyche": "Updated",
            "strengths": "Updated",
            "weaknesses": "Updated",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.archetype.refresh_from_db()
        self.assertEqual(self.archetype.name, "Updated Archetype")


class TestShadowArchetype404Handling(TestCase):
    """Test 404 error handling for archetype views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_archetype_detail_returns_404_for_invalid_pk(self):
        """Test that archetype detail returns 404 for non-existent archetype."""
        self.client.login(username="user", password="password")
        response = self.client.get(
            reverse("characters:wraith:shadow_archetype", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_archetype_update_returns_404_for_invalid_pk(self):
        """Test that archetype update returns 404 for non-existent archetype."""
        self.client.login(username="user", password="password")
        response = self.client.get(
            reverse("characters:wraith:update:shadow_archetype", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
