"""
Enhanced Mentor/NPC creation form that supports all character types with their basics.
This form creates NPCs with essential information filled in, ready for completion.
"""
from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.thrall import Thrall
from characters.models.mage.companion import Companion
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.wraith import Wraith
from characters.models.wraith.wtohuman import WtOHuman
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.core.archetype import Archetype
from django import forms


class MentorEnhancedForm(forms.Form):
    """
    Enhanced form for creating NPC allies with proper basics.
    Supports all character types in the system.
    """

    # Character type choices - organized by gameline
    ALLY_TYPE_CHOICES = [
        ("--- Vampire ---", [
            ("vampire", "Vampire"),
            ("vtmhuman", "Human (Vampire)"),
            ("ghoul", "Ghoul"),
        ]),
        ("--- Werewolf ---", [
            ("werewolf", "Werewolf (Garou)"),
            ("wtahuman", "Human (Werewolf)"),
            ("kinfolk", "Kinfolk"),
            ("fera", "Fera (Changing Breeds)"),
            ("fomor", "Fomor"),
        ]),
        ("--- Mage ---", [
            ("mage", "Mage (Awakened)"),
            ("mtahuman", "Human (Mage)"),
            ("sorcerer", "Sorcerer"),
            ("companion", "Companion"),
        ]),
        ("--- Wraith ---", [
            ("wraith", "Wraith"),
            ("wtohuman", "Human (Wraith)"),
        ]),
        ("--- Changeling ---", [
            ("changeling", "Changeling"),
            ("ctdhuman", "Human (Changeling)"),
        ]),
        ("--- Demon ---", [
            ("demon", "Demon"),
            ("dtfhuman", "Human (Demon)"),
            ("thrall", "Thrall"),
        ]),
        ("--- Other ---", [
            ("spirit", "Spirit"),
        ]),
    ]

    ALLY_CLASSES = {
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
    mentor_type = forms.ChoiceField(
        choices=ALLY_TYPE_CHOICES,
        label="Mentor Type",
        help_text="Select the type of character to create"
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
        label="Mentor Rating",
        help_text="Mentor background rating (0-5)"
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
        help_text="Inner self (leave blank for Werewolf/Changeling)"
    )
    demeanor = forms.ModelChoiceField(
        queryset=Archetype.objects.all(),
        label="Demeanor",
        required=False,
        help_text="Outer personality (leave blank for Werewolf/Changeling)"
    )

    # Gameline-specific basics - collected but only used if relevant
    # Vampire
    clan_name = forms.CharField(
        max_length=100,
        required=False,
        label="Clan",
        widget=forms.TextInput(attrs={"placeholder": "Vampire clan (if Vampire)"}),
        help_text="For Vampires only"
    )
    sect_name = forms.CharField(
        max_length=100,
        required=False,
        label="Sect",
        widget=forms.TextInput(attrs={"placeholder": "Vampire sect (if Vampire)"}),
        help_text="For Vampires only"
    )

    # Werewolf
    breed_name = forms.CharField(
        max_length=100,
        required=False,
        label="Breed",
        widget=forms.TextInput(attrs={"placeholder": "Homid/Metis/Lupus"}),
        help_text="For Werewolves/Fera only"
    )
    auspice_name = forms.CharField(
        max_length=100,
        required=False,
        label="Auspice",
        widget=forms.TextInput(attrs={"placeholder": "Moon sign"}),
        help_text="For Werewolves only"
    )
    tribe_name = forms.CharField(
        max_length=100,
        required=False,
        label="Tribe",
        widget=forms.TextInput(attrs={"placeholder": "Tribe name"}),
        help_text="For Werewolves/Kinfolk only"
    )

    # Mage
    affiliation_name = forms.CharField(
        max_length=100,
        required=False,
        label="Affiliation",
        widget=forms.TextInput(attrs={"placeholder": "Tradition/Technocracy/etc"}),
        help_text="For Mages only"
    )

    # Wraith
    guild_name = forms.CharField(
        max_length=100,
        required=False,
        label="Guild",
        widget=forms.TextInput(attrs={"placeholder": "Wraith guild"}),
        help_text="For Wraiths only"
    )

    # Changeling
    kith_name = forms.CharField(
        max_length=100,
        required=False,
        label="Kith",
        widget=forms.TextInput(attrs={"placeholder": "Changeling kith"}),
        help_text="For Changelings only"
    )
    court_name = forms.CharField(
        max_length=100,
        required=False,
        label="Court",
        widget=forms.TextInput(attrs={"placeholder": "Seelie/Unseelie"}),
        help_text="For Changelings only"
    )

    # Demon
    house_name = forms.CharField(
        max_length=100,
        required=False,
        label="House",
        widget=forms.TextInput(attrs={"placeholder": "Demon house"}),
        help_text="For Demons only"
    )

    # Fera special
    fera_type_name = forms.CharField(
        max_length=100,
        required=False,
        label="Fera Type",
        widget=forms.TextInput(attrs={"placeholder": "Ratkin/Mokole/Bastet/etc"}),
        help_text="For Fera only"
    )

    # General notes
    note = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Additional notes about this mentor", "rows": 4}),
        label="Notes",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.obj = kwargs.pop("obj", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Create the NPC character with basic information filled in.
        The character is created with status='Un' (Unfinished) so it can be completed later.
        """
        mentor_type = self.cleaned_data["mentor_type"]
        char_class = self.ALLY_CLASSES[mentor_type]

        # Build base note with rank
        note = (
            (self.cleaned_data.get("note") or "")
            + "<br>Rank "
            + str(self.cleaned_data["rank"])
            + " Mentor"
        )
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
        if mentor_type not in ["werewolf", "changeling", "fera"]:
            if self.cleaned_data.get("nature"):
                char_data["nature"] = self.cleaned_data["nature"]
            if self.cleaned_data.get("demeanor"):
                char_data["demeanor"] = self.cleaned_data["demeanor"]

        # Add gameline-specific basics to notes for reference
        # We store these in notes since the actual ForeignKey fields need real objects
        specific_info = []

        if mentor_type == "vampire" and self.cleaned_data.get("clan_name"):
            specific_info.append(f"Clan: {self.cleaned_data['clan_name']}")
        if mentor_type == "vampire" and self.cleaned_data.get("sect_name"):
            specific_info.append(f"Sect: {self.cleaned_data['sect_name']}")

        if mentor_type in ["werewolf", "fera"] and self.cleaned_data.get("breed_name"):
            specific_info.append(f"Breed: {self.cleaned_data['breed_name']}")
        if mentor_type == "werewolf" and self.cleaned_data.get("auspice_name"):
            specific_info.append(f"Auspice: {self.cleaned_data['auspice_name']}")
        if mentor_type in ["werewolf", "kinfolk"] and self.cleaned_data.get("tribe_name"):
            specific_info.append(f"Tribe: {self.cleaned_data['tribe_name']}")

        if mentor_type == "mage" and self.cleaned_data.get("affiliation_name"):
            specific_info.append(f"Affiliation: {self.cleaned_data['affiliation_name']}")

        if mentor_type == "wraith" and self.cleaned_data.get("guild_name"):
            specific_info.append(f"Guild: {self.cleaned_data['guild_name']}")

        if mentor_type == "changeling":
            if self.cleaned_data.get("kith_name"):
                specific_info.append(f"Kith: {self.cleaned_data['kith_name']}")
            if self.cleaned_data.get("court_name"):
                specific_info.append(f"Court: {self.cleaned_data['court_name']}")

        if mentor_type == "demon" and self.cleaned_data.get("house_name"):
            specific_info.append(f"House: {self.cleaned_data['house_name']}")

        if mentor_type == "fera" and self.cleaned_data.get("fera_type_name"):
            specific_info.append(f"Fera Type: {self.cleaned_data['fera_type_name']}")

        if specific_info:
            char_data["notes"] += "<br><br><strong>Basics to set:</strong><br>" + "<br>".join(specific_info)

        # Create the character
        obj = char_class.objects.create(**char_data)
        return obj
