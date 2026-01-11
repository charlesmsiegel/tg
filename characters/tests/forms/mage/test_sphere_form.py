"""
Tests for the SphereForm with PointPoolWidget integration.
"""

from django.test import TestCase

from characters.forms.mage.sphere_form import SphereForm


class MockCharacter:
    """Mock character object for testing."""

    def __init__(self, arete=1):
        self.arete = arete


class TestSphereForm(TestCase):
    """Tests for SphereForm."""

    def test_valid_allocation_within_budget(self):
        """Test valid sphere allocation totaling 6 points."""
        data = {
            "correspondence": 2,
            "time": 1,
            "spirit": 1,
            "forces": 1,
            "matter": 1,
            "life": 0,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, arete=3)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_over_budget(self):
        """Test that allocations over 6 points are rejected."""
        data = {
            "correspondence": 2,
            "time": 2,
            "spirit": 2,
            "forces": 2,
            "matter": 0,
            "life": 0,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, arete=3)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("exceeds", form.errors["__all__"][0].lower())

    def test_invalid_under_budget(self):
        """Test that allocations under 6 points are rejected."""
        data = {
            "correspondence": 1,
            "time": 1,
            "spirit": 1,
            "forces": 0,
            "matter": 0,
            "life": 0,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, arete=3)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("exactly", form.errors["__all__"][0].lower())


class TestSphereFormDynamicMax(TestCase):
    """Tests for SphereForm with dynamic arete-based max."""

    def test_arete_1_caps_spheres_at_1(self):
        """Test that arete 1 limits spheres to 1."""
        data = {
            "correspondence": 1,
            "time": 1,
            "spirit": 1,
            "forces": 1,
            "matter": 1,
            "life": 1,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, arete=1)
        self.assertTrue(form.is_valid(), form.errors)

    def test_arete_1_rejects_sphere_above_1(self):
        """Test that arete 1 rejects spheres above 1."""
        data = {
            "correspondence": 2,  # Over arete limit
            "time": 1,
            "spirit": 1,
            "forces": 1,
            "matter": 1,
            "life": 0,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, arete=1)
        self.assertFalse(form.is_valid())
        self.assertIn("correspondence", form.errors)

    def test_arete_3_allows_spheres_up_to_3(self):
        """Test that arete 3 allows spheres up to 3."""
        data = {
            "correspondence": 3,
            "time": 3,
            "spirit": 0,
            "forces": 0,
            "matter": 0,
            "life": 0,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, arete=3)
        self.assertTrue(form.is_valid(), form.errors)

    def test_character_object_sets_max(self):
        """Test that passing a character object sets the max."""
        character = MockCharacter(arete=2)
        data = {
            "correspondence": 2,
            "time": 2,
            "spirit": 2,
            "forces": 0,
            "matter": 0,
            "life": 0,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, character=character)
        self.assertTrue(form.is_valid(), form.errors)

    def test_character_object_enforces_max(self):
        """Test that character arete is enforced as max."""
        character = MockCharacter(arete=2)
        data = {
            "correspondence": 3,  # Over arete=2 limit
            "time": 2,
            "spirit": 1,
            "forces": 0,
            "matter": 0,
            "life": 0,
            "entropy": 0,
            "mind": 0,
            "prime": 0,
        }
        form = SphereForm(data=data, character=character)
        self.assertFalse(form.is_valid())
        self.assertIn("correspondence", form.errors)


class TestSphereFormWidgets(TestCase):
    """Tests for SphereForm widget configuration."""

    def test_widgets_configured_with_pool_attributes(self):
        """Test that form fields have point pool widget attributes."""
        form = SphereForm(arete=3)

        # Check first field has pool config
        corr_widget = form.fields["correspondence"].widget
        self.assertTrue(hasattr(corr_widget, "pool_name"))
        self.assertEqual(corr_widget.pool_name, "spheres")

    def test_widget_max_reflects_arete(self):
        """Test that widget max attribute reflects arete."""
        form = SphereForm(arete=2)

        for field_name in form.pool_fields:
            widget = form.fields[field_name].widget
            self.assertEqual(widget.attrs.get("max"), 2)

    def test_default_max_when_no_arete_provided(self):
        """Test default max (5) when no arete provided."""
        form = SphereForm()

        corr_widget = form.fields["correspondence"].widget
        self.assertEqual(corr_widget.attrs.get("max"), 5)
