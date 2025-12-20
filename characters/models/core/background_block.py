from characters.models.core.statistic import Statistic
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q


class Background(Statistic):
    type = "background"

    multiplier = models.IntegerField(default=1)
    alternate_name = models.CharField(default="", max_length=100)

    class Meta:
        ordering = ["name"]


class BackgroundRating(models.Model):
    bg = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True)
    char = models.ForeignKey(
        "characters.Human",
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
    pooled = models.BooleanField(default=False)
    display_alt_name = models.BooleanField(default=False)

    class Meta:
        ordering = ["bg__name"]
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="characters_backgroundrating_rating_range",
                violation_error_message="Background rating must be between 0 and 10",
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


class PooledBackgroundRating(models.Model):
    bg = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        "characters.Group",
        on_delete=models.SET_NULL,
        null=True,
        related_name="pooled_backgrounds",
    )
    rating = models.IntegerField(default=0)
    note = models.CharField(default="", max_length=100)
    url = models.CharField(default="", max_length=500)
    complete = models.BooleanField(default=False)

    class Meta:
        ordering = ["bg__name"]

    def __str__(self):
        return f"{self.bg} ({self.note})"


class BackgroundBlock(models.Model):
    allowed_backgrounds = []
    background_points = 5

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for bg in self.allowed_backgrounds:
            if not hasattr(self.__class__, bg):
                setattr(self.__class__, bg, self._create_property(bg))

    def _create_property(self, bg):
        return property(
            lambda self: self._get_property(bg),
            lambda self, value: self._set_property(bg, value),
        )

    def _get_property(self, bg):
        return self.total_background_rating(bg)

    def _set_property(self, prop, value):
        if value != 0:
            bg, _ = Background.objects.get_or_create(
                property_name=prop, defaults={"name": prop.replace("_", " ").title()}
            )
            BackgroundRating.objects.create(char=self, bg=bg, rating=value)
        else:
            BackgroundRating.objects.filter(char=self, bg__property_name=prop).delete()

    def total_background_rating(self, bg_name):
        return sum(
            [
                x.rating
                for x in BackgroundRating.objects.filter(bg__property_name=bg_name, char=self)
            ]
        )

    def get_backgrounds(self):
        return {bg: getattr(self, bg) for bg in self.allowed_backgrounds}

    def add_background(self, background, maximum=5):
        if isinstance(background, str):
            bg, _ = Background.objects.get_or_create(
                property_name=background,
                defaults={"name": background.replace("_", " ").title()},
            )
            ratings = BackgroundRating.objects.filter(char=self, bg=bg)
            if ratings.filter(rating__lt=5).count() > 0:
                background = ratings.filter(rating__lt=5).first()
            else:
                background = BackgroundRating.objects.create(char=self, bg=bg)
        elif isinstance(background, Background):
            ratings = BackgroundRating.objects.filter(char=self, bg=background)
            if ratings.filter(rating__lt=5).count() > 0:
                background = ratings.filter(rating__lt=5).first()
            else:
                background = BackgroundRating.objects.create(char=self, bg=background)
        else:
            raise ValueError(
                "Must be a background name, Background object, or BackgroundRating object"
            )
        if background.rating == 5:
            return False
        background.rating += 1
        background.save()
        return True

    def total_backgrounds(self):
        return sum(self.get_backgrounds().values())

    def filter_backgrounds(self, minimum=0, maximum=5):
        return {k: v for k, v in self.get_backgrounds().items() if minimum <= v <= maximum}

    def has_backgrounds(self):
        if self.total_backgrounds() > self.background_points:
            self.freebies -= self.total_backgrounds() - self.background_points
        return self.total_backgrounds() >= self.background_points

    def new_background_freebies(self, form):
        trait = form.cleaned_data["example"]
        cost = trait.multiplier
        value = 1
        trait = Background.objects.get(pk=form.data["example"])
        if "pooled" in form.data.keys():
            pbgr = PooledBackgroundRating.objects.get_or_create(
                bg=trait, group=self.get_group(), note=form.data["note"]
            )[0]
            pbgr.rating += 1
            pbgr.save()
            BackgroundRating.objects.create(
                bg=trait,
                rating=1,
                char=self,
                note=form.data["note"],
                complete=True,
                pooled=True,
            )
        else:
            BackgroundRating.objects.create(
                bg=trait,
                rating=1,
                char=self,
                note=form.data["note"],
                pooled=False,
            )
        self.freebies -= cost
        trait = str(trait)
        if form.data["note"]:
            trait += f" ({form.data['note']})"
        return trait, value, cost

    def existing_background_freebies(self, form):
        trait = form.cleaned_data["example"]
        cost = trait.bg.multiplier
        if trait.pooled:
            pbgr = PooledBackgroundRating.objects.get(
                bg=trait.bg, group=self.get_group(), note=trait.note
            )
            pbgr.rating += 1
            pbgr.save()
        value = trait.rating + 1
        trait.rating += 1
        trait.save()
        self.freebies -= cost
        trait = str(trait)
        return trait, value, cost
