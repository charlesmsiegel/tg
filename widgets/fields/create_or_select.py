"""
Create or Select Form Field

Provides CreateOrSelectField that combines a toggle, select dropdown,
and integrates with a creation form for a streamlined create-or-select experience.
"""

from django import forms

from ..widgets.create_or_select import CreateOrSelectWidget


class CreateOrSelectField(forms.BooleanField):
    """
    A boolean field representing the create-or-select toggle.

    When True: user is creating a new object
    When False: user is selecting an existing object

    Works with CreateOrSelectWidget to auto-inject JavaScript for visibility toggling.

    Usage:
        class MyForm(forms.Form):
            select_or_create = CreateOrSelectField(
                label="Create new?",
                select_field='select',
                required_if_selecting=True,  # Require selection when not creating
            )
            select = forms.ModelChoiceField(queryset=Model.objects.all(), required=False)
            # ... creation fields

    The field automatically validates that either a selection is made or
    creation mode is enabled.
    """

    widget = CreateOrSelectWidget

    def __init__(
        self,
        *,
        select_field="select",
        required_if_selecting=True,
        create_error_message=None,
        group_name=None,
        **kwargs,
    ):
        """
        Initialize the field.

        Args:
            select_field: Name of the ModelChoiceField used for selection.
            required_if_selecting: If True, selection is required when not creating.
            create_error_message: Custom error message when neither mode is satisfied.
            group_name: Custom group name for the toggle (passed to widget).
            **kwargs: Standard field arguments.
        """
        self.select_field = select_field
        self.required_if_selecting = required_if_selecting
        self.create_error_message = create_error_message or (
            f"You must either select an existing item or choose to create a new one."
        )
        self.group_name = group_name

        # Override widget with configured group name
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", CreateOrSelectWidget(group_name=group_name))

        super().__init__(**kwargs)

    def clean(self, value):
        """Clean the value - boolean for create mode."""
        # Convert to boolean (checkbox values can be various truthy things)
        return bool(value)


class CreateOrSelectModelChoiceField(forms.ModelChoiceField):
    """
    A ModelChoiceField variant designed to work with CreateOrSelectField.

    Provides automatic required validation based on the toggle state.
    """

    def __init__(self, queryset, *, toggle_field="select_or_create", **kwargs):
        """
        Initialize the field.

        Args:
            queryset: The queryset for available selections.
            toggle_field: Name of the CreateOrSelectField that controls this field.
            **kwargs: Standard ModelChoiceField arguments.
        """
        self.toggle_field = toggle_field
        kwargs.setdefault("required", False)
        super().__init__(queryset, **kwargs)
