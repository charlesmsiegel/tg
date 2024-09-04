from core.models import Model
from django.db import models
from django.urls import reverse


class BattleScar(Model):
    type = "battle_scar"

    glory = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Battle Scar"
        verbose_name_plural = "Battle Scars"

    def get_absolute_url(self):
        return reverse("characters:werewolf:battlescar", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:battlescar", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:battlescar")

    def get_heading(self):
        return "wta_heading"
