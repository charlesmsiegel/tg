from django import forms
from django.db import transaction
from django.db.models import Q

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

    IE = "Integrated Effects"
    NEW = "New Background"
    EXISTING = "Existing Background"

    category = ChainedChoiceField(choices=[])
    example = ChainedChoiceField(parent_field="category", choices_map={}, required=False)
    note = forms.CharField(max_length=300, required=False)
    display_alt_name = forms.BooleanField(required=False)

    # Conditional field visibility rules (widgets.ConditionalFieldsMixin format)
    conditional_fields = {
        "example": {"visible_when": {"category": {"value_in": [NEW, EXISTING]}}},
        "note": {"visible_when": {"category": {"value_is": NEW}}},
        "display_alt_name": {"visible_when": {"category": {"value_is": NEW}}},
    }

    def __init__(self, *args, chantry, **kwargs):
        # The view already resolved (and 404ed on) the chantry; reuse its
        # instance instead of refetching a row that may vanish in between.
        self.object = chantry
        super().__init__(*args, **kwargs)

        # Only options the points service says are allowed and affordable.
        new, existing = chantry_points.affordable_backgrounds(self.object)
        category_choices = [("-----", "-----")]
        if chantry_points.can_buy_ie(self.object):
            category_choices.append((self.IE, self.IE))
        if new:
            category_choices.append((self.NEW, self.NEW))
        if existing:
            category_choices.append((self.EXISTING, self.EXISTING))
        self.fields["category"].choices = category_choices

        example_choices_map = {value: [] for value, _ in category_choices}
        example_choices_map[self.NEW] = [(str(bg.pk), str(bg)) for bg in new]
        example_choices_map[self.EXISTING] = [(str(r.pk), str(r)) for r in existing]
        self.fields["example"].choices_map = example_choices_map

        # Re-run chain setup after choices configured
        self._setup_chains()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        example = str(cleaned_data.get("example") or "")
        self.background = None

        if category == self.IE:
            error = chantry_points.ie_purchase_error(self.object)
        elif category in (self.NEW, self.EXISTING):
            if not example:
                raise forms.ValidationError("Need to choose a Background")
            if not example.isdigit():
                raise forms.ValidationError("Choose a valid Background.")
            if category == self.NEW:
                self.background = Background.objects.filter(pk=example).first()
                current = None
            else:
                rating = self.object.backgrounds.select_related("bg").filter(pk=example).first()
                self.background = rating.bg if rating is not None else None
                current = rating.rating if rating is not None else None
            if self.background is None:
                raise forms.ValidationError("Choose a valid Background.")
            error = chantry_points.background_purchase_error(
                self.object, self.background, current_rating=current
            )
        else:
            error = None
        if error:
            raise forms.ValidationError(error)
        return cleaned_data

    def save(self, commit=True):
        """Spend the points through the service.

        Returns the new Integrated Effects score, the bought
        ``ChantryBackgroundRating``, or None for "-----". Raises
        ``ValidationError`` if a concurrent purchase used the points first.
        """
        category = self.cleaned_data["category"]
        if category == self.IE:
            return chantry_points.buy_ie_dot(self.object)
        if category == self.NEW:
            return chantry_points.buy_background_dot(
                self.object,
                self.background,
                note=self.cleaned_data["note"],
                display_alt_name=self.cleaned_data["display_alt_name"],
            )
        if category == self.EXISTING:
            return chantry_points.buy_background_dot(self.object, self.background)
        return None


class ChantryRemoveForm(forms.Form):
    """Undo one purchase: a background dot, an Integrated Effects dot or an effect.

    POST ``action=remove`` plus exactly one of ``rating=<ChantryBackgroundRating
    pk>``, ``ie=on`` or ``effect=<Effect pk>``.
    """

    ACTION = "remove"

    rating = forms.ModelChoiceField(
        queryset=ChantryBackgroundRating.objects.none(),
        required=False,
        widget=forms.HiddenInput,
    )
    ie = forms.BooleanField(required=False, widget=forms.HiddenInput)
    effect = forms.ModelChoiceField(
        queryset=Effect.objects.none(), required=False, widget=forms.HiddenInput
    )

    def __init__(self, *args, chantry, **kwargs):
        self.chantry = chantry
        super().__init__(*args, **kwargs)
        self.fields["rating"].queryset = chantry.backgrounds.select_related("bg")
        self.fields["effect"].queryset = chantry.integrated_effects.all()

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        chosen = [name for name in ("rating", "ie", "effect") if cleaned_data.get(name)]
        if len(chosen) != 1:
            raise forms.ValidationError("Choose exactly one thing to remove.")
        if chosen == ["rating"]:
            error = chantry_points.background_removal_error(cleaned_data["rating"])
        elif chosen == ["ie"]:
            error = chantry_points.ie_removal_error(self.chantry)
        else:
            error = None
        if error:
            raise forms.ValidationError(error)
        return cleaned_data

    def save(self):
        """Apply the removal through the service; may raise ``ValidationError``."""
        if self.cleaned_data.get("rating"):
            return chantry_points.remove_background_dot(self.cleaned_data["rating"])
        if self.cleaned_data.get("ie"):
            return chantry_points.remove_ie_dot(self.chantry)
        return chantry_points.remove_effect(self.chantry, self.cleaned_data["effect"])


# Form for choosing effects
class ChantryEffectsForm(EffectCreateOrSelectForm):
    def __init__(self, *args, chantry, **kwargs):
        self.object = chantry
        super().__init__(*args, **kwargs)
        q = Effect.objects.filter(max_sphere__lte=self.object.rank)
        q = q.exclude(pk__in=self.object.integrated_effects.all())
        q = q.exclude(rote_cost__gt=self.object.current_ie_points())
        self.fields["select"].queryset = q

    def save(self, commit=True):
        effect = super().save(commit=commit)
        self.object.integrated_effects.add(effect)


class ChantryFundingMixin:
    """Route a chantry ModelForm's ``total_points`` through the points service.

    ``clean_total_points`` asks ``funding_error`` when the submitted total differs
    from the stored one, for a field error: never negative and, on a saved chantry,
    never below what is already spent. On a saved chantry ``save(commit=True)``
    writes the other fields with ``update_fields`` (never ``total_points``) and
    then, only when the total differs, writes it with ``set_total_points``, which
    locks the row and re-checks, all in one transaction. So a storyteller edit
    cannot race a player's purchase into a negative balance, and a submission that
    matches the stored total neither re-validates old state nor touches the row.
    The submitted total is absolute, though: a join that landed between the page
    load and the save is replaced by it, as with any edit-the-total form. A new
    chantry has spent nothing, so its INSERT carries the validated total.
    ``save()`` may raise ``ValidationError``; with ``commit=False`` the caller
    funds the chantry itself.
    """

    def clean_total_points(self):
        total = self.cleaned_data["total_points"]
        if "total_points" not in self.changed_data:
            return total
        error = chantry_points.funding_error(self.instance, total)
        if error:
            raise forms.ValidationError(error)
        return total

    def save(self, commit=True):
        if self.instance.pk is None or not commit:
            return super().save(commit)
        with transaction.atomic():
            chantry = super().save(commit=False)
            fields = [
                field.name
                for field in chantry._meta.concrete_fields
                if field.name in self.fields and field.name != "total_points"
            ]
            if fields:
                chantry.save(update_fields=fields)
            self.save_m2m()
            if "total_points" in self.changed_data:
                chantry_points.set_total_points(chantry, self.cleaned_data["total_points"])
            else:
                chantry.refresh_from_db(fields=["total_points"])
        return chantry


def funded(form_class):
    """``form_class`` with ``ChantryFundingMixin`` in front, for registry-built forms."""
    return type(f"Funded{form_class.__name__}", (ChantryFundingMixin, form_class), {})


class ChantryCreateForm(ChantryFundingMixin, forms.ModelForm):
    total_points = forms.IntegerField(
        min_value=0, error_messages={"min_value": "Total points must be 0 or higher."}
    )

    class Meta:
        model = Chantry
        fields = ["name", "chronicle", *_CHANTRY_DETAIL_FIELDS]
        widgets = _CHANTRY_WIDGETS

    def save(self, commit=True):
        # ``total_points`` is a declared field here, not a Meta field, so the
        # ModelForm never copies it onto the instance; and ChantryFundingMixin
        # leaves an unsaved chantry to its caller. Fund it through the service.
        chantry = super().save(commit=False)
        chantry_points.set_total_points(chantry, self.cleaned_data["total_points"])
        if commit:
            chantry.save()
            self.save_m2m()
        return chantry


def joinable_chantries(character):
    """Chantries the character's Chantry background may pool its points into.

    Joining only adds points, and points can only be spent while the chantry is
    still in its wizard, so only unfinished (``Un``) or returned (``Rev``)
    chantries qualify. Pooling into another player's chantry would raise its rank
    behind their back, so the chantry must be owned by the character's player or
    already count the character among its members. It must also share the
    character's chronicle (or, for a chronicle-less character, have none).
    """
    who = Q(members=character)
    if character.owner_id is not None:
        who |= Q(owner_id=character.owner_id)
    queryset = Chantry.objects.filter(who, status__in=chantry_points.OPEN_STATUSES)
    if character.chronicle_id is None:
        queryset = queryset.filter(chronicle__isnull=True)
    else:
        queryset = queryset.filter(chronicle_id=character.chronicle_id)
    return queryset.distinct()


class ChantrySelectOrCreateForm(CreateOrSelectMixin, forms.ModelForm):
    """Create a chantry for a character's Chantry background, or join one.

    ``points`` is the character's Chantry background rating. A new chantry is
    owned by the character's player, starts unfinished in the chantry wizard and
    is funded with exactly those points. Joining only adds the points to one of
    ``joinable_chantries(character)``; the chosen chantry's owner, chronicle and
    status are never touched. Both paths fund the chantry through
    ``locations.services.chantry_points``.
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
        self.fields["existing_chantry"].queryset = joinable_chantries(character)

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
                chantry_points.set_total_points(chantry, self.points)
                chantry.save()
                self.save_m2m()
                chantry_points.apply_type_grants(chantry)
                return chantry
            chantry = self.cleaned_data["existing_chantry"]
            chantry_points.add_points(chantry, self.points)
            return chantry
