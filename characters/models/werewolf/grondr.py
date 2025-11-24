from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Grondr(Fera):
    """
    Grondr (wereboars) - The Lost Breed
    Extinct shapeshifters who were once fierce warriors. They fell to
    corruption and were destroyed. Only historical records remain.
    Useful for dark ages or alternate history chronicles.
    """

    type = "grondr"

    # Grondr breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("suidae", "Suidae"),  # Born boar
        ("metis", "Metis"),  # Born to two Grondr
    ]

    # Grondr auspices (based on seasons)
    AUSPICES = [
        ("spring", "Spring"),  # Planters and growers
        ("summer", "Summer"),  # Warriors and defenders
        ("autumn", "Autumn"),  # Harvesters and judges
        ("winter", "Winter"),  # Mystics and seers
    ]

    auspice = models.CharField(default="", max_length=100, choices=AUSPICES)

    # Grondr renown
    glory = models.IntegerField(default=0)  # Martial prowess
    honor = models.IntegerField(default=0)  # Integrity
    wisdom = models.IntegerField(default=0)  # Knowledge

    class Meta:
        verbose_name = "Grondr"
        verbose_name_plural = "Grondr"

    def get_absolute_url(self):
        return reverse("characters:werewolf:grondr", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="grondr", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(1)
        elif breed == "metis":
            self.set_gnosis(3)
        elif breed == "suidae":
            self.set_gnosis(5)

        self.save()
        return True

    def has_auspice(self):
        return self.auspice != ""

    def set_auspice(self, auspice):
        self.auspice = auspice
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="grondr", condition=auspice)[0]
        )

        # Set starting Rage by auspice
        if auspice == "summer":
            self.set_rage(4)
        elif auspice == "autumn":
            self.set_rage(3)
        elif auspice == "spring":
            self.set_rage(2)
        elif auspice == "winter":
            self.set_rage(2)

        self.save()
        return True
