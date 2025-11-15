from items.models.core.weapon import Weapon


class MeleeWeapon(Weapon):
    type = "melee_weapon"

    class Meta:
        verbose_name = "Melee Weapon"
        verbose_name_plural = "Melee Weapons"
