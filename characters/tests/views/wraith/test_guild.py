"""Tests for Guild views.

Guild is a reference model (public game data) and should be accessible without login.
"""

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.wraith.guild import Guild


class TestGuildDetailView(TestCase):
    """Test GuildDetailView permissions and functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.guild = Guild.objects.create(
            name="Artificers",
            description="Crafters of ghostly items",
            guild_type="greater",
            willpower=6,
            owner=self.user,
        )

    def test_detail_view_publicly_accessible(self):
        """Test that guild detail view is accessible without login (reference model)."""
        response = self.client.get(self.guild.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        response = self.client.get(self.guild.get_absolute_url())
        self.assertTemplateUsed(response, "characters/wraith/guild/detail.html")


class TestGuildListView(TestCase):
    """Test GuildListView functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.guild = Guild.objects.create(name="Masquers", guild_type="greater", owner=self.user)

    def test_list_view_publicly_accessible(self):
        """Test that guild list view is accessible without login (reference model)."""
        url = reverse("characters:wraith:list:guild")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_guilds(self):
        """Test that list view shows guilds."""
        url = reverse("characters:wraith:list:guild")
        response = self.client.get(url)
        self.assertContains(response, "Masquers")


class TestGuildCreateView(TestCase):
    """Test GuildCreateView functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.user.is_staff = True
        self.user.save(update_fields=["is_staff"])

    def test_create_view_requires_login(self):
        """Test that guild create view is restricted to authenticated editors (reference model)."""
        url = reverse("characters:wraith:create:guild")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used."""
        from django.contrib.auth import get_user_model
        self.client.force_login(get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True))
        url = reverse("characters:wraith:create:guild")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/guild/form.html")

    def test_create_guild_successfully(self):
        """Test creating a guild successfully."""
        from django.contrib.auth import get_user_model
        self.client.force_login(get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True))
        url = reverse("characters:wraith:create:guild")
        data = {
            "name": "Mnemoi",
            "description": "Memory keepers",
            "guild_type": "banned",
            "willpower": 7,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Guild.objects.filter(name="Mnemoi").exists())


class TestGuildUpdateView(TestCase):
    """Test GuildUpdateView functionality."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.guild = Guild.objects.create(name="Spooks", guild_type="lesser", owner=self.user)
        self.user.is_staff = True
        self.user.save(update_fields=["is_staff"])

    def test_update_view_requires_login(self):
        """Test that guild update view is restricted to authenticated editors (reference model)."""
        url = self.guild.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used."""
        from django.contrib.auth import get_user_model
        self.client.force_login(get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True))
        url = self.guild.get_update_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/guild/form.html")

    def test_update_guild_successfully(self):
        """Test updating a guild successfully."""
        from django.contrib.auth import get_user_model
        self.client.force_login(get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True))
        url = self.guild.get_update_url()
        data = {
            "name": "Updated Guild",
            "description": "Updated description",
            "guild_type": "greater",
            "willpower": 8,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.guild.refresh_from_db()
        self.assertEqual(self.guild.name, "Updated Guild")


class TestGuild404Handling(TestCase):
    """Test 404 error handling for guild views."""

    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_guild_detail_returns_404_for_invalid_pk(self):
        """Test that guild detail returns 404 for non-existent guild."""
        response = self.client.get(reverse("characters:wraith:guild", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_guild_update_returns_404_for_invalid_pk(self):
        """Test that guild update returns 404 for non-existent guild."""
        from django.contrib.auth import get_user_model
        self.client.force_login(get_user_model().objects.create_user("__legacy_auth_staff", is_staff=True))
        response = self.client.get(reverse("characters:wraith:update:guild", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)
