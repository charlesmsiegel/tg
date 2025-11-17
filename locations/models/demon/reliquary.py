from django.db import models
from locations.models.core.location import LocationModel


class Reliquary(LocationModel):
    """Physical anchor for Earthbound demons."""

    type = "reliquary"

    # Type of reliquary
    reliquary_type = models.CharField(
        max_length=100,
        default="improvised",
        choices=[
            ("perfect", "Perfect Reliquary"),
            ("improvised", "Improvised Reliquary"),
            ("location", "Location Reliquary"),
        ],
    )

    # Material/composition for object reliquaries
    material = models.TextField(default="")

    # Soak type
    soak_type = models.CharField(
        max_length=100,
        default="temporary_willpower",
        choices=[
            ("permanent_willpower_auto", "Permanent Willpower (automatic)"),
            (
                "permanent_willpower_rolled",
                "Permanent Willpower (rolled)",
            ),
            ("temporary_willpower", "Temporary Willpower (rolled)"),
        ],
    )

    # Health levels (equal to permanent Faith of bound demon)
    health_levels = models.IntegerField(default=0)

    # Regeneration rate
    regeneration_rate = models.CharField(
        max_length=100,
        default="1_per_month",
        choices=[
            ("1_per_week", "1 Faith per week"),
            ("1_per_month", "1 Faith per month"),
        ],
    )

    # Maximum Hoard rating
    max_hoard = models.IntegerField(default=5)

    # Manifestation cost
    manifestation_cost = models.IntegerField(
        default=1
    )  # Faith per turn (1 or 2)

    # Special properties for location reliquaries
    is_location_reliquary = models.BooleanField(default=False)
    location_size = models.CharField(
        max_length=100,
        default="small",
        choices=[
            ("small", "Small (Faith 3-5)"),
            ("large", "Large Structure (Faith 6-8)"),
            ("enormous", "Enormous (Faith 9-10)"),
        ],
    )

    class Meta:
        verbose_name = "Reliquary"
        verbose_name_plural = "Reliquaries"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_reliquary_type_display()})"

    def calculate_health_levels(self, faith_rating):
        """Calculate health levels based on bound demon's Faith."""
        if self.is_location_reliquary:
            # Location reliquaries have more health
            self.health_levels = faith_rating * 2
        else:
            self.health_levels = faith_rating
        self.save()
        return self.health_levels

    def get_manifestation_cost(self):
        """Get the Faith cost per turn for manifestation."""
        if self.reliquary_type == "improvised":
            return 1
        else:
            return 2
