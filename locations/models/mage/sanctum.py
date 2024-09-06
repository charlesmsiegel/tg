from django.db import models
from django.urls import reverse
from locations.models.core.location import LocationModel
from locations.models.mage.realityzone import RealityZone


class Sanctum(LocationModel):
    type = "sanctum"

    reality_zone = models.ForeignKey(
        RealityZone, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Sanctum"
        verbose_name_plural = "Sanctum"

    def get_update_url(self):
        return reverse("locations:mage:update:sanctum", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:sanctum")

    def get_heading(self):
        return "mta_heading"
