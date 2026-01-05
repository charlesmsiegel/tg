from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class TremereChantry(LocationModel):
    """
    Represents a Tremere Chantry (fortified house of the Tremere clan).
    Chantries serve as ritual centers, libraries, and sanctuaries for Tremere vampires.
    """

    type = "tremere_chantry"
    gameline = "vtm"

    # Size and importance
    size = models.IntegerField(
        default=1,
        help_text="Size of the chantry (1-5 dots, where 5 is a major regional chantry)",
    )

    # Security measures
    security_level = models.IntegerField(
        default=1,
        help_text="Physical and mystical security (1-5 dots)",
    )

    # Library quality
    library_rating = models.IntegerField(
        default=0,
        help_text="Quality and breadth of occult library (0-5 dots)",
    )

    # Resources available
    ritual_rooms = models.IntegerField(
        default=1,
        help_text="Number of dedicated ritual chambers",
    )

    blood_vault_capacity = models.IntegerField(
        default=10,
        help_text="Blood points that can be stored in the chantry's vault",
    )

    # Leadership
    regent_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of the Tremere Regent who leads this chantry",
    )

    # Chantry residents
    resident_count = models.IntegerField(
        default=1,
        help_text="Number of Tremere vampires residing here",
    )

    apprentice_count = models.IntegerField(
        default=0,
        help_text="Number of apprentices (ghouls or young Tremere) training here",
    )

    # Special features
    has_wards = models.BooleanField(
        default=True,
        help_text="Protected by mystical wards against intrusion",
    )

    has_sanctum = models.BooleanField(
        default=False,
        help_text="Contains a powerful private sanctum for high-level rituals",
    )

    has_blood_forge = models.BooleanField(
        default=False,
        help_text="Contains facilities for creating blood stones and other blood magic items",
    )

    has_scrying_chamber = models.BooleanField(
        default=False,
        help_text="Contains a chamber dedicated to remote viewing and divination",
    )

    has_gargoyle_guardians = models.BooleanField(
        default=False,
        help_text="Protected by Gargoyle servitors",
    )

    # Connections to the Pyramid
    pyramid_level = models.IntegerField(
        default=1,
        help_text="Importance in the Tremere hierarchy (1-5, where 5 is Vienna)",
    )

    reports_to = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of the superior chantry or Pontifex this chantry reports to",
    )

    # Total chantry rating (calculated)
    total_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Tremere Chantry"
        verbose_name_plural = "Tremere Chantries"

    def get_update_url(self):
        return reverse("locations:vampire:update:chantry", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:vampire:create:chantry")

    def calculate_total_rating(self):
        """Calculate total Chantry value."""
        total = self.size + self.security_level + self.library_rating
        if self.has_sanctum:
            total += 2
        if self.has_wards:
            total += 1
        if self.has_blood_forge:
            total += 1
        if self.has_scrying_chamber:
            total += 1
        if self.has_gargoyle_guardians:
            total += 1
        self.total_rating = total
        return total

    def save(self, *args, **kwargs):
        """Override save to recalculate total rating."""
        self.calculate_total_rating()
        super().save(*args, **kwargs)
