from django import forms
from locations.models.changeling import DreamRealm


class DreamRealmForm(forms.ModelForm):
    """Form for creating and editing Dream Realms"""

    class Meta:
        model = DreamRealm
        fields = (
            "name",
            "description",
            "depth",
            "realm_type",
            "stability",
            "accessibility",
            "appearance",
            "laws_of_reality",
            "inhabitants",
            "ruler",
            "emotional_tone",
            "entry_requirements",
            "exit_difficulty",
            "mundane_connection",
            "glamour_level",
            "provides_glamour",
            "treasures",
            "time_flow",
            "is_mutable",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Enter dream realm description"}
            ),
            "appearance": forms.Textarea(
                attrs={"rows": 3, "placeholder": "What this realm looks like - dream logic applies"}
            ),
            "laws_of_reality": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "How reality works here (gravity, time, causality)",
                }
            ),
            "inhabitants": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Who or what lives in this realm (chimera, dreamers)",
                }
            ),
            "entry_requirements": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "What's needed to enter (trod, ritual, state of mind)",
                }
            ),
            "mundane_connection": forms.Textarea(
                attrs={"rows": 2, "placeholder": "What in the Autumn World this realm connects to"}
            ),
            "treasures": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Special items, knowledge, or powers found here"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter dream realm name"})
        self.fields["ruler"].widget.attrs.update(
            {"placeholder": "Who rules or controls this realm (if anyone)"}
        )
        self.fields["emotional_tone"].widget.attrs.update(
            {"placeholder": "E.g., peaceful, chaotic, melancholic"}
        )

        # Set help text
        self.fields["stability"].help_text = "0-5 dots. How stable/permanent this realm is"
        self.fields["accessibility"].help_text = "0-5 dots. How easy it is to reach"
        self.fields["exit_difficulty"].help_text = "0-10. How hard it is to leave"
        self.fields["glamour_level"].help_text = "0-10. How much Glamour permeates this realm"
