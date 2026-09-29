"""
Chained Select Form Mixin

Mixin for forms with chained select fields.
"""

from django.core.exceptions import ValidationError

from ..fields.chained import ChainedChoiceField, ChainedModelChoiceField
from ..widgets.chained import ChainedSelect, HtmxChainedSelect


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
            if isinstance(field, ChainedChoiceField | ChainedModelChoiceField):
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
                        self._choice_to_dict(choice) for choice in field.choices if choice[0] != ""
                    ]
                    choices_tree["_root_field"] = field_name

                # Get choices map for children to use (for embedded mode)
                if field.choices_map:
                    for parent_val, child_choices in field.choices_map.items():
                        key = f"{parent_field}:{parent_val}"
                        choices_tree[key] = [
                            self._choice_to_dict(choice) for choice in child_choices
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

    def chain_for(self, name):
        """Field names of the chain containing ``name``, root first.

        Follows ``parent_field`` links, so a plain ChoiceField can be the root
        (as ``category`` is in the freebie forms).
        """
        children = {}
        for field_name, field in self.fields.items():
            parent = getattr(field, "parent_field", None)
            if isinstance(field, ChainedChoiceField) and parent in self.fields:
                children[parent] = field_name
        root = name
        while getattr(self.fields[root], "parent_field", None) in self.fields:
            root = self.fields[root].parent_field
        chain = [root]
        while chain[-1] in children:
            chain.append(children[chain[-1]])
        return chain

    def enable_htmx_chains(self, options_url):
        """Fetch child options from ``options_url`` instead of an embedded tree.

        Children are (re)filled from the current parent values, so a bound form
        re-renders with the options for what was submitted.
        """
        self.htmx_chains = True
        roots = {
            tuple(self.chain_for(name))
            for name, field in self.fields.items()
            if isinstance(field, ChainedChoiceField) and field.parent_field in self.fields
        }
        for names in roots:
            include = ", ".join(f"#{self[name].auto_id}" for name in names)
            for position, name in enumerate(names):
                field = self.fields[name]
                if position:
                    parent_value = self._chain_value(names[position - 1])
                    # Option metadata (3-tuples) stays in choices_map for the
                    # server's visibility rules; Select renders (value, label).
                    field.choices = [
                        choice[:2] for choice in field.get_choices_for_parent(parent_value)
                    ]
                child = names[position + 1] if position + 1 < len(names) else None
                widget = HtmxChainedSelect(
                    options_url=options_url,
                    child=child,
                    child_id=self[child].auto_id if child else None,
                    include=include,
                    attrs=field.widget.attrs,
                )
                widget.choices = field.choices
                field.widget = widget

    def _chain_value(self, name):
        if self.is_bound:
            return self.data.get(self.add_prefix(name), "")
        field = self.fields[name]
        value = self.get_initial_for_field(field, name)
        value = getattr(value, "pk", value)
        if value in (None, "") and getattr(field, "choices", None):
            # An unselected <select> shows (and submits) its first option, so
            # its children must start with that option's choices.
            value = next(iter(field.choices), ("",))[0]
        return "" if value is None else value

    def _choice_to_dict(self, choice):
        """
        Convert a choice tuple to a dict for the choices tree.

        Supports:
        - 2-tuple: (value, label)
        - 3-tuple: (value, label, metadata_dict)
        """
        if len(choice) >= 3:
            return {"value": str(choice[0]), "label": str(choice[1]), "metadata": choice[2]}
        return {"value": str(choice[0]), "label": str(choice[1])}

    def clean(self):
        """Validate chained field consistency."""
        cleaned_data = super().clean()

        # Find all chains and validate
        validated_chains = set()

        for field_name, field in self.fields.items():
            if not isinstance(field, ChainedChoiceField | ChainedModelChoiceField):
                continue
            if not field.parent_field:
                continue

            chain_name = getattr(field, "_chain_name", None)
            if chain_name in validated_chains:
                continue

            # Validate this field against its parent
            value = cleaned_data.get(field_name)
            parent_value = cleaned_data.get(field.parent_field)

            # Handle model instances - get the pk for comparison. A field's
            # clean_<name>() may already have turned its value into one.
            if hasattr(parent_value, "pk"):
                parent_value = parent_value.pk
            if hasattr(value, "pk"):
                value = value.pk

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
