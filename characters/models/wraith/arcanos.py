from django.db import models
from django.urls import reverse

from core.models import Model


class Arcanos(Model):
    type = "arcanos"
    gameline = "wto"

    ARCANOS_TYPE_CHOICES = [
        ("standard", "Standard Arcanos"),
        ("dark", "Dark Arcanos"),
    ]

    arcanos_type = models.CharField(max_length=20, choices=ARCANOS_TYPE_CHOICES, default="standard")
    level = models.IntegerField(default=1)
    pathos_cost = models.IntegerField(default=0)
    angst_cost = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=6)
    description = models.TextField(default="")
    parent_arcanos = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="levels",
    )

    class Meta:
        verbose_name = "Arcanos"
        verbose_name_plural = "Arcanoi"

    def get_absolute_url(self):
        return reverse("characters:wraith:arcanos", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:wraith:update:arcanos", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:arcanos")
