from django import forms
from locations.models.changeling import Holding


class HoldingForm(forms.ModelForm):
    """Form for creating and editing Holdings"""

    class Meta:
        model = Holding
        fields = (
            "name",
            "description",
            "rank",
            "court",
            "ruler_name",
            "ruler_title",
            "territory_description",
            "mundane_location",
            "vassals",
            "liege",
            "freehold_count",
            "major_freeholds",
            "population",
            "military_strength",
            "wealth",
            "stability",
            "political_situation",
            "notable_laws",
            "rival_holdings",
            "history",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Enter holding description"}
            ),
            "territory_description": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Geographic area this holding covers"}
            ),
            "mundane_location": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Real-world location this holding encompasses"}
            ),
            "vassals": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Lesser nobles who owe fealty to this holding's ruler",
                }
            ),
            "major_freeholds": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Names and descriptions of major freeholds"}
            ),
            "political_situation": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Current political climate, tensions, alliances"}
            ),
            "notable_laws": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Important laws or customs specific to this holding",
                }
            ),
            "rival_holdings": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Neighboring or rival holdings and their relations",
                }
            ),
            "history": forms.Textarea(
                attrs={"rows": 4, "placeholder": "History of this holding, major events"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter holding name"})
        self.fields["ruler_name"].widget.attrs.update(
            {"placeholder": "Name of the noble who rules this holding"}
        )
        self.fields["ruler_title"].widget.attrs.update(
            {"placeholder": "E.g., 'Baron of the Silver Mists'"}
        )
        self.fields["liege"].widget.attrs.update(
            {"placeholder": "Higher noble this holding owes allegiance to"}
        )
        self.fields["population"].widget.attrs.update(
            {"placeholder": "E.g., small, moderate, large"}
        )

        # Set help text
        self.fields["military_strength"].help_text = "0-5 dots. Military/defensive capability"
        self.fields["wealth"].help_text = "0-5 dots. Economic resources"
        self.fields["stability"].help_text = (
            "0-5 dots. Political stability (0=chaos, 5=very stable)"
        )
        self.fields["freehold_count"].help_text = "Number of freeholds within this holding (0-50)"
