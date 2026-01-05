from django.db import models
from django.urls import reverse
from items.models.mage.wonder import Wonder


class Talen(Wonder):
    """
    Talens are one-use spirit-infused items. Unlike Fetishes, which can be
    used multiple times, Talens are consumed or destroyed after a single use.
    """

    type = "talen"
    gameline = "wta"

    gnosis = models.IntegerField(default=0)
    spirit = models.CharField(default="", max_length=200, blank=True)

    class Meta:
        verbose_name = "Talen"
        verbose_name_plural = "Talens"

    def get_update_url(self):
        return reverse("items:werewolf:update:talen", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:werewolf:create:talen")

    def save(self, *args, **kwargs):
        # Talens typically cost Background points equal to their rank
        self.background_cost = self.rank
        return super().save(*args, **kwargs)
