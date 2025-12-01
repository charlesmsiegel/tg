from characters.forms.core.freebies import CATEGORY_CHOICES, HumanFreebiesForm
from characters.models.core.ability_block import Ability
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from core.widgets import AutocompleteTextInput
from django import forms

CATEGORY_CHOICES = CATEGORY_CHOICES + [
    ("Sphere", "Sphere"),
    ("Rotes", "Rotes"),
    ("Resonance", "Resonance"),
    ("Tenet", "Tenet"),
    ("Practice", "Practice"),
    ("Arete", "Arete"),
    ("Quintessence", "Quintessence"),
]


class CompanionFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        ADDITIONAL_CATS = [("Advantage", "Advantage")]
        if self.instance.companion_type == "familiar":
            ADDITIONAL_CATS.append(("Charms", "Charms"))
        self.fields["category"].choices += ADDITIONAL_CATS
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]

    def save(self, *args, **kwargs):
        return self.instance


class SorcererFreebiesForm(HumanFreebiesForm):
    practice = forms.ModelChoiceField(
        queryset=Practice.objects.exclude(polymorphic_ctype__model="specializedpractice").exclude(
            polymorphic_ctype__model="corruptedpractice"
        ),
        required=False,
    )
    ability = forms.ModelChoiceField(queryset=Ability.objects.all(), required=False)

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        ADDITIONAL_CATS = [("Existing Path", "Existing Path"), ("New Path", "New Path")]
        if self.instance.sorcerer_type == "hedge_mage":
            ADDITIONAL_CATS.append(("Create Ritual", "Create Ritual"))
            ADDITIONAL_CATS.append(("Select Ritual", "Select Ritual"))
        self.fields["category"].choices += ADDITIONAL_CATS
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]
        self.fields["ability"].queryset = Ability.objects.none()

    def validator(self, trait_type):
        trait_type = trait_type.lower().split(" ")[-1]
        if not isinstance(self.instance.freebie_cost(trait_type), int):
            return True
        if self.instance.freebie_cost(trait_type) == 10000:
            return True
        if self.instance.freebie_cost(trait_type) <= self.instance.freebies:
            return True
        return False

    def save(self, *args, **kwargs):
        return self.instance


class MageFreebiesForm(HumanFreebiesForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    resonance = forms.CharField(required=False, widget=AutocompleteTextInput(suggestions=[]))

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        self.fields["resonance"].widget.suggestions = suggestions
        ADDITIONAL_CATS = [
            ("Sphere", "Sphere"),
            ("Rotes", "Rotes"),
            ("Resonance", "Resonance"),
            ("Tenet", "Tenet"),
            ("Practice", "Practice"),
            ("Arete", "Arete"),
            ("Quintessence", "Quintessence"),
        ]
        if (
            self.instance.freebies < 4
            or (self.instance.total_freebies() == 45 and self.instance.arete >= 4)
            or (self.instance.total_freebies() != 45 and self.instance.arete >= 3)
            or (self.instance.other_tenets.count() + 3 == self.instance.arete)
        ):
            ADDITIONAL_CATS = [x for x in ADDITIONAL_CATS if x[0] != "Arete"]
        if self.instance.freebies < 7:
            ADDITIONAL_CATS = [x for x in ADDITIONAL_CATS if x[0] != "Sphere"]
        if self.instance.freebies < 3:
            ADDITIONAL_CATS = [x for x in ADDITIONAL_CATS if x[0] != "Resonance"]
        self.fields["category"].choices += ADDITIONAL_CATS
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]

        if self.is_bound:
            if self.data["category"] == "Sphere":
                self.fields["example"].queryset = Sphere.objects.all()
            if self.data["category"] == "Tenet":
                self.fields["example"].queryset = Tenet.objects.all()
            if self.data["category"] == "Practice" or self.data["category"] == "Arete":
                self.fields["example"].queryset = Practice.objects.all()

    def save(self, *args, **kwargs):
        return self.instance
