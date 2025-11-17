from characters.models.demon.house import DemonHouse
from core.models import Model
from django.db import models


class Visage(Model):
    """Represents a specific visage/aspect of an apocalyptic form."""

    type = "visage"

    house = models.ForeignKey(
        DemonHouse,
        on_delete=models.CASCADE,
        related_name="visages",
        null=True,
        blank=True,
    )

    # Available apocalyptic form traits for this visage
    low_torment_traits = models.ManyToManyField(
        "ApocalypticFormTrait", blank=True, related_name="low_torment_visages"
    )
    high_torment_traits = models.ManyToManyField(
        "ApocalypticFormTrait", blank=True, related_name="high_torment_visages"
    )

    class Meta:
        verbose_name = "Visage"
        verbose_name_plural = "Visages"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_available_traits(self):
        """Get all traits available for this visage."""
        return self.available_traits.all()

    def total_traits(self):
        """Get total number of available traits."""
        return self.available_traits.count()
