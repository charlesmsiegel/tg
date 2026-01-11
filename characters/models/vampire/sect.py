from django.db import models
from django.urls import reverse

from core.models import Model


class VampireSect(Model):
    """
    Represents a Vampire Sect.
    Examples: Camarilla, Sabbat, Anarch Movement, Independent
    """

    type = "vampire_sect"
    gameline = "vtm"

    # Sect description
    philosophy = models.TextField(blank=True)

    class Meta:
        verbose_name = "Vampire Sect"
        verbose_name_plural = "Vampire Sects"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:vampire:sect", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:sect", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:sect")
