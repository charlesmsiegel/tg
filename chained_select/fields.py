"""
Chained Select Form Fields and Mixin - Self-Contained Version

Provides ChainedChoiceField and ChainedModelChoiceField that automatically
configure themselves. Just define the fields and add the mixin.
"""

import uuid

from django import forms
from django.core.exceptions import ValidationError

from .widgets import ChainedSelect


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


class ChainedSelectMixin:
    """
    Mixin for forms with chained select fields.

    Automatically:
    - Detects ChainedChoiceFields and links them into chains
    - Configures widgets with proper data attributes
    - Builds and embeds choice trees for client-side operation
    - Validates that selections are consistent

    Usage:
        class MyForm(ChainedSelectMixin, forms.Form):
            affiliation = ChainedChoiceField(choices=[...])
            faction = ChainedChoiceField(parent_field='affiliation', choices_map={...})
            subfaction = ChainedChoiceField(parent_field='faction', choices_map={...})

    That's it! Include {{ form.media }} in your template and it just works.
    """

    # Override to use a custom AJAX URL instead of the auto-registered one
    chained_ajax_url = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_chains()

    def _get_form_path(self):
        """Get the full import path for this form class."""
        cls = self.__class__
        return f"{cls.__module__}.{cls.__name__}"

    def _setup_chains(self):
        """Detect and configure all chained field relationships."""

        # Find all chained fields and their relationships
        chained_fields = {}
        for name, field in self.fields.items():
            if isinstance(field, (ChainedChoiceField, ChainedModelChoiceField)):
                chained_fields[name] = {
                    "field": field,
                    "parent": getattr(field, "parent_field", None),
                }

        if not chained_fields:
            return

        # Build chains by following parent relationships
        chains = self._build_chains(chained_fields)

        # Configure each chain
        for chain_name, field_names in chains.items():
            self._configure_chain(chain_name, field_names)

    def _build_chains(self, chained_fields):
        """
        Build chains from parent relationships.
        Returns dict of chain_name -> [field_names in order]
        """
        chains = {}
        chain_counter = 0

        # Find root fields (no parent)
        roots = [name for name, info in chained_fields.items() if not info["parent"]]

        for root in roots:
            chain_name = f"chain_{chain_counter}"
            chain_counter += 1

            # Follow the chain from root to leaves
            chain = [root]
            current = root

            while True:
                # Find child of current
                child = None
                for name, info in chained_fields.items():
                    if info["parent"] == current:
                        child = name
                        break

                if child:
                    chain.append(child)
                    current = child
                else:
                    break

            chains[chain_name] = chain

        return chains

    def _configure_chain(self, chain_name, field_names):
        """Configure widgets and build choice tree for a chain."""

        # Build the complete choices tree for embedding
        choices_tree = {}

        # Determine AJAX URL - use auto-registered one if not specified
        ajax_url = self.chained_ajax_url or "/__chained_select__/"
        form_path = self._get_form_path()

        # Check if any field needs AJAX (has choices_callback but no choices_map)
        needs_ajax = any(
            isinstance(self.fields[name], ChainedChoiceField)
            and self.fields[name].choices_callback
            and not self.fields[name].choices_map
            for name in field_names
        )

        for position, field_name in enumerate(field_names):
            field = self.fields[field_name]
            parent_field = field_names[position - 1] if position > 0 else None

            # Store chain info on field
            field._chain_name = chain_name
            field._chain_position = position

            # Configure widget
            widget = field.widget
            if not isinstance(widget, ChainedSelect):
                # Wrap in ChainedSelect
                widget = ChainedSelect(
                    choices=field.choices,
                    attrs=widget.attrs if hasattr(widget, "attrs") else {},
                )
                field.widget = widget

            widget.chain_name = chain_name
            widget.chain_position = position
            widget.parent_field = parent_field
            widget.empty_label = getattr(field, "empty_label", "---------")

            # Set AJAX URL and form path if this field needs AJAX
            if needs_ajax and isinstance(field, ChainedChoiceField) and field.choices_callback:
                widget.ajax_url = ajax_url
                widget.form_path = form_path

            # Build choices tree for this field
            if isinstance(field, ChainedChoiceField):
                if position == 0:
                    # Root field - store its choices
                    choices_tree["_root"] = [
                        {"value": str(v), "label": str(l)} for v, l in field.choices if v != ""
                    ]
                    choices_tree["_root_field"] = field_name

                # Get choices map for children to use (for embedded mode)
                if field.choices_map:
                    for parent_val, child_choices in field.choices_map.items():
                        key = f"{field_name}:{parent_val}"
                        choices_tree[key] = [
                            {"value": str(v), "label": str(l)} for v, l in child_choices
                        ]

        # Attach tree to root widget for embedding
        root_field = self.fields[field_names[0]]
        root_field.widget.choices_tree = choices_tree

        # Populate choices for bound forms / initial data
        self._populate_initial_choices(field_names)

    def _populate_initial_choices(self, field_names):
        """Populate child fields based on initial/bound data."""
        for position, field_name in enumerate(field_names):
            if position == 0:
                continue

            field = self.fields[field_name]
            parent_field_name = field_names[position - 1]

            # Get parent value
            parent_value = None
            if self.is_bound:
                parent_value = self.data.get(self.add_prefix(parent_field_name))
            elif self.initial:
                parent_value = self.initial.get(parent_field_name)

            # Handle model instances - get the pk
            if hasattr(parent_value, "pk"):
                parent_value = parent_value.pk

            if parent_value and isinstance(field, ChainedChoiceField):
                choices = field.get_choices_for_parent(parent_value)
                field.choices = choices
                field.widget.choices = choices

    def clean(self):
        """Validate chained field consistency."""
        cleaned_data = super().clean()

        # Find all chains and validate
        validated_chains = set()

        for field_name, field in self.fields.items():
            if not isinstance(field, (ChainedChoiceField, ChainedModelChoiceField)):
                continue
            if not field.parent_field:
                continue

            chain_name = getattr(field, "_chain_name", None)
            if chain_name in validated_chains:
                continue

            # Validate this field against its parent
            value = cleaned_data.get(field_name)
            parent_value = cleaned_data.get(field.parent_field)

            # Handle model instances - get the pk for comparison
            if hasattr(parent_value, "pk"):
                parent_value = parent_value.pk

            if value and isinstance(field, ChainedChoiceField):
                valid_choices = field.get_choices_for_parent(parent_value)
                valid_values = [str(c[0]) for c in valid_choices]

                if str(value) not in valid_values:
                    self.add_error(
                        field_name,
                        ValidationError(
                            f"Invalid selection for the chosen {field.parent_field}.",
                            code="invalid_choice",
                        ),
                    )

        return cleaned_data
