from django.db import models
from django.urls import reverse

from locations.models.core import LocationModel


class Citadel(LocationModel):
    """Fortified stronghold within a Necropolis or independent territory."""

    type = "citadel"
    gameline = "wto"

    CITADEL_PURPOSE_CHOICES = [
        ("guild_hall", "Guild Hall"),
        ("legion_fortress", "Legion Fortress"),
        ("hierarchy_outpost", "Hierarchy Outpost"),
        ("renegade_stronghold", "Renegade Stronghold"),
        ("trade_hub", "Trade Hub"),
        ("prison", "Prison/Oubliette"),
        ("palace", "Palace/Seat of Power"),
        ("other", "Other"),
    ]

    purpose = models.CharField(max_length=50, choices=CITADEL_PURPOSE_CHOICES, default="guild_hall")

    # Defense and military
    defense_rating = models.IntegerField(default=1, help_text="Defense strength (1-10)")
    garrison_size = models.IntegerField(default=0, help_text="Number of wraiths garrisoned")
    commander = models.CharField(max_length=100, blank=True, help_text="Name of military commander")

    # Affiliation
    controlling_faction = models.CharField(
        max_length=100, blank=True, help_text="Guild, Legion, or faction in control"
    )

    # Special features
    has_soulforges = models.BooleanField(default=False, help_text="Contains soulforging facilities")
    has_prison = models.BooleanField(default=False, help_text="Contains prison/oubliette")
    has_gateway = models.BooleanField(default=False, help_text="Contains gateway to other realms")

    class Meta:
        verbose_name = "Citadel"
        verbose_name_plural = "Citadels"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Citadel)"

    def get_absolute_url(self):
        return reverse("locations:wraith:citadel", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("locations:wraith:update:citadel", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:wraith:create:citadel")
