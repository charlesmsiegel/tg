from characters.models.core.character import Character
from characters.models.werewolf.charm import SpiritCharm
from django.db import models
from django.urls import reverse


class SpiritCharacter(Character):
    type = "spirit_character"

    gameline = "wta"

    willpower = models.IntegerField(default=0)
    rage = models.IntegerField(default=0)
    gnosis = models.IntegerField(default=0)
    essence = models.IntegerField(default=0)

    charms = models.ManyToManyField(SpiritCharm, blank=True)

    class Meta:
        verbose_name = "Spirit"
        verbose_name_plural = "Spirits"

    def get_update_url(self):
        return reverse("characters:werewolf:update:spirit", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:spirit")
