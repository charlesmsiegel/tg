from characters.forms.core.xp import CATEGORY_CHOICES, XPForm
from characters.models.mage.focus import Practice, SpecializedPractice, Tenet
from characters.models.mage.mage import PracticeRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from core.widgets import AutocompleteTextInput
from django import forms

CATEGORY_CHOICES = CATEGORY_CHOICES + [
    ("Sphere", "Sphere"),
    ("Rote Points", "Rote Points"),
    ("Resonance", "Resonance"),
    ("Tenet", "Tenet"),
    ("Remove Tenet", "Remove Tenet"),
    ("Practice", "Practice"),
    ("Arete", "Arete"),
    ("Rote", "Rote"),
]


class MageXPForm(XPForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    resonance = forms.CharField(required=False, widget=AutocompleteTextInput(suggestions=[]))

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        self.fields["resonance"].widget.suggestions = suggestions
        if not self.spheres_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Sphere"
            ]
        if not self.rote_points_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Rote Points"
            ]
        if not self.resonance_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Resonance"
            ]
        if not self.add_tenet_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Tenet"
            ]
        if not self.remove_tenet_valid():

            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Remove Tenet"
            ]
        if not self.practice_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Practice"
            ]
        if not self.arete_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Arete"
            ]
        if not self.rote_valid():
            self.fields["category"].choices = [
                x for x in self.fields["category"].choices if x[0] != "Rote"
            ]

        category = self.data.get("category")
        if category == "Sphere":
            self.fields["example"].choices = [
                (sphere.id, sphere.name) for sphere in Sphere.objects.all()
            ]
        elif category == "Tenet":
            self.fields["example"].choices = [
                (tenet.id, tenet.name) for tenet in Tenet.objects.all()
            ]
        elif category == "Remove Tenet":
            self.fields["example"].choices = [
                (tenet.id, tenet.name) for tenet in Tenet.objects.all()
            ]
        elif category == "Practice":
            self.fields["example"].choices = [
                (practice.id, practice.name) for practice in Practice.objects.all()
            ]

    def spheres_valid(self):
        filtered_spheres = [
            sphere
            for sphere in Sphere.objects.all()
            if getattr(self.character, sphere.property_name) < self.character.arete
        ]
        filtered_for_xp_cost = [
            x
            for x in filtered_spheres
            if self.character.xp_cost(
                self.character.sphere_to_trait_type(x.property_name),
                getattr(self.character, x.property_name),
            )
            <= self.character.xp
        ]
        return len(filtered_for_xp_cost) > 0

    def rote_points_valid(self):
        return self.character.xp > 0

    def resonance_valid(self):
        return self.character.xp >= 3

    def add_tenet_valid(self):
        return True

    def remove_tenet_valid(self):
        if self.character.other_tenets.count() + 3 <= self.character.arete:
            return False
        if self.character.other_tenets.count() + 3 > self.character.xp:
            return False
        return True

    def practice_valid(self):
        examples = Practice.objects.exclude(polymorphic_ctype__model="specializedpractice").exclude(
            polymorphic_ctype__model="corruptedpractice"
        )
        spec = SpecializedPractice.objects.filter(faction=self.character.faction)
        if spec.count() > 0:
            examples = examples.exclude(
                id__in=[x.parent_practice.id for x in spec]
            ) | Practice.objects.filter(id__in=[x.id for x in spec])

        ids = PracticeRating.objects.filter(mage=self.character, rating=5).values_list(
            "practice__id", flat=True
        )

        filtered_practices = examples.exclude(pk__in=ids).order_by("name")
        filtered_for_xp_cost = [
            x
            for x in filtered_practices
            if self.character.xp_cost(
                "practice",
                self.character.practice_rating(x),
            )
            <= self.character.xp
        ]
        return len(filtered_for_xp_cost) > 0

    def arete_valid(self):
        return (
            self.character.xp_cost("arete", self.character.arete) <= self.character.xp
            and self.character.arete <= self.character.other_tenets.count() + 3
        )

    def rote_valid(self):
        return self.character.rote_points > 0

    def clean_example(self):
        example = super().clean_example()
        category = self.cleaned_data.get("category")

        if category == "Sphere":
            example = Sphere.objects.get(pk=example)
        if category == "Tenet":
            example = Tenet.objects.get(pk=example)
        if category == "Remove Tenet":
            example = Tenet.objects.get(pk=example)
        if category == "Practice":
            example = Practice.objects.get(pk=example)

        return example
