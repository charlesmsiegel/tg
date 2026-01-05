from characters.models.core.group import Group
from django.urls import reverse


class Motley(Group):
    type = "motley"
    gameline = "ctd"

    class Meta:
        verbose_name = "Motley"
        verbose_name_plural = "Motleys"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:motley")

    def get_update_url(self):
        return reverse("characters:changeling:update:motley", kwargs={"pk": self.pk})
