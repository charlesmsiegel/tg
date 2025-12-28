from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.resonance import Resonance
from core.models import Number
from core.widgets import AutocompleteTextInput
from django import forms
from game.models import ObjectType
from locations.forms.mage.reality_zone import RealityZonePracticeRatingFormSet
from locations.models.mage import Node
from locations.models.mage.node import NodeMeritFlawRating, NodeResonanceRating
from locations.models.mage.reality_zone import RealityZone


class NodeResonanceRatingForm(forms.ModelForm):
    class Meta:
        model = NodeResonanceRating
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


class BaseNodeResonanceRatingFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions = suggestions or [
            x.name.title() for x in Resonance.objects.order_by("name")
        ]

    def _construct_form(self, i, **kwargs):
        kwargs["suggestions"] = self.suggestions
        return super()._construct_form(i, **kwargs)


NodeResonanceRatingFormSet = forms.inlineformset_factory(
    Node,
    NodeResonanceRating,
    form=NodeResonanceRatingForm,
    formset=BaseNodeResonanceRatingFormSet,
    extra=1,
    can_delete=False,
)


class NodeMeritFlawForm(forms.ModelForm):
    class Meta:
        model = NodeMeritFlawRating
        fields = ["mf", "rating"]

    rating = forms.ModelChoiceField(queryset=Number.objects.none(), required=False)
    mf = forms.ModelChoiceField(queryset=MeritFlaw.objects.none())

    def __init__(self, *args, **kwargs):
        n = ObjectType.objects.get_or_create(
            name="node", defaults={"type": "loc", "gameline": "mta"}
        )[0]
        super().__init__(*args, **kwargs)
        self.fields["mf"].queryset = MeritFlaw.objects.filter(allowed_types__in=[n])

        if self.is_bound:
            mf_id = self.data.get(self.add_prefix("mf"))
            if mf_id:
                try:
                    mf = MeritFlaw.objects.get(pk=mf_id)
                    self.fields["rating"].queryset = mf.ratings.all()
                except MeritFlaw.DoesNotExist:
                    self.fields["rating"].queryset = Number.objects.none()
            else:
                self.fields["rating"].queryset = Number.objects.none()
        elif self.instance.pk:
            mf = self.instance.mf
            self.fields["rating"].queryset = mf.ratings.all()
        else:
            self.fields["rating"].queryset = Number.objects.none()

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        return rating.value


NodeMeritFlawRatingFormSet = forms.inlineformset_factory(
    Node,
    NodeMeritFlawRating,
    form=NodeMeritFlawForm,
    extra=1,
    can_delete=False,
)


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = (
            "name",
            "rank",
            "description",
            "ratio",
            "size",
            "quintessence_form",
            "tass_form",
            "parent",
            "gauntlet",
            "shroud",
            "dimension_barrier",
        )

    def __init__(self, *args, **kwargs):
        super(NodeForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["quintessence_form"].widget.attrs.update(
            {"placeholder": "Enter Quintessence Form here"}
        )
        self.fields["tass_form"].widget.attrs.update({"placeholder": "Enter Tass Form here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        self.fields["parent"].required = False

        self.resonance_formset = NodeResonanceRatingFormSet(
            instance=self.instance,
            data=self.data if self.is_bound else None,
            prefix="resonance",
        )
        self.merit_flaw_formset = NodeMeritFlawRatingFormSet(
            instance=self.instance,
            data=self.data if self.is_bound else None,
            prefix="merit_flaw",
        )
        # Initialize RealityZone instance
        if self.instance.pk and self.instance.reality_zone:
            self.reality_zone = self.instance.reality_zone
        else:
            self.reality_zone = RealityZone()

        # Initialize RealityZonePracticeRatingFormSet
        self.reality_zone_formset = RealityZonePracticeRatingFormSet(
            instance=self.reality_zone,
            data=self.data if self.is_bound else None,
            prefix="reality_zone",
        )

    def is_valid(self):
        valid = super(NodeForm, self).is_valid()
        valid = valid and self.resonance_formset.is_valid()
        valid = valid and self.merit_flaw_formset.is_valid()
        valid = valid and self.reality_zone_formset.is_valid()
        return valid

    def save(self, commit=True):
        node = super(NodeForm, self).save(commit=False)
        node.rank = self.cleaned_data.get("rank")
        node.tass_per_week = self.tass_per_week
        node.quintessence_per_week = self.quintessence_per_week
        if commit:
            node.save()

            # Save the resonance and merit/flaw formsets
            self.resonance_formset.instance = node
            self.resonance_formset.save()
            self.merit_flaw_formset.instance = node
            self.merit_flaw_formset.save()

            # Save the RealityZone
            self.reality_zone.name = node.name  # Or get from form if you have a RealityZoneForm
            self.reality_zone.save()
            node.reality_zone = self.reality_zone
            node.save()

            # Save the RealityZonePracticeRatingFormSet
            self.reality_zone_formset.instance = self.reality_zone
            self.reality_zone_formset.save()

        return node

    def clean(self):
        cleaned_data = super().clean()

        rank = cleaned_data.get("rank", None)
        if rank is None:
            raise forms.ValidationError("Rank cannot be none")

        ratio = self.cleaned_data.get("ratio")
        size = self.cleaned_data.get("size")

        self.resonance_formset.full_clean()
        self.merit_flaw_formset.full_clean()
        self.reality_zone_formset.full_clean()

        if not self.resonance_formset.is_valid():
            return cleaned_data

        if not self.merit_flaw_formset.is_valid():
            return cleaned_data

        if not self.reality_zone_formset.is_valid():
            return cleaned_data

        # get rank either from kwargs or form
        # determine if owner from kwargs
        # determine if chronicle from kwargs
        # status = "Sub"

        total_resonance_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.resonance_formset
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )

        if total_resonance_rating < rank:
            raise forms.ValidationError("Resonance total must match or exceed rank")

        total_mf_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.merit_flaw_formset
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )

        total_rz_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.reality_zone_formset
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )

        total_positive_rz_rating = sum(
            form.cleaned_data.get("rating", 0)
            for form in self.reality_zone_formset
            if form.cleaned_data
            and not form.cleaned_data.get("DELETE", False)
            and form.cleaned_data.get("rating", 0) > 0
        )

        if total_rz_rating != 0:
            raise forms.ValidationError("Reality Zone Ratings must total 0")

        if total_positive_rz_rating != rank:
            raise forms.ValidationError("Positive Reality Zone Ratings must sum to Node rating")

        points_remaining = (
            3 * rank - (total_resonance_rating - rank) - total_mf_rating - ratio - size
        )

        if points_remaining <= 0:
            raise forms.ValidationError(
                "Node invalid: spend fewer points on merits/flaws, resonance, size, or ratio"
            )

        if ratio == -2:
            ratio = 0.0
        elif ratio == -1:
            ratio = 0.25
        elif ratio == 0:
            ratio = 0.5
        elif ratio == 1:
            ratio = 0.75
        elif ratio == 2:
            ratio = 1.0

        self.quintessence_per_week = int(points_remaining * float(ratio))
        self.tass_per_week = points_remaining - self.quintessence_per_week

        return cleaned_data
