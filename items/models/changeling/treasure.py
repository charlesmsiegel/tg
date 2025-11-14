from django.db import models
from django.urls import reverse
from items.models.core import ItemModel


class Treasure(ItemModel):
    """
    Treasures are magically powerful items created or bound with Glamour.
    They represent enchanted artifacts available to Changelings.
    """

    type = "treasure"

    rating = models.IntegerField(
        default=1,
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text="1-2 dots: Minor, 3-4: Significant, 5: Legendary",
    )

    # Treasure type
    treasure_type = models.CharField(
        max_length=30,
        choices=[
            ("weapon", "Weapon"),
            ("armor", "Armor"),
            ("talisman", "Talisman"),
            ("wonder", "Wonder"),
            ("other", "Other"),
        ],
        blank=True,
        default="",
    )

    # Creation and properties
    creator = models.CharField(
        max_length=100, blank=True, default="", help_text="Who created this Treasure"
    )
    creation_method = models.TextField(
        blank=True, default="", help_text="How it was created"
    )
    permanence = models.BooleanField(
        default=True, help_text="Whether this Treasure is permanent"
    )

    # Abilities and effects
    effects = models.JSONField(
        default=list, help_text="List of special abilities/effects"
    )
    special_abilities = models.TextField(
        blank=True, default="", help_text="Description of special abilities"
    )

    # Glamour properties
    glamour_storage = models.IntegerField(
        default=0, help_text="If it can store Glamour, how much"
    )
    glamour_affinity = models.CharField(
        max_length=30,
        blank=True,
        default="",
        help_text="Type of Glamour it attracts or uses",
    )

    class Meta:
        verbose_name = "Treasure"
        verbose_name_plural = "Treasures"

    def get_update_url(self):
        return reverse("items:changeling:update:treasure", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:changeling:create:treasure")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        if self.name and self.rating:
            return f"{self.name} (★{'★' * (self.rating - 1)})"
        return super().__str__()
