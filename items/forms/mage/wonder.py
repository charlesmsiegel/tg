from characters.forms.mage.effect import EffectCreateOrSelectFormSet
from characters.models.mage.effect import Effect
from characters.models.mage.resonance import Resonance
from core.widgets import AutocompleteTextInput
from django import forms
from items.models.mage.artifact import Artifact
from items.models.mage.charm import Charm
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder, WonderResonanceRating


class WonderResonanceRatingForm(forms.ModelForm):
    class Meta:
        model = WonderResonanceRating
        fields = ["resonance", "rating"]

    rating = forms.IntegerField(min_value=0, max_value=5, initial=0)
    resonance = forms.CharField(required=False, widget=AutocompleteTextInput(suggestions=[]))

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        self.fields["resonance"].widget.suggestions = suggestions
        self.fields["resonance"].widget.attrs.update({"placeholder": "Enter Resonance Trait"})

    def clean_resonance(self):
        resonance = self.cleaned_data.get("resonance")
        return Resonance.objects.get_or_create(name=resonance)[0]


class BaseWonderResonanceRatingFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions = suggestions or [
            x.name.title() for x in Resonance.objects.order_by("name")
        ]

    def _construct_form(self, i, **kwargs):
        # Pass suggestions to each form
        kwargs["suggestions"] = self.suggestions
        return super()._construct_form(i, **kwargs)


WonderResonanceRatingFormSet = forms.inlineformset_factory(
    Wonder,
    WonderResonanceRating,
    form=WonderResonanceRatingForm,
    formset=BaseWonderResonanceRatingFormSet,
    extra=1,
    can_delete=False,
)


class WonderForm(forms.Form):
    WONDER_CHOICES = [
        ("charm", "Charm"),
        ("artifact", "Artifact"),
        ("talisman", "Talisman"),
    ]

    wonder_classes = {
        "charm": Charm,
        "artifact": Artifact,
        "talisman": Talisman,
    }

    wonder_type = forms.ChoiceField(choices=WONDER_CHOICES, label="Wonder Type", required=True)
    name = forms.CharField(max_length=100, label="Name", required=True)
    description = forms.CharField(widget=forms.Textarea, label="Description", required=True)
    rank = forms.IntegerField(label="Arete", required=True)
    arete = forms.IntegerField(label="Arete", required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        self.rank = kwargs.pop("rank", 0)
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})

        self.resonance_formset = WonderResonanceRatingFormSet(
            instance=self.instance,
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
        # Ensure clean() was called to populate cleaned_data
        if not hasattr(self, "cleaned_data"):
            self.full_clean()

        wonder_type = self.cleaned_data.get("wonder_type")
        # If self.instance exists, use it; otherwise, create a new one
        if self.instance:
            wonder = self.instance
        else:
            wonder = self.wonder_classes[wonder_type]()

        wonder.name = self.cleaned_data.get("name")
        wonder.description = self.cleaned_data.get("description")
        wonder.rank = self.cleaned_data.get("rank")

        if self.cleaned_data.get("arete"):
            wonder.arete = self.cleaned_data.get("arete")

        if commit:
            wonder.save()

            self.resonance_formset.instance = wonder
            self.resonance_formset.save()

            self.effect_formset.instance = wonder
            effects = self.effect_formset.save()

            if wonder_type in ["charm", "artifact"]:
                wonder.power = effects[0]
            else:
                for effect in effects:
                    wonder.powers.add(effect)
            wonder.save()
        return wonder

    def clean(self):
        cleaned_data = super().clean()
        rank = cleaned_data.get("rank", None)
        if rank is None:
            raise forms.ValidationError("Rank cannot be none")
        points = rank * 3

        if cleaned_data.get("arete") is None and cleaned_data.get("wonder_type") != "artifact":
            raise forms.ValidationError("Charms and Talismans must have Arete ratings")

        if not self.resonance_formset.is_valid():
            return cleaned_data

        if (
            cleaned_data.get("arete", 0) < cleaned_data.get("rank")
            and cleaned_data.get("wonder_type") != "artifact"
        ):
            raise forms.ValidationError(
                "Charms and Talismans need Arete rating at least equal to rank"
            )

        total_resonance_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.resonance_formset
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )

        if total_resonance_rating < rank:
            raise forms.ValidationError("Resonance total must match or exceed rank")

        if cleaned_data.get("wonder_type") == "charm":
            max_cost = cleaned_data.get("rank")
        else:
            max_cost = 2 * cleaned_data.get("rank")

        if not self.effect_formset.is_valid():
            raise forms.ValidationError("Effects invalid!")
        num_powers = len([form.cleaned_data for form in self.effect_formset if form.cleaned_data])
        if cleaned_data.get("wonder_type") == "talisman" and num_powers > cleaned_data.get("rank"):
            raise forms.ValidationError("Talismans may up to their rank in powers")
        elif num_powers > 1:
            if cleaned_data.get("wonder_type") == "charm":
                raise forms.ValidationError("Charms can only have one power")
            if cleaned_data.get("wonder_type") == "artifact":
                raise forms.ValidationError("Artifact can only have one power")

        for form in self.effect_formset:
            if form.cost() > max_cost:
                raise forms.ValidationError(
                    f"Some Effects too expensive, maximum cost is {max_cost}"
                )

        total_cost = total_resonance_rating - cleaned_data.get("rank")
        if cleaned_data.get("wonder_type") != "talisman":
            total_cost += cleaned_data.get("arete", cleaned_data.get("rank")) - cleaned_data.get(
                "rank"
            )
        for form in self.effect_formset:
            total_cost += form.cost()

        if total_cost > points:
            raise forms.ValidationError(
                "Extra Resonance, Arete, and Effects must be less than 3 times the rank of the Wonder"
            )
        return cleaned_data


class WonderCreateOrSelectForm(forms.Form):
    select_or_create = forms.BooleanField(required=False)
    select = forms.ModelChoiceField(queryset=Wonder.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False

        self.wonder_form = WonderForm(
            instance=self.instance,
            data=self.data if self.is_bound else None,
            prefix="wonder",
        )

    def clean(self):
        cleaned_data = super().clean()
        select_or_create = cleaned_data.get("select_or_create")
        select = cleaned_data.get("select")

        # If not creating a new one, user must have selected an existing effect.
        if not select_or_create and not select:
            self.add_error(
                "select",
                "You must either select an existing wonder or choose to create a new one.",
            )
        return cleaned_data

    def save(self, commit=True):
        """
        Custom save logic:
        - If select_or_create is False and an existing effect is chosen, return that existing effect.
        - Otherwise, create a new effect using the provided fields.
        """
        select_or_create = self.cleaned_data.get("select_or_create")
        select = self.cleaned_data.get("select")

        if not select_or_create and select:
            # User chose an existing effect
            # Return the existing effect without creating a new one.
            return select

        # Otherwise, create a new effect by calling the super save method
        # Note: This will create a new Effect instance with the data from the form
        return super().save(commit=commit)
