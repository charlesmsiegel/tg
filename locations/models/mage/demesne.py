from django.db import models
from django.urls import reverse
from locations.models.core.location import LocationModel
from locations.models.mage.reality_zone import RealityZone


class Demesne(LocationModel):
    type = "demesne"
    gameline = "mta"

    rank = models.IntegerField(default=0)
    reality_zone = models.ForeignKey(RealityZone, blank=True, null=True, on_delete=models.SET_NULL)
    size = models.CharField(
        max_length=100,
        blank=True,
        help_text="Approximate size of the demesne (e.g., 'Small chamber', 'Expansive realm')",
    )
    accessibility = models.CharField(
        max_length=20,
        choices=[
            ("easy", "Easy to Enter"),
            ("moderate", "Moderate Difficulty"),
            ("difficult", "Difficult to Enter"),
            ("private", "Private/Restricted"),
        ],
        default="moderate",
        help_text="How accessible the demesne is to outsiders",
    )

    class Meta:
        verbose_name = "Demesne"
        verbose_name_plural = "Demesnes"

    def get_update_url(self):
        return reverse("locations:mage:update:demesne", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:demesne")
