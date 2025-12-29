from characters.models.core.statistic import Statistic
from django.urls import reverse


class Sphere(Statistic):
    type = "sphere"
    gameline = "mta"

    class Meta:
        verbose_name = "Sphere"
        verbose_name_plural = "Spheres"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:mage:sphere", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:mage:update:sphere", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:sphere")

    def get_heading(self):
        return "mta_heading"
