from django.db import models

from items.models.core.weapon import Weapon


class RangedWeapon(Weapon):
    type = "ranged_weapon"

    range = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    clip = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Ranged Weapon"
        verbose_name_plural = "Ranged Weapons"
