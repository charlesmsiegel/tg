from django.db import models

from core.registry_urls import RegistryURLMixin


class Material(RegistryURLMixin, models.Model):
    type = "material"

    name = models.TextField(default="")
    is_hard = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def __str__(self):
        return f"{self.name}"
