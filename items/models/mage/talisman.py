from django.db import models

from characters.models.mage.effect import Effect
from items.models.mage.wonder import Wonder


class Talisman(Wonder):
    type = "talisman"

    arete = models.IntegerField(default=0)
    powers = models.ManyToManyField(Effect, blank=True)

    class Meta:
        verbose_name = "Talisman"
        verbose_name_plural = "Talismans"

    def add_power(self, power):
        self.powers.add(power)
        return True

    def has_powers(self):
        return self.powers.count() == self.rank
