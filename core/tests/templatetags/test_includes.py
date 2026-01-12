"""
Tests for reusable template includes.

Tests cover:
- stat_row.html for stat display with dots
- stat_card.html for card wrapper
- property_row.html for simple label/value rows
"""

from django.template import Context, Template
from django.test import TestCase


class MockCharacter:
    """Mock character for testing get_specialty filter."""

    def __init__(self, specialties=None):
        self.specialties = specialties or {}

    def get_specialty(self, stat):
        return self.specialties.get(stat, "")


class TestStatRowInclude(TestCase):
    """Test the stat_row.html template include."""

    def test_stat_row_basic(self):
        """Test basic stat row rendering with name and value."""
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Strength" value=3 %}'
        )
        result = template.render(Context({}))
        self.assertIn("Strength", result)
        self.assertIn("●●●○○", result)
        self.assertIn('class="row mb-2"', result)

    def test_stat_row_with_zero_value(self):
        """Test stat row with zero value."""
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Alertness" value=0 %}'
        )
        result = template.render(Context({}))
        self.assertIn("Alertness", result)
        self.assertIn("○○○○○", result)

    def test_stat_row_with_max_value(self):
        """Test stat row with maximum value."""
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Arete" value=5 %}'
        )
        result = template.render(Context({}))
        self.assertIn("Arete", result)
        self.assertIn("●●●●●", result)

    def test_stat_row_with_custom_max_dots(self):
        """Test stat row with custom maximum dots."""
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Willpower" value=7 max_dots=10 %}'
        )
        result = template.render(Context({}))
        self.assertIn("Willpower", result)
        self.assertIn("●●●●●●●○○○", result)

    def test_stat_row_with_specialty_string(self):
        """Test stat row with pre-computed specialty."""
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Firearms" value=4 specialty="Pistols" %}'
        )
        result = template.render(Context({}))
        self.assertIn("Firearms", result)
        self.assertIn("(Pistols)", result)
        self.assertIn("●●●●○", result)

    def test_stat_row_with_property_name_and_object(self):
        """Test stat row with property_name and object for specialty lookup."""
        character = MockCharacter(specialties={"brawl": "Kindred"})
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Brawl" value=3 property_name="brawl" object=character %}'
        )
        result = template.render(Context({"character": character}))
        self.assertIn("Brawl", result)
        self.assertIn("(Kindred)", result)
        self.assertIn("●●●○○", result)

    def test_stat_row_without_specialty(self):
        """Test stat row without any specialty displays correctly."""
        character = MockCharacter(specialties={})
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Athletics" value=2 property_name="athletics" object=character %}'
        )
        result = template.render(Context({"character": character}))
        self.assertIn("Athletics", result)
        self.assertNotIn("()", result)  # No empty parentheses
        self.assertIn("●●○○○", result)

    def test_stat_row_with_custom_col_ratio(self):
        """Test stat row with custom column ratio."""
        template = Template(
            '{% include "core/includes/stat_row.html" with name="Stealth" value=2 col_ratio="4" %}'
        )
        result = template.render(Context({}))
        self.assertIn('class="col-4"', result)


class TestStatCardInclude(TestCase):
    """Test the stat_card.html template include."""

    def test_stat_card_basic(self):
        """Test basic stat card rendering."""
        template = Template(
            '{% include "core/includes/stat_card.html" with title="Talents" heading_class="mta_heading" %}'
        )
        result = template.render(Context({}))
        self.assertIn('class="tg-card"', result)
        self.assertIn("Talents", result)
        self.assertIn("mta_heading", result)
        self.assertIn('class="tg-card-title mb-0"', result)

    def test_stat_card_with_content(self):
        """Test stat card with content variable."""
        template = Template(
            '{% include "core/includes/stat_card.html" with title="Skills" heading_class="vtm_heading" content="<p>Test content</p>" %}'
        )
        result = template.render(Context({}))
        self.assertIn("Skills", result)
        self.assertIn("Test content", result)

    def test_stat_card_with_custom_h_level(self):
        """Test stat card with custom heading level."""
        template = Template(
            '{% include "core/includes/stat_card.html" with title="Knowledges" heading_class="wta_heading" h_level="5" %}'
        )
        result = template.render(Context({}))
        self.assertIn("<h5", result)
        self.assertIn("</h5>", result)

    def test_stat_card_with_full_height(self):
        """Test stat card with full_height option."""
        template = Template(
            '{% include "core/includes/stat_card.html" with title="Test" heading_class="test" full_height=True %}'
        )
        result = template.render(Context({}))
        self.assertIn("h-100", result)

    def test_stat_card_with_card_id_collapsible(self):
        """Test stat card with collapse functionality."""
        template = Template(
            '{% include "core/includes/stat_card.html" with title="Abilities" heading_class="mta_heading" card_id="abilitiesCollapse" %}'
        )
        result = template.render(Context({}))
        self.assertIn('id="abilitiesCollapse"', result)
        self.assertIn('data-toggle="collapse"', result)
        self.assertIn('data-target="#abilitiesCollapse"', result)
        self.assertIn("show", result)  # Not collapsed by default

    def test_stat_card_collapsed(self):
        """Test stat card that starts collapsed."""
        template = Template(
            '{% include "core/includes/stat_card.html" with title="Abilities" heading_class="mta_heading" card_id="test" collapsed=True %}'
        )
        result = template.render(Context({}))
        self.assertIn("collapse", result)
        # When collapsed=True, 'show' class should not appear in the collapse div
        # The div will have 'collapse' but not 'collapse show'
        self.assertIn('class="collapse', result)


class TestPropertyRowInclude(TestCase):
    """Test the property_row.html template include."""

    def test_property_row_basic(self):
        """Test basic property row rendering."""
        template = Template(
            '{% include "core/includes/property_row.html" with label="Concept:" value="Wandering Scholar" %}'
        )
        result = template.render(Context({}))
        self.assertIn("Concept:", result)
        self.assertIn("Wandering Scholar", result)
        self.assertIn('class="row mb-2"', result)

    def test_property_row_with_url(self):
        """Test property row with URL link."""
        template = Template(
            '{% include "core/includes/property_row.html" with label="Nature:" value="Visionary" url="/reference/nature/visionary/" %}'
        )
        result = template.render(Context({}))
        self.assertIn("Nature:", result)
        self.assertIn('href="/reference/nature/visionary/"', result)
        self.assertIn("Visionary</a>", result)

    def test_property_row_without_url(self):
        """Test property row without URL (no anchor tag)."""
        template = Template(
            '{% include "core/includes/property_row.html" with label="Player:" value="John" %}'
        )
        result = template.render(Context({}))
        self.assertIn("Player:", result)
        self.assertIn("John", result)
        self.assertNotIn("<a ", result)

    def test_property_row_with_custom_col_ratio(self):
        """Test property row with custom column ratio."""
        template = Template(
            '{% include "core/includes/property_row.html" with label="Name:" value="Test" col_ratio="4" %}'
        )
        result = template.render(Context({}))
        self.assertIn('class="col-4"', result)

    def test_property_row_with_label_class(self):
        """Test property row with additional label CSS class."""
        template = Template(
            '{% include "core/includes/property_row.html" with label="Important:" value="Value" label_class="font-weight-bold" %}'
        )
        result = template.render(Context({}))
        self.assertIn("font-weight-bold", result)


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
