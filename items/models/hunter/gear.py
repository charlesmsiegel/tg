from django.db import models
from django.urls import reverse

from items.models.core import ItemModel


class HunterGear(ItemModel):
    """
    Specialized hunter equipment and tools.
    Includes weapons, armor, surveillance equipment, and other mundane gear.
    """

    type = "hunter_gear"

    GEAR_TYPE_CHOICES = [
        ("weapon", "Weapon"),
        ("armor", "Armor"),
        ("surveillance", "Surveillance Equipment"),
        ("medical", "Medical Supplies"),
        ("occult", "Occult Tools"),
        ("transportation", "Transportation"),
        ("communication", "Communication Device"),
        ("utility", "Utility Equipment"),
    ]

    gear_type = models.CharField(
        max_length=50,
        choices=GEAR_TYPE_CHOICES,
        default="weapon",
        help_text="Type of equipment",
    )

    # Weapon stats (for weapons)
    damage = models.CharField(
        max_length=100,
        blank=True,
        help_text="Damage rating (e.g., 'Strength +2')",
    )

    range = models.CharField(
        max_length=100,
        blank=True,
        help_text="Effective range",
    )

    rate = models.CharField(
        max_length=100,
        blank=True,
        help_text="Rate of fire",
    )

    capacity = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ammunition capacity",
    )

    concealability = models.CharField(
        max_length=100,
        blank=True,
        help_text="Concealability rating",
    )

    # General stats
    availability = models.IntegerField(
        default=1,
        help_text="Resources dots needed to acquire (1-5)",
    )

    LEGALITY_CHOICES = [
        ("legal", "Legal"),
        ("restricted", "Restricted"),
        ("illegal", "Illegal"),
    ]

    legality = models.CharField(
        max_length=50,
        choices=LEGALITY_CHOICES,
        default="legal",
        help_text="Legal status",
    )

    requires_training = models.BooleanField(
        default=False,
        help_text="Requires specialized training to use effectively",
    )

    class Meta:
        verbose_name = "Hunter Gear"
        verbose_name_plural = "Hunter Gear"

    def get_update_url(self):
        return reverse("items:hunter:update:gear", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:hunter:create:gear")

    def get_heading(self):
        return "htr_heading"
