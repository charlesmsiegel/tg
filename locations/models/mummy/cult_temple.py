from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from locations.models.core.location import LocationModel


class CultTemple(LocationModel):
    """
    Temple or gathering place for mortal cultists who serve/worship an Amenti.
    Represents Background: Cult
    """

    type = "cult_temple"
    gameline = "mtr"

    # Cult size/influence
    cult_size = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Size and devotion of the cult (0-10)",
    )

    # Public cover
    COVER_CHOICES = [
        ("museum", "Museum or Archaeological Society"),
        ("church", "Religious Organization"),
        ("university", "Academic Institution"),
        ("society", "Secret Society"),
        ("business", "Business Front"),
        ("none", "No Cover (Secret)"),
    ]

    public_cover = models.CharField(
        max_length=20,
        choices=COVER_CHOICES,
        default="none",
        help_text="Public facade for the cult",
    )

    # Cult leader (mortal)
    cult_leader_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name of the mortal cult leader/high priest",
    )

    # Resources
    cult_wealth = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Financial resources of the cult (0-5)",
    )

    has_library = models.BooleanField(
        default=False, help_text="Contains occult/Egyptian library"
    )

    has_ritual_chamber = models.BooleanField(
        default=True, help_text="Space for performing Hekau rituals"
    )

    def get_absolute_url(self):
        return reverse("locations:mummy:cult_temple", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:mummy:update:cult_temple", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mummy:create:cult_temple")

    def get_heading(self):
        return "mtr_heading"

    class Meta:
        verbose_name = "Cult Temple"
        verbose_name_plural = "Cult Temples"
