from django.db import models

from items.models.mage.wonder import Wonder


class Fetish(Wonder):
    type = "fetish"
    gameline = "wta"

    gnosis = models.IntegerField(default=0)
    spirit = models.CharField(default="", max_length=100, blank=True)

    class Meta:
        verbose_name = "Fetish"
        verbose_name_plural = "Fetishes"

    def save(self, *args, **kwargs):
        self.background_cost = self.rank
        return super().save(*args, **kwargs)
