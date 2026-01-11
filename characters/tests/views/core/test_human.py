"""Tests for human views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from core.models import Number
from game.models import ObjectType


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


class TestLoadValuesView(TestCase):
    """Test load_values AJAX view 404 handling."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chartype, _ = ObjectType.objects.get_or_create(
            name="human", defaults={"type": "char", "gameline": "wod"}
        )
        self.mf = MeritFlaw.objects.create(name="Test Merit")
        self.mf.allowed_types.add(self.chartype)
        # Add ratings via Number model
        num1, _ = Number.objects.get_or_create(value=1)
        num2, _ = Number.objects.get_or_create(value=2)
        self.mf.ratings.add(num1, num2)

        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
        )

    def test_load_values_returns_404_for_invalid_meritflaw(self):
        """Test that load_values returns 404 for non-existent merit/flaw."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:ajax:load_values"),
            {"example": 99999},
        )
        self.assertEqual(response.status_code, 404)

    def test_load_values_returns_404_for_invalid_character(self):
        """Test that load_values returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:ajax:load_values"),
            {"example": self.mf.pk, "object": 99999},
        )
        self.assertEqual(response.status_code, 404)

    def test_load_values_returns_200_for_valid_meritflaw(self):
        """Test that load_values returns 200 for valid merit/flaw."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:ajax:load_values"),
            {"example": self.mf.pk},
        )
        self.assertEqual(response.status_code, 200)


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
