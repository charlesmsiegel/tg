"""
Attribute allocation form with point pool validation.

Uses the PointPoolWidget for real-time constraint validation and
eliminates the need for custom JavaScript in the template.
"""

from django import forms
from widgets import DistributionPoolMixin


class AttributeForm(DistributionPoolMixin, forms.Form):
    """
    Form for allocating attribute points during character creation.

    Validates that points are distributed across physical/social/mental
    categories according to primary/secondary/tertiary allocation rules.

    Usage:
        # In view, calculate targets based on primary/secondary/tertiary values
        class MyAttributeView(UpdateView):
            def get_form_class(self):
                return AttributeForm.with_targets(
                    primary=7, secondary=5, tertiary=3  # Dots to distribute
                )
    """

    # Distribution configuration
    distribution_pool_name = "attributes"
    distribution_groups = {
        "physical": ["strength", "dexterity", "stamina"],
        "social": ["charisma", "manipulation", "appearance"],
        "mental": ["perception", "intelligence", "wits"],
    }
    # Default targets (base 3 per category + allocated dots)
    distribution_targets = [6, 8, 10]  # tertiary=3+3, secondary=3+5, primary=3+7
    distribution_min = 1
    distribution_max = 5

    # Physical attributes
    strength = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    dexterity = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    stamina = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    # Social attributes
    charisma = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    manipulation = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    appearance = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    # Mental attributes
    perception = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    intelligence = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    wits = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    @classmethod
    def with_targets(cls, primary=7, secondary=5, tertiary=3):
        """
        Create a form class with custom primary/secondary/tertiary targets.

        Args:
            primary: Dots to add to primary category (default 7)
            secondary: Dots to add to secondary category (default 5)
            tertiary: Dots to add to tertiary category (default 3)

        Returns:
            A new form class with the specified distribution targets.
        """
        base = 3  # Each category starts with 3 (1 dot per attribute)
        targets = sorted([base + tertiary, base + secondary, base + primary])

        class DynamicAttributeForm(cls):
            distribution_targets = targets

        return DynamicAttributeForm


class HumanAttributeForm(AttributeForm):
    """
    Attribute form for Human character creation.

    Uses the standard 7/5/3 distribution for primary/secondary/tertiary.
    """

    distribution_targets = [6, 8, 10]  # base 3 + 3/5/7
