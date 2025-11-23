"""
Limited edit forms for character owners.

These forms restrict owners to editing only descriptive fields (notes, history, goals, description)
and prevent them from directly modifying mechanical fields (stats, attributes, abilities, etc.).

Owners must use the XP/freebie spending system to modify stats.
Only Chronicle Head STs and Admins can directly edit mechanical fields.
"""

from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.core.character import Character
from characters.models.core.human import Human
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.wraith import Wraith
from characters.models.wraith.wtohuman import WtOHuman
from django import forms


class LimitedCharacterEditForm(forms.ModelForm):
    """
    Limited edit form for Character (base).

    Owners can only edit:
    - notes (character journal/notes)
    - description (physical description, public info)
    - public_info (publicly visible information)
    - image (character portrait)

    Owners CANNOT edit:
    - name, concept, status, chronicle
    - Any mechanical fields (attributes, abilities, backgrounds, etc.)
    """

    class Meta:
        model = Character
        fields = [
            "notes",
            "description",
            "public_info",
            "image",
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
        }
        help_texts = {
            "notes": "Private notes only visible to you and storytellers",
            "description": "Physical description and character details",
            "public_info": "Information other players can see about your character",
            "image": "Character portrait (will require ST approval)",
        }


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


def create_limited_edit_form(model_class):
    """
    Factory function to create a limited edit form for a specific character model.

    Args:
        model_class: The character model class (e.g., Mage, Vampire, Garou)

    Returns:
        A LimitedHumanEditForm subclass configured for the specified model

    Example:
        >>> LimitedMageEditForm = create_limited_edit_form(Mage)
        >>> form = LimitedMageEditForm(instance=mage_instance)
    """

    class GeneratedLimitedEditForm(LimitedHumanEditForm):
        class Meta(LimitedHumanEditForm.Meta):
            model = model_class

    # Set a meaningful name for the generated class
    GeneratedLimitedEditForm.__name__ = f"Limited{model_class.__name__}EditForm"
    GeneratedLimitedEditForm.__qualname__ = f"Limited{model_class.__name__}EditForm"

    return GeneratedLimitedEditForm


# Generate limited edit forms for all gameline-specific character types
LimitedMageEditForm = create_limited_edit_form(Mage)
LimitedMtAHumanEditForm = create_limited_edit_form(MtAHuman)
LimitedVampireEditForm = create_limited_edit_form(Vampire)
LimitedVtMHumanEditForm = create_limited_edit_form(VtMHuman)
LimitedGarouEditForm = create_limited_edit_form(Garou)
LimitedWtAHumanEditForm = create_limited_edit_form(WtAHuman)
LimitedChangelingEditForm = create_limited_edit_form(Changeling)
LimitedCtDHumanEditForm = create_limited_edit_form(CtDHuman)
LimitedWraithEditForm = create_limited_edit_form(Wraith)
LimitedWtOHumanEditForm = create_limited_edit_form(WtOHuman)
LimitedDemonEditForm = create_limited_edit_form(Demon)
LimitedDtFHumanEditForm = create_limited_edit_form(DtFHuman)
