"""Tests for Visage views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.demon.visage import Visage


class TestVisageDetailView(TestCase):
    """Test VisageDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.visage = Visage.objects.create(
            name="Bel",
            owner=self.user,
        )

    def test_detail_view_accessible_when_logged_in(self):
        """Test that visage detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.visage.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.visage.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/visage/detail.html")


class TestVisageListView(TestCase):
    """Test VisageListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that visage list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:visage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_visages(self):
        """Test that list view shows visages."""
        visage = Visage.objects.create(name="Bel", owner=self.user)
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:visage")
        response = self.client.get(url)
        self.assertContains(response, "Bel")


class TestVisageCreateView(TestCase):
    """Test VisageCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that visage create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:visage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVisageUpdateView(TestCase):
    """Test VisageUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.visage = Visage.objects.create(name="Bel", owner=self.user)

    def test_update_view_accessible_when_logged_in(self):
        """Test that visage update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.visage.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVisage404Handling(TestCase):
    """Test 404 error handling for visage views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_visage_detail_returns_404_for_invalid_pk(self):
        """Test that visage detail returns 404 for non-existent visage."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:demon:visage", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_visage_update_returns_404_for_invalid_pk(self):
        """Test that visage update returns 404 for non-existent visage."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:demon:update:visage", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)
