from core.models import Model, Number
from django.core.validators import MaxValueValidator, MinValueValidator
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


class MeritFlawRating(models.Model):
    character = models.ForeignKey("Human", on_delete=models.SET_NULL, null=True)
    mf = models.ForeignKey(MeritFlaw, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(-10), MaxValueValidator(10)]
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

    def __str__(self):
        return f"{self.mf}: {self.rating}"


class MeritFlawBlock(models.Model):
    merits_and_flaws = models.ManyToManyField(
        MeritFlaw, blank=True, through=MeritFlawRating, related_name="flawed"
    )

    class Meta:
        abstract = True

    def num_languages(self):
        mf_list = self.merits_and_flaws.all().values_list("name", flat=True)
        if "Language" not in mf_list:
            return 0
        language_rating = self.mf_rating(MeritFlaw.objects.get(name="Language"))
        if "Natural Linguist" in mf_list:
            language_rating *= 2
        return language_rating

    def get_mf_and_rating_list(self):
        return [(x, self.mf_rating(x)) for x in self.merits_and_flaws.all()]

    def add_mf(self, mf, rating):
        if rating in mf.get_ratings():
            mfr, _ = MeritFlawRating.objects.get_or_create(character=self, mf=mf)
            mfr.rating = rating
            mfr.save()
            return True
        return False

    def filter_mfs(self):
        character_type = self.type
        if character_type in ["fomor"]:
            character_type = "human"

        new_mfs = MeritFlaw.objects.exclude(pk__in=self.merits_and_flaws.all())

        non_max_mf = MeritFlawRating.objects.filter(character=self).exclude(
            Q(rating=F("mf__max_rating"))
        )

        had_mfs = MeritFlaw.objects.filter(pk__in=non_max_mf)
        mf = new_mfs | had_mfs
        if self.has_max_flaws():
            mf = mf.filter(max_rating__gt=0)
        character_type_object = ObjectType.objects.get(name=character_type)
        return mf.filter(allowed_types=character_type_object)

    def mf_rating(self, mf):
        try:
            return MeritFlawRating.objects.get(character=self, mf=mf).rating
        except MeritFlawRating.DoesNotExist:
            return 0

    def has_max_flaws(self):
        return self.total_flaws() <= -7

    def total_flaws(self):
        from django.db.models import Sum

        result = MeritFlawRating.objects.filter(character=self, rating__lt=0).aggregate(
            Sum("rating")
        )
        return result["rating__sum"] or 0

    def total_merits(self):
        from django.db.models import Sum

        result = MeritFlawRating.objects.filter(character=self, rating__gt=0).aggregate(
            Sum("rating")
        )
        return result["rating__sum"] or 0

    def meritflaw_freebies(self, form):
        trait = form.cleaned_data["example"]
        value = int(form.data["value"])
        cost = value
        self.add_mf(trait, value)
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost
