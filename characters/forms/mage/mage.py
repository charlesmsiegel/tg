from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from django import forms
from django.core.exceptions import ValidationError


class MageCreationForm(forms.ModelForm):
    class Meta:
        model = Mage
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "affiliation",
            "faction",
            "subfaction",
            "essence",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["affiliation"].queryset = MageFaction.objects.filter(parent=None)
        self.fields["faction"].queryset = MageFaction.objects.none()
        self.fields["subfaction"].queryset = MageFaction.objects.none()
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["image"].required = False
        if self.user is not None:
            if not self.user.profile.is_st():
                self.fields["affiliation"].queryset = self.fields["affiliation"].queryset.exclude(
                    name__in=["Nephandi", "Marauders"]
                )

        if self.is_bound:
            self.fields["faction"].queryset = MageFaction.objects.all()
            self.fields["subfaction"].queryset = MageFaction.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # If we have a user
            instance.owner = self.user
        if commit:
            instance.save()
        return instance


class MageSpheresForm(forms.ModelForm):
    """Form for selecting Spheres and Arete during character creation."""

    class Meta:
        model = Mage
        fields = [
            "arete",
            "correspondence",
            "time",
            "spirit",
            "forces",
            "matter",
            "life",
            "entropy",
            "mind",
            "prime",
            "affinity_sphere",
            "corr_name",
            "prime_name",
            "spirit_name",
            "resonance",
        ]

    def clean_affinity_sphere(self):
        """Validate that an affinity sphere is selected."""
        affinity_sphere = self.cleaned_data.get("affinity_sphere")
        if affinity_sphere is None:
            raise ValidationError("You must select a valid affinity sphere.")
        return affinity_sphere

    def clean_arete(self):
        """Validate that Arete doesn't exceed 3 at character creation."""
        arete = self.cleaned_data.get("arete", 1)
        if arete > 3:
            raise ValidationError("Arete may not exceed 3 at character creation.")
        return arete

    def clean(self):
        """Validate sphere ratings and distribution."""
        cleaned_data = super().clean()

        # Get all sphere values
        arete = cleaned_data.get("arete", 1)
        correspondence = cleaned_data.get("correspondence", 0)
        time = cleaned_data.get("time", 0)
        spirit = cleaned_data.get("spirit", 0)
        forces = cleaned_data.get("forces", 0)
        matter = cleaned_data.get("matter", 0)
        life = cleaned_data.get("life", 0)
        entropy = cleaned_data.get("entropy", 0)
        mind = cleaned_data.get("mind", 0)
        prime = cleaned_data.get("prime", 0)
        affinity_sphere = cleaned_data.get("affinity_sphere")

        # Check individual sphere ratings
        spheres = [
            correspondence,
            time,
            spirit,
            forces,
            matter,
            life,
            entropy,
            mind,
            prime,
        ]
        for sphere_value in spheres:
            if sphere_value < 0 or sphere_value > arete:
                raise ValidationError("Spheres must range from 0-Arete Rating.")

        # Check that affinity sphere is nonzero
        if affinity_sphere and self.instance:
            affinity_value = getattr(self.instance, affinity_sphere.property_name, None)
            # Check in cleaned_data first (in case it's being set now)
            if affinity_value == 0 and cleaned_data.get(affinity_sphere.property_name, 0) == 0:
                raise ValidationError("Affinity Sphere must be nonzero.")

        # Check total sphere points
        total_spheres = sum(spheres)
        if total_spheres != 6:
            raise ValidationError(f"Spheres must total 6 (currently {total_spheres}).")

        return cleaned_data
