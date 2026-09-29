from django import forms
from django.db.models import Q

from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from characters.services.rotes import SPHERE_FIELDS, learn_rote
from widgets import ChainedChoiceField, ChainedSelectMixin
from widgets.fields.create_or_select import CreateOrSelectField


class RoteCreationForm(ChainedSelectMixin, forms.Form):
    select_or_create_rote = CreateOrSelectField(
        select_field="rote_options",
        group_name="select_or_create_rote",
    )
    select_or_create_effect = CreateOrSelectField(
        select_field="effect_options",
        group_name="select_or_create_effect",
    )

    rote_options = forms.ModelChoiceField(queryset=Rote.objects.all(), required=False)
    effect_options = forms.ModelChoiceField(queryset=Effect.objects.all(), required=False)

    name = forms.CharField(max_length=100, required=False)
    practice = ChainedChoiceField(choices=[], required=False)
    attribute = forms.ModelChoiceField(queryset=Attribute.objects.all(), required=False)
    ability = ChainedChoiceField(parent_field="practice", choices_map={}, required=False)
    systems = forms.CharField(widget=forms.Textarea(), required=False)
    description = forms.CharField(widget=forms.Textarea(), required=False)
    correspondence = forms.IntegerField(min_value=0, initial=0, required=False)
    time = forms.IntegerField(min_value=0, initial=0, required=False)
    spirit = forms.IntegerField(min_value=0, initial=0, required=False)
    matter = forms.IntegerField(min_value=0, initial=0, required=False)
    life = forms.IntegerField(min_value=0, initial=0, required=False)
    forces = forms.IntegerField(min_value=0, initial=0, required=False)
    entropy = forms.IntegerField(min_value=0, initial=0, required=False)
    mind = forms.IntegerField(min_value=0, initial=0, required=False)
    prime = forms.IntegerField(min_value=0, initial=0, required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)

        practice_choices = self.instance.practices.exclude(
            polymorphic_ctype__model="specializedpractice"
        ).exclude(polymorphic_ctype__model="corruptedpractice")

        special_practices = self.instance.practices.filter(
            polymorphic_ctype__model="specializedpractice"
        ) | self.instance.practices.filter(polymorphic_ctype__model="corruptedpractice")
        special_practices = Practice.objects.filter(
            id__in=[x.parent_practice.id for x in special_practices]
        )

        practices = (practice_choices | special_practices).order_by("name")

        # Build practice choices for ChainedChoiceField
        self.fields["practice"].choices = [("", "---------")] + [
            (str(p.pk), str(p)) for p in practices
        ]

        # Build ability choices_map (practice → abilities)
        ability_choices_map = {}
        for practice in practices:
            abilities = practice.abilities.all().order_by("name")
            ability_choices_map[str(practice.pk)] = [(str(a.pk), str(a)) for a in abilities]
        self.fields["ability"].choices_map = ability_choices_map
        self.fields["correspondence"].widget.attrs["max"] = self.instance.correspondence
        self.fields["time"].widget.attrs["max"] = self.instance.time
        self.fields["spirit"].widget.attrs["max"] = self.instance.spirit
        self.fields["matter"].widget.attrs["max"] = self.instance.matter
        self.fields["life"].widget.attrs["max"] = self.instance.life
        self.fields["forces"].widget.attrs["max"] = self.instance.forces
        self.fields["entropy"].widget.attrs["max"] = self.instance.entropy
        self.fields["mind"].widget.attrs["max"] = self.instance.mind
        self.fields["prime"].widget.attrs["max"] = self.instance.prime

        # Query spheres once and reuse
        spheres = list(Sphere.objects.all())

        rote_filter_dict = {}
        effect_filter_dict = {}
        for sphere in spheres:
            rote_filter_dict["effect__" + sphere.property_name + "__lte"] = getattr(
                self.instance, sphere.property_name
            )
            effect_filter_dict[sphere.property_name + "__lte"] = getattr(
                self.instance, sphere.property_name
            )

        rote_filter_dict["effect__rote_cost__lte"] = self.instance.rote_points
        effect_filter_dict["rote_cost__lte"] = self.instance.rote_points

        rote_filter_dict["practice__in"] = list(self.instance.practices.all()) + [
            getattr(x, "parent_practice", None)
            for x in self.instance.practices.all()
            if getattr(x, "parent_practice", None) is not None
        ]

        pracdict = {x.practice: x.rating for x in self.instance.practicerating_set.all()}
        pracdict.update(
            {
                getattr(x.practice, "parent_practice", None): x.rating
                for x in self.instance.practicerating_set.all()
                if getattr(x.practice, "parent_practice", None) is not None
            }
        )

        practice_filter = Q()
        for practice, rating in pracdict.items():
            sphere_filter = {}
            for sphere in spheres:
                sphere_filter["effect__" + sphere.property_name + "__lte"] = rating
            practice_filter |= Q(practice=practice, **sphere_filter)

        effects_known = [x.effect.id for x in self.instance.rotes.all()]
        # Legacy global library entries have no creator or chronicle. They
        # remain selectable; private submitted work belongs to its creator.
        selectable = Q(status="App") | Q(owner__isnull=True, chronicle__isnull=True)
        if self.instance.owner_id is not None:
            selectable |= Q(owner_id=self.instance.owner_id)

        self.fields["rote_options"].queryset = (
            Rote.objects.filter(**rote_filter_dict)
            .filter(practice_filter)
            .filter(selectable)
            .exclude(id__in=self.instance.rotes.all())
        )
        self.fields["effect_options"].queryset = (
            Effect.objects.filter(**effect_filter_dict)
            .filter(selectable)
            .exclude(id__in=effects_known)
        )

        # Re-run chain setup after choices are configured
        self._setup_chains()

    # Fields a newly created rote must fill, in the order they are reported.
    REQUIRED_FOR_NEW_ROTE = (
        ("name", "Must choose rote name"),
        ("practice", "Must choose rote Practice"),
        ("attribute", "Must choose rote Attribute"),
        ("ability", "Must choose rote Ability"),
        ("description", "Must choose rote description"),
    )

    def clean(self):
        """Require a complete choice: a rote selected, or a new rote with an effect."""
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        if not cleaned_data["select_or_create_rote"] and not cleaned_data["rote_options"]:
            raise forms.ValidationError("Must create or select a rote")
        if not cleaned_data["select_or_create_rote"]:
            return cleaned_data
        if not cleaned_data["select_or_create_effect"] and not cleaned_data["effect_options"]:
            raise forms.ValidationError("Must create or select an effect")
        for field, message in self.REQUIRED_FOR_NEW_ROTE:
            if not cleaned_data[field]:
                raise forms.ValidationError(message)
        if cleaned_data["select_or_create_effect"]:
            if not cleaned_data["systems"]:
                raise forms.ValidationError("Must choose rote systems")
            if sum(cleaned_data[sphere] or 0 for sphere in SPHERE_FIELDS) == 0:
                raise forms.ValidationError("Effects must have sphere ratings")
        return cleaned_data

    def save(self, mage):
        """Learn the chosen rote; raises ValidationError when points run short."""
        result = learn_rote(mage, self.cleaned_data)
        if not result.success:
            raise forms.ValidationError(result.error)
        return True
