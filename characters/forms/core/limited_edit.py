"""
Limited edit forms for character owners.

These forms restrict owners to editing only descriptive fields (notes, history, goals, description)
and prevent them from directly modifying mechanical fields (stats, attributes, abilities, etc.).

Owners must use the XP/freebie spending system to modify stats.
Only Chronicle Head STs and Admins can directly edit mechanical fields.

Usage:
    - LimitedHumanEditForm: For Human and ALL Human subclasses (Mage, Vampire, etc.)
      Django ModelForms work with subclass instances, so LimitedHumanEditForm can be
      used directly with any Human subclass (e.g., form = LimitedHumanEditForm(instance=mage))
"""

from django import forms

from characters.models.core.character import Character
from characters.models.core.human import Human


class OwnerUnapprovedCharacterEditForm(forms.ModelForm):
    """Editable character fields while its creator is drafting revisions."""

    class Meta:
        model = Character
        fields = ["name", "concept", "notes", "description", "public_info", "image"]


class LimitedHumanEditForm(forms.ModelForm):
    """
    Limited edit form for Human characters.

    Extends Character fields with:
    - history (character background)
    - goals (character goals and motivations)
    """

    class Meta:
        model = Human
        fields = [
            "notes",
            "description",
            "public_info",
            "image",
            "history",
            "goals",
        ]
        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Personal notes and journal entries...",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Physical description, personality, mannerisms...",
                }
            ),
            "public_info": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Information visible to other players...",
                }
            ),
            "history": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Character background and history..."}
            ),
            "goals": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Character goals and motivations..."}
            ),
        }
        help_texts = {
            "notes": "Private notes only visible to you and storytellers",
            "description": "Physical description and character details",
            "public_info": "Information other players can see about your character",
            "history": "Your character's background story",
            "goals": "What your character wants to achieve",
            "image": "Character portrait (will require ST approval)",
        }
