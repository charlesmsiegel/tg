from core.models import BaseMeritFlawRating, Model, Number
from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.urls import reverse
from game.models import ObjectType


class MeritFlaw(Model):
    type = "merit_flaw"
    gameline = "wod"

    ratings = models.ManyToManyField(Number, blank=True)
    max_rating = models.IntegerField(default=0)
    min_rating = models.IntegerField(default=0)

    allowed_types = models.ManyToManyField(ObjectType, blank=True)

    class Meta:
        verbose_name = "Merit or Flaw"
        verbose_name_plural = "Merits and Flaws"
        ordering = ["name"]

    def __str__(self):
        ratings = [x.value for x in self.ratings.all()]
        ratings.sort()
        ratings = ",".join([str(x) for x in ratings])
        return f"{self.name} ({ratings})"

    def get_absolute_url(self):
        return reverse("characters:meritflaw", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:update:meritflaw", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:create:meritflaw")

    def get_heading(self):
        return "wod_heading"

    def update_max_rating(self):
        ratings = list(self.ratings.values_list("value", flat=True))
        self.max_rating = max(ratings) if ratings else 0
        self.save()

    def update_min_rating(self):
        ratings = list(self.ratings.values_list("value", flat=True))
        self.min_rating = min(ratings) if ratings else 0
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

    def check_type(self, type_name):
        if self.allowed_types.get(value=type_name).exists():
            return True
        return False


class MeritFlawRating(BaseMeritFlawRating):
    """Through model for Character merit/flaw ratings."""

    character = models.ForeignKey(
        "Human",
        on_delete=models.SET_NULL,
        null=True,
        related_name="merit_flaw_ratings",
        db_index=True,
    )
    mf = models.ForeignKey(
        MeritFlaw,
        on_delete=models.SET_NULL,
        null=True,
        related_name="character_ratings",
        db_index=True,
    )

    class Meta:
        verbose_name = "Merit or Flaw Rating"
        verbose_name_plural = "Merit and Flaw Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=-10, rating__lte=10),
                name="characters_meritflawrating_rating_range",
                violation_error_message="Merit/Flaw rating must be between -10 and 10",
            ),
        ]


class MeritFlawBlock(models.Model):
    """
    Abstract mixin providing merit/flaw functionality for any model.

    Subclasses must define:
    - merits_and_flaws: ManyToManyField to MeritFlaw with a through model
    - type: str - the object type for ObjectType filtering
    - gameline: str - the gameline for ObjectType filtering

    The through model must have:
    - A ForeignKey to the parent model (detected automatically)
    - A ForeignKey to MeritFlaw named 'mf'
    - A rating field
    """

    class Meta:
        abstract = True

    def _get_through_model(self):
        """Get the through model for the merits_and_flaws relationship."""
        return self._meta.get_field("merits_and_flaws").remote_field.through

    def _get_parent_fk_name(self):
        """
        Get the FK field name pointing to this model in the through model.
        E.g., 'character' for MeritFlawRating, 'node' for NodeMeritFlawRating.
        """
        through_model = self._get_through_model()
        for field in through_model._meta.get_fields():
            related_model = getattr(field, "related_model", None)
            if related_model is not None and isinstance(self, related_model):
                return field.name
        # Fallback to the model name in lowercase
        return self.__class__.__name__.lower()

    def _get_object_type(self):
        """Get or create the ObjectType for this object type."""
        object_type = self.type
        # Handle special cases
        if object_type in ["fomor"]:
            object_type = "human"

        # Determine type category ('char' for characters, 'loc' for locations)
        from locations.models.core import LocationModel

        type_category = "loc" if isinstance(self, LocationModel) else "char"

        return ObjectType.objects.get_or_create(
            name=object_type,
            defaults={"type": type_category, "gameline": getattr(self, "gameline", "wod")},
        )[0]

    def num_languages(self):
        """Character-specific method to count languages."""
        mf_list = self.merits_and_flaws.all().values_list("name", flat=True)
        if "Language" not in mf_list:
            return 0
        language_rating = self.mf_rating(MeritFlaw.objects.get(name="Language"))
        if "Natural Linguist" in mf_list:
            language_rating *= 2
        return language_rating

    def get_mf_and_rating_list(self):
        """Return list of (MeritFlaw, rating) tuples."""
        return [(x, self.mf_rating(x)) for x in self.merits_and_flaws.all()]

    def add_mf(self, mf, rating):
        """
        Add or update a merit/flaw.

        Args:
            mf: MeritFlaw instance
            rating: int - the rating value

        Returns:
            bool - True if successfully added/updated, False otherwise
        """
        if rating not in mf.get_ratings():
            return False

        through_model = self._get_through_model()
        fk_name = self._get_parent_fk_name()

        mfr, _ = through_model.objects.get_or_create(**{fk_name: self, "mf": mf})
        mfr.rating = rating
        mfr.save()
        return True

    def filter_mfs(self):
        """
        Filter available merits/flaws for this object.

        Returns:
            QuerySet of MeritFlaw objects that can be added
        """
        through_model = self._get_through_model()
        fk_name = self._get_parent_fk_name()

        new_mfs = MeritFlaw.objects.exclude(pk__in=self.merits_and_flaws.all())

        non_max_mf = through_model.objects.filter(**{fk_name: self}).exclude(
            Q(rating=F("mf__max_rating"))
        )

        had_mfs = MeritFlaw.objects.filter(pk__in=non_max_mf.values_list("mf", flat=True))
        mf = new_mfs | had_mfs
        if self.has_max_flaws():
            mf = mf.filter(max_rating__gt=0)

        object_type = self._get_object_type()
        return mf.filter(allowed_types=object_type)

    def mf_rating(self, mf):
        """Get the rating for a specific merit/flaw."""
        through_model = self._get_through_model()
        fk_name = self._get_parent_fk_name()
        try:
            return through_model.objects.get(**{fk_name: self, "mf": mf}).rating
        except through_model.DoesNotExist:
            return 0

    def has_max_flaws(self):
        """Check if max flaws limit reached (-7 points)."""
        return self.total_flaws() <= -7

    def total_flaws(self):
        """Get the sum of all negative flaw ratings."""
        from django.db.models import Sum

        through_model = self._get_through_model()
        fk_name = self._get_parent_fk_name()
        result = through_model.objects.filter(**{fk_name: self, "rating__lt": 0}).aggregate(
            Sum("rating")
        )
        return result["rating__sum"] or 0

    def total_merits(self):
        """Get the sum of all positive merit ratings."""
        from django.db.models import Sum

        through_model = self._get_through_model()
        fk_name = self._get_parent_fk_name()
        result = through_model.objects.filter(**{fk_name: self, "rating__gt": 0}).aggregate(
            Sum("rating")
        )
        return result["rating__sum"] or 0

    def total_mf(self):
        """Get the total of all merit/flaw ratings (merits minus flaws)."""
        through_model = self._get_through_model()
        fk_name = self._get_parent_fk_name()
        return sum(r.rating for r in through_model.objects.filter(**{fk_name: self}))

    def meritflaw_freebies(self, form):
        """Character-specific method for spending freebies on merits/flaws."""
        trait = form.cleaned_data["example"]
        value = int(form.data["value"])
        cost = value
        self.add_mf(trait, value)
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost
