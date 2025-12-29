"""Tests for Demon views."""

from characters.models.demon import Demon
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.visage import Visage
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestDemonDetailView(TestCase):
    """Test DemonDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.demon = Demon.objects.create(
            name="Test Demon",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that demon detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.demon.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that demon detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.demon.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.demon.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404 (not login redirect)."""
        response = self.client.get(self.demon.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used for demon detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.demon.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/demon/detail.html")

    def test_detail_view_unapproved_hidden_from_others(self):
        """Test that unapproved characters are hidden from non-owners."""
        unapproved = Demon.objects.create(
            name="Unapproved Demon",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.client.login(username="other", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        self.assertIn(response.status_code, [403, 404])

    def test_detail_view_unapproved_visible_to_owner(self):
        """Test that unapproved characters are visible to owners."""
        unapproved = Demon.objects.create(
            name="Unapproved Demon",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestDemonCreateView(TestCase):
    """Test DemonCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.faction = DemonFaction.objects.create(name="Cryptics", owner=self.user)
        self.visage = Visage.objects.create(name="Bel", owner=self.user)

    def test_create_view_accessible_when_logged_in(self):
        """Test that demon create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:demon")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_redirects_when_not_logged_in(self):
        """Test that create view redirects when not logged in."""
        url = reverse("characters:demon:create:demon")
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used for demon create view."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:demon")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/demon/demon/demonbasics.html")


class TestDemonUpdateView(TestCase):
    """Test DemonUpdateView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.demon = Demon.objects.create(
            name="Test Demon",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_full_update_view_denied_to_owner(self):
        """Test that full update is denied to owners (ST-only)."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:demon:update:demon_full", kwargs={"pk": self.demon.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_full_update_view_accessible_to_st(self):
        """Test that full demon update view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        url = reverse("characters:demon:update:demon_full", kwargs={"pk": self.demon.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_full_update_view_denied_to_other_users(self):
        """Test that full demon update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse("characters:demon:update:demon_full", kwargs={"pk": self.demon.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])


class TestDemonListView(TestCase):
    """Test DemonListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_list_view_accessible_when_logged_in(self):
        """Test that demon list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:demon")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_own_characters(self):
        """Test that list view shows user's own characters."""
        demon = Demon.objects.create(
            name="My Demon", owner=self.user, status="App"
        )
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:demon")
        response = self.client.get(url)
        self.assertContains(response, "My Demon")

    def test_list_view_hides_other_users_characters(self):
        """Test that list view hides other users' characters."""
        other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        demon = Demon.objects.create(
            name="Other Demon", owner=other_user, status="App"
        )
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:demon")
        response = self.client.get(url)
        self.assertNotContains(response, "Other Demon")


class TestDemon404Handling(TestCase):
    """Test 404 error handling for demon views with invalid IDs."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_demon_detail_returns_404_for_invalid_pk(self):
        """Test that demon detail returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:demon", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_demon_update_returns_404_for_invalid_pk(self):
        """Test that demon update returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:update:demon", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_demon_full_update_returns_404_for_invalid_pk(self):
        """Test that demon full update returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:update:demon_full", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
