from django.db import models
from django.urls import reverse
from locations.models.core.location import LocationModel
from locations.models.mage.reality_zone import RealityZone


class HorizonRealm(LocationModel):
    type = "horizon_realm"
    gameline = "mta"

    reality_zone = models.ForeignKey(RealityZone, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Horizon Realm"
        verbose_name_plural = "Horizon Realms"

    def get_update_url(self):
        return reverse("locations:mage:update:horizon_realm", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:horizon_realm")

    def get_heading(self):
        return "mta_heading"
