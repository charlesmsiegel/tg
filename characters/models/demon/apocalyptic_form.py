from core.models import Model
from django.db import models


class ApocalypticFormTrait(Model):
    """Represents a specific ability/trait available in apocalyptic form."""

    type = "apocalyptic_form_trait"

    # Description of what this trait does
    description = models.TextField(default="")

    # Point cost for this trait (1-5, typically 1-3)
    cost = models.IntegerField(default=1)

    # Power level categorization
    POWER_LEVELS = [
        ("minor", "Minor"),
        ("moderate", "Moderate"),
        ("major", "Major"),
        ("legendary", "Legendary"),
    ]
    power_level = models.CharField(
        max_length=20, choices=POWER_LEVELS, default="minor"
    )

    # Associated house (optional - some traits might be universal)
    house = models.ForeignKey(
        "House",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apocalyptic_traits",
    )

    class Meta:
        verbose_name = "Apocalyptic Form Trait"
        verbose_name_plural = "Apocalyptic Form Traits"
        ordering = ["cost", "name"]

    def __str__(self):
        return f"{self.name} ({self.cost} pts)"
