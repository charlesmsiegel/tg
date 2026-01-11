"""Tests for Trod form."""

from django.test import TestCase

from locations.forms.changeling import TrodForm
from locations.models.changeling import Trod


class TrodFormTest(TestCase):
    """Tests for the TrodForm."""

    def test_form_has_correct_model(self):
        """Test that form uses the Trod model."""
        form = TrodForm()
        self.assertEqual(form.Meta.model, Trod)

    def test_form_has_required_fields(self):
        """Test that form includes the expected fields."""
        form = TrodForm()
        expected_fields = [
            "name",
            "description",
            "trod_type",
            "origin_name",
            "origin_description",
            "destination_name",
            "destination_description",
            "strength",
            "difficulty",
            "access_requirements",
            "guardians",
            "travel_duration",
            "is_two_way",
            "is_stable",
            "glamour_cost",
            "accessibility_notes",
            "journey_description",
            "known_to",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_form_valid_with_minimal_data(self):
        """Test that form validates with minimal required data."""
        data = {
            "name": "Test Trod",
            "trod_type": "silver_path",
            "strength": 1,
            "difficulty": 5,
            "is_two_way": True,
            "is_stable": True,
            "glamour_cost": 0,
        }
        form = TrodForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valid_with_full_data(self):
        """Test that form validates with full data."""
        data = {
            "name": "The Moonlit Path",
            "description": "A shimmering path that appears under full moons",
            "trod_type": "moonpath",
            "origin_name": "The Old Oak",
            "origin_description": "An ancient oak in the city park",
            "destination_name": "The Silver Glade",
            "destination_description": "A clearing in the Near Dreaming",
            "strength": 3,
            "difficulty": 4,
            "access_requirements": "Must walk counterclockwise around the oak",
            "guardians": "A pair of chimerical wolves",
            "travel_duration": "5 minutes",
            "is_two_way": True,
            "is_stable": False,
            "glamour_cost": 1,
            "accessibility_notes": "Only during full moon nights",
            "journey_description": "Silver light surrounds travelers",
            "known_to": "Local Seelie court members",
        }
        form = TrodForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_saves_correctly(self):
        """Test that form saves a Trod correctly."""
        data = {
            "name": "Test Path",
            "trod_type": "rath",
            "strength": 4,
            "difficulty": 3,
            "is_two_way": False,
            "is_stable": True,
            "glamour_cost": 2,
        }
        form = TrodForm(data=data)
        self.assertTrue(form.is_valid())
        trod = form.save()
        self.assertEqual(trod.name, "Test Path")
        self.assertEqual(trod.trod_type, "rath")
        self.assertFalse(trod.is_two_way)
        self.assertEqual(trod.glamour_cost, 2)

    def test_form_invalid_strength_above_max(self):
        """Test that form rejects strength above 5."""
        data = {
            "name": "Invalid Trod",
            "trod_type": "silver_path",
            "strength": 6,  # Invalid - max is 5
            "difficulty": 5,
            "is_two_way": True,
            "is_stable": True,
            "glamour_cost": 0,
        }
        form = TrodForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("strength", form.errors)

    def test_form_invalid_difficulty_above_max(self):
        """Test that form rejects difficulty above 10."""
        data = {
            "name": "Invalid Trod",
            "trod_type": "silver_path",
            "strength": 1,
            "difficulty": 11,  # Invalid - max is 10
            "is_two_way": True,
            "is_stable": True,
            "glamour_cost": 0,
        }
        form = TrodForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("difficulty", form.errors)

    def test_form_invalid_glamour_cost_above_max(self):
        """Test that form rejects glamour cost above 10."""
        data = {
            "name": "Invalid Trod",
            "trod_type": "silver_path",
            "strength": 1,
            "difficulty": 5,
            "is_two_way": True,
            "is_stable": True,
            "glamour_cost": 11,  # Invalid - max is 10
        }
        form = TrodForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("glamour_cost", form.errors)
