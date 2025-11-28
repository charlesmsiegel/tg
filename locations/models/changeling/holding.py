from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core import LocationModel


class Holding(LocationModel):
    """
    A Holding - a noble's territory in changeling society.
    These are political divisions ruled by titled nobles (Barons, Counts, Dukes).
    Holdings can be Baronies, Counties, Duchies, or even Kingdoms.
    """

    type = "holding"
    gameline = "ctd"

    # Holding rank (political level)
    RANKS = [
        ("barony", "Barony"),  # Ruled by a Baron/Baroness
        ("county", "County"),  # Ruled by a Count/Countess
        ("duchy", "Duchy"),  # Ruled by a Duke/Duchess
        ("kingdom", "Kingdom"),  # Ruled by a King/Queen (rare)
        ("province", "Province"),  # Larger region
    ]

    rank = models.CharField(
        max_length=20,
        choices=RANKS,
        default="barony",
        help_text="The political rank of this holding",
    )

    # Who rules it
    ruler_name = models.CharField(
        max_length=200,
        default="",
        blank=True,
        help_text="Name of the noble who rules this holding",
    )

    ruler_title = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Full title of the ruler (e.g., 'Baron of the Silver Mists')",
    )

    # Court affiliation
    COURTS = [
        ("seelie", "Seelie Court"),
        ("unseelie", "Unseelie Court"),
        ("shadow", "Shadow Court"),
        ("independent", "Independent"),
        ("disputed", "Disputed"),
    ]

    court = models.CharField(
        max_length=20,
        choices=COURTS,
        default="seelie",
        help_text="Which court controls this holding",
    )

    # Geographic coverage
    territory_description = models.TextField(
        default="",
        blank=True,
        help_text="Geographic area this holding covers (city districts, rural area, etc.)",
    )

    mundane_location = models.TextField(
        default="",
        blank=True,
        help_text="The real-world location this holding encompasses",
    )

    # Political details
    vassals = models.TextField(
        default="",
        blank=True,
        help_text="Lesser nobles who owe fealty to this holding's ruler",
    )

    liege = models.CharField(
        max_length=200,
        default="",
        blank=True,
        help_text="Higher noble this holding owes allegiance to",
    )

    # Freeholds within the holding
    freehold_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text="Number of freeholds within this holding",
    )

    major_freeholds = models.TextField(
        default="",
        blank=True,
        help_text="Names and descriptions of major freeholds in this holding",
    )

    # Resources and strength
    population = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Approximate changeling population (small, moderate, large, etc.)",
    )

    military_strength = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Military/defensive capability (0-5 dots)",
    )

    wealth = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Economic resources (0-5 dots)",
    )

    # Political climate
    stability = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Political stability (0=chaos, 5=very stable)",
    )

    political_situation = models.TextField(
        default="",
        blank=True,
        help_text="Current political climate, tensions, alliances",
    )

    # Laws and customs
    notable_laws = models.TextField(
        default="",
        blank=True,
        help_text="Important laws or customs specific to this holding",
    )

    # Conflicts and threats
    rival_holdings = models.TextField(
        default="",
        blank=True,
        help_text="Neighboring or rival holdings and their relations",
    )

    threats = models.JSONField(
        default=list,
        blank=True,
        help_text="Current threats (Autumn People, Thallain, rival courts, etc.)",
    )

    # Historical significance
    history = models.TextField(
        default="",
        blank=True,
        help_text="History of this holding, how it was established, major events",
    )

    class Meta:
        verbose_name = "Holding"
        verbose_name_plural = "Holdings"
        constraints = [
            CheckConstraint(
                check=Q(military_strength__gte=0, military_strength__lte=5),
                name="locations_holding_military_range",
                violation_error_message="Military strength must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(wealth__gte=0, wealth__lte=5),
                name="locations_holding_wealth_range",
                violation_error_message="Wealth must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(stability__gte=0, stability__lte=5),
                name="locations_holding_stability_range",
                violation_error_message="Stability must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(freehold_count__gte=0, freehold_count__lte=50),
                name="locations_holding_freehold_count_range",
                violation_error_message="Freehold count must be between 0 and 50",
            ),
        ]

    def get_absolute_url(self):
        return reverse("locations:changeling:holding", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:changeling:update:holding", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:changeling:create:holding")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        if self.ruler_name:
            return f"{self.name} ({self.get_rank_display()}, ruled by {self.ruler_name})"
        return f"{self.name} ({self.get_rank_display()})"
