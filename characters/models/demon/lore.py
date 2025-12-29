from characters.models.demon.house import DemonHouse
from core.models import Model
from django.db import models
from django.urls import reverse


class Lore(Model):
    """Represents one of the 23 Lore types."""

    type = "lore"
    gameline = "dtf"

    property_name = models.CharField(max_length=100, unique=True)

    # Which houses have this as a house lore (can be multiple)
    houses = models.ManyToManyField(DemonHouse, blank=True, related_name="lores")

    # Description of what this lore does
    description = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "Lore"
        verbose_name_plural = "Lores"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:demon:lore", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:lore", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:lore")

    def get_heading(self):
        return "dtf_heading"
