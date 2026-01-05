from characters.models.core.group import Group
from django.urls import reverse


class Coterie(Group):
    type = "coterie"
    gameline = "vtm"

    class Meta:
        verbose_name = "Coterie"
        verbose_name_plural = "Coteries"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:coterie")

    def get_update_url(self):
        return reverse("characters:vampire:update:coterie", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("characters:vampire:coterie", kwargs={"pk": self.pk})
