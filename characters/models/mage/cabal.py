from characters.models.core.group import Group
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from core.utils import weighted_choice
from django.urls import reverse


class Cabal(Group):
    type = "cabal"
    gameline = "mta"

    class Meta:
        verbose_name = "Cabal"
        verbose_name_plural = "Cabals"

    def get_display_type(self):
        if self.leader is None:
            return "Cabal"
        if not Mage.objects.filter(pk=self.leader.pk).exists():
            return "Cabal"
        m = Mage.objects.get(pk=self.leader.pk)
        if m.affiliation == MageFaction.objects.get_or_create(name="Technocratic Union")[0]:
            return "Amalgam"
        return self.type.title()

    def get_update_url(self):
        return reverse("characters:mage:update:cabal", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:cabal")
