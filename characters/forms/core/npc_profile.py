from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.changeling.house import House
from characters.models.changeling.kith import Kith
from characters.models.changeling.legacy import Legacy
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.thrall import Thrall
from characters.models.mage.companion import Companion
from characters.models.mage.faction import MageFaction
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.guild import Guild
from characters.models.wraith.wraith import Wraith
from characters.models.wraith.wtohuman import WtOHuman
from django import forms
from game.models import Chronicle


class NPCProfileForm(forms.Form):
    """
    Unified form for creating NPC profiles of any character type.
    Used for creating mentors, contacts, allies, and other NPCs related to PCs.
    """

    NPC_TYPE_CHOICES = [
        ("Vampire", (("vtm_human", "Human (Vampire)"),)),
        (
            "Werewolf",
            (
                ("wta_human", "Human (Werewolf)"),
                ("kinfolk", "Kinfolk"),
                ("fomor", "Fomor"),
                ("werewolf", "Werewolf"),
            ),
        ),
        (
            "Mage",
            (
                ("mta_human", "Human (Mage)"),
                ("sorcerer", "Sorcerer"),
                ("companion", "Companion"),
                ("mage", "Mage"),
            ),
        ),
        (
            "Wraith",
            (
                ("wto_human", "Human (Wraith)"),
                ("wraith", "Wraith"),
            ),
        ),
        (
            "Changeling",
            (
                ("ctd_human", "Human (Changeling)"),
                ("changeling", "Changeling"),
            ),
        ),
        (
            "Demon",
            (
                ("dtf_human", "Human (Demon)"),
                ("thrall", "Thrall"),
                ("demon", "Demon"),
            ),
        ),
    ]

    NPC_CLASSES = {
        "vtm_human": VtMHuman,
        "wta_human": WtAHuman,
        "mta_human": MtAHuman,
        "ctd_human": CtDHuman,
        "wto_human": WtOHuman,
        "dtf_human": DtFHuman,
        "mage": Mage,
        "sorcerer": Sorcerer,
        "companion": Companion,
        "kinfolk": Kinfolk,
        "fomor": Fomor,
        "werewolf": Werewolf,
        "wraith": Wraith,
        "changeling": Changeling,
        "thrall": Thrall,
        "demon": Demon,
    }

    NPC_ROLE_CHOICES = [
        ("", "-- Select Role (Optional) --"),
        ("mentor", "Mentor"),
        ("contact", "Contact"),
        ("ally", "Ally"),
        ("retainer", "Retainer"),
        ("enemy", "Enemy"),
        ("rival", "Rival"),
        ("patron", "Patron"),
        ("employer", "Employer"),
        ("family", "Family Member"),
        ("friend", "Friend"),
        ("other", "Other"),
    ]

    # Basic Information
    npc_type = forms.ChoiceField(
        choices=NPC_TYPE_CHOICES,
        label="Character Type",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter NPC name"}
        ),
    )

    concept = forms.CharField(
        max_length=100,
        label="Concept",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Brief concept (e.g., 'Grizzled Detective', 'Occult Librarian')",
            }
        ),
    )

    # Role and Relationship
    npc_role = forms.ChoiceField(
        choices=NPC_ROLE_CHOICES,
        label="NPC Role",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Chronicle
    chronicle = forms.ModelChoiceField(
        queryset=Chronicle.objects.all(),
        label="Chronicle",
        required=False,
        empty_label="-- No Chronicle --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Descriptive Fields
    description = forms.CharField(
        label="Physical Description",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Physical appearance, mannerisms, notable features...",
            }
        ),
    )

    public_info = forms.CharField(
        label="Public Information",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "What players/characters generally know about this NPC...",
            }
        ),
    )

    st_notes = forms.CharField(
        label="Storyteller Notes",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Private notes for the Storyteller (motivations, secrets, plot hooks)...",
            }
        ),
    )

    notes = forms.CharField(
        label="General Notes",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Additional notes about this NPC...",
            }
        ),
    )

    # Image
    image = forms.ImageField(
        label="Portrait Image",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}),
    )

    # ========================================
    # Character Type-Specific Fields
    # ========================================

    # Mage-specific fields
    mage_affiliation = forms.ModelChoiceField(
        queryset=MageFaction.objects.filter(parent__isnull=True),
        label="Affiliation",
        required=False,
        empty_label="-- Select Affiliation --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    mage_faction = forms.ModelChoiceField(
        queryset=MageFaction.objects.none(),
        label="Faction",
        required=False,
        empty_label="-- Select Faction --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    mage_subfaction = forms.ModelChoiceField(
        queryset=MageFaction.objects.none(),
        label="Subfaction",
        required=False,
        empty_label="-- Select Subfaction --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    mage_essence = forms.ChoiceField(
        choices=[("", "-- Select Essence --")]
        + [
            ("Dynamic", "Dynamic"),
            ("Pattern", "Pattern"),
            ("Primordial", "Primordial"),
            ("Questing", "Questing"),
        ],
        label="Essence",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Werewolf-specific fields
    werewolf_tribe = forms.ModelChoiceField(
        queryset=Tribe.objects.all(),
        label="Tribe",
        required=False,
        empty_label="-- Select Tribe --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    werewolf_breed = forms.ChoiceField(
        choices=[("", "-- Select Breed --")]
        + [
            ("homid", "Homid"),
            ("metis", "Metis"),
            ("lupus", "Lupus"),
        ],
        label="Breed",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    werewolf_auspice = forms.ChoiceField(
        choices=[("", "-- Select Auspice --")]
        + [
            ("ragabash", "Ragabash"),
            ("theurge", "Theurge"),
            ("philodox", "Philodox"),
            ("galliard", "Galliard"),
            ("ahroun", "Ahroun"),
        ],
        label="Auspice",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Kinfolk-specific fields (breed and tribe, no auspice)
    kinfolk_tribe = forms.ModelChoiceField(
        queryset=Tribe.objects.all(),
        label="Tribe",
        required=False,
        empty_label="-- Select Tribe --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    kinfolk_breed = forms.ChoiceField(
        choices=[("", "-- Select Breed --")]
        + [
            ("homid", "Homid"),
            ("lupus", "Lupus"),
        ],
        label="Breed",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Wraith-specific fields
    wraith_guild = forms.ModelChoiceField(
        queryset=Guild.objects.all(),
        label="Guild",
        required=False,
        empty_label="-- Select Guild --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    wraith_legion = forms.ModelChoiceField(
        queryset=WraithFaction.objects.filter(faction_type="legion"),
        label="Legion",
        required=False,
        empty_label="-- Select Legion --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    wraith_faction = forms.ModelChoiceField(
        queryset=WraithFaction.objects.filter(faction_type="faction"),
        label="Faction",
        required=False,
        empty_label="-- Select Faction --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    wraith_character_type = forms.ChoiceField(
        choices=[("", "-- Select Type --")]
        + [
            ("wraith", "Wraith"),
            ("spectre", "Spectre"),
            ("doppelganger", "Doppelganger"),
            ("chosen", "Chosen"),
            ("dark_spirit", "Dark Spirit"),
            ("risen", "Risen"),
        ],
        label="Wraith Type",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Changeling-specific fields
    changeling_kith = forms.ModelChoiceField(
        queryset=Kith.objects.all(),
        label="Kith",
        required=False,
        empty_label="-- Select Kith --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    changeling_house = forms.ModelChoiceField(
        queryset=House.objects.all(),
        label="House",
        required=False,
        empty_label="-- Select House --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    changeling_court = forms.ChoiceField(
        choices=[
            ("", "-- Select Court --"),
            ("seelie", "Seelie"),
            ("unseelie", "Unseelie"),
        ],
        label="Court",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    changeling_seeming = forms.ChoiceField(
        choices=[("", "-- Select Seeming --")]
        + [
            ("childling", "Childling"),
            ("wilder", "Wilder"),
            ("grump", "Grump"),
        ],
        label="Seeming",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Sorcerer-specific fields
    sorcerer_fellowship = forms.ModelChoiceField(
        queryset=SorcererFellowship.objects.all(),
        label="Fellowship",
        required=False,
        empty_label="-- Select Fellowship --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Thrall-specific fields
    thrall_master = forms.ModelChoiceField(
        queryset=Demon.objects.all(),
        label="Master Demon",
        required=False,
        empty_label="-- Select Master Demon --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Demon-specific fields
    demon_house = forms.ModelChoiceField(
        queryset=DemonHouse.objects.all(),
        label="House",
        required=False,
        empty_label="-- Select House --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    demon_faction = forms.ModelChoiceField(
        queryset=DemonFaction.objects.all(),
        label="Faction",
        required=False,
        empty_label="-- Select Faction --",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.related_character = kwargs.pop("related_character", None)
        super().__init__(*args, **kwargs)

        # Pre-populate chronicle if related character exists
        if self.related_character and self.related_character.chronicle:
            self.fields["chronicle"].initial = self.related_character.chronicle

    def clean_npc_type(self):
        npc_type = self.cleaned_data.get("npc_type")
        if npc_type not in self.NPC_CLASSES:
            raise forms.ValidationError("Invalid NPC type selected.")
        return npc_type

    def save(self, commit=True):
        """Create the NPC character instance."""
        npc_type = self.cleaned_data["npc_type"]
        npc_class = self.NPC_CLASSES[npc_type]

        # Build notes with role information
        notes_parts = []

        if self.cleaned_data.get("npc_role"):
            role_display = dict(self.NPC_ROLE_CHOICES).get(
                self.cleaned_data["npc_role"], self.cleaned_data["npc_role"]
            )
            notes_parts.append(f"Role: {role_display}")

        if self.related_character:
            notes_parts.append(f"Related to: {self.related_character.name}")

        if self.cleaned_data.get("notes"):
            notes_parts.append(self.cleaned_data["notes"])

        combined_notes = "\n".join(notes_parts)

        # Create the NPC instance
        npc = npc_class(
            name=self.cleaned_data["name"],
            concept=self.cleaned_data["concept"],
            npc=True,
            status="Un",
        )

        # Set optional fields
        if self.cleaned_data.get("chronicle"):
            npc.chronicle = self.cleaned_data["chronicle"]

        if self.cleaned_data.get("description"):
            npc.description = self.cleaned_data["description"]

        if self.cleaned_data.get("public_info"):
            npc.public_info = self.cleaned_data["public_info"]

        if self.cleaned_data.get("st_notes"):
            npc.st_notes = self.cleaned_data["st_notes"]

        if combined_notes:
            npc.notes = combined_notes

        if self.cleaned_data.get("image"):
            npc.image = self.cleaned_data["image"]

        if self.user:
            npc.owner = self.user

        # Set character type-specific fields
        if npc_type == "mage":
            if self.cleaned_data.get("mage_affiliation"):
                npc.affiliation = self.cleaned_data["mage_affiliation"]
            if self.cleaned_data.get("mage_faction"):
                npc.faction = self.cleaned_data["mage_faction"]
            if self.cleaned_data.get("mage_subfaction"):
                npc.subfaction = self.cleaned_data["mage_subfaction"]
            if self.cleaned_data.get("mage_essence"):
                npc.essence = self.cleaned_data["mage_essence"]

        elif npc_type == "werewolf":
            if self.cleaned_data.get("werewolf_tribe"):
                npc.tribe = self.cleaned_data["werewolf_tribe"]
            if self.cleaned_data.get("werewolf_breed"):
                npc.breed = self.cleaned_data["werewolf_breed"]
            if self.cleaned_data.get("werewolf_auspice"):
                npc.auspice = self.cleaned_data["werewolf_auspice"]

        elif npc_type == "kinfolk":
            if self.cleaned_data.get("kinfolk_tribe"):
                npc.tribe = self.cleaned_data["kinfolk_tribe"]
            if self.cleaned_data.get("kinfolk_breed"):
                npc.breed = self.cleaned_data["kinfolk_breed"]

        elif npc_type == "wraith":
            if self.cleaned_data.get("wraith_guild"):
                npc.guild = self.cleaned_data["wraith_guild"]
            if self.cleaned_data.get("wraith_legion"):
                npc.legion = self.cleaned_data["wraith_legion"]
            if self.cleaned_data.get("wraith_faction"):
                npc.faction = self.cleaned_data["wraith_faction"]
            if self.cleaned_data.get("wraith_character_type"):
                npc.character_type = self.cleaned_data["wraith_character_type"]

        elif npc_type == "changeling":
            if self.cleaned_data.get("changeling_kith"):
                npc.kith = self.cleaned_data["changeling_kith"]
            if self.cleaned_data.get("changeling_house"):
                npc.house = self.cleaned_data["changeling_house"]
            if self.cleaned_data.get("changeling_court"):
                npc.court = self.cleaned_data["changeling_court"]
            if self.cleaned_data.get("changeling_seeming"):
                npc.seeming = self.cleaned_data["changeling_seeming"]

        elif npc_type == "sorcerer":
            if self.cleaned_data.get("sorcerer_fellowship"):
                npc.fellowship = self.cleaned_data["sorcerer_fellowship"]

        elif npc_type == "thrall":
            if self.cleaned_data.get("thrall_master"):
                npc.master = self.cleaned_data["thrall_master"]

        elif npc_type == "demon":
            if self.cleaned_data.get("demon_house"):
                npc.house = self.cleaned_data["demon_house"]
            if self.cleaned_data.get("demon_faction"):
                npc.faction = self.cleaned_data["demon_faction"]

        if commit:
            npc.save()

        return npc
