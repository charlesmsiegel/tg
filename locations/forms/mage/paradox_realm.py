from django import forms
from locations.models.mage import ParadoxRealm


class ParadoxRealmForm(forms.ModelForm):
    """Form for creating and editing Paradox Realms"""

    class Meta:
        model = ParadoxRealm
        fields = (
            "name",
            "description",
            "primary_sphere",
            "paradigm",
            "atmosphere_details",
            "obstacles",
            "final_obstacle",
            "parent",
            "gauntlet",
            "shroud",
            "dimension_barrier",
        )
        widgets = {
            "atmosphere_details": forms.Textarea(attrs={"rows": 4}),
            "obstacles": forms.Textarea(attrs={"rows": 6}),
            "final_obstacle": forms.Textarea(attrs={"rows": 3}),
        }

    generate_random = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Check this to generate a random paradox realm"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter realm name"})
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description of the realm"}
        )
        self.fields["parent"].required = False

        # Add help text
        self.fields["primary_sphere"].help_text = (
            "The sphere that created the greatest paradox buildup"
        )
        self.fields["paradigm"].help_text = (
            "How the paradox realm interprets reality"
        )

    def clean(self):
        cleaned_data = super().clean()

        # If generate_random is checked, override with random data
        if cleaned_data.get("generate_random"):
            name = cleaned_data.get("name", "Random Paradox Realm")
            realm = ParadoxRealm.generate_random(name=name)

            # Update cleaned_data with random values
            cleaned_data["primary_sphere"] = realm.primary_sphere
            cleaned_data["paradigm"] = realm.paradigm
            cleaned_data["atmosphere_details"] = realm.atmosphere_details
            cleaned_data["obstacles"] = realm.obstacles
            cleaned_data["final_obstacle"] = realm.final_obstacle

        return cleaned_data

    def save(self, commit=True):
        realm = super().save(commit=False)

        if commit:
            realm.save()

        return realm
