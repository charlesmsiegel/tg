from django.db import models
from django.urls import reverse

from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission


class Corax(Fera):
    """
    Corax (wereravens) - The Eyes of Helios
    Messengers and spies who serve the sun god Helios. They gather
    secrets and spread information. No tribes - all Corax are one people.
    """

    type = "corax"

    # Corax breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("corvid", "Corvid"),  # Born raven
    ]

    # Note: No metis - Corax cannot breed with each other
    # Note: No tribes - all Corax are one unified group

    # Corax are driven by curiosity and knowledge
    curiosity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Corax"
        verbose_name_plural = "Corax"

    def get_absolute_url(self):
        return reverse("characters:werewolf:corax", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="corax", condition=breed)[0]
        )
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="corax", condition="corax")[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(3)
        elif breed == "corvid":
            self.set_gnosis(6)

        # Corax start with low Rage
        self.set_rage(1)

        self.save()
        return True
