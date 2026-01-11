"""Tests for URL namespace configuration."""

from django.test import TestCase
from django.urls import resolve, reverse


class CoreNamespaceTest(TestCase):
    """Tests for core app URL namespace."""

    def test_core_namespace_exists(self):
        """Test that core namespace is accessible."""
        url = reverse("core:home")
        self.assertEqual(url, "/")

    def test_core_book_urls_use_namespace(self):
        """Test that book URLs use core namespace."""
        url = reverse("core:index_book")
        self.assertEqual(url, "/book/")

    def test_core_language_urls_use_namespace(self):
        """Test that language URLs use core namespace."""
        url = reverse("core:index_language")
        self.assertEqual(url, "/language/")


class AccountsNamespaceTest(TestCase):
    """Tests for accounts app URL namespace."""

    def test_accounts_namespace_exists(self):
        """Test that accounts namespace is accessible."""
        url = reverse("accounts:signup")
        self.assertEqual(url, "/accounts/signup/")

    def test_accounts_profile_urls_use_namespace(self):
        """Test that profile URLs use accounts namespace."""
        url = reverse("accounts:profile", kwargs={"pk": 1})
        self.assertEqual(url, "/accounts/profile/1/")

    def test_accounts_profile_update_url(self):
        """Test that profile update URL resolves correctly."""
        url = reverse("accounts:profile_update", kwargs={"pk": 1})
        self.assertEqual(url, "/accounts/profile/update/1/")


class GameNamespaceTest(TestCase):
    """Tests for game app URL namespace."""

    def test_game_namespace_exists(self):
        """Test that game namespace is accessible."""
        url = reverse("game:chronicles")
        self.assertEqual(url, "/game/chronicles/")

    def test_game_nested_namespaces(self):
        """Test that game nested namespaces work correctly."""
        url = reverse("game:story:list")
        self.assertEqual(url, "/game/story/list/")


class CharactersNamespaceTest(TestCase):
    """Tests for characters app URL namespace."""

    def test_characters_namespace_exists(self):
        """Test that characters namespace is accessible."""
        url = reverse("characters:index")
        self.assertEqual(url, "/characters/index/")

    def test_characters_list_namespace(self):
        """Test that characters:list namespace is accessible."""
        resolver = resolve("/characters/list/")
        self.assertIsNotNone(resolver)

    def test_characters_ajax_namespace(self):
        """Test that characters:ajax namespace is accessible."""
        resolver = resolve("/characters/ajax/")
        self.assertIsNotNone(resolver)

    def test_characters_create_namespace(self):
        """Test that characters:create namespace is accessible."""
        resolver = resolve("/characters/create/")
        self.assertIsNotNone(resolver)


class LocationsNamespaceTest(TestCase):
    """Tests for locations app URL namespace."""

    def test_locations_namespace_exists(self):
        """Test that locations namespace is accessible."""
        url = reverse("locations:index")
        self.assertEqual(url, "/locations/index/")


class ItemsNamespaceTest(TestCase):
    """Tests for items app URL namespace."""

    def test_items_namespace_exists(self):
        """Test that items namespace is accessible."""
        url = reverse("items:index")
        self.assertEqual(url, "/items/index/")
