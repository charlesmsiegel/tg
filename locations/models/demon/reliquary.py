from django.db import models
from django.urls import reverse

from locations.models.core.location import LocationModel


class Reliquary(LocationModel):
    """
    Reliquary (Location) - A location that serves as an Earthbound's vessel

    Some Earthbound dwell not in objects, but in locations - temples, groves,
    caves, or other sanctified places. The demon's essence suffuses the entire
    structure.
    """

    type = "reliquary"
    gameline = "dtf"

    # Reliquary types
    RELIQUARY_TYPES = [
        ("location", "Location (Stationary)"),
        ("perfect", "Perfect Reliquary (Object)"),
        ("improvised", "Improvised Reliquary (Object)"),
    ]

    reliquary_type = models.CharField(
        max_length=20,
        choices=RELIQUARY_TYPES,
        default="location",
        help_text="Type of reliquary",
    )

    # For location reliquaries
    location_size = models.CharField(
        max_length=200,
        blank=True,
        help_text="Description of the location's size and boundaries",
    )

    # Health levels (for tracking damage)
    max_health_levels = models.IntegerField(
        default=20,
        help_text="Maximum health levels (Faith + Willpower x 2 for locations)",
    )

    current_health_levels = models.IntegerField(default=20, help_text="Current health levels")

    # Soak rating
    soak_rating = models.IntegerField(
        default=0, help_text="Soak rating equal to permanent Willpower"
    )

    # Special features for location reliquaries
    has_pervasiveness = models.BooleanField(
        default=True, help_text="Earthbound can sense everything within the location"
    )

    has_manifestation = models.BooleanField(
        default=True, help_text="Can manifest apocalyptic form within location"
    )

    manifestation_range = models.IntegerField(
        default=0,
        help_text="Range in yards the Earthbound can move outside location (= Faith)",
    )

    class Meta:
        verbose_name = "Reliquary"
        verbose_name_plural = "Reliquaries"

    def get_absolute_url(self):
        return reverse("locations:demon:reliquary", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("locations:demon:update:reliquary", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:demon:create:reliquary")

    def is_damaged(self):
        """Check if the reliquary has taken damage"""
        return self.current_health_levels < self.max_health_levels

    def damage_percentage(self):
        """Return percentage of damage taken"""
        if self.max_health_levels == 0:
            return 0
        return (self.max_health_levels - self.current_health_levels) / self.max_health_levels * 100
