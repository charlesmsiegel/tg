"""Tests for Holding form."""

from django.test import TestCase

from locations.forms.changeling import HoldingForm
from locations.models.changeling import Holding


class HoldingFormTest(TestCase):
    """Tests for the HoldingForm."""

    def test_form_has_correct_model(self):
        """Test that form uses the Holding model."""
        form = HoldingForm()
        self.assertEqual(form.Meta.model, Holding)

    def test_form_has_required_fields(self):
        """Test that form includes the expected fields."""
        form = HoldingForm()
        expected_fields = [
            "name",
            "description",
            "rank",
            "court",
            "ruler_name",
            "ruler_title",
            "territory_description",
            "mundane_location",
            "vassals",
            "liege",
            "freehold_count",
            "major_freeholds",
            "population",
            "military_strength",
            "wealth",
            "stability",
            "political_situation",
            "notable_laws",
            "rival_holdings",
            "history",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_form_valid_with_minimal_data(self):
        """Test that form validates with minimal required data."""
        data = {
            "name": "Test Holding",
            "rank": "barony",
            "court": "seelie",
            "military_strength": 1,
            "wealth": 1,
            "stability": 3,
            "freehold_count": 0,
        }
        form = HoldingForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valid_with_full_data(self):
        """Test that form validates with full data."""
        data = {
            "name": "The Silver Duchy",
            "description": "A beautiful duchy in the mountains",
            "rank": "duchy",
            "court": "seelie",
            "ruler_name": "Duke Silvanus",
            "ruler_title": "Duke of the Silver Peaks",
            "territory_description": "The mountain region",
            "mundane_location": "Rocky Mountains, Colorado",
            "vassals": "Baron Ironwood, Baroness Starlight",
            "liege": "King Oberon",
            "freehold_count": 5,
            "major_freeholds": "The Silver Court, The Mountain Lodge",
            "population": "large",
            "military_strength": 4,
            "wealth": 3,
            "stability": 4,
            "political_situation": "Peaceful but watchful",
            "notable_laws": "No cold iron within borders",
            "rival_holdings": "The Unseelie Barony to the south",
            "history": "Founded in 1452 during the Great Migration",
        }
        form = HoldingForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_saves_correctly(self):
        """Test that form saves a Holding correctly."""
        data = {
            "name": "Test Barony",
            "rank": "barony",
            "court": "unseelie",
            "military_strength": 2,
            "wealth": 1,
            "stability": 2,
            "freehold_count": 1,
        }
        form = HoldingForm(data=data)
        self.assertTrue(form.is_valid())
        holding = form.save()
        self.assertEqual(holding.name, "Test Barony")
        self.assertEqual(holding.rank, "barony")
        self.assertEqual(holding.court, "unseelie")

    def test_form_invalid_military_strength_above_max(self):
        """Test that form rejects military strength above 5."""
        data = {
            "name": "Invalid Holding",
            "rank": "barony",
            "court": "seelie",
            "military_strength": 6,  # Invalid - max is 5
            "wealth": 1,
            "stability": 3,
            "freehold_count": 0,
        }
        form = HoldingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("military_strength", form.errors)

    def test_form_invalid_wealth_above_max(self):
        """Test that form rejects wealth above 5."""
        data = {
            "name": "Invalid Holding",
            "rank": "barony",
            "court": "seelie",
            "military_strength": 1,
            "wealth": 6,  # Invalid - max is 5
            "stability": 3,
            "freehold_count": 0,
        }
        form = HoldingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("wealth", form.errors)

    def test_form_invalid_stability_above_max(self):
        """Test that form rejects stability above 5."""
        data = {
            "name": "Invalid Holding",
            "rank": "barony",
            "court": "seelie",
            "military_strength": 1,
            "wealth": 1,
            "stability": 6,  # Invalid - max is 5
            "freehold_count": 0,
        }
        form = HoldingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("stability", form.errors)
