from django.db import models
from django.urls import reverse

from items.models.core import ItemModel


class Bloodstone(ItemModel):
    """
    Represents a Bloodstone (Thaumaturgy ritual item for storing blood).
    Created with the Craft Bloodstone ritual (Thaumaturgy Level 2).
    """

    type = "bloodstone"
    gameline = "vtm"

    # Blood storage
    blood_stored = models.IntegerField(
        default=0,
        help_text="Blood points currently stored",
    )

    max_blood = models.IntegerField(
        default=10,
        help_text="Maximum blood points that can be stored",
    )

    # Properties
    is_active = models.BooleanField(
        default=True,
        help_text="Bloodstone is active and functional",
    )

    # Creator information
    created_by_generation = models.IntegerField(
        default=13,
        help_text="Generation of vampire who created this bloodstone",
    )

    # Physical form
    stone_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Type of stone used (ruby, garnet, etc.)",
    )

    class Meta:
        verbose_name = "Bloodstone"
        verbose_name_plural = "Bloodstones"

    def get_update_url(self):
        return reverse("items:vampire:update:bloodstone", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:vampire:create:bloodstone")

    def add_blood(self, amount):
        """Add blood to the bloodstone, respecting max capacity."""
        if not self.is_active:
            return False
        potential_total = self.blood_stored + amount
        if potential_total <= self.max_blood:
            self.blood_stored = potential_total
            return True
        return False

    def remove_blood(self, amount):
        """Remove blood from the bloodstone."""
        if not self.is_active:
            return False
        if self.blood_stored >= amount:
            self.blood_stored -= amount
            return True
        return False
