from core.models import Model
from django.db import models
from django.urls import reverse


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

    def get_absolute_url(self):
        return reverse("characters:demon:faction", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:faction", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:faction")

    def get_heading(self):
        return "dtf_heading"
