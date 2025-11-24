from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Ananasi(Fera):
    """
    Ananasi (werespiders) - The Weavers
    Mysterious shapeshifters who serve the Weaver. They can take spider
    forms and are driven by duty and the need to maintain order.
    """

    type = "ananasi"

    # Ananasi breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("lilian", "Lilian"),  # Born spider
        ("ananasi", "Ananasi"),  # Born to two Ananasi
    ]

    # Ananasi aspects (like auspices)
    ASPECTS = [
        ("kumoti", "Kumoti"),  # Tricksters and spies
        ("tenere", "Tenere"),  # Warriors and protectors
        ("hatar", "Hatar"),  # Web-weavers and mystics
    ]

    aspect = models.CharField(default="", max_length=100, choices=ASPECTS)

    # Ananasi renown
    cunning = models.IntegerField(default=0)  # Cleverness and deceit
    obedience = models.IntegerField(default=0)  # Service to the Weaver
    wisdom = models.IntegerField(default=0)  # Knowledge and patience

    class Meta:
        verbose_name = "Ananasi"
        verbose_name_plural = "Ananasi"

    def get_absolute_url(self):
        return reverse("characters:werewolf:ananasi", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="ananasi", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(1)
        elif breed == "ananasi":
            self.set_gnosis(3)
        elif breed == "lilian":
            self.set_gnosis(5)

        self.save()
        return True

    def has_aspect(self):
        return self.aspect != ""

    def set_aspect(self, aspect):
        self.aspect = aspect
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="ananasi", condition=aspect)[0]
        )

        # Set starting Rage by aspect
        if aspect == "tenere":
            self.set_rage(4)
        elif aspect == "kumoti":
            self.set_rage(3)
        elif aspect == "hatar":
            self.set_rage(2)

        self.save()
        return True
