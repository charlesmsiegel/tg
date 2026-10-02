from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse

from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.mtahuman import MtAHuman
from characters.models.werewolf.charm import SpiritCharm
from core.models import Model, Number


class Advantage(Model):
    type = "advantage"

    ratings = models.ManyToManyField(Number, blank=True)
    max_rating = models.IntegerField(default=0)
    min_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Special Advantage"
        verbose_name_plural = "Special Advantage"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:mage:advantage", kwargs={"pk": self.pk})

    def update_max_rating(self):
        if not self.ratings.exists():
            self.max_rating = 0
        else:
            self.max_rating = max(self.ratings.all().values_list("value", flat=True))
        self.save()

    def update_min_rating(self):
        if not self.ratings.exists():
            self.min_rating = 0
        else:
            self.min_rating = min(self.ratings.all().values_list("value", flat=True))
        self.save()

    def get_ratings(self):
        tmp = list(self.ratings.all().values_list("value", flat=True))
        tmp.sort()
        return tmp

    def add_rating(self, number):
        n = Number.objects.get_or_create(value=number)[0]
        self.ratings.add(n)
        self.update_max_rating()
        self.update_min_rating()

    def add_ratings(self, num_list):
        for x in num_list:
            self.add_rating(x)


class Companion(MtAHuman):
    type = "companion"

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "arcane",
        "backup",
        "blessing",
        "certification",
        "chantry",
        "cult",
        "demesne",
        "destiny",
        "dream",
        "enhancement",
        "fame",
        "influence",
        "legend",
        "library",
        "node",
        "past_lives",
        "patron",
        "rank",
        "requisitions",
        "resources",
        "retainers",
        "sanctum",
        "secret_weapons",
        "spies",
        "status_background",
        "totem",
        "wonder",
    ]

    companion_type = models.CharField(
        max_length=20,
        choices=[
            ("companion", "Companion"),
            ("consor", "Consor"),
            ("familiar", "Familiar"),
        ],
        default="companion",
    )

    companion_of = models.ForeignKey(Human, blank=True, null=True, on_delete=models.SET_NULL)

    advantages = models.ManyToManyField(
        Advantage, blank=True, through="AdvantageRating", related_name="advantaged"
    )

    background_points = 5
    essence = models.IntegerField(default=0)
    rage = models.IntegerField(default=0)
    charms = models.ManyToManyField(SpiritCharm, blank=True)

    class Meta:
        verbose_name = "Companion"
        verbose_name_plural = "Companions"

    # Starting freebies by companion_type. The keys are preserved from the
    # original chargen step; see the Step 4 spec, defect D2 ("acoylte",
    # "backup" and "ally" are not companion_type choices).
    STARTING_FREEBIES = {"acoylte": 15, "backup": 15, "consor": 21, "ally": 21}
    FAMILIAR_FREEBIES = 25
    FAMILIAR_PACKAGE_FLAW = ("Thaumivore", -5)
    FAMILIAR_PACKAGE_ADVANTAGES = (("Bond-Sharing", 4), ("Paradox Nullification", 2))
    FAMILIAR_PACKAGE_CHARM = "Airt Sense"

    def get_update_url(self):
        # No chargen router is routed under update:companion; edit the full form.
        return self.get_full_update_url()

    def prepare_starting_freebies(self):
        """Set the chargen freebie budget; familiars also get their fixed package.

        A player familiar starts with 25 freebies (NPC familiars keep theirs),
        takes Thaumivore, Bond-Sharing, Paradox Nullification and Airt Sense,
        and the package costs one freebie net. Raises ``DoesNotExist`` when the
        package's reference rows are missing. The caller saves.
        """
        if self.companion_type in self.STARTING_FREEBIES:
            self.freebies = self.STARTING_FREEBIES[self.companion_type]
        elif self.companion_type == "familiar":
            if not self.npc:
                self.freebies = self.FAMILIAR_FREEBIES
            flaw_name, flaw_rating = self.FAMILIAR_PACKAGE_FLAW
            flaw = MeritFlaw.objects.get(name=flaw_name)
            advantages = [
                (Advantage.objects.get(name=name), rating)
                for name, rating in self.FAMILIAR_PACKAGE_ADVANTAGES
            ]
            charm = SpiritCharm.objects.get(name=self.FAMILIAR_PACKAGE_CHARM)
            self.add_mf(flaw, flaw_rating)
            self.spent_freebies.append(
                self.freebie_spend_record(flaw.name, "meritflaw", flaw_rating, cost=flaw_rating)
            )
            for advantage, rating in advantages:
                self.add_advantage(advantage, rating)
                self.spent_freebies.append(
                    self.freebie_spend_record(advantage.name, "advantage", rating, cost=rating)
                )
            self.add_charm(charm)
            self.freebies -= 1

    def add_advantage(self, advantage, rating):
        if rating in advantage.get_ratings():
            ar, _ = AdvantageRating.objects.get_or_create(character=self, advantage=advantage)
            ar.rating = rating
            ar.save()
            return True
        return False

    @property
    def advantage_ratings(self):
        """Special Advantage ratings with their advantage, for the sheet."""
        return (
            self.advantagerating_set.filter(advantage__isnull=False)
            .select_related("advantage")
            .order_by("advantage__name")
        )

    def get_advantage_and_rating_list(self):
        return [(x.name, self.advantage_rating(x)) for x in self.advantages.all()]

    def advantage_rating(self, advantage):
        if advantage not in self.advantages.all():
            return 0
        return AdvantageRating.objects.get(character=self, advantage=advantage).rating

    def add_charm(self, trait):
        if trait in self.charms.all():
            return False
        self.charms.add(trait)
        return True


class AdvantageRating(models.Model):
    character = models.ForeignKey(Companion, on_delete=models.SET_NULL, null=True)
    advantage = models.ForeignKey(Advantage, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Advantage Rating"
        verbose_name_plural = "Advantage Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="characters_mage_advantagerating_rating_range",
                violation_error_message="Advantage rating must be between 0 and 10",
            ),
        ]

    def __str__(self):
        return f"{self.advantage}: {self.rating}"
