from characters.models.changeling.house_faction import HouseFaction
from core.models import Model
from django.db import models
from django.urls import reverse


class House(Model):
    type = "house"
    gameline = "ctd"

    court = models.CharField(
        max_length=20,
        choices=[("seelie", "Seelie"), ("unseelie", "Unseelie")],
        blank=True,
        null=True,
    )
    boon = models.TextField(default="", blank=True)
    flaw = models.TextField(default="", blank=True)
    factions = models.ManyToManyField(HouseFaction, blank=True)

    class Meta:
        verbose_name = "House"
        verbose_name_plural = "Houses"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:house")

    def get_absolute_url(self):
        return reverse("characters:changeling:house", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:changeling:update:house", kwargs={"pk": self.pk})

    def get_heading(self):
        return "ctd_heading"
