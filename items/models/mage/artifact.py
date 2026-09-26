from django.db import models

from characters.models.mage.effect import Effect
from items.models.mage.wonder import Wonder


class Artifact(Wonder):
    type = "artifact"

    power = models.ForeignKey(Effect, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Artifact"
        verbose_name_plural = "Artifacts"

    def set_power(self, power):
        self.power = power
        self.save()
        return True

    def has_power(self):
        return self.power is not None
