from django import forms

from characters.forms.constants import BASE_CATEGORY_CHOICES
from characters.forms.core.freebies import HumanFreebiesForm
from characters.models.demon.lore import Lore

DTFHUMAN_CATEGORY_CHOICES = BASE_CATEGORY_CHOICES

THRALL_CATEGORY_CHOICES = BASE_CATEGORY_CHOICES + [
    ("Faith Potential", "Faith Potential"),
    ("Virtue", "Virtue"),
]

DEMON_CATEGORY_CHOICES = BASE_CATEGORY_CHOICES + [
    ("Lore", "Lore"),
    ("Faith", "Faith"),
    ("Virtue", "Virtue"),
    ("Temporary Faith", "Temporary Faith"),
]


class DtFHumanFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=DTFHUMAN_CATEGORY_CHOICES)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter out categories that can't be afforded
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]


class ThrallFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=THRALL_CATEGORY_CHOICES)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter out categories that can't be afforded
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]


class DemonFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=DEMON_CATEGORY_CHOICES)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter out categories that can't be afforded
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]

        if self.is_bound:
            if self.data["category"] == "Lore":
                self.fields["example"].queryset = Lore.objects.all()
