from characters.costs import get_freebie_cost
from characters.forms.core.freebies import HumanFreebiesForm
from django import forms


class WraithFreebiesForm(HumanFreebiesForm):
    """Freebie form for Wraith characters with Wraith-specific categories."""

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # No need to add custom category choices here - categories are determined
        # dynamically by get_category_functions() in the view

    def validator(self, trait_type):
        """Check if the character can afford this trait type."""
        trait_type_lower = trait_type.lower().replace(" ", "_")
        cost = get_freebie_cost(trait_type_lower)

        if not isinstance(cost, int):
            return True
        if cost == 10000:  # Blocked category
            return False
        if cost <= self.instance.freebies:
            return True
        return False

    def save(self, *args, **kwargs):
        return self.instance
