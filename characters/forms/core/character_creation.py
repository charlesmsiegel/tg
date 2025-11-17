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
        group_types = ["cabal", "group", "pack", "motley"]

        if user.is_authenticated:
            if user.profile.is_st():
                choices = [
                    (x.name, self._format_label(x.name))
                    for x in ObjectType.objects.filter(type="char")
                    if x.name
                    in [
                        "mage",
                        "sorcerer",
                        "mta_human",
                        "wto_human",
                        "ctd_human",
                        "wta_human",
                        "vtm_human",
                        "changeling",
                        "kinfolk",
                        "fomor",
                        "companion",
                        "werewolf",
                        "spirit_character",
                    ]
                ]
                # Sort alphabetically by label
                self.fields["char_type"].choices = sorted(choices, key=lambda x: x[1])
            else:
                choices = [
                    (x.name, self._format_label(x.name))
                    for x in ObjectType.objects.filter(type="char")
                    if x.name in ["mage", "sorcerer"]
                ]
                # Sort alphabetically by label
                self.fields["char_type"].choices = sorted(choices, key=lambda x: x[1])
