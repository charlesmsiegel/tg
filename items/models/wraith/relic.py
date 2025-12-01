from django.db import models
from django.urls import reverse
from items.models.core import ItemModel


class WraithRelic(ItemModel):
    type = "relic"
    gameline = "wto"

    level = models.IntegerField(default=1)
    background_cost = models.IntegerField(default=0)

    RELIC_TYPE_CHOICES = [
        ("common", "Common"),
        ("uncommon", "Uncommon"),
        ("rare", "Rare"),
        ("very_rare", "Very Rare"),
        ("legendary", "Legendary"),
    ]

    rarity = models.CharField(max_length=20, choices=RELIC_TYPE_CHOICES, default="common")

    # Properties
    pathos_cost = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = "Relic"
        verbose_name_plural = "Relics"

    def get_update_url(self):
        return reverse("items:wraith:update:relic", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:wraith:create:relic")

    def get_heading(self):
        return "wto_heading"

    def set_level(self, level):
        self.level = level
        self.background_cost = level
        return True

    def has_level(self):
        return self.level != 0

    def save(self, *args, **kwargs):
        self.background_cost = self.level
        return super().save(*args, **kwargs)
