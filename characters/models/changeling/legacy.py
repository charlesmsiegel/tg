from core.models import Model
from django.db import models
from django.urls import reverse


class Legacy(Model):
    type = "legacy"
    gameline = "ctd"

    court = models.CharField(
        max_length=20,
        choices=[("seelie", "Seelie"), ("unseelie", "Unseelie")],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Legacy"
        verbose_name_plural = "Legacies"

    def get_absolute_url(self):
        return reverse("characters:changeling:legacy", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:legacy")

    def get_update_url(self):
        return reverse("characters:changeling:update:legacy", kwargs={"pk": self.pk})

    def get_heading(self):
        return "ctd_heading"
