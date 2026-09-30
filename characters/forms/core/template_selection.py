"""Approved, public starting concepts, scoped to a gameline and character type."""

from django import forms
from django.db.models import Q

from core.models import CharacterTemplate


class CharacterTemplateSelectionForm(forms.Form):
    gameline = None
    character_type = None

    template = forms.ModelChoiceField(
        queryset=CharacterTemplate.objects.none(),
        required=False,
        empty_label="No template - build from scratch",
        widget=forms.RadioSelect,
        help_text="Select a pre-made character concept to speed up creation",
    )

    def __init__(self, *args, character=None, **kwargs):
        super().__init__(*args, **kwargs)
        if character is not None:
            # Official templates (seeded, editable only by scoped editors) count as
            # vetted even while the seed data leaves them at the default status.
            vetted = Q(status="App") | (Q(is_official=True) & ~Q(status__in=["Ret", "Dec"]))
            self.fields["template"].queryset = CharacterTemplate.objects.filter(
                vetted,
                gameline=self.gameline,
                character_type=self.character_type,
                is_public=True,
            ).order_by("name")
