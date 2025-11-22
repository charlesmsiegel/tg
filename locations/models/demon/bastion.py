from django.db import models
from locations.models.core.location import LocationModel


class Bastion(LocationModel):
    """
    Bastion - fortified stronghold of the Earthbound

    Bastions are powerfully defended locations created through complex rituals.
    They serve as sanctuaries for Earthbound demons and their cults.
    """

    type = "bastion"

    # Bastion-specific fields
    ritual_strength = models.IntegerField(
        default=0, help_text="Strength of the ritual defenses (0-10)"
    )

    warding_level = models.IntegerField(
        default=0, help_text="Level of mystical warding protecting the bastion"
    )

    consecration_date = models.DateField(
        blank=True, null=True, help_text="Date when the bastion was consecrated"
    )

    class Meta:
        verbose_name = "Bastion"
        verbose_name_plural = "Bastions"

    def get_heading(self):
        return "dtf_heading"
