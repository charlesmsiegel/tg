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
from characters.models.demon.dtfhuman import DtFHuman
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.garou import Garou
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


class LimitedMageEditForm(LimitedHumanEditForm):
    """Limited edit form for Mage characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = Mage


class LimitedMtAHumanEditForm(LimitedHumanEditForm):
    """Limited edit form for MtA Human characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = MtAHuman


class LimitedVampireEditForm(LimitedHumanEditForm):
    """Limited edit form for Vampire characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = Vampire


class LimitedVtMHumanEditForm(LimitedHumanEditForm):
    """Limited edit form for VtM Human characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = VtMHuman


class LimitedGarouEditForm(LimitedHumanEditForm):
    """Limited edit form for Garou characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = Garou


class LimitedWtAHumanEditForm(LimitedHumanEditForm):
    """Limited edit form for WtA Human characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = WtAHuman


class LimitedChangelingEditForm(LimitedHumanEditForm):
    """Limited edit form for Changeling characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = Changeling


class LimitedCtDHumanEditForm(LimitedHumanEditForm):
    """Limited edit form for CtD Human characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = CtDHuman


class LimitedWraithEditForm(LimitedHumanEditForm):
    """Limited edit form for Wraith characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = Wraith


class LimitedWtOHumanEditForm(LimitedHumanEditForm):
    """Limited edit form for WtO Human characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = WtOHuman


class LimitedDemonEditForm(LimitedHumanEditForm):
    """Limited edit form for Demon characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = Demon


class LimitedDtFHumanEditForm(LimitedHumanEditForm):
    """Limited edit form for DtF Human characters."""

    class Meta(LimitedHumanEditForm.Meta):
        model = DtFHuman
