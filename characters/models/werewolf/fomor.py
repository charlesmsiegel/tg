from django.db import models

from characters.models.werewolf.fomoripower import FomoriPower
from characters.models.werewolf.wtahuman import WtAHuman


class Fomor(WtAHuman):
    type = "fomor"

    rage = models.IntegerField(default=0)
    gnosis = models.IntegerField(default=0)
    powers = models.ManyToManyField(FomoriPower, blank=True)

    allowed_backgrounds = ["allies", "contacts", "resources"]

    background_points = 3

    class Meta:
        verbose_name = "Fomor"
        verbose_name_plural = "Fomori"

    def add_power(self, power):
        self.powers.add(power)
        return True

    def filter_powers(self):
        return FomoriPower.objects.exclude(pk__in=self.powers.all())
