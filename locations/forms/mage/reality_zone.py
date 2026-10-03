from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

from characters.models.mage.focus import Practice
from core.permissions import PermissionManager
from locations.models.mage.reality_zone import RealityZone, ZoneRating


class RealityZonePracticeRatingForm(forms.ModelForm):
    class Meta:
        model = ZoneRating
        fields = ["practice", "rating"]

    practice = forms.ModelChoiceField(
        queryset=Practice.objects.exclude(polymorphic_ctype__model="specializedpractice").exclude(
            polymorphic_ctype__model="corruptedpractice"
        )
    )
    rating = forms.IntegerField(min_value=-5, max_value=5, initial=0)


class BaseZoneRatingFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = form.save(commit=False)
        obj.zone = self.instance  # Associate with the RealityZone instance
        if commit:
            obj.save()
        return obj


RealityZonePracticeRatingFormSet = inlineformset_factory(
    RealityZone,
    ZoneRating,
    form=RealityZonePracticeRatingForm,
    formset=BaseZoneRatingFormSet,
    extra=1,
    can_delete=True,
)


class RealityZoneFormMixin:
    """Shared balancing and persistence for a place's potentially shared zone."""

    requires_reality_zone_permissions = True

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        zone_id = self.instance.reality_zone_id
        self.can_edit_reality_zone = zone_id is None or (
            request is not None
            and PermissionManager.filter_queryset_for_user(
                request.user, RealityZone.objects.filter(pk=zone_id)
            ).exists()
        )
        if not self.can_edit_reality_zone:
            # Missing actor context must also fail closed for an existing zone.
            # Do not fetch, initialize or bind the shared zone's private rows.
            # Descriptive parent edits can proceed at the parent's current rank.
            self.reality_zone = None
            self.reality_zone_formset = None
            self.fields["rank"].disabled = True
            return
        self.reality_zone = (
            self.instance.reality_zone
            if self.instance.reality_zone_id
            else RealityZone(name="Reality Zone", is_player_zone=True)
        )
        self.reality_zone_formset = RealityZonePracticeRatingFormSet(
            instance=self.reality_zone,
            data=self.data if self.is_bound else None,
            prefix="reality_zone",
        )

    def is_valid(self):
        return super().is_valid() and (
            not self.can_edit_reality_zone or self.reality_zone_formset.is_valid()
        )

    def clean_reality_zone(self, rank):
        if not self.can_edit_reality_zone:
            # The inline formset's prefix is independent of the parent form's.
            prefix = "reality_zone-"
            posted_rank = self.data.get(self.add_prefix("rank"))
            if any(key.startswith(prefix) for key in self.data) or (
                posted_rank is not None and str(posted_rank) != str(self.initial["rank"])
            ):
                raise forms.ValidationError(
                    "Rank and shared reality zone ratings are read-only here; ask staff to edit them."
                )
            return
        if not self.reality_zone_formset.is_valid():
            return
        ratings = [
            form.cleaned_data.get("rating", 0)
            for form in self.reality_zone_formset
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        ]
        if sum(ratings) != 0:
            raise forms.ValidationError("Reality Zone Ratings must total 0")
        if sum(rating for rating in ratings if rating > 0) != rank:
            label = self.instance._meta.verbose_name.title()
            raise forms.ValidationError(f"Positive Reality Zone Ratings must sum to {label} rating")

    def save_reality_zone(self, place):
        if not self.can_edit_reality_zone:
            return
        # Names belong to the zone itself, never to one of its linked places.
        # Existing shared zones retain both their identity and staff-edited name.
        if self.reality_zone.pk is None:
            self.reality_zone.save()
        place.reality_zone = self.reality_zone
        place.save()
        self.reality_zone_formset.instance = self.reality_zone
        self.reality_zone_formset.save()
