"""Tests for Sector forms."""

from django.test import TestCase

from locations.forms.mage.sector import SectorForm


class TestSectorFormFields(TestCase):
    """Test SectorForm field configuration."""

    def test_form_fields(self):
        """Test form has expected fields."""
        form = SectorForm()
        expected_fields = [
            "name",
            "description",
            "contained_within",
            "sector_class",
            "access_level",
            "power_rating",
            "security_level",
            "requires_password",
            "password_hint",
            "approved_users",
            "constraints",
            "genre_theme",
            "size_rating",
            "administrator",
            "reality_zone",
            "difficulty_modifier",
            "has_lag",
            "paradox_risk_modifier",
            "is_reformattable",
            "corruption_level",
            "time_dilation",
            "temporal_instability",
            "aro_count",
            "aro_density",
            "data_flow_rate",
            "estimated_users",
            "connected_sectors",
            "hazards",
            "notable_features",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_name_placeholder(self):
        """Test name field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["name"].widget.attrs.get("placeholder")
        self.assertIn("Sector name", placeholder)

    def test_description_placeholder(self):
        """Test description field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["description"].widget.attrs.get("placeholder")
        self.assertIn("Describe", placeholder)

    def test_genre_theme_placeholder(self):
        """Test genre theme field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["genre_theme"].widget.attrs.get("placeholder")
        self.assertIn("Film Noir", placeholder)

    def test_constraints_placeholder(self):
        """Test constraints field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["constraints"].widget.attrs.get("placeholder")
        self.assertIn("constraint protocols", placeholder)

    def test_password_hint_placeholder(self):
        """Test password hint field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["password_hint"].widget.attrs.get("placeholder")
        self.assertIn("Hint", placeholder)

    def test_approved_users_placeholder(self):
        """Test approved users field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["approved_users"].widget.attrs.get("placeholder")
        self.assertIn("approved user types", placeholder)

    def test_administrator_placeholder(self):
        """Test administrator field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["administrator"].widget.attrs.get("placeholder")
        self.assertIn("Iteration X", placeholder)

    def test_hazards_placeholder(self):
        """Test hazards field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["hazards"].widget.attrs.get("placeholder")
        self.assertIn("Environmental hazards", placeholder)

    def test_notable_features_placeholder(self):
        """Test notable features field has placeholder."""
        form = SectorForm()
        placeholder = form.fields["notable_features"].widget.attrs.get("placeholder")
        self.assertIn("Landmarks", placeholder)

    def test_contained_within_not_required(self):
        """Test contained_within field is not required."""
        form = SectorForm()
        self.assertFalse(form.fields["contained_within"].required)

    def test_optional_fields_not_required(self):
        """Test optional fields are not required."""
        form = SectorForm()
        for field in ["password_hint", "genre_theme", "data_flow_rate", "reality_zone"]:
            self.assertFalse(form.fields[field].required, f"{field} should not be required")


class TestSectorFormValidation(TestCase):
    """Test SectorForm clean method validation."""

    def test_valid_basic_form(self):
        """Test basic form submission is valid."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "grid",
            "access_level": "free",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_password_required_warning_without_hint(self):
        """Test warning when password required but no hint."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "grid",
            "access_level": "free",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": True,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        form.is_valid()
        self.assertIn("password_hint", form.errors)

    def test_restricted_sector_needs_security_measures(self):
        """Test restricted sectors need password or approved users."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "grid",
            "access_level": "restricted",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        form.is_valid()
        self.assertIn("approved_users", form.errors)

    def test_restricted_sector_with_password_is_valid(self):
        """Test restricted sector with password is valid."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "grid",
            "access_level": "restricted",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": True,
            "password_hint": "Think about numbers",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_restricted_sector_with_approved_users_is_valid(self):
        """Test restricted sector with approved users is valid."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "grid",
            "access_level": "restricted",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "admin\nviewer",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_high_corruption_should_be_unreformattable(self):
        """Test heavily corrupted sectors should be unreformattable."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "corrupted",
            "access_level": "free",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 8,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        form.is_valid()
        self.assertIn("is_reformattable", form.errors)

    def test_warzone_needs_high_power_rating(self):
        """Test warzones should have power rating of 7+."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "warzone",
            "access_level": "free",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        form.is_valid()
        self.assertIn("power_rating", form.errors)

    def test_warzone_with_high_power_is_valid(self):
        """Test warzone with power rating 7+ is valid."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "warzone",
            "access_level": "free",
            "power_rating": 7,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": False,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_temporal_instability_needs_unusual_dilation(self):
        """Test temporally unstable sectors need unusual time dilation."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "grid",
            "access_level": "free",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "1.00",
            "temporal_instability": True,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        form.is_valid()
        self.assertIn("time_dilation", form.errors)

    def test_temporal_instability_with_unusual_dilation_is_valid(self):
        """Test temporally unstable sector with unusual dilation is valid."""
        form_data = {
            "name": "Test Sector",
            "description": "A test sector",
            "sector_class": "grid",
            "access_level": "free",
            "power_rating": 5,
            "security_level": 0,
            "requires_password": False,
            "password_hint": "",
            "approved_users": "",
            "constraints": "",
            "genre_theme": "",
            "size_rating": 1,
            "administrator": "",
            "difficulty_modifier": 0,
            "has_lag": False,
            "paradox_risk_modifier": 0,
            "is_reformattable": True,
            "corruption_level": 0,
            "time_dilation": "2.50",
            "temporal_instability": True,
            "aro_count": 0,
            "aro_density": "moderate",
            "data_flow_rate": "",
            "estimated_users": 0,
            "hazards": "",
            "notable_features": "",
        }
        form = SectorForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
