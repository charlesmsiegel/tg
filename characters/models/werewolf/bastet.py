from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Bastet(Fera):
    """
    Bastet (werecats) - The Eyes of Gaia
    Solitary shapeshifters who take feline forms. They serve as scouts,
    spies, and keepers of secrets. Nine tribes exist worldwide.
    """

    type = "bastet"

    # Bastet tribes (9 tribes)
    TRIBES = [
        ("bagheera", "Bagheera"),  # Black panthers of India
        ("balam", "Balam"),  # Jaguars of Central/South America
        ("bubasti", "Bubasti"),  # Egyptian cats
        ("ceilican", "Ceilican"),  # Faerie cats of Europe
        ("khan", "Khan"),  # Tigers of Asia
        ("pumonca", "Pumonca"),  # Pumas of North America
        ("qualmi", "Qualmi"),  # Lynx of North America
        ("simba", "Simba"),  # Lions of Africa
        ("swara", "Swara"),  # Cheetahs of Africa
    ]

    # Bastet breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("feline", "Feline"),  # Born cat
        ("metis", "Metis"),  # Born to two Bastet
    ]

    # Pryio (Bastet auspice-like system based on moon)
    PRYIO = [
        ("daylight", "Daylight"),  # Solitary hunters
        ("twilight", "Twilight"),  # Between worlds
        ("midnight", "Midnight"),  # Mystics and seers
    ]

    tribe = models.CharField(default="", max_length=100, choices=TRIBES)
    pryio = models.CharField(default="", max_length=100, choices=PRYIO)

    # Bastet use a simplified renown system
    ferocity = models.IntegerField(default=0)  # Like Glory
    honor = models.IntegerField(default=0)  # Like Honor
    cunning = models.IntegerField(default=0)  # Like Wisdom

    class Meta:
        verbose_name = "Bastet"
        verbose_name_plural = "Bastet"

    def get_absolute_url(self):
        return reverse("characters:werewolf:bastet", kwargs={"pk": self.pk})

    def has_tribe(self):
        return self.tribe != ""

    def set_tribe(self, tribe):
        self.tribe = tribe
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="bastet", condition=tribe)[0]
        )
        self.save()
        return True

    def has_pryio(self):
        return self.pryio != ""

    def set_pryio(self, pryio):
        self.pryio = pryio
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="bastet", condition=pryio)[0]
        )
        self.save()
        return True

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="bastet", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(1)
        elif breed == "metis":
            self.set_gnosis(3)
        elif breed == "feline":
            self.set_gnosis(5)

        self.save()
        return True
