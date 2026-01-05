from characters.models.core import MeritFlaw
from characters.models.core.merit_flaw_block import MeritFlawBlock
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from core.models import BaseMeritFlawRating, BaseResonanceRating
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core import LocationModel
from locations.models.mage.reality_zone import RealityZone


class SizeChoices(models.IntegerChoices):
    TINY = -2, "Household Object"
    SMALL = -1, "Small Room"
    NORMAL = 0, "Average Room"
    LARGE = 1, "Small Building"
    HUGE = 2, "Large Building"


class RatioChoices(models.IntegerChoices):
    TINY = -2, "0.0"
    SMALL = -1, "0.25"
    NORMAL = 0, "0.5"
    LARGE = 1, "0.75"
    HUGE = 2, "1.0"


class Node(MeritFlawBlock, LocationModel):
    type = "node"
    gameline = "mta"

    rank = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    size = models.IntegerField(default=SizeChoices.NORMAL, choices=SizeChoices.choices)
    ratio = models.IntegerField(default=RatioChoices.NORMAL, choices=RatioChoices.choices)

    points = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    merits_and_flaws = models.ManyToManyField(MeritFlaw, blank=True, through="NodeMeritFlawRating")
    resonance = models.ManyToManyField(
        "characters.Resonance", blank=True, through="NodeResonanceRating"
    )

    quintessence_per_week = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tass_per_week = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tass_form = models.CharField(default="", max_length=100, blank=True)
    quintessence_form = models.CharField(default="", max_length=100, blank=True)
    reality_zone = models.ForeignKey(RealityZone, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"
        constraints = [
            CheckConstraint(
                check=Q(rank__gte=0, rank__lte=10),
                name="locations_node_rank_range",
                violation_error_message="Node rank must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(points__gte=0, points__lte=100),
                name="locations_node_points_range",
                violation_error_message="Node points must be between 0 and 100",
            ),
            CheckConstraint(
                check=Q(quintessence_per_week__gte=0, quintessence_per_week__lte=100),
                name="locations_node_quintessence_range",
                violation_error_message="Quintessence per week must be between 0 and 100",
            ),
            CheckConstraint(
                check=Q(tass_per_week__gte=0, tass_per_week__lte=100),
                name="locations_node_tass_range",
                violation_error_message="Tass per week must be between 0 and 100",
            ),
        ]

    def get_update_url(self):
        return reverse("locations:mage:update:node", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:node")

    def set_rank(self, rank):
        self.rank = rank
        self.points = 3 * self.rank
        return True

    # Merit/Flaw methods inherited from MeritFlawBlock:
    # - get_mf_and_rating_list()
    # - add_mf(mf, rating)
    # - mf_rating(mf)
    # - total_mf()
    # - total_merits()
    # - total_flaws()
    # - has_max_flaws()
    # - filter_mfs()

    def filter_mf(self, minimum=-10, maximum=10):
        """
        Filter available merits/flaws with min/max rating constraints.

        This extends the base filter_mfs() method with additional rating filtering.

        Args:
            minimum: Minimum rating value to include (default -10)
            maximum: Maximum rating value to include (default 10)

        Returns:
            QuerySet of MeritFlaw objects that can be added to this node
        """
        # Get base filtered queryset from MeritFlawBlock
        queryset = self.filter_mfs()
        # Apply additional min/max filters
        queryset = queryset.filter(max_rating__lte=maximum)
        queryset = queryset.filter(min_rating__gte=minimum)
        return queryset

    def add_resonance(self, resonance):
        r, _ = NodeResonanceRating.objects.get_or_create(resonance=resonance, node=self)
        if r.rating == 5:
            return False
        r.rating += 1
        r.save()
        return True

    def resonance_rating(self, resonance):
        if resonance in self.resonance.all():
            return NodeResonanceRating.objects.get(node=self, resonance=resonance).rating
        return 0

    def filter_resonance(self, minimum=0, maximum=5, sphere=None):
        all_res = Resonance.objects.all()
        if sphere is None:
            q = Q()
        else:
            q = Q(**{sphere: True})
        all_res = all_res.filter(q)

        maxed_resonance = [
            x.resonance.id
            for x in NodeResonanceRating.objects.filter(node=self, rating__gt=maximum)
        ]
        mined_resonance = [
            x.resonance.id
            for x in NodeResonanceRating.objects.filter(node=self, rating__lt=minimum)
        ]
        all_res = all_res.exclude(pk__in=maxed_resonance)
        all_res = all_res.exclude(pk__in=mined_resonance)
        if minimum > 0:
            all_res = all_res.filter(
                pk__in=[
                    x.resonance.id
                    for x in NodeResonanceRating.objects.filter(node=self, rating__gt=0)
                ]
            )
        return all_res

    def total_resonance(self):
        return sum(x.rating for x in NodeResonanceRating.objects.filter(node=self))

    def check_resonance(self, resonance, sphere=None):
        if self.resonance_rating(resonance) < 5:
            if sphere is None:
                return True
            return getattr(resonance, sphere)
        return False

    def resonance_postprocessing(self):
        if "Corrupted" in [x.name for x in self.merits_and_flaws.all()]:
            res, _ = Resonance.objects.get_or_create(name="Corrupted")
            self.add_resonance(res)
            self.add_resonance(res)
        if any([x.name.startswith("Sphere Attuned") for x in self.merits_and_flaws.all()]):
            for mf in [
                x for x in self.merits_and_flaws.all() if x.name.startswith("Sphere Attuned")
            ]:
                sphere_name = mf.name.split("(")[-1].split(")")[0]
                s = Sphere.objects.get(name=sphere_name)
                # Add a resonance attuned to this sphere
                sphere_resonances = Resonance.objects.filter(**{s.property_name: True})
                if sphere_resonances.exists():
                    self.add_resonance(sphere_resonances.first())

    def has_resonance(self):
        return self.total_resonance() >= self.rank

    def has_output_forms(self):
        return self.quintessence_form != "" and self.tass_form != ""

    def set_output_forms(self, quint_form, tass_form):
        self.quintessence_form = quint_form
        self.tass_form = tass_form
        return True

    def has_output(self):
        return self.quintessence_per_week != 0 or self.tass_per_week != 0

    def set_ratio(self, ratio):
        self.ratio = ratio
        return True

    def set_size(self, size):
        self.size = size
        return True

    def update_output(self):
        self.quintessence_per_week = int(self.points * float(self.get_ratio_display()))
        self.tass_per_week = self.points - self.quintessence_per_week
        return True


class NodeMeritFlawRating(BaseMeritFlawRating):
    """Through model for Node merit/flaw ratings."""

    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)
    mf = models.ForeignKey(MeritFlaw, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Node Merit or Flaw Rating"
        verbose_name_plural = "Node Merits and Flaws Rating"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=-10, rating__lte=10),
                name="locations_nodemeritflawrating_rating_range",
                violation_error_message="Node merit/flaw rating must be between -10 and 10",
            ),
        ]


class NodeResonanceRating(BaseResonanceRating):
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)
    resonance = models.ForeignKey(Resonance, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Node Resonance Rating"
        verbose_name_plural = "Node Resonance Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="locations_noderesonancerating_rating_range",
                violation_error_message="Node resonance rating must be between 0 and 10",
            ),
        ]

    def __str__(self):
        return f"{self.node}: {self.resonance} {self.rating}"
