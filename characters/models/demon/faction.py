from core.models import Model
from django.db import models


class DemonFaction(Model):
    """Represents one of the five major demon factions (Luciferans, Faustians, etc.)."""

    type = "demon_faction"

    philosophy = models.TextField(default="")
    goal = models.TextField(default="")
    leadership = models.TextField(default="")
    tactics = models.TextField(default="")

    class Meta:
        verbose_name = "Demon Faction"
        verbose_name_plural = "Demon Factions"
        ordering = ["name"]

    def __str__(self):
        return self.name
