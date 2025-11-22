from django import forms
from game.models import ObjectType


class CharacterCreationForm(forms.Form):
    char_type = forms.ChoiceField(choices=[])

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

        # Group types to exclude from character creation
        group_types = ["cabal", "group", "pack", "motley", "coterie", "circle", "conclave"]

        # Non-character types to exclude (metadata/game objects)
        non_character_types = [
            "statistic", "specialty", "attribute", "merit_flaw", "human", "derangement",
            "character", "archetype", "ability", "background", "gameline", "house_rule",
            "discipline", "path", "vampire_clan", "vampire_sect", "battle_scar", "camp",
            "totem", "spirit", "spirit_charm", "tribe", "renown_incident", "rite", "gift",
            "gift_permission", "fomori_power", "sphere", "rote", "resonance", "instrument",
            "practice", "specialized_practice", "corrupted_practice", "tenet", "paradigm",
            "mage_faction", "effect", "advantage"
        ]

        if user.is_authenticated:
            if user.profile.is_st():
                # For STs, show all character types except groups and non-character metadata
                excluded_types = group_types + non_character_types
                choices = [
                    (x.name, self._format_label(x.name))
                    for x in ObjectType.objects.filter(type="char")
                    if x.name not in excluded_types
                ]
                # Sort alphabetically by label
                self.fields["char_type"].choices = sorted(choices, key=lambda x: x[1])
            else:
                # For regular users, only show mage and sorcerer
                choices = [
                    (x.name, self._format_label(x.name))
                    for x in ObjectType.objects.filter(type="char")
                    if x.name in ["mage", "sorcerer"]
                ]
                # Sort alphabetically by label
                self.fields["char_type"].choices = sorted(choices, key=lambda x: x[1])
