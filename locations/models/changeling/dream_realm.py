from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core import LocationModel


class DreamRealm(LocationModel):
    """
    A DreamRealm - a location within the Dreaming itself.
    These exist in the Near Dreaming (close to reality), Far Dreaming
    (deeper, more fantastical), or Deep Dreaming (ancient, primal).
    """

    type = "dream_realm"
    gameline = "ctd"

    # Depth in the Dreaming
    DEPTHS = [
        ("near", "Near Dreaming"),  # Close to the Autumn World
        ("far", "Far Dreaming"),  # Deeper, more fantastical
        ("deep", "Deep Dreaming"),  # Ancient, primal, dangerous
    ]

    depth = models.CharField(
        max_length=10,
        choices=DEPTHS,
        default="near",
        help_text="How deep in the Dreaming this realm exists",
    )

    # Nature of the realm
    REALM_TYPES = [
        ("personal", "Personal Dream"),  # Someone's recurring dream
        ("collective", "Collective Dream"),  # Shared dream space
        ("mythic", "Mythic Realm"),  # Based on legend/story
        ("nightmare", "Nightmare Realm"),  # Dark dream space
        ("paradise", "Paradise"),  # Idealized dream space
        ("memory", "Memory Realm"),  # Preserved memory
        ("imagination", "Pure Imagination"),  # Raw creative energy
    ]

    realm_type = models.CharField(
        max_length=20,
        choices=REALM_TYPES,
        default="collective",
        help_text="The nature of this dream realm",
    )

    # Stability and accessibility
    stability = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="How stable/permanent this realm is (0=fleeting, 5=eternal)",
    )

    accessibility = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="How easy it is to reach (0=hidden, 5=open gateway)",
    )

    # Physical properties (dream logic)
    appearance = models.TextField(
        default="",
        blank=True,
        help_text="What this realm looks like - remember, dream logic applies",
    )

    laws_of_reality = models.TextField(
        default="",
        blank=True,
        help_text="How reality works here (gravity, time, causality, etc.)",
    )

    # Inhabitants
    inhabitants = models.TextField(
        default="",
        blank=True,
        help_text="Who or what lives in this realm (chimera, dreamers, etc.)",
    )

    ruler = models.CharField(
        max_length=200,
        default="",
        blank=True,
        help_text="Who rules or controls this realm (if anyone)",
    )

    # Dream characteristics
    emotional_tone = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="The emotional atmosphere (peaceful, chaotic, melancholic, etc.)",
    )

    dominant_themes = models.JSONField(
        default=list,
        blank=True,
        help_text="Recurring themes, symbols, or motifs in this realm",
    )

    # Access and navigation
    entry_requirements = models.TextField(
        default="",
        blank=True,
        help_text="What's needed to enter (specific trod, ritual, state of mind)",
    )

    exit_difficulty = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="How hard it is to leave (0=easy, 10=nearly impossible)",
    )

    # Connection to Autumn World
    mundane_connection = models.TextField(
        default="",
        blank=True,
        help_text="What in the Autumn World this realm connects to (if anything)",
    )

    # Glamour properties
    glamour_level = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="How much Glamour permeates this realm",
    )

    provides_glamour = models.BooleanField(
        default=True, help_text="Can changelings harvest Glamour here?"
    )

    # Dangers and rewards
    hazards = models.JSONField(
        default=list,
        blank=True,
        help_text="Dangers in this realm (nightmare creatures, shifting reality, etc.)",
    )

    treasures = models.TextField(
        default="",
        blank=True,
        help_text="Special items, knowledge, or powers that can be found here",
    )

    # Time dilation
    TIME_FLOW = [
        ("normal", "Normal"),  # Time flows normally
        ("faster", "Faster"),  # Time moves faster than outside
        ("slower", "Slower"),  # Time moves slower
        ("variable", "Variable"),  # Time is unpredictable
        ("frozen", "Frozen"),  # Time doesn't pass
    ]

    time_flow = models.CharField(
        max_length=20,
        choices=TIME_FLOW,
        default="normal",
        help_text="How time passes in this realm compared to outside",
    )

    # Changeability
    is_mutable = models.BooleanField(
        default=True,
        help_text="Can this realm be reshaped by will/imagination?",
    )

    # Special properties
    special_properties = models.JSONField(
        default=list,
        blank=True,
        help_text="Unique characteristics of this realm",
    )

    class Meta:
        verbose_name = "Dream Realm"
        verbose_name_plural = "Dream Realms"
        constraints = [
            CheckConstraint(
                check=Q(stability__gte=0, stability__lte=5),
                name="locations_dream_realm_stability_range",
                violation_error_message="Stability must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(accessibility__gte=0, accessibility__lte=5),
                name="locations_dream_realm_accessibility_range",
                violation_error_message="Accessibility must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(exit_difficulty__gte=0, exit_difficulty__lte=10),
                name="locations_dream_realm_exit_difficulty_range",
                violation_error_message="Exit difficulty must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(glamour_level__gte=0, glamour_level__lte=10),
                name="locations_dream_realm_glamour_level_range",
                violation_error_message="Glamour level must be between 0 and 10",
            ),
        ]

    def get_absolute_url(self):
        return reverse("locations:changeling:dream_realm", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:changeling:update:dream_realm", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:changeling:create:dream_realm")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        return f"{self.name} ({self.get_depth_display()})"

    def get_depth_description(self):
        """Return a description of what this depth means"""
        descriptions = {
            "near": "Close to the Autumn World, relatively stable and familiar",
            "far": "Deep in fantasy, where dream logic prevails",
            "deep": "Primal and ancient, where reality itself is malleable",
        }
        return descriptions.get(self.depth, "")
