from django.db import models
from django.urls import reverse


class Pact(models.Model):
    """Through table for Demon-Thrall many-to-many relationship with pact details."""

    demon = models.ForeignKey("Demon", on_delete=models.CASCADE, null=True)
    thrall = models.ForeignKey("Thrall", on_delete=models.CASCADE, null=True)

    terms = models.TextField(default="", blank=True)
    faith_payment = models.IntegerField(default=0)  # How much Faith thrall provides per interval
    enhancements = models.JSONField(
        default=list, blank=True
    )  # List of enhancements granted (list is callable - safe)

    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Pact"
        verbose_name_plural = "Pacts"

    def __str__(self):
        demon_name = self.demon.name if self.demon else "No Demon"
        thrall_name = self.thrall.name if self.thrall else "No Thrall"
        return f"Pact: {demon_name} <-> {thrall_name}"

    def get_absolute_url(self):
        return reverse("characters:demon:pact", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:pact", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:pact")
