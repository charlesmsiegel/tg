from django import forms

from locations.forms.mage.reality_zone import RealityZoneFormMixin
from locations.models.mage.sanctum import Sanctum


class SanctumForm(RealityZoneFormMixin, forms.ModelForm):
    class Meta:
        model = Sanctum
        fields = ("name", "contained_within", "description", "rank")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        self.fields["contained_within"].required = False

    def save(self, commit=True):
        sanctum = super().save(commit=False)
        sanctum.rank = self.cleaned_data.get("rank")
        if commit:
            sanctum.save()
            self.save_m2m()
            self.save_reality_zone(sanctum)

        return sanctum

    def clean(self):
        cleaned_data = super().clean()

        rank = cleaned_data.get("rank", None)
        if rank is None:
            raise forms.ValidationError("Rank cannot be none")

        self.clean_reality_zone(rank)

        return cleaned_data
