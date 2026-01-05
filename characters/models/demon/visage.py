from characters.models.demon.house import DemonHouse
from core.models import Model
from django.db import models
from django.urls import reverse


class Visage(Model):
    """
    Represents a specific visage/aspect of a demon's apocalyptic form.

    A Visage is primarily descriptive - it has a name and description.
    It also has a default ApocalypticForm that demons can use as a starting point.
    """

    type = "visage"
    gameline = "dtf"

    house = models.ForeignKey(
        DemonHouse,
        on_delete=models.CASCADE,
        related_name="visages",
        null=True,
        blank=True,
    )

    # Default apocalyptic form for this visage
    default_apocalyptic_form = models.ForeignKey(
        "ApocalypticForm",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visages_using_as_default",
        help_text="The default apocalyptic form traits for this visage",
    )

    class Meta:
        verbose_name = "Visage"
        verbose_name_plural = "Visages"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:demon:visage", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:visage", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:visage")
