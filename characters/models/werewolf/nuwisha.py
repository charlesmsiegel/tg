from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Nuwisha(Fera):
    """
    Nuwisha (werecoyotes) - The Tricksters
    Sacred clowns who teach through humor and pranks. They expose
    hypocrisy and remind others not to take themselves too seriously.
    Rare and solitary, with no formal tribes or structure.
    """

    type = "nuwisha"

    # Nuwisha breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("latrani", "Latrani"),  # Born coyote
    ]

    # Note: No metis - Nuwisha cannot breed with each other
    # Note: No tribes - all Nuwisha are solitary tricksters

    # Nuwisha "roles" (loose affiliations, not strict auspices)
    ROLES = [
        ("kojubat", "Kojubat"),  # Teachers
        ("kitmoti", "Kitmoti"),  # Tricksters
        ("umbagi", "Umbagi"),  # Warriors (rare)
    ]

    role = models.CharField(default="", max_length=100, choices=ROLES, blank=True)

    # Nuwisha renown (simplified)
    glory = models.IntegerField(default=0)
    humor = models.IntegerField(default=0)  # Unique to Nuwisha
    cunning = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Nuwisha"
        verbose_name_plural = "Nuwisha"

    def get_absolute_url(self):
        return reverse("characters:werewolf:nuwisha", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="nuwisha", condition=breed)[0]
        )
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="nuwisha", condition="nuwisha")[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(2)
        elif breed == "latrani":
            self.set_gnosis(5)

        # Nuwisha have moderate Rage
        self.set_rage(3)

        self.save()
        return True

    def has_role(self):
        return self.role != ""

    def set_role(self, role):
        if role:
            self.role = role
            self.gift_permissions.add(
                GiftPermission.objects.get_or_create(shifter="nuwisha", condition=role)[0]
            )
            self.save()
        return True
