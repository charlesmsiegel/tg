from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Kitsune(Fera):
    """
    Kitsune (werefoxes) - The Trickster Spirits
    Japanese shapeshifters who walk between worlds. Masters of illusion and
    deception, they serve the balance between the spirit and material realms.
    """

    type = "kitsune"

    # Kitsune breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("kitsune", "Kitsune"),  # Born fox
        ("kojin", "Kojin"),  # Born of spirits
    ]

    # Kitsune paths (like auspices)
    PATHS = [
        ("doshi", "Doshi"),  # Hermit scholars
        ("eji", "Eji"),  # Noble courtiers
        ("gukutsushi", "Gukutsushi"),  # Trickster puppeteers
    ]

    path = models.CharField(default="", max_length=100, choices=PATHS, blank=True)

    # Kitsune renown (Japanese-themed)
    chie = models.IntegerField(default=0)  # Wisdom
    toku = models.IntegerField(default=0)  # Virtue
    kagayaki = models.IntegerField(default=0)  # Glory

    class Meta:
        verbose_name = "Kitsune"
        verbose_name_plural = "Kitsune"

    def get_absolute_url(self):
        return reverse("characters:werewolf:kitsune", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="kitsune", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(2)
        elif breed == "kitsune":
            self.set_gnosis(4)
        elif breed == "kojin":
            self.set_gnosis(6)

        # Kitsune have low Rage
        self.set_rage(1)

        self.save()
        return True

    def has_path(self):
        return self.path != ""

    def set_path(self, path):
        self.path = path
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="kitsune", condition=path)[0]
        )
        self.save()
        return True
