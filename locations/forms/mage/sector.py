from django import forms
from locations.models.mage.sector import Sector


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = [
            "name",
            "description",
            "parent",
            # Classification
            "sector_class",
            "access_level",
            # Power and Security
            "power_rating",
            "security_level",
            "requires_password",
            "password_hint",
            "approved_users",
            # Constraints
            "constraints",
            "genre_theme",
            # Structure
            "size_rating",
            "administrator",
            # Reality Zone
            "reality_zone",
            "difficulty_modifier",
            # Special Properties
            "has_lag",
            "paradox_risk_modifier",
            # Corruption
            "is_reformattable",
            "corruption_level",
            # Temporal
            "time_dilation",
            "temporal_instability",
            # ARO
            "aro_count",
            "aro_density",
            # Streamland
            "data_flow_rate",
            # Population
            "estimated_users",
            # Connections
            "connected_sectors",
            # Notes
            "hazards",
            "notable_features",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "constraints": forms.Textarea(attrs={"rows": 6}),
            "approved_users": forms.Textarea(attrs={"rows": 4}),
            "hazards": forms.Textarea(attrs={"rows": 4}),
            "notable_features": forms.Textarea(attrs={"rows": 4}),
            "connected_sectors": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and help text
        self.fields["name"].widget.attrs.update(
            {"placeholder": "Sector name (e.g., 'Spy's Demise')"}
        )
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Describe the sector's appearance, purpose, and general atmosphere..."}
        )
        self.fields["genre_theme"].widget.attrs.update(
            {"placeholder": "e.g., Film Noir, Cyberpunk, Medieval Fantasy"}
        )
        self.fields["constraints"].widget.attrs.update(
            {"placeholder": "Describe constraint protocols: genre enforcement, tech requirements, paradigm restrictions..."}
        )
        self.fields["password_hint"].widget.attrs.update(
            {"placeholder": "Hint for sector password (if applicable)"}
        )
        self.fields["approved_users"].widget.attrs.update(
            {"placeholder": "List approved user types/credentials, one per line"}
        )
        self.fields["administrator"].widget.attrs.update(
            {"placeholder": "e.g., Iteration X, The Bartender, Virtual Adepts"}
        )
        self.fields["hazards"].widget.attrs.update(
            {"placeholder": "Environmental hazards, hostile entities, security measures, etc."}
        )
        self.fields["notable_features"].widget.attrs.update(
            {"placeholder": "Landmarks, AROs, unique properties, special locations..."}
        )

        # Set parent as not required
        self.fields["parent"].required = False
        self.fields["parent"].empty_label = "Parent Location (Optional)"

        # Optional fields
        for field in ["password_hint", "genre_theme", "data_flow_rate", "reality_zone"]:
            if field in self.fields:
                self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()

        # Validate password requirements
        requires_password = cleaned_data.get("requires_password")
        password_hint = cleaned_data.get("password_hint")
        access_level = cleaned_data.get("access_level")

        if requires_password and not password_hint:
            self.add_error(
                "password_hint",
                "Password hint is recommended when password is required."
            )

        # Validate restricted sector has security measures
        if access_level == "restricted":
            approved_users = cleaned_data.get("approved_users")
            if not requires_password and not approved_users:
                self.add_error(
                    "approved_users",
                    "Restricted sectors should have either a password or approved users list."
                )

        # Validate corruption level
        corruption_level = cleaned_data.get("corruption_level", 0)
        is_reformattable = cleaned_data.get("is_reformattable", True)

        if corruption_level >= 8 and is_reformattable:
            self.add_error(
                "is_reformattable",
                "Heavily corrupted sectors (8+) are typically unreformattable."
            )

        # Validate power rating for warzones
        sector_class = cleaned_data.get("sector_class")
        power_rating = cleaned_data.get("power_rating", 5)

        if sector_class == "warzone" and power_rating < 7:
            self.add_error(
                "power_rating",
                "Warzones should have power rating of 7 to handle combat."
            )

        # Validate time dilation for hung sectors
        temporal_instability = cleaned_data.get("temporal_instability", False)
        time_dilation = cleaned_data.get("time_dilation", 1.00)

        if temporal_instability and time_dilation == 1.00:
            self.add_error(
                "time_dilation",
                "Temporally unstable sectors should have unusual time dilation."
            )

        return cleaned_data
