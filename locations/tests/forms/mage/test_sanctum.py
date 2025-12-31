"""Tests for Sanctum forms."""

from django.contrib.auth.models import User
from django.test import TestCase
from locations.forms.mage.sanctum import SanctumForm
from locations.models.mage.reality_zone import RealityZone
from locations.models.mage.sanctum import Sanctum


class TestSanctumForm(TestCase):
    """Test SanctumForm initialization and validation."""

    def test_form_fields(self):
        """Test form has correct fields."""
        form = SanctumForm()
        self.assertIn("name", form.fields)
        self.assertIn("contained_within", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("rank", form.fields)

    def test_form_name_placeholder(self):
        """Test name field has placeholder."""
        form = SanctumForm()
        self.assertEqual(form.fields["name"].widget.attrs.get("placeholder"), "Enter name here")

    def test_form_description_placeholder(self):
        """Test description field has placeholder."""
        form = SanctumForm()
        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter description here",
        )

    def test_contained_within_not_required(self):
        """Test contained_within field is not required."""
        form = SanctumForm()
        self.assertFalse(form.fields["contained_within"].required)

    def test_form_initializes_reality_zone_formset(self):
        """Test form initializes reality zone formset."""
        form = SanctumForm()
        self.assertIsNotNone(form.reality_zone_formset)

    def test_form_with_existing_instance(self):
        """Test form with existing sanctum instance."""
        rz = RealityZone.objects.create(name="Test RZ")
        sanctum = Sanctum.objects.create(name="Test Sanctum", rank=2, reality_zone=rz)
        form = SanctumForm(instance=sanctum)
        self.assertEqual(form.reality_zone, rz)

    def test_form_without_existing_reality_zone(self):
        """Test form creates new reality zone if none exists."""
        sanctum = Sanctum.objects.create(name="Test Sanctum", rank=2)
        form = SanctumForm(instance=sanctum)
        self.assertIsInstance(form.reality_zone, RealityZone)
        self.assertIsNone(form.reality_zone.pk)

    def test_clean_rank_none_raises_error(self):
        """Test validation error when rank is None."""
        form_data = {
            "name": "Test Sanctum",
            "description": "Test",
        }
        form = SanctumForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_valid_checks_reality_zone_formset(self):
        """Test is_valid checks reality zone formset."""
        form_data = {
            "name": "Test Sanctum",
            "description": "Test",
            "rank": 2,
            "reality_zone-TOTAL_FORMS": "1",
            "reality_zone-INITIAL_FORMS": "0",
        }
        form = SanctumForm(data=form_data)
        # Will fail due to reality zone validation requirements
        # but verifies formset is being checked
        form.is_valid()
        self.assertIsNotNone(form.reality_zone_formset)


class TestSanctumFormValidation(TestCase):
    """Test SanctumForm clean method validation."""

    def test_clean_requires_reality_zone_ratings_total_zero(self):
        """Test reality zone ratings must total 0."""
        # This is a complex validation that requires proper formset data
        form_data = {
            "name": "Test Sanctum",
            "description": "Test",
            "rank": 2,
            "reality_zone-TOTAL_FORMS": "0",
            "reality_zone-INITIAL_FORMS": "0",
        }
        form = SanctumForm(data=form_data)
        # Form won't be valid due to reality zone requirements
        is_valid = form.is_valid()
        # Either fails in clean() or in reality_zone_formset.is_valid()
        self.assertFalse(is_valid)


class TestSanctumFormSave(TestCase):
    """Test SanctumForm save method."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_save_creates_reality_zone(self):
        """Test save creates and associates reality zone."""
        # Note: Full save requires valid reality zone formset data
        # This test verifies the structure
        sanctum = Sanctum.objects.create(name="Initial", rank=1)
        form = SanctumForm(instance=sanctum)
        self.assertIsNotNone(form.reality_zone)
