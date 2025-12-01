from characters.forms.mage.effect import EffectCreateOrSelectFormSet
from characters.models.mage.effect import Effect
from characters.models.mage.resonance import Resonance
from django import forms
from items.models.mage.periapt import Periapt
from items.models.mage.wonder import WonderResonanceRating


class WonderResonanceRatingForm(forms.ModelForm):
    class Meta:
        model = WonderResonanceRating
        fields = ["resonance", "rating"]

    rating = forms.IntegerField(min_value=0, max_value=5, initial=0)
    resonance = forms.ModelChoiceField(queryset=Resonance.objects.all(), required=False)


class BaseWonderResonanceRatingFormSet(forms.BaseInlineFormSet):
    pass


PeriaptResonanceRatingFormSet = forms.inlineformset_factory(
    Periapt,
    WonderResonanceRating,
    form=WonderResonanceRatingForm,
    formset=BaseWonderResonanceRatingFormSet,
    extra=1,
    can_delete=False,
)


class PeriaptForm(forms.ModelForm):
    class Meta:
        model = Periapt
        fields = (
            "name",
            "description",
            "rank",
            "arete",
            "max_charges",
            "current_charges",
            "is_consumable",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})

        self.resonance_formset = PeriaptResonanceRatingFormSet(
            instance=self.instance if self.instance.pk else None,
            data=self.data if self.is_bound else None,
            prefix="resonance",
        )

        self.effect_formset = EffectCreateOrSelectFormSet(
            queryset=Effect.objects.none(),
            data=self.data if self.is_bound else None,
            prefix="effects",
        )

    def is_valid(self):
        valid = super().is_valid()
        valid = valid and self.resonance_formset.is_valid()
        valid = valid and self.effect_formset.is_valid()
        return valid

    def save(self, commit=True):
        periapt = super().save(commit=False)

        if commit:
            periapt.save()

            self.resonance_formset.instance = periapt
            self.resonance_formset.save()

            effects = self.effect_formset.save()
            if effects:
                periapt.power = effects[0]
                periapt.save()

        return periapt

    def clean(self):
        cleaned_data = super().clean()
        rank = cleaned_data.get("rank", None)
        arete = cleaned_data.get("arete", None)
        max_charges = cleaned_data.get("max_charges", 1)
        current_charges = cleaned_data.get("current_charges", 1)

        if rank is None:
            raise forms.ValidationError("Rank cannot be none")

        if arete is None:
            raise forms.ValidationError("Periapts must have an Arete rating")

        if arete < rank:
            raise forms.ValidationError("Periapt Arete rating must be at least equal to rank")

        if current_charges > max_charges:
            raise forms.ValidationError("Current charges cannot exceed maximum charges")

        if not self.resonance_formset.is_valid():
            return cleaned_data

        total_resonance_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.resonance_formset
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )

        if total_resonance_rating < rank:
            raise forms.ValidationError("Resonance total must match or exceed rank")

        if not self.effect_formset.is_valid():
            raise forms.ValidationError("Effects invalid!")

        num_powers = len([form.cleaned_data for form in self.effect_formset if form.cleaned_data])

        if num_powers > 1:
            raise forms.ValidationError("Periapts can only have one power")

        max_cost = rank
        for form in self.effect_formset:
            if form.cost() > max_cost:
                raise forms.ValidationError(f"Effect too expensive, maximum cost is {max_cost}")

        points = rank * 3
        total_cost = total_resonance_rating - rank
        total_cost += arete - rank
        for form in self.effect_formset:
            total_cost += form.cost()

        if total_cost > points:
            raise forms.ValidationError(
                "Extra Resonance, Arete, and Effects must be less than 3 times the rank of the Periapt"
            )

        return cleaned_data
