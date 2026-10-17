"""Dynamic widget text and attributes must not become executable markup."""

from django import forms
from django.template import Context, Template
from django.test import SimpleTestCase
from django.utils.html import escape
from django.utils.safestring import mark_safe

from widgets.mixins.conditional import ConditionalFieldsMixin
from widgets.templatetags.formset_tags import formset_add_btn, formset_container


class WidgetHTMLEscapingTests(SimpleTestCase):
    def test_conditional_label_escapes_text_and_preserves_field_markup(self):
        class DetailForm(ConditionalFieldsMixin, forms.Form):
            detail = forms.CharField()

        form = DetailForm()
        label = '<img src=x onerror="alert(1)"> & detail'
        html = form.wrap_field("detail", label)
        self.assertIn(escape(label), html)
        self.assertNotIn("<img", html)
        self.assertIn(str(form["detail"]), html)
        self.assertIn('id="detail_wrap" class="col-sm d-none"', html)

    def test_conditional_label_preserves_explicitly_trusted_markup(self):
        class DetailForm(ConditionalFieldsMixin, forms.Form):
            detail = forms.CharField()

        html = DetailForm().wrap_field("detail", mark_safe("<strong>Detail</strong>"))
        self.assertIn("<strong>Detail</strong> <input", html)

    def test_advanced_container_escapes_attribute_values(self):
        value = 'items" onmouseover="alert(1)'
        html = formset_container(value, empty_form_id=value, animate=True)
        self.assertIn(f'data-formset-prefix="{escape(value)}"', html)
        self.assertIn(f'data-formset-empty-form="{escape(value)}"', html)
        self.assertNotIn(' onmouseover="', html)
        self.assertIn('data-formset-animate="true"', html)

    def test_advanced_button_escapes_text_and_attributes(self):
        value = 'items" onclick="alert(1)'
        label = '<img src=x onerror="alert(1)">'
        html = formset_add_btn(value, label, **{"class": value, "aria_label": value})
        for name in ("data-formset-add", "class", "aria-label"):
            self.assertIn(f'{name}="{escape(value)}"', html)
        self.assertIn(escape(label), html)
        self.assertNotIn("<img", html)
        self.assertNotIn(' onclick="', html)

    def test_advanced_button_preserves_trusted_label(self):
        html = formset_add_btn("items", mark_safe("<strong>Add</strong>"))
        self.assertIn("<strong>Add</strong></button>", html)

    def render_formset(self, value, label):
        class ItemForm(forms.Form):
            name = forms.CharField()

        formset = forms.formset_factory(ItemForm, extra=1)(prefix="items")
        template = Template(
            "{% load formset_tags %}"
            "{% formset fs prefix=value add_label=label remove_label=label "
            "add_class=value remove_class=value wrapper_class=value animate=True %}"
            "<span>{{ subform.name }}</span>{% endformset %}"
        )
        return template.render(Context({"fs": formset, "value": value, "label": label}))

    def test_block_tag_escapes_dynamic_attributes_and_labels(self):
        value = 'items" onclick="alert(1)'
        label = '<img src=x onerror="alert(1)">'
        html = self.render_formset(value, label)
        for fragment in (
            f'id="{escape(value)}_formset"',
            f'id="empty_{escape(value)}_form"',
            f'data-formset-prefix="{escape(value)}"',
            f'data-formset-add="{escape(value)}"',
            f'data-formset-remove="{escape(value)}"',
            f'class="{escape(value)}"',
        ):
            self.assertIn(fragment, html)
        self.assertEqual(html.count(escape(label)), 3)
        self.assertNotIn("<img", html)
        self.assertNotIn(' onclick="', html)
        self.assertIn('<span><input type="text"', html)
        self.assertIn('name="items-TOTAL_FORMS"', html)
        self.assertIn('data-formset-animate="true"', html)

    def test_block_tag_preserves_trusted_label_and_normal_markup(self):
        html = self.render_formset("items", mark_safe("<strong>Add</strong>"))
        self.assertEqual(html.count("<strong>Add</strong></button>"), 3)
        self.assertIn('id="items_formset"', html)
        self.assertIn('id="empty_items_form"', html)
        self.assertIn('name="items-__prefix__-name"', html)
