"""
Create or Select Widget for Django

A checkbox widget declaring JavaScript through Django Media to switch between
"select existing" and "create new" modes.

Declares its JavaScript through Django Media.
Include {{ form.media }} when rendering standalone fragments.
"""

from django import forms


class CreateOrSelectWidget(forms.CheckboxInput):
    """
    A checkbox widget that toggles visibility between select and create containers.

    Declares its JavaScript through Django Media.
    Include {{ form.media }} when rendering standalone fragments.

    Usage in template:
        <div data-create-or-select-container="{{ form.field_name.name }}" data-create-or-select-mode="select">
            {{ form.select_field }}
        </div>
        <div data-create-or-select-container="{{ form.field_name.name }}" data-create-or-select-mode="create">
            {{ form.create_fields }}
        </div>

    Or use the simpler template tags provided by this module.
    """

    class Media:
        js = ("widgets/create_or_select.js",)

    def __init__(self, group_name=None, create_label="Create new", attrs=None):
        """
        Initialize the widget.

        Args:
            group_name: Optional custom group name. If not provided, uses the field name.
            create_label: Label text for the checkbox (displayed next to toggle)
            attrs: Additional HTML attributes for the checkbox
        """
        self.group_name = group_name
        self.create_label = create_label
        super().__init__(attrs=attrs)

    def get_group_name(self, name):
        """Get the group name for this toggle, deriving from field name if not set."""
        return self.group_name or name

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        # Add data attributes for the toggle
        if attrs is None:
            attrs = {}

        group_name = self.get_group_name(name)
        attrs["data-create-or-select-toggle"] = "true"
        attrs["data-create-or-select-group"] = group_name

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} create-or-select-toggle".strip()

        return super().render(name, value, attrs, renderer)
