from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Rokea(Fera):
    """
    Rokea (weresharks) - The Warriors of the Sea
    Primal shapeshifters who patrol the oceans. They are solitary hunters
    with fierce territorial instincts and little contact with land-based shifters.
    """

    type = "rokea"

    # Rokea breeds (Metis are killed at birth in Rokea culture)
    BREEDS = [
        ("homid", "Homid"),  # Born human (Same-Bito)
        ("squamus", "Squamus"),  # Born shark
    ]

    # Rokea auspices (based on time of birth)
    AUSPICES = [
        ("brightwater", "Brightwater"),  # Born during day - warriors
        ("darkwater", "Darkwater"),  # Born at night - mystics
    ]

    auspice = models.CharField(default="", max_length=100, choices=AUSPICES, blank=True)

    # Rokea renown
    valor = models.IntegerField(default=0)  # Courage and ferocity
    harmony = models.IntegerField(default=0)  # Balance with the Sea
    innovation = models.IntegerField(default=0)  # Adaptation and learning

    class Meta:
        verbose_name = "Rokea"
        verbose_name_plural = "Rokea"

    def get_absolute_url(self):
        return reverse("characters:werewolf:rokea", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="rokea", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(1)
        elif breed == "squamus":
            self.set_gnosis(5)

        # Rokea have high starting Rage
        self.set_rage(5)

        self.save()
        return True

    def has_auspice(self):
        return self.auspice != ""

    def set_auspice(self, auspice):
        self.auspice = auspice
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="rokea", condition=auspice)[0]
        )
        self.save()
        return True
