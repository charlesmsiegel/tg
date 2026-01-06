from django import forms

from items.models.mage import SorcererArtifact
from widgets import CreateOrSelectField, CreateOrSelectFormMixin


class SorcererArtifactForm(forms.ModelForm):
    class Meta:
        model = SorcererArtifact
        fields = ["name", "rank", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})


class ArtifactCreateOrSelectForm(CreateOrSelectFormMixin, forms.Form):
    """Form for selecting an existing Artifact or creating a new one."""

    create_or_select_config = {
        "toggle_field": "select_or_create",
        "select_field": "select",
        "creation_form_attr": "artifact_form",
        "error_message": "You must either select an existing Artifact or choose to create a new one.",
    }

    select_or_create = CreateOrSelectField(label="Create new Artifact?")
    select = forms.ModelChoiceField(queryset=SorcererArtifact.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artifact_form = SorcererArtifactForm(
            data=self.data if self.is_bound else None,
            prefix="artifact",
        )
