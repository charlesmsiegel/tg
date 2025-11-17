from django.db import models
from locations.models.core.location import LocationModel


class Haunt(LocationModel):
    """Faith-rich location where the Veil is weakened."""

    type = "haunt"

    # Type of haunt
    haunt_type = models.CharField(
        max_length=100,
        default="sacred_site",
        choices=[
            ("sacred_site", "Sacred Site"),
            ("battlefield", "Battlefield"),
            ("crime_scene", "Crime Scene"),
            ("sickroom", "Sickroom"),
            ("place_of_worship", "Place of Worship"),
            ("place_of_tragedy", "Place of Tragedy"),
            ("other", "Other"),
        ],
    )

    # Veil difficulty (default 5, easier to cross than normal)
    veil_difficulty = models.IntegerField(default=5)

    # Faith resonance
    faith_resonance = models.TextField(default="")

    # Whether ghosts are attracted
    attracts_ghosts = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Haunt"
        verbose_name_plural = "Haunts"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Haunt)"
