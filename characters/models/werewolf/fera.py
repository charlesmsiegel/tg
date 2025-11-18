from characters.models.werewolf.gift import Gift, GiftPermission
from characters.models.werewolf.rite import Rite
from characters.models.werewolf.wtahuman import WtAHuman
from core.utils import add_dot
from django.db import models
from django.urls import reverse
from items.models.werewolf.fetish import Fetish


class Fera(WtAHuman):
    """
    Base class for all Changing Breeds (Fera).
    Fera are shapeshifters other than Garou, each with unique cultures,
    abilities, and relationships to Gaia.
    """

    type = "fera"

    freebie_step = 8

    # Fera breed - varies by type
    breed = models.CharField(default="", max_length=100)

    # Most Fera have some form of tribal/aspect system
    faction = models.CharField(default="", max_length=100)

    # Fera use Rage, Gnosis, and Willpower like Garou
    gnosis = models.IntegerField(default=0)
    rage = models.IntegerField(default=0)

    # Most Fera have some form of renown, though it may differ from Garou
    renown = models.IntegerField(default=0)
    temporary_renown = models.IntegerField(default=0)

    # Gifts and supernatural abilities
    gifts = models.ManyToManyField(Gift, blank=True)
    rites_known = models.ManyToManyField(Rite, blank=True)
    fetishes_owned = models.ManyToManyField(Fetish, blank=True)

    # Story information
    first_change = models.TextField(default="")
    age_of_first_change = models.IntegerField(default=0)

    gift_permissions = models.ManyToManyField(GiftPermission, blank=True)

    class Meta:
        verbose_name = "Fera"
        verbose_name_plural = "Fera"

    def add_gift(self, gift):
        if gift in self.gifts.all():
            return False
        self.gifts.add(gift)
        self.save()
        return True

    def filter_gifts(self):
        return Gift.objects.filter(allowed__in=self.gift_permissions.all()).exclude(
            pk__in=self.gifts.all()
        )

    def add_rite(self, rite):
        self.rites_known.add(rite)
        self.save()
        return True

    def filter_rites(self):
        return Rite.objects.exclude(pk__in=self.rites_known.all())

    def add_gnosis(self):
        return add_dot(self, "gnosis", 10)

    def set_gnosis(self, gnosis):
        self.gnosis = gnosis
        self.save()
        return True

    def add_rage(self):
        return add_dot(self, "rage", 10)

    def set_rage(self, rage):
        self.rage = rage
        self.save()
        return True

    def add_fetish(self, fetish):
        if fetish in self.fetishes_owned.all():
            return False
        self.fetishes_owned.add(fetish)
        return True

    def has_breed(self):
        return self.breed != ""

    def has_faction(self):
        return self.faction != ""

    def filter_fetishes(self, min_rating=0, max_rating=5):
        return Fetish.objects.filter(
            rank__lte=max_rating, rank__gte=min_rating
        ).exclude(pk__in=self.fetishes_owned.all())

    def total_fetish_rating(self):
        return sum(x.rank for x in self.fetishes_owned.all())
