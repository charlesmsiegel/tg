from characters.models.mage.focus import Practice
from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from locations.models.mage.reality_zone import RealityZone, ZoneRating


class RealityZonePracticeRatingForm(forms.ModelForm):
    class Meta:
        model = ZoneRating
        fields = ["practice", "rating"]

    practice = forms.ModelChoiceField(
        queryset=Practice.objects.exclude(polymorphic_ctype__model="specializedpractice").exclude(
            polymorphic_ctype__model="corruptedpractice"
        )
    )
    rating = forms.IntegerField(min_value=-5, max_value=5, initial=0)


class BaseZoneRatingFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = form.save(commit=False)
        obj.zone = self.instance  # Associate with the RealityZone instance
        if commit:
            obj.save()
        return obj


RealityZonePracticeRatingFormSet = inlineformset_factory(
    RealityZone,
    ZoneRating,
    form=RealityZonePracticeRatingForm,
    formset=BaseZoneRatingFormSet,
    extra=1,
    can_delete=True,
)
