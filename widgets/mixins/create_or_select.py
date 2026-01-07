"""
Create or Select Form Mixin

Provides CreateOrSelectMixin for automatic handling of create-or-select
validation and save logic in ModelForms.
"""


class CreateOrSelectMixin:
    """
    Mixin for ModelForms that implement a create-or-select pattern.

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
            select = forms.ModelChoiceField(queryset=Effect.objects.all(), required=False)

            class Meta:
                model = Effect
                fields = ['select_or_create', 'select', 'name', 'description', ...]

    Attributes:
        create_or_select_config (dict): Configuration for the mixin with keys:
            - toggle_field: Name of the boolean toggle field (default: 'select_or_create')
            - select_field: Name of the selection field (default: 'select')
            - error_message: Custom validation error message
    """

    create_or_select_config = {}

    def get_create_or_select_config(self):
        """Get the configuration with defaults."""
        defaults = {
            "toggle_field": "select_or_create",
            "select_field": "select",
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

    def _is_creating_from_data(self):
        """Check if in create mode directly from cleaned_data (for use in _post_clean)."""
        config = self.get_create_or_select_config()
        toggle_field = config["toggle_field"]
        return getattr(self, "cleaned_data", {}).get(toggle_field, False)

    def _post_clean(self):
        """
        Skip model validation when in select mode.

        When selecting an existing object, we don't need to validate the model
        fields since we're returning an existing (already valid) object.
        """
        # If we're in select mode with a valid selection, skip model validation
        if not self._is_creating_from_data():
            config = self.get_create_or_select_config()
            select_field = config["select_field"]
            selection = self.cleaned_data.get(select_field)
            if selection:
                # Clear any model-related errors since we're using an existing object
                # Don't run model validation - just ensure the instance is set
                self.instance = selection
                return
        # In create mode, run normal model validation
        super()._post_clean()

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
