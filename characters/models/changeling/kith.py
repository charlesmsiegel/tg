from core.models import Model
from django.db import models
from django.urls import reverse


class Kith(Model):
    type = "kith"
    gameline = "ctd"

    affinity = models.CharField(max_length=20, default="", blank=True)
    birthrights = models.JSONField(default=list, blank=True)
    frailty = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "Kith"
        verbose_name_plural = "Kiths"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:kith")

    def get_absolute_url(self):
        return reverse("characters:changeling:kith", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:changeling:update:kith", kwargs={"pk": self.pk})

    def get_heading(self):
        return "ctd_heading"
