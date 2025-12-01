from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background
from characters.models.core.merit_flaw_block import MeritFlaw
from core.models import Number
from django import forms

CATEGORY_CHOICES = [
    ("-----", "-----"),
    ("Attribute", "Attribute"),
    ("Ability", "Ability"),
    ("New Background", "New Background"),
    ("Existing Background", "Existing Background"),
    ("Willpower", "Willpower"),
    ("MeritFlaw", "MeritFlaw"),
]


class HumanFreebiesForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    example = forms.ModelChoiceField(queryset=Attribute.objects.none(), required=False)
    value = forms.ChoiceField(choices=[], required=False)
    note = forms.CharField(max_length=300, required=False)
    pooled = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)
        CATEGORY_CHOICES = [
            ("-----", "-----"),
            ("Attribute", "Attribute"),
            ("Ability", "Ability"),
            ("New Background", "New Background"),
            ("Existing Background", "Existing Background"),
            ("Willpower", "Willpower"),
            ("MeritFlaw", "MeritFlaw"),
        ]
        if self.instance.freebies < 5:
            CATEGORY_CHOICES = [x for x in CATEGORY_CHOICES if x[0] != "Attribute"]
        if self.instance.freebies < 2:
            CATEGORY_CHOICES = [x for x in CATEGORY_CHOICES if x[0] != "Ability"]
        self.fields["category"].choices = CATEGORY_CHOICES
        self.fields["category"].choices = [
            x for x in self.fields["category"].choices if self.validator(x[0])
        ]
        if self.is_bound:
            if self.data["category"] == "Attribute":
                self.fields["example"].queryset = Attribute.objects.all()
            if self.data["category"] == "Ability":
                self.fields["example"].queryset = Ability.objects.all()
            if self.data["category"] == "New Background":
                self.fields["example"].queryset = Background.objects.all()
            if self.data["category"] == "Existing Background":
                self.fields["example"].queryset = self.instance.backgrounds.all()
            if self.data["category"] == "MeritFlaw":
                self.fields["example"].queryset = MeritFlaw.objects.all()
                self.fields["value"].choices = [(x, x) for x in range(-100, 101)]

    def validator(self, trait_type):
        trait_type = trait_type.lower().split(" ")[-1]
        if not isinstance(self.instance.freebie_cost(trait_type), int):
            return True
        if self.instance.freebie_cost(trait_type) == 10000:
            return True
        if self.instance.freebie_cost(trait_type) <= self.instance.freebies:
            return True
        return False

    def clean(self):
        cleaned_data = super().clean()
        category = self.data.get("category")
        if category == "-----":
            raise forms.ValidationError("Must Choose Freebie Expenditure Type")
        elif category == "MeritFlaw" and (self.data["example"] == "" or self.data["value"] == ""):
            raise forms.ValidationError("Must Choose Merit/Flaw and rating")
        elif (
            category
            in [
                "Attribute",
                "Ability",
                "New Background",
                "Existing Background",
                "Sphere",
                "Tenet",
                "Practice",
            ]
            and self.data["example"] == ""
        ):
            raise forms.ValidationError("Must Choose Trait")
        elif category == "Resonance" and self.data["resonance"] == "":
            raise forms.ValidationError("Must Choose Resonance")
        return cleaned_data
