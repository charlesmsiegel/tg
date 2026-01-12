from django import forms

from characters.forms.constants import BASE_CATEGORY_CHOICES
from characters.forms.core.freebies import HumanFreebiesForm
from characters.models.vampire.discipline import Discipline

VAMPIRE_CATEGORY_CHOICES = BASE_CATEGORY_CHOICES + [
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


class GhoulFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=BASE_CATEGORY_CHOICES + [("Discipline", "Discipline")])

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter out categories that can't be afforded
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]

        if self.is_bound:
            if self.data["category"] == "Discipline":
                self.fields["example"].queryset = Discipline.objects.all()
