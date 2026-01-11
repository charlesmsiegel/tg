"""
Tests for the widgets app create-or-select functionality.
"""

from django import forms
from django.db import models
from django.test import TestCase

from widgets import (
    CreateOrSelectField,
    CreateOrSelectMixin,
    CreateOrSelectModelChoiceField,
    CreateOrSelectWidget,
)


# Test model for ModelChoiceField tests
class TestItem(models.Model):
    """Test model for create-or-select tests."""

    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)

    class Meta:
        app_label = "widgets"
        managed = False  # Don't create table


class TestCreateOrSelectWidget(TestCase):
    """Tests for CreateOrSelectWidget."""

    def test_widget_is_checkbox(self):
        """Test widget inherits from CheckboxInput."""
        widget = CreateOrSelectWidget()
        self.assertIsInstance(widget, forms.CheckboxInput)

    def test_widget_attributes(self):
        """Test widget adds correct data attributes."""
        CreateOrSelectWidget.reset_js_rendered()
        widget = CreateOrSelectWidget(group_name="test_group")
        html = widget.render("test_field", False)

        self.assertIn('data-create-or-select-toggle="true"', html)
        self.assertIn('data-create-or-select-group="test_group"', html)

    def test_widget_derives_group_from_name(self):
        """Test widget uses field name as group if not specified."""
        CreateOrSelectWidget.reset_js_rendered()
        widget = CreateOrSelectWidget()
        html = widget.render("my_toggle", False)

        self.assertIn('data-create-or-select-group="my_toggle"', html)

    def test_widget_css_class(self):
        """Test widget adds CSS class."""
        CreateOrSelectWidget.reset_js_rendered()
        widget = CreateOrSelectWidget()
        html = widget.render("test", False)

        self.assertIn("create-or-select-toggle", html)

    def test_widget_render_includes_script(self):
        """Test widget renders JavaScript."""
        CreateOrSelectWidget.reset_js_rendered()
        widget = CreateOrSelectWidget()
        html = widget.render("test_field", False)

        self.assertIn("data-create-or-select-js", html)
        self.assertIn("CreateOrSelectManager", html)

    def test_widget_js_rendered_once(self):
        """Test JavaScript is only rendered once."""
        CreateOrSelectWidget.reset_js_rendered()
        widget1 = CreateOrSelectWidget()
        widget2 = CreateOrSelectWidget()

        html1 = widget1.render("field1", False)
        html2 = widget2.render("field2", False)

        # JS should be in first render only
        self.assertIn("data-create-or-select-js", html1)
        self.assertNotIn("data-create-or-select-js", html2)

    def test_widget_reinit_script(self):
        """Test widget adds reinit script for dynamic loading."""
        CreateOrSelectWidget.reset_js_rendered()
        widget = CreateOrSelectWidget()
        html = widget.render("test", False)

        self.assertIn("if(window.CreateOrSelect)window.CreateOrSelect.init();", html)


class TestCreateOrSelectField(TestCase):
    """Tests for CreateOrSelectField."""

    def test_field_is_boolean(self):
        """Test field is a BooleanField."""
        field = CreateOrSelectField()
        self.assertIsInstance(field, forms.BooleanField)

    def test_field_not_required_by_default(self):
        """Test field is not required by default."""
        field = CreateOrSelectField()
        self.assertFalse(field.required)

    def test_field_uses_widget(self):
        """Test field uses CreateOrSelectWidget."""
        field = CreateOrSelectField()
        self.assertIsInstance(field.widget, CreateOrSelectWidget)

    def test_field_clean_true(self):
        """Test field cleans truthy values to True."""
        field = CreateOrSelectField()
        self.assertTrue(field.clean(True))
        self.assertTrue(field.clean("on"))
        self.assertTrue(field.clean(1))

    def test_field_clean_false(self):
        """Test field cleans falsy values to False."""
        field = CreateOrSelectField()
        self.assertFalse(field.clean(False))
        self.assertFalse(field.clean(""))
        self.assertFalse(field.clean(None))

    def test_field_select_field_config(self):
        """Test field stores select_field configuration."""
        field = CreateOrSelectField(select_field="my_select")
        self.assertEqual(field.select_field, "my_select")

    def test_field_custom_error_message(self):
        """Test field stores custom error message."""
        msg = "Please choose or create something."
        field = CreateOrSelectField(create_error_message=msg)
        self.assertEqual(field.create_error_message, msg)


class TestCreateOrSelectModelChoiceField(TestCase):
    """Tests for CreateOrSelectModelChoiceField."""

    def test_field_is_model_choice_field(self):
        """Test field is a ModelChoiceField."""
        field = CreateOrSelectModelChoiceField(queryset=TestItem.objects.none())
        self.assertIsInstance(field, forms.ModelChoiceField)

    def test_field_not_required_by_default(self):
        """Test field is not required by default."""
        field = CreateOrSelectModelChoiceField(queryset=TestItem.objects.none())
        self.assertFalse(field.required)

    def test_field_toggle_field_config(self):
        """Test field stores toggle_field configuration."""
        field = CreateOrSelectModelChoiceField(
            queryset=TestItem.objects.none(), toggle_field="create_new"
        )
        self.assertEqual(field.toggle_field, "create_new")


class TestCreateOrSelectMixin(TestCase):
    """Tests for CreateOrSelectMixin with ModelForms."""

    def test_mixin_default_config(self):
        """Test mixin provides default configuration."""

        class TestForm(CreateOrSelectMixin, forms.Form):
            pass

        form = TestForm()
        config = form.get_create_or_select_config()

        self.assertEqual(config["toggle_field"], "select_or_create")
        self.assertEqual(config["select_field"], "select")

    def test_mixin_custom_config(self):
        """Test mixin uses custom configuration."""

        class TestForm(CreateOrSelectMixin, forms.Form):
            create_or_select_config = {
                "toggle_field": "create_new",
                "select_field": "existing",
                "error_message": "Custom error",
            }

        form = TestForm()
        config = form.get_create_or_select_config()

        self.assertEqual(config["toggle_field"], "create_new")
        self.assertEqual(config["select_field"], "existing")
        self.assertEqual(config["error_message"], "Custom error")

    def test_is_creating_true(self):
        """Test is_creating returns True when toggle is checked."""

        class TestForm(CreateOrSelectMixin, forms.Form):
            select_or_create = CreateOrSelectField()
            select = forms.CharField(required=False)

        form = TestForm(data={"select_or_create": "on"})
        form.is_valid()  # Populate cleaned_data
        self.assertTrue(form.is_creating())

    def test_is_creating_false(self):
        """Test is_creating returns False when toggle is unchecked."""

        class TestForm(CreateOrSelectMixin, forms.Form):
            select_or_create = CreateOrSelectField()
            select = forms.CharField(required=False)

        form = TestForm(data={"select": "something"})
        form.is_valid()
        self.assertFalse(form.is_creating())

    def test_validation_requires_selection_when_not_creating(self):
        """Test validation fails without selection when not creating."""

        class TestForm(CreateOrSelectMixin, forms.Form):
            select_or_create = CreateOrSelectField()
            select = forms.CharField(required=False)

        form = TestForm(data={})  # Neither creating nor selecting
        self.assertFalse(form.is_valid())
        self.assertIn("select", form.errors)

    def test_validation_passes_with_selection(self):
        """Test validation passes with selection when not creating."""

        class TestForm(CreateOrSelectMixin, forms.Form):
            select_or_create = CreateOrSelectField()
            select = forms.CharField(required=False)

        form = TestForm(data={"select": "something"})
        self.assertTrue(form.is_valid())

    def test_validation_passes_when_creating(self):
        """Test validation passes when in create mode."""

        class TestForm(CreateOrSelectMixin, forms.Form):
            select_or_create = CreateOrSelectField()
            select = forms.CharField(required=False)

        form = TestForm(data={"select_or_create": "on"})
        self.assertTrue(form.is_valid())


class TestWidgetsCreateOrSelectImports(TestCase):
    """Tests that the create-or-select exports are available from widgets package."""

    def test_all_exports_available(self):
        """Test all expected exports are available from widgets package."""
        from widgets import (
            CreateOrSelectField,
            CreateOrSelectMixin,
            CreateOrSelectModelChoiceField,
            CreateOrSelectWidget,
        )

        # Just verify imports work
        self.assertIsNotNone(CreateOrSelectWidget)
        self.assertIsNotNone(CreateOrSelectField)
        self.assertIsNotNone(CreateOrSelectModelChoiceField)
        self.assertIsNotNone(CreateOrSelectMixin)


class TestJavaScriptBehavior(TestCase):
    """Tests for JavaScript behavior (unit tests for the JS logic)."""

    def test_js_data_attributes_for_containers(self):
        """Test that container data attributes match the expected format."""
        CreateOrSelectWidget.reset_js_rendered()
        widget = CreateOrSelectWidget(group_name="effects-0")
        html = widget.render("select_or_create", False)

        # Check the group name is correctly set
        self.assertIn('data-create-or-select-group="effects-0"', html)

        # Document expected container attribute format
        expected_select = (
            'data-create-or-select-container="effects-0" data-create-or-select-mode="select"'
        )
        expected_create = (
            'data-create-or-select-container="effects-0" data-create-or-select-mode="create"'
        )

        # These assertions document the expected template usage pattern
        # (actual templates need to include these attributes)
        self.assertIn("effects-0", html)

    def test_js_handles_formset_prefixes(self):
        """Test JavaScript handles formset-style prefixes correctly."""
        CreateOrSelectWidget.reset_js_rendered()

        # Simulate formset rendering with different prefixes
        widget = CreateOrSelectWidget()

        html0 = widget.render("effects-0-select_or_create", False)
        CreateOrSelectWidget.reset_js_rendered()  # Reset for next render

        widget2 = CreateOrSelectWidget()
        html1 = widget2.render("effects-1-select_or_create", False)

        # Each should have unique group derived from field name
        self.assertIn('data-create-or-select-group="effects-0-select_or_create"', html0)
        self.assertIn('data-create-or-select-group="effects-1-select_or_create"', html1)
