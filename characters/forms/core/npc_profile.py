from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.thrall import Thrall
from characters.models.mage.companion import Companion
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.wtahuman import WtAHuman
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
        ("Vampire", (
            ("vtm_human", "Human (Vampire)"),
        )),
        ("Werewolf", (
            ("wta_human", "Human (Werewolf)"),
            ("kinfolk", "Kinfolk"),
            ("fomor", "Fomor"),
            ("werewolf", "Werewolf"),
            ("spirit", "Spirit"),
        )),
        ("Mage", (
            ("mta_human", "Human (Mage)"),
            ("sorcerer", "Sorcerer"),
            ("companion", "Companion"),
            ("mage", "Mage"),
        )),
        ("Wraith", (
            ("wto_human", "Human (Wraith)"),
            ("wraith", "Wraith"),
        )),
        ("Changeling", (
            ("ctd_human", "Human (Changeling)"),
            ("changeling", "Changeling"),
        )),
        ("Demon", (
            ("dtf_human", "Human (Demon)"),
            ("thrall", "Thrall"),
            ("demon", "Demon"),
        )),
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
        "spirit": SpiritCharacter,
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

        if commit:
            npc.save()

        return npc
