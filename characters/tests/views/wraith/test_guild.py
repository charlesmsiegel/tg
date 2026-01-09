"""Tests for Guild views."""

from characters.models.wraith.guild import Guild
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestGuildDetailView(TestCase):
    """Test GuildDetailView permissions and functionality."""

    def setUp(self):
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

    def test_detail_view_accessible_when_logged_in(self):
        """Test that guild detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.guild.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.guild.get_absolute_url())
        self.assertTemplateUsed(response, "characters/wraith/guild/detail.html")


class TestGuildListView(TestCase):
    """Test GuildListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that guild list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:list:guild")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_guilds(self):
        """Test that list view shows guilds."""
        guild = Guild.objects.create(name="Masquers", guild_type="greater", owner=self.user)
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:list:guild")
        response = self.client.get(url)
        self.assertContains(response, "Masquers")


class TestGuildCreateView(TestCase):
    """Test GuildCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_requires_login(self):
        """Test that create view requires login."""
        url = reverse("characters:wraith:create:guild")
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 401, 403])

    def test_create_view_accessible_when_logged_in(self):
        """Test that guild create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:guild")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = reverse("characters:wraith:create:guild")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/guild/form.html")

    def test_create_guild_successfully(self):
        """Test creating a guild successfully."""
        self.client.login(username="user", password="password")
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
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.guild = Guild.objects.create(name="Spooks", guild_type="lesser", owner=self.user)

    def test_update_view_requires_login(self):
        """Test that update view requires login."""
        url = self.guild.get_update_url()
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 401, 403])

    def test_update_view_accessible_when_logged_in(self):
        """Test that guild update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.guild.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        url = self.guild.get_update_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/guild/form.html")

    def test_update_guild_successfully(self):
        """Test updating a guild successfully."""
        self.client.login(username="user", password="password")
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
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_guild_detail_returns_404_for_invalid_pk(self):
        """Test that guild detail returns 404 for non-existent guild."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:wraith:guild", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_guild_update_returns_404_for_invalid_pk(self):
        """Test that guild update returns 404 for non-existent guild."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:wraith:update:guild", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)
