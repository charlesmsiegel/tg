from django.db import models
from django.urls import reverse

from core.models import Model


class Specialty(Model):
    type = "specialty"
    gameline = "wod"

    stat = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"

    def display_stat(self):
        return self.stat.replace("_", " ").title()

    def get_absolute_url(self):
        return reverse("characters:specialty", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:update:specialty", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:create:specialty")

    def __str__(self):
        return f"{self.name} ({self.display_stat()})"
