from characters.models.core.background_block import Background, BackgroundBlock
from characters.models.core.human import Human
from characters.models.mage.effect import Effect
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core.location import LocationModel


class Chantry(BackgroundBlock, LocationModel):
    allowed_backgrounds = [
        "allies",
        "arcane",
        "backup",
        "cult",
        "elders",
        "retainers",
        "spies",
        "resources",
        "enhancement",
        "requisitions",
        "sanctum",
        "node",
        "library",
    ]

    INTEGRATED_EFFECTS_NUMBERS = {
        0: 0,
        1: 4,
        2: 8,
        3: 15,
        4: 20,
        5: 25,
        6: 35,
        7: 45,
        8: 55,
        9: 70,
        10: 90,
    }

    type = "chantry"
    gameline = "mta"

    faction = models.ForeignKey(
        "characters.MageFaction", blank=True, null=True, on_delete=models.SET_NULL
    )

    LEADERSHIP_CHOICES = [
        ("panel", "Panel of Cabal Leaders"),
        ("teachers", "Teachers"),
        ("triumvirate", "Triumvirate"),
        ("democracy", "Democracy"),
        ("anarchy", "Anarchy"),
        ("single_deacon", "Single Deacon"),
        ("council_of_elders", "Council of Elders"),
        ("meritocracy", "Meritocracy"),
    ]

    leadership_type = models.CharField(
        max_length=20, null=True, choices=LEADERSHIP_CHOICES
    )
    leaders = models.ManyToManyField(
        Human, blank=True, related_name="chantry_leader_at"
    )

    SEASONS = [
        ("spring", "Spring"),
        ("winter", "Winter"),
        ("summer", "Summer"),
        ("autumn", "Autumn"),
    ]

    season = models.CharField(
        max_length=100,
        null=True,
        choices=SEASONS,
    )

    CHANTRY_TYPES = [
        ("exploration", "Exploration"),
        ("ancestral", "Ancestral"),
        ("hereditary", "Hereditary"),
        ("college", "College"),
        ("squatter", "Squatter"),
        ("war", "War"),
        ("library", "Library"),
        ("healing", "Healing"),
        ("research", "Research"),
        ("fortress", "Fortress"),
        ("diplomatic", "Diplomatic"),
    ]

    chantry_type = models.CharField(
        max_length=100,
        null=True,
        choices=CHANTRY_TYPES,
    )

    total_points = models.IntegerField(default=0)

    integrated_effects = models.ManyToManyField(Effect, blank=True)
    integrated_effects_score = models.IntegerField(default=0)

    members = models.ManyToManyField(Human, blank=True, related_name="member_of")
    cabals = models.ManyToManyField("characters.Cabal", blank=True)

    ambassador = models.ForeignKey(
        Human,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="ambassador_from",
    )
    node_tender = models.ForeignKey(
        Human,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="tends_node_at",
    )
    investigator = models.ManyToManyField(
        Human, blank=True, related_name="investigator_at"
    )
    guardian = models.ManyToManyField(Human, blank=True, related_name="guardian_of")
    teacher = models.ManyToManyField(Human, blank=True, related_name="teacher_at")

    factional_names = {
        "Akashayana": [
            "Monastery",
            "Torii",
            "Pagoda",
            "Bodhimandala",
            "Tao Chang",
            "Dojo",
            "Dojang",
            "Xiudaoyuan",
        ],
        "Celestial Chorus": ["Chapel", "Covenant", "Sanctuary", "Adytum", "Temple"],
        "Cult of Ecstasy": ["Pleasuredome"],
        "Dreamspeakers": ["Lodge"],
        "Euthanatos": ["Marabout"],
        "Order of Hermes": ["Covenant", "Chantry"],
        "Hollow Ones": ["Hideout", "Hole", "Crashspace", "Haunt"],
        "Society of Ether": ["Laboratory"],
        "Verbena": ["Covenhouse", "Circle", "Great Hall"],
        "Virtual Adepts": ["Epicenter", "Fortress", "Net"],
        "Traditions": ["Chantry"],
        "Technocratic Union": ["Construct"],
        "Kopa Loei": ["He'iau"],
    }

    class Meta:
        verbose_name = "Chantry"
        verbose_name_plural = "Chantries"

    def get_update_url(self):
        return reverse("locations:mage:update:chantry", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:chantry")

    def get_heading(self):
        return "mta_heading"

    @property
    def points(self):
        return self.total_points - self.total_cost()

    def bg_cost(self, background_rating):
        return (
            self.trait_cost(background_rating.bg.property_name)
            * background_rating.rating
        )

    def total_cost(self):
        tot = 0
        for bgr in self.backgrounds.all():
            tot += self.bg_cost(bgr)
        tot += self.integrated_effects_score * 2
        return tot

    def integrated_effects_number(self):
        return self.INTEGRATED_EFFECTS_NUMBERS[self.integrated_effects_score]

    def spent_integrated_effect_points(self):
        return sum([x.rote_cost for x in self.integrated_effects.all()])

    def current_ie_points(self):
        return self.integrated_effects_number() - self.spent_integrated_effect_points()

    @property
    def rank(self):
        if self.total_points < 11:
            return 1
        elif self.total_points < 21:
            return 2
        elif self.total_points < 31:
            return 3
        elif self.total_points < 71:
            return 4
        return 5

    def has_season(self):
        return self.season is not None

    def set_season(self, season):
        self.season = season
        self.save()
        return True

    def has_chantry_type(self):
        return self.chantry_type is not None

    def set_chantry_type(self, chantry_type):
        self.chantry_type = chantry_type
        if chantry_type == "library":
            self.library = 3
        self.save()
        return True

    def trait_cost(self, trait):
        if trait in [
            "allies",
            "arcane",
            "backup",
            "cult",
            "elders",
            "integrated_effects",
            "library",
            "retainers",
            "spies",
        ]:
            return 2
        if trait in ["node", "resources"]:
            return 3
        if trait in ["enhancement", "requisitions"]:
            return 4
        if trait in ["sanctum"]:
            return 5
        return 1000

    def points_spent(self):
        return (
            2
            * (
                self.allies
                + self.arcane
                + self.backup
                + self.cult
                + self.elders
                + self.integrated_effects
                + self.library
                + self.retainers
                + self.spies
            )
            + 3 * (self.node + self.resources)
            + 4 * (self.enhancement + self.requisitions)
            + 5 * (self.sanctum)
        )

    def has_node(self):
        return self.total_node() == self.node

    def add_node(self, node):
        self.nodes.add(node)
        self.save()

    def total_node(self):
        return sum(x.rank for x in self.nodes.all())

    def has_library(self):
        if self.chantry_library is not None:
            return self.chantry_library.rank == self.chantry_library.num_books()
        return False

    def set_library(self, library):
        self.chantry_library = library
        library.parent = self
        library.save()
        return True

    def set_rank(self, rank):
        self.rank = rank
        return True

    def get_traits(self):
        return {
            "allies": self.allies,
            "arcane": self.arcane,
            "backup": self.backup,
            "cult": self.cult,
            "elders": self.elders,
            "integrated_effects": self.integrated_effects,
            "retainers": self.retainers,
            "spies": self.spies,
            "resources": self.resources,
            "enhancement": self.enhancement,
            "requisitions": self.requisitions,
            "reality_zone": self.sanctum,
            "node": self.node,
            "library": self.library,
        }

    def set_faction(self, faction):
        self.faction = faction
        return True

    def has_faction(self):
        return self.faction is not None

    def get_independent_members(self):
        """Returns members who aren't part of any cabals in this chantry."""
        cabal_member_ids = set()
        for cabal in self.cabals.all():
            cabal_member_ids.update(cabal.members.values_list("id", flat=True))
        return self.members.exclude(id__in=cabal_member_ids)


class ChantryBackgroundRating(models.Model):
    bg = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True)
    chantry = models.ForeignKey(
        Chantry,
        on_delete=models.SET_NULL,
        null=True,
        related_name="backgrounds",
    )
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    note = models.CharField(default="", max_length=100)
    url = models.CharField(default="", max_length=500)
    complete = models.BooleanField(default=False)
    display_alt_name = models.BooleanField(default=False)

    class Meta:
        ordering = ["bg__name"]
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="locations_chantrybackgroundrating_rating_range",
                violation_error_message="Chantry background rating must be between 0 and 10",
            ),
        ]

    def __str__(self):
        return f"{self.bg} ({self.note})"

    def display_name(self):
        if self.bg.alternate_name == "":
            return self.bg.name
        elif self.display_alt_name:
            return self.bg.alternate_name
        return self.bg.name
