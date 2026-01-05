from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class Byway(LocationModel):
    """Tempest path connecting Necropolises and other underworld locations."""

    type = "byway"
    gameline = "wto"

    DANGER_LEVEL_CHOICES = [
        ("safe", "Safe - Well-patrolled and maintained"),
        ("moderate", "Moderate - Occasional dangers"),
        ("dangerous", "Dangerous - Frequent hazards"),
        ("treacherous", "Treacherous - Extreme danger"),
        ("lethal", "Lethal - Nearly impassable"),
    ]

    STABILITY_CHOICES = [
        ("stable", "Stable - Permanent route"),
        ("shifting", "Shifting - Route changes occasionally"),
        ("unstable", "Unstable - Frequently changes"),
        ("ephemeral", "Ephemeral - Temporary route"),
    ]

    danger_level = models.CharField(max_length=20, choices=DANGER_LEVEL_CHOICES, default="moderate")

    stability = models.CharField(max_length=20, choices=STABILITY_CHOICES, default="stable")

    # Travel details
    origin = models.CharField(
        max_length=200, blank=True, help_text="Starting location (e.g., Necropolis name)"
    )
    destination = models.CharField(
        max_length=200,
        blank=True,
        help_text="Ending location (e.g., Necropolis name)",
    )
    travel_time = models.CharField(
        max_length=100,
        blank=True,
        help_text="Typical travel time (e.g., '3 days', '1 week')",
    )

    # Tempest properties
    maelstrom_proximity = models.IntegerField(
        default=5, help_text="Proximity to maelstroms (1-10, higher = closer/more dangerous)"
    )
    spectral_activity = models.IntegerField(default=5, help_text="Level of Spectre activity (1-10)")

    # Special features
    has_waystation = models.BooleanField(
        default=False, help_text="Contains rest stop or waystation"
    )
    patrolled = models.BooleanField(
        default=False, help_text="Regularly patrolled by Hierarchy forces"
    )
    haunted = models.BooleanField(
        default=False, help_text="Known to be haunted by dangerous entities"
    )

    class Meta:
        verbose_name = "Byway"
        verbose_name_plural = "Byways"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Byway)"

    def get_absolute_url(self):
        return reverse("locations:wraith:byway", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("locations:wraith:update:byway", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:wraith:create:byway")
