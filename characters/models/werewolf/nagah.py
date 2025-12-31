from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Nagah(Fera):
    """
    Nagah (wereserpents) - The Silent Striders
    Secret assassins and spies who serve Gaia. They infiltrate corrupt
    organizations and eliminate threats. Masters of disguise and poison.
    """

    type = "nagah"

    # Nagah breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("balaram", "Balaram"),  # Born cobra
        ("vasuki", "Vasuki"),  # Born to two Nagah (naga)
    ]

    # Nagah auspices
    AUSPICES = [
        ("kamakshi", "Kamakshi"),  # Warriors
        ("kartikeya", "Kartikeya"),  # Judges
        ("kamsa", "Kamsa"),  # Seers
        ("kali", "Kali"),  # Assassins
    ]

    auspice = models.CharField(default="", max_length=100, choices=AUSPICES, blank=True)

    # Nagah renown
    obligation = models.IntegerField(default=0)  # Duty to Gaia
    wisdom = models.IntegerField(default=0)  # Knowledge and patience
    subtlety = models.IntegerField(default=0)  # Stealth and cunning

    class Meta:
        verbose_name = "Nagah"
        verbose_name_plural = "Nagah"

    def get_absolute_url(self):
        return reverse("characters:werewolf:nagah", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="nagah", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(2)
        elif breed == "vasuki":
            self.set_gnosis(4)
        elif breed == "balaram":
            self.set_gnosis(6)

        self.save()
        return True

    def has_auspice(self):
        return self.auspice != ""

    def set_auspice(self, auspice):
        self.auspice = auspice
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="nagah", condition=auspice)[0]
        )

        # Set starting Rage by auspice
        if auspice == "kamakshi":
            self.set_rage(4)
        elif auspice == "kali":
            self.set_rage(3)
        elif auspice == "kartikeya":
            self.set_rage(2)
        elif auspice == "kamsa":
            self.set_rage(1)

        self.save()
        return True
