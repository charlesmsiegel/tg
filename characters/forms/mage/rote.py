
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from django import forms
from django.db.models import Q


class RoteCreationForm(forms.Form):
    select_or_create_rote = forms.BooleanField(required=False)
    select_or_create_effect = forms.BooleanField(required=False)

    rote_options = forms.ModelChoiceField(queryset=Rote.objects.all(), required=False)
    effect_options = forms.ModelChoiceField(
        queryset=Effect.objects.all(), required=False
    )

    name = forms.CharField(max_length=100, required=False)
    practice = forms.ModelChoiceField(queryset=Practice.objects.none(), required=False)
    attribute = forms.ModelChoiceField(queryset=Attribute.objects.all(), required=False)
    ability = forms.ModelChoiceField(queryset=Ability.objects.all(), required=False)
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

        self.fields["practice"].queryset = (
            practice_choices | special_practices
        ).order_by("name")
        self.fields["correspondence"].widget.attrs["max"] = getattr(
            self.instance, "correspondence"
        )
        self.fields["time"].widget.attrs["max"] = getattr(self.instance, "time")
        self.fields["spirit"].widget.attrs["max"] = getattr(self.instance, "spirit")
        self.fields["matter"].widget.attrs["max"] = getattr(self.instance, "matter")
        self.fields["life"].widget.attrs["max"] = getattr(self.instance, "life")
        self.fields["forces"].widget.attrs["max"] = getattr(self.instance, "forces")
        self.fields["entropy"].widget.attrs["max"] = getattr(self.instance, "entropy")
        self.fields["mind"].widget.attrs["max"] = getattr(self.instance, "mind")
        self.fields["prime"].widget.attrs["max"] = getattr(self.instance, "prime")

        rote_filter_dict = {}
        effect_filter_dict = {}
        for sphere in Sphere.objects.all():
            rote_filter_dict["effect__" + sphere.property_name + "__lte"] = getattr(
                self.instance, sphere.property_name
            )
            effect_filter_dict[sphere.property_name + "__lte"] = getattr(
                self.instance, sphere.property_name
            )

        rote_filter_dict["effect__rote_cost__lte"] = getattr(
            self.instance, "rote_points"
        )
        effect_filter_dict["rote_cost__lte"] = getattr(self.instance, "rote_points")

        rote_filter_dict["practice__in"] = list(self.instance.practices.all()) + [
            getattr(x, "parent_practice", None)
            for x in self.instance.practices.all()
            if getattr(x, "parent_practice", None) is not None
        ]

        pracdict = {
            x.practice: x.rating for x in self.instance.practicerating_set.all()
        }
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
            for sphere in Sphere.objects.all():
                sphere_filter["effect__" + sphere.property_name + "__lte"] = rating
            practice_filter |= Q(practice=practice, **sphere_filter)

        effects_known = [x.effect.id for x in self.instance.rotes.all()]

        self.fields["rote_options"].queryset = (
            Rote.objects.filter(**rote_filter_dict)
            .filter(practice_filter)
            .exclude(id__in=self.instance.rotes.all())
        )
        self.fields["effect_options"].queryset = Effect.objects.filter(
            **effect_filter_dict
        ).exclude(id__in=effects_known)

    def save(self, mage):
        if self.cleaned_data["select_or_create_rote"]:
            # Create Rote
            name = self.cleaned_data.get("name")
            practice = self.cleaned_data.get("practice")
            attribute = self.cleaned_data.get("attribute")
            ability = Ability.objects.get(pk=self.data.get("ability"))
            description = self.cleaned_data.get("description")
            if self.cleaned_data["select_or_create_effect"]:
                # Create Effect
                systems = self.cleaned_data.get("systems")
                correspondence = self.cleaned_data.get("correspondence")
                time = self.cleaned_data.get("time")
                spirit = self.cleaned_data.get("spirit")
                matter = self.cleaned_data.get("matter")
                life = self.cleaned_data.get("life")
                forces = self.cleaned_data.get("forces")
                entropy = self.cleaned_data.get("entropy")
                mind = self.cleaned_data.get("mind")
                prime = self.cleaned_data.get("prime")
                e = Effect(
                    correspondence=correspondence,
                    time=time,
                    spirit=spirit,
                    matter=matter,
                    life=life,
                    forces=forces,
                    entropy=entropy,
                    mind=mind,
                    prime=prime,
                    description=systems,
                    name=name,
                    status="Sub",
                )
                if e.is_learnable(mage) and e.cost() <= mage.rote_points:
                    e.save()
                else:
                    raise forms.ValidationError("Not enough Rote Points")
            else:
                # Select Effect
                e = self.cleaned_data["effect_options"]
            r = Rote.objects.create(
                name=name,
                practice=practice,
                attribute=attribute,
                ability=ability,
                description=description,
                effect=e,
                status="Sub",
                chronicle=self.instance.chronicle,
            )
        else:
            # Select Rote
            r = self.cleaned_data["rote_options"]
            e = r.effect
        mage.rotes.add(r)
        mage.rote_points -= e.cost()
        mage.save()
        return True
