"""Tests for location_tags template tag."""

from unittest.mock import MagicMock

from django.test import TestCase

from locations.templatetags.location_tags import show_location


class ShowLocationTagTest(TestCase):
    """Tests for show_location inclusion tag."""

    def test_returns_context_with_location(self):
        """Test tag returns context containing the location."""
        mock_location = MagicMock()
        mock_location.name = "Test Location"

        result = show_location(mock_location)

        self.assertIn("location", result)
        self.assertEqual(result["location"], mock_location)

    def test_returns_context_with_default_indent_level(self):
        """Test tag returns default indent_level of 0."""
        mock_location = MagicMock()

        result = show_location(mock_location)

        self.assertIn("indent_level", result)
        self.assertEqual(result["indent_level"], 0)

    def test_returns_context_with_custom_indent_level(self):
        """Test tag returns custom indent_level when specified."""
        mock_location = MagicMock()

        result = show_location(mock_location, indent_level=30)

        self.assertEqual(result["indent_level"], 30)

    def test_supports_nested_indent_levels(self):
        """Test tag supports various indent levels for nesting."""
        mock_location = MagicMock()

        for level in [0, 30, 60, 90, 120]:
            result = show_location(mock_location, indent_level=level)
            self.assertEqual(result["indent_level"], level)

    def test_preserves_location_attributes(self):
        """Test that location object is passed through unchanged."""
        mock_location = MagicMock()
        mock_location.id = 42
        mock_location.name = "Haunted House"
        mock_location.get_absolute_url.return_value = "/locations/42/"

        result = show_location(mock_location)

        self.assertEqual(result["location"].id, 42)
        self.assertEqual(result["location"].name, "Haunted House")
        self.assertEqual(
            result["location"].get_absolute_url(),
            "/locations/42/"
        )

    def test_context_keys(self):
        """Test tag returns exactly the expected context keys."""
        mock_location = MagicMock()

        result = show_location(mock_location)

        self.assertEqual(set(result.keys()), {"location", "indent_level"})
