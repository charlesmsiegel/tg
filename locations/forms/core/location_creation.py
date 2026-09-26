from django import forms

from core.constants import GameLine
from core.model_registry import get_registry
from widgets import ChainedChoiceField, ChainedSelectMixin


class LocationCreationForm(ChainedSelectMixin, forms.Form):
    gameline = ChainedChoiceField(choices=[], label="Game Line")
    loc_type = ChainedChoiceField(parent_field="gameline", choices_map={}, label="Location Type")
    name = forms.CharField(max_length=100, required=False)
    rank = forms.IntegerField(initial=1, max_value=5)

    def _format_label(self, name):
        return name.replace("_", " ").title()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if not user or not user.is_authenticated:
            return
        entries = get_registry("locations").menu(user)
        choices = {}
        for entry in entries:
            choices.setdefault(entry.gameline, []).append((entry.slug, entry.menu_label))
        self.fields["gameline"].choices = [
            (code, label) for code, label in GameLine.CHOICES if code in choices
        ]
        self.fields["loc_type"].choices_map = choices
        self.fields["gameline"].widget.attrs["id"] = "id_loc_gameline"
        self.fields["loc_type"].widget.attrs["id"] = "id_loc_type"
        self._setup_chains()
