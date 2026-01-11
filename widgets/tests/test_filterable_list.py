"""
Tests for the FilterableListWidget.

These tests verify the Python rendering functions.
The JavaScript behavior would be tested via browser/integration tests.
"""

from django.template import Context, Template
from django.test import TestCase

from widgets import get_filterable_list_js, render_filterable_list_script


class TestFilterableListScript(TestCase):
    """Tests for the filterable list script rendering."""

    def test_get_filterable_list_js_returns_string(self):
        """Test that get_filterable_list_js returns JavaScript code."""
        js = get_filterable_list_js()
        self.assertIsInstance(js, str)
        self.assertIn("FilterableListManager", js)
        self.assertIn("window.FilterableList", js)

    def test_render_filterable_list_script(self):
        """Test that render_filterable_list_script returns script tag."""
        html = render_filterable_list_script()
        self.assertIn("<script", html)
        self.assertIn("data-filterable-list-js", html)
        self.assertIn("FilterableListManager", html)

    def test_script_contains_key_features(self):
        """Test that the JavaScript includes key functionality."""
        js = get_filterable_list_js()

        # Core manager class
        self.assertIn("class FilterableListManager", js)

        # Data attribute selectors
        self.assertIn("data-filterable-list", js)
        self.assertIn("data-filterable-item", js)
        self.assertIn("data-filter-input", js)
        self.assertIn("data-filter-select", js)
        self.assertIn("data-filter-checkbox", js)
        self.assertIn("data-filter-max", js)
        self.assertIn("data-filter-clear", js)
        self.assertIn("data-filter-count", js)
        self.assertIn("data-filter-no-results", js)

        # Filter modes
        self.assertIn("data-filter-mode", js)

        # Public API methods
        self.assertIn("refresh", js)
        self.assertIn("clearFilters", js)
        self.assertIn("updateFilters", js)
        self.assertIn("getMaxFilters", js)

    def test_script_handles_htmx_turbo(self):
        """Test that the script re-initializes for htmx/Turbo."""
        js = get_filterable_list_js()
        self.assertIn("htmx:afterSwap", js)
        self.assertIn("turbo:render", js)
        self.assertIn("turbo:frame-load", js)

    def test_script_prevents_double_init(self):
        """Test that the script prevents double initialization."""
        js = get_filterable_list_js()
        self.assertIn("if (window.FilterableList) return", js)


class TestFilterableListTemplateTag(TestCase):
    """Tests for the filterable_list template tag."""

    def test_template_tag_renders(self):
        """Test that the template tag renders correctly."""
        template = Template("{% load filterable_list %}{% filterable_list_script %}")
        html = template.render(Context({}))
        self.assertIn("<script", html)
        self.assertIn("FilterableListManager", html)

    def test_template_tag_used_multiple_times(self):
        """Test that multiple uses of the tag work correctly."""
        template = Template(
            "{% load filterable_list %}"
            "{% filterable_list_script %}"
            "{% filterable_list_script %}"
        )
        html = template.render(Context({}))
        # Should have two script tags, each containing "FilterableListManager" twice
        # (once in class declaration, once in window assignment)
        self.assertEqual(html.count("<script"), 2)
        self.assertEqual(html.count("FilterableListManager"), 4)


class TestFilterableListDocumentation(TestCase):
    """Tests to verify documentation and docstrings."""

    def test_module_docstring_exists(self):
        """Test that the module has documentation."""
        from widgets.widgets import filterable

        self.assertIsNotNone(filterable.__doc__)
        self.assertIn("data-filterable-list", filterable.__doc__)

    def test_example_in_docstring(self):
        """Test that the docstring includes usage examples."""
        from widgets.widgets import filterable

        doc = filterable.__doc__
        self.assertIn("data-filter-input", doc)
        self.assertIn("data-filter-select", doc)
        self.assertIn("data-filter-checkbox", doc)
        self.assertIn("data-filter-max", doc)


class TestFilterableListImports(TestCase):
    """Tests for package imports."""

    def test_imports_from_widgets_package(self):
        """Test that functions can be imported from widgets package."""
        from widgets import get_filterable_list_js, render_filterable_list_script

        self.assertIsNotNone(get_filterable_list_js)
        self.assertIsNotNone(render_filterable_list_script)

    def test_imports_from_widgets_filterable_module(self):
        """Test direct import from filterable module."""
        from widgets.widgets.filterable import (
            get_filterable_list_js,
            render_filterable_list_script,
        )

        self.assertIsNotNone(get_filterable_list_js)
        self.assertIsNotNone(render_filterable_list_script)
