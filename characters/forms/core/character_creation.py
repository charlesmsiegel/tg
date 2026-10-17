from django import forms

from core.constants import GameLine
from core.create_redirects import creatable_character_types
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
        self.fields["gameline"].widget.attrs["class"] = "tg-form-control tg-form-select"
        self.fields["char_type"].widget.attrs["id"] = "id_char_type"

        if not user or not user.is_authenticated:
            return

        self._configure_creation_choices(user)
        # Re-run chain setup after choices are configured.
        self._setup_chains()

    def _configure_creation_choices(self, user):
        object_types = ObjectType.objects.filter(type="char").exclude(name__in=self.EXCLUDED_TYPES)
        if user.profile.is_st():
            gamelines = GameLine.CHOICES
            choices_map = {}
        else:
            object_types = object_types.filter(gameline="mta")
            gamelines = [("mta", "Mage: the Ascension")]
            # Players keep the Mage picker even when its catalogue is empty.
            choices_map = {"mta": []}

        choices_map.update(self._group_character_types(object_types))
        gameline_choices = [(code, label) for code, label in gamelines if code in choices_map]
        self.fields["gameline"].choices = gameline_choices
        self.fields["char_type"].choices_map = choices_map

        if gameline_choices:
            first_gameline = gameline_choices[0][0]
            self.fields["char_type"].choices = [("", "---------")] + choices_map[first_gameline]

    def _group_character_types(self, object_types):
        """Group routed character types by gameline, with labels in display order."""
        choices_map = {}
        for obj in creatable_character_types(object_types):
            choices_map.setdefault(obj.gameline, []).append(
                (obj.name, self._format_label(obj.name))
            )
        for choices in choices_map.values():
            choices.sort(key=lambda choice: choice[1])
        return choices_map
