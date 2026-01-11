"""Tests for Lore views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.demon.lore import Lore


class TestLoreDetailView(TestCase):
    """Test LoreDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.lore = Lore.objects.create(
            name="Lore of Flame",
            property_name="flame",
            description="Control fire",
            owner=self.user,
        )

    def test_detail_view_accessible_when_logged_in(self):
        """Test that lore detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.lore.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.lore.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/lore/detail.html")


class TestLoreListView(TestCase):
    """Test LoreListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that lore list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:lore")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_lores(self):
        """Test that list view shows lores."""
        lore = Lore.objects.create(name="Lore of Flame", property_name="flame", owner=self.user)
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:lore")
        response = self.client.get(url)
        self.assertContains(response, "Lore of Flame")


class TestLoreCreateView(TestCase):
    """Test LoreCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that lore create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:lore")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestLoreUpdateView(TestCase):
    """Test LoreUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.lore = Lore.objects.create(
            name="Lore of Flame", property_name="flame", owner=self.user
        )

    def test_update_view_accessible_when_logged_in(self):
        """Test that lore update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.lore.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestLore404Handling(TestCase):
    """Test 404 error handling for lore views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_lore_detail_returns_404_for_invalid_pk(self):
        """Test that lore detail returns 404 for non-existent lore."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:demon:lore", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_lore_update_returns_404_for_invalid_pk(self):
        """Test that lore update returns 404 for non-existent lore."""
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("characters:demon:update:lore", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)
