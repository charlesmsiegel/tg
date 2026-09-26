from django.db import models

from core.registry_urls import RegistryURLMixin


class Medium(RegistryURLMixin, models.Model):
    type = "medium"

    name = models.TextField(default="")
    length_modifier_type = models.CharField(max_length=1, default="/", blank=True, null=True)
    length_modifier = models.IntegerField(default=1, blank=True, null=True)

    class Meta:
        verbose_name = "Medium"
        verbose_name_plural = "Media"

    def __str__(self):
        return f"{self.name}"
