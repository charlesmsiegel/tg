from core.models import Model
from django.db import models
from django.urls import reverse


class Ritual(Model):
    """Represents a Demon ritual that can be learned and performed."""

    type = "ritual"

    # Which house this ritual belongs to
    house = models.ForeignKey(
        "DemonHouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rituals",
    )

    # Primary lore requirement (e.g., "Lore of Storms")
    primary_lore = models.ForeignKey(
        "Lore",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_rituals",
        help_text="The primary lore required to act as Ankida",
    )
    primary_lore_rating = models.IntegerField(
        default=1, help_text="Dots of primary lore required (1-5)"
    )

    # Secondary lore requirements stored as JSON
    # Format: [{"lore_id": 1, "rating": 2}, {"lore_id": 3, "rating": 1}]
    secondary_lore_requirements = models.JSONField(
        default=list, blank=True, help_text="List of secondary lore requirements"
    )

    # Experience point cost to learn
    base_cost = models.IntegerField(
        default=6,
        help_text="Experience points required to learn this ritual",
    )

    # Restrictions on performing the ritual
    restrictions = models.TextField(
        default="",
        help_text="Requirements for performing the ritual (time, location, materials, etc.)",
    )

    # Minimum time to cast in minutes
    minimum_casting_time = models.IntegerField(
        default=10, help_text="Minimum time in minutes to perform the ritual"
    )

    # System mechanics
    system = models.TextField(
        default="",
        help_text="Roll and effect description for the ritual",
    )

    # High-Torment effect
    torment_effect = models.TextField(
        default="",
        help_text="Description of the ritual's high-Torment variant",
    )

    # Known variations
    variations = models.TextField(
        default="",
        blank=True,
        help_text="Alternate versions or modifications of this ritual",
    )

    # Additional flavor/history text
    flavor_text = models.TextField(
        default="",
        blank=True,
        help_text="Historical context or descriptive flavor text",
    )

    # Source page reference
    source_page = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Page reference from source book",
    )

    class Meta:
        verbose_name = "Ritual"
        verbose_name_plural = "Rituals"
        ordering = ["house__name", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:demon:ritual", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:ritual", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:ritual")

    def get_heading(self):
        return "dtf_heading"

    def get_secondary_lores(self):
        """Get list of secondary lore objects with ratings."""
        from characters.models.demon.lore import Lore

        lores = []
        for req in self.secondary_lore_requirements:
            try:
                lore = Lore.objects.get(pk=req["lore_id"])
                lores.append({"lore": lore, "rating": req["rating"]})
            except (Lore.DoesNotExist, KeyError):
                continue
        return lores

    def total_lore_dots(self):
        """Calculate total dots of lore required."""
        total = self.primary_lore_rating
        for req in self.secondary_lore_requirements:
            total += req.get("rating", 0)
        return total

    def total_lore_paths(self):
        """Calculate total number of lore paths required."""
        return 1 + len(self.secondary_lore_requirements)

    def get_primary_lore_display(self):
        """Get formatted display of primary lore requirement."""
        if self.primary_lore:
            dots = "•" * self.primary_lore_rating
            return f"{self.primary_lore.name} {dots}"
        return ""

    def get_secondary_lore_display(self):
        """Get formatted list of secondary lore requirements."""
        displays = []
        for lore_info in self.get_secondary_lores():
            dots = "•" * lore_info["rating"]
            displays.append(f"{lore_info['lore'].name} {dots}")
        return displays
