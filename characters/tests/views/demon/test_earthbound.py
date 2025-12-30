"""Tests for Earthbound views."""

from characters.models.demon.earthbound import Earthbound
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestEarthboundDetailView(TestCase):
    """Test EarthboundDetailView permissions and functionality."""

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

        self.earthbound = Earthbound.objects.create(
            name="Test Earthbound",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that earthbound detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.earthbound.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that earthbound detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.earthbound.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.earthbound.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404 (not login redirect)."""
        response = self.client.get(self.earthbound.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used for earthbound detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.earthbound.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/earthbound/detail.html")


class TestEarthboundCreateView(TestCase):
    """Test EarthboundCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that earthbound create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:earthbound")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_redirects_when_not_logged_in(self):
        """Test that create view requires authentication."""
        url = reverse("characters:demon:create:earthbound")
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 401, 403])


class TestEarthboundUpdateView(TestCase):
    """Test EarthboundUpdateView permissions and functionality."""

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

        self.earthbound = Earthbound.objects.create(
            name="Test Earthbound",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )



class TestEarthboundListView(TestCase):
    """Test EarthboundListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_list_view_accessible_when_logged_in(self):
        """Test that earthbound list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:earthbound")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_own_characters(self):
        """Test that list view shows user's own characters."""
        earthbound = Earthbound.objects.create(
            name="My Earthbound", owner=self.user, status="App"
        )
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:earthbound")
        response = self.client.get(url)
        self.assertContains(response, "My Earthbound")


class TestEarthbound404Handling(TestCase):
    """Test 404 error handling for earthbound views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_earthbound_detail_returns_404_for_invalid_pk(self):
        """Test that earthbound detail returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:earthbound", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_earthbound_update_returns_404_for_invalid_pk(self):
        """Test that earthbound update returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:update:earthbound", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
