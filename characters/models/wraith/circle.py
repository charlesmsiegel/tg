from characters.models.core.group import Group
from django.urls import reverse


class Circle(Group):
    type = "circle"
    gameline = "wto"

    class Meta:
        verbose_name = "Circle"
        verbose_name_plural = "Circles"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:circle")

    def get_update_url(self):
        return reverse("characters:wraith:update:circle", kwargs={"pk": self.pk})
