from django import forms

from locations.forms.mage.reality_zone import RealityZoneFormMixin
from locations.models.mage.demesne import Demesne


class DemesneForm(RealityZoneFormMixin, forms.ModelForm):
    class Meta:
        model = Demesne
        fields = ("name", "contained_within", "description", "rank", "size", "accessibility")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        self.fields["size"].widget.attrs.update(
            {"placeholder": "e.g., Small chamber, Expansive realm"}
        )
        self.fields["contained_within"].required = False

    def save(self, commit=True):
        demesne = super().save(commit=False)
        demesne.rank = self.cleaned_data.get("rank")
        if commit:
            demesne.save()
            self.save_m2m()
            self.save_reality_zone(demesne)

        return demesne

    def clean(self):
        cleaned_data = super().clean()

        rank = cleaned_data.get("rank", None)
        if rank is None:
            raise forms.ValidationError("Rank cannot be none")

        self.clean_reality_zone(rank)

        return cleaned_data
