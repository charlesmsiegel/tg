from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, router, transaction
from django.db.models import CheckConstraint, Q

from characters.models.mage.focus import Practice
from core.models import BasePracticeRating
from core.registry_urls import RegistryURLMixin


class ZoneRating(BasePracticeRating):
    """Practice rating for a Reality Zone (rating range: -10 to 10)."""

    zone = models.ForeignKey("RealityZone", on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(-10), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Reality Zone Rating"
        verbose_name_plural = "Reality Zone Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=-10, rating__lte=10),
                name="locations_zonerating_rating_range",
                violation_error_message="Reality zone rating must be between -10 and 10",
            ),
        ]


class RealityZone(RegistryURLMixin, models.Model):
    type = "reality_zone"
    gameline = "mta"

    name = models.CharField(max_length=100)
    practices = models.ManyToManyField(Practice, through=ZoneRating, blank=True)
    description = models.TextField(default="")
    # Sticky provenance, backfilled for existing links by tg_schema 0012. A
    # detached player zone must not become a public standalone reference.
    is_player_zone = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "Reality Zone"
        verbose_name_plural = "Reality Zone"

    def get_heading(self):
        return "mta_heading"

    def save(self, *args, **kwargs):
        using = kwargs.get("using", args[2] if len(args) > 2 else None) or router.db_for_write(
            type(self), instance=self
        )
        with transaction.atomic(using=using):
            if self.pk is not None:
                previous = (
                    type(self).objects.using(using).select_for_update().filter(pk=self.pk).first()
                )
                if previous is not None:
                    self.is_player_zone = self.is_player_zone or previous.is_player_zone
            return super().save(*args, **kwargs)

    def get_positive_practices(self):
        return (
            ZoneRating.objects.filter(zone=self, rating__gt=0)
            .select_related("practice")
            .order_by("-rating", "practice__name")
        )

    def get_negative_practices(self):
        return (
            ZoneRating.objects.filter(zone=self, rating__lt=0)
            .select_related("practice")
            .order_by("rating", "practice__name")
        )

    def get_applied_to(self):
        return [
            location
            for relation in self.get_location_relations()
            for location in getattr(self, relation.get_accessor_name()).all()
        ]

    @classmethod
    def get_location_relations(cls):
        """Include every zone-bearing location, including inherited realm types."""
        return tuple(
            relation
            for relation in cls._meta.related_objects
            if relation.field.name == "reality_zone"
        )

    def __str__(self):
        return self.name
