"""Tests for get_specialty template tag filter."""

from unittest.mock import MagicMock

from characters.templatetags.get_specialty import get_specialty
from django.template import Context, Template
from django.test import TestCase


class GetSpecialtyFilterTest(TestCase):
    """Tests for get_specialty filter."""

    def test_returns_specialty_name_when_present(self):
        """Test filter returns specialty name when character has specialty for stat."""
        mock_character = MagicMock()
        mock_character.get_specialty.return_value = "Fast Draw"

        result = get_specialty(mock_character, "firearms")

        self.assertEqual(result, "Fast Draw")
        mock_character.get_specialty.assert_called_once_with("firearms")

    def test_returns_none_when_no_specialty(self):
        """Test filter returns None when character has no specialty for stat."""
        mock_character = MagicMock()
        mock_character.get_specialty.return_value = None

        result = get_specialty(mock_character, "brawl")

        self.assertIsNone(result)
        mock_character.get_specialty.assert_called_once_with("brawl")

    def test_passes_stat_correctly(self):
        """Test filter passes stat parameter correctly to character method."""
        mock_character = MagicMock()
        mock_character.get_specialty.return_value = "Swords"

        get_specialty(mock_character, "melee")

        mock_character.get_specialty.assert_called_once_with("melee")

    def test_handles_different_stat_names(self):
        """Test filter works with various stat names."""
        mock_character = MagicMock()
        mock_character.get_specialty.return_value = "Running"

        result = get_specialty(mock_character, "athletics")

        self.assertEqual(result, "Running")


class GetSpecialtyTemplateTest(TestCase):
    """Tests for get_specialty filter usage in templates."""

    def test_filter_in_template_with_specialty(self):
        """Test filter can be used in Django templates with a specialty present."""
        mock_character = MagicMock()
        mock_character.get_specialty.return_value = "Shotguns"

        template = Template(
            "{% load get_specialty %}{{ character|get_specialty:'firearms' }}"
        )
        context = Context({"character": mock_character})
        result = template.render(context)

        self.assertEqual(result.strip(), "Shotguns")

    def test_filter_in_template_no_specialty(self):
        """Test filter renders correctly when no specialty exists."""
        mock_character = MagicMock()
        mock_character.get_specialty.return_value = None

        template = Template(
            "{% load get_specialty %}{% if character|get_specialty:'brawl' %}Has specialty{% else %}No specialty{% endif %}"
        )
        context = Context({"character": mock_character})
        result = template.render(context)

        self.assertEqual(result.strip(), "No specialty")

    def test_filter_conditional_display(self):
        """Test filter in conditional template logic."""
        mock_character = MagicMock()
        mock_character.get_specialty.return_value = "Swimming"

        template = Template(
            "{% load get_specialty %}{% with spec=character|get_specialty:'athletics' %}{% if spec %}Specialty: {{ spec }}{% endif %}{% endwith %}"
        )
        context = Context({"character": mock_character})
        result = template.render(context)

        self.assertIn("Specialty: Swimming", result)
