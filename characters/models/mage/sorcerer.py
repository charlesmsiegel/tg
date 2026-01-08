from collections import defaultdict

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.focus import Practice
from characters.models.mage.mtahuman import MtAHuman
from core.models import Model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse


class LinearMagicPath(Model):
    type = "linear_magic_path"
    gameline = "mta"

    freebie_step = 8

    numina_type = models.CharField(
        max_length=20,
        choices=[
            ("hedge_magic", "Hedge Magic"),
            ("psychic", "Psychic Phenomenon"),
        ],
        default="hedge_magic",
    )

    class Meta:
        verbose_name = "Linear Magic Path"
        verbose_name_plural = "Linear Magic Paths"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:mage:path", kwargs={"pk": self.pk})

    @property
    def property_name(self):
        return self.name.replace(" ", "_").replace(",", "_").replace("__", "_").lower()


class LinearMagicRitual(Model):
    type = "linear_magic_path"
    gameline = "mta"

    path = models.ForeignKey(LinearMagicPath, blank=True, null=True, on_delete=models.SET_NULL)
    level = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Linear Magic Ritual"
        verbose_name_plural = "Linear Magic Rituals"
        ordering = ["path", "level", "name"]

    def get_absolute_url(self):
        return reverse("characters:mage:ritual", kwargs={"pk": self.pk})


class Sorcerer(MtAHuman):
    type = "sorcerer"
    freebie_step = 8

    allowed_backgrounds = [
        "allies",
        "alternate_identity",
        "arcane",
        "artifact",
        "backup",
        "blessing",
        "certification",
        "chantry",
        "contacts",
        "cult",
        "demesne",
        "destiny",
        "dream",
        "enhancement",
        "fame",
        "familiar",
        "influence",
        "library",
        "mentor",
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
    ]

    fellowship = models.ForeignKey(
        SorcererFellowship,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sorcerer_affiliations",
    )

    sorcerer_type = models.CharField(
        max_length=20,
        choices=[
            ("hedge_mage", "Hedge Mage"),
            ("psychic", "Psychic"),
        ],
        default="hedge_mage",
    )

    paths = models.ManyToManyField(
        LinearMagicPath, blank=True, through="PathRating", related_name="known_to"
    )
    rituals = models.ManyToManyField(LinearMagicRitual, blank=True)

    affinity_path = models.ForeignKey(
        LinearMagicPath, blank=True, null=True, on_delete=models.SET_NULL
    )
    casting_attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL
    )
    quintessence = models.IntegerField(default=0)

    background_points = 5

    def freebie_costs(self):
        costs = super().freebie_costs()
        costs.update(
            {
                "path": 7,
                "ritual": 3,
            }
        )
        return costs

    class Meta:
        verbose_name = "Sorcerer"
        verbose_name_plural = "Sorcerers"

    def freebie_cost(self, trait):
        cost = super().freebie_cost(trait)
        if cost != 10000:
            return cost
        costs = defaultdict(
            lambda: 10000,
            {
                "path": 7,
                "ritual": 3,
            },
        )
        return costs[trait]

    def path_rating(self, path):
        ratings = PathRating.objects.filter(path=path, character=self)
        if not ratings.exists():
            return 0
        return ratings.first().rating

    def add_path(self, path, practice, ability):
        if self.path_rating(path) == 0:
            PathRating.objects.create(
                character=self, path=path, rating=1, practice=practice, ability=ability
            )
            return True
        pr = PathRating.objects.get(character=self, path=path)
        pr.rating += 1
        pr.save()
        return True

    def add_ritual(self, ritual):
        self.rituals.add(ritual)
        return True

    def get_quintessence_wheel(self):
        return list(range(10))

    def xp_cost(self, trait_type, trait_value):
        """XP costs for Sorcerer-specific traits."""
        sorcerer_costs = {
            "path": 7,  # 7 XP per existing path level
            "new_path": 10,  # 10 XP for new path at rating 1
            "ritual": 2,  # 2 XP per ritual level
        }
        if trait_type == "path" and trait_value == 0:
            return sorcerer_costs["new_path"]
        if trait_type in sorcerer_costs:
            return sorcerer_costs[trait_type] * trait_value
        return super().xp_cost(trait_type, trait_value)


class PathRating(models.Model):
    character = models.ForeignKey(Sorcerer, on_delete=models.SET_NULL, null=True)
    path = models.ForeignKey(LinearMagicPath, on_delete=models.SET_NULL, null=True)
    practice = models.ForeignKey(Practice, on_delete=models.SET_NULL, null=True)
    ability = models.ForeignKey(Ability, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Path Rating"
        verbose_name_plural = "Path Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="characters_mage_pathrating_rating_range",
                violation_error_message="Path rating must be between 0 and 10",
            ),
        ]

    def __str__(self):
        return f"{self.path}: {self.rating}"
