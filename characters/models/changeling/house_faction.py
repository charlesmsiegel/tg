from core.models import Model
from django.urls import reverse


class HouseFaction(Model):
    type = "house_faction"
    gameline = "ctd"

    class Meta:
        verbose_name = "House Faction"
        verbose_name_plural = "House Factions"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:house_faction")

    def get_absolute_url(self):
        return reverse("characters:changeling:house_faction", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:changeling:update:house_faction", kwargs={"pk": self.pk})
