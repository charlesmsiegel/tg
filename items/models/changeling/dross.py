from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from items.models.core import ItemModel


class Dross(ItemModel):
    """
    Dross - Physical manifestation of Glamour.
    Dross is crystallized dream energy that changelings can use to power
    their Arts or store for later use. It's essentially Glamour currency.
    """

    type = "dross"

    # Dross quality (affects how much Glamour it provides)
    QUALITY_LEVELS = [
        ("ephemeral", "Ephemeral"),  # 1 Glamour, fades quickly
        ("common", "Common"),  # 2-3 Glamour, standard dross
        ("fine", "Fine"),  # 4-5 Glamour, high quality
        ("exquisite", "Exquisite"),  # 6-8 Glamour, rare
        ("legendary", "Legendary"),  # 9-10 Glamour, extremely rare
    ]

    quality = models.CharField(
        max_length=20,
        choices=QUALITY_LEVELS,
        default="common",
        help_text="The quality/potency of this dross",
    )

    # Glamour value
    glamour_value = models.IntegerField(
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="How much Glamour this dross contains (1-10 points)",
    )

    # Physical form
    FORMS = [
        ("crystal", "Crystal"),  # Crystalline shard
        ("liquid", "Liquid"),  # Glowing liquid
        ("vapor", "Vapor"),  # Shimmering mist
        ("object", "Object"),  # Physical object infused with glamour
        ("other", "Other"),
    ]

    physical_form = models.CharField(
        max_length=20,
        choices=FORMS,
        default="crystal",
        help_text="What form this dross takes",
    )

    # Appearance
    color = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Color or appearance of the dross",
    )

    # Source
    SOURCE_TYPES = [
        ("balefire", "From Balefire"),
        ("dream", "Harvested from Dream"),
        ("art", "Created by Art"),
        ("natural", "Natural Formation"),
        ("refined", "Refined from Raw Glamour"),
        ("unknown", "Unknown Origin"),
    ]

    source = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        default="natural",
        help_text="Where this dross came from",
    )

    # Stability
    is_stable = models.BooleanField(
        default=True,
        help_text="Is this dross stable, or does it decay over time?",
    )

    decay_rate = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="How quickly it decays if unstable (hours, days, weeks)",
    )

    # Special properties
    resonance = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Emotional or thematic resonance (joy, sorrow, courage, etc.)",
    )

    special_effects = models.TextField(
        default="",
        blank=True,
        help_text="Any special effects or properties when used",
    )

    # Usage restrictions
    restricted_to = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Can only be used by specific kiths, courts, or individuals",
    )

    # Single use or renewable
    is_consumable = models.BooleanField(
        default=True,
        help_text="Is this dross consumed when used (vs. renewable)?",
    )

    recharge_method = models.TextField(
        default="",
        blank=True,
        help_text="If renewable, how does it recharge?",
    )

    # Container (if applicable)
    container_description = models.TextField(
        default="",
        blank=True,
        help_text="What contains this dross (vial, pouch, box, etc.)",
    )

    # Trade value
    estimated_value = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Approximate trade value in changeling society",
    )

    class Meta:
        verbose_name = "Dross"
        verbose_name_plural = "Dross"
        constraints = [
            CheckConstraint(
                check=Q(glamour_value__gte=1, glamour_value__lte=10),
                name="items_dross_glamour_value_range",
                violation_error_message="Glamour value must be between 1 and 10",
            ),
        ]

    def get_absolute_url(self):
        return reverse("items:changeling:dross", args=[str(self.id)])

    def get_update_url(self):
        return reverse("items:changeling:update:dross", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:changeling:create:dross")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.glamour_value} Glamour)"
        return f"{self.get_quality_display()} Dross ({self.glamour_value} Glamour)"

    def get_quality_multiplier(self):
        """Return a rough multiplier based on quality"""
        multipliers = {
            "ephemeral": 0.5,
            "common": 1.0,
            "fine": 2.0,
            "exquisite": 4.0,
            "legendary": 10.0,
        }
        return multipliers.get(self.quality, 1.0)
