"""
Tests for the widgets app conditional fields functionality.
"""

from django import forms
from django.test import TestCase
from widgets import ConditionalFieldsMixin
from widgets.mixins.conditional import CONDITIONAL_FIELDS_JS, ConditionalFieldsMixin


class TestConditionalFieldsMixin(TestCase):
    """Tests for ConditionalFieldsMixin form mixin."""

    def test_mixin_provides_script_property(self):
        """Test mixin provides conditional_fields_script property."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A"), ("b", "B")])
            example = forms.CharField()

            conditional_fields = {
                "category": {
                    "example": {"values": ["a"]},
                }
            }

        form = TestForm()
        self.assertTrue(hasattr(form, "conditional_fields_script"))

    def test_script_includes_javascript(self):
        """Test script output includes JavaScript library."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A")])
            example = forms.CharField()

            conditional_fields = {
                "category": {
                    "example": {"values": ["a"]},
                }
            }

        form = TestForm()
        script = form.conditional_fields_script
        self.assertIn("ConditionalFieldsManager", script)
        self.assertIn("data-conditional-fields-js", script)

    def test_script_includes_rules_json(self):
        """Test script output includes rules as JSON."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A")])
            example = forms.CharField()

            conditional_fields = {
                "category": {
                    "example": {"values": ["a", "b"]},
                }
            }

        form = TestForm()
        script = form.conditional_fields_script
        self.assertIn("data-conditional-rules", script)
        self.assertIn('"category"', script)
        self.assertIn('"example"', script)
        self.assertIn('"values"', script)

    def test_script_js_rendered_once(self):
        """Test JavaScript library is only rendered once."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A")])
            example = forms.CharField()

            conditional_fields = {
                "category": {
                    "example": {"values": ["a"]},
                }
            }

        form1 = TestForm()
        form2 = TestForm()

        script1 = form1.conditional_fields_script
        script2 = form2.conditional_fields_script

        # JS library should be in first render only
        self.assertIn("data-conditional-fields-js", script1)
        self.assertNotIn("data-conditional-fields-js", script2)

        # But both should have rules
        self.assertIn("data-conditional-rules", script1)
        self.assertIn("data-conditional-rules", script2)

    def test_empty_rules_returns_empty_string(self):
        """Test empty conditional_fields returns empty script."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A")])
            example = forms.CharField()

            conditional_fields = {}

        form = TestForm()
        self.assertEqual(form.conditional_fields_script, "")

    def test_get_conditional_fields_override(self):
        """Test get_conditional_fields can be overridden for dynamic rules."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A")])
            example = forms.CharField()
            note = forms.CharField()

            def __init__(self, *args, show_note=False, **kwargs):
                self.show_note = show_note
                super().__init__(*args, **kwargs)

            def get_conditional_fields(self):
                rules = {
                    "category": {
                        "example": {"values": ["a"]},
                    }
                }
                if self.show_note:
                    rules["category"]["note"] = {"values": ["a"]}
                return rules

        ConditionalFieldsMixin._conditional_js_rendered = False
        form_without_note = TestForm(show_note=False)
        script1 = form_without_note.conditional_fields_script
        self.assertIn('"example"', script1)
        self.assertNotIn('"note"', script1)

        ConditionalFieldsMixin._conditional_js_rendered = False
        form_with_note = TestForm(show_note=True)
        script2 = form_with_note.conditional_fields_script
        self.assertIn('"example"', script2)
        self.assertIn('"note"', script2)

    def test_formset_prefix_included(self):
        """Test form prefix is included in data attributes."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A")])
            example = forms.CharField()

            conditional_fields = {
                "category": {
                    "example": {"values": ["a"]},
                }
            }

        form = TestForm(prefix="items-0")
        script = form.conditional_fields_script
        self.assertIn('data-form-prefix="items-0"', script)

    def test_render_conditional_wrapper(self):
        """Test render_conditional_wrapper helper method."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            example = forms.CharField()

        form = TestForm()
        wrapper = form.render_conditional_wrapper("example", "<input>", "extra-class")

        self.assertIn('id="example_wrap"', wrapper)
        self.assertIn('class="d-none extra-class"', wrapper)
        self.assertIn('data-conditional-field="example"', wrapper)
        self.assertIn("<input>", wrapper)


class TestConditionalFieldsRuleTypes(TestCase):
    """Tests for different rule types in conditional fields."""

    def test_values_rule(self):
        """Test 'values' rule for exact match."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A"), ("b", "B")])
            example = forms.CharField()

            conditional_fields = {
                "category": {
                    "example": {"values": ["a"]},
                }
            }

        form = TestForm()
        script = form.conditional_fields_script
        self.assertIn('"values":["a"]', script.replace(" ", "").replace("'", '"'))

    def test_exclude_rule(self):
        """Test 'exclude' rule for negative match."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A"), ("b", "B")])
            example = forms.CharField()

            conditional_fields = {
                "category": {
                    "example": {"exclude": ["-----", "none"]},
                }
            }

        form = TestForm()
        script = form.conditional_fields_script
        self.assertIn("exclude", script)
        self.assertIn("-----", script)

    def test_checked_rule(self):
        """Test 'checked' rule for checkbox fields."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            create_new = forms.BooleanField(required=False)
            new_name = forms.CharField()

            conditional_fields = {
                "create_new": {
                    "new_name": {"checked": True},
                }
            }

        form = TestForm()
        script = form.conditional_fields_script
        self.assertIn('"checked":true', script.replace(" ", "").replace("'", '"'))

    def test_multiple_targets(self):
        """Test multiple target fields for one controller."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A"), ("b", "B")])
            example = forms.CharField()
            note = forms.CharField()
            value = forms.IntegerField()

            conditional_fields = {
                "category": {
                    "example": {"exclude": ["-----"]},
                    "note": {"values": ["b"]},
                    "value": {"values": ["a"]},
                }
            }

        form = TestForm()
        script = form.conditional_fields_script
        self.assertIn('"example"', script)
        self.assertIn('"note"', script)
        self.assertIn('"value"', script)

    def test_multiple_controllers(self):
        """Test form with multiple controller fields."""
        ConditionalFieldsMixin._conditional_js_rendered = False

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[("a", "A")])
            type = forms.ChoiceField(choices=[("x", "X")])
            for_category = forms.CharField()
            for_type = forms.CharField()

            conditional_fields = {
                "category": {
                    "for_category": {"values": ["a"]},
                },
                "type": {
                    "for_type": {"values": ["x"]},
                },
            }

        form = TestForm()
        script = form.conditional_fields_script
        self.assertIn('"category"', script)
        self.assertIn('"type"', script)
        self.assertIn('"for_category"', script)
        self.assertIn('"for_type"', script)


class TestConditionalFieldsJavaScript(TestCase):
    """Tests for the embedded JavaScript."""

    def test_js_contains_manager_class(self):
        """Test JavaScript contains the manager class."""
        self.assertIn("class ConditionalFieldsManager", CONDITIONAL_FIELDS_JS)

    def test_js_contains_init_function(self):
        """Test JavaScript contains init function."""
        self.assertIn("init()", CONDITIONAL_FIELDS_JS)

    def test_js_handles_htmx(self):
        """Test JavaScript handles htmx:afterSwap event."""
        self.assertIn("htmx:afterSwap", CONDITIONAL_FIELDS_JS)

    def test_js_handles_turbo(self):
        """Test JavaScript handles Turbo events."""
        self.assertIn("turbo:render", CONDITIONAL_FIELDS_JS)
        self.assertIn("turbo:frame-load", CONDITIONAL_FIELDS_JS)

    def test_js_uses_d_none_class(self):
        """Test JavaScript uses Bootstrap d-none class."""
        self.assertIn("d-none", CONDITIONAL_FIELDS_JS)

    def test_js_handles_checkbox(self):
        """Test JavaScript handles checkbox type."""
        self.assertIn("checkbox", CONDITIONAL_FIELDS_JS)

    def test_js_evaluates_values_rule(self):
        """Test JavaScript evaluates 'values' rule."""
        self.assertIn("rule.values", CONDITIONAL_FIELDS_JS)

    def test_js_evaluates_exclude_rule(self):
        """Test JavaScript evaluates 'exclude' rule."""
        self.assertIn("rule.exclude", CONDITIONAL_FIELDS_JS)

    def test_js_evaluates_checked_rule(self):
        """Test JavaScript evaluates 'checked' rule."""
        self.assertIn("rule.checked", CONDITIONAL_FIELDS_JS)


class TestWidgetsConditionalImports(TestCase):
    """Tests that conditional fields are exported correctly."""

    def test_conditional_fields_mixin_importable(self):
        """Test ConditionalFieldsMixin is importable from widgets package."""
        from widgets import ConditionalFieldsMixin

        self.assertIsNotNone(ConditionalFieldsMixin)

    def test_conditional_fields_mixin_in_all(self):
        """Test ConditionalFieldsMixin is in __all__."""
        import widgets

        self.assertIn("ConditionalFieldsMixin", widgets.__all__)
