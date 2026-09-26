"""
Point Pool Widget for Django

A widget that manages point allocations across form fields with real-time
validation and constraint enforcement.

Supports two modes:
1. Simple Mode: Single budget constraint across fields (e.g., 7 points for backgrounds)
2. Distribution Mode: Multiple groups with target totals in any permutation
   (e.g., primary/secondary/tertiary patterns)
"""

from django import forms
from django.utils.safestring import mark_safe

from widgets.utils import config_script


class PointPoolInput(forms.NumberInput):
    """
    A number input widget for point pool fields.

    Declares its JavaScript through Django Media.
    Works with PointPoolMixin to provide constraint enforcement.
    """

    class Media:
        js = ("widgets/point_pool.js",)

    def __init__(
        self,
        pool_name=None,
        pool_group=None,
        pool_config=None,
        is_root=False,
        attrs=None,
    ):
        self.pool_name = pool_name
        self.pool_group = pool_group
        self.pool_config = pool_config
        self.is_root = is_root  # First widget renders config

        if attrs is None:
            attrs = {}
        super().__init__(attrs=attrs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)

        attrs["data-point-pool"] = "true"

        if self.pool_name:
            attrs["data-pool-name"] = self.pool_name

        if self.pool_group:
            attrs["data-pool-group"] = self.pool_group

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} point-pool-input".strip()

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if self.is_root and self.pool_config and self.pool_name:
            html += config_script(self.pool_config, **{"data-pool-config": self.pool_name})
        return mark_safe(html)


class PointPoolSelect(forms.Select):
    """
    A select widget for point pool fields.

    Use this when fields have a finite set of valid values (e.g., 0-5).
    """

    class Media:
        js = ("widgets/point_pool.js",)

    def __init__(
        self,
        pool_name=None,
        pool_group=None,
        pool_config=None,
        is_root=False,
        attrs=None,
        choices=(),
    ):
        self.pool_name = pool_name
        self.pool_group = pool_group
        self.pool_config = pool_config
        self.is_root = is_root

        if attrs is None:
            attrs = {}
        super().__init__(attrs=attrs, choices=choices)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)

        attrs["data-point-pool"] = "true"

        if self.pool_name:
            attrs["data-pool-name"] = self.pool_name

        if self.pool_group:
            attrs["data-pool-group"] = self.pool_group

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} point-pool-select".strip()

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if self.is_root and self.pool_config and self.pool_name:
            html += config_script(self.pool_config, **{"data-pool-config": self.pool_name})
        return mark_safe(html)
