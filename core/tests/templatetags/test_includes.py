"""Tests for the get_specialty template filter."""

from django.template import Context, Template
from django.test import TestCase


class MockCharacter:
    """Mock character for testing get_specialty filter."""

    def __init__(self, specialties=None):
        self.specialties = specialties or {}

    def get_specialty(self, stat):
        return self.specialties.get(stat, "")


class TestGetSpecialtyFilter(TestCase):
    """Test the get_specialty template filter in core."""

    def test_get_specialty_filter_returns_specialty(self):
        """Test that get_specialty filter returns the specialty."""
        character = MockCharacter(specialties={"firearms": "Rifles"})
        template = Template(
            "{% load get_specialty %}{{ character|get_specialty:'firearms' }}"
        )
        result = template.render(Context({"character": character}))
        self.assertEqual(result.strip(), "Rifles")

    def test_get_specialty_filter_returns_empty_for_no_specialty(self):
        """Test that get_specialty filter returns empty for missing specialty."""
        character = MockCharacter(specialties={})
        template = Template(
            "{% load get_specialty %}{{ character|get_specialty:'brawl' }}"
        )
        result = template.render(Context({"character": character}))
        self.assertEqual(result.strip(), "")

    def test_get_specialty_filter_in_conditional(self):
        """Test get_specialty filter usage in conditional."""
        character = MockCharacter(specialties={"athletics": "Running"})
        template = Template(
            "{% load get_specialty %}{% if character|get_specialty:'athletics' %}Has specialty{% else %}No specialty{% endif %}"
        )
        result = template.render(Context({"character": character}))
        self.assertEqual(result.strip(), "Has specialty")
