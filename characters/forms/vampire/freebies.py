from django import forms

from characters.costs import get_freebie_cost
from characters.forms.core.freebies import CATEGORY_CHOICES, HumanFreebiesForm
from characters.models.vampire.discipline import Discipline

VAMPIRE_CATEGORY_CHOICES = CATEGORY_CHOICES + [
    ("Discipline", "Discipline"),
    ("Virtue", "Virtue"),
    ("Humanity", "Humanity"),
    ("Path Rating", "Path Rating"),
]


class VampireFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=VAMPIRE_CATEGORY_CHOICES)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter out categories that can't be afforded
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]

        if self.is_bound:
            if self.data["category"] == "Discipline":
                self.fields["example"].queryset = Discipline.objects.all()

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


class GhoulFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES + [("Discipline", "Discipline")])

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter out categories that can't be afforded
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]

        if self.is_bound:
            if self.data["category"] == "Discipline":
                self.fields["example"].queryset = Discipline.objects.all()

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
