"""Tests for human views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.human import Human


class TestHumanDetailView(TestCase):
    """Test HumanDetailView permissions and 404 handling."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.owner,
            status="App",
        )

    def test_detail_view_returns_404_for_invalid_pk(self):
        """Test that detail view returns 404 for non-existent character."""
        self.client.login(username="owner", password="password")
        response = self.client.get(reverse("characters:character", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)


class TestHumanChargenView(TestCase):
    """Test HumanChargenView 404 handling."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )

    def test_chargen_view_returns_404_for_invalid_pk(self):
        """Test that chargen view returns 404 for non-existent character."""
        self.client.login(username="owner", password="password")
        response = self.client.get(reverse("characters:update:human", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)
