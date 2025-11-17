from characters.models.demon.house import House
from core.models import Model
from django.db import models


class Visage(Model):
    """Represents a specific visage/aspect of an apocalyptic form."""

    type = "visage"

    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="visages", null=True, blank=True
    )

    # JSON field containing list of apocalyptic form abilities
    abilities = models.JSONField(default=list)

    class Meta:
        verbose_name = "Visage"
        verbose_name_plural = "Visages"
        ordering = ["name"]

    def __str__(self):
        return self.name
