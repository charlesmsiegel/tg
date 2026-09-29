"""
Unified NPC/linked character creation form for all background types.
This single form handles Allies, Mentors, Contacts, Retainers, and Followers.
Character type selects the model; subtype and parent choices must match that
model's existing rules before they are copied into canonical character fields.
"""

import json

from django import forms

from characters.forms.werewolf.fera import FERA_CLASSES, FeraCreationForm
from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.changeling.kith import Kith
from characters.models.core.archetype import Archetype
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.house import DemonHouse
from characters.models.demon.thrall import Thrall
from characters.models.mage.companion import Companion
from characters.models.mage.faction import MageFaction
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.guild import Guild
from characters.models.wraith.wraith import Wraith
from characters.models.wraith.wtohuman import WtOHuman


class LinkedNPCForm(forms.Form):
    """
    Unified form for creating NPC characters linked through backgrounds.
    Used for: Allies, Mentors, Contacts, Retainers, Followers, etc.

    This form supports creating any character type in the system with their basics,
    making them ready for completion after the linking character finishes creation.
    """

    # Character type choices - organized by gameline
    NPC_TYPE_CHOICES = [
        (
            "--- Vampire ---",
            [
                ("vampire", "Vampire"),
                ("vtmhuman", "Human (Vampire)"),
                ("ghoul", "Ghoul"),
            ],
        ),
        (
            "--- Werewolf ---",
            [
                ("werewolf", "Werewolf (Garou)"),
                ("wtahuman", "Human (Werewolf)"),
                ("kinfolk", "Kinfolk"),
                ("fera", "Fera (Changing Breeds)"),
                ("fomor", "Fomor"),
            ],
        ),
        (
            "--- Mage ---",
            [
                ("mage", "Mage (Awakened)"),
                ("mtahuman", "Human (Mage)"),
                ("sorcerer", "Sorcerer"),
                ("companion", "Companion"),
            ],
        ),
        (
            "--- Wraith ---",
            [
                ("wraith", "Wraith"),
                ("wtohuman", "Human (Wraith)"),
            ],
        ),
        (
            "--- Changeling ---",
            [
                ("changeling", "Changeling"),
                ("ctdhuman", "Human (Changeling)"),
            ],
        ),
        (
            "--- Demon ---",
            [
                ("demon", "Demon"),
                ("dtfhuman", "Human (Demon)"),
                ("thrall", "Thrall"),
            ],
        ),
        (
            "--- Other ---",
            [
                ("spirit", "Spirit"),
            ],
        ),
    ]

    NPC_CLASSES = {
        "vampire": Vampire,
        "vtmhuman": VtMHuman,
        "ghoul": Ghoul,
        "werewolf": Werewolf,
        "wtahuman": WtAHuman,
        "kinfolk": Kinfolk,
        "fera": Fera,
        "fomor": Fomor,
        "mage": Mage,
        "mtahuman": MtAHuman,
        "sorcerer": Sorcerer,
        "companion": Companion,
        "wraith": Wraith,
        "wtohuman": WtOHuman,
        "changeling": Changeling,
        "ctdhuman": CtDHuman,
        "demon": Demon,
        "dtfhuman": DtFHuman,
        "thrall": Thrall,
        "spirit": SpiritCharacter,
    }

    # Common fields for all types
    npc_type = forms.ChoiceField(
        choices=NPC_TYPE_CHOICES,
        label="Character Type",
        help_text="Select the type of character to create",
    )
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(attrs={"placeholder": "Character name"}),
    )
    rank = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=1,
        label="Background Rating",
        help_text="Background rating (0-5)",
    )
    concept = forms.CharField(
        max_length=100,
        label="Concept",
        widget=forms.TextInput(attrs={"placeholder": "Brief character concept"}),
        required=False,
    )

    # Archetype fields (for types that use them)
    nature = forms.ModelChoiceField(
        queryset=Archetype.objects.all(),
        label="Nature",
        required=False,
        help_text="Inner self",
    )
    demeanor = forms.ModelChoiceField(
        queryset=Archetype.objects.all(),
        label="Demeanor",
        required=False,
        help_text="Outer personality",
    )

    # The selected values belong on the new character's actual fields.
    clan = forms.ModelChoiceField(
        queryset=VampireClan.objects.all(),
        required=False,
        label="Clan",
    )
    sect = forms.ModelChoiceField(
        queryset=VampireSect.objects.all(),
        required=False,
        label="Sect",
    )

    werewolf_breed = forms.ChoiceField(
        choices=[("", "Choose breed"), *Werewolf.BREEDS], required=False, label="Breed"
    )
    auspice = forms.ChoiceField(
        choices=[("", "Choose auspice"), *Werewolf.AUSPICES], required=False, label="Auspice"
    )
    tribe = forms.ModelChoiceField(queryset=Tribe.objects.all(), required=False, label="Tribe")

    fera_type = forms.ChoiceField(
        choices=[("", "Choose Fera type"), *FeraCreationForm.FERA_TYPES],
        required=False,
        label="Fera Type",
    )
    fera_breed = forms.ChoiceField(
        choices=[
            ("", "Choose breed"),
            *dict(
                breed for fera_class in FERA_CLASSES.values() for breed in fera_class.BREEDS
            ).items(),
        ],
        required=False,
        label="Breed",
    )

    affiliation = forms.ModelChoiceField(
        queryset=MageFaction.objects.top_level(),
        required=False,
        label="Affiliation",
    )
    faction = forms.ModelChoiceField(
        queryset=MageFaction.objects.all(), required=False, label="Faction"
    )
    subfaction = forms.ModelChoiceField(
        queryset=MageFaction.objects.all(), required=False, label="Subfaction"
    )
    fellowship = forms.ModelChoiceField(
        queryset=SorcererFellowship.objects.all(), required=False, label="Fellowship"
    )

    guild = forms.ModelChoiceField(
        queryset=Guild.objects.all(),
        required=False,
        label="Guild",
    )

    kith = forms.ModelChoiceField(
        queryset=Kith.objects.all(),
        required=False,
        label="Kith",
    )
    court = forms.ChoiceField(
        choices=[("", "Choose court"), *Changeling._meta.get_field("court").choices],
        required=False,
        label="Court",
    )

    house = forms.ModelChoiceField(
        queryset=DemonHouse.objects.all(),
        required=False,
        label="House",
    )

    # General notes
    note = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "How do you know them, and what can they do for you?", "rows": 4}
        ),
        label="Notes",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with optional customization.

        Parameters:
            obj: The character this NPC is being created for
            npc_role: The role/relationship (e.g., 'ally', 'mentor', 'contact', 'retainer', 'follower')
        """
        self.obj = kwargs.pop("obj", None)
        self.npc_role = kwargs.pop("npc_role", "ally")  # Default to 'ally'
        super().__init__(*args, **kwargs)

        # Customize label based on role
        role_display = self.npc_role.capitalize()
        self.fields["rank"].label = f"{role_display} Rating"
        self.fera_breeds_json = json.dumps(
            {name: [breed for breed, _ in model.BREEDS] for name, model in FERA_CLASSES.items()}
        )
        self.faction_parents_json = json.dumps(
            {
                str(pk): str(parent_id) if parent_id else ""
                for pk, parent_id in MageFaction.objects.values_list("pk", "parent_id")
            }
        )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("npc_type") == "fera":
            fera_class = FERA_CLASSES.get(cleaned.get("fera_type"))
            if not fera_class:
                self.add_error("fera_type", "Choose a Fera type.")
            elif cleaned.get("fera_breed") and cleaned["fera_breed"] not in dict(fera_class.BREEDS):
                self.add_error("fera_breed", "Choose a breed available to this Fera type.")
        if cleaned.get("npc_type") == "mage":
            affiliation = cleaned.get("affiliation")
            faction = cleaned.get("faction")
            subfaction = cleaned.get("subfaction")
            if faction and (not affiliation or faction.parent_id != affiliation.pk):
                self.add_error("faction", "Choose a faction within the affiliation.")
            if subfaction and (not faction or subfaction.parent_id != faction.pk):
                self.add_error("subfaction", "Choose a subfaction within the faction.")
        return cleaned

    def save(self, commit=True):
        """
        Create the NPC character with basic information filled in.
        The character is created with status='Un' (Unfinished) so it can be completed later.
        """
        npc_type = self.cleaned_data["npc_type"]
        char_class = (
            FERA_CLASSES[self.cleaned_data["fera_type"]]
            if npc_type == "fera"
            else self.NPC_CLASSES[npc_type]
        )

        # Build base note with rank and role
        role_display = self.npc_role.capitalize()
        note = (
            self.cleaned_data.get("note") or ""
        ) + f"<br>Rank {self.cleaned_data['rank']} {role_display}"
        if self.obj is not None:
            note += " for " + self.obj.name

        # Prepare common fields
        char_data = {
            "name": self.cleaned_data["name"],
            "concept": self.cleaned_data.get("concept") or "",
            "notes": note,
            "status": "Un",  # Unfinished - to be completed later
            "npc": True,
        }

        # Add archetypes for types that use them
        # Werewolves, Changelings, and Fera don't use nature/demeanor
        if npc_type not in ["werewolf", "changeling", "fera"]:
            if self.cleaned_data.get("nature"):
                char_data["nature"] = self.cleaned_data["nature"]
            if self.cleaned_data.get("demeanor"):
                char_data["demeanor"] = self.cleaned_data["demeanor"]

        # Copy selected rules data to the new character's real fields.
        field_map = {
            "vampire": {"clan": "clan", "sect": "sect"},
            "werewolf": {
                "werewolf_breed": "breed",
                "auspice": "auspice",
                "tribe": "tribe",
            },
            "kinfolk": {"tribe": "tribe"},
            "fera": {"fera_breed": "breed"},
            "mage": {
                "affiliation": "affiliation",
                "faction": "faction",
                "subfaction": "subfaction",
            },
            "sorcerer": {"fellowship": "fellowship"},
            "wraith": {"guild": "guild"},
            "changeling": {"kith": "kith", "court": "court"},
            "demon": {"house": "house"},
        }
        for source, target in field_map.get(npc_type, {}).items():
            if value := self.cleaned_data.get(source):
                char_data[target] = value

        # Create the character
        obj = char_class.objects.create(**char_data)
        return obj
