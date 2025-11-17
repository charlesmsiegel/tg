from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Gurahl(Fera):
    """
    Gurahl (werebears) - The Healers and Protectors
    Powerful shapeshifters who heal the land and protect sacred places.
    Nearly extinct, working to restore their numbers and purpose.
    """

    type = "gurahl"

    # Gurahl breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("ursine", "Ursine"),  # Born bear
        ("arthren", "Arthren"),  # Born to two Gurahl (like metis)
    ]

    # Gurahl auspices (tied to seasons)
    AUSPICES = [
        ("arcas", "Arcas"),  # Summer - Warriors
        ("uzmati", "Uzmati"),  # Autumn - Judges
        ("kojubat", "Kojubat"),  # Winter - Seers
        ("kieh", "Kieh"),  # Spring - Healers
    ]

    auspice = models.CharField(default="", max_length=100, choices=AUSPICES)

    # Gurahl renown
    honor = models.IntegerField(default=0)
    succor = models.IntegerField(default=0)  # Healing and nurturing
    vision = models.IntegerField(default=0)  # Wisdom and foresight

    class Meta:
        verbose_name = "Gurahl"
        verbose_name_plural = "Gurahl"

    def get_absolute_url(self):
        return reverse("characters:werewolf:gurahl", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="gurahl", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(2)
        elif breed == "arthren":
            self.set_gnosis(4)
        elif breed == "ursine":
            self.set_gnosis(6)

        self.save()
        return True

    def has_auspice(self):
        return self.auspice != ""

    def set_auspice(self, auspice):
        self.auspice = auspice
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="gurahl", condition=auspice)[0]
        )

        # Set starting Rage by auspice
        if auspice == "arcas":
            self.set_rage(4)
        elif auspice == "uzmati":
            self.set_rage(3)
        elif auspice == "kojubat":
            self.set_rage(2)
        elif auspice == "kieh":
            self.set_rage(1)

        self.save()
        return True
