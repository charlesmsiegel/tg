"""Choosing a Demon's Apocalyptic Form during character creation."""

from django import forms

from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from characters.rules.limits import (
    APOCALYPTIC_FORM_POINT_BUDGET,
    APOCALYPTIC_FORM_TRAITS_PER_STATE,
)


class ApocalypticFormSelectionForm(forms.Form):
    """Four low- and four high-Torment traits, within budget and disjoint.

    Low-Torment choices exclude high-Torment-only traits. The selected trait
    objects are available as ``low_traits`` and ``high_traits`` once valid.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.traits = {trait.id: trait for trait in ApocalypticFormTrait.objects.all()}
        for state, traits in (
            ("low", [t for t in self.traits.values() if not t.high_torment_only]),
            ("high", list(self.traits.values())),
        ):
            for trait in traits:
                self.fields[f"{state}_trait_{trait.id}"] = forms.BooleanField(
                    required=False,
                    label=f"{trait.name} ({trait.cost} points)",
                    help_text=trait.description,
                )

    def selected(self, state):
        prefix = f"{state}_trait_"
        return [
            self.traits[int(name[len(prefix) :])]
            for name, value in self.cleaned_data.items()
            if value and name.startswith(prefix)
        ]

    def clean(self):
        cleaned_data = super().clean()
        self.low_traits = self.selected("low")
        self.high_traits = self.selected("high")
        for state, chosen in (("low", self.low_traits), ("high", self.high_traits)):
            if len(chosen) != APOCALYPTIC_FORM_TRAITS_PER_STATE:
                raise forms.ValidationError(
                    f"You must select exactly {APOCALYPTIC_FORM_TRAITS_PER_STATE} {state} "
                    f"torment traits. Currently: {len(chosen)}"
                )
        total_cost = sum(trait.cost for trait in self.low_traits + self.high_traits)
        if total_cost > APOCALYPTIC_FORM_POINT_BUDGET:
            raise forms.ValidationError(
                f"Point budget exceeded. Maximum is {APOCALYPTIC_FORM_POINT_BUDGET} points. "
                f"Currently: {total_cost}"
            )
        if {t.id for t in self.low_traits} & {t.id for t in self.high_traits}:
            raise forms.ValidationError("A trait cannot be selected as both low and high torment.")
        return cleaned_data
