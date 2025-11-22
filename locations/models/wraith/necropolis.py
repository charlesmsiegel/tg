from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class Necropolis(LocationModel):
    type = "necropolis"

    REGION_CHOICES = [
        ("stygia", "Stygia"),
        ("ivory", "Dark Kingdom of Ivory"),
        ("jade", "Dark Kingdom of Jade"),
        ("obsidian", "Dark Kingdom of Obsidian"),
        ("other", "Other"),
    ]

    region = models.CharField(max_length=20, choices=REGION_CHOICES, default="stygia")
    population = models.IntegerField(default=0)
    deathlord = models.CharField(max_length=100, default="", blank=True)

    class Meta:
        verbose_name = "Necropolis"
        verbose_name_plural = "Necropolises"

    def get_absolute_url(self):
        return reverse("locations:wraith:necropolis", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("locations:wraith:update:necropolis", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:wraith:create:necropolis")

    def get_heading(self):
        return "wto_heading"
