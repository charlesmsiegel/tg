from characters.models.core.attribute_block import Attribute
from core.models import Model
from django.db import models
from django.urls import reverse


class SorcererFellowship(Model):
    type = "sorcerer_fellowship"
    gameline = "mta"

    favored_attributes = models.ManyToManyField(Attribute, blank=True)
    favored_paths = models.ManyToManyField("characters.LinearMagicPath")

    class Meta:
        verbose_name = "Sorcerer Fellowship"
        verbose_name_plural = "Sorcerer Fellowships"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:mage:sorcerer_fellowship", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:sorcerer_fellowship", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:sorcerer_fellowship")
