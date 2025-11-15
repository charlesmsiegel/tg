from items.models.core.weapon import Weapon


class ThrownWeapon(Weapon):
    type = "thrown_weapon"

    class Meta:
        verbose_name = "Thrown Weapon"
        verbose_name_plural = "Thrown Weapons"
