from django.db import models
from django.db.models import CheckConstraint, Q, Sum

from characters.models.core.statistic import Statistic
from core.models import BaseBackgroundRating


class Background(Statistic):
    type = "background"

    multiplier = models.IntegerField(default=1)
    alternate_name = models.CharField(default="", max_length=100)
    poolable = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]


class BackgroundRating(BaseBackgroundRating):
    """Background rating for a character."""

    char = models.ForeignKey(
        "characters.Human",
        on_delete=models.SET_NULL,
        null=True,
        related_name="backgrounds",
        db_index=True,
    )
    pooled = models.BooleanField(default=False)
    display_alt_name = models.BooleanField(default=False)

    class Meta:
        ordering = ["bg__name"]
        indexes = [
            models.Index(fields=["char", "bg"]),
        ]
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="characters_backgroundrating_rating_range",
                violation_error_message="Background rating must be between 0 and 10",
            ),
        ]

    def display_name(self):
        if self.bg.alternate_name == "":
            return self.bg.name
        elif self.display_alt_name:
            return self.bg.alternate_name
        return self.bg.name


class PooledBackgroundRating(BaseBackgroundRating):
    """Background rating for a group (pooled backgrounds)."""

    group = models.ForeignKey(
        "characters.Group",
        on_delete=models.SET_NULL,
        null=True,
        related_name="pooled_backgrounds",
    )

    class Meta:
        ordering = ["bg__name"]


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
        result = BackgroundRating.objects.filter(bg__property_name=bg_name, char=self).aggregate(
            total=Sum("rating")
        )
        return result["total"] or 0

    def get_backgrounds(self):
        return {bg: getattr(self, bg) for bg in self.allowed_backgrounds}

    def add_background(self, background, maximum=5):
        if isinstance(background, str):
            bg, _ = Background.objects.get_or_create(
                property_name=background,
                defaults={"name": background.replace("_", " ").title()},
            )
            background = BackgroundRating.objects.filter(char=self, bg=bg, rating__lt=5).first()
            if not background:
                background = BackgroundRating.objects.create(char=self, bg=bg)
        elif isinstance(background, Background):
            bg = background
            background = BackgroundRating.objects.filter(char=self, bg=bg, rating__lt=5).first()
            if not background:
                background = BackgroundRating.objects.create(char=self, bg=bg)
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
        # Only allow pooling if the background is poolable
        if "pooled" in form.data.keys() and trait.poolable:
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
