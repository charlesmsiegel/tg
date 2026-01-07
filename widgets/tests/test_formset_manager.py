"""
Tests for the FormsetManager widget and template tags.
"""

from django import forms
from django.template import Context, Template
from django.test import TestCase
from widgets.templatetags.formset_tags import (
    formset_add_btn,
    formset_container,
    formset_form_wrapper,
    formset_remove_btn,
    formset_script,
)
from widgets.widgets.formset_manager import (
    FORMSET_MANAGER_JS,
    _reset_js_rendered,
    render_formset_manager_script,
    render_formset_manager_script_once,
)


class TestFormsetManagerScript(TestCase):
    """Tests for FormsetManager JavaScript rendering."""

    def setUp(self):
        """Reset JS rendered flag before each test."""
        _reset_js_rendered()

    def test_render_formset_manager_script(self):
        """Test render_formset_manager_script returns script tag."""
        html = render_formset_manager_script()
        self.assertIn("data-formset-manager-js", html)
        self.assertIn("FormsetManagerClass", html)

    def test_render_formset_manager_script_once(self):
        """Test render_formset_manager_script_once only renders once."""
        html1 = render_formset_manager_script_once()
        html2 = render_formset_manager_script_once()

        self.assertIn("data-formset-manager-js", html1)
        self.assertEqual(html2, "")

    def test_reset_js_rendered(self):
        """Test _reset_js_rendered resets the flag."""
        render_formset_manager_script_once()
        _reset_js_rendered()
        html = render_formset_manager_script_once()
        self.assertIn("data-formset-manager-js", html)

    def test_js_contains_formset_manager_class(self):
        """Test JavaScript contains FormsetManagerClass."""
        self.assertIn("class FormsetManagerClass", FORMSET_MANAGER_JS)

    def test_js_contains_init_method(self):
        """Test JavaScript contains init method."""
        self.assertIn("init()", FORMSET_MANAGER_JS)

    def test_js_contains_add_form_method(self):
        """Test JavaScript contains addForm method."""
        self.assertIn("addForm(prefix)", FORMSET_MANAGER_JS)

    def test_js_contains_remove_form_method(self):
        """Test JavaScript contains removeForm method."""
        self.assertIn("removeForm(removeBtn, prefix)", FORMSET_MANAGER_JS)

    def test_js_contains_reinitialize_widgets(self):
        """Test JavaScript reinitializes ChainedSelect."""
        self.assertIn("window.ChainedSelect", FORMSET_MANAGER_JS)

    def test_js_fires_custom_events(self):
        """Test JavaScript fires formset:added and formset:removed events."""
        self.assertIn("formset:added", FORMSET_MANAGER_JS)
        self.assertIn("formset:removed", FORMSET_MANAGER_JS)


class TestFormsetTemplateTags(TestCase):
    """Tests for formset simple template tags (advanced use)."""

    def setUp(self):
        """Reset JS rendered flag before each test."""
        _reset_js_rendered()

    def test_formset_script_tag(self):
        """Test formset_script template tag."""
        result = formset_script()
        self.assertIn("data-formset-manager-js", result)

    def test_formset_container_basic(self):
        """Test formset_container returns correct attributes."""
        result = formset_container("my_prefix")
        self.assertIn('data-formset-container=""', result)
        self.assertIn('data-formset-prefix="my_prefix"', result)

    def test_formset_container_with_empty_form_id(self):
        """Test formset_container with custom empty form ID."""
        result = formset_container("my_prefix", empty_form_id="custom_empty")
        self.assertIn('data-formset-empty-form="custom_empty"', result)

    def test_formset_container_with_animate(self):
        """Test formset_container with animation enabled."""
        result = formset_container("my_prefix", animate=True)
        self.assertIn('data-formset-animate="true"', result)

    def test_formset_add_btn_basic(self):
        """Test formset_add_btn creates button."""
        result = formset_add_btn("my_prefix", "Add Item")
        self.assertIn("<button", result)
        self.assertIn('data-formset-add="my_prefix"', result)
        self.assertIn('type="button"', result)
        self.assertIn("Add Item", result)

    def test_formset_add_btn_with_attrs(self):
        """Test formset_add_btn with custom attributes."""
        result = formset_add_btn("my_prefix", "Add", **{"class": "btn btn-primary"})
        self.assertIn('class="btn btn-primary"', result)

    def test_formset_remove_btn(self):
        """Test formset_remove_btn returns correct attribute."""
        result = formset_remove_btn("my_prefix")
        self.assertIn('data-formset-remove="my_prefix"', result)

    def test_formset_form_wrapper(self):
        """Test formset_form_wrapper returns correct attribute."""
        result = formset_form_wrapper()
        self.assertIn('data-formset-form=""', result)


class TestFormsetBlockTag(TestCase):
    """Tests for the {% formset %} block tag."""

    def setUp(self):
        """Reset JS rendered flag before each test."""
        _reset_js_rendered()

    def _create_formset(self, prefix="items", extra=1):
        """Create a simple formset for testing."""

        class ItemForm(forms.Form):
            name = forms.CharField()
            quantity = forms.IntegerField()

        ItemFormSet = forms.formset_factory(ItemForm, extra=extra)
        return ItemFormSet(prefix=prefix)

    def test_formset_block_tag_renders_management_form(self):
        """Test block tag renders management form."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" %}
            {{ subform.name }}
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertIn("id_items-TOTAL_FORMS", result)
        self.assertIn("id_items-INITIAL_FORMS", result)

    def test_formset_block_tag_renders_container(self):
        """Test block tag renders container with data attributes."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" %}
            {{ subform.name }}
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertIn('data-formset-container=""', result)
        self.assertIn('data-formset-prefix="items"', result)
        self.assertIn('id="items_formset"', result)

    def test_formset_block_tag_renders_empty_form(self):
        """Test block tag renders hidden empty form template."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" %}
            {{ subform.name }}
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertIn('id="empty_items_form"', result)
        self.assertIn('class="d-none"', result)

    def test_formset_block_tag_renders_add_button(self):
        """Test block tag renders add button."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" add_label="Add Item" %}
            {{ subform.name }}
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertIn('data-formset-add="items"', result)
        self.assertIn("Add Item", result)

    def test_formset_block_tag_renders_js_once(self):
        """Test block tag renders JS only once."""
        formset1 = self._create_formset(prefix="items1")
        formset2 = self._create_formset(prefix="items2")
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs1 prefix="items1" %}{{ subform.name }}{% endformset %}
        {% formset fs2 prefix="items2" %}{{ subform.name }}{% endformset %}
        """
        )

        result = template.render(Context({"fs1": formset1, "fs2": formset2}))
        count = result.count("data-formset-manager-js")
        self.assertEqual(count, 1)

    def test_formset_block_tag_renders_remove_buttons(self):
        """Test block tag renders remove buttons by default."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" %}
            {{ subform.name }}
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertIn('data-formset-remove="items"', result)

    def test_formset_block_tag_hide_remove_buttons(self):
        """Test block tag can hide remove buttons."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" show_remove=False %}
            {{ subform.name }}
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertNotIn('data-formset-remove="items"', result)

    def test_formset_block_tag_custom_wrapper_class(self):
        """Test block tag uses custom wrapper class."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" wrapper_class="custom-row" %}
            {{ subform.name }}
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertIn('class="custom-row"', result)

    def test_formset_block_tag_renders_form_fields(self):
        """Test block tag renders form fields correctly."""
        formset = self._create_formset()
        _reset_js_rendered()

        template = Template(
            """
        {% load formset_tags %}
        {% formset fs prefix="items" %}
            <div class="field">{{ subform.name }}</div>
        {% endformset %}
        """
        )

        result = template.render(Context({"fs": formset}))
        self.assertIn('class="field"', result)
        self.assertIn("id_items-0-name", result)


class TestFormsetTemplateTagsInTemplate(TestCase):
    """Tests for formset template tags when used in actual templates."""

    def setUp(self):
        """Reset JS rendered flag before each test."""
        _reset_js_rendered()

    def test_formset_script_in_template(self):
        """Test formset_script tag works in template context."""
        template = Template("{% load formset_tags %}{% formset_script %}")
        result = template.render(Context({}))
        self.assertIn("FormsetManagerClass", result)

    def test_formset_container_in_template(self):
        """Test formset_container tag works in template context."""
        template = Template('{% load formset_tags %}<div {% formset_container "test" %}></div>')
        result = template.render(Context({}))
        self.assertIn('data-formset-container=""', result)
        self.assertIn('data-formset-prefix="test"', result)

    def test_formset_add_btn_in_template(self):
        """Test formset_add_btn tag works in template context."""
        template = Template('{% load formset_tags %}{% formset_add_btn "test" "Add Row" %}')
        result = template.render(Context({}))
        self.assertIn("<button", result)
        self.assertIn("Add Row", result)

    def test_formset_remove_btn_in_template(self):
        """Test formset_remove_btn tag works in template context."""
        template = Template(
            '{% load formset_tags %}<button {% formset_remove_btn "test" %}>Remove</button>'
        )
        result = template.render(Context({}))
        self.assertIn('data-formset-remove="test"', result)


class TestFormsetManagerIntegration(TestCase):
    """Integration tests for FormsetManager with Django formsets."""

    def setUp(self):
        """Reset JS rendered flag before each test."""
        _reset_js_rendered()

    def test_formset_rendering_pattern_advanced(self):
        """Test the complete formset rendering pattern with advanced tags."""

        class ItemForm(forms.Form):
            name = forms.CharField()
            quantity = forms.IntegerField()

        ItemFormSet = forms.formset_factory(ItemForm, extra=1)
        formset = ItemFormSet(prefix="items")

        template = Template(
            """
        {% load formset_tags %}
        {{ formset.management_form }}
        <div id="items_formset" {% formset_container "items" %}>
            {% for form in formset %}
                <div class="form-row" {% formset_form_wrapper %}>
                    {{ form.name }} {{ form.quantity }}
                </div>
            {% endfor %}
        </div>
        <div id="empty_items_form" class="d-none">
            <div class="form-row" {% formset_form_wrapper %}>
                {{ formset.empty_form.name }} {{ formset.empty_form.quantity }}
            </div>
        </div>
        {% formset_add_btn "items" "Add Item" %}
        {% formset_script %}
        """
        )

        result = template.render(Context({"formset": formset}))

        # Check all necessary elements are present
        self.assertIn('data-formset-container=""', result)
        self.assertIn('data-formset-prefix="items"', result)
        self.assertIn('data-formset-form=""', result)
        self.assertIn('data-formset-add="items"', result)
        self.assertIn("data-formset-manager-js", result)
        self.assertIn("id_items-TOTAL_FORMS", result)

    def test_script_only_rendered_once_across_formsets(self):
        """Test script is only rendered once even with multiple formsets."""
        template = Template(
            """
        {% load formset_tags %}
        {% formset_script %}
        {% formset_script %}
        {% formset_script %}
        """
        )

        result = template.render(Context({}))

        # Should only appear once
        count = result.count("data-formset-manager-js")
        self.assertEqual(count, 1)
