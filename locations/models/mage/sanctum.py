from django.db import models

from locations.models.core.location import LocationModel
from locations.models.mage.reality_zone import RealityZone


class Sanctum(LocationModel):
    type = "sanctum"
    gameline = "mta"

    rank = models.IntegerField(default=0)
    reality_zone = models.ForeignKey(RealityZone, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Sanctum"
        verbose_name_plural = "Sanctum"
