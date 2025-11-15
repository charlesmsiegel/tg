from django.db import models
from django.urls import reverse
from items.models.core.item import ItemModel


class Weapon(ItemModel):
    type = "weapon"

    class Meta:
        verbose_name = "Weapon"
        verbose_name_plural = "Weapons"

    difficulty = models.IntegerField(default=0)
    damage = models.IntegerField(default=0)
    damage_type = models.CharField(
        max_length=1,
        default="L",
        choices=[("B", "Bashing"), ("L", "Lethal"), ("A", "Aggravated")],
    )
    conceal = models.CharField(
        max_length=1,
        default="P",
        choices=[
            ("P", "Pocket"),
            ("J", "Jacket"),
            ("T", "Trenchcoat"),
            ("N", "Not Applicable"),
        ],
    )

    def get_update_url(self):
        return reverse(f"items:update:{self.type}", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse(f"items:create:{cls.type}")
