from django import forms
from django.core.exceptions import ValidationError

from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from core.permissions import PermissionManager
from game.models import Chronicle
from widgets import ChainedChoiceField, ChainedModelChoiceField, ChainedSelectMixin


def get_child_factions(parent_id):
    """Get child factions for a given parent faction ID."""
    if not parent_id:
        return []
    return list(
        MageFaction.objects.filter(parent_id=parent_id).order_by("name").values_list("id", "name")
    )


class MageCreationForm(ChainedSelectMixin, forms.ModelForm):
    affiliation = ChainedModelChoiceField(
        queryset=MageFaction.objects.none(),
        empty_label="Select affiliation...",
    )

    # Override faction and subfaction with ChainedChoiceField (excluded from Meta.fields)
    faction = ChainedChoiceField(
        parent_field="affiliation",
        choices_callback=get_child_factions,
        empty_label="Select faction...",
        required=False,
    )
    subfaction = ChainedChoiceField(
        parent_field="faction",
        choices_callback=get_child_factions,
        empty_label="Select subfaction...",
        required=False,
    )

    class Meta:
        model = Mage
        # Note: faction and subfaction are handled manually via ChainedChoiceField
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "affiliation",
            "essence",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["affiliation"].queryset = MageFaction.objects.filter(parent=None)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["image"].required = False
        if self.user is not None:
            chronicle_id = (
                self.data.get("chronicle") if self.is_bound else self.initial.get("chronicle")
            )
            chronicle = None
            if chronicle_id is not None:
                value = str(getattr(chronicle_id, "pk", chronicle_id))
                if value.isascii() and value.isdecimal() and len(value) <= 20:
                    chronicle = Chronicle.objects.filter(pk=int(value)).first()
            if not PermissionManager.can_manage_scope(self.user, chronicle, "mta"):
                self.fields["affiliation"].queryset = self.fields["affiliation"].queryset.exclude(
                    name__in=["Nephandi", "Marauders"]
                )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # If we have a user
            instance.owner = self.user

        # Convert faction/subfaction IDs to model instances
        faction_id = self.cleaned_data.get("faction")
        if faction_id:
            instance.faction = MageFaction.objects.get(pk=faction_id)
        else:
            instance.faction = None

        subfaction_id = self.cleaned_data.get("subfaction")
        if subfaction_id:
            instance.subfaction = MageFaction.objects.get(pk=subfaction_id)
        else:
            instance.subfaction = None

        if commit:
            instance.save()
        return instance


class MageSpheresForm(forms.ModelForm):
    """Form for selecting Spheres and Arete during character creation."""

    class Meta:
        model = Mage
        fields = [
            "arete",
            "correspondence",
            "time",
            "spirit",
            "forces",
            "matter",
            "life",
            "entropy",
            "mind",
            "prime",
            "affinity_sphere",
            "corr_name",
            "prime_name",
            "spirit_name",
        ]

    # Resonance is typed free text resolved by Mage.add_resonance, not a pick
    # from the model's through-table M2M.
    resonance = forms.CharField(max_length=100)

    def clean_affinity_sphere(self):
        """Validate that an affinity sphere is selected."""
        affinity_sphere = self.cleaned_data.get("affinity_sphere")
        if affinity_sphere is None:
            raise ValidationError("You must select a valid affinity sphere.")
        return affinity_sphere

    def clean_arete(self):
        """Validate that Arete doesn't exceed 3 at character creation."""
        arete = self.cleaned_data.get("arete", 1)
        if arete > 3:
            raise ValidationError("Arete may not exceed 3 at character creation.")
        return arete

    def clean(self):
        """Validate sphere ratings and distribution."""
        cleaned_data = super().clean()

        # Get all sphere values
        arete = cleaned_data.get("arete", 1)
        correspondence = cleaned_data.get("correspondence", 0)
        time = cleaned_data.get("time", 0)
        spirit = cleaned_data.get("spirit", 0)
        forces = cleaned_data.get("forces", 0)
        matter = cleaned_data.get("matter", 0)
        life = cleaned_data.get("life", 0)
        entropy = cleaned_data.get("entropy", 0)
        mind = cleaned_data.get("mind", 0)
        prime = cleaned_data.get("prime", 0)
        affinity_sphere = cleaned_data.get("affinity_sphere")

        # Check individual sphere ratings
        spheres = [
            correspondence,
            time,
            spirit,
            forces,
            matter,
            life,
            entropy,
            mind,
            prime,
        ]
        for sphere_value in spheres:
            if sphere_value < 0 or sphere_value > arete:
                raise ValidationError("Spheres must range from 0-Arete Rating.")

        # Check that affinity sphere is nonzero
        if affinity_sphere and self.instance:
            affinity_value = getattr(self.instance, affinity_sphere.property_name, None)
            # Check in cleaned_data first (in case it's being set now)
            if affinity_value == 0 and cleaned_data.get(affinity_sphere.property_name, 0) == 0:
                raise ValidationError("Affinity Sphere must be nonzero.")

        # Check total sphere points
        total_spheres = sum(spheres)
        if total_spheres != 6:
            raise ValidationError(f"Spheres must total 6 (currently {total_spheres}).")

        return cleaned_data


TENET_LABELS = (
    ("metaphysical_tenet", "Metaphysical"),
    ("personal_tenet", "Personal"),
    ("ascension_tenet", "Ascension"),
)
PRACTICE_TOTAL_ERROR = "Starting Practices must add up to Arete rating"
PRACTICE_ABILITY_ERROR = (
    "You must have at least 2 dots in associated abilities for each dot of a Practice"
)


def starting_practice_error(mage, rows):
    """The first Focus-step practice rule ``rows`` break, or None.

    ``rows`` are (practice, rating) pairs, either possibly None. Ratings sum
    to Arete, and each practice dot needs two dots among its abilities.
    """
    if sum(rating for _, rating in rows if rating is not None) != mage.arete:
        return PRACTICE_TOTAL_ERROR
    for practice, rating in rows:
        if practice is None:
            continue
        ability_total = sum(
            getattr(mage, ability.property_name, 0) for ability in practice.abilities.all()
        )
        if rating is None or rating > ability_total / 2:
            return PRACTICE_ABILITY_ERROR
    return None


class MageFocusForm(forms.ModelForm):
    """Tenets, validated together with the starting-practice formset."""

    class Meta:
        model = Mage
        fields = ["metaphysical_tenet", "personal_tenet", "ascension_tenet", "other_tenets"]

    def __init__(self, *args, practice_formset=None, **kwargs):
        self.practice_formset = practice_formset
        super().__init__(*args, **kwargs)

    def practice_rows(self):
        return [
            (form.cleaned_data.get("practice"), form.cleaned_data.get("rating"))
            for form in self.practice_formset
        ]

    def clean(self):
        cleaned_data = super().clean()
        for field, label in TENET_LABELS:
            if cleaned_data.get(field) is None:
                raise ValidationError(f"Must include {label} Tenet")
        if self.practice_formset is not None and self.practice_formset.is_valid():
            error = starting_practice_error(self.instance, self.practice_rows())
            if error:
                raise ValidationError(error)
        return cleaned_data
