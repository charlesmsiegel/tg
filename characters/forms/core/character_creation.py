from core.constants import GameLine
from django import forms
from game.models import ObjectType
from widgets import ChainedChoiceField, ChainedSelectMixin


class CharacterCreationForm(ChainedSelectMixin, forms.Form):
    gameline = ChainedChoiceField(
        choices=[],
        label="Game Line",
    )
    char_type = ChainedChoiceField(
        parent_field="gameline",
        choices_map={},
        label="Character Type",
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
            "htr": "Hunter",
            "mtr": "Mummy",
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

    # Types to exclude from character creation
    EXCLUDED_TYPES = [
        # Groups (available via separate form)
        "cabal",
        "group",
        "pack",
        "motley",
        "coterie",
        "circle",
        "conclave",
        # Core mechanics
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
        # Changeling mechanics
        "kith",
        "house",
        "house_faction",
        "legacy",
        "cantrip",
        "chimera",
        # Demon mechanics
        "demon_faction",
        "demon_house",
        "lore",
        "visage",
        "pact",
        "demon_ritual",
        "apocalyptic_form_trait",
        # Hunter mechanics
        "creed",
        "edge",
        "hunter_organization",
        # Mage mechanics
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
        "sorcerer_fellowship",
        "linear_magic_path",
        "linear_magic_ritual",
        # Mummy mechanics
        "dynasty",
        "mummy_title",
        # Vampire mechanics
        "discipline",
        "path",
        "vampire_clan",
        "vampire_sect",
        "vampire_title",
        "revenant_family",
        # Werewolf mechanics
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
        "sept_position",
        # Wraith mechanics
        "wraith_faction",
        "guild",
        "arcanos",
        "thorn",
        "shadow_archetype",
    ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Set widget ids
        self.fields["gameline"].widget.attrs["id"] = "id_gameline"
        self.fields["char_type"].widget.attrs["id"] = "id_char_type"

        if user and user.is_authenticated:
            if user.profile.is_st():
                # For STs, show all gamelines and character types
                gamelines_with_chars = set()
                all_char_types = ObjectType.objects.filter(type="char").exclude(
                    name__in=self.EXCLUDED_TYPES
                )

                for obj in all_char_types:
                    gamelines_with_chars.add(obj.gameline)

                # Create gameline choices from GameLine.CHOICES
                gameline_choices = [
                    (code, name) for code, name in GameLine.CHOICES if code in gamelines_with_chars
                ]
                self.fields["gameline"].choices = gameline_choices

                # Build choices_map for ChainedChoiceField
                choices_map = {}
                for obj in all_char_types:
                    if obj.gameline not in choices_map:
                        choices_map[obj.gameline] = []
                    choices_map[obj.gameline].append((obj.name, self._format_label(obj.name)))

                # Sort each gameline's types by label
                for gameline in choices_map:
                    choices_map[gameline].sort(key=lambda x: x[1])

                # Assign choices_map to the char_type field
                self.fields["char_type"].choices_map = choices_map

                # Pre-populate initial char_type choices from first gameline
                if gameline_choices:
                    first_gameline = gameline_choices[0][0]
                    if first_gameline in choices_map:
                        initial_choices = [("", "---------")] + choices_map[first_gameline]
                        self.fields["char_type"].choices = initial_choices
            else:
                # For regular users, only show mage gameline
                self.fields["gameline"].choices = [("mta", "Mage: the Ascension")]

                mage_types = ObjectType.objects.filter(type="char", gameline="mta").exclude(
                    name__in=self.EXCLUDED_TYPES
                )

                choices_map = {
                    "mta": sorted(
                        [(obj.name, self._format_label(obj.name)) for obj in mage_types],
                        key=lambda x: x[1],
                    )
                }
                self.fields["char_type"].choices_map = choices_map

                # Pre-populate initial char_type choices from mta gameline
                if "mta" in choices_map:
                    initial_choices = [("", "---------")] + choices_map["mta"]
                    self.fields["char_type"].choices = initial_choices

            # Re-run chain setup after choices are configured
            self._setup_chains()
