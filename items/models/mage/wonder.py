from characters.models.mage.resonance import Resonance
from core.utils import fast_selector
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from items.models.core import ItemModel


class WonderResonanceRating(models.Model):
    class Meta:
        verbose_name = "Wonder Resonance Rating"
        verbose_name_plural = "Wonder Resonance Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="items_wonderresonancerating_rating_range",
                violation_error_message="Wonder resonance rating must be between 0 and 10",
            ),
        ]

    wonder = models.ForeignKey("Wonder", on_delete=models.SET_NULL, null=True)
    resonance = models.ForeignKey(
        "characters.Resonance", on_delete=models.SET_NULL, null=True
    )
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.resonance}: {self.rating}"


class Wonder(ItemModel):
    type = "wonder"

    rank = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    background_cost = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    quintessence_max = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    resonance = models.ManyToManyField(
        "characters.Resonance", blank=True, through=WonderResonanceRating
    )

    class Meta:
        verbose_name = "Wonder"
        verbose_name_plural = "Wonders"
        constraints = [
            CheckConstraint(
                check=Q(rank__gte=0, rank__lte=10),
                name="items_wonder_rank_range",
                violation_error_message="Wonder rank must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(background_cost__gte=0, background_cost__lte=10),
                name="items_wonder_background_cost_range",
                violation_error_message="Wonder background cost must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(quintessence_max__gte=0, quintessence_max__lte=100),
                name="items_wonder_quintessence_max_range",
                violation_error_message="Wonder quintessence max must be between 0 and 100",
            ),
        ]

    def get_update_url(self):
        return reverse("items:mage:update:wonder", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mage:create:wonder")

    def get_heading(self):
        return "mta_heading"

    def set_rank(self, rank):
        self.rank = rank
        return True

    def has_rank(self):
        return self.rank != 0

    def add_resonance(self, resonance):
        from characters.models.mage.resonance import Resonance

        # Accept string name or Resonance object
        if isinstance(resonance, str):
            resonance, _ = Resonance.objects.get_or_create(name=resonance)
        r, _ = WonderResonanceRating.objects.get_or_create(
            resonance=resonance, wonder=self
        )
        if r.rating == 5:
            return False
        r.rating += 1
        r.save()
        return True

    def resonance_rating(self, resonance):
        if resonance in self.resonance.all():
            return WonderResonanceRating.objects.get(
                wonder=self, resonance=resonance
            ).rating
        return 0

    def filter_resonance(self, minimum=0, maximum=5):
        all_res = Resonance.objects.all()

        maxed_resonance = [
            x.resonance.id
            for x in WonderResonanceRating.objects.filter(
                wonder=self, rating__gt=maximum
            )
        ]
        mined_resonance = [
            x.resonance.id
            for x in WonderResonanceRating.objects.filter(
                wonder=self, rating__lt=minimum
            )
        ]
        all_res = all_res.exclude(pk__in=maxed_resonance)
        all_res = all_res.exclude(pk__in=mined_resonance)
        if minimum > 0:
            all_res = all_res.filter(
                pk__in=[
                    x.resonance.id
                    for x in WonderResonanceRating.objects.filter(
                        wonder=self, rating__gt=0
                    )
                ]
            )
        return all_res

    def total_resonance(self):
        return sum(x.rating for x in WonderResonanceRating.objects.filter(wonder=self))

    def has_resonance(self):
        return self.total_resonance() >= self.rank
