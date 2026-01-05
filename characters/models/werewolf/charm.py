from core.models import Model
from django.db import models
from django.urls import reverse


class SpiritCharm(Model):
    type = "spirit_charm"
    gameline = "wta"

    essence_cost = models.IntegerField(default=0)
    point_cost = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Spirit Charm"
        verbose_name_plural = "Spirit Charms"

    def get_absolute_url(self):
        return reverse("characters:werewolf:spirit_charm", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:spirit_charm", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:spirit_charm")
