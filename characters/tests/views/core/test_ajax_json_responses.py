"""
Tests for AJAX views returning JSON responses.

These tests verify that AJAX endpoints return properly formatted JSON
responses instead of HTML fragments, to prevent XSS vulnerabilities.

Also tests that AJAX views properly require authentication and return
appropriate error responses for unauthenticated users.
"""

import json

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background
from characters.models.core.merit_flaw_block import MeritFlaw
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestLoadExamplesJsonResponse(TestCase):
    """Test that load_examples returns JSON instead of HTML."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.client.login(username="testuser", password="password")

        # Create test data
        Attribute.objects.get_or_create(name="Strength", property_name="strength")
        Attribute.objects.get_or_create(name="Dexterity", property_name="dexterity")

    def test_returns_json_content_type(self):
        """Test that response has JSON content type."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Attribute"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_returns_options_structure(self):
        """Test that response has options array structure."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Attribute"},
        )
        data = json.loads(response.content)

        self.assertIn("options", data)
        self.assertIsInstance(data["options"], list)

    def test_options_have_value_and_label(self):
        """Test that each option has value and label keys."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Attribute"},
        )
        data = json.loads(response.content)

        for option in data["options"]:
            self.assertIn("value", option)
            self.assertIn("label", option)


class TestLoadValuesJsonResponse(TestCase):
    """Test that load_values returns JSON instead of HTML."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.client.login(username="testuser", password="password")

        # Create a merit/flaw with ratings
        self.mf = MeritFlaw.objects.create(name="Test Merit", max_rating=3)

    def test_returns_json_content_type(self):
        """Test that response has JSON content type."""
        response = self.client.get(
            reverse("characters:ajax:load_values"),
            {"example": self.mf.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_returns_values_structure(self):
        """Test that response has values array structure."""
        response = self.client.get(
            reverse("characters:ajax:load_values"),
            {"example": self.mf.pk},
        )
        data = json.loads(response.content)

        self.assertIn("values", data)
        self.assertIsInstance(data["values"], list)


class TestMageLoadMfRatingsJsonResponse(TestCase):
    """Test that load_mf_ratings returns JSON instead of HTML."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.client.login(username="testuser", password="password")

        # Create a merit/flaw
        self.mf = MeritFlaw.objects.create(name="Test Flaw", max_rating=-3)

    def test_returns_json_content_type(self):
        """Test that response has JSON content type."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_mf_ratings"),
            {"mf": self.mf.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_returns_values_structure(self):
        """Test that response has values array structure."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_mf_ratings"),
            {"mf": self.mf.pk},
        )
        data = json.loads(response.content)

        self.assertIn("values", data)
        self.assertIsInstance(data["values"], list)


class TestAjaxAuthenticationRequired(TestCase):
    """Test that all AJAX views require authentication."""

    def setUp(self):
        self.client = Client()
        # Create test data
        Attribute.objects.get_or_create(name="Strength", property_name="strength")

    def test_load_examples_requires_auth(self):
        """Test that load_examples returns 401 for unauthenticated users."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Attribute"},
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_load_values_requires_auth(self):
        """Test that load_values returns 401 for unauthenticated users."""
        mf = MeritFlaw.objects.create(name="Test Merit", max_rating=3)
        response = self.client.get(
            reverse("characters:ajax:load_values"),
            {"example": mf.pk},
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn("error", data)


class TestLoadExamplesCategories(TestCase):
    """Test that load_examples returns correct data for different categories."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.client.login(username="testuser", password="password")

        # Create test data for each category
        Attribute.objects.get_or_create(name="Strength", property_name="strength")
        Ability.objects.get_or_create(name="Alertness", property_name="alertness")
        Background.objects.get_or_create(name="Allies", property_name="allies")
        MeritFlaw.objects.create(name="Test Merit", max_rating=3)

    def test_load_attributes(self):
        """Test loading Attribute category."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Attribute"},
        )
        data = json.loads(response.content)
        self.assertIn("options", data)
        self.assertGreater(len(data["options"]), 0)

    def test_load_abilities(self):
        """Test loading Ability category."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Ability"},
        )
        data = json.loads(response.content)
        self.assertIn("options", data)
        self.assertGreater(len(data["options"]), 0)

    def test_load_backgrounds(self):
        """Test loading Background category."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Background"},
        )
        data = json.loads(response.content)
        self.assertIn("options", data)
        self.assertGreater(len(data["options"]), 0)

    def test_load_meritflaws(self):
        """Test loading MeritFlaw category."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "MeritFlaw"},
        )
        data = json.loads(response.content)
        self.assertIn("options", data)
        self.assertGreater(len(data["options"]), 0)

    def test_invalid_category_returns_empty(self):
        """Test that invalid category returns empty options list."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "InvalidCategory"},
        )
        data = json.loads(response.content)
        self.assertIn("options", data)
        self.assertEqual(len(data["options"]), 0)
