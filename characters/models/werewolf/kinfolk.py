from django.db import models

from characters.models.core.derangement import Derangement
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.werewolf.gift import Gift, GiftPermission, gifts_by_rank
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman
from characters.rules.allocation import RuleViolation
from characters.rules.limits import KINFOLK_TRIBE_BACKGROUND_LIMITS
from items.models.werewolf.fetish import Fetish


class Kinfolk(WtAHuman):
    type = "kinfolk"

    allowed_backgrounds = ["allies", "contacts", "mentor", "pure_breed", "resources"]

    BREEDS = [
        ("homid", "Homid"),
        ("lupus", "Lupus"),
    ]

    breed = models.CharField(
        default="",
        max_length=100,
        choices=BREEDS,
        blank=True,
    )

    tribe = models.ForeignKey(Tribe, blank=True, null=True, on_delete=models.SET_NULL)

    relation = models.CharField(max_length=100, default="", blank=True)
    gifts = models.ManyToManyField(Gift, blank=True)

    gift_permissions = models.ManyToManyField(GiftPermission, blank=True)

    gnosis = models.IntegerField(default=0)
    fetishes_owned = models.ManyToManyField(Fetish, blank=True)

    glory = models.IntegerField(default=0)
    temporary_glory = models.IntegerField(default=0)
    wisdom = models.IntegerField(default=0)
    temporary_wisdom = models.IntegerField(default=0)
    honor = models.IntegerField(default=0)
    temporary_honor = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Kinfolk"
        verbose_name_plural = "Kinfolk"

    def add_mf(self, mf, rating):
        val = super().add_mf(mf, rating)
        if val:
            if mf.name == "Gnosis":
                self.gnosis = rating - 4
        return val

    def has_breed(self):
        return self.breed != ""

    def set_breed(self, breed):
        for b in self.BREEDS:
            self.gift_permissions.remove(
                GiftPermission.objects.get_or_create(shifter="werewolf", condition=b)[0]
            )
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="werewolf", condition=breed)[0]
        )

        self.breed = breed
        self.save()
        return True

    def has_tribe(self):
        return self.tribe is not None

    def set_tribe(self, tribe):
        for t in Tribe.objects.all():
            self.gift_permissions.remove(
                GiftPermission.objects.get_or_create(shifter="werewolf", condition=t.name)[0]
            )
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="werewolf", condition=tribe.name)[0]
        )

        if tribe.name == "Red Talons" and self.breed == "homid":
            return False
        self.tribe = tribe
        if self.tribe.name == "Silver Fangs" and self.pure_breed < 1:
            self.pure_breed = 1
        if self.tribe.name == "Black Spiral Dancers":
            derangement = Derangement.objects.first()
            if derangement:
                self.derangements.add(derangement)
        self.save()
        return True

    def gifts_by_rank(self):
        """Gifts grouped by rank, each labelled with its Tribe, Breed or Kinfolk source."""
        sources = {}
        if self.tribe_id:
            sources[self.tribe.name] = self.tribe.name
        if self.breed:
            sources[self.breed] = self.get_breed_display()
        sources["Kinfolk"] = "Kinfolk"
        return gifts_by_rank(self.gifts.all(), sources, "werewolf")

    def renown_tracks(self):
        """(label, permanent, temporary) for the sheet's Renown section."""
        return [
            ("Glory", self.glory, self.temporary_glory),
            ("Honor", self.honor, self.temporary_honor),
            ("Wisdom", self.wisdom, self.temporary_wisdom),
        ]

    def tribe_background_limits(self):
        if self.tribe is None:
            return {}
        return KINFOLK_TRIBE_BACKGROUND_LIMITS.get(self.tribe.name, {})

    def background_violations(self, ratings):
        """The first tribal restriction a chargen background allocation breaks."""
        limits = self.tribe_background_limits()
        if not limits:
            return []
        tribe = self.tribe.name
        for index, (background, rating) in enumerate(ratings):
            if rating == 0:
                continue
            if background.property_name in limits.get("forbidden", ()):
                message = f"{tribe} may not purchase {background.name}"
                return [(index, RuleViolation(message, field="bg"))]
            cap = limits.get("max", {}).get(background.property_name)
            if cap is not None and rating > cap:
                message = f"{tribe} may not purchase more than {cap} dots of {background.name}"
                return [(index, RuleViolation(message, field="rating"))]
        for name in limits.get("required", ()):
            if not any(bg.property_name == name and rating >= 1 for bg, rating in ratings):
                label = name.replace("_", " ").title()
                return [(0, RuleViolation(f"{tribe} must purchase at least 1 dot of {label}"))]
        return []

    def add_background(self, background, maximum=5):
        limits = self.tribe_background_limits()
        if background in limits.get("forbidden", ()):
            return False
        cap = limits.get("max", {}).get(background)
        if cap is not None and getattr(self, background, 0) == cap:
            return False
        return super().add_background(background, maximum=maximum)

    def filter_gifts(self):
        return Gift.objects.filter(rank__lte=1, allowed__in=self.gift_permissions.all()).exclude(
            pk__in=self.gifts.all()
        )

    def add_gift(self, gift):
        if gift in self.gifts.all():
            return False
        self.gifts.add(gift)
        self.save()
        return True

    def set_relation(self, relation):
        self.relation = relation
        return True

    def has_relation(self):
        return self.relation != ""

    def mf_based_corrections(self):
        if self.merits_and_flaws.filter(name="Gnosis").exists():
            gnosis = MeritFlaw.objects.get(name="Gnosis")
            rating = MeritFlawRating.objects.get(mf=gnosis, character=self).rating
            self.gnosis = rating - 4
        if self.merits_and_flaws.filter(name="Fetish").exists():
            fetish = Fetish.objects.first()
            if fetish:
                self.fetishes_owned.add(fetish)
        return super().mf_based_corrections()

    def add_fetish(self, fetish):
        if fetish in self.fetishes_owned.all():
            return False
        self.fetishes_owned.add(fetish)
        return True

    def filter_fetishes(self, min_rating=0, max_rating=5):
        return Fetish.objects.filter(rank__lte=max_rating, rank__gte=min_rating).exclude(
            pk__in=self.fetishes_owned.all()
        )
