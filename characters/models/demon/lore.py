from characters.models.demon.house import DemonHouse
from core.models import Model
from django.db import models


class Lore(Model):
    """Represents one of the 23 Lore types."""

    type = "lore"

    property_name = models.CharField(max_length=100, unique=True)

    # Which houses have this as a house lore (can be multiple)
    houses = models.ManyToManyField(DemonHouse, blank=True, related_name="lores")

    # Description of what this lore does
    description = models.TextField(default="")

    class Meta:
        verbose_name = "Lore"
        verbose_name_plural = "Lores"
        ordering = ["name"]

    def __str__(self):
        return self.name
