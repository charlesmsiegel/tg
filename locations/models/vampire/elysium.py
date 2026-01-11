from django.db import models
from django.urls import reverse

from locations.models.core import LocationModel


class Elysium(LocationModel):
    """
    Represents an Elysium (neutral ground where violence is forbidden).
    Elysiums are sacred places in Camarilla society.
    """

    type = "elysium"
    gameline = "vtm"

    # Elysium prestige
    prestige = models.IntegerField(
        default=1,
        help_text="Prestige and importance of Elysium (1-5)",
    )

    # Keeper of Elysium
    keeper_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of the Keeper of Elysium",
    )

    # Elysium type
    elysium_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="E.g., 'Museum', 'Opera House', 'Private Club', 'Cathedral'",
    )

    # Rules and restrictions
    is_protected = models.BooleanField(
        default=True,
        help_text="Violence forbidden (standard Elysium rule)",
    )

    allows_weapons = models.BooleanField(
        default=False,
        help_text="Whether weapons are permitted",
    )

    has_blood_dolls = models.BooleanField(
        default=False,
        help_text="Whether feeding vessels are provided",
    )

    # Special features
    has_art_collection = models.BooleanField(
        default=False,
        help_text="Notable art or cultural collection",
    )

    has_library = models.BooleanField(
        default=False,
        help_text="Contains library or archives",
    )

    # Political significance
    is_court = models.BooleanField(
        default=False,
        help_text="Prince holds court here",
    )

    class Meta:
        verbose_name = "Elysium"
        verbose_name_plural = "Elysiums"

    def get_update_url(self):
        return reverse("locations:vampire:update:elysium", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:vampire:create:elysium")
