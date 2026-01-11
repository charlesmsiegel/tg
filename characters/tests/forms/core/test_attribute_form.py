"""
Tests for the AttributeForm with PointPoolWidget integration.
"""

from django.test import TestCase

from characters.forms.core.attribute_form import AttributeForm, HumanAttributeForm


class TestAttributeForm(TestCase):
    """Tests for AttributeForm."""

    def test_valid_distribution_physical_primary(self):
        """Test valid distribution with physical as primary."""
        data = {
            # Physical = 10 (primary: 3 + 7)
            "strength": 4,
            "dexterity": 3,
            "stamina": 3,
            # Social = 8 (secondary: 3 + 5)
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            # Mental = 6 (tertiary: 3 + 3)
            "perception": 2,
            "intelligence": 2,
            "wits": 2,
        }
        form = AttributeForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_distribution_mental_primary(self):
        """Test valid distribution with mental as primary."""
        data = {
            # Physical = 6 (tertiary)
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            # Social = 8 (secondary)
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            # Mental = 10 (primary)
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
        }
        form = AttributeForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_distribution_social_primary(self):
        """Test valid distribution with social as primary."""
        data = {
            # Physical = 8 (secondary)
            "strength": 3,
            "dexterity": 3,
            "stamina": 2,
            # Social = 10 (primary)
            "charisma": 4,
            "manipulation": 3,
            "appearance": 3,
            # Mental = 6 (tertiary)
            "perception": 2,
            "intelligence": 2,
            "wits": 2,
        }
        form = AttributeForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_distribution_all_equal(self):
        """Test that equal distribution is rejected."""
        data = {
            # All categories = 8
            "strength": 3,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            "perception": 3,
            "intelligence": 3,
            "wits": 2,
        }
        form = AttributeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("distribution", form.errors["__all__"][0].lower())

    def test_invalid_over_max_attribute(self):
        """Test that attributes over 5 are rejected."""
        data = {
            "strength": 6,  # Over max
            "dexterity": 2,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            "perception": 2,
            "intelligence": 2,
            "wits": 2,
        }
        form = AttributeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("strength", form.errors)

    def test_invalid_under_min_attribute(self):
        """Test that attributes under 1 are rejected."""
        data = {
            "strength": 0,  # Under min
            "dexterity": 5,
            "stamina": 5,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            "perception": 2,
            "intelligence": 2,
            "wits": 2,
        }
        form = AttributeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("strength", form.errors)


class TestAttributeFormWithTargets(TestCase):
    """Tests for AttributeForm.with_targets() factory."""

    def test_custom_targets(self):
        """Test form with custom primary/secondary/tertiary values."""
        # Create form with 9/6/3 distribution
        FormClass = AttributeForm.with_targets(primary=9, secondary=6, tertiary=3)

        # Valid distribution: 12/9/6 (base 3 + 9/6/3)
        data = {
            # Physical = 12 (primary: 3 + 9)
            "strength": 5,
            "dexterity": 4,
            "stamina": 3,
            # Social = 9 (secondary: 3 + 6)
            "charisma": 3,
            "manipulation": 3,
            "appearance": 3,
            # Mental = 6 (tertiary: 3 + 3)
            "perception": 2,
            "intelligence": 2,
            "wits": 2,
        }
        form = FormClass(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_targets_sorted_correctly(self):
        """Test that targets are always sorted for comparison."""
        # Pass targets in any order
        FormClass = AttributeForm.with_targets(primary=3, secondary=7, tertiary=5)

        # Expected targets: [6, 8, 10] (base 3 + [3, 5, 7])
        self.assertEqual(sorted(FormClass.distribution_targets), [6, 8, 10])


class TestHumanAttributeForm(TestCase):
    """Tests for HumanAttributeForm."""

    def test_human_form_uses_standard_targets(self):
        """Test that HumanAttributeForm uses 7/5/3 targets."""
        self.assertEqual(sorted(HumanAttributeForm.distribution_targets), [6, 8, 10])

    def test_human_form_validation(self):
        """Test HumanAttributeForm validation."""
        data = {
            "strength": 4,
            "dexterity": 3,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            "perception": 2,
            "intelligence": 2,
            "wits": 2,
        }
        form = HumanAttributeForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)


class TestAttributeFormWidgets(TestCase):
    """Tests for AttributeForm widget configuration."""

    def test_widgets_configured_with_pool_attributes(self):
        """Test that form fields have point pool widget attributes."""
        form = AttributeForm()

        # Check first field has pool config
        strength_widget = form.fields["strength"].widget
        self.assertTrue(hasattr(strength_widget, "pool_name"))
        self.assertEqual(strength_widget.pool_name, "attributes")

    def test_physical_fields_in_physical_group(self):
        """Test physical attributes are assigned to physical group."""
        form = AttributeForm()

        for field_name in ["strength", "dexterity", "stamina"]:
            widget = form.fields[field_name].widget
            self.assertEqual(widget.pool_group, "physical")

    def test_social_fields_in_social_group(self):
        """Test social attributes are assigned to social group."""
        form = AttributeForm()

        for field_name in ["charisma", "manipulation", "appearance"]:
            widget = form.fields[field_name].widget
            self.assertEqual(widget.pool_group, "social")

    def test_mental_fields_in_mental_group(self):
        """Test mental attributes are assigned to mental group."""
        form = AttributeForm()

        for field_name in ["perception", "intelligence", "wits"]:
            widget = form.fields[field_name].widget
            self.assertEqual(widget.pool_group, "mental")
