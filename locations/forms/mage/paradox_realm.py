from django import forms

from locations.models.mage import ParadoxAtmosphere, ParadoxObstacle, ParadoxRealm


class ParadoxObstacleForm(forms.ModelForm):
    """Form for creating/editing individual obstacles"""

    class Meta:
        model = ParadoxObstacle
        fields = ["sphere", "obstacle_number", "order", "name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter obstacle name"})
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Enter obstacle description", "rows": 3}
        )


ParadoxObstacleFormSet = forms.inlineformset_factory(
    ParadoxRealm,
    ParadoxObstacle,
    form=ParadoxObstacleForm,
    extra=1,
    can_delete=True,
)


class ParadoxAtmosphereForm(forms.ModelForm):
    """Form for creating/editing individual atmosphere elements"""

    class Meta:
        model = ParadoxAtmosphere
        fields = ["paradigm", "atmosphere_number", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Enter atmosphere description", "rows": 3}
        )


ParadoxAtmosphereFormSet = forms.inlineformset_factory(
    ParadoxRealm,
    ParadoxAtmosphere,
    form=ParadoxAtmosphereForm,
    extra=1,
    can_delete=True,
)


class ParadoxRealmForm(forms.ModelForm):
    """Form for creating and editing Paradox Realms"""

    class Meta:
        model = ParadoxRealm
        fields = (
            "name",
            "description",
            "primary_sphere",
            "secondary_sphere",
            "paradigm",
            "secondary_paradigm",
            "num_primary_obstacles",
            "num_random_obstacles",
            "final_obstacle_type",
            "final_obstacle_details",
            "contained_within",
            "gauntlet",
            "shroud",
            "dimension_barrier",
        )
        widgets = {
            "final_obstacle_details": forms.Textarea(attrs={"rows": 3}),
        }

    generate_random = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Check this to automatically generate a random paradox realm",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter realm name"})
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description of the realm", "rows": 4}
        )
        self.fields["contained_within"].required = False
        self.fields["secondary_sphere"].required = False
        self.fields["secondary_paradigm"].required = False

        # Initialize formsets
        self.obstacle_formset = ParadoxObstacleFormSet(
            instance=self.instance if self.instance.pk else None,
            data=self.data if self.is_bound else None,
            prefix="obstacles",
        )

        self.atmosphere_formset = ParadoxAtmosphereFormSet(
            instance=self.instance if self.instance.pk else None,
            data=self.data if self.is_bound else None,
            prefix="atmospheres",
        )

    def is_valid(self):
        valid = super().is_valid()
        # Only validate formsets if not generating random
        if not self.cleaned_data.get("generate_random", False):
            valid = valid and self.obstacle_formset.is_valid()
            valid = valid and self.atmosphere_formset.is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()

        # If generate_random is checked, we'll handle this in save()
        # No additional validation needed here

        return cleaned_data

    def save(self, commit=True):
        # Check if we should generate random
        generate_random = self.cleaned_data.get("generate_random", False)

        if generate_random:
            # Generate a completely random realm
            name = self.cleaned_data.get("name", "Random Paradox Realm")
            realm = ParadoxRealm.random(name=name, save=commit)
            return realm
        else:
            # Normal save
            realm = super().save(commit=False)

            if commit:
                realm.save()

                # Save the formsets
                self.obstacle_formset.instance = realm
                self.obstacle_formset.save()

                self.atmosphere_formset.instance = realm
                self.atmosphere_formset.save()

            return realm
