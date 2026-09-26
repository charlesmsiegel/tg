from django.db import models

from locations.models.core import LocationModel


class Necropolis(LocationModel):
    type = "necropolis"
    gameline = "wto"

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
