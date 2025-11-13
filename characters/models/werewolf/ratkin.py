from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import GiftPermission
from django.db import models
from django.urls import reverse


class Ratkin(Fera):
    """
    Ratkin (wererats) - Survivors and Plague-bringers
    Cunning shapeshifters who thrive in cities and sewers. They serve
    as Gaia's final solution - the cleanup crew after the Apocalypse.
    """

    type = "ratkin"

    # Ratkin breeds
    BREEDS = [
        ("homid", "Homid"),  # Born human
        ("rodent", "Rodent"),  # Born rat
        ("metis", "Metis"),  # Born to two Ratkin
    ]

    # Ratkin aspects (like auspices)
    ASPECTS = [
        ("tunnel_runner", "Tunnel Runner"),  # Scouts and spies
        ("warrior", "Warrior"),  # Soldiers
        ("plague_lord", "Plague Lord"),  # Disease-bringers
        ("tinkerer", "Tinkerer"),  # Inventors
        ("munchmausen", "Munchmausen"),  # Storytellers
        ("knife_skull", "Knife-Skull"),  # Assassins
        ("shadow_seer", "Shadow Seer"),  # Mystics
    ]

    # Ratkin colonies (like tribes)
    COLONIES = [
        ("rat_fink", "Rat Fink"),  # Urban survivors
        ("engineers", "Engineers"),  # Tech specialists
        ("plague_lords", "Plague Lords"),  # Disease specialists
        ("munchmausen", "Munchmausen"),  # Wanderers
        ("warriors", "Warriors"),  # Fighters
    ]

    aspect = models.CharField(default="", max_length=100, choices=ASPECTS)
    colony = models.CharField(default="", max_length=100, choices=COLONIES, blank=True)

    # Ratkin renown
    infamy = models.IntegerField(default=0)  # Like Glory
    obligation = models.IntegerField(default=0)  # Like Honor
    cunning = models.IntegerField(default=0)  # Like Wisdom

    class Meta:
        verbose_name = "Ratkin"
        verbose_name_plural = "Ratkin"

    def get_absolute_url(self):
        return reverse("characters:werewolf:ratkin", kwargs={"pk": self.pk})

    def set_breed(self, breed):
        self.breed = breed
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="ratkin", condition=breed)[0]
        )

        # Set starting Gnosis by breed
        if breed == "homid":
            self.set_gnosis(1)
        elif breed == "metis":
            self.set_gnosis(3)
        elif breed == "rodent":
            self.set_gnosis(5)

        self.save()
        return True

    def has_aspect(self):
        return self.aspect != ""

    def set_aspect(self, aspect):
        self.aspect = aspect
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="ratkin", condition=aspect)[0]
        )

        # Set starting Rage by aspect (varies)
        if aspect in ["warrior", "knife_skull"]:
            self.set_rage(4)
        elif aspect in ["tunnel_runner", "plague_lord"]:
            self.set_rage(3)
        else:
            self.set_rage(2)

        self.save()
        return True

    def has_colony(self):
        return self.colony != ""

    def set_colony(self, colony):
        self.colony = colony
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="ratkin", condition=colony)[0]
        )
        self.save()
        return True
