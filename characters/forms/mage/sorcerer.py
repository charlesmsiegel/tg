"""Forms for Sorcerer character type."""

from characters.models.core.archetype import Archetype
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.sorcerer import LinearMagicPath, Sorcerer
from django import forms
from game.models import Chronicle
from widgets import ChainedChoiceField, ChainedSelectMixin


class SorcererBasicsForm(ChainedSelectMixin, forms.ModelForm):
    """Form for Sorcerer character creation basics step."""

    fellowship = ChainedChoiceField(
        choices=[],
        label="Fellowship",
        required=False,
    )
    casting_attribute = ChainedChoiceField(
        parent_field="fellowship",
        choices_map={},
        label="Casting Attribute",
        required=False,
    )
    affinity_path = ChainedChoiceField(
        parent_field="fellowship",
        choices_map={},
        label="Affinity Path",
        required=False,
    )

    class Meta:
        model = Sorcerer
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "fellowship",
            "affinity_path",
            "casting_attribute",
            "sorcerer_type",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up basic field querysets
        self.fields["nature"].queryset = Archetype.objects.all().order_by("name")
        self.fields["demeanor"].queryset = Archetype.objects.all().order_by("name")
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["image"].required = False

        # Build fellowship choices
        fellowships = SorcererFellowship.objects.all().order_by("name")
        fellowship_choices = [("", "---------")] + [(str(f.pk), str(f)) for f in fellowships]
        self.fields["fellowship"].choices = fellowship_choices

        # Build choices_map for casting_attribute (fellowship → attributes)
        attr_choices_map = {}
        for fellowship in fellowships:
            attrs = fellowship.favored_attributes.all()
            attr_choices_map[str(fellowship.pk)] = [(str(a.pk), str(a)) for a in attrs]
        self.fields["casting_attribute"].choices_map = attr_choices_map

        # Build choices_map for affinity_path (fellowship → paths)
        path_choices_map = {}
        for fellowship in fellowships:
            paths = fellowship.favored_paths.all()
            path_choices_map[str(fellowship.pk)] = [(str(p.pk), str(p)) for p in paths]
        self.fields["affinity_path"].choices_map = path_choices_map

        # Re-run chain setup after choices are configured
        self._setup_chains()


class SorcererForm(forms.ModelForm):
    """Full edit form for Sorcerer characters (ST use)."""

    class Meta:
        model = Sorcerer
        fields = [
            # Basic Information
            "name",
            "owner",
            "chronicle",
            "nature",
            "demeanor",
            "concept",
            "npc",
            "status",
            # Sorcerer-specific
            "fellowship",
            "sorcerer_type",
            "affinity_path",
            "casting_attribute",
            "quintessence",
            # Attributes
            "strength",
            "dexterity",
            "stamina",
            "perception",
            "intelligence",
            "wits",
            "charisma",
            "manipulation",
            "appearance",
            # Abilities - Primary
            "alertness",
            "athletics",
            "brawl",
            "empathy",
            "expression",
            "intimidation",
            "streetwise",
            "subterfuge",
            "awareness",
            "art",
            "leadership",
            "crafts",
            "drive",
            "etiquette",
            "firearms",
            "melee",
            "stealth",
            "larceny",
            "meditation",
            "research",
            "survival",
            "technology",
            "academics",
            "computer",
            "investigation",
            "medicine",
            "science",
            "cosmology",
            "enigmas",
            "finance",
            "law",
            "occult",
            "politics",
            # Secondary Abilities
            "animal_kinship",
            "blatancy",
            "carousing",
            "flying",
            "high_ritual",
            "lucid_dreaming",
            "search",
            "seduction",
            "cooking",
            "diplomacy",
            "instruction",
            "intrigue",
            "intuition",
            "mimicry",
            "negotiation",
            "newspeak",
            "scan",
            "scrounging",
            "style",
            "acrobatics",
            "archery",
            "biotech",
            "energy_weapons",
            "jetpack",
            "riding",
            "torture",
            "blind_fighting",
            "climbing",
            "disguise",
            "elusion",
            "escapology",
            "fast_draw",
            "fast_talk",
            "fencing",
            "fortune_telling",
            "gambling",
            "gunsmith",
            "heavy_weapons",
            "hunting",
            "hypnotism",
            "jury_rigging",
            "microgravity_operations",
            "misdirection",
            "networking",
            "pilot",
            "psychology",
            "security",
            "speed_reading",
            "swimming",
            "area_knowledge",
            "belief_systems",
            "cryptography",
            "demolitions",
            "lore",
            "media",
            "pharmacopeia",
            "conspiracy_theory",
            "chantry_politics",
            "covert_culture",
            "cultural_savvy",
            "helmsman",
            "history_knowledge",
            "power_brokering",
            "propaganda",
            "theology",
            "unconventional_warface",
            "vice",
            # Advantages
            "willpower",
            # Appearance
            "age",
            "apparent_age",
            "date_of_birth",
            "description",
            # History
            "history",
            "goals",
            "notes",
            "public_info",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Physical description..."}
            ),
            "history": forms.Textarea(attrs={"rows": 6, "placeholder": "Character history..."}),
            "goals": forms.Textarea(attrs={"rows": 4, "placeholder": "Character goals..."}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Private notes (ST only)..."}),
            "public_info": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Publicly visible information..."}
            ),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter fellowship based on sorcerer type if instance exists
        if self.instance and self.instance.pk:
            self.fields["fellowship"].queryset = SorcererFellowship.objects.all().order_by("name")
            if self.instance.sorcerer_type == "hedge_mage":
                self.fields["affinity_path"].queryset = LinearMagicPath.objects.filter(
                    numina_type="hedge_magic"
                ).order_by("name")
            else:
                self.fields["affinity_path"].queryset = LinearMagicPath.objects.filter(
                    numina_type="psychic"
                ).order_by("name")
        else:
            self.fields["fellowship"].queryset = SorcererFellowship.objects.all().order_by("name")
            self.fields["affinity_path"].queryset = LinearMagicPath.objects.all().order_by("name")
