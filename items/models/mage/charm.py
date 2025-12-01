from django.db import models
from django.urls import reverse

from .wonder import Wonder


class Charm(Wonder):
    type = "charm"

    arete = models.IntegerField(default=0)
    power = models.ForeignKey("characters.Effect", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Charm"
        verbose_name_plural = "Charms"

    def get_update_url(self):
        return reverse("items:mage:update:charm", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mage:create:charm")

    def set_power(self, power):
        self.power = power
        return True

    def has_power(self):
        return self.power is not None
