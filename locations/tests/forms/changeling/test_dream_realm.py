"""Tests for DreamRealm form."""

from django.test import TestCase

from locations.forms.changeling import DreamRealmForm
from locations.models.changeling import DreamRealm


class DreamRealmFormTest(TestCase):
    """Tests for the DreamRealmForm."""

    def test_form_has_correct_model(self):
        """Test that form uses the DreamRealm model."""
        form = DreamRealmForm()
        self.assertEqual(form.Meta.model, DreamRealm)

    def test_form_has_required_fields(self):
        """Test that form includes the expected fields."""
        form = DreamRealmForm()
        expected_fields = [
            "name",
            "description",
            "depth",
            "realm_type",
            "stability",
            "accessibility",
            "appearance",
            "laws_of_reality",
            "inhabitants",
            "ruler",
            "emotional_tone",
            "entry_requirements",
            "exit_difficulty",
            "mundane_connection",
            "glamour_level",
            "provides_glamour",
            "treasures",
            "time_flow",
            "is_mutable",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_form_valid_with_minimal_data(self):
        """Test that form validates with minimal required data."""
        data = {
            "name": "Test Realm",
            "depth": "near",
            "realm_type": "collective",
            "stability": 3,
            "accessibility": 3,
            "exit_difficulty": 3,
            "glamour_level": 3,
            "provides_glamour": True,
            "time_flow": "normal",
            "is_mutable": True,
        }
        form = DreamRealmForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valid_with_full_data(self):
        """Test that form validates with full data."""
        data = {
            "name": "The Crystal Gardens",
            "description": "A realm of living crystal formations",
            "depth": "far",
            "realm_type": "mythic",
            "stability": 4,
            "accessibility": 2,
            "appearance": "Towering crystal spires under a purple sky",
            "laws_of_reality": "Gravity pulls toward the largest crystal",
            "inhabitants": "Crystal chimera and light elementals",
            "ruler": "The Crystal Queen",
            "emotional_tone": "serene yet alien",
            "entry_requirements": "Hold a crystal focus while dreaming",
            "exit_difficulty": 5,
            "mundane_connection": "Crystal caves in the mundane world",
            "glamour_level": 7,
            "provides_glamour": True,
            "treasures": "Living crystal implements",
            "time_flow": "slower",
            "is_mutable": False,
        }
        form = DreamRealmForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_saves_correctly(self):
        """Test that form saves a DreamRealm correctly."""
        data = {
            "name": "Nightmare Hollow",
            "depth": "deep",
            "realm_type": "nightmare",
            "stability": 2,
            "accessibility": 1,
            "exit_difficulty": 8,
            "glamour_level": 5,
            "provides_glamour": False,
            "time_flow": "variable",
            "is_mutable": True,
        }
        form = DreamRealmForm(data=data)
        self.assertTrue(form.is_valid())
        realm = form.save()
        self.assertEqual(realm.name, "Nightmare Hollow")
        self.assertEqual(realm.depth, "deep")
        self.assertEqual(realm.realm_type, "nightmare")
        self.assertFalse(realm.provides_glamour)

    def test_form_invalid_stability_above_max(self):
        """Test that form rejects stability above 5."""
        data = {
            "name": "Invalid Realm",
            "depth": "near",
            "realm_type": "collective",
            "stability": 6,  # Invalid - max is 5
            "accessibility": 3,
            "exit_difficulty": 3,
            "glamour_level": 3,
            "provides_glamour": True,
            "time_flow": "normal",
            "is_mutable": True,
        }
        form = DreamRealmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("stability", form.errors)

    def test_form_invalid_accessibility_above_max(self):
        """Test that form rejects accessibility above 5."""
        data = {
            "name": "Invalid Realm",
            "depth": "near",
            "realm_type": "collective",
            "stability": 3,
            "accessibility": 6,  # Invalid - max is 5
            "exit_difficulty": 3,
            "glamour_level": 3,
            "provides_glamour": True,
            "time_flow": "normal",
            "is_mutable": True,
        }
        form = DreamRealmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("accessibility", form.errors)

    def test_form_invalid_exit_difficulty_above_max(self):
        """Test that form rejects exit difficulty above 10."""
        data = {
            "name": "Invalid Realm",
            "depth": "near",
            "realm_type": "collective",
            "stability": 3,
            "accessibility": 3,
            "exit_difficulty": 11,  # Invalid - max is 10
            "glamour_level": 3,
            "provides_glamour": True,
            "time_flow": "normal",
            "is_mutable": True,
        }
        form = DreamRealmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("exit_difficulty", form.errors)

    def test_form_invalid_glamour_level_above_max(self):
        """Test that form rejects glamour level above 10."""
        data = {
            "name": "Invalid Realm",
            "depth": "near",
            "realm_type": "collective",
            "stability": 3,
            "accessibility": 3,
            "exit_difficulty": 3,
            "glamour_level": 11,  # Invalid - max is 10
            "provides_glamour": True,
            "time_flow": "normal",
            "is_mutable": True,
        }
        form = DreamRealmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("glamour_level", form.errors)
