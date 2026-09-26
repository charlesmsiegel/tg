from django import forms
from django.db import transaction
from django.db.models import F

from characters.forms.mage.effect import EffectCreateOrSelectForm
from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from locations.models.mage import Chantry
from locations.models.mage.chantry import ChantryBackgroundRating
from locations.services import chantry_points
from widgets import (
    ChainedChoiceField,
    ChainedSelectMixin,
    ConditionalFieldsMixin,
    CreateOrSelectField,
    CreateOrSelectMixin,
)

# Fields (and widgets) shared by ChantryCreateForm and ChantrySelectOrCreateForm's Meta,
# after each form's own leading fields.
_CHANTRY_DETAIL_FIELDS = [
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
_CHANTRY_WIDGETS = {
    "name": forms.TextInput(attrs={"placeholder": "Enter name here"}),
    "description": forms.Textarea(attrs={"placeholder": "Enter description here"}),
}


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
        fields = ["name", "chronicle", *_CHANTRY_DETAIL_FIELDS]
        widgets = _CHANTRY_WIDGETS

    def save(self, commit=True):
        chantry = super().save(commit=commit)
        chantry.total_points = int(self.cleaned_data.get("total_points"))
        chantry.save()
        return chantry


class ChantrySelectOrCreateForm(CreateOrSelectMixin, forms.ModelForm):
    """Create a chantry for a character's Chantry background, or join one.

    ``points`` is the character's Chantry background rating. A new chantry is
    owned by the character's player, starts unfinished in the chantry wizard and
    is funded with exactly those points. Joining only adds the points; the
    chosen chantry's owner, chronicle and status are never touched.
    """

    create_or_select_config = {
        "toggle_field": "create_new",
        "select_field": "existing_chantry",
        "error_message": "Please select an existing Chantry.",
    }

    create_new = CreateOrSelectField(label="Create a new Chantry?")
    existing_chantry = forms.ModelChoiceField(
        queryset=Chantry.objects.none(),
        required=False,
        label="Select an existing Chantry",
    )

    class Meta:
        model = Chantry
        fields = ["create_new", "existing_chantry", "name", *_CHANTRY_DETAIL_FIELDS]
        widgets = _CHANTRY_WIDGETS

    def __init__(self, *args, character, points=0, **kwargs):
        self.character = character
        self.points = points
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
        if character.chronicle is None:
            # A chronicle-less character may only join their own chronicle-less
            # chantries, not pool points into another player's.
            queryset = Chantry.objects.filter(chronicle__isnull=True, owner=character.owner)
        else:
            queryset = Chantry.objects.filter(chronicle=character.chronicle)
        self.fields["existing_chantry"].queryset = queryset.exclude(status__in=["Ret", "Dec"])

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("create_new") and not (cleaned_data.get("name") or "").strip():
            self.add_error("name", "A new Chantry needs a name.")
        return cleaned_data

    def save(self, commit=True):
        """Create or join the chantry and return it. Always commits."""
        with transaction.atomic():
            if self.is_creating():
                chantry = super().save(commit=False)
                chantry.owner = self.character.owner
                chantry.chronicle = self.character.chronicle
                chantry.status = "Un"
                chantry.creation_status = 1
                chantry.total_points = self.points
                chantry.save()
                self.save_m2m()
                chantry_points.apply_type_grants(chantry)
                return chantry
            pk = self.cleaned_data["existing_chantry"].pk
            # A single atomic UPDATE, not select_for_update() (a no-op on SQLite): two
            # concurrent joins each add their own points instead of racing on a read.
            Chantry.objects.filter(pk=pk).update(total_points=F("total_points") + self.points)
            return Chantry.objects.get(pk=pk)
