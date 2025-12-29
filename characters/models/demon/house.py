from core.models import Model
from django.db import models
from django.urls import reverse


class DemonHouse(Model):
    """Represents one of the seven Houses of the Fallen."""

    type = "house"
    gameline = "dtf"

    celestial_name = models.CharField(max_length=100, unique=True)
    starting_torment = models.IntegerField(default=3)

    # Domain/specialty description
    domain = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "House"
        verbose_name_plural = "Houses"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.celestial_name})"

    def get_absolute_url(self):
        return reverse("characters:demon:house", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:house", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:house")

    def get_heading(self):
        return "dtf_heading"
