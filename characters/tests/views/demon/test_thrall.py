"""Tests for Thrall views."""

from characters.models.demon.thrall import Thrall
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestThrallDetailView(TestCase):
    """Test ThrallDetailView permissions and functionality."""

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

        self.thrall = Thrall.objects.create(
            name="Test Thrall",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that thrall detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.thrall.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that thrall detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.thrall.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.thrall.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404 (not login redirect)."""
        response = self.client.get(self.thrall.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used for thrall detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.thrall.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/thrall/detail.html")


class TestThrallCreateView(TestCase):
    """Test ThrallCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that thrall create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:thrall")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_redirects_when_not_logged_in(self):
        """Test that create view redirects when not logged in."""
        url = reverse("characters:demon:create:thrall")
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])


class TestThrallUpdateView(TestCase):
    """Test ThrallUpdateView permissions and functionality."""

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

        self.thrall = Thrall.objects.create(
            name="Test Thrall",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_full_update_view_denied_to_owner(self):
        """Test that full update is denied to owners (ST-only)."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:demon:update:thrall_full", kwargs={"pk": self.thrall.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_full_update_view_accessible_to_st(self):
        """Test that full thrall update view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        url = reverse("characters:demon:update:thrall_full", kwargs={"pk": self.thrall.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_full_update_view_denied_to_other_users(self):
        """Test that full thrall update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse("characters:demon:update:thrall_full", kwargs={"pk": self.thrall.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])


class TestThrallListView(TestCase):
    """Test ThrallListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_list_view_accessible_when_logged_in(self):
        """Test that thrall list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:thrall")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_own_characters(self):
        """Test that list view shows user's own characters."""
        thrall = Thrall.objects.create(
            name="My Thrall", owner=self.user, status="App"
        )
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:thrall")
        response = self.client.get(url)
        self.assertContains(response, "My Thrall")


class TestThrall404Handling(TestCase):
    """Test 404 error handling for thrall views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_thrall_detail_returns_404_for_invalid_pk(self):
        """Test that thrall detail returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:thrall", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_thrall_update_returns_404_for_invalid_pk(self):
        """Test that thrall update returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:update:thrall_full", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
