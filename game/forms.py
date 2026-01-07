from characters.models.core import CharacterModel
from core.constants import GameLine, XPApprovalStatus
from django import forms
from django.db import transaction
from game.models import (
    Chronicle,
    FreebieSpendingRecord,
    ObjectType,
    Scene,
    Story,
    StoryXPRequest,
    STRelationship,
    WeeklyXPRequest,
    XPSpendingRequest,
)
from locations.models.core import LocationModel
from widgets import ChainedChoiceField, ChainedSelectMixin


class SceneCreationForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Scene Title"})
    )
    location = forms.ModelChoiceField(
        queryset=LocationModel.objects.order_by("name"), empty_label="Select Location"
    )
    date_of_scene = forms.CharField(max_length=100, widget=forms.DateInput(attrs={"type": "date"}))
    gameline = forms.ChoiceField(
        choices=GameLine.CHOICES,
        initial=GameLine.WOD,
    )

    # Mapping from Gameline model names to GameLine choice codes
    GAMELINE_NAME_TO_CODE = {
        "World of Darkness": GameLine.WOD,
        "Vampire: the Masquerade": GameLine.VTM,
        "Werewolf: the Apocalypse": GameLine.WTA,
        "Mage: the Ascension": GameLine.MTA,
        "Wraith: the Oblivion": GameLine.WTO,
        "Changeling: the Dreaming": GameLine.CTD,
        "Demon: the Fallen": GameLine.DTF,
        "Hunter: the Reckoning": GameLine.HTR,
        "Mummy: the Resurrection": GameLine.MTR,
    }

    def __init__(self, *args, **kwargs):
        chronicle = kwargs.pop("chronicle")
        super().__init__(*args, **kwargs)
        self.fields["location"].queryset = LocationModel.objects.filter(
            chronicle=chronicle
        ).order_by("name")

        # Filter gameline choices to only those with STs for this chronicle
        from game.models import STRelationship

        st_gamelines = STRelationship.objects.filter(chronicle=chronicle).values_list(
            "gameline__name", flat=True
        )
        allowed_codes = {
            self.GAMELINE_NAME_TO_CODE.get(name)
            for name in st_gamelines
            if name in self.GAMELINE_NAME_TO_CODE
        }

        if allowed_codes:
            self.fields["gameline"].choices = [
                (code, label) for code, label in GameLine.CHOICES if code in allowed_codes
            ]
            # Set default to first available gameline if WOD is not available
            if GameLine.WOD not in allowed_codes:
                self.fields["gameline"].initial = self.fields["gameline"].choices[0][0]


class ChronicleObjectCreationFormBase(ChainedSelectMixin, forms.Form):
    """Base class for chronicle-aware object creation forms."""

    # Mapping from Gameline model names to GameLine choice codes
    GAMELINE_NAME_TO_CODE = {
        "World of Darkness": GameLine.WOD,
        "Vampire: the Masquerade": GameLine.VTM,
        "Werewolf: the Apocalypse": GameLine.WTA,
        "Mage: the Ascension": GameLine.MTA,
        "Wraith: the Oblivion": GameLine.WTO,
        "Changeling: the Dreaming": GameLine.CTD,
        "Demon: the Fallen": GameLine.DTF,
        "Hunter: the Reckoning": GameLine.HTR,
        "Mummy: the Resurrection": GameLine.MTR,
    }

    # Subclasses must define these
    object_type_code = None  # 'char', 'loc', or 'obj'
    type_field_name = None  # 'char_type', 'loc_type', or 'item_type'

    gameline = ChainedChoiceField(choices=[], label="Game Line")
    # type field is added dynamically in subclasses

    def _format_label(self, name):
        """Format type labels with special handling."""
        # Mapping of gameline prefixes to full names for humans
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

    def _get_st_gameline_codes(self, chronicle):
        """Get the set of gameline codes that have STs for this chronicle."""
        st_gamelines = STRelationship.objects.filter(chronicle=chronicle).values_list(
            "gameline__name", flat=True
        )
        return {
            self.GAMELINE_NAME_TO_CODE.get(name)
            for name in st_gamelines
            if name in self.GAMELINE_NAME_TO_CODE
        }

    def _get_allowed_type_names(self, chronicle):
        """Get allowed object type names from chronicle's allowed_objects."""
        return set(
            chronicle.allowed_objects.filter(type=self.object_type_code).values_list(
                "name", flat=True
            )
        )

    def _build_choices(self, chronicle, user, excluded_types=None):
        """Build gameline and type choices based on permissions.

        Returns tuple of (gameline_choices, choices_map) where choices_map
        is in format suitable for ChainedChoiceField.
        """
        excluded_types = excluded_types or []
        is_privileged = user.is_staff or user.profile.is_st()

        # Get all object types for this category
        all_types = ObjectType.objects.filter(type=self.object_type_code).exclude(
            name__in=excluded_types
        )

        if is_privileged:
            # STs and admins can create anything
            allowed_gamelines = {obj.gameline for obj in all_types}
            allowed_type_names = {obj.name for obj in all_types}
        else:
            # Regular users: filter by ST gamelines and allowed_objects
            allowed_gamelines = self._get_st_gameline_codes(chronicle)
            allowed_type_names = self._get_allowed_type_names(chronicle)

        # Build gameline choices
        gameline_choices = [
            (code, label) for code, label in GameLine.CHOICES if code in allowed_gamelines
        ]

        # Build choices_map for ChainedChoiceField
        choices_map = {}
        for obj in all_types:
            if obj.gameline in allowed_gamelines and obj.name in allowed_type_names:
                if obj.gameline not in choices_map:
                    choices_map[obj.gameline] = []
                choices_map[obj.gameline].append((obj.name, self._format_label(obj.name)))

        # Sort each gameline's types
        for gameline in choices_map:
            choices_map[gameline].sort(key=lambda x: x[1])

        return gameline_choices, choices_map


class ChronicleCharacterCreationForm(ChronicleObjectCreationFormBase):
    """Character creation form filtered by chronicle's allowed_objects and ST gamelines."""

    object_type_code = "char"
    type_field_name = "char_type"

    char_type = ChainedChoiceField(
        parent_field="gameline",
        choices_map={},
        label="Character Type",
    )

    # Group types and non-character types to exclude
    EXCLUDED_TYPES = [
        # Groups
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
        chronicle = kwargs.pop("chronicle")
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        gameline_choices, choices_map = self._build_choices(chronicle, user, self.EXCLUDED_TYPES)

        self.fields["gameline"].choices = gameline_choices
        self.fields["char_type"].choices_map = choices_map

        # Re-run chain setup after choices are configured
        self._setup_chains()


class ChronicleLocationCreationForm(ChronicleObjectCreationFormBase):
    """Location creation form filtered by chronicle's allowed_objects and ST gamelines."""

    object_type_code = "loc"
    type_field_name = "loc_type"

    loc_type = ChainedChoiceField(
        parent_field="gameline",
        choices_map={},
        label="Location Type",
    )

    def __init__(self, *args, **kwargs):
        chronicle = kwargs.pop("chronicle")
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        gameline_choices, choices_map = self._build_choices(chronicle, user)

        self.fields["gameline"].choices = gameline_choices
        self.fields["loc_type"].choices_map = choices_map

        # Re-run chain setup after choices are configured
        self._setup_chains()


class ChronicleItemCreationForm(ChronicleObjectCreationFormBase):
    """Item creation form filtered by chronicle's allowed_objects and ST gamelines."""

    object_type_code = "obj"
    type_field_name = "item_type"

    item_type = ChainedChoiceField(
        parent_field="gameline",
        choices_map={},
        label="Item Type",
    )

    def __init__(self, *args, **kwargs):
        chronicle = kwargs.pop("chronicle")
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        gameline_choices, choices_map = self._build_choices(chronicle, user)

        self.fields["gameline"].choices = gameline_choices
        self.fields["item_type"].choices_map = choices_map

        # Re-run chain setup after choices are configured
        self._setup_chains()


class AddCharForm(forms.Form):
    character_to_add = forms.ModelChoiceField(
        queryset=CharacterModel.objects.none(), empty_label="Add Character"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        scene = kwargs.pop("scene")
        super().__init__(*args, **kwargs)
        self.fields["character_to_add"].queryset = CharacterModel.objects.filter(
            owner=user, chronicle=scene.chronicle
        ).exclude(pk__in=scene.characters.all())


class PostForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=CharacterModel.objects.none(), empty_label="Character Select"
    )
    display_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Display Name (Optional)", "rows": 1, "cols": 25}
        ),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message"}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        scene = kwargs.pop("scene")
        super().__init__(*args, **kwargs)
        self.fields["character"].queryset = CharacterModel.objects.filter(
            owner=user,
            chronicle=scene.chronicle,
            pk__in=scene.characters.all(),
        )

    def clean(self):
        cleaned_data = super().clean()

        if "character" in self.errors.keys():
            del self.errors["character"]

        message = cleaned_data.get("message")

        # Validate the message content (example: no prohibited words or empty message)
        if not message or len(message.strip()) == 0:
            raise forms.ValidationError("The message cannot be empty.")
        return cleaned_data


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Story Name"})


class JournalEntryForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message"}))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"placeholder": "Journal Entry"})

    def save(self, commit=True):
        return self.instance.add_post(self.cleaned_data["date"], self.cleaned_data["message"])


class STResponseForm(forms.Form):
    st_message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message"}))

    def __init__(self, *args, **kwargs):
        self.entry = kwargs.pop("entry")
        super().__init__(*args, **kwargs)
        self.fields["st_message"].widget.attrs.update({"placeholder": "Journal Response"})

    def save(self, commit=True):
        self.entry.st_message = self.cleaned_data["st_message"]
        self.entry.save()


class WeeklyXPRequestForm(forms.ModelForm):
    class Meta:
        model = WeeklyXPRequest
        fields = [
            "finishing",
            "learning",
            "rp",
            "focus",
            "standingout",
            "learning_scene",
            "rp_scene",
            "focus_scene",
            "standingout_scene",
        ]

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        self.week = kwargs.pop("week", None)
        super().__init__(*args, **kwargs)
        self.fields["learning_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["rp_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["focus_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["standingout_scene"].queryset = (
            self.week.finished_scenes().filter(characters=self.character) if self.week else None
        )
        self.fields["finishing"].required = False
        self.fields["learning_scene"].required = False
        self.fields["rp_scene"].required = False
        self.fields["focus_scene"].required = False
        self.fields["standingout_scene"].required = False

    def player_save(self, commit=True):
        if not self.instance.pk:
            self.instance = super().save(commit=False)
        self.instance.finishing = True
        self.instance.week = self.week
        self.instance.character = self.character
        if commit:
            self.instance.save()
        return self.instance

    @transaction.atomic
    def st_save(self, commit=True):
        """Approve the XP request and award XP to the character atomically."""
        # Directly modify the instance bound to the form
        self.instance.approved = True
        self.instance.finishing = self.cleaned_data["finishing"]
        self.instance.learning = self.cleaned_data["learning"]
        self.instance.rp = self.cleaned_data["rp"]
        self.instance.focus = self.cleaned_data["focus"]
        self.instance.standingout = self.cleaned_data["standingout"]

        # Update character XP based on the form fields
        xp_increase = sum(
            [
                self.instance.finishing,
                self.instance.learning,
                self.instance.rp,
                self.instance.focus,
                self.instance.standingout,
            ]
        )
        self.character.xp += xp_increase
        self.character.save()

        if commit:
            self.instance.save()
        return self.instance

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["learning"]:
            if cleaned_data["learning_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        if cleaned_data["rp"]:
            if cleaned_data["rp_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        if cleaned_data["focus"]:
            if cleaned_data["focus_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        if cleaned_data["standingout"]:
            if cleaned_data["standingout_scene"] is None:
                raise forms.ValidationError("Must include scene for any XP claimed")
        return cleaned_data


class XPSpendingRequestForm(forms.ModelForm):
    """Form for creating and updating XP spending requests."""

    class Meta:
        model = XPSpendingRequest
        fields = ["trait_name", "trait_type", "trait_value", "cost"]

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        super().__init__(*args, **kwargs)
        # Add help text placeholders
        self.fields["trait_name"].widget.attrs.update({"placeholder": "e.g., Strength"})
        self.fields["trait_type"].widget.attrs.update({"placeholder": "e.g., Attribute"})
        self.fields["trait_value"].widget.attrs.update({"placeholder": "New value"})
        self.fields["cost"].widget.attrs.update({"placeholder": "XP cost"})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.character:
            instance.character = self.character
        if commit:
            instance.save()
        return instance


class XPSpendingRequestApprovalForm(forms.ModelForm):
    """Form for STs to approve/deny XP spending requests."""

    class Meta:
        model = XPSpendingRequest
        fields = ["approved"]
        widgets = {
            "approved": forms.Select(choices=XPApprovalStatus.CHOICES),
        }


class FreebieSpendingRecordForm(forms.ModelForm):
    """Form for creating and updating freebie spending records."""

    class Meta:
        model = FreebieSpendingRecord
        fields = ["trait_name", "trait_type", "trait_value", "cost"]

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        super().__init__(*args, **kwargs)
        self.fields["trait_name"].widget.attrs.update({"placeholder": "e.g., Strength"})
        self.fields["trait_type"].widget.attrs.update({"placeholder": "e.g., Attribute"})
        self.fields["trait_value"].widget.attrs.update({"placeholder": "Value gained"})
        self.fields["cost"].widget.attrs.update({"placeholder": "Freebie cost"})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.character:
            instance.character = self.character
        if commit:
            instance.save()
        return instance


class StoryXPRequestForm(forms.ModelForm):
    """Form for creating and updating story XP requests."""

    class Meta:
        model = StoryXPRequest
        fields = ["story", "success", "danger", "growth", "drama", "duration"]

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.character:
            instance.character = self.character
        if commit:
            instance.save()
        return instance


class ChronicleForm(forms.ModelForm):
    """Form for creating and updating chronicles."""

    class Meta:
        model = Chronicle
        fields = ["name", "head_st", "theme", "mood", "year", "headings"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Chronicle Name"})
        self.fields["theme"].widget.attrs.update({"placeholder": "Chronicle Theme (optional)"})
        self.fields["mood"].widget.attrs.update({"placeholder": "Chronicle Mood (optional)"})
        self.fields["year"].widget.attrs.update({"placeholder": "In-game year"})


class SceneForm(forms.ModelForm):
    """Form for updating scene details."""

    class Meta:
        model = Scene
        fields = ["name", "location", "date_of_scene", "gameline", "finished", "xp_given"]
        widgets = {
            "date_of_scene": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.chronicle = kwargs.pop("chronicle", None)
        super().__init__(*args, **kwargs)
        # Filter location by chronicle if available
        if self.chronicle:
            self.fields["location"].queryset = LocationModel.objects.filter(
                chronicle=self.chronicle
            ).order_by("name")
        elif self.instance and self.instance.chronicle:
            self.fields["location"].queryset = LocationModel.objects.filter(
                chronicle=self.instance.chronicle
            ).order_by("name")
