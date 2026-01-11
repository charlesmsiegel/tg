from django.db import models
from django.urls import reverse

from characters.models.werewolf.gift import Gift, GiftPermission
from core.models import Model


class Tribe(Model):
    type = "tribe"
    gameline = "wta"

    willpower = models.IntegerField(default=3)

    class Meta:
        verbose_name = "Tribe"
        verbose_name_plural = "Tribes"

    def get_absolute_url(self):
        return reverse("characters:werewolf:tribe", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:tribe", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:tribe")

    def get_camps(self):
        from characters.models.werewolf.camp import Camp

        return Camp.objects.filter(tribe=self)

    def get_gifts_by_rank(self, rank):
        tribe_permission = GiftPermission.objects.get(shifter="werewolf", condition=self.name)
        return Gift.objects.filter(rank=rank, allowed=tribe_permission)

    @property
    def gifts_1(self):
        return self.get_gifts_by_rank(1)

    @property
    def gifts_2(self):
        return self.get_gifts_by_rank(2)

    @property
    def gifts_3(self):
        return self.get_gifts_by_rank(3)

    @property
    def gifts_4(self):
        return self.get_gifts_by_rank(4)

    @property
    def gifts_5(self):
        return self.get_gifts_by_rank(5)

    @property
    def gifts_6(self):
        return self.get_gifts_by_rank(6)
