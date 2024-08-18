from django.db import models
from django.urls import reverse
from items.models.mage.wonder import Wonder


# Create your models here.
class Fetish(Wonder):
    type = "fetish"

    gnosis = models.IntegerField(default=0)
    spirit = models.CharField(default="", max_length=100)

    class Meta:
        verbose_name = "Fetish"
        verbose_name_plural = "Fetishes"

    def get_update_url(self):
        return reverse("items:werewolf:update:fetish", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:werewolf:create:fetish")

    def get_heading(self):
        return "wta_heading"

    def save(self, *args, **kwargs):
        self.background_cost = self.rank
        return super().save(*args, **kwargs)
