from core.models import Model
from django.db import models
from django.urls import reverse


class DemonFaction(Model):
    """Represents one of the five major demon factions (Luciferans, Faustians, etc.)."""

    type = "demon_faction"
    gameline = "dtf"

    philosophy = models.TextField(default="", blank=True)
    goal = models.TextField(default="", blank=True)
    leadership = models.TextField(default="", blank=True)
    tactics = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "Demon Faction"
        verbose_name_plural = "Demon Factions"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:demon:faction", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:faction", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:faction")
