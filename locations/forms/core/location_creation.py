import json

from core.constants import GameLine
from django import forms
from game.models import ObjectType


class LocationCreationForm(forms.Form):
    gameline = forms.ChoiceField(
        choices=[],
        label="Game Line",
        widget=forms.Select(attrs={"id": "id_loc_gameline"}),
    )
    loc_type = forms.ChoiceField(
        choices=[],
        label="Location Type",
        widget=forms.Select(attrs={"id": "id_loc_type"}),
    )
    name = forms.CharField(
        max_length=100,
        label="Name",
        required=False,
    )
    rank = forms.IntegerField(
        initial=1,
        max_value=5,
    )

    def _format_label(self, name):
        """Format location type labels."""
        # Special cases
        special_labels = {
            "reality_zone": "Reality Zone",
            "horizon_realm": "Horizon Realm",
        }

        if name in special_labels:
            return special_labels[name]

        # Default: title case with underscores replaced
        return name.replace("_", " ").title()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            if user.profile.is_st():
                # For STs, show all gamelines and location types
                gamelines_with_locs = set()
                all_loc_types = ObjectType.objects.filter(type="loc")

                for obj in all_loc_types:
                    gamelines_with_locs.add(obj.gameline)

                # Create gameline choices
                gameline_choices = [
                    (code, name) for code, name in GameLine.CHOICES if code in gamelines_with_locs
                ]
                self.fields["gameline"].choices = gameline_choices

                # Build location type choices organized by gameline
                loc_types_by_gameline = {}
                for obj in all_loc_types:
                    if obj.gameline not in loc_types_by_gameline:
                        loc_types_by_gameline[obj.gameline] = []
                    loc_types_by_gameline[obj.gameline].append(
                        {"value": obj.name, "label": self._format_label(obj.name)}
                    )

                # Sort each gameline's types by label
                for gameline in loc_types_by_gameline:
                    loc_types_by_gameline[gameline].sort(key=lambda x: x["label"])

                # Store in widget attrs for JavaScript access
                self.fields["loc_type"].widget.attrs["data-types-by-gameline"] = json.dumps(
                    loc_types_by_gameline
                )

                # Initially populate with first gameline's types
                if gameline_choices:
                    first_gameline = gameline_choices[0][0]
                    initial_choices = [
                        (t["value"], t["label"])
                        for t in loc_types_by_gameline.get(first_gameline, [])
                    ]
                    self.fields["loc_type"].choices = initial_choices
            else:
                # For regular users, only show mage gameline
                self.fields["gameline"].choices = [("mta", "Mage: the Ascension")]

                mage_locs = ObjectType.objects.filter(type="loc", gameline="mta")

                loc_types_by_gameline = {
                    "mta": [
                        {"value": obj.name, "label": self._format_label(obj.name)}
                        for obj in mage_locs
                    ]
                }
                loc_types_by_gameline["mta"].sort(key=lambda x: x["label"])

                self.fields["loc_type"].widget.attrs["data-types-by-gameline"] = json.dumps(
                    loc_types_by_gameline
                )
                self.fields["loc_type"].choices = [
                    (t["value"], t["label"]) for t in loc_types_by_gameline["mta"]
                ]
