from django.db import models
from django.urls import reverse

from locations.models.core import LocationModel


class Safehouse(LocationModel):
    """
    Hunter cell's base of operations.
    A secure location used for planning, storing equipment, and recovering.
    """

    type = "safehouse"

    # Size and capacity
    size = models.IntegerField(
        default=1,
        help_text="Size of safehouse (1-5 dots)",
    )

    capacity = models.IntegerField(
        default=5,
        help_text="Maximum number of occupants",
    )

    # Security and resources
    security_level = models.IntegerField(
        default=1,
        help_text="Security measures and fortification (1-5)",
    )

    armory_level = models.IntegerField(
        default=0,
        help_text="Quality and quantity of weapons stored (0-5)",
    )

    surveillance_level = models.IntegerField(
        default=0,
        help_text="Surveillance and monitoring capabilities (0-5)",
    )

    medical_facilities = models.IntegerField(
        default=0,
        help_text="Medical equipment and supplies (0-5)",
    )

    # Secrecy
    is_compromised = models.BooleanField(
        default=False,
        help_text="Location is known to enemies",
    )

    is_mobile = models.BooleanField(
        default=False,
        help_text="Mobile safehouse (RV, boat, etc.)",
    )

    # Features
    has_panic_room = models.BooleanField(
        default=False,
        help_text="Contains a reinforced panic room",
    )

    has_escape_routes = models.BooleanField(
        default=False,
        help_text="Multiple escape routes available",
    )

    has_dead_drop = models.BooleanField(
        default=False,
        help_text="Has secure dead drop location",
    )

    has_communications = models.BooleanField(
        default=True,
        help_text="Secure communications equipment",
    )

    # Ownership
    cover_story = models.TextField(
        blank=True,
        help_text="Cover story for the location's use",
    )

    legal_owner = models.CharField(
        max_length=200,
        blank=True,
        help_text="Legal owner on record",
    )

    # Total rating calculation
    total_rating = models.IntegerField(
        default=0,
        help_text="Total value of safehouse resources",
    )

    class Meta:
        verbose_name = "Safehouse"
        verbose_name_plural = "Safehouses"

    def get_update_url(self):
        return reverse("locations:hunter:update:safehouse", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:hunter:create:safehouse")

    def get_heading(self):
        return "htr_heading"

    def calculate_total_rating(self):
        """Calculate total safehouse value."""
        total = (
            self.size
            + self.security_level
            + self.armory_level
            + self.surveillance_level
            + self.medical_facilities
        )

        # Bonuses
        if self.has_panic_room:
            total += 1
        if self.has_escape_routes:
            total += 1
        if self.has_dead_drop:
            total += 1

        # Penalties
        if self.is_compromised:
            total -= 2

        self.total_rating = max(0, total)
        return self.total_rating

    def save(self, *args, **kwargs):
        """Override save to recalculate total rating."""
        self.calculate_total_rating()
        super().save(*args, **kwargs)
