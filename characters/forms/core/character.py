from django import forms

from characters.models.core import Character


class LimitedCharacterForm(forms.ModelForm):
    """
    Form for character owners to edit descriptive fields only.

    Owners can edit:
    - notes: Personal notes about the character
    - description: Character description
    - public_info: Information visible to other players
    - concept: Character concept
    - image: Character image (subject to ST approval)

    Owners CANNOT edit mechanical fields like:
    - name, chronicle, status, xp, spent_xp, creation_status
    - display, visibility, freebies_approved
    - owner (security risk)
    """

    class Meta:
        model = Character
        fields = [
            "concept",
            "description",
            "public_info",
            "notes",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholders for better UX
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter character concept"})
        self.fields["description"].widget.attrs.update(
            {
                "placeholder": "Describe your character's appearance, personality, history, etc.",
                "rows": 6,
            }
        )
        self.fields["public_info"].widget.attrs.update(
            {
                "placeholder": "Information that other players can see about your character",
                "rows": 4,
            }
        )
        self.fields["notes"].widget.attrs.update(
            {
                "placeholder": "Private notes (only you and STs can see these)",
                "rows": 4,
            }
        )

        # Image is optional
        self.fields["image"].required = False

        # Add help text
        self.fields["public_info"].help_text = (
            "This information is visible to other players based on visibility settings."
        )
        self.fields["notes"].help_text = "Private notes visible only to you and storytellers."

    def save(self, commit=True):
        """
        Save the form.

        When saving with an image, reset image_status to 'sub' (submitted)
        so STs can review/approve the new image.
        """
        instance = super().save(commit=False)

        # If image was changed, mark it as needing approval
        if "image" in self.changed_data and instance.image:
            instance.image_status = "sub"

        if commit:
            instance.save()

        return instance
