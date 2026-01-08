"""Tests for AutocompleteTextInput widget."""

import json
import re

from django.test import TestCase

from core.widgets import AutocompleteTextInput


class AutocompleteTextInputTests(TestCase):
    """Tests for the AutocompleteTextInput widget."""

    def test_render_basic(self):
        """Test basic rendering with simple name and suggestions."""
        widget = AutocompleteTextInput(suggestions=["apple", "banana", "cherry"])
        html = widget.render("fruit", "")

        self.assertIn("<input", html)
        self.assertIn("<script>", html)
        self.assertIn('["apple", "banana", "cherry"]', html)

    def test_render_empty_suggestions(self):
        """Test rendering with no suggestions."""
        widget = AutocompleteTextInput(suggestions=[])
        html = widget.render("field_name", "")

        self.assertIn("<input", html)
        self.assertIn("<script>", html)
        self.assertIn("[]", html)

    def test_render_no_suggestions(self):
        """Test rendering when suggestions is None."""
        widget = AutocompleteTextInput()
        html = widget.render("field_name", "")

        self.assertIn("<input", html)
        self.assertIn("[]", html)

    def test_render_with_value(self):
        """Test rendering with an initial value."""
        widget = AutocompleteTextInput(suggestions=["test"])
        html = widget.render("field_name", "initial_value")

        self.assertIn("initial_value", html)

    def test_suggestions_json_escaped(self):
        """Test that suggestions with special characters are properly JSON escaped."""
        suggestions = ['He said "hello"', "It's fine", "back\\slash"]
        widget = AutocompleteTextInput(suggestions=suggestions)
        html = widget.render("test_field", "")

        # The suggestions should be valid JSON
        self.assertIn(json.dumps(suggestions), html)

    def test_field_name_with_special_chars_escaped(self):
        """Test that field names with special characters are safely escaped.

        Even though field names typically come from developer-controlled code,
        the widget should handle edge cases defensively.
        """
        widget = AutocompleteTextInput(suggestions=["test"])

        # Test with quotes in field name
        html = widget.render('field"name', "")
        # The rendered HTML should not have unescaped quotes that break JS
        self.assertIn("<script>", html)
        # Check that the name is properly escaped in JavaScript context
        self.assertNotIn('input[name="field"name"]', html)

    def test_field_name_with_backslash_escaped(self):
        """Test that backslashes in field names are properly escaped."""
        widget = AutocompleteTextInput(suggestions=["test"])
        html = widget.render("field\\name", "")

        # Should not break the JavaScript
        self.assertIn("<script>", html)
        # The backslash should be escaped in the JavaScript string
        self.assertIn("\\\\", html)

    def test_field_name_with_single_quotes_escaped(self):
        """Test that single quotes in field names are handled."""
        widget = AutocompleteTextInput(suggestions=["test"])
        html = widget.render("field'name", "")

        self.assertIn("<script>", html)

    def test_get_context_includes_suggestions(self):
        """Test that get_context includes suggestions in widget context."""
        widget = AutocompleteTextInput(suggestions=["a", "b", "c"])
        context = widget.get_context("test", "", {})

        self.assertEqual(context["widget"]["suggestions"], ["a", "b", "c"])

    def test_jquery_selector_uses_name(self):
        """Test that the jQuery selector properly targets the input by name."""
        widget = AutocompleteTextInput(suggestions=["test"])
        html = widget.render("my_field", "")

        # Should have proper selector structure
        self.assertIn("input[name=", html)
        self.assertIn("my_field", html)

    def test_autocomplete_minlength(self):
        """Test that autocomplete has minLength set to 2."""
        widget = AutocompleteTextInput(suggestions=["test"])
        html = widget.render("field", "")

        self.assertIn("minLength: 2", html)
