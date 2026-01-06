"""
Chained Select Form Fields

Provides ChainedChoiceField and ChainedModelChoiceField that automatically
configure themselves. Just define the fields and add the mixin.
"""

from django import forms

from ..widgets.chained import ChainedSelect


class ChainedChoiceField(forms.ChoiceField):
    """
    A ChoiceField for use in cascading dropdown chains.

    For root fields (no parent), provide choices directly.
    For child fields, provide parent_field and either:
      - choices_map: dict mapping parent values to choice lists
      - choices_callback: function(parent_value) -> choice list

    Example:
        affiliation = ChainedChoiceField(
            choices=[('traditions', 'Traditions'), ('technocracy', 'Technocracy')]
        )

        faction = ChainedChoiceField(
            parent_field='affiliation',
            choices_map={
                'traditions': [('hermetic', 'Order of Hermes'), ...],
                'technocracy': [('iteration_x', 'Iteration X'), ...],
            }
        )
    """

    widget = ChainedSelect

    def __init__(
        self,
        *,
        parent_field=None,
        choices_map=None,
        choices_callback=None,
        empty_label="---------",
        # Standard ChoiceField args
        choices=(),
        **kwargs,
    ):
        self.parent_field = parent_field
        self.choices_map = choices_map
        self.choices_callback = choices_callback
        self.empty_label = empty_label
        self._chain_name = None  # Set by mixin
        self._chain_position = None  # Set by mixin

        # For root field, use provided choices
        # For child fields, start with empty (populated dynamically)
        if parent_field and not choices:
            choices = [("", empty_label)]
        elif not any(c[0] == "" for c in choices):
            # Prepend empty choice if not present
            choices = [("", empty_label)] + list(choices)

        super().__init__(choices=choices, **kwargs)

    def valid_value(self, value):
        """Allow values that will be validated at form level."""
        if value == "":
            return True
        if not self.parent_field:
            return super().valid_value(value)
        # Child fields defer to form-level validation
        return True

    def get_choices_for_parent(self, parent_value):
        """Get valid choices given a parent value."""
        choices = [("", self.empty_label)]

        if not parent_value:
            return choices

        if self.choices_map and parent_value in self.choices_map:
            choices.extend(self.choices_map[parent_value])
        elif self.choices_callback:
            result = self.choices_callback(parent_value)
            # Handle querysets
            if hasattr(result, "__iter__") and not isinstance(result, (str, dict)):
                choices.extend(result)

        return choices

    def get_full_choices_tree(self):
        """
        Get the complete choices tree for embedding in page.
        Returns dict mapping parent values to child choices.
        """
        if self.choices_map:
            return self.choices_map
        return None


class ChainedModelChoiceField(forms.ModelChoiceField):
    """
    A ModelChoiceField variant for chained selects with database-backed choices.

    Example:
        faction = ChainedModelChoiceField(
            queryset=Faction.objects.none(),  # Start empty
            parent_field='affiliation',
            parent_fk='affiliation',  # FK field name on model
        )
    """

    widget = ChainedSelect

    def __init__(
        self, queryset, *, parent_field=None, parent_fk=None, empty_label="---------", **kwargs
    ):
        self.parent_field = parent_field
        self.parent_fk = parent_fk or parent_field
        self._chain_name = None
        self._chain_position = None

        super().__init__(queryset=queryset, empty_label=empty_label, **kwargs)

    def get_queryset_for_parent(self, parent_value):
        """Get filtered queryset for a parent value."""
        if not parent_value:
            return self.queryset.none()
        return self.queryset.filter(**{self.parent_fk: parent_value})
