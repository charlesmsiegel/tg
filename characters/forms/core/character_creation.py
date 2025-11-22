import json

from core.constants import GameLine
from django import forms
from game.models import ObjectType


class CharacterCreationForm(forms.Form):
    gameline = forms.ChoiceField(
        choices=[],
        label="Game Line",
        widget=forms.Select(attrs={"id": "id_gameline"}),
    )
    char_type = forms.ChoiceField(
        choices=[],
        label="Character Type",
        widget=forms.Select(attrs={"id": "id_char_type"}),
    )

    def _format_label(self, name):
        """Format character type labels with special handling for humans."""
        # Mapping of gameline prefixes to full names
        gameline_map = {
            "mta": "Mage",
            "wto": "Wraith",
            "ctd": "Changeling",
            "wta": "Werewolf",
            "vtm": "Vampire",
            "dtf": "Demon",
        }

        # Check if this is a human type
        if "_human" in name:
            prefix = name.split("_")[0]
            gameline = gameline_map.get(prefix, prefix.upper())
            return f"Human ({gameline})"

        # Special cases
        if name == "spirit_character":
            return "Spirit"

        # Default: title case with underscores replaced
        return name.replace("_", " ").title()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Group types to exclude from character creation (available via separate form)
        group_types = [
            "cabal",
            "group",
            "pack",
            "motley",
            "coterie",
            "circle",
            "conclave",
        ]

        # Non-character types to exclude (metadata/game objects)
        non_character_types = [
            "statistic",
            "specialty",
            "attribute",
            "merit_flaw",
            "human",
            "derangement",
            "character",
            "archetype",
            "ability",
            "background",
            "gameline",
            "house_rule",
            "discipline",
            "path",
            "vampire_clan",
            "vampire_sect",
            "battle_scar",
            "camp",
            "totem",
            "spirit",
            "spirit_charm",
            "tribe",
            "renown_incident",
            "rite",
            "gift",
            "gift_permission",
            "fomori_power",
            "sphere",
            "rote",
            "resonance",
            "instrument",
            "practice",
            "specialized_practice",
            "corrupted_practice",
            "tenet",
            "paradigm",
            "mage_faction",
            "effect",
            "advantage",
        ]

        excluded_types = group_types + non_character_types

        if user and user.is_authenticated:
            if user.profile.is_st():
                # For STs, show all gamelines and character types
                # Build gameline choices
                gamelines_with_chars = set()
                all_char_types = ObjectType.objects.filter(type="char").exclude(
                    name__in=excluded_types
                )

                for obj in all_char_types:
                    gamelines_with_chars.add(obj.gameline)

                # Create gameline choices from GameLine.CHOICES, filtered to those with characters
                gameline_choices = [
                    (code, name)
                    for code, name in GameLine.CHOICES
                    if code in gamelines_with_chars
                ]
                self.fields["gameline"].choices = gameline_choices

                # Build character type choices organized by gameline
                # Store as data attribute for JavaScript filtering
                char_types_by_gameline = {}
                for obj in all_char_types:
                    if obj.gameline not in char_types_by_gameline:
                        char_types_by_gameline[obj.gameline] = []
                    char_types_by_gameline[obj.gameline].append(
                        {"value": obj.name, "label": self._format_label(obj.name)}
                    )

                # Sort each gameline's types by label
                for gameline in char_types_by_gameline:
                    char_types_by_gameline[gameline].sort(key=lambda x: x["label"])

                # Store in widget attrs for JavaScript access
                self.fields["char_type"].widget.attrs[
                    "data-types-by-gameline"
                ] = json.dumps(char_types_by_gameline)

                # Initially populate with first gameline's types
                if gameline_choices:
                    first_gameline = gameline_choices[0][0]
                    initial_choices = [
                        (t["value"], t["label"])
                        for t in char_types_by_gameline.get(first_gameline, [])
                    ]
                    self.fields["char_type"].choices = initial_choices
            else:
                # For regular users, only show mage gameline
                self.fields["gameline"].choices = [("mta", "Mage: the Ascension")]

                mage_types = ObjectType.objects.filter(
                    type="char", gameline="mta"
                ).exclude(name__in=excluded_types)

                char_types_by_gameline = {
                    "mta": [
                        {"value": obj.name, "label": self._format_label(obj.name)}
                        for obj in mage_types
                    ]
                }
                char_types_by_gameline["mta"].sort(key=lambda x: x["label"])

                self.fields["char_type"].widget.attrs[
                    "data-types-by-gameline"
                ] = json.dumps(char_types_by_gameline)
                self.fields["char_type"].choices = [
                    (t["value"], t["label"]) for t in char_types_by_gameline["mta"]
                ]
