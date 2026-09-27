from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human


class BackgroundRatingForm(forms.ModelForm):
    class Meta:
        model = BackgroundRating
        fields = ["bg", "rating", "note", "display_alt_name", "pooled"]

    bg = forms.ModelChoiceField(
        queryset=Background.objects.all(), empty_label="Choose a Background"
    )
    rating = forms.IntegerField(min_value=0, max_value=5, initial=0)

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        super().__init__(*args, **kwargs)
        self.fields["bg"].queryset = Background.objects.all().order_by("name")
        self.fields["note"].required = False
        self.fields["display_alt_name"].required = False
        self.fields["pooled"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.char = self.character
        if commit:
            instance.save()
        return instance


class BaseBackgroundRatingFormSet(BaseInlineFormSet):
    """Background ratings; with ``enforce_allocation`` also the chargen limits.

    The chargen step spends exactly ``character.background_points`` (each dot
    costs the background's multiplier) and obeys the character's own
    ``background_violations`` (for example Kinfolk tribal restrictions, which
    are reported before the total).
    """

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        self.enforce_allocation = kwargs.pop("enforce_allocation", False)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.enforce_allocation or any(form.errors for form in self.forms):
            return
        rated = self._rated_forms()
        pairs = [(form.cleaned_data["bg"], form.cleaned_data["rating"]) for form in rated]
        for index, violation in self.character.background_violations(pairs):
            target = rated[index] if rated else (self.forms[0] if self.forms else None)
            if target is None:
                raise forms.ValidationError(violation.message)
            target.add_error(violation.field, violation.message)
            return
        total = self.points_spent(pairs)
        if total != self.character.background_points:
            message = f"Backgrounds must total {self.character.background_points} points"
            for form in self.forms:
                form.add_error(None, message)

    def _rated_forms(self):
        return [
            form
            for form in self.forms
            if "rating" in getattr(form, "cleaned_data", {}) and "bg" in form.cleaned_data
        ]

    @staticmethod
    def points_spent(pairs):
        return sum(rating * bg.multiplier for bg, rating in pairs)

    def allocation_status(self):
        """Running total of a validated formset: the arithmetic clean() enforces.

        Rows whose background or rating failed validation do not count, as they
        could not be saved.
        """
        pairs = [
            (form.cleaned_data["bg"], form.cleaned_data["rating"])
            for form in self._rated_forms()
            if not form.cleaned_data.get("DELETE")
        ]
        budget = self.character.background_points
        spent = self.points_spent(pairs)
        return {
            "name": "backgrounds",
            "label": "Background points",
            "current": spent,
            "target": budget,
            "satisfied": spent == budget,
        }

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["bg"].queryset = Background.objects.all().order_by("name")

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["character"] = self.character
        return kwargs

    def save_new(self, form, commit=True):
        if form.cleaned_data.get("bg") and form.cleaned_data.get("rating"):
            return super().save_new(form, commit=commit)
        return None

    def save_existing(self, form, instance, commit=True):
        if form.cleaned_data.get("bg") and form.cleaned_data.get("rating"):
            return super().save_existing(form, instance, commit=commit)
        return None


BackgroundRatingFormSet = inlineformset_factory(
    Human,
    BackgroundRating,
    form=BackgroundRatingForm,
    extra=1,
    can_delete=False,
    formset=BaseBackgroundRatingFormSet,
)
