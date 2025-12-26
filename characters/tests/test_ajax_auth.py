"""
Tests for AJAX view authentication requirements.

Tests verify that all AJAX endpoints require authentication to prevent
unauthorized access to game data.
"""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestMageAjaxAuthenticationRequired(TestCase):
    """Test that Mage AJAX views require authentication."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def assertRequiresAuth(self, response):
        """Assert that the response indicates authentication is required.

        The application may return either:
        - 302 redirect to login page
        - 401 Unauthorized for AJAX requests
        """
        self.assertIn(
            response.status_code,
            [302, 401],
            f"Expected 302 or 401, got {response.status_code}",
        )
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_load_factions_requires_auth(self):
        """Test that load_factions view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_factions"),
            {"affiliation": "1"},
        )
        self.assertRequiresAuth(response)

    def test_load_factions_accessible_when_logged_in(self):
        """Test that load_factions is accessible when authenticated."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_factions"),
            {"affiliation": "1"},
        )
        # Should be accessible (may return empty results)
        self.assertIn(response.status_code, [200, 404])

    def test_load_subfactions_requires_auth(self):
        """Test that load_subfactions view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_subfactions"),
            {"faction": "1"},
        )
        self.assertRequiresAuth(response)

    def test_load_mf_ratings_requires_auth(self):
        """Test that load_mf_ratings view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_mf_ratings"),
            {"mf": "1"},
        )
        self.assertRequiresAuth(response)

    def test_get_abilities_requires_auth(self):
        """Test that get_abilities view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:get_abilities"),
            {"object": "1", "practice_id": "1"},
        )
        self.assertRequiresAuth(response)

    def test_load_attributes_requires_auth(self):
        """Test that load_attributes view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_attributes"),
            {"fellowship": "1"},
        )
        self.assertRequiresAuth(response)

    def test_load_affinities_requires_auth(self):
        """Test that load_affinities view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_affinities"),
            {"fellowship": "1"},
        )
        self.assertRequiresAuth(response)

    def test_load_sorcerer_examples_requires_auth(self):
        """Test that sorcerer LoadExamplesView requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_sorcerer_examples"),
            {"category": "Attribute", "object": "1"},
        )
        self.assertRequiresAuth(response)

    def test_load_companion_examples_requires_auth(self):
        """Test that companion LoadExamplesView requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_companion_examples"),
            {"category": "Attribute", "object": "1"},
        )
        self.assertRequiresAuth(response)

    def test_load_advantage_values_requires_auth(self):
        """Test that load_companion_values view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:load_advantage_values"),
            {"example": "1"},
        )
        self.assertRequiresAuth(response)

    def test_get_practice_abilities_requires_auth(self):
        """Test that sorcerer get_abilities view requires authentication."""
        response = self.client.get(
            reverse("characters:mage:ajax:get_practice_abilities"),
            {"practice_id": "1"},
        )
        self.assertRequiresAuth(response)


class TestCoreAjaxAuthenticationRequired(TestCase):
    """Test that Core AJAX views require authentication."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def assertRequiresAuth(self, response):
        """Assert that the response indicates authentication is required.

        The application may return either:
        - 302 redirect to login page
        - 401 Unauthorized for AJAX requests
        """
        self.assertIn(
            response.status_code,
            [302, 401],
            f"Expected 302 or 401, got {response.status_code}",
        )
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_load_examples_requires_auth(self):
        """Test that load_examples view requires authentication."""
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Attribute"},
        )
        self.assertRequiresAuth(response)

    def test_load_examples_accessible_when_logged_in(self):
        """Test that load_examples is accessible when authenticated."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:ajax:load_examples"),
            {"category": "Attribute"},
        )
        # Should be accessible
        self.assertEqual(response.status_code, 200)

    def test_load_values_requires_auth(self):
        """Test that load_values view requires authentication."""
        response = self.client.get(
            reverse("characters:ajax:load_values"),
            {"example": "1"},
        )
        self.assertRequiresAuth(response)
