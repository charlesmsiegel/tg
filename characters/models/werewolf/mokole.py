from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Mokole(Fera):
    """
    Mokole (weresaurians) - The Memory of Gaia
    Ancient shapeshifters who carry Gaia's memories from the age of
    dinosaurs. They can take reptilian forms and guard sacred knowledge.
    """

    type = "mokole"

    # Mokole breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("suchid", "Suchid"),  # Born reptile (crocodile, lizard, etc.)
        ("metis", "Metis"),  # Born to two Mokole (called "Unktehi")
    ]

    # Mokole streams (like tribes, based on region/culture)
    STREAMS = [
        ("makara", "Makara"),  # Indian/Asian
        ("zhong_lung", "Zhong Lung"),  # Chinese dragons
        ("gumagan", "Gumagan"),  # Australian
        ("mokolembembe", "Mokolembembe"),  # African
        ("decorated", "Decorated"),  # Native American
    ]

    # Mokole auspices (based on sun position)
    AUSPICES = [
        ("rising_sun", "Rising Sun"),  # Dawn - Warriors
        ("noonday_sun", "Noonday Sun"),  # Noon - Leaders
        ("setting_sun", "Setting Sun"),  # Dusk - Mystics
        ("shrouded_sun", "Shrouded Sun"),  # Twilight - Scholars
        ("midnight_sun", "Midnight Sun"),  # Night - Seers
        ("decorated_sun", "Decorated Sun"),  # Special - Elders
        ("solar_eclipse", "Solar Eclipse"),  # Rare - Chosen
    ]

    stream = models.CharField(default="", max_length=100, choices=STREAMS)
    auspice = models.CharField(default="", max_length=100, choices=AUSPICES)

    # Mokole renown
    valor = models.IntegerField(default=0)  # Courage
    harmony = models.IntegerField(default=0)  # Balance
    wisdom = models.IntegerField(default=0)  # Knowledge

    # Mnesis (racial memory) - unique to Mokole
    mnesis = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Mokole"
        verbose_name_plural = "Mokole"

    def get_absolute_url(self):
        return reverse("characters:werewolf:mokole", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="mokole", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(3)
        elif breed == "metis":
            self.set_gnosis(5)
        elif breed == "suchid":
            self.set_gnosis(7)

        self.save()
        return True

    def has_stream(self):
        return self.stream != ""

    def set_stream(self, stream):
        self.stream = stream
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="mokole", condition=stream)[0]
        )
        self.save()
        return True

    def has_auspice(self):
        return self.auspice != ""

    def set_auspice(self, auspice):
        self.auspice = auspice
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="mokole", condition=auspice)[
                0
            ]
        )

        # Set starting Rage by auspice
        if auspice == "rising_sun":
            self.set_rage(5)
        elif auspice == "noonday_sun":
            self.set_rage(4)
        elif auspice == "setting_sun":
            self.set_rage(3)
        elif auspice == "midnight_sun":
            self.set_rage(2)

        self.save()
        return True
