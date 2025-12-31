"""Tests for DemonFaction views."""

from characters.models.demon.faction import DemonFaction
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestFactionDetailView(TestCase):
    """Test FactionDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.faction = DemonFaction.objects.create(
            name="Cryptics",
            philosophy="Seek knowledge",
            owner=self.user,
        )

    def test_detail_view_accessible_when_logged_in(self):
        """Test that faction detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.faction.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.faction.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/faction/detail.html")


class TestFactionListView(TestCase):
    """Test FactionListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that faction list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:faction")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_factions(self):
        """Test that list view shows factions."""
        faction = DemonFaction.objects.create(name="Cryptics", owner=self.user)
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:faction")
        response = self.client.get(url)
        self.assertContains(response, "Cryptics")


class TestFactionCreateView(TestCase):
    """Test FactionCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that faction create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:faction")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestFactionUpdateView(TestCase):
    """Test FactionUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.faction = DemonFaction.objects.create(name="Cryptics", owner=self.user)

    def test_update_view_accessible_when_logged_in(self):
        """Test that faction update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.faction.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestFaction404Handling(TestCase):
    """Test 404 error handling for faction views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_faction_detail_returns_404_for_invalid_pk(self):
        """Test that faction detail returns 404 for non-existent faction."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:demon:faction", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_faction_update_returns_404_for_invalid_pk(self):
        """Test that faction update returns 404 for non-existent faction."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:demon:update:faction", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)
