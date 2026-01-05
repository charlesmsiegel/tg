from core.models import Model
from django.db import models
from django.urls import reverse


class WraithFaction(Model):
    type = "wraith_faction"
    gameline = "wto"

    FACTION_TYPE_CHOICES = [
        ("legion", "Legion"),
        ("guild", "Guild Organization"),
        ("heretic", "Heretic Group"),
        ("spectre", "Spectre Organization"),
        ("other", "Other"),
    ]

    faction_type = models.CharField(max_length=20, choices=FACTION_TYPE_CHOICES, default="legion")
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="subfactions",
    )

    class Meta:
        verbose_name = "Wraith Faction"
        verbose_name_plural = "Wraith Factions"

    def get_absolute_url(self):
        return reverse("characters:wraith:faction", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:wraith:update:faction", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:faction")
