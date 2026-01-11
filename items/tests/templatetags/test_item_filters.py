"""Tests for item_filters template tag filter."""

from django.template import Context, Template
from django.test import TestCase

from items.templatetags.item_filters import replace_underscore


class ReplaceUnderscoreFilterTest(TestCase):
    """Tests for replace_underscore filter."""

    def test_replaces_single_underscore(self):
        """Test filter replaces a single underscore with space."""
        result = replace_underscore("hello_world")
        self.assertEqual(result, "hello world")

    def test_replaces_multiple_underscores(self):
        """Test filter replaces multiple underscores with spaces."""
        result = replace_underscore("one_two_three_four")
        self.assertEqual(result, "one two three four")

    def test_returns_empty_string_unchanged(self):
        """Test filter returns empty string unchanged."""
        result = replace_underscore("")
        self.assertEqual(result, "")

    def test_returns_none_for_none_input(self):
        """Test filter returns None for None input."""
        result = replace_underscore(None)
        self.assertIsNone(result)

    def test_returns_falsy_values_unchanged(self):
        """Test filter returns falsy values unchanged."""
        result = replace_underscore(0)
        self.assertEqual(result, 0)

    def test_converts_non_string_to_string(self):
        """Test filter converts non-string types to string before replacement."""
        # Integer with no underscores returns as string
        result = replace_underscore(123)
        self.assertEqual(result, "123")

    def test_handles_consecutive_underscores(self):
        """Test filter handles consecutive underscores."""
        result = replace_underscore("hello__world")
        self.assertEqual(result, "hello  world")

    def test_handles_leading_underscore(self):
        """Test filter handles leading underscore."""
        result = replace_underscore("_private")
        self.assertEqual(result, " private")

    def test_handles_trailing_underscore(self):
        """Test filter handles trailing underscore."""
        result = replace_underscore("test_")
        self.assertEqual(result, "test ")

    def test_no_underscore_unchanged(self):
        """Test filter returns string without underscores unchanged."""
        result = replace_underscore("no change")
        self.assertEqual(result, "no change")

    def test_only_underscores(self):
        """Test filter handles string of only underscores."""
        result = replace_underscore("___")
        self.assertEqual(result, "   ")


class ReplaceUnderscoreTemplateTest(TestCase):
    """Tests for replace_underscore filter usage in templates."""

    def test_filter_in_template(self):
        """Test filter can be used in Django templates."""
        template = Template("{% load item_filters %}{{ item_type|replace_underscore }}")
        context = Context({"item_type": "long_sword"})
        result = template.render(context)
        self.assertEqual(result.strip(), "long sword")

    def test_filter_in_template_with_title_case(self):
        """Test filter combined with title case in template."""
        template = Template("{% load item_filters %}{{ item_type|replace_underscore|title }}")
        context = Context({"item_type": "battle_axe"})
        result = template.render(context)
        self.assertEqual(result.strip(), "Battle Axe")

    def test_filter_with_empty_context(self):
        """Test filter handles empty string in template context."""
        template = Template("{% load item_filters %}[{{ item_type|replace_underscore }}]")
        context = Context({"item_type": ""})
        result = template.render(context)
        self.assertEqual(result.strip(), "[]")
