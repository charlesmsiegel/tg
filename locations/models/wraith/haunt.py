from django.db import models
from django.urls import reverse
from locations.models.core.location import LocationModel


class Haunt(LocationModel):
    """Faith-rich location where the Veil is weakened."""

    type = "haunt"
    gameline = "wto"

    rank = models.IntegerField(default=1)
    shroud_rating = models.IntegerField(default=5)

    # Type of haunt
    haunt_type = models.CharField(
        max_length=100,
        default="sacred_site",
        choices=[
            ("sacred_site", "Sacred Site"),
            ("battlefield", "Battlefield"),
            ("crime_scene", "Crime Scene"),
            ("sickroom", "Sickroom"),
            ("place_of_worship", "Place of Worship"),
            ("place_of_tragedy", "Place of Tragedy"),
            ("other", "Other"),
        ],
    )

    HAUNT_SIZE_CHOICES = [
        ("single_room", "Single Room"),
        ("apartment", "Small Apartment/Shop"),
        ("house", "House/Small Warehouse"),
        ("mansion", "Mansion/Large Building"),
        ("estate", "Estate/Compound"),
    ]

    haunt_size = models.CharField(max_length=20, choices=HAUNT_SIZE_CHOICES, default="single_room")

    # Faith resonance
    faith_resonance = models.TextField(default="", blank=True)

    # Whether ghosts are attracted
    attracts_ghosts = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Haunt"
        verbose_name_plural = "Haunts"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Haunt)"

    def get_absolute_url(self):
        return reverse("locations:wraith:haunt", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("locations:wraith:update:haunt", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:wraith:create:haunt")

    def set_rank(self, rank):
        self.rank = rank
        # Set shroud rating based on rank
        shroud_map = {
            1: 5,
            2: 4,
            3: 3,
            4: 2,
            5: 1,
        }
        self.shroud_rating = shroud_map.get(rank, 5)
        return True
