from core.models import Model
from django.db import models
from django.urls import reverse


class Rite(Model):
    type = "rite"

    level = models.IntegerField(default=0)
    rite_type = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = "Rite"
        verbose_name_plural = "Rites"

    def get_absolute_url(self):
        return reverse("characters:werewolf:rite", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:rite", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:rite")

    def get_heading(self):
        return "wta_heading"
