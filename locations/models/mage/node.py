from characters.models.core import MeritFlaw
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from django.db import models
from django.db.models import F, Q, CheckConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from game.models import ObjectType
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


class Node(LocationModel):
    type = "node"

    rank = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    size = models.IntegerField(default=SizeChoices.NORMAL, choices=SizeChoices.choices)
    ratio = models.IntegerField(
        default=RatioChoices.NORMAL, choices=RatioChoices.choices
    )

    points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    merits_and_flaws = models.ManyToManyField(
        MeritFlaw, blank=True, through="NodeMeritFlawRating"
    )
    resonance = models.ManyToManyField(
        "characters.Resonance", blank=True, through="NodeResonanceRating"
    )

    quintessence_per_week = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tass_per_week = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tass_form = models.CharField(default="", max_length=100)
    quintessence_form = models.CharField(default="", max_length=100)
    reality_zone = models.ForeignKey(
        RealityZone, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"
        constraints = [
            CheckConstraint(
                check=Q(rank__gte=0, rank__lte=10),
                name='locations_node_rank_range',
                violation_error_message="Node rank must be between 0 and 10"
            ),
            CheckConstraint(
                check=Q(points__gte=0, points__lte=100),
                name='locations_node_points_range',
                violation_error_message="Node points must be between 0 and 100"
            ),
            CheckConstraint(
                check=Q(quintessence_per_week__gte=0, quintessence_per_week__lte=100),
                name='locations_node_quintessence_range',
                violation_error_message="Quintessence per week must be between 0 and 100"
            ),
            CheckConstraint(
                check=Q(tass_per_week__gte=0, tass_per_week__lte=100),
                name='locations_node_tass_range',
                violation_error_message="Tass per week must be between 0 and 100"
            ),
        ]

    def get_update_url(self):
        return reverse("locations:mage:update:node", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:node")

    def get_heading(self):
        return "mta_heading"

    def set_rank(self, rank):
        self.rank = rank
        self.points = 3 * self.rank
        return True

    def get_mf_and_rating_list(self):
        return [(x, self.mf_rating(x)) for x in self.merits_and_flaws.all()]

    def add_mf(self, mf, rating):
        node = ObjectType.objects.get_or_create(
            name="node", type="loc", gameline="mta"
        )[0]
        if node not in mf.allowed_types.all():
            return False
        if not mf.ratings.filter(value=rating).exists():
            return False
        if mf in self.merits_and_flaws.all():
            current_rating = NodeMeritFlawRating.objects.get(node=self, mf=mf).rating
            if 0 < current_rating < rating:
                x = NodeMeritFlawRating.objects.get(node=self, mf=mf)
                x.rating = rating
                x.save()
                return True
            if 0 > current_rating > rating:
                x = NodeMeritFlawRating.objects.get(node=self, mf=mf)
                x.rating = rating
                x.save()
                return True
            return False
        NodeMeritFlawRating.objects.create(node=self, mf=mf, rating=rating)
        return True

    def total_mf(self):
        return sum(x.rating for x in NodeMeritFlawRating.objects.filter(node=self))

    def filter_mf(self, minimum=-10, maximum=10):
        node = ObjectType.objects.get_or_create(
            name="node", type="loc", gameline="mta"
        )[0]

        new_mfs = MeritFlaw.objects.filter(allowed_types__in=[node.pk]).exclude(
            pk__in=self.merits_and_flaws.all()
        )
        had_mf_ratings = NodeMeritFlawRating.objects.all()
        had_mf_ratings = had_mf_ratings.filter(rating__lt=F("mf__max_rating"))

        had_mfs = MeritFlaw.objects.filter(
            pk__in=had_mf_ratings.values_list("mf", flat=True)
        )
        q = new_mfs | had_mfs

        q = q.filter(max_rating__lte=maximum)
        q = q.filter(min_rating__gte=minimum)

        return q

    def mf_rating(self, mf):
        if mf not in self.merits_and_flaws.all():
            return 0
        return NodeMeritFlawRating.objects.get(node=self, mf=mf).rating

    def add_resonance(self, resonance):
        r, _ = NodeResonanceRating.objects.get_or_create(resonance=resonance, node=self)
        if r.rating == 5:
            return False
        r.rating += 1
        r.save()
        return True

    def resonance_rating(self, resonance):
        if resonance in self.resonance.all():
            return NodeResonanceRating.objects.get(
                node=self, resonance=resonance
            ).rating
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
        if any(
            [x.name.startswith("Sphere Attuned") for x in self.merits_and_flaws.all()]
        ):
            for mf in [
                x
                for x in self.merits_and_flaws.all()
                if x.name.startswith("Sphere Attuned")
            ]:
                sphere_name = mf.name.split("(")[-1].split(")")[0]
                s = Sphere.objects.get(name=sphere_name)
                # self.random_resonance(sphere=s.property_name)

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


class NodeMeritFlawRating(models.Model):
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)
    mf = models.ForeignKey(MeritFlaw, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-10), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Node Merit or Flaw Rating"
        verbose_name_plural = "Node Merits and Flaws Rating"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=-10, rating__lte=10),
                name='locations_nodemeritflawrating_rating_range',
                violation_error_message="Node merit/flaw rating must be between -10 and 10"
            ),
        ]


class NodeResonanceRating(models.Model):
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)
    resonance = models.ForeignKey(Resonance, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Node Resonance Rating"
        verbose_name_plural = "Node Resonance Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name='locations_noderesonancerating_rating_range',
                violation_error_message="Node resonance rating must be between 0 and 10"
            ),
        ]

    def __str__(self):
        return f"{self.node}: {self.resonance} {self.rating}"
