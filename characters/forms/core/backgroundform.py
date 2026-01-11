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
    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop("character", None)
        super().__init__(*args, **kwargs)

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
