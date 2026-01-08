from characters.forms.mage.effect import EffectCreateOrSelectForm
from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from django import forms
from locations.models.mage import Chantry
from locations.models.mage.chantry import ChantryBackgroundRating
from widgets import (
    ChainedChoiceField,
    ChainedSelectMixin,
    ConditionalFieldsMixin,
    CreateOrSelectField,
    CreateOrSelectMixin,
)


class ChantryPointForm(ChainedSelectMixin, ConditionalFieldsMixin, forms.Form):
    INTEGRATED_EFFECTS_NUMBERS = {
        0: 0,
        1: 4,
        2: 8,
        3: 15,
        4: 20,
        5: 25,
        6: 35,
        7: 45,
        8: 55,
        9: 70,
        10: 90,
    }

    category = ChainedChoiceField(choices=[])
    example = ChainedChoiceField(parent_field="category", choices_map={}, required=False)
    note = forms.CharField(max_length=300, required=False)
    display_alt_name = forms.BooleanField(required=False)

    # Conditional field visibility rules
    conditional_fields = {
        "category": {
            "example": {"exclude": ["-----", "Integrated Effects"]},
            "note": {"values": ["New Background"]},
            "display_alt_name": {"values": ["New Background"]},
        }
    }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        self.object = Chantry.objects.get(pk=pk)
        super().__init__(*args, **kwargs)

        # Build category choices
        category_choices = [
            ("-----", "-----"),
            ("Integrated Effects", "Integrated Effects"),
            ("New Background", "New Background"),
            ("Existing Background", "Existing Background"),
        ]

        if not self.object.backgrounds.exists():
            category_choices = [
                ("-----", "-----"),
                ("Integrated Effects", "Integrated Effects"),
                ("New Background", "New Background"),
            ]

        if self.object.integrated_effects_score == 10:
            category_choices = [x for x in category_choices if x[0] != "Integrated Effects"]

        self.fields["category"].choices = category_choices

        # Build example choices_map based on category
        example_choices_map = {}
        for cat_value, cat_label in category_choices:
            if cat_value == "New Background":
                examples = Background.objects.all().order_by("name")
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            elif cat_value == "Existing Background":
                examples = self.object.backgrounds.all()
                example_choices_map[cat_value] = [(str(x.pk), str(x)) for x in examples]
            else:
                example_choices_map[cat_value] = []

        self.fields["example"].choices_map = example_choices_map

        # Re-run chain setup after choices configured
        self._setup_chains()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        example = cleaned_data.get("example")

        if category == "New Background" and not example:
            raise forms.ValidationError("Need to choose a Background")
        if category == "Existing Background" and not example:
            raise forms.ValidationError("Need to choose a Background")

        return cleaned_data

    def save(self, commit=True):
        category = self.cleaned_data["category"]
        example_pk = self.cleaned_data["example"]
        if category == "Integrated Effects":
            self.object.integrated_effects_score += 1
            self.object.save()
        elif "New Background" == category:
            bg = Background.objects.get(pk=example_pk)
            ChantryBackgroundRating.objects.create(
                bg=bg,
                note=self.cleaned_data["note"],
                chantry=self.object,
                display_alt_name=self.cleaned_data["display_alt_name"],
                rating=1,
            )
        elif "Existing Background" == category:
            bg_rating = ChantryBackgroundRating.objects.get(pk=example_pk)
            bg_rating.rating += 1
            bg_rating.save()
        else:
            pass


# Form for choosing effects
class ChantryEffectsForm(EffectCreateOrSelectForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        self.object = Chantry.objects.get(pk=pk)
        super().__init__(*args, **kwargs)
        q = Effect.objects.filter(max_sphere__lte=self.object.rank)
        q = q.exclude(pk__in=self.object.integrated_effects.all())
        q = q.exclude(rote_cost__gt=self.object.current_ie_points())
        self.fields["select"].queryset = q

    def save(self, commit=True):
        effect = super().save(commit=commit)
        self.object.integrated_effects.add(effect)


class ChantryCreateForm(forms.ModelForm):
    total_points = forms.IntegerField(
        min_value=0, error_messages={"min_value": "Total points must be 0 or higher."}
    )

    class Meta:
        model = Chantry
        fields = [
            "name",
            "chronicle",
            "contained_within",
            "description",
            "faction",
            "leadership_type",
            "season",
            "chantry_type",
            "gauntlet",
            "shroud",
            "dimension_barrier",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter name here"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter description here"}),
        }

    def save(self, commit=True):
        chantry = super().save(commit=commit)
        chantry.total_points = int(self.cleaned_data.get("total_points"))
        chantry.save()
        return chantry


class ChantrySelectOrCreateForm(CreateOrSelectMixin, forms.ModelForm):
    """Form for selecting an existing Chantry or creating a new one."""

    create_or_select_config = {
        "toggle_field": "create_new",
        "select_field": "existing_chantry",
        "error_message": "Please select an existing Chantry.",
    }

    create_new = CreateOrSelectField(label="Create a new Chantry?")
    existing_chantry = forms.ModelChoiceField(
        queryset=Chantry.objects.all(),
        required=False,
        label="Select an existing Chantry",
    )
    total_points = forms.IntegerField(
        min_value=0,
        required=False,
        error_messages={"min_value": "Total points must be 0 or higher."},
    )

    class Meta:
        model = Chantry
        fields = [
            "create_new",
            "existing_chantry",
            "name",
            "chronicle",
            "contained_within",
            "description",
            "faction",
            "leadership_type",
            "season",
            "chantry_type",
            "gauntlet",
            "shroud",
            "dimension_barrier",
            "total_points",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter name here"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter description here"}),
        }

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character")
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False

        if self.character is not None:
            self.fields["existing_chantry"].queryset = Chantry.objects.filter(
                chronicle=self.character.chronicle
            )

    def save(self, commit=True):
        if self.is_creating():
            chantry = super().save(commit=commit)
            chantry.total_points = int(self.cleaned_data.get("total_points") or 0)
            chantry.save()
        else:
            chantry = self.cleaned_data.get("existing_chantry")
            chantry.total_points += int(self.cleaned_data.get("total_points") or 0)
            chantry.save()
        return chantry
