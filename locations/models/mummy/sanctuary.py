from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from locations.models.core.location import LocationModel


class UndergroundSanctuary(LocationModel):
    """
    Hidden underground refuge, not a formal tomb but a safe place.
    Modern Amenti may create these as backup safe houses.
    """

    type = "underground_sanctuary"
    gameline = "mtr"

    SANCTUARY_TYPE_CHOICES = [
        ("catacombs", "Ancient Catacombs"),
        ("basement", "Modern Building Basement"),
        ("caves", "Natural Cave System"),
        ("subway", "Abandoned Subway/Infrastructure"),
        ("bunker", "Military/Emergency Bunker"),
    ]

    sanctuary_type = models.CharField(
        max_length=20,
        choices=SANCTUARY_TYPE_CHOICES,
        default="basement",
    )

    concealment_rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="How well hidden is this sanctuary?",
    )

    def get_absolute_url(self):
        return reverse("locations:mummy:sanctuary", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:mummy:update:sanctuary", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mummy:create:sanctuary")

    class Meta:
        verbose_name = "Underground Sanctuary"
        verbose_name_plural = "Underground Sanctuaries"
