"""Tests for startswith template tag filter."""

from django.template import Context, Template
from django.test import TestCase

from characters.templatetags.startswith import startswith


class StartsWithFilterTest(TestCase):
    """Tests for startswith filter."""

    def test_returns_true_for_matching_prefix(self):
        """Test filter returns True when string starts with prefix."""
        result = startswith("hello world", "hello")
        self.assertTrue(result)

    def test_returns_false_for_non_matching_prefix(self):
        """Test filter returns False when string doesn't start with prefix."""
        result = startswith("hello world", "world")
        self.assertFalse(result)

    def test_returns_true_for_empty_prefix(self):
        """Test filter returns True for empty prefix (all strings start with empty string)."""
        result = startswith("hello", "")
        self.assertTrue(result)

    def test_returns_false_for_empty_string_non_empty_prefix(self):
        """Test filter returns False for empty string with non-empty prefix."""
        result = startswith("", "hello")
        self.assertFalse(result)

    def test_returns_true_for_both_empty(self):
        """Test filter returns True when both string and prefix are empty."""
        result = startswith("", "")
        self.assertTrue(result)

    def test_case_sensitive(self):
        """Test filter is case-sensitive."""
        result = startswith("Hello", "hello")
        self.assertFalse(result)

    def test_exact_match(self):
        """Test filter returns True when string exactly equals prefix."""
        result = startswith("test", "test")
        self.assertTrue(result)

    def test_prefix_longer_than_string(self):
        """Test filter returns False when prefix is longer than string."""
        result = startswith("hi", "hello")
        self.assertFalse(result)

    def test_single_character(self):
        """Test filter works with single character strings."""
        self.assertTrue(startswith("a", "a"))
        self.assertFalse(startswith("a", "b"))


class StartsWithTemplateTest(TestCase):
    """Tests for startswith filter usage in templates."""

    def test_filter_in_template(self):
        """Test filter can be used in Django templates."""
        template = Template('{% load startswith %}{% if name|startswith:"Mr" %}Title{% endif %}')
        context = Context({"name": "Mr. Smith"})
        result = template.render(context)
        self.assertEqual(result.strip(), "Title")

    def test_filter_in_template_false_case(self):
        """Test filter returns correctly when prefix doesn't match in template."""
        template = Template(
            '{% load startswith %}{% if name|startswith:"Dr" %}Doctor{% else %}No title{% endif %}'
        )
        context = Context({"name": "Mr. Smith"})
        result = template.render(context)
        self.assertEqual(result.strip(), "No title")
