from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from characters.models.mage.focus import Practice, SpecializedPractice
from characters.models.mage.mage import Mage, PracticeRating
from widgets.widgets.dots import DotRatingInput


def available_practices(mage=None):
    """Faction-appropriate practices with enough supporting ability dots."""
    practices = Practice.objects.exclude(polymorphic_ctype__model="specializedpractice").exclude(
        polymorphic_ctype__model="corruptedpractice"
    )
    if mage is not None:
        specialized = SpecializedPractice.objects.filter(faction=mage.faction)
        if specialized.exists():
            practices = practices.exclude(
                id__in=specialized.values_list("parent_practice_id", flat=True)
            ) | Practice.objects.filter(id__in=specialized)
        eligible = list(starting_practice_limits(mage, practices).keys())
        practices = practices.filter(pk__in=eligible)
    return practices.order_by("name")


def starting_practice_limits(mage, practices):
    """Maximum starting dots by each practice's supporting abilities and Arete."""
    limits = {}
    for practice in practices.prefetch_related("abilities"):
        dots = sum(getattr(mage, ability.property_name, 0) for ability in practice.abilities.all())
        maximum = min(5, mage.arete, dots // 2)
        if maximum:
            limits[practice.pk] = maximum
    return limits


class PracticeRatingForm(forms.ModelForm):
    class Meta:
        model = PracticeRating
        fields = ["practice", "rating"]

    practice = forms.ModelChoiceField(
        queryset=Practice.objects.none(), empty_label="Choose a Practice"
    )
    rating = forms.IntegerField(min_value=0, max_value=5, initial=0)

    def __init__(self, *args, **kwargs):
        mage = kwargs.pop("mage", None)
        super().__init__(*args, **kwargs)
        self.fields["practice"].queryset = available_practices(mage)
        self.fields["rating"].widget = DotRatingInput(
            minimum=0, maximum=min(5, mage.arete) if mage else 5, label="Practice", alpine=False
        )


class BasePracticeRatingFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.mage = kwargs.pop("mage", None)
        super().__init__(*args, **kwargs)
        self.practice_limits = {
            str(pk): rating
            for pk, rating in starting_practice_limits(
                self.mage, self.get_practice_queryset()
            ).items()
        } if self.mage else {}

    def get_form_kwargs(self, index):
        return {**super().get_form_kwargs(index), "mage": self.mage}

    def get_practice_queryset(self):
        return available_practices(self.mage)


PracticeRatingFormSet = inlineformset_factory(
    Mage,
    PracticeRating,
    form=PracticeRatingForm,
    extra=1,
    can_delete=False,
    formset=BasePracticeRatingFormSet,
)
