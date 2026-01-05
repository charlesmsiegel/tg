from characters.models.core import MeritFlaw
from characters.models.core.merit_flaw_block import MeritFlawBlock
from characters.models.mage.resonance import Resonance
from core.models import BaseMeritFlawRating
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core.location import LocationModel
from locations.models.mage.reality_zone import RealityZone


class SizeChoices(models.IntegerChoices):
    """Size of the Horizon Realm (5 points per dot)."""

    SINGLE_ROOM = 1, "A single room"
    SMALL_BUILDING = 2, "A small building and yard"
    LARGE_BUILDING = 3, "A large building and grounds"
    CITY = 4, "The size of a city"
    COUNTRY = 5, "The size of a country"
    WORLD = 6, "An entire world"


class EnvironmentChoices(models.IntegerChoices):
    """Environment type of the Horizon Realm (3 points per dot)."""

    SAME_AS_CONNECTION = 1, "Same as Primary Earthly Connection"
    SIMILAR_MUNDANE = 2, "Mundane environment similar to connection"
    ANY_MUNDANE = 3, "Any mundane Earthly environment"
    EXOTIC_MUNDANE = 4, "Mundane environment not found on Earth"
    SUBTLE_MAGICAL = 5, "Magical environment with subtle effects"
    ANYTHING_POSSIBLE = 6, "Anything is possible"


class HorizonRealm(MeritFlawBlock, LocationModel):
    """
    A Horizon Realm is a pocket dimension existing in the Umbra.

    Creating a Horizon Realm requires Spirit 5 and significant Quintessence investment.
    Horizon Realms can be substantial territories with their own physical laws,
    inhabitants, and histories.
    """

    type = "horizon_realm"
    gameline = "mta"

    # Core Statistics
    rank = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Realm power level (1-10). Higher ranks have more build points but higher maintenance.",
    )
    build_points = models.IntegerField(
        default=11,
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        help_text="Points available for purchasing traits (derived from rank).",
    )
    base_maintenance = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Base Quintessence per month needed to maintain the Realm.",
    )
    quintessence_maintenance = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Final Quintessence per month after all modifiers.",
    )

    # Primary Earthly Connection
    primary_earthly_connection = models.CharField(
        max_length=500,
        blank=True,
        help_text="The first place this Realm connected to on Earth. Influences default environment.",
    )

    # Structure Traits
    size = models.IntegerField(
        default=SizeChoices.SINGLE_ROOM,
        choices=SizeChoices.choices,
        help_text="Physical extent of the Realm (5 points per dot).",
    )
    environment = models.IntegerField(
        default=EnvironmentChoices.SAME_AS_CONNECTION,
        choices=EnvironmentChoices.choices,
        help_text="Type of environment in the Realm (3 points per dot).",
    )
    access_points = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Number of direct connections to the Realm (first one is free, 2 points each after).",
    )

    # Inhabitant Traits (each 0-5)
    plants = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Plant life level (0=none, 5=significantly magical). 2 points per dot.",
    )
    animals = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Animal life level (0=none, 5=significantly magical). 2 points per dot.",
    )
    people = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Human/intelligent being population (0=none, 5=mixed supernatural society). 5 points per dot.",
    )
    ephemera = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Incorporeal beings level (0=incidental, 5=diverse unique individuals). 4 points per dot.",
    )

    # Magick Traits
    resonance = models.ManyToManyField(Resonance, blank=True, through="HorizonRealmResonanceRating")
    reality_zone = models.ForeignKey(RealityZone, blank=True, null=True, on_delete=models.SET_NULL)

    # Security Traits
    guardians = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Guardian beings level. Each dot = 10 Freebie Points for building guardians. 3 points per dot.",
    )
    arcane = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="How hidden/forgettable the Realm is. 2 points per dot.",
    )

    # Merits and Flaws
    merits_and_flaws = models.ManyToManyField(
        MeritFlaw, blank=True, through="HorizonRealmMeritFlawRating"
    )

    class Meta:
        verbose_name = "Horizon Realm"
        verbose_name_plural = "Horizon Realms"
        constraints = [
            CheckConstraint(
                check=Q(rank__gte=1, rank__lte=10),
                name="locations_horizonrealm_rank_range",
                violation_error_message="Horizon Realm rank must be between 1 and 10",
            ),
            CheckConstraint(
                check=Q(build_points__gte=0, build_points__lte=200),
                name="locations_horizonrealm_build_points_range",
                violation_error_message="Build points must be between 0 and 200",
            ),
            CheckConstraint(
                check=Q(base_maintenance__gte=0, base_maintenance__lte=100),
                name="locations_horizonrealm_base_maintenance_range",
                violation_error_message="Base maintenance must be between 0 and 100",
            ),
            CheckConstraint(
                check=Q(quintessence_maintenance__gte=0, quintessence_maintenance__lte=100),
                name="locations_horizonrealm_quint_maintenance_range",
                violation_error_message="Quintessence maintenance must be between 0 and 100",
            ),
            CheckConstraint(
                check=Q(plants__gte=0, plants__lte=5),
                name="locations_horizonrealm_plants_range",
                violation_error_message="Plants must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(animals__gte=0, animals__lte=5),
                name="locations_horizonrealm_animals_range",
                violation_error_message="Animals must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(people__gte=0, people__lte=5),
                name="locations_horizonrealm_people_range",
                violation_error_message="People must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(ephemera__gte=0, ephemera__lte=5),
                name="locations_horizonrealm_ephemera_range",
                violation_error_message="Ephemera must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(guardians__gte=0, guardians__lte=10),
                name="locations_horizonrealm_guardians_range",
                violation_error_message="Guardians must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(arcane__gte=0, arcane__lte=5),
                name="locations_horizonrealm_arcane_range",
                violation_error_message="Arcane must be between 0 and 5",
            ),
        ]

    def get_update_url(self):
        return reverse("locations:mage:update:horizon_realm", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:horizon_realm")

    # Rank and Build Points
    RANK_BUILD_POINTS = {
        1: 11,
        2: 22,
        3: 33,
        4: 44,
        5: 55,
        6: 70,
        7: 85,
        8: 100,
        9: 115,
        10: 150,
    }

    RANK_BASE_MAINTENANCE = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 10,
        7: 15,
        8: 20,
        9: 25,
        10: 50,
    }

    def set_rank(self, rank):
        """Set the rank and update build points and base maintenance accordingly."""
        self.rank = rank
        self.build_points = self.RANK_BUILD_POINTS.get(rank, 11)
        self.base_maintenance = self.RANK_BASE_MAINTENANCE.get(rank, 1)
        self.quintessence_maintenance = self.base_maintenance
        return True

    # Point Cost Calculations
    def structure_cost(self):
        """Calculate total structure cost: Size (5/dot) + Environment (3/dot) + Access Points (2 each after first)."""
        size_cost = self.size * 5
        environment_cost = self.environment * 3
        access_cost = max(0, self.access_points - 1) * 2
        return size_cost + environment_cost + access_cost

    def inhabitants_cost(self):
        """Calculate total inhabitants cost: Plants (2/dot) + Animals (2/dot) + People (5/dot) + Ephemera (4/dot)."""
        return (self.plants * 2) + (self.animals * 2) + (self.people * 5) + (self.ephemera * 4)

    def security_cost(self):
        """Calculate total security cost: Guardians (3/dot) + Arcane (2/dot)."""
        return (self.guardians * 3) + (self.arcane * 2)

    def total_cost(self):
        """Calculate total build point cost."""
        return self.structure_cost() + self.inhabitants_cost() + self.security_cost()

    def remaining_points(self):
        """Calculate remaining build points after all purchases."""
        return self.build_points - self.total_cost()

    # Resonance Methods
    def add_resonance(self, resonance):
        """Add or increase resonance rating by 1."""
        r, _ = HorizonRealmResonanceRating.objects.get_or_create(
            resonance=resonance, horizon_realm=self
        )
        if r.rating >= 5:
            return False
        r.rating += 1
        r.save()
        return True

    def resonance_rating(self, resonance):
        """Get the rating for a specific resonance."""
        if resonance in self.resonance.all():
            return HorizonRealmResonanceRating.objects.get(
                horizon_realm=self, resonance=resonance
            ).rating
        return 0

    def total_resonance(self):
        """Get the sum of all resonance ratings."""
        return sum(x.rating for x in HorizonRealmResonanceRating.objects.filter(horizon_realm=self))

    def has_resonance(self):
        """Check if the Realm has sufficient resonance (at least rank dots)."""
        return self.total_resonance() >= self.rank

    # Merit/Flaw filter extension
    def filter_mf(self, minimum=-10, maximum=10):
        """Filter available merits/flaws with min/max rating constraints."""
        queryset = self.filter_mfs()
        queryset = queryset.filter(max_rating__lte=maximum)
        queryset = queryset.filter(min_rating__gte=minimum)
        return queryset


class HorizonRealmMeritFlawRating(BaseMeritFlawRating):
    """Through model for Horizon Realm merit/flaw ratings."""

    horizon_realm = models.ForeignKey(HorizonRealm, on_delete=models.SET_NULL, null=True)
    mf = models.ForeignKey(MeritFlaw, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Horizon Realm Merit or Flaw Rating"
        verbose_name_plural = "Horizon Realm Merits and Flaws Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=-10, rating__lte=10),
                name="locations_horizonrealmmeritflawrating_rating_range",
                violation_error_message="Horizon Realm merit/flaw rating must be between -10 and 10",
            ),
        ]


class HorizonRealmResonanceRating(models.Model):
    """Through model for Horizon Realm resonance ratings."""

    horizon_realm = models.ForeignKey(HorizonRealm, on_delete=models.SET_NULL, null=True)
    resonance = models.ForeignKey(Resonance, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Horizon Realm Resonance Rating"
        verbose_name_plural = "Horizon Realm Resonance Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="locations_horizonrealmresonancerating_rating_range",
                violation_error_message="Horizon Realm resonance rating must be between 0 and 10",
            ),
        ]

    def __str__(self):
        return f"{self.horizon_realm}: {self.resonance} {self.rating}"
