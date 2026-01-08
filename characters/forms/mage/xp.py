from characters.forms.core.xp import CATEGORY_CHOICES, XPForm
from characters.models.mage.focus import Practice, SpecializedPractice, Tenet
from characters.models.mage.mage import PracticeRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from core.widgets import AutocompleteTextInput
from django import forms

MAGE_CATEGORY_CHOICES = CATEGORY_CHOICES + [
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
    resonance = forms.CharField(required=False, widget=AutocompleteTextInput(suggestions=[]))

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        self.fields["resonance"].widget.suggestions = suggestions

        # Add mage-specific categories to the choices
        category_choices = list(MAGE_CATEGORY_CHOICES)

        # Filter out invalid base categories (already done in parent)
        if not self.image_valid():
            category_choices = [x for x in category_choices if x[0] != "Image"]
        if not self.attribute_valid():
            category_choices = [x for x in category_choices if x[0] != "Attribute"]
        if not self.ability_valid():
            category_choices = [x for x in category_choices if x[0] != "Ability"]
        if not self.background_valid():
            category_choices = [x for x in category_choices if x[0] != "Background"]
        if not self.willpower_valid():
            category_choices = [x for x in category_choices if x[0] != "Willpower"]
        if not self.mf_valid():
            category_choices = [x for x in category_choices if x[0] != "MeritFlaw"]

        # Filter mage-specific categories
        if not self.spheres_valid():
            category_choices = [x for x in category_choices if x[0] != "Sphere"]
        if not self.rote_points_valid():
            category_choices = [x for x in category_choices if x[0] != "Rote Points"]
        if not self.resonance_valid():
            category_choices = [x for x in category_choices if x[0] != "Resonance"]
        if not self.add_tenet_valid():
            category_choices = [x for x in category_choices if x[0] != "Tenet"]
        if not self.remove_tenet_valid():
            category_choices = [x for x in category_choices if x[0] != "Remove Tenet"]
        if not self.practice_valid():
            category_choices = [x for x in category_choices if x[0] != "Practice"]
        if not self.arete_valid():
            category_choices = [x for x in category_choices if x[0] != "Arete"]
        if not self.rote_valid():
            category_choices = [x for x in category_choices if x[0] != "Rote"]

        self.fields["category"].choices = category_choices

        # Build example choices_map with mage-specific categories
        example_choices_map = self._build_example_choices_map(category_choices)
        self.fields["example"].choices_map = example_choices_map

        # Build value choices_map
        value_choices_map = self._build_value_choices_map(example_choices_map)
        self.fields["value"].choices_map = value_choices_map

        # Re-run chain setup
        self._setup_chains()

    def _build_example_choices_map(self, category_choices):
        """Override to add mage-specific categories."""
        example_choices_map = super()._build_example_choices_map(category_choices)
        char = self.character

        for cat_value, cat_label in category_choices:
            if cat_value == "Sphere":
                examples = [
                    sphere
                    for sphere in Sphere.objects.all()
                    if getattr(char, sphere.property_name) < char.arete
                    and char.xp_cost(
                        char.sphere_to_trait_type(sphere.property_name),
                        getattr(char, sphere.property_name),
                    )
                    <= char.xp
                ]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Tenet":
                examples = Tenet.objects.all()
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Remove Tenet":
                examples = char.other_tenets.all()
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Practice":
                examples = Practice.objects.exclude(
                    polymorphic_ctype__model="specializedpractice"
                ).exclude(polymorphic_ctype__model="corruptedpractice")
                spec = SpecializedPractice.objects.filter(faction=char.faction)
                if spec.exists():
                    examples = examples.exclude(
                        id__in=[x.parent_practice.id for x in spec]
                    ) | Practice.objects.filter(id__in=[x.id for x in spec])
                ids = PracticeRating.objects.filter(mage=char, rating=5).values_list(
                    "practice__id", flat=True
                )
                examples = examples.exclude(pk__in=ids).order_by("name")
                examples = [
                    x
                    for x in examples
                    if char.xp_cost("practice", char.practice_rating(x)) <= char.xp
                ]
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]

        return example_choices_map

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
        if spec.exists():
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
