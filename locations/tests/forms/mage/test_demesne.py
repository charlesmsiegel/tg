"""
Tests for Demesne forms.

Tests cover:
- DemesneForm: Creating and editing demesnes with reality zones
- RealityZonePracticeRatingFormSet: Managing reality zone practice ratings
- Validation logic for reality zone ratings summing to 0
- Positive ratings summing to demesne rank
"""

from django.test import TestCase

from characters.models.mage.focus import Practice
from characters.tests.utils import mage_setup
from locations.forms.mage.demesne import DemesneForm
from locations.models.mage.demesne import Demesne
from locations.models.mage.reality_zone import RealityZone, ZoneRating


class TestDemesneFormSetup(TestCase):
    """Shared setup for DemesneForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for DemesneForm tests."""
        mage_setup()
        cls.practice1 = Practice.objects.first()
        cls.practice2 = Practice.objects.exclude(pk=cls.practice1.pk).first()


class TestDemesneFormBasics(TestDemesneFormSetup):
    """Test basic DemesneForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = DemesneForm()

        self.assertIn("name", form.fields)
        self.assertIn("contained_within", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("rank", form.fields)
        self.assertIn("size", form.fields)
        self.assertIn("accessibility", form.fields)

    def test_name_widget_has_placeholder(self):
        """Test that name field has placeholder text."""
        form = DemesneForm()

        self.assertIn("placeholder", form.fields["name"].widget.attrs)

    def test_description_widget_has_placeholder(self):
        """Test that description field has placeholder text."""
        form = DemesneForm()

        self.assertIn("placeholder", form.fields["description"].widget.attrs)

    def test_size_widget_has_placeholder(self):
        """Test that size field has placeholder text."""
        form = DemesneForm()

        self.assertIn("placeholder", form.fields["size"].widget.attrs)

    def test_contained_within_not_required(self):
        """Test that contained_within field is not required."""
        form = DemesneForm()

        self.assertFalse(form.fields["contained_within"].required)

    def test_form_has_reality_zone_formset(self):
        """Test that form has embedded reality zone formset."""
        form = DemesneForm()

        self.assertIsNotNone(form.reality_zone_formset)

    def test_new_demesne_gets_new_reality_zone(self):
        """Test that new demesne creates a new RealityZone."""
        form = DemesneForm()

        # reality_zone should be an unsaved RealityZone instance
        self.assertIsInstance(form.reality_zone, RealityZone)
        self.assertIsNone(form.reality_zone.pk)

    def test_existing_demesne_uses_existing_reality_zone(self):
        """Test that existing demesne uses its reality zone."""
        reality_zone = RealityZone.objects.create(name="Test Zone")
        demesne = Demesne.objects.create(name="Test Demesne", rank=2, reality_zone=reality_zone)

        form = DemesneForm(instance=demesne)

        self.assertEqual(form.reality_zone.pk, reality_zone.pk)


class TestDemesneFormValidation(TestDemesneFormSetup):
    """Test DemesneForm validation logic."""

    def test_valid_form_with_balanced_reality_zone(self):
        """Test that form is valid with balanced reality zone ratings."""
        form_data = {
            "name": "Test Demesne",
            "description": "A test demesne",
            "rank": 2,
            "size": "Small chamber",
            "accessibility": "moderate",
            # Formset data - ratings sum to 0, positive ratings sum to rank
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "2",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "-2",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_invalid_without_rank(self):
        """Test that form is invalid without rank."""
        form_data = {
            "name": "Test Demesne",
            "description": "A test demesne",
            "size": "Small chamber",
            "accessibility": "moderate",
            "reality_zone-TOTAL_FORMS": "0",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
        }

        form = DemesneForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_reality_zone_ratings_not_zero_sum(self):
        """Test that form is invalid when reality zone ratings don't sum to 0."""
        form_data = {
            "name": "Test Demesne",
            "description": "A test demesne",
            "rank": 2,
            "size": "Small chamber",
            "accessibility": "moderate",
            # Ratings don't sum to 0 (total = 3)
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "2",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "1",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_positive_ratings_not_equal_to_rank(self):
        """Test that form is invalid when positive ratings don't sum to rank."""
        form_data = {
            "name": "Test Demesne",
            "description": "A test demesne",
            "rank": 3,  # Rank is 3
            "size": "Small chamber",
            "accessibility": "moderate",
            # Positive ratings sum to 2 (not 3), total sums to 0
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "2",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "-2",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data)

        self.assertFalse(form.is_valid())


class TestDemesneFormIsValid(TestDemesneFormSetup):
    """Test DemesneForm.is_valid() method."""

    def test_is_valid_checks_formset(self):
        """Test that is_valid checks the reality zone formset validity."""
        form_data = {
            "name": "Test Demesne",
            "description": "A test demesne",
            "rank": 2,
            "size": "Small chamber",
            "accessibility": "moderate",
            # Invalid formset - missing TOTAL_FORMS will cause formset to be invalid
            "reality_zone-TOTAL_FORMS": "invalid",
            "reality_zone-INITIAL_FORMS": "0",
        }

        form = DemesneForm(data=form_data)

        self.assertFalse(form.is_valid())


class TestDemesneFormSave(TestDemesneFormSetup):
    """Test DemesneForm save logic."""

    def test_save_creates_demesne(self):
        """Test that saving creates a new Demesne."""
        initial_count = Demesne.objects.count()

        form_data = {
            "name": "New Demesne",
            "description": "A new demesne",
            "rank": 2,
            "size": "Expansive realm",
            "accessibility": "difficult",
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "2",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "-2",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        demesne = form.save()

        self.assertEqual(Demesne.objects.count(), initial_count + 1)
        self.assertEqual(demesne.name, "New Demesne")
        self.assertEqual(demesne.rank, 2)

    def test_save_creates_reality_zone(self):
        """Test that saving creates a RealityZone for the demesne."""
        form_data = {
            "name": "New Demesne",
            "description": "A new demesne",
            "rank": 2,
            "size": "Small chamber",
            "accessibility": "moderate",
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "2",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "-2",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        demesne = form.save()

        self.assertIsNotNone(demesne.reality_zone)
        self.assertEqual(demesne.reality_zone.name, "New Demesne")

    def test_save_creates_zone_ratings(self):
        """Test that saving creates ZoneRatings for the demesne's reality zone."""
        form_data = {
            "name": "New Demesne",
            "description": "A new demesne",
            "rank": 2,
            "size": "Small chamber",
            "accessibility": "moderate",
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "2",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "-2",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        demesne = form.save()

        zone_ratings = ZoneRating.objects.filter(zone=demesne.reality_zone)
        self.assertEqual(zone_ratings.count(), 2)

    def test_save_without_commit(self):
        """Test that save with commit=False doesn't save to database."""
        initial_demesne_count = Demesne.objects.count()
        initial_rz_count = RealityZone.objects.count()

        form_data = {
            "name": "Unsaved Demesne",
            "description": "A test demesne",
            "rank": 1,
            "size": "Small",
            "accessibility": "easy",
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "1",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "-1",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        demesne = form.save(commit=False)

        # Object created but not saved
        self.assertIsNotNone(demesne)
        self.assertEqual(Demesne.objects.count(), initial_demesne_count)
        self.assertEqual(RealityZone.objects.count(), initial_rz_count)


class TestDemesneFormEditing(TestDemesneFormSetup):
    """Test DemesneForm editing existing demesnes."""

    def test_edit_existing_demesne(self):
        """Test editing an existing demesne."""
        reality_zone = RealityZone.objects.create(name="Original Zone")
        demesne = Demesne.objects.create(
            name="Original Demesne",
            description="Original description",
            rank=2,
            reality_zone=reality_zone,
        )

        form_data = {
            "name": "Updated Demesne",
            "description": "Updated description",
            "rank": 3,
            "size": "Large",
            "accessibility": "difficult",
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": "3",
            "reality_zone-0-DELETE": "",
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": "-3",
            "reality_zone-1-DELETE": "",
        }

        form = DemesneForm(data=form_data, instance=demesne)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        updated_demesne = form.save()

        self.assertEqual(updated_demesne.name, "Updated Demesne")
        self.assertEqual(updated_demesne.rank, 3)
        self.assertEqual(updated_demesne.pk, demesne.pk)


class TestDemesneFormAccessibility(TestDemesneFormSetup):
    """Test accessibility field in DemesneForm."""

    def test_valid_accessibility_choices(self):
        """Test that all accessibility choices are valid."""
        valid_choices = ["easy", "moderate", "difficult", "private"]

        for choice in valid_choices:
            form_data = {
                "name": "Test Demesne",
                "description": "A test demesne",
                "rank": 1,
                "size": "Small",
                "accessibility": choice,
                "reality_zone-TOTAL_FORMS": "2",
                "reality_zone-INITIAL_FORMS": "0",
                "reality_zone-MIN_NUM_FORMS": "0",
                "reality_zone-MAX_NUM_FORMS": "1000",
                "reality_zone-0-practice": str(self.practice1.pk),
                "reality_zone-0-rating": "1",
                "reality_zone-0-DELETE": "",
                "reality_zone-1-practice": str(self.practice2.pk),
                "reality_zone-1-rating": "-1",
                "reality_zone-1-DELETE": "",
            }

            form = DemesneForm(data=form_data)
            self.assertTrue(form.is_valid(), f"Form should be valid for accessibility '{choice}'")
