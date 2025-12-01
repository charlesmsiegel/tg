import json

from core.constants import GameLine
from django import forms
from game.models import ObjectType


class ItemCreationForm(forms.Form):
    gameline = forms.ChoiceField(
        choices=[],
        label="Game Line",
        widget=forms.Select(attrs={"id": "id_item_gameline"}),
    )
    item_type = forms.ChoiceField(
        choices=[],
        label="Item Type",
        widget=forms.Select(attrs={"id": "id_item_type"}),
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
        """Format item type labels."""
        # Special cases
        special_labels = {
            "sorcerer_artifact": "Sorcerer Artifact",
            "vampire_artifact": "Vampire Artifact",
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
                # For STs, show all gamelines and item types
                gamelines_with_items = set()
                all_item_types = ObjectType.objects.filter(type="obj")

                for obj in all_item_types:
                    gamelines_with_items.add(obj.gameline)

                # Create gameline choices
                gameline_choices = [
                    (code, name) for code, name in GameLine.CHOICES if code in gamelines_with_items
                ]
                self.fields["gameline"].choices = gameline_choices

                # Build item type choices organized by gameline
                item_types_by_gameline = {}
                for obj in all_item_types:
                    if obj.gameline not in item_types_by_gameline:
                        item_types_by_gameline[obj.gameline] = []
                    item_types_by_gameline[obj.gameline].append(
                        {"value": obj.name, "label": self._format_label(obj.name)}
                    )

                # Sort each gameline's types by label
                for gameline in item_types_by_gameline:
                    item_types_by_gameline[gameline].sort(key=lambda x: x["label"])

                # Store in widget attrs for JavaScript access
                self.fields["item_type"].widget.attrs["data-types-by-gameline"] = json.dumps(
                    item_types_by_gameline
                )

                # Initially populate with first gameline's types
                if gameline_choices:
                    first_gameline = gameline_choices[0][0]
                    initial_choices = [
                        (t["value"], t["label"])
                        for t in item_types_by_gameline.get(first_gameline, [])
                    ]
                    self.fields["item_type"].choices = initial_choices
            else:
                # For regular users, only show mage gameline
                self.fields["gameline"].choices = [("mta", "Mage: the Ascension")]

                mage_items = ObjectType.objects.filter(type="obj", gameline="mta")

                item_types_by_gameline = {
                    "mta": [
                        {"value": obj.name, "label": self._format_label(obj.name)}
                        for obj in mage_items
                    ]
                }
                item_types_by_gameline["mta"].sort(key=lambda x: x["label"])

                self.fields["item_type"].widget.attrs["data-types-by-gameline"] = json.dumps(
                    item_types_by_gameline
                )
                self.fields["item_type"].choices = [
                    (t["value"], t["label"]) for t in item_types_by_gameline["mta"]
                ]
