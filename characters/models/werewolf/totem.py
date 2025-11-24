from core.models import Model
from django.db import models
from django.urls import reverse


class Totem(Model):
    type = "totem"
    gameline = "wta"

    TYPES = [
        ("respect", "Respect"),
        ("war", "War"),
        ("wisdom", "Wisdom"),
        ("cunning", "Cunning"),
    ]

    cost = models.IntegerField(default=0)
    totem_type = models.CharField(max_length=20, choices=TYPES)
    individual_traits = models.TextField(default="")
    pack_traits = models.TextField(default="")
    ban = models.TextField(default="")

    class Meta:
        verbose_name = "Totem"
        verbose_name_plural = "Totems"

    def get_absolute_url(self):
        return reverse("characters:werewolf:totem", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:totem", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:totem")

    def get_heading(self):
        return "wta_heading"
