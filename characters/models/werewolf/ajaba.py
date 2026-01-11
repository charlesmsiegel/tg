from django.db import models
from django.urls import reverse

from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission


class Ajaba(Fera):
    """
    Ajaba (werehyenas) - The Lost Hunters
    Nearly extinct shapeshifters of Africa. Once proud hunters, they were
    nearly destroyed by the Black Spiral Dancers. Few remain today.
    """

    type = "ajaba"

    # Ajaba breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("ajaba", "Ajaba"),  # Born hyena
        ("crocas", "Crocas"),  # Born to two Ajaba (metis)
    ]

    # Ajaba auspices (based on lunar cycle)
    AUSPICES = [
        ("new_moon", "New Moon"),  # Scouts and tricksters
        ("crescent_moon", "Crescent Moon"),  # Questioners
        ("half_moon", "Half Moon"),  # Judges
        ("gibbous_moon", "Gibbous Moon"),  # Moon dancers
        ("full_moon", "Full Moon"),  # Warriors
    ]

    auspice = models.CharField(default="", max_length=100, choices=AUSPICES, blank=True)

    # Ajaba renown
    ferocity = models.IntegerField(default=0)  # Savage strength
    obligation = models.IntegerField(default=0)  # Duty to the pack
    wisdom = models.IntegerField(default=0)  # Knowledge and cunning

    class Meta:
        verbose_name = "Ajaba"
        verbose_name_plural = "Ajaba"

    def get_absolute_url(self):
        return reverse("characters:werewolf:ajaba", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="ajaba", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(1)
        elif breed == "crocas":
            self.set_gnosis(3)
        elif breed == "ajaba":
            self.set_gnosis(5)

        self.save()
        return True

    def has_auspice(self):
        return self.auspice != ""

    def set_auspice(self, auspice):
        self.auspice = auspice
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="ajaba", condition=auspice)[0]
        )

        # Set starting Rage by auspice
        if auspice == "full_moon":
            self.set_rage(5)
        elif auspice == "gibbous_moon":
            self.set_rage(4)
        elif auspice == "half_moon":
            self.set_rage(3)
        elif auspice == "crescent_moon":
            self.set_rage(2)
        elif auspice == "new_moon":
            self.set_rage(1)

        self.save()
        return True
