from django.db import models
from django.urls import reverse


class Medium(models.Model):
    type = "medium"

    name = models.TextField(default="")
    length_modifier_type = models.CharField(max_length=1, default="/", blank=True, null=True)
    length_modifier = models.IntegerField(default=1, blank=True, null=True)

    class Meta:
        verbose_name = "Medium"
        verbose_name_plural = "Media"

    def get_absolute_url(self):
        return reverse("items:medium", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("items:update:medium", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("items:create:medium")

    def __str__(self):
        return f"{self.name}"
