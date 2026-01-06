"""
Create or Select Form Mixin

Provides CreateOrSelectMixin for automatic handling of create-or-select
validation and save logic in ModelForms.
"""

from django import forms


class CreateOrSelectMixin:
    """
    Mixin for forms that implement a create-or-select pattern.

    Provides:
    - Automatic validation ensuring selection when not creating
    - A save() method that returns existing objects or creates new ones
    - Helper methods for determining current mode

    Usage:
        class EffectCreateOrSelectForm(CreateOrSelectMixin, forms.ModelForm):
            # Configure the mixin
            create_or_select_config = {
                'toggle_field': 'select_or_create',
                'select_field': 'select',
                'error_message': 'Please select an effect or create a new one.',
            }

            select_or_create = CreateOrSelectField()
            select = CreateOrSelectModelChoiceField(queryset=Effect.objects.all())

            class Meta:
                model = Effect
                fields = ['name', 'description', ...]

    Attributes:
        create_or_select_config (dict): Configuration for the mixin with keys:
            - toggle_field: Name of the boolean toggle field (default: 'select_or_create')
            - select_field: Name of the selection field (default: 'select')
            - error_message: Custom validation error message
            - exclude_from_create: List of fields to exclude when determining creation data
    """

    create_or_select_config = {}

    def get_create_or_select_config(self):
        """Get the configuration with defaults."""
        defaults = {
            "toggle_field": "select_or_create",
            "select_field": "select",
            "error_message": "You must either select an existing item or choose to create a new one.",
            "exclude_from_create": None,
        }
        config = defaults.copy()
        config.update(self.create_or_select_config)
        return config

    def is_creating(self):
        """Return True if the form is in create mode."""
        config = self.get_create_or_select_config()
        toggle_field = config["toggle_field"]
        return self.cleaned_data.get(toggle_field, False)

    def get_selected_object(self):
        """Return the selected object, or None if creating or no selection."""
        if self.is_creating():
            return None
        config = self.get_create_or_select_config()
        select_field = config["select_field"]
        return self.cleaned_data.get(select_field)

    def clean(self):
        """Validate that either selection is made or creation mode is enabled."""
        cleaned_data = super().clean()
        config = self.get_create_or_select_config()

        toggle_field = config["toggle_field"]
        select_field = config["select_field"]
        error_message = config["error_message"]

        is_creating = cleaned_data.get(toggle_field, False)
        selection = cleaned_data.get(select_field)

        # If not creating, must have a selection
        if not is_creating and not selection:
            self.add_error(select_field, error_message)

        return cleaned_data

    def save(self, commit=True):
        """
        Save the form, returning either the selected object or a new instance.

        Returns:
            The selected object if not creating, or a new instance if creating.
        """
        # If not creating and we have a selection, return the selected object
        selected = self.get_selected_object()
        if selected is not None:
            return selected

        # Otherwise, create a new instance via the standard ModelForm save
        return super().save(commit=commit)


class CreateOrSelectFormMixin:
    """
    Mixin for regular Form classes (not ModelForm) that delegate to a nested form.

    Usage:
        class ArtifactCreateOrSelectForm(CreateOrSelectFormMixin, forms.Form):
            create_or_select_config = {
                'toggle_field': 'select_or_create',
                'select_field': 'select',
                'creation_form_attr': 'artifact_form',
            }

            select_or_create = CreateOrSelectField()
            select = forms.ModelChoiceField(queryset=SorcererArtifact.objects.all(), required=False)

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.artifact_form = SorcererArtifactForm(
                    data=self.data if self.is_bound else None,
                    prefix="artifact",
                )
    """

    create_or_select_config = {}

    def get_create_or_select_config(self):
        """Get the configuration with defaults."""
        defaults = {
            "toggle_field": "select_or_create",
            "select_field": "select",
            "creation_form_attr": None,
            "error_message": "You must either select an existing item or choose to create a new one.",
        }
        config = defaults.copy()
        config.update(self.create_or_select_config)
        return config

    def is_creating(self):
        """Return True if the form is in create mode."""
        config = self.get_create_or_select_config()
        toggle_field = config["toggle_field"]
        return self.cleaned_data.get(toggle_field, False)

    def get_selected_object(self):
        """Return the selected object, or None if creating or no selection."""
        if self.is_creating():
            return None
        config = self.get_create_or_select_config()
        select_field = config["select_field"]
        return self.cleaned_data.get(select_field)

    def get_creation_form(self):
        """Return the nested creation form, if configured."""
        config = self.get_create_or_select_config()
        form_attr = config.get("creation_form_attr")
        if form_attr:
            return getattr(self, form_attr, None)
        return None

    def clean(self):
        """Validate that either selection is made or creation mode is enabled."""
        cleaned_data = super().clean()
        config = self.get_create_or_select_config()

        toggle_field = config["toggle_field"]
        select_field = config["select_field"]
        error_message = config["error_message"]

        is_creating = cleaned_data.get(toggle_field, False)
        selection = cleaned_data.get(select_field)

        # If not creating, must have a selection
        if not is_creating and not selection:
            self.add_error(select_field, error_message)

        # If creating and we have a nested form, validate it
        if is_creating:
            creation_form = self.get_creation_form()
            if creation_form and not creation_form.is_valid():
                # Propagate nested form errors
                for field, errors in creation_form.errors.items():
                    for error in errors:
                        self.add_error(None, f"{field}: {error}")

        return cleaned_data

    def save(self, commit=True):
        """
        Save the form, returning either the selected object or a new instance.

        Returns:
            The selected object if not creating, or a new instance from the nested form.
        """
        selected = self.get_selected_object()
        if selected is not None:
            return selected

        # Delegate to the creation form
        creation_form = self.get_creation_form()
        if creation_form:
            return creation_form.save(commit=commit)

        raise ValueError(
            "CreateOrSelectFormMixin.save() called in create mode but no creation_form_attr configured"
        )
