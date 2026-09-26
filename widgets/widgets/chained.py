"""
Chained Select Widget for Django

A widget that renders dependent/cascading dropdowns with zero configuration.
Render the field and include {{ form.media }} in standalone templates.
"""

from django import forms
from django.utils.safestring import mark_safe

from widgets.utils import config_script


class ChainedSelect(forms.Select):
    """
    A Select widget for cascading/dependent dropdowns.

    Declares its JavaScript through Django Media.
    Include {{ form.media }} when rendering standalone fragments.
    """

    class Media:
        js = ("widgets/chained.js",)

    def __init__(
        self,
        chain_name=None,
        chain_position=0,
        parent_field=None,
        choices_tree=None,
        ajax_url=None,
        form_path=None,
        empty_label="---------",
        attrs=None,
        choices=(),
    ):
        self.chain_name = chain_name
        self.chain_position = chain_position
        self.parent_field = parent_field
        self.choices_tree = choices_tree
        self.ajax_url = ajax_url
        self.form_path = form_path
        self.empty_label = empty_label

        super().__init__(attrs=attrs, choices=choices)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)

        attrs["data-chained-select"] = "true"

        if self.chain_name:
            attrs["data-chain-name"] = self.chain_name
        attrs["data-chain-position"] = str(self.chain_position)

        if self.parent_field:
            attrs["data-parent-field"] = self.parent_field

        if self.ajax_url:
            attrs["data-ajax-url"] = self.ajax_url

        if self.form_path:
            attrs["data-form-path"] = self.form_path

        attrs["data-empty-label"] = self.empty_label

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} chained-select".strip()

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if self.choices_tree and self.chain_position == 0 and self.chain_name:
            html += config_script(self.choices_tree, **{"data-chain-tree": self.chain_name})
        return mark_safe(html)
