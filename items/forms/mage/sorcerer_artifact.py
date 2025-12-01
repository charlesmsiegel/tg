from django import forms
from items.models.mage import SorcererArtifact


class SorcererArtifactForm(forms.ModelForm):
    class Meta:
        model = SorcererArtifact
        fields = ["name", "rank", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})


class ArtifactCreateOrSelectForm(forms.Form):
    select_or_create = forms.BooleanField(required=False)
    select = forms.ModelChoiceField(queryset=SorcererArtifact.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False

        self.artifact_form = SorcererArtifactForm(
            data=self.data if self.is_bound else None,
            prefix="artifact",
        )

    def save(self, commit=True):
        select_or_create = self.cleaned_data.get("select_or_create")
        select = self.cleaned_data.get("select")
        if not select_or_create and select:
            return select
        return self.artifact_form.save(commit=commit)

    def clean(self):
        cleaned_data = super().clean()
        select_or_create = cleaned_data.get("select_or_create")
        select = cleaned_data.get("select")

        # If not creating a new one, user must have selected an existing effect.
        if not select_or_create and not select:
            self.add_error(
                "select",
                "You must either select an existing Artifact or choose to create a new one.",
            )
        return cleaned_data
