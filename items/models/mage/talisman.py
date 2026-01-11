from django.db import models
from django.urls import reverse

from characters.models.mage.effect import Effect
from items.models.mage.wonder import Wonder


class Talisman(Wonder):
    type = "talisman"

    arete = models.IntegerField(default=0)
    powers = models.ManyToManyField(Effect, blank=True)

    class Meta:
        verbose_name = "Talisman"
        verbose_name_plural = "Talismans"

    def get_update_url(self):
        return reverse("items:mage:update:talisman", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mage:create:talisman")

    def add_power(self, power):
        self.powers.add(power)
        return True

    def has_powers(self):
        return self.powers.count() == self.rank
