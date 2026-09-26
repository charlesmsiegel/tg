from django.db import models

from .wonder import Wonder


class Charm(Wonder):
    type = "charm"

    arete = models.IntegerField(default=0)
    power = models.ForeignKey("characters.Effect", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Charm"
        verbose_name_plural = "Charms"

    def set_power(self, power):
        self.power = power
        return True

    def has_power(self):
        return self.power is not None
