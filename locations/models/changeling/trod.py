from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core import LocationModel


class Trod(LocationModel):
    """
    A Trod - a magical pathway connecting locations in the Dreaming.
    Trods are the silver paths that changelings use to travel between
    the mundane world and the Dreaming, or between different locations.
    """

    type = "trod"

    # Trod type
    TROD_TYPES = [
        ("silver_path", "Silver Path"),  # Common trod
        ("rath", "Rath"),  # Powerful, ancient trod
        ("moonpath", "Moonpath"),  # Only appears at night
        ("seasonal", "Seasonal Path"),  # Only exists certain times
        ("hidden", "Hidden Path"),  # Requires special knowledge
    ]

    trod_type = models.CharField(
        max_length=20,
        choices=TROD_TYPES,
        default="silver_path",
        help_text="The type of trod this represents",
    )

    # Starting location
    origin_name = models.CharField(
        max_length=200,
        default="",
        blank=True,
        help_text="Name of where this trod starts",
    )

    origin_description = models.TextField(
        default="",
        blank=True,
        help_text="Description of the origin point (mundane location)",
    )

    # Destination
    destination_name = models.CharField(
        max_length=200,
        default="",
        blank=True,
        help_text="Name of where this trod leads",
    )

    destination_description = models.TextField(
        default="",
        blank=True,
        help_text="Description of the destination",
    )

    # Power/difficulty rating
    strength = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="How strong/stable this trod is (0-5 dots)",
    )

    # How dangerous or challenging the trod is to traverse
    difficulty = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Difficulty to traverse (0=easy, 10=nearly impossible)",
    )

    # Requirements to access
    access_requirements = models.TextField(
        default="",
        blank=True,
        help_text="What's needed to access this trod (key, ritual, knowledge)",
    )

    # Guardians or hazards
    guardians = models.TextField(
        default="",
        blank=True,
        help_text="Creatures or beings that guard this trod",
    )

    hazards = models.JSONField(
        default=list,
        blank=True,
        help_text="Dangers along this trod (chimerical beasts, terrain, etc.)",
    )

    # Travel time
    travel_duration = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="How long it takes to traverse (instant, minutes, hours, etc.)",
    )

    # Special properties
    is_two_way = models.BooleanField(
        default=True, help_text="Can you travel both directions?"
    )

    is_stable = models.BooleanField(
        default=True, help_text="Is this trod permanently accessible?"
    )

    glamour_cost = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Glamour required to activate/traverse",
    )

    # When it's accessible
    accessibility_notes = models.TextField(
        default="",
        blank=True,
        help_text="When or how this trod can be accessed (time, season, conditions)",
    )

    # What the journey looks like
    journey_description = models.TextField(
        default="",
        blank=True,
        help_text="What traveling this trod is like - sights, sounds, sensations",
    )

    # Who knows about it
    known_to = models.TextField(
        default="",
        blank=True,
        help_text="Which changelings or groups know about this trod",
    )

    class Meta:
        verbose_name = "Trod"
        verbose_name_plural = "Trods"
        constraints = [
            CheckConstraint(
                check=Q(strength__gte=0, strength__lte=5),
                name="locations_trod_strength_range",
                violation_error_message="Trod strength must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(difficulty__gte=0, difficulty__lte=10),
                name="locations_trod_difficulty_range",
                violation_error_message="Difficulty must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(glamour_cost__gte=0, glamour_cost__lte=10),
                name="locations_trod_glamour_cost_range",
                violation_error_message="Glamour cost must be between 0 and 10",
            ),
        ]

    def get_absolute_url(self):
        return reverse("locations:changeling:trod", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:changeling:update:trod", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:changeling:create:trod")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        if self.origin_name and self.destination_name:
            return f"{self.name} ({self.origin_name} → {self.destination_name})"
        return super().__str__()
