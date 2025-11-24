from characters.models.werewolf.septposition import SeptPosition
from django import forms


class SeptPositionForm(forms.ModelForm):
    class Meta:
        model = SeptPosition
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"placeholder": "Position name (e.g., Master of the Challenge)"}
        )
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Describe the responsibilities and duties of this position"}
        )
