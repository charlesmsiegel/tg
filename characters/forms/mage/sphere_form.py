"""
Sphere allocation form with point pool validation.

Uses the PointPoolWidget for real-time constraint validation.
Sphere maximum is dynamically capped at the character's Arete rating.
"""

from django import forms

from widgets import SimplePoolMixin


class SphereForm(SimplePoolMixin, forms.Form):
    """
    Form for allocating sphere points during Mage character creation.

    Validates that:
    - Total sphere points equal 6
    - No sphere exceeds the character's Arete rating
    - All spheres are non-negative

    Usage:
        # In view
        def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['character'] = self.object
            return kwargs
    """

    simple_pool_name = "spheres"
    simple_pool_budget = 6
    simple_pool_min = 0
    simple_pool_max = 5  # Default, overridden by arete

    pool_fields = [
        "correspondence",
        "time",
        "spirit",
        "forces",
        "matter",
        "life",
        "entropy",
        "mind",
        "prime",
    ]

    correspondence = forms.IntegerField(min_value=0, initial=0)
    time = forms.IntegerField(min_value=0, initial=0)
    spirit = forms.IntegerField(min_value=0, initial=0)
    forces = forms.IntegerField(min_value=0, initial=0)
    matter = forms.IntegerField(min_value=0, initial=0)
    life = forms.IntegerField(min_value=0, initial=0)
    entropy = forms.IntegerField(min_value=0, initial=0)
    mind = forms.IntegerField(min_value=0, initial=0)
    prime = forms.IntegerField(min_value=0, initial=0)

    def __init__(self, *args, character=None, arete=None, **kwargs):
        """
        Initialize the form with dynamic max based on character's Arete.

        Args:
            character: Character instance with arete attribute
            arete: Direct arete value (alternative to character)
        """
        # Determine arete value before super().__init__ runs mixin setup
        if character and hasattr(character, "arete"):
            self.simple_pool_max = character.arete
        elif arete is not None:
            self.simple_pool_max = arete
        # else use default (5)

        super().__init__(*args, **kwargs)

        # Update field constraints for Django validation
        max_val = self.simple_pool_max
        for field_name in self.pool_fields:
            self.fields[field_name].max_value = max_val
            self.fields[field_name].widget.attrs["max"] = max_val
