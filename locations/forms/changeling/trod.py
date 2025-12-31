from django import forms
from locations.models.changeling import Trod


class TrodForm(forms.ModelForm):
    """Form for creating and editing Trods"""

    class Meta:
        model = Trod
        fields = (
            "name",
            "description",
            "trod_type",
            "origin_name",
            "origin_description",
            "destination_name",
            "destination_description",
            "strength",
            "difficulty",
            "access_requirements",
            "guardians",
            "travel_duration",
            "is_two_way",
            "is_stable",
            "glamour_cost",
            "accessibility_notes",
            "journey_description",
            "known_to",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Enter trod description"}
            ),
            "origin_description": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Description of the origin point"}
            ),
            "destination_description": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Description of the destination"}
            ),
            "access_requirements": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "What's needed to access this trod (key, ritual, knowledge)",
                }
            ),
            "guardians": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Creatures or beings that guard this trod"}
            ),
            "accessibility_notes": forms.Textarea(
                attrs={"rows": 2, "placeholder": "When or how this trod can be accessed"}
            ),
            "journey_description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "What traveling this trod is like - sights, sounds, sensations",
                }
            ),
            "known_to": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Which changelings or groups know about this trod"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter trod name"})
        self.fields["origin_name"].widget.attrs.update(
            {"placeholder": "Name of where this trod starts"}
        )
        self.fields["destination_name"].widget.attrs.update(
            {"placeholder": "Name of where this trod leads"}
        )
        self.fields["travel_duration"].widget.attrs.update(
            {"placeholder": "E.g., instant, minutes, hours"}
        )

        # Set help text
        self.fields["strength"].help_text = "0-5 dots. How strong/stable this trod is"
        self.fields["difficulty"].help_text = (
            "0-10. Difficulty to traverse (0=easy, 10=nearly impossible)"
        )
        self.fields["glamour_cost"].help_text = "0-10. Glamour required to activate/traverse"
