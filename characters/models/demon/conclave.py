from characters.models.core.group import Group
from django.urls import reverse


class Conclave(Group):
    type = "conclave"

    class Meta:
        verbose_name = "Conclave"
        verbose_name_plural = "Conclaves"

    def get_heading(self):
        return "dtf_heading"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:conclave")

    def get_update_url(self):
        return reverse("characters:demon:update:conclave", kwargs={"pk": self.pk})
