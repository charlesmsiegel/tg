from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Q

from characters.forms.core.xp import XPForm
from characters.forms.mage.xp import MageXPForm
from characters.models.core import CharacterModel
from characters.models.mage.mage import Mage
from core.constants import GameLine, XPApprovalStatus
from core.permissions import PermissionManager
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
from game.security import staffed_chronicles
from locations.models.core import LocationModel
from widgets import ChainedChoiceField, ChainedSelectMixin


class SceneCreationForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Scene Title"})
    )
    location = forms.ModelChoiceField(
        queryset=LocationModel.objects.order_by("name"), empty_label="Select Location"
    )
    date_of_scene = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
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
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["location"].queryset = LocationModel.objects.filter(
            chronicle=chronicle
        ).order_by("name")

        # Filter gameline choices to only those with STs for this chronicle
        from game.models import STRelationship

        if user is not None and (
            user.is_staff or user.is_superuser or chronicle.head_st_id == user.pk
        ):
            return
        st_gamelines = STRelationship.objects.filter(chronicle=chronicle, user=user).values_list(
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

    def _setup_chains(self):
        if not self.is_bound and not self.initial.get("gameline"):
            first_choice = next(iter(self.fields["gameline"].choices), None)
            if first_choice:
                self.initial["gameline"] = first_choice[0]
        super()._setup_chains()
        # All three creation forms appear on one page, so their chain names and
        # field IDs must be distinct even though they share the same field names.
        chain_name = f"chronicle_{self.object_type_code}"
        for field_name in ("gameline", self.type_field_name):
            widget = self.fields[field_name].widget
            widget.chain_name = chain_name
            widget.attrs["id"] = f"id_{chain_name}_{field_name}"
            widget.attrs.setdefault("class", "tg-form-control tg-form-select")

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
        is_privileged = user.is_staff or user.is_superuser or chronicle.head_st_id == user.pk

        # Get all object types for this category
        all_types = ObjectType.objects.filter(type=self.object_type_code).exclude(
            name__in=excluded_types
        )

        if is_privileged:
            # STs and admins can create anything
            allowed_gamelines = {obj.gameline for obj in all_types}
            allowed_type_names = {obj.name for obj in all_types}
        else:
            assigned = STRelationship.objects.filter(chronicle=chronicle, user=user).values_list(
                "gameline__name", flat=True
            )
            assigned_codes = {
                self.GAMELINE_NAME_TO_CODE[name]
                for name in assigned
                if name in self.GAMELINE_NAME_TO_CODE
            }
            if assigned_codes:
                allowed_gamelines = assigned_codes
                allowed_type_names = {obj.name for obj in all_types}
            else:
                # Players can use only the chronicle's approved type catalogue.
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

        queryset = CharacterModel.objects.filter(chronicle=scene.chronicle)
        if not PermissionManager.can_manage_scope(user, scene.chronicle, scene.gameline):
            queryset = queryset.filter(owner=user)
        self.fields["character_to_add"].queryset = queryset.exclude(pk__in=scene.characters.all())


class PostForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=CharacterModel.objects.none(), empty_label="Character Select", required=False
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
        self.user = kwargs.pop("user")
        self.scene = kwargs.pop("scene")
        super().__init__(*args, **kwargs)
        self.character_queryset = CharacterModel.objects.filter(
            owner=self.user,
            chronicle=self.scene.chronicle,
            pk__in=self.scene.characters.all(),
        )
        self.fields["character"].queryset = self.character_queryset

    def clean(self):
        cleaned_data = super().clean()
        message = cleaned_data.get("message")

        # Validate the message content
        if not message or len(message.strip()) == 0:
            self.add_error("message", "The message cannot be empty.")

        # Character is required only when user has multiple characters in the scene
        if self.character_queryset.count() > 1 and not cleaned_data.get("character"):
            self.add_error("character", "Please select a character.")

        return cleaned_data


class StoryForm(forms.ModelForm):
    """A chronicle page's "New story": the chronicle comes from the page."""

    class Meta:
        model = Story
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Story Name"})


class StoryEditForm(StoryForm):
    """The standalone story create / edit form, where the chronicle is chosen."""

    class Meta(StoryForm.Meta):
        fields = ("name", "chronicle")

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        chronicle = self.fields["chronicle"]
        chronicle.queryset = staffed_chronicles(user).order_by("name")
        chronicle.empty_label = "Unassigned"
        chronicle.help_text = "The chronicle whose Stories tab lists this story."


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

    def already_filed(self):
        return WeeklyXPRequest.objects.filter(week=self.week, character=self.character).exists()

    def submit(self):
        """File the player's request; None when the week already has one for the character.

        The (week, character) constraint settles a double submit: the losing save fails
        model validation or the insert, and the caller reports the request already filed.
        """
        if self.already_filed():
            return None
        instance = self.player_save(commit=False)
        try:
            with transaction.atomic():
                instance.save()
        except (IntegrityError, ValidationError):
            if self.already_filed():
                return None
            raise
        return instance

    def st_save(self, commit=True):
        """Approve the XP request and award XP to the character.

        Delegates to the model's approve() method for business logic.
        """
        xp_data = {
            "finishing": self.cleaned_data["finishing"],
            "learning": self.cleaned_data["learning"],
            "learning_scene": self.cleaned_data["learning_scene"],
            "rp": self.cleaned_data["rp"],
            "rp_scene": self.cleaned_data["rp_scene"],
            "focus": self.cleaned_data["focus"],
            "focus_scene": self.cleaned_data["focus_scene"],
            "standingout": self.cleaned_data["standingout"],
            "standingout_scene": self.cleaned_data["standingout_scene"],
        }
        self.instance.approve(xp_data=xp_data)
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


class XPSpendingRequestCorrectionForm(forms.ModelForm):
    """A Storyteller's correction to a pending request: what it names, never its cost.

    The cost was deducted when the request was filed and a denial refunds it, so the
    cost stays as filed.
    """

    class Meta:
        model = XPSpendingRequest
        fields = ["trait_name", "trait_type", "trait_value"]


# Trait types the Spend XP page (Spread M8) offers: the rated traits of the character's
# own XP form. Its other categories (image, rotes, tenets, resonance, rote points) keep
# their fields on the character sheet.
XP_SPEND_TRAIT_TYPES = (
    "Attribute",
    "Ability",
    "Background",
    "Willpower",
    "MeritFlaw",
    "Sphere",
    "Arete",
    "Practice",
)
XP_SPEND_TYPE_LABELS = {"MeritFlaw": "Merit or flaw"}
# Trait types without a list of traits to choose from.
XP_SPEND_SINGLE_TRAITS = ("Willpower", "Arete")


class XPSpendFormMixin:
    """Spend XP (Spread M8): trait type, trait and, for merits and flaws, the rating.

    The choices come from the character's own XP form (XPForm, or MageXPForm for a
    mage), which knows which traits the character may raise and can afford. Only the
    chosen trait type's traits (and the chosen merit's ratings) are built, and plain
    selects replace the chained widgets: htmx asks the page again for the fields.
    """

    def __init__(self, *args, character, **kwargs):
        data = args[0] if args else kwargs.get("data")
        source = data if data is not None else (kwargs.get("initial") or {})
        self.selected_category = source.get("category") or ""
        self.selected_example = source.get("example") or ""
        super().__init__(*args, character=character, **kwargs)
        types = [
            (value, XP_SPEND_TYPE_LABELS.get(value, label))
            for value, label in self.fields["category"].choices
            if value in XP_SPEND_TRAIT_TYPES
        ]
        traits = self.fields["example"].choices_map.get(self.selected_category, [])
        ratings = self.fields["value"].choices_map.get(self.selected_example, [])
        self.fields["category"] = forms.ChoiceField(
            label="Trait type", choices=[("", "Choose a trait type")] + types
        )
        self.fields["example"] = forms.ChoiceField(
            label="Trait", required=False, choices=[("", "Choose a trait")] + list(traits)
        )
        self.fields["value"] = forms.ChoiceField(
            label="Rating", required=False, choices=[("", "Choose a rating")] + list(ratings)
        )
        self.fields["note"].label = "Note"
        self.fields["note"].help_text = "For a new background: what it is (optional)."
        for name in ("pooled", "image_field", "resonance"):
            self.fields.pop(name, None)
        self._forget_stale_choices()

    def _forget_stale_choices(self):
        """A trait or rating not on offer for the chosen trait type counts as unchosen.

        Changing the trait type still submits the previous type's trait; it must not
        block Willpower or Arete (which list no traits) or mark the new list invalid.
        """
        if not self.is_bound:
            return
        stale = [
            name
            for name in ("example", "value")
            if self.data.get(name)
            and self.data.get(name) not in {str(value) for value, _ in self.fields[name].choices}
        ]
        if stale:
            self.data = self.data.copy()
            for name in stale:
                self.data.pop(name, None)
            if "example" in stale:
                self.selected_example = ""

    def _build_example_choices_map(self, category_choices):
        chosen = [choice for choice in category_choices if choice[0] == self.selected_category]
        return super()._build_example_choices_map(chosen)

    def _build_value_choices_map(self, example_choices_map):
        chosen = [
            choice
            for choice in example_choices_map.get("MeritFlaw", [])
            if choice[0] == self.selected_example
        ]
        return super()._build_value_choices_map({"MeritFlaw": chosen} if chosen else {})

    @property
    def has_traits(self):
        """Whether the chosen trait type lists traits (Willpower and Arete do not)."""
        return self.selected_category not in XP_SPEND_SINGLE_TRAITS

    def enable_htmx(self, url):
        """Each select asks ``url`` for the fields and preview of the new selection."""
        for name in ("category", "example", "value"):
            self.fields[name].widget.attrs.update(
                {
                    "hx-get": url,
                    # Arrowing through a closed select fires change per step.
                    "hx-trigger": "change delay:200ms",
                    "hx-target": "#xp-spend-fields",
                    "hx-swap": "innerHTML",
                    "hx-sync": "closest form:replace",
                    # The selection only: never the CSRF token.
                    "hx-include": "#xp-spend-fields",
                }
            )

    def quiet(self):
        """Drop validation messages: a preview asks what the selection costs, and an
        unfinished selection is not an error yet. Call after reading is_valid()."""
        self.errors.clear()

    def clean_example(self):
        category = self.cleaned_data.get("category")
        if not self.cleaned_data.get("example"):
            if category and category not in XP_SPEND_SINGLE_TRAITS:
                raise forms.ValidationError("Choose a trait.")
            return None
        return super().clean_example()

    def clean_value(self):
        value = super().clean_value()
        if value is None and self.cleaned_data.get("category") == "MeritFlaw":
            raise forms.ValidationError("Choose a rating.")
        return value


class XPSpendForm(XPSpendFormMixin, XPForm):
    pass


class MageXPSpendForm(XPSpendFormMixin, MageXPForm):
    pass


def xp_spend_form_class(character):
    return MageXPSpendForm if isinstance(character, Mage) else XPSpendForm


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
        character = self.character or (self.instance.character if self.instance.pk else None)
        if character is not None:
            # The character's own chronicle's stories, and those from before stories
            # belonged to a chronicle: never another chronicle's story.
            self.fields["story"].queryset = Story.objects.filter(
                Q(chronicle_id=character.chronicle_id) | Q(chronicle__isnull=True)
            ).order_by("name")

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
        fields = [
            "name",
            "location",
            "date_of_scene",
            "gameline",
            "visibility",
            "finished",
            "xp_given",
        ]
        widgets = {
            "date_of_scene": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.chronicle = kwargs.pop("chronicle", None)
        super().__init__(*args, **kwargs)
        self.fields["visibility"].required = False
        self.fields["visibility"].initial = Scene.Visibility.CHRONICLE
        # Filter location by chronicle if available
        if self.chronicle:
            self.fields["location"].queryset = LocationModel.objects.filter(
                chronicle=self.chronicle
            ).order_by("name")
        elif self.instance and self.instance.chronicle:
            self.fields["location"].queryset = LocationModel.objects.filter(
                chronicle=self.instance.chronicle
            ).order_by("name")

    def clean_visibility(self):
        return self.cleaned_data.get("visibility") or Scene.Visibility.CHRONICLE
