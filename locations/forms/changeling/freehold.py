from django import forms
from locations.models.changeling import Freehold


class FreeholdForm(forms.ModelForm):
    """Form for creating and editing Freeholds"""

    class Meta:
        model = Freehold
        fields = (
            "name",
            "description",
            "archetype",
            "aspect",
            "quirks",
            "balefire",
            "size",
            "sanctuary",
            "resources",
            "passages",
            "powers",
            "academy_ability",
            "hearth_ability",
            "dual_nature_archetype",
            "dual_nature_ability",
            "resource_description",
            "passage_description",
            "balefire_description",
            "parent",
            "owned_by",
            "gauntlet",
            "shroud",
            "dimension_barrier",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Enter freehold description"}
            ),
            "aspect": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "E.g., 'birthplace of chimerical creatures' or 'sexy nightclub with hidden primal darkness'",
                }
            ),
            "quirks": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Unique features that don't respond to holders' wishes",
                }
            ),
            "resource_description": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "What resources does this freehold generate?",
                }
            ),
            "passage_description": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Describe trods/raths and where they lead",
                }
            ),
            "balefire_description": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "What does the balefire look like and where is it?",
                }
            ),
            "powers": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter freehold name"})
        self.fields["academy_ability"].widget.attrs.update({"placeholder": "E.g., Melee, Kenning"})
        self.fields["dual_nature_ability"].widget.attrs.update(
            {"placeholder": "If dual nature second archetype is Academy"}
        )

        # Make parent and owned_by not required
        self.fields["parent"].required = False
        self.fields["owned_by"].required = False

        # Set help text
        self.fields["balefire"].help_text = "0-5 dots. Determines Glamour/dross generation"
        self.fields["size"].help_text = "0-5 dots. Determines physical size"
        self.fields["sanctuary"].help_text = "0-5 dots. Grants defense bonuses"
        self.fields["resources"].help_text = "0-5 dots. Mundane or chimerical resources"
        self.fields["passages"].help_text = "Number of trods/raths (first is free)"

        # Show/hide archetype-specific fields based on selection
        if self.instance and self.instance.pk:
            # For editing existing freehold
            if self.instance.archetype != "academy":
                self.fields["academy_ability"].widget = forms.HiddenInput()
            if self.instance.archetype != "hearth":
                self.fields["hearth_ability"].widget = forms.HiddenInput()
            if "dual_nature" not in self.instance.powers:
                self.fields["dual_nature_archetype"].widget = forms.HiddenInput()
                self.fields["dual_nature_ability"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        archetype = cleaned_data.get("archetype")
        powers = cleaned_data.get("powers", [])

        # Validate Academy archetype has ability
        if archetype == "academy" and not cleaned_data.get("academy_ability"):
            raise forms.ValidationError("Academy archetype requires an associated ability")

        # Validate Hearth archetype has ability choice
        if archetype == "hearth" and not cleaned_data.get("hearth_ability"):
            raise forms.ValidationError(
                "Hearth archetype requires choosing Leadership or Socialize"
            )

        # Validate Dual Nature has second archetype
        if "dual_nature" in powers and not cleaned_data.get("dual_nature_archetype"):
            raise forms.ValidationError("Dual Nature power requires a second archetype")

        # Validate Dual Nature Academy has ability
        if (
            "dual_nature" in powers
            and cleaned_data.get("dual_nature_archetype") == "academy"
            and not cleaned_data.get("dual_nature_ability")
        ):
            raise forms.ValidationError("Dual Nature Academy requires an associated ability")

        # Calculate feature points
        balefire = cleaned_data.get("balefire", 0)
        size = cleaned_data.get("size", 0)
        sanctuary = cleaned_data.get("sanctuary", 0)
        resources = cleaned_data.get("resources", 0)
        passages = cleaned_data.get("passages", 1)

        feature_points = balefire + size + sanctuary + resources

        # First passage is free
        if passages > 1:
            feature_points += passages - 1

        # Add power costs
        power_costs = {
            "warning_call": 1,
            "glamour_to_dross": 2,
            "resonant_dreams": 2,
            "call_forth_flame": 3,
            "dual_nature": 3,
        }
        for power in powers:
            feature_points += power_costs.get(power, 0)

        # Store for display
        self.feature_points = feature_points
        self.holdings_required = (feature_points + 2) // 3  # Round up

        return cleaned_data

    def save(self, commit=True):
        freehold = super().save(commit=False)

        # Clear archetype-specific fields that don't apply
        if freehold.archetype != "academy":
            freehold.academy_ability = ""
        if freehold.archetype != "hearth":
            freehold.hearth_ability = ""
        if "dual_nature" not in freehold.powers:
            freehold.dual_nature_archetype = ""
            freehold.dual_nature_ability = ""

        if commit:
            freehold.save()

        return freehold
