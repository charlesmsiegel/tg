"""
Ability allocation form with point pool validation.

Uses the PointPoolWidget for real-time constraint validation and
distribution mode for talents/skills/knowledges categories.
"""

from django import forms

from core.constants import AbilityFields
from widgets import DistributionPoolMixin


class AbilityForm(DistributionPoolMixin, forms.Form):
    """
    Form for allocating ability points during character creation.

    Validates that points are distributed across talents/skills/knowledges
    categories according to primary/secondary/tertiary allocation rules.

    Default distribution: 11/7/4 (can be customized via with_targets)

    Usage:
        # Use default 11/7/4 distribution
        form = AbilityForm(data=request.POST)

        # Or customize targets
        CustomForm = AbilityForm.with_targets(primary=13, secondary=9, tertiary=5)
        form = CustomForm(data=request.POST)
    """

    # Distribution configuration
    distribution_pool_name = "abilities"
    distribution_groups = {
        "talents": AbilityFields.TALENTS,
        "skills": AbilityFields.SKILLS,
        "knowledges": AbilityFields.KNOWLEDGES,
    }
    # Default: 11/7/4 distribution
    distribution_targets = [4, 7, 11]
    distribution_min = 0
    distribution_max = 3  # Max 3 at character creation

    # Talents
    alertness = forms.IntegerField(min_value=0, max_value=3, initial=0)
    athletics = forms.IntegerField(min_value=0, max_value=3, initial=0)
    brawl = forms.IntegerField(min_value=0, max_value=3, initial=0)
    empathy = forms.IntegerField(min_value=0, max_value=3, initial=0)
    expression = forms.IntegerField(min_value=0, max_value=3, initial=0)
    intimidation = forms.IntegerField(min_value=0, max_value=3, initial=0)
    streetwise = forms.IntegerField(min_value=0, max_value=3, initial=0)
    subterfuge = forms.IntegerField(min_value=0, max_value=3, initial=0)

    # Skills
    crafts = forms.IntegerField(min_value=0, max_value=3, initial=0)
    drive = forms.IntegerField(min_value=0, max_value=3, initial=0)
    etiquette = forms.IntegerField(min_value=0, max_value=3, initial=0)
    firearms = forms.IntegerField(min_value=0, max_value=3, initial=0)
    melee = forms.IntegerField(min_value=0, max_value=3, initial=0)
    stealth = forms.IntegerField(min_value=0, max_value=3, initial=0)

    # Knowledges
    academics = forms.IntegerField(min_value=0, max_value=3, initial=0)
    computer = forms.IntegerField(min_value=0, max_value=3, initial=0)
    investigation = forms.IntegerField(min_value=0, max_value=3, initial=0)
    medicine = forms.IntegerField(min_value=0, max_value=3, initial=0)
    science = forms.IntegerField(min_value=0, max_value=3, initial=0)

    @classmethod
    def with_targets(cls, primary=11, secondary=7, tertiary=4):
        """
        Create a form class with custom primary/secondary/tertiary targets.

        Args:
            primary: Points for primary category (default 11)
            secondary: Points for secondary category (default 7)
            tertiary: Points for tertiary category (default 4)

        Returns:
            A new form class with the specified distribution targets.
        """
        targets = sorted([tertiary, secondary, primary])

        class DynamicAbilityForm(cls):
            distribution_targets = targets

        return DynamicAbilityForm


class HumanAbilityForm(AbilityForm):
    """
    Ability form for Human character creation.

    Uses the standard 11/7/4 distribution for primary/secondary/tertiary.
    """

    distribution_targets = [4, 7, 11]
