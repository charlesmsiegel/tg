"""
Multi-step forms for Freehold creation.
Each step corresponds to a stage in the creation process from Book of Freeholds.
"""
from django import forms
from locations.models.changeling import Freehold


class FreeholdBasicsForm(forms.ModelForm):
    """Step 1: Basic information (Name, Archetype, Aspect, Acquisition)"""

    class Meta:
        model = Freehold
        fields = ("name", "archetype", "aspect", "description")
        widgets = {
            "aspect": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "E.g., 'birthplace of chimerical creatures' or 'sexy nightclub with hidden primal darkness'"
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "How was this freehold acquired? What is its story?"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter freehold name"})
        self.fields["name"].help_text = "The name of your freehold"
        self.fields["archetype"].help_text = "The role this freehold plays in changeling society"
        self.fields["aspect"].help_text = "The underlying dream or story (e.g., water aspect, birthplace of  creatures)"
        self.fields["description"].help_text = "Acquisition story: how did you come across this freehold?"


class FreeholdFeaturesForm(forms.ModelForm):
    """Step 2: Feature allocation (Balefire, Size, Sanctuary, Resources, Passages)"""

    class Meta:
        model = Freehold
        fields = ("balefire", "size", "sanctuary", "resources", "passages", "balefire_description")
        widgets = {
            "balefire_description": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "What does the balefire look like and where is it located?"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["balefire"].help_text = "0-5 dots. Generates this many Glamour/dross per day"
        self.fields["size"].help_text = "0-5 dots. Determines physical area of the freehold"
        self.fields["sanctuary"].help_text = "0-5 dots. Grants defense bonuses and threshold"
        self.fields["resources"].help_text = "0-5 dots. Mundane or chimerical resources generated"
        self.fields["passages"].help_text = "Number of trods/raths (first is free, others cost 1 feature point each)"

    def clean(self):
        cleaned_data = super().clean()

        # Calculate feature points
        balefire = cleaned_data.get("balefire", 0)
        size = cleaned_data.get("size", 0)
        sanctuary = cleaned_data.get("sanctuary", 0)
        resources = cleaned_data.get("resources", 0)
        passages = cleaned_data.get("passages", 1)

        feature_points = balefire + size + sanctuary + resources
        if passages > 1:
            feature_points += (passages - 1)

        # Store for later access
        self.feature_points = feature_points

        return cleaned_data


class FreeholdPowersForm(forms.ModelForm):
    """Step 3: Powers selection"""

    class Meta:
        model = Freehold
        fields = ("powers", "dual_nature_archetype", "dual_nature_ability")
        widgets = {
            "powers": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dual_nature_archetype"].required = False
        self.fields["dual_nature_ability"].required = False
        self.fields["dual_nature_archetype"].help_text = "Required if Dual Nature power is selected"
        self.fields["dual_nature_ability"].help_text = "Required if dual nature archetype is Academy"

    def clean(self):
        cleaned_data = super().clean()
        powers = cleaned_data.get("powers", [])

        # Validate Dual Nature
        if "dual_nature" in powers:
            if not cleaned_data.get("dual_nature_archetype"):
                raise forms.ValidationError("Dual Nature power requires selecting a second archetype")
            if cleaned_data.get("dual_nature_archetype") == "academy" and not cleaned_data.get("dual_nature_ability"):
                raise forms.ValidationError("Dual Nature Academy requires specifying an ability")

        return cleaned_data


class FreeholdDetailsForm(forms.ModelForm):
    """Step 4: Details and descriptions"""

    class Meta:
        model = Freehold
        fields = (
            "academy_ability",
            "hearth_ability",
            "resource_description",
            "passage_description",
            "quirks",
            "parent",
            "owned_by",
        )
        widgets = {
            "resource_description": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "What resources does this freehold generate?"
            }),
            "passage_description": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Describe trods/raths and where they lead"
            }),
            "quirks": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Unique features that don't respond to holders' wishes"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["academy_ability"].required = False
        self.fields["hearth_ability"].required = False
        self.fields["parent"].required = False
        self.fields["owned_by"].required = False

        # Show/hide based on archetype
        if self.instance and self.instance.pk:
            if self.instance.archetype != "academy":
                self.fields["academy_ability"].widget = forms.HiddenInput()
            if self.instance.archetype != "hearth":
                self.fields["hearth_ability"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()

        # Get archetype from instance (it was set in step 1)
        if self.instance:
            archetype = self.instance.archetype

            # Validate Academy archetype
            if archetype == "academy" and not cleaned_data.get("academy_ability"):
                raise forms.ValidationError("Academy archetype requires an associated ability")

            # Validate Hearth archetype
            if archetype == "hearth" and not cleaned_data.get("hearth_ability"):
                raise forms.ValidationError("Hearth archetype requires choosing Leadership or Socialize")

        return cleaned_data
