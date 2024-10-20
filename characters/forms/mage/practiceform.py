from characters.models.mage.focus import Practice, SpecializedPractice
from characters.models.mage.mage import Mage, PracticeRating
from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory


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
        if mage:
            q = Practice.objects.exclude(
                polymorphic_ctype__model="specializedpractice"
            ).exclude(polymorphic_ctype__model="corruptedpractice")
            spec = SpecializedPractice.objects.get(faction=mage.faction)
            q = q.exclude(id=spec.parent_practice.id) | Practice.objects.filter(
                id=spec.id
            )
            self.fields["practice"].queryset = q.order_by("name")
        else:
            self.fields["practice"].queryset = Practice.objects.exclude(
                polymorphic_ctype__model="specializedpractice"
            ).exclude(polymorphic_ctype__model="corruptedpractice")


class BasePracticeRatingFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.mage = kwargs.pop("mage", None)
        super().__init__(*args, **kwargs)

        for form in self.forms:
            form.fields["practice"].queryset = self.get_practice_queryset()

    def get_practice_queryset(self):
        if self.mage:
            q = Practice.objects.exclude(
                polymorphic_ctype__model="specializedpractice"
            ).exclude(polymorphic_ctype__model="corruptedpractice")
            if self.mage.faction is not None:
                spec = SpecializedPractice.objects.get(faction=self.mage.faction)
                q = q.exclude(id=spec.parent_practice.id) | Practice.objects.filter(
                    id=spec.id
                )
            return q.order_by("name")
        return Practice.objects.exclude(
            polymorphic_ctype__model="specializedpractice"
        ).exclude(polymorphic_ctype__model="corruptedpractice")


PracticeRatingFormSet = inlineformset_factory(
    Mage,
    PracticeRating,
    form=PracticeRatingForm,
    extra=1,
    can_delete=False,
    formset=BasePracticeRatingFormSet,
)
