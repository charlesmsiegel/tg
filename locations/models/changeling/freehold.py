from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core import LocationModel


class ArchetypeChoices(models.TextChoices):
    ACADEMY = "academy", "Academy"
    HEARTH = "hearth", "Hearth"
    HOMESTEAD = "homestead", "Homestead"
    MANOR = "manor", "Manor"
    MARKET = "market", "Market"
    REPOSITORY = "repository", "Repository"
    STRONGHOLD = "stronghold", "Stronghold"
    THORPE = "thorpe", "Thorpe"
    WORKSHOP = "workshop", "Workshop"


class PowerChoices(models.TextChoices):
    WARNING_CALL = "warning_call", "Warning Call (•)"
    GLAMOUR_TO_DROSS = "glamour_to_dross", "Glamour to Dross (••)"
    RESONANT_DREAMS = "resonant_dreams", "Resonant Dreams (••)"
    CALL_FORTH_FLAME = "call_forth_flame", "Call Forth the Flame (•••)"
    DUAL_NATURE = "dual_nature", "Dual Nature (•••)"


class HearthAbilityChoices(models.TextChoices):
    LEADERSHIP = "leadership", "Leadership"
    SOCIALIZE = "socialize", "Socialize"


class Freehold(LocationModel):
    """
    A Freehold - a constructed place between the Dreaming and the Autumn World
    where changelings work, socialize, hold court, and take refuge from Banality.

    Based on Book of Freeholds for Changeling: The Dreaming 20th Anniversary Edition.
    """

    type = "freehold"
    gameline = "ctd"

    # Core archetype
    archetype = models.CharField(
        max_length=20,
        choices=ArchetypeChoices.choices,
        default=ArchetypeChoices.HEARTH,
        help_text="The role this freehold plays in changeling society",
    )

    # Aspect - the story/theme of the freehold
    aspect = models.TextField(
        blank=True,
        help_text="The underlying dream or story of this freehold (e.g., 'birthplace of chimerical creatures')",
    )

    # Quirks - unique features
    quirks = models.TextField(
        blank=True,
        help_text="Unique features or oddities of this freehold that don't match holders' desires",
    )

    # Ratings (0-5 dots)
    balefire = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Rating of the balefire, determines Glamour/dross generation (0-5 dots)",
    )

    size = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Physical size of the freehold (0-5 dots)",
    )

    sanctuary = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Defense rating, grants bonus dice for defense and threshold (0-5 dots)",
    )

    resources = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Mundane or chimerical resources generated (0-5 dots)",
    )

    passages = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Number of trods/raths connected to this freehold (one free, additional cost 1 feature point each)",
    )

    # Powers - stored as JSON array of power choices
    powers = models.JSONField(
        default=list,
        blank=True,
        help_text="List of special powers this freehold possesses",
    )

    # Archetype-specific fields
    # Academy - associated ability
    academy_ability = models.CharField(
        max_length=50,
        blank=True,
        help_text="The Ability this Academy teaches as its specialty (for Academy archetype)",
    )

    # Hearth - Leadership or Socialize choice
    hearth_ability = models.CharField(
        max_length=20,
        choices=HearthAbilityChoices.choices,
        blank=True,
        help_text="Which ability Hearth grants bonus to (for Hearth archetype)",
    )

    # Dual Nature - second archetype
    dual_nature_archetype = models.CharField(
        max_length=20,
        choices=ArchetypeChoices.choices,
        blank=True,
        help_text="Second archetype if Dual Nature power is taken",
    )

    dual_nature_ability = models.CharField(
        max_length=50,
        blank=True,
        help_text="Associated ability for dual nature archetype if applicable",
    )

    # Resource details
    resource_description = models.TextField(
        blank=True, help_text="Description of what resources this freehold generates"
    )

    # Passage details
    passage_description = models.TextField(
        blank=True, help_text="Description of trods/raths and where they lead"
    )

    # Balefire appearance
    balefire_description = models.TextField(
        blank=True,
        help_text="Description of what the balefire looks like and where it's located",
    )

    # Multi-step creation tracking
    # 0 = not started, 1 = basics done, 2 = features done, 3 = powers done, 4 = details done, 5 = complete
    # Similar to character creation_status

    class Meta:
        verbose_name = "Freehold"
        verbose_name_plural = "Freeholds"
        constraints = [
            CheckConstraint(
                check=Q(balefire__gte=0, balefire__lte=5),
                name="locations_freehold_balefire_range",
                violation_error_message="Balefire rating must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(size__gte=0, size__lte=5),
                name="locations_freehold_size_range",
                violation_error_message="Size rating must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(sanctuary__gte=0, sanctuary__lte=5),
                name="locations_freehold_sanctuary_range",
                violation_error_message="Sanctuary rating must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(resources__gte=0, resources__lte=5),
                name="locations_freehold_resources_range",
                violation_error_message="Resources rating must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(passages__gte=0, passages__lte=20),
                name="locations_freehold_passages_range",
                violation_error_message="Passages must be between 0 and 20",
            ),
        ]

    def get_absolute_url(self):
        return reverse("locations:changeling:freehold", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:changeling:update:freehold", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:changeling:create:freehold")

    def get_archetype_display_with_benefit(self):
        """Returns archetype with its mechanical benefit"""
        benefits = {
            "academy": f"-2 difficulty on {self.academy_ability or '[Ability]'}",
            "hearth": f"-2 difficulty on {self.get_hearth_ability_display() if self.hearth_ability else 'Leadership/Socialize'}",
            "homestead": "-2 difficulty on Survival or Animal Ken",
            "manor": "-2 difficulty on Etiquette",
            "market": "-2 difficulty on Persuasion or Subterfuge",
            "repository": "-2 difficulty on Lore",
            "stronghold": "-2 difficulty on Firearms or Melee",
            "thorpe": "-2 difficulty on Empathy",
            "workshop": "-2 difficulty on Craft",
        }
        archetype_name = self.get_archetype_display()
        benefit = benefits.get(self.archetype, "")
        if benefit:
            return f"{archetype_name} ({benefit})"
        return archetype_name

    def get_total_feature_points(self):
        """Calculate total feature points spent"""
        total = self.balefire + self.size + self.sanctuary + self.resources
        # Passages: first is free, rest cost 1 each
        if self.passages > 1:
            total += self.passages - 1

        # Powers
        power_costs = {
            "warning_call": 1,
            "glamour_to_dross": 2,
            "resonant_dreams": 2,
            "call_forth_flame": 3,
            "dual_nature": 3,
        }
        for power in self.powers:
            total += power_costs.get(power, 0)

        return total

    def get_holdings_required(self):
        """Calculate Holdings dots required (feature points / 3, rounded up)"""
        import math

        return math.ceil(self.get_total_feature_points() / 3)

    def has_power(self, power_name):
        """Check if freehold has a specific power"""
        return power_name in self.powers

    def get_size_description(self):
        """Return textual description of size"""
        descriptions = {
            0: "Miniscule, out in the open with no walls",
            1: "An apartment; one to two average rooms",
            2: "A home; three to four average rooms",
            3: "A mansion, warehouse, or church; five to eight average rooms",
            4: "A sprawling estate, fortress, or network of tunnels; nine to 15 average rooms",
            5: "A significant chunk of the countryside, or a town",
        }
        return descriptions.get(self.size, f"Size {self.size}")
