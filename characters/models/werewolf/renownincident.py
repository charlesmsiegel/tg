from characters.models.werewolf.rite import Rite
from core.models import Model
from django.db import models
from django.urls import reverse


class RenownIncident(Model):
    type = "renown_incident"
    gameline = "wta"

    glory = models.IntegerField(default=0)
    honor = models.IntegerField(default=0)
    wisdom = models.IntegerField(default=0)

    posthumous = models.BooleanField(default=False)
    only_once = models.BooleanField(default=False)
    breed = models.CharField(default="", max_length=10, blank=True)
    rite = models.ForeignKey(Rite, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Renown Incident"
        verbose_name_plural = "Renown Incidents"

    def get_absolute_url(self):
        return reverse("characters:werewolf:renownincident", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:renownincident", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:renownincident")
