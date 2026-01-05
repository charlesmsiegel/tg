from core.models import Model
from django.db import models
from django.urls import reverse


class GiftPermission(models.Model):
    shifter = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.shifter}/{self.condition}"


class Gift(Model):
    type = "gift"
    gameline = "wta"

    rank = models.IntegerField(default=0)
    allowed = models.ManyToManyField(GiftPermission, blank=True)

    class Meta:
        verbose_name = "Gift"
        verbose_name_plural = "Gifts"

    def get_absolute_url(self):
        return reverse("characters:werewolf:gift", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:gift", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:gift")
