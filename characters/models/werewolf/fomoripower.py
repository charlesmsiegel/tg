from core.models import Model
from django.urls import reverse


class FomoriPower(Model):
    type = "fomoripower"

    class Meta:
        verbose_name = "Fomori Power"
        verbose_name_plural = "Fomori Powers"

    def get_absolute_url(self):
        return reverse("characters:werewolf:fomoripower", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:fomoripower", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:fomoripower")

    def get_heading(self):
        return "wta_heading"
