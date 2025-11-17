from characters.models.demon.house import House
from core.models import Model
from django.db import models


class Visage(Model):
    """Represents a specific visage/aspect of an apocalyptic form."""

    type = "visage"

    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="visages", null=True, blank=True
    )

    # Available apocalyptic form traits for this visage
    available_traits = models.ManyToManyField(
        "ApocalypticFormTrait", blank=True, related_name="visages"
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
