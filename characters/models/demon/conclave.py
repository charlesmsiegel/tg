from characters.models.core.group import Group
from django.urls import reverse


class Conclave(Group):
    type = "conclave"
    gameline = "dtf"

    class Meta:
        verbose_name = "Conclave"
        verbose_name_plural = "Conclaves"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:conclave")

    def get_update_url(self):
        return reverse("characters:demon:update:conclave", kwargs={"pk": self.pk})
