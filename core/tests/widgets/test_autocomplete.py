"""Tests for AutocompleteTextInput widget."""

from django.test import TestCase

from core.widgets import AutocompleteTextInput


class AutocompleteTextInputTests(TestCase):
    """AutocompleteTextInput offers suggestions through a native <datalist>, no script."""

    def test_render_basic(self):
        widget = AutocompleteTextInput(suggestions=["apple", "banana", "cherry"])
        html = widget.render("fruit", "")

        self.assertIn("<input", html)
        self.assertIn('list="fruit-suggestions"', html)
        self.assertIn('<datalist id="fruit-suggestions">', html)
        for fruit in ("apple", "banana", "cherry"):
            self.assertIn(f'<option value="{fruit}"></option>', html)
        self.assertNotIn("<script", html)

    def test_list_follows_the_input_id(self):
        widget = AutocompleteTextInput(suggestions=["x"])
        html = widget.render("fruit", "", attrs={"id": "id_fruit"})
        self.assertIn('list="id_fruit-suggestions"', html)
        self.assertIn('<datalist id="id_fruit-suggestions">', html)

    def test_render_empty_suggestions(self):
        widget = AutocompleteTextInput(suggestions=[])
        html = widget.render("field_name", "")

        self.assertIn("<input", html)
        self.assertIn('<datalist id="field_name-suggestions"></datalist>', html)

    def test_render_no_suggestions(self):
        widget = AutocompleteTextInput()
        html = widget.render("field_name", "")

        self.assertIn("<input", html)
        self.assertIn('<datalist id="field_name-suggestions"></datalist>', html)

    def test_render_with_value(self):
        widget = AutocompleteTextInput(suggestions=["test"])
        html = widget.render("field_name", "initial_value")

        self.assertIn('value="initial_value"', html)

    def test_suggestions_are_html_escaped(self):
        suggestions = ['He said "hello"', "It's fine", "<script>alert(1)</script>"]
        widget = AutocompleteTextInput(suggestions=suggestions)
        html = widget.render("test_field", "")

        self.assertIn('value="He said &quot;hello&quot;"', html)
        self.assertIn('value="It&#x27;s fine"', html)
        self.assertNotIn("<script", html)

    def test_field_name_with_special_chars_escaped(self):
        widget = AutocompleteTextInput(suggestions=["test"])
        html = widget.render('field"name', "")
        self.assertNotIn('list="field"name', html)
        self.assertIn("field&quot;name-suggestions", html)

    def test_get_context_includes_suggestions(self):
        widget = AutocompleteTextInput(suggestions=["a", "b", "c"])
        context = widget.get_context("test", "", {})

        self.assertEqual(context["widget"]["suggestions"], ["a", "b", "c"])
        self.assertEqual(context["widget"]["attrs"]["list"], "test-suggestions")
