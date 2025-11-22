from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class Rack(LocationModel):
    """
    Represents a Rack (hunting/feeding ground for vampires).
    Part of the Herd Background but can also be a standalone location.
    """

    type = "rack"

    # Quality of feeding ground
    quality = models.IntegerField(
        default=1,
        help_text="Quality and safety of hunting (1-5 dots)",
    )

    # Population density
    population_density = models.IntegerField(
        default=1,
        help_text="Number of available vessels (1-5 dots)",
    )

    # Security/Risk
    risk_level = models.IntegerField(
        default=3,
        help_text="Risk of exposure or danger (1=very safe, 5=very dangerous)",
    )

    # Rack type
    rack_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="E.g., 'Nightclub', 'Hospital', 'Red light district', 'University'",
    )

    # Blood quality
    blood_quality = models.CharField(
        max_length=100,
        blank=True,
        help_text="Special qualities of blood available here",
    )

    # Special features
    is_protected = models.BooleanField(
        default=False,
        help_text="Protected by Kindred law or custom",
    )

    is_exclusive = models.BooleanField(
        default=False,
        help_text="Reserved for specific vampires",
    )

    is_contested = models.BooleanField(
        default=False,
        help_text="Multiple vampires claim rights here",
    )

    # Masquerade risk
    masquerade_risk = models.IntegerField(
        default=3,
        help_text="Risk of Masquerade breach (1=very low, 5=very high)",
    )

    class Meta:
        verbose_name = "Rack"
        verbose_name_plural = "Racks"

    def get_update_url(self):
        return reverse("locations:vampire:update:rack", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:vampire:create:rack")

    def get_heading(self):
        return "vtm_heading"

    def get_total_value(self):
        """Calculate the overall value of this rack."""
        value = self.quality + self.population_density
        value -= self.risk_level - 3  # Adjust for risk
        if self.is_protected:
            value += 1
        if self.is_exclusive:
            value += 1
        if self.is_contested:
            value -= 1
        return max(0, value)
