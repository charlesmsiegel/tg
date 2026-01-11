from django.db import models
from django.urls import reverse

from items.models.mage.wonder import Wonder


class Fetish(Wonder):
    type = "fetish"
    gameline = "wta"

    gnosis = models.IntegerField(default=0)
    spirit = models.CharField(default="", max_length=100, blank=True)

    class Meta:
        verbose_name = "Fetish"
        verbose_name_plural = "Fetishes"

    def get_update_url(self):
        return reverse("items:werewolf:update:fetish", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:werewolf:create:fetish")

    def save(self, *args, **kwargs):
        self.background_cost = self.rank
        return super().save(*args, **kwargs)
