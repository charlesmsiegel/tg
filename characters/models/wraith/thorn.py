from core.models import Model
from django.db import models
from django.urls import reverse


class Thorn(Model):
    type = "thorn"
    gameline = "wto"

    THORN_TYPE_CHOICES = [
        ("individual", "Individual Thorn"),
        ("collective", "Collective Thorn"),
    ]

    thorn_type = models.CharField(
        max_length=20, choices=THORN_TYPE_CHOICES, default="individual"
    )
    point_cost = models.IntegerField(default=1)
    activation_cost = models.CharField(max_length=100, default="")  # e.g., "1 Angst"
    activation_trigger = models.TextField(default="")
    mechanical_description = models.TextField(default="")
    resistance_system = models.TextField(default="")
    resistance_difficulty = models.IntegerField(default=6, null=True, blank=True)
    duration = models.CharField(max_length=200, default="")
    frequency_limitation = models.CharField(max_length=200, default="")
    limitations = models.TextField(default="")

    class Meta:
        verbose_name = "Thorn"
        verbose_name_plural = "Thorns"

    def get_absolute_url(self):
        return reverse("characters:wraith:thorn", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:wraith:update:thorn", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:thorn")

    def get_heading(self):
        return "wto_heading"
