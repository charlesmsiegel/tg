from core.models import Model
from django.urls import reverse


class Archetype(Model):
    type = "archetype"
    gameline = "wod"

    class Meta:
        verbose_name = "Archetype"
        verbose_name_plural = "Archetypes"

    def get_absolute_url(self):
        return reverse("characters:archetype", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:update:archetype", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:create:archetype")
