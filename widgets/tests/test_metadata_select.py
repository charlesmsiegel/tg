"""
Tests for the OptionMetadataSelect widget.
"""

from django import forms
from django.test import TestCase

from widgets import OptionMetadataSelect, OptionMetadataSelectMultiple
from widgets.utils import normalize_choices


class TestOptionMetadataSelect(TestCase):
    """Tests for OptionMetadataSelect widget."""

    def test_widget_attributes(self):
        """Test widget adds correct data attributes."""
        widget = OptionMetadataSelect()
        attrs = widget.build_attrs({})
        self.assertEqual(attrs["data-metadata-select"], "true")

    def test_widget_render_includes_script(self):
        """Test widget renders JavaScript."""
        OptionMetadataSelect.reset_js_rendered()
        widget = OptionMetadataSelect(choices=[("a", "A")])
        html = widget.render("test_field", "a")
        self.assertIn("data-option-metadata-js", html)
        self.assertIn("OptionMetadataManager", html)

    def test_widget_js_rendered_once(self):
        """Test JavaScript is only rendered once."""
        OptionMetadataSelect.reset_js_rendered()
        widget1 = OptionMetadataSelect(choices=[])
        widget2 = OptionMetadataSelect(choices=[])

        html1 = widget1.render("field1", "")
        html2 = widget2.render("field2", "")

        # JS should be in first render only
        self.assertIn("data-option-metadata-js", html1)
        self.assertNotIn("data-option-metadata-js", html2)

    def test_option_with_metadata(self):
        """Test options with 3-tuple metadata render data attributes."""
        OptionMetadataSelect.reset_js_rendered()
        choices = [
            ("val1", "Label 1", {"poolable": "true", "cost": "5"}),
            ("val2", "Label 2", {"poolable": "false", "cost": "3"}),
        ]
        widget = OptionMetadataSelect(choices=choices)
        html = widget.render("test_field", "")

        self.assertIn('data-poolable="true"', html)
        self.assertIn('data-poolable="false"', html)
        self.assertIn('data-cost="5"', html)
        self.assertIn('data-cost="3"', html)

    def test_option_without_metadata(self):
        """Test standard 2-tuple choices work normally."""
        OptionMetadataSelect.reset_js_rendered()
        choices = [
            ("val1", "Label 1"),
            ("val2", "Label 2"),
        ]
        widget = OptionMetadataSelect(choices=choices)
        html = widget.render("test_field", "")

        # Should render normally without data attributes
        self.assertIn("Label 1", html)
        self.assertIn("Label 2", html)

    def test_mixed_choices(self):
        """Test mix of 2-tuple and 3-tuple choices."""
        OptionMetadataSelect.reset_js_rendered()
        choices = [
            ("val1", "With Metadata", {"extra": "yes"}),
            ("val2", "Without Metadata"),
        ]
        widget = OptionMetadataSelect(choices=choices)
        html = widget.render("test_field", "")

        self.assertIn('data-extra="yes"', html)
        self.assertIn("Without Metadata", html)


class TestOptionMetadataSelectMultiple(TestCase):
    """Tests for OptionMetadataSelectMultiple widget."""

    def test_multiple_select_inherits_metadata_select(self):
        """Test OptionMetadataSelectMultiple inherits from OptionMetadataSelect."""
        widget = OptionMetadataSelectMultiple()
        self.assertIsInstance(widget, OptionMetadataSelect)


class TestNormalizeChoicesWithMetadata(TestCase):
    """Tests for normalize_choices with metadata support."""

    def test_normalize_2tuple_choices(self):
        """Test normalizing standard 2-tuple choices."""
        choices = [("a", "Label A"), ("b", "Label B")]
        result = normalize_choices(choices)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {"value": "a", "label": "Label A"})
        self.assertEqual(result[1], {"value": "b", "label": "Label B"})

    def test_normalize_3tuple_choices(self):
        """Test normalizing 3-tuple choices with metadata."""
        choices = [
            ("a", "Label A", {"poolable": "true"}),
            ("b", "Label B", {"poolable": "false", "cost": "5"}),
        ]
        result = normalize_choices(choices)

        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0],
            {"value": "a", "label": "Label A", "metadata": {"poolable": "true"}},
        )
        self.assertEqual(
            result[1],
            {
                "value": "b",
                "label": "Label B",
                "metadata": {"poolable": "false", "cost": "5"},
            },
        )

    def test_normalize_mixed_choices(self):
        """Test normalizing mixed 2-tuple and 3-tuple choices."""
        choices = [
            ("a", "Label A"),
            ("b", "Label B", {"extra": "data"}),
        ]
        result = normalize_choices(choices)

        self.assertEqual(result[0], {"value": "a", "label": "Label A"})
        self.assertEqual(
            result[1], {"value": "b", "label": "Label B", "metadata": {"extra": "data"}}
        )

    def test_normalize_empty_metadata(self):
        """Test normalizing 3-tuple with empty metadata dict."""
        choices = [("a", "Label A", {})]
        result = normalize_choices(choices)

        # Empty metadata should not be included
        self.assertEqual(result[0], {"value": "a", "label": "Label A"})

    def test_normalize_none_metadata(self):
        """Test normalizing 3-tuple with None metadata."""
        choices = [("a", "Label A", None)]
        result = normalize_choices(choices)

        # None metadata should not be included
        self.assertEqual(result[0], {"value": "a", "label": "Label A"})


class TestChainedSelectWithMetadata(TestCase):
    """Tests for ChainedSelect with metadata support."""

    def test_chained_select_with_metadata_choices(self):
        """Test ChainedSelectMixin handles 3-tuple choices correctly."""
        from widgets import ChainedChoiceField, ChainedSelectMixin

        class TestForm(ChainedSelectMixin, forms.Form):
            category = ChainedChoiceField(choices=[("bg", "Background"), ("mf", "Merit/Flaw")])
            example = ChainedChoiceField(
                parent_field="category",
                choices_map={
                    "bg": [
                        ("bg1", "Allies", {"poolable": "true"}),
                        ("bg2", "Resources", {"poolable": "false"}),
                    ],
                    "mf": [("mf1", "Acute Sense"), ("mf2", "Ambidextrous")],
                },
            )

        form = TestForm()

        # The choices tree should include metadata
        root_widget = form.fields["category"].widget
        self.assertIsNotNone(root_widget.choices_tree)

        # Check that metadata is preserved in the tree
        bg_key = "example:bg"
        self.assertIn(bg_key, root_widget.choices_tree)

        bg_choices = root_widget.choices_tree[bg_key]
        self.assertEqual(len(bg_choices), 2)

        # First choice should have metadata
        self.assertEqual(bg_choices[0]["value"], "bg1")
        self.assertEqual(bg_choices[0]["metadata"], {"poolable": "true"})

        # Second choice should also have metadata
        self.assertEqual(bg_choices[1]["value"], "bg2")
        self.assertEqual(bg_choices[1]["metadata"], {"poolable": "false"})

    def test_chained_select_mf_choices_without_metadata(self):
        """Test ChainedSelectMixin handles 2-tuple choices correctly."""
        from widgets import ChainedChoiceField, ChainedSelectMixin

        class TestForm(ChainedSelectMixin, forms.Form):
            category = ChainedChoiceField(choices=[("bg", "Background"), ("mf", "Merit/Flaw")])
            example = ChainedChoiceField(
                parent_field="category",
                choices_map={
                    "bg": [("bg1", "Allies"), ("bg2", "Resources")],
                    "mf": [("mf1", "Acute Sense"), ("mf2", "Ambidextrous")],
                },
            )

        form = TestForm()

        # The choices tree should work without metadata
        root_widget = form.fields["category"].widget
        bg_choices = root_widget.choices_tree["example:bg"]

        # Choices should not have metadata key
        self.assertNotIn("metadata", bg_choices[0])


class TestImports(TestCase):
    """Tests that the new exports are available."""

    def test_option_metadata_exports(self):
        """Test OptionMetadataSelect exports are available from widgets package."""
        from widgets import OptionMetadataSelect, OptionMetadataSelectMultiple

        self.assertIsNotNone(OptionMetadataSelect)
        self.assertIsNotNone(OptionMetadataSelectMultiple)
