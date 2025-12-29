"""Tests for field template tags."""

from core.templatetags.field import add_attr, add_class, field
from django import forms
from django.test import TestCase


class MockForm(forms.Form):
    """Mock form for testing field template tags."""

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea)


class FieldFilterTest(TestCase):
    """Tests for field filter."""

    def test_returns_field_by_name(self):
        """Test filter returns correct field by name."""
        form = MockForm()
        result = field(form, "name")
        self.assertEqual(result.name, "name")

    def test_returns_different_fields(self):
        """Test filter returns different fields correctly."""
        form = MockForm()

        name_field = field(form, "name")
        email_field = field(form, "email")

        self.assertEqual(name_field.name, "name")
        self.assertEqual(email_field.name, "email")
        self.assertNotEqual(name_field, email_field)

    def test_returns_empty_string_for_nonexistent_field(self):
        """Test filter returns empty string for nonexistent field name."""
        form = MockForm()
        result = field(form, "nonexistent")
        self.assertEqual(result, "")

    def test_returns_empty_string_for_invalid_form(self):
        """Test filter returns empty string for invalid form object."""
        result = field(None, "name")
        self.assertEqual(result, "")

        result = field("not a form", "name")
        self.assertEqual(result, "")


class AddClassFilterTest(TestCase):
    """Tests for add_class filter."""

    def test_adds_css_class_to_field(self):
        """Test filter adds CSS class to form field."""
        form = MockForm()
        form_field = form["name"]

        result = add_class(form_field, "my-class")

        self.assertIn('class="my-class"', str(result))

    def test_adds_multiple_classes(self):
        """Test filter can add multiple CSS classes."""
        form = MockForm()
        form_field = form["name"]

        result = add_class(form_field, "class1 class2")

        self.assertIn('class="class1 class2"', str(result))

    def test_returns_field_unchanged_if_no_as_widget(self):
        """Test filter returns field unchanged if no as_widget method."""
        result = add_class("not a field", "my-class")
        self.assertEqual(result, "not a field")

    def test_works_with_textarea(self):
        """Test filter works with textarea widget."""
        form = MockForm()
        form_field = form["description"]

        result = add_class(form_field, "textarea-class")

        self.assertIn('class="textarea-class"', str(result))
        self.assertIn("<textarea", str(result))


class AddAttrFilterTest(TestCase):
    """Tests for add_attr filter."""

    def test_adds_attribute_to_field(self):
        """Test filter adds attribute to form field."""
        form = MockForm()
        form_field = form["name"]

        result = add_attr(form_field, "placeholder:Enter name")

        self.assertIn('placeholder="Enter name"', str(result))

    def test_adds_rows_attribute_to_textarea(self):
        """Test filter adds rows attribute to textarea."""
        form = MockForm()
        form_field = form["description"]

        result = add_attr(form_field, "rows:5")

        self.assertIn('rows="5"', str(result))

    def test_returns_field_unchanged_if_no_as_widget(self):
        """Test filter returns field unchanged if no as_widget method."""
        result = add_attr("not a field", "attr:value")
        self.assertEqual(result, "not a field")

    def test_returns_field_unchanged_for_invalid_attr_string(self):
        """Test filter returns field unchanged for invalid attribute string."""
        form = MockForm()
        form_field = form["name"]

        # Missing colon separator
        result = add_attr(form_field, "invalid")

        # Should return the field unchanged (as widget without added attr)
        self.assertIsNotNone(result)

    def test_handles_colon_in_value(self):
        """Test filter handles colons in attribute value."""
        form = MockForm()
        form_field = form["name"]

        result = add_attr(form_field, "data-url:http://example.com")

        self.assertIn('data-url="http://example.com"', str(result))

    def test_can_chain_with_add_class(self):
        """Test filter can be chained with add_class."""
        form = MockForm()
        form_field = form["name"]

        # First add class, then add attribute
        result = add_class(form_field, "form-control")
        # Note: add_attr returns a new widget, so we test separately
        form_field2 = form["name"]
        result2 = add_attr(form_field2, "placeholder:Enter text")

        self.assertIn('class="form-control"', str(result))
        self.assertIn('placeholder="Enter text"', str(result2))

    def test_preserves_existing_widget_attrs(self):
        """Test filter preserves existing widget attributes."""

        class FormWithAttrs(forms.Form):
            name = forms.CharField(widget=forms.TextInput(attrs={"data-existing": "value"}))

        form = FormWithAttrs()
        form_field = form["name"]

        result = add_attr(form_field, "placeholder:New attr")

        result_str = str(result)
        self.assertIn('data-existing="value"', result_str)
        self.assertIn('placeholder="New attr"', result_str)
