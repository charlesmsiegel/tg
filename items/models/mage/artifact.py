from django.db import models
from django.urls import reverse

from characters.models.mage.effect import Effect
from items.models.mage.wonder import Wonder


class Artifact(Wonder):
    type = "artifact"

    power = models.ForeignKey(Effect, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Artifact"
        verbose_name_plural = "Artifacts"

    def get_update_url(self):
        return reverse("items:mage:update:artifact", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mage:create:artifact")

    def set_power(self, power):
        self.power = power
        self.save()
        return True

    def has_power(self):
        return self.power is not None
