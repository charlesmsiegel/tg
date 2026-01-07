"""
Tests for the widgets app chained select functionality.
"""

from django import forms
from django.test import RequestFactory, TestCase
from widgets import (
    ChainedChoiceField,
    ChainedModelChoiceField,
    ChainedSelect,
    ChainedSelectMixin,
    ChainedSelectMultiple,
)


class TestChainedChoiceField(TestCase):
    """Tests for ChainedChoiceField."""

    def test_field_with_choices(self):
        """Test basic field with direct choices."""
        field = ChainedChoiceField(
            choices=[("a", "Option A"), ("b", "Option B")],
        )
        # Empty choice is prepended
        self.assertEqual(len(field.choices), 3)
        self.assertEqual(field.choices[0][0], "")

    def test_field_with_parent(self):
        """Test child field with parent_field."""
        field = ChainedChoiceField(
            parent_field="parent",
            choices_map={
                "a": [("a1", "A1"), ("a2", "A2")],
                "b": [("b1", "B1")],
            },
        )
        self.assertEqual(field.parent_field, "parent")
        self.assertEqual(len(field.choices_map["a"]), 2)

    def test_get_choices_for_parent(self):
        """Test getting choices based on parent value."""
        field = ChainedChoiceField(
            parent_field="parent",
            choices_map={
                "a": [("a1", "A1"), ("a2", "A2")],
                "b": [("b1", "B1")],
            },
        )
        choices = field.get_choices_for_parent("a")
        # Should include empty choice plus mapped choices
        self.assertEqual(len(choices), 3)
        self.assertEqual(choices[1][0], "a1")

    def test_get_choices_for_parent_empty(self):
        """Test getting choices with no parent value."""
        field = ChainedChoiceField(
            parent_field="parent",
            choices_map={"a": [("a1", "A1")]},
        )
        choices = field.get_choices_for_parent("")
        # Only empty choice
        self.assertEqual(len(choices), 1)

    def test_valid_value_root_field(self):
        """Test validation for root field."""
        field = ChainedChoiceField(
            choices=[("a", "Option A"), ("b", "Option B")],
        )
        self.assertTrue(field.valid_value("a"))
        self.assertTrue(field.valid_value(""))
        self.assertFalse(field.valid_value("invalid"))

    def test_valid_value_child_field(self):
        """Test validation for child field defers to form level."""
        field = ChainedChoiceField(
            parent_field="parent",
            choices_map={"a": [("a1", "A1")]},
        )
        # Child fields always return True for non-empty values
        self.assertTrue(field.valid_value("any_value"))

    def test_choices_callback(self):
        """Test field with choices_callback."""

        def get_choices(parent_value):
            if parent_value == "x":
                return [("x1", "X1")]
            return []

        field = ChainedChoiceField(
            parent_field="parent",
            choices_callback=get_choices,
        )
        choices = field.get_choices_for_parent("x")
        self.assertEqual(len(choices), 2)  # empty + x1


class TestChainedSelect(TestCase):
    """Tests for ChainedSelect widget."""

    def test_widget_attributes(self):
        """Test widget adds correct data attributes."""
        widget = ChainedSelect(
            chain_name="test_chain",
            chain_position=1,
            parent_field="parent",
        )
        attrs = widget.build_attrs({})
        self.assertEqual(attrs["data-chained-select"], "true")
        self.assertEqual(attrs["data-chain-name"], "test_chain")
        self.assertEqual(attrs["data-chain-position"], "1")
        self.assertEqual(attrs["data-parent-field"], "parent")

    def test_widget_css_class(self):
        """Test widget adds CSS class."""
        widget = ChainedSelect()
        attrs = widget.build_attrs({})
        self.assertIn("chained-select", attrs["class"])

    def test_widget_render_includes_script(self):
        """Test widget renders JavaScript."""
        ChainedSelect.reset_js_rendered()
        widget = ChainedSelect(
            chain_name="test",
            chain_position=0,
            choices=[("a", "A")],
        )
        html = widget.render("test_field", "a")
        self.assertIn("data-chained-select-js", html)
        self.assertIn("ChainedSelectManager", html)

    def test_widget_render_choices_tree(self):
        """Test widget embeds choices tree for root position."""
        ChainedSelect.reset_js_rendered()
        widget = ChainedSelect(
            chain_name="test",
            chain_position=0,
            choices_tree={"key": [{"value": "1", "label": "One"}]},
            choices=[("a", "A")],
        )
        html = widget.render("test_field", "a")
        self.assertIn("data-chain-tree", html)

    def test_widget_js_rendered_once(self):
        """Test JavaScript is only rendered once."""
        ChainedSelect.reset_js_rendered()
        widget1 = ChainedSelect(chain_name="test1", chain_position=0, choices=[])
        widget2 = ChainedSelect(chain_name="test2", chain_position=0, choices=[])

        html1 = widget1.render("field1", "")
        html2 = widget2.render("field2", "")

        # JS should be in first render only
        self.assertIn("data-chained-select-js", html1)
        self.assertNotIn("data-chained-select-js", html2)


class TestChainedSelectMultiple(TestCase):
    """Tests for ChainedSelectMultiple widget."""

    def test_multiple_select_inherits_chained_select(self):
        """Test ChainedSelectMultiple inherits from ChainedSelect."""
        widget = ChainedSelectMultiple()
        self.assertIsInstance(widget, ChainedSelect)


class TestChainedSelectMixin(TestCase):
    """Tests for ChainedSelectMixin form mixin."""

    def test_simple_chain_setup(self):
        """Test mixin sets up simple parent-child chain."""

        class TestForm(ChainedSelectMixin, forms.Form):
            parent = ChainedChoiceField(
                choices=[("a", "A"), ("b", "B")],
            )
            child = ChainedChoiceField(
                parent_field="parent",
                choices_map={
                    "a": [("a1", "A1")],
                    "b": [("b1", "B1")],
                },
            )

        form = TestForm()
        # Check chain is configured
        self.assertIsNotNone(form.fields["parent"]._chain_name)
        self.assertEqual(form.fields["parent"]._chain_position, 0)
        self.assertEqual(form.fields["child"]._chain_position, 1)

    def test_three_level_chain(self):
        """Test mixin handles three-level chain."""

        class TestForm(ChainedSelectMixin, forms.Form):
            level1 = ChainedChoiceField(choices=[("x", "X")])
            level2 = ChainedChoiceField(
                parent_field="level1",
                choices_map={"x": [("x1", "X1")]},
            )
            level3 = ChainedChoiceField(
                parent_field="level2",
                choices_map={"x1": [("x1a", "X1A")]},
            )

        form = TestForm()
        self.assertEqual(form.fields["level1"]._chain_position, 0)
        self.assertEqual(form.fields["level2"]._chain_position, 1)
        self.assertEqual(form.fields["level3"]._chain_position, 2)

    def test_bound_form_populates_choices(self):
        """Test bound form populates child choices from parent value."""

        class TestForm(ChainedSelectMixin, forms.Form):
            parent = ChainedChoiceField(
                choices=[("a", "A"), ("b", "B")],
            )
            child = ChainedChoiceField(
                parent_field="parent",
                choices_map={
                    "a": [("a1", "A1"), ("a2", "A2")],
                    "b": [("b1", "B1")],
                },
            )

        form = TestForm(data={"parent": "a", "child": "a1"})
        # Child should have parent "a" choices
        child_values = [c[0] for c in form.fields["child"].choices]
        self.assertIn("a1", child_values)
        self.assertIn("a2", child_values)

    def test_form_validation_valid_selection(self):
        """Test form validates consistent selections."""

        class TestForm(ChainedSelectMixin, forms.Form):
            parent = ChainedChoiceField(
                choices=[("a", "A"), ("b", "B")],
            )
            child = ChainedChoiceField(
                parent_field="parent",
                choices_map={
                    "a": [("a1", "A1")],
                    "b": [("b1", "B1")],
                },
            )

        form = TestForm(data={"parent": "a", "child": "a1"})
        self.assertTrue(form.is_valid())

    def test_form_validation_invalid_selection(self):
        """Test form rejects inconsistent selections."""

        class TestForm(ChainedSelectMixin, forms.Form):
            parent = ChainedChoiceField(
                choices=[("a", "A"), ("b", "B")],
            )
            child = ChainedChoiceField(
                parent_field="parent",
                choices_map={
                    "a": [("a1", "A1")],
                    "b": [("b1", "B1")],
                },
            )

        form = TestForm(data={"parent": "a", "child": "b1"})
        self.assertFalse(form.is_valid())
        self.assertIn("child", form.errors)

    def test_initial_data_populates_choices(self):
        """Test form with initial data populates child choices."""

        class TestForm(ChainedSelectMixin, forms.Form):
            parent = ChainedChoiceField(
                choices=[("a", "A"), ("b", "B")],
            )
            child = ChainedChoiceField(
                parent_field="parent",
                choices_map={
                    "a": [("a1", "A1")],
                    "b": [("b1", "B1")],
                },
            )

        form = TestForm(initial={"parent": "b"})
        child_values = [c[0] for c in form.fields["child"].choices]
        self.assertIn("b1", child_values)

    def test_multiple_independent_chains(self):
        """Test form with multiple independent chains."""

        class TestForm(ChainedSelectMixin, forms.Form):
            # First chain
            color = ChainedChoiceField(choices=[("red", "Red")])
            shade = ChainedChoiceField(
                parent_field="color",
                choices_map={"red": [("dark", "Dark")]},
            )
            # Second chain
            size = ChainedChoiceField(choices=[("small", "Small")])
            detail = ChainedChoiceField(
                parent_field="size",
                choices_map={"small": [("tiny", "Tiny")]},
            )

        form = TestForm()
        # Should have two separate chains
        self.assertNotEqual(
            form.fields["color"]._chain_name,
            form.fields["size"]._chain_name,
        )


class TestWidgetsImports(TestCase):
    """Tests that the widgets package exports correctly."""

    def test_all_exports_available(self):
        """Test all expected exports are available from widgets package."""
        from widgets import (
            ChainedChoiceField,
            ChainedModelChoiceField,
            ChainedSelect,
            ChainedSelectAjaxView,
            ChainedSelectMixin,
            ChainedSelectMultiple,
            auto_chained_ajax_view,
            make_ajax_view,
        )

        # Just verify imports work
        self.assertIsNotNone(ChainedChoiceField)
        self.assertIsNotNone(ChainedModelChoiceField)
        self.assertIsNotNone(ChainedSelect)
        self.assertIsNotNone(ChainedSelectMultiple)
        self.assertIsNotNone(ChainedSelectMixin)
        self.assertIsNotNone(ChainedSelectAjaxView)
        self.assertIsNotNone(auto_chained_ajax_view)
        self.assertIsNotNone(make_ajax_view)


class TestBackwardCompatibility(TestCase):
    """Tests for backward compatibility with chained_select package."""

    def test_chained_select_import_works(self):
        """Test importing from chained_select still works (with deprecation warning)."""
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # This should work but emit a deprecation warning
            from chained_select import ChainedChoiceField as OldField

            self.assertIsNotNone(OldField)
            # Should have warning
            self.assertTrue(any("deprecated" in str(warning.message).lower() for warning in w))

    def test_both_imports_return_same_class(self):
        """Test old and new imports return the same class."""
        import warnings

        from widgets import ChainedChoiceField as NewField

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from chained_select import ChainedChoiceField as OldField

        self.assertIs(NewField, OldField)
