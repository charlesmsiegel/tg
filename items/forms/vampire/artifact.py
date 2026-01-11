"""
Forms for VampireArtifact model.

Includes both full edit form for STs/admins and limited edit form for owners.
"""

from django import forms

from items.models.vampire import VampireArtifact


class VampireArtifactForm(forms.ModelForm):
    """
    Full edit form for VampireArtifact.

    Available to:
    - Chronicle Head STs (full permissions)
    - Admins (full permissions)

    Includes all mechanical and descriptive fields.
    """

    class Meta:
        model = VampireArtifact
        fields = [
            "name",
            "description",
            "power_level",
            "background_cost",
            "is_cursed",
            "is_unique",
            "requires_blood",
            "powers",
            "history",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter artifact name...",
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Physical description and appearance...",
                    "class": "form-control",
                }
            ),
            "power_level": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 5,
                    "class": "form-control",
                }
            ),
            "background_cost": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 10,
                    "class": "form-control",
                }
            ),
            "is_cursed": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_unique": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "requires_blood": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "powers": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Describe the artifact's powers and effects...",
                    "class": "form-control",
                }
            ),
            "history": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "History and provenance of the artifact...",
                    "class": "form-control",
                }
            ),
        }
        help_texts = {
            "name": "Name of the vampire artifact",
            "description": "Physical appearance and basic description",
            "power_level": "Power level from 1 (minor) to 5 (legendary)",
            "background_cost": "Background points required to own this artifact",
            "is_cursed": "Check if the artifact carries a curse",
            "is_unique": "Check if this is a one-of-a-kind artifact",
            "requires_blood": "Check if the artifact requires blood to activate or use",
            "powers": "Detailed description of the artifact's powers and game effects",
            "history": "Historical background and lore surrounding the artifact",
        }


class LimitedVampireArtifactEditForm(forms.ModelForm):
    """
    Limited edit form for VampireArtifact owners.

    Owners can only edit:
    - description (physical appearance)
    - history (background/lore)

    Owners CANNOT edit:
    - name, power_level, background_cost
    - Mechanical properties (is_cursed, is_unique, requires_blood)
    - powers (game mechanics)
    """

    class Meta:
        model = VampireArtifact
        fields = [
            "description",
            "history",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Physical description and appearance...",
                    "class": "form-control",
                }
            ),
            "history": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "History and provenance of the artifact...",
                    "class": "form-control",
                }
            ),
        }
        help_texts = {
            "description": "Update the physical appearance and basic description",
            "history": "Add to the historical background and lore (subject to ST approval)",
        }
