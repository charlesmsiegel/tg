from characters.models.werewolf.tribe import Tribe
from core.models import Model
from django.db import models
from django.urls import reverse


class Camp(Model):
    type = "camp"
    gameline = "wta"

    tribe = models.ForeignKey(Tribe, blank=True, null=True, on_delete=models.SET_NULL)
    camp_type = models.CharField(
        max_length=100,
        default="camp",
        choices=[
            ("camp", "Camp"),
            ("lodge", "Lodge"),
            ("house", "House"),
            ("philosophy", "Philosophy"),
        ],
    )

    class Meta:
        verbose_name = "Camp"
        verbose_name_plural = "Camps"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:camp")

    def get_absolute_url(self):
        return reverse("characters:werewolf:camp", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:camp", kwargs={"pk": self.pk})
