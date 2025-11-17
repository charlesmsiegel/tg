from core.models import Model
from django.db import models


class House(Model):
    """Represents one of the seven Houses of the Fallen."""

    type = "house"

    celestial_name = models.CharField(max_length=100, unique=True)
    starting_torment = models.IntegerField(default=3)

    # Domain/specialty description
    domain = models.TextField(default="")

    class Meta:
        verbose_name = "House"
        verbose_name_plural = "Houses"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.celestial_name})"
