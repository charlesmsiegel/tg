"""Approved, public starting concepts, scoped to a gameline and character type."""

from django import forms

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
            self.fields["template"].queryset = CharacterTemplate.objects.filter(
                gameline=self.gameline,
                character_type=self.character_type,
                is_public=True,
                status="App",
            ).order_by("name")
