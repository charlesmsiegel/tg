"""Tests for DemonHouse views."""

from characters.models.demon.house import DemonHouse
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestHouseDetailView(TestCase):
    """Test HouseDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.house = DemonHouse.objects.create(
            name="Devils",
            celestial_name="Namaru",
            starting_torment=4,
            owner=self.user,
        )

    def test_detail_view_accessible_when_logged_in(self):
        """Test that house detail view is accessible when logged in."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.house.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.house.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/house/detail.html")


class TestHouseListView(TestCase):
    """Test HouseListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_list_view_accessible_when_logged_in(self):
        """Test that house list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:house")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_houses(self):
        """Test that list view shows houses."""
        house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:house")
        response = self.client.get(url)
        self.assertContains(response, "Devils")


class TestHouseCreateView(TestCase):
    """Test HouseCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that house create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:house")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestHouseUpdateView(TestCase):
    """Test HouseUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )

    def test_update_view_accessible_when_logged_in(self):
        """Test that house update view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = self.house.get_update_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestHouse404Handling(TestCase):
    """Test 404 error handling for house views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_house_detail_returns_404_for_invalid_pk(self):
        """Test that house detail returns 404 for non-existent house."""
        self.client.login(username="user", password="password")
        response = self.client.get(
            reverse("characters:demon:house", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_house_update_returns_404_for_invalid_pk(self):
        """Test that house update returns 404 for non-existent house."""
        self.client.login(username="user", password="password")
        response = self.client.get(
            reverse("characters:demon:update:house", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
