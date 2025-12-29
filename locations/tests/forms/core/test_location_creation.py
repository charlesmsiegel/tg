"""
Tests for LocationCreationForm.

Tests cover:
- Form structure and fields
- ST vs regular user behavior
- Gameline and location type filtering
- Label formatting
"""

from accounts.models import Profile
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, ObjectType
from locations.forms.core.location_creation import LocationCreationForm


class TestLocationCreationFormSetup(TestCase):
    """Shared setup for LocationCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for LocationCreationForm tests."""
        # Create users
        cls.regular_user = User.objects.create_user(username="regular", password="password")
        Profile.objects.get_or_create(user=cls.regular_user)

        cls.st_user = User.objects.create_user(username="st", password="password")
        Profile.objects.get_or_create(user=cls.st_user)

        # Create chronicle for ST relationship
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")
        cls.chronicle.storytellers.add(cls.st_user)

        # Create location ObjectTypes
        ObjectType.objects.get_or_create(name="node", type="loc", gameline="mta")
        ObjectType.objects.get_or_create(name="chantry", type="loc", gameline="mta")
        ObjectType.objects.get_or_create(name="sanctum", type="loc", gameline="mta")
        ObjectType.objects.get_or_create(name="reality_zone", type="loc", gameline="mta")
        ObjectType.objects.get_or_create(name="domain", type="loc", gameline="vtm")
        ObjectType.objects.get_or_create(name="haven", type="loc", gameline="vtm")
        ObjectType.objects.get_or_create(name="freehold", type="loc", gameline="ctd")
        ObjectType.objects.get_or_create(name="horizon_realm", type="loc", gameline="mta")


class TestLocationCreationFormBasics(TestLocationCreationFormSetup):
    """Test basic LocationCreationForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = LocationCreationForm(user=self.st_user)

        self.assertIn("gameline", form.fields)
        self.assertIn("loc_type", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("rank", form.fields)

    def test_name_field_not_required(self):
        """Test that name field is not required."""
        form = LocationCreationForm(user=self.st_user)

        self.assertFalse(form.fields["name"].required)

    def test_rank_has_max_value(self):
        """Test that rank field has max_value of 5."""
        form = LocationCreationForm(user=self.st_user)

        self.assertEqual(form.fields["rank"].max_value, 5)

    def test_rank_has_initial_value(self):
        """Test that rank field has initial value of 1."""
        form = LocationCreationForm(user=self.st_user)

        self.assertEqual(form.fields["rank"].initial, 1)

    def test_gameline_select_has_id(self):
        """Test that gameline select has correct id attribute."""
        form = LocationCreationForm(user=self.st_user)

        self.assertEqual(form.fields["gameline"].widget.attrs.get("id"), "id_loc_gameline")

    def test_loc_type_select_has_id(self):
        """Test that loc_type select has correct id attribute."""
        form = LocationCreationForm(user=self.st_user)

        self.assertEqual(form.fields["loc_type"].widget.attrs.get("id"), "id_loc_type")


class TestLocationCreationFormSTBehavior(TestLocationCreationFormSetup):
    """Test LocationCreationForm behavior for ST users."""

    def test_st_sees_all_gamelines(self):
        """Test that ST users see all gamelines with locations."""
        form = LocationCreationForm(user=self.st_user)

        gameline_values = [choice[0] for choice in form.fields["gameline"].choices]

        # Should have all gamelines that have location types
        self.assertIn("mta", gameline_values)
        self.assertIn("vtm", gameline_values)
        self.assertIn("ctd", gameline_values)

    def test_st_sees_all_location_types(self):
        """Test that ST users see all location types."""
        form = LocationCreationForm(user=self.st_user)

        # Check data-types-by-gameline contains all types
        types_json = form.fields["loc_type"].widget.attrs.get("data-types-by-gameline")
        self.assertIsNotNone(types_json)

        import json

        types_by_gameline = json.loads(types_json)

        # Check MtA types
        mta_type_values = [t["value"] for t in types_by_gameline.get("mta", [])]
        self.assertIn("node", mta_type_values)
        self.assertIn("chantry", mta_type_values)
        self.assertIn("sanctum", mta_type_values)

        # Check VtM types
        vtm_type_values = [t["value"] for t in types_by_gameline.get("vtm", [])]
        self.assertIn("domain", vtm_type_values)
        self.assertIn("haven", vtm_type_values)

    def test_st_initial_loc_type_choices(self):
        """Test that ST users get initial loc_type choices from first gameline."""
        form = LocationCreationForm(user=self.st_user)

        # Initial choices should be from the first gameline
        loc_type_values = [choice[0] for choice in form.fields["loc_type"].choices]

        # Should have some location types
        self.assertGreater(len(loc_type_values), 0)


class TestLocationCreationFormRegularUserBehavior(TestLocationCreationFormSetup):
    """Test LocationCreationForm behavior for regular users."""

    def test_regular_user_sees_only_mage(self):
        """Test that regular users only see mage gameline."""
        form = LocationCreationForm(user=self.regular_user)

        gameline_values = [choice[0] for choice in form.fields["gameline"].choices]

        self.assertEqual(len(gameline_values), 1)
        self.assertIn("mta", gameline_values)
        self.assertNotIn("vtm", gameline_values)
        self.assertNotIn("ctd", gameline_values)

    def test_regular_user_sees_only_mage_locations(self):
        """Test that regular users only see mage location types."""
        form = LocationCreationForm(user=self.regular_user)

        loc_type_values = [choice[0] for choice in form.fields["loc_type"].choices]

        self.assertIn("node", loc_type_values)
        self.assertIn("chantry", loc_type_values)
        self.assertIn("sanctum", loc_type_values)
        self.assertNotIn("domain", loc_type_values)
        self.assertNotIn("haven", loc_type_values)

    def test_regular_user_types_by_gameline_data(self):
        """Test that regular users have types-by-gameline data."""
        form = LocationCreationForm(user=self.regular_user)

        types_json = form.fields["loc_type"].widget.attrs.get("data-types-by-gameline")
        self.assertIsNotNone(types_json)

        import json

        types_by_gameline = json.loads(types_json)

        # Should only have mta
        self.assertIn("mta", types_by_gameline)
        self.assertEqual(len(types_by_gameline), 1)


class TestLocationCreationFormLabelFormatting(TestLocationCreationFormSetup):
    """Test label formatting in LocationCreationForm."""

    def test_format_label_regular(self):
        """Test formatting of regular labels."""
        form = LocationCreationForm(user=self.st_user)

        self.assertEqual(form._format_label("node"), "Node")
        self.assertEqual(form._format_label("chantry"), "Chantry")
        self.assertEqual(form._format_label("sanctum"), "Sanctum")

    def test_format_label_special_cases(self):
        """Test formatting of special case labels."""
        form = LocationCreationForm(user=self.st_user)

        self.assertEqual(form._format_label("reality_zone"), "Reality Zone")
        self.assertEqual(form._format_label("horizon_realm"), "Horizon Realm")

    def test_format_label_underscore_handling(self):
        """Test that underscores are replaced with spaces."""
        form = LocationCreationForm(user=self.st_user)

        self.assertEqual(form._format_label("some_location_type"), "Some Location Type")


class TestLocationCreationFormValidation(TestLocationCreationFormSetup):
    """Test LocationCreationForm validation."""

    def test_valid_form_data(self):
        """Test that form validates with valid data."""
        # Get the first available gameline and loc_type
        form = LocationCreationForm(user=self.st_user)
        first_gameline = form.fields["gameline"].choices[0][0]
        first_loc_type = form.fields["loc_type"].choices[0][0]

        form_data = {
            "gameline": first_gameline,
            "loc_type": first_loc_type,
            "name": "Test Location",
            "rank": 3,
        }

        form2 = LocationCreationForm(data=form_data, user=self.st_user)

        self.assertTrue(form2.is_valid(), f"Form errors: {form2.errors}")

    def test_valid_form_without_name(self):
        """Test that form validates without name (not required)."""
        # Get the first available gameline and loc_type
        form = LocationCreationForm(user=self.st_user)
        first_gameline = form.fields["gameline"].choices[0][0]
        first_loc_type = form.fields["loc_type"].choices[0][0]

        form_data = {
            "gameline": first_gameline,
            "loc_type": first_loc_type,
            "rank": 2,
        }

        form2 = LocationCreationForm(data=form_data, user=self.st_user)

        self.assertTrue(form2.is_valid(), f"Form errors: {form2.errors}")

    def test_invalid_rank_too_high(self):
        """Test that rank > 5 is invalid."""
        # Get the first available gameline and loc_type
        form = LocationCreationForm(user=self.st_user)
        first_gameline = form.fields["gameline"].choices[0][0]
        first_loc_type = form.fields["loc_type"].choices[0][0]

        form_data = {
            "gameline": first_gameline,
            "loc_type": first_loc_type,
            "rank": 6,
        }

        form2 = LocationCreationForm(data=form_data, user=self.st_user)

        self.assertFalse(form2.is_valid())
        self.assertIn("rank", form2.errors)

    def test_valid_rank_at_max(self):
        """Test that rank = 5 is valid."""
        # Get the first available gameline and loc_type
        form = LocationCreationForm(user=self.st_user)
        first_gameline = form.fields["gameline"].choices[0][0]
        first_loc_type = form.fields["loc_type"].choices[0][0]

        form_data = {
            "gameline": first_gameline,
            "loc_type": first_loc_type,
            "rank": 5,
        }

        form2 = LocationCreationForm(data=form_data, user=self.st_user)

        self.assertTrue(form2.is_valid(), f"Form errors: {form2.errors}")


class TestLocationCreationFormAnonymous(TestLocationCreationFormSetup):
    """Test LocationCreationForm behavior for anonymous users."""

    def test_anonymous_user_empty_choices(self):
        """Test that anonymous users get empty choices."""
        form = LocationCreationForm(user=None)

        self.assertEqual(len(form.fields["gameline"].choices), 0)
        self.assertEqual(len(form.fields["loc_type"].choices), 0)

    def test_no_user_empty_choices(self):
        """Test that form without user gets empty choices."""
        form = LocationCreationForm()

        self.assertEqual(len(form.fields["gameline"].choices), 0)
        self.assertEqual(len(form.fields["loc_type"].choices), 0)
