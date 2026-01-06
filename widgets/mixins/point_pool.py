"""
Point Pool Form Mixin

Mixin for forms with point pool fields that require constraint validation.
"""

from itertools import permutations

from django.core.exceptions import ValidationError

from ..widgets.point_pool import PointPoolInput, PointPoolSelect


class PointPoolMixin:
    """
    Mixin for forms with point pool allocation fields.

    Automatically:
    - Configures fields with point pool widgets
    - Validates point allocations against constraints
    - Supports simple (budget) and distribution (primary/secondary/tertiary) modes

    Simple Mode Usage (single budget):
        class BackgroundsForm(PointPoolMixin, forms.Form):
            pool_config = {
                'mode': 'simple',
                'pool_name': 'backgrounds',
                'total_budget': 7,
                'min_value': 0,
                'max_value': 5,
            }
            pool_fields = ['allies', 'contacts', 'resources', 'mentor', 'fame']

            allies = forms.IntegerField(min_value=0, max_value=5)
            contacts = forms.IntegerField(min_value=0, max_value=5)
            # ... etc

    Distribution Mode Usage (primary/secondary/tertiary):
        class AttributesForm(PointPoolMixin, forms.Form):
            pool_config = {
                'mode': 'distribution',
                'pool_name': 'attributes',
                'groups': {
                    'physical': ['strength', 'dexterity', 'stamina'],
                    'social': ['charisma', 'manipulation', 'appearance'],
                    'mental': ['perception', 'intelligence', 'wits'],
                },
                'targets': [6, 8, 10],  # tertiary, secondary, primary totals
                'min_value': 1,
                'max_value': 5,
            }
            pool_fields = ['strength', 'dexterity', 'stamina', ...]

            strength = forms.IntegerField(min_value=1, max_value=5)
            # ... etc
    """

    pool_config = None
    pool_fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_pool_widgets()

    def _setup_pool_widgets(self):
        """Configure point pool widgets for all pool fields."""
        if not self.pool_config or not self.pool_fields:
            return

        config = self.pool_config
        pool_name = config.get("pool_name", "pool")
        mode = config.get("mode", "simple")
        groups = config.get("groups", {})
        min_value = config.get("min_value", 0)
        max_value = config.get("max_value", 10)

        # Build group lookup for distribution mode
        field_to_group = {}
        if mode == "distribution" and groups:
            for group_name, field_names in groups.items():
                for field_name in field_names:
                    field_to_group[field_name] = group_name

        # Configure each pool field
        is_first = True
        for field_name in self.pool_fields:
            if field_name not in self.fields:
                continue

            field = self.fields[field_name]
            group_name = field_to_group.get(field_name)

            # Determine widget type based on field choices
            if hasattr(field, "choices") and field.choices:
                widget_class = PointPoolSelect
                widget = widget_class(
                    pool_name=pool_name,
                    pool_group=group_name,
                    pool_config=config if is_first else None,
                    is_root=is_first,
                    attrs=field.widget.attrs.copy() if hasattr(field.widget, "attrs") else {},
                    choices=field.choices,
                )
            else:
                widget_class = PointPoolInput
                widget = widget_class(
                    pool_name=pool_name,
                    pool_group=group_name,
                    pool_config=config if is_first else None,
                    is_root=is_first,
                    attrs=field.widget.attrs.copy() if hasattr(field.widget, "attrs") else {},
                )
                widget.attrs["min"] = min_value
                widget.attrs["max"] = max_value

            field.widget = widget
            is_first = False

    def clean(self):
        """Validate point pool constraints."""
        cleaned_data = super().clean()

        if not self.pool_config or not self.pool_fields:
            return cleaned_data

        config = self.pool_config
        mode = config.get("mode", "simple")

        if mode == "simple":
            self._validate_simple_pool(cleaned_data)
        elif mode == "distribution":
            self._validate_distribution_pool(cleaned_data)

        return cleaned_data

    def _validate_simple_pool(self, cleaned_data):
        """Validate simple mode: total must not exceed budget."""
        config = self.pool_config
        total_budget = config.get("total_budget", 0)
        min_value = config.get("min_value", 0)
        max_value = config.get("max_value", 10)

        total = 0
        for field_name in self.pool_fields:
            value = cleaned_data.get(field_name, 0)
            if value is None:
                value = 0

            # Validate range
            if value < min_value or value > max_value:
                self.add_error(
                    field_name,
                    ValidationError(
                        f"Value must be between {min_value} and {max_value}.",
                        code="invalid_range",
                    ),
                )
            total += value

        if total > total_budget:
            self.add_error(
                None,
                ValidationError(
                    f"Total points ({total}) exceeds budget ({total_budget}).",
                    code="budget_exceeded",
                ),
            )
        elif total < total_budget:
            self.add_error(
                None,
                ValidationError(
                    f"Must allocate exactly {total_budget} points (currently {total}).",
                    code="insufficient_allocation",
                ),
            )

    def _validate_distribution_pool(self, cleaned_data):
        """Validate distribution mode: groups must match target totals in some permutation."""
        config = self.pool_config
        groups = config.get("groups", {})
        targets = config.get("targets", [])
        min_value = config.get("min_value", 0)
        max_value = config.get("max_value", 10)

        # Calculate group totals
        group_totals = {}
        for group_name, field_names in groups.items():
            total = 0
            for field_name in field_names:
                value = cleaned_data.get(field_name, min_value)
                if value is None:
                    value = min_value

                # Validate range
                if value < min_value or value > max_value:
                    self.add_error(
                        field_name,
                        ValidationError(
                            f"Value must be between {min_value} and {max_value}.",
                            code="invalid_range",
                        ),
                    )
                total += value
            group_totals[group_name] = total

        # Check if distribution matches any permutation of targets
        sorted_totals = sorted(group_totals.values())
        sorted_targets = sorted(targets)

        if sorted_totals != sorted_targets:
            # Format error message
            target_str = "/".join(str(t) for t in sorted(targets, reverse=True))
            actual_str = ", ".join(f"{name}: {total}" for name, total in group_totals.items())
            self.add_error(
                None,
                ValidationError(
                    f"Distribution must be {target_str}. Current: {actual_str}.",
                    code="invalid_distribution",
                ),
            )


class SimplePoolMixin(PointPoolMixin):
    """
    Convenience mixin for simple budget-constrained pools.

    Usage:
        class BackgroundsForm(SimplePoolMixin, forms.Form):
            simple_pool_name = 'backgrounds'
            simple_pool_budget = 7
            simple_pool_min = 0
            simple_pool_max = 5
            pool_fields = ['allies', 'contacts', 'resources']

            allies = forms.IntegerField(min_value=0, max_value=5)
            # ...
    """

    simple_pool_name = "pool"
    simple_pool_budget = 0
    simple_pool_min = 0
    simple_pool_max = 10

    @property
    def pool_config(self):
        return {
            "mode": "simple",
            "pool_name": self.simple_pool_name,
            "total_budget": self.simple_pool_budget,
            "min_value": self.simple_pool_min,
            "max_value": self.simple_pool_max,
        }


class DistributionPoolMixin(PointPoolMixin):
    """
    Convenience mixin for distribution-constrained pools (primary/secondary/tertiary).

    Usage:
        class AttributesForm(DistributionPoolMixin, forms.Form):
            distribution_pool_name = 'attributes'
            distribution_groups = {
                'physical': ['strength', 'dexterity', 'stamina'],
                'social': ['charisma', 'manipulation', 'appearance'],
                'mental': ['perception', 'intelligence', 'wits'],
            }
            distribution_targets = [6, 8, 10]  # Totals for tertiary, secondary, primary
            distribution_min = 1
            distribution_max = 5

            # pool_fields auto-generated from groups

            strength = forms.IntegerField(min_value=1, max_value=5)
            # ...
    """

    distribution_pool_name = "pool"
    distribution_groups = {}
    distribution_targets = []
    distribution_min = 0
    distribution_max = 10

    @property
    def pool_config(self):
        return {
            "mode": "distribution",
            "pool_name": self.distribution_pool_name,
            "groups": self.distribution_groups,
            "targets": self.distribution_targets,
            "min_value": self.distribution_min,
            "max_value": self.distribution_max,
        }

    @property
    def pool_fields(self):
        """Auto-generate pool_fields from distribution_groups."""
        fields = []
        for field_names in self.distribution_groups.values():
            fields.extend(field_names)
        return fields
