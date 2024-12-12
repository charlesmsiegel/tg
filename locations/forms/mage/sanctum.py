from django import forms
from locations.forms.mage.reality_zone import RealityZonePracticeRatingFormSet
from locations.models.core.location import LocationModel
from locations.models.mage.reality_zone import RealityZone
from locations.models.mage.sanctum import Sanctum


class SanctumForm(forms.ModelForm):
    class Meta:
        model = Sanctum
        fields = ("name", "parent", "description", "rank")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        self.fields["parent"].required = False
        if self.instance.pk and self.instance.reality_zone:
            self.reality_zone = self.instance.reality_zone
        else:
            self.reality_zone = RealityZone()

        self.reality_zone_formset = RealityZonePracticeRatingFormSet(
            instance=self.reality_zone,
            data=self.data if self.is_bound else None,
            prefix="reality_zone",
        )

    def is_valid(self):
        valid = super().is_valid()
        valid = valid and self.reality_zone_formset.is_valid()
        return valid

    def save(self, commit=True):
        sanctum = super().save(commit=False)
        sanctum.rank = self.cleaned_data.get("rank")
        if commit:
            sanctum.save()
            self.reality_zone.name = (
                sanctum.name
            )  # Or get from form if you have a RealityZoneForm
            self.reality_zone.save()
            sanctum.reality_zone = self.reality_zone
            sanctum.save()

            # Save the RealityZonePracticeRatingFormSet
            self.reality_zone_formset.instance = self.reality_zone
            self.reality_zone_formset.save()

        return sanctum

    def clean(self):
        cleaned_data = super().clean()

        rank = cleaned_data.get("rank", None)
        if rank is None:
            raise forms.ValidationError("Rank cannot be none")

        if not self.reality_zone_formset.is_valid():
            return cleaned_data

        total_rz_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.reality_zone_formset
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )

        total_positive_rz_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.reality_zone_formset
            if form.cleaned_data
            and not form.cleaned_data.get("DELETE", False)
            and form.cleaned_data.get("rating", 0) > 0
        )

        if total_rz_rating != 0:
            raise forms.ValidationError("Reality Zone Ratings must total 0")

        if total_positive_rz_rating != rank:
            raise forms.ValidationError(
                "Positive Reality Zone Ratings must sum to Node rating"
            )

        return cleaned_data
