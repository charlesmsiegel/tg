"""
Tests for the AbilityForm with PointPoolWidget integration.
"""

from django.test import TestCase

from characters.forms.core.ability_form import AbilityForm, HumanAbilityForm


class TestAbilityForm(TestCase):
    """Tests for AbilityForm."""

    def test_valid_distribution_talents_primary(self):
        """Test valid distribution with talents as primary (11 points)."""
        data = {
            # Talents = 11 (primary)
            "alertness": 2,
            "athletics": 2,
            "brawl": 1,
            "empathy": 2,
            "expression": 1,
            "intimidation": 1,
            "streetwise": 1,
            "subterfuge": 1,
            # Skills = 7 (secondary)
            "crafts": 2,
            "drive": 1,
            "etiquette": 1,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,
            # Knowledges = 4 (tertiary)
            "academics": 1,
            "computer": 1,
            "investigation": 1,
            "medicine": 1,
            "science": 0,
        }
        form = AbilityForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_distribution_knowledges_primary(self):
        """Test valid distribution with knowledges as primary."""
        data = {
            # Talents = 4 (tertiary)
            "alertness": 1,
            "athletics": 1,
            "brawl": 0,
            "empathy": 1,
            "expression": 0,
            "intimidation": 1,
            "streetwise": 0,
            "subterfuge": 0,
            # Skills = 7 (secondary)
            "crafts": 2,
            "drive": 1,
            "etiquette": 1,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,
            # Knowledges = 11 (primary) - 5 abilities, need 11 points, max 3 each
            "academics": 3,
            "computer": 3,
            "investigation": 2,
            "medicine": 2,
            "science": 1,
        }
        form = AbilityForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_distribution_all_equal(self):
        """Test that equal distribution is rejected."""
        data = {
            # All categories approximately equal - invalid
            "alertness": 1,
            "athletics": 1,
            "brawl": 1,
            "empathy": 1,
            "expression": 1,
            "intimidation": 1,
            "streetwise": 1,
            "subterfuge": 0,  # Talents = 7
            "crafts": 2,
            "drive": 1,
            "etiquette": 1,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,  # Skills = 7
            "academics": 2,
            "computer": 2,
            "investigation": 1,
            "medicine": 1,
            "science": 1,  # Knowledges = 7
        }
        form = AbilityForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_invalid_over_max_ability(self):
        """Test that abilities over 3 are rejected at chargen."""
        data = {
            "alertness": 4,  # Over max
            "athletics": 1,
            "brawl": 1,
            "empathy": 1,
            "expression": 1,
            "intimidation": 1,
            "streetwise": 1,
            "subterfuge": 0,
            "crafts": 2,
            "drive": 1,
            "etiquette": 1,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,
            "academics": 1,
            "computer": 1,
            "investigation": 1,
            "medicine": 1,
            "science": 0,
        }
        form = AbilityForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("alertness", form.errors)

    def test_invalid_negative_ability(self):
        """Test that negative abilities are rejected."""
        data = {
            "alertness": -1,  # Negative
            "athletics": 3,
            "brawl": 3,
            "empathy": 3,
            "expression": 2,
            "intimidation": 1,
            "streetwise": 0,
            "subterfuge": 0,
            "crafts": 2,
            "drive": 1,
            "etiquette": 1,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,
            "academics": 1,
            "computer": 1,
            "investigation": 1,
            "medicine": 1,
            "science": 0,
        }
        form = AbilityForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("alertness", form.errors)


class TestAbilityFormWithTargets(TestCase):
    """Tests for AbilityForm.with_targets() factory."""

    def test_custom_targets(self):
        """Test form with custom primary/secondary/tertiary values."""
        # Create form with 13/9/5 distribution
        FormClass = AbilityForm.with_targets(primary=13, secondary=9, tertiary=5)

        data = {
            # Talents = 13 (primary)
            "alertness": 2,
            "athletics": 2,
            "brawl": 2,
            "empathy": 2,
            "expression": 2,
            "intimidation": 1,
            "streetwise": 1,
            "subterfuge": 1,
            # Skills = 9 (secondary)
            "crafts": 2,
            "drive": 2,
            "etiquette": 2,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,
            # Knowledges = 5 (tertiary)
            "academics": 1,
            "computer": 1,
            "investigation": 1,
            "medicine": 1,
            "science": 1,
        }
        form = FormClass(data=data)
        self.assertTrue(form.is_valid(), form.errors)


class TestHumanAbilityForm(TestCase):
    """Tests for HumanAbilityForm."""

    def test_human_form_uses_standard_targets(self):
        """Test that HumanAbilityForm uses 11/7/4 targets."""
        self.assertEqual(sorted(HumanAbilityForm.distribution_targets), [4, 7, 11])


class TestAbilityFormWidgets(TestCase):
    """Tests for AbilityForm widget configuration."""

    def test_widgets_configured_with_pool_attributes(self):
        """Test that form fields have point pool widget attributes."""
        form = AbilityForm()

        # Check first field has pool config
        alertness_widget = form.fields["alertness"].widget
        self.assertTrue(hasattr(alertness_widget, "pool_name"))
        self.assertEqual(alertness_widget.pool_name, "abilities")

    def test_talent_fields_in_talents_group(self):
        """Test talent abilities are assigned to talents group."""
        form = AbilityForm()

        for field_name in ["alertness", "athletics", "brawl", "empathy"]:
            widget = form.fields[field_name].widget
            self.assertEqual(widget.pool_group, "talents")

    def test_skill_fields_in_skills_group(self):
        """Test skill abilities are assigned to skills group."""
        form = AbilityForm()

        for field_name in ["crafts", "drive", "etiquette", "firearms"]:
            widget = form.fields[field_name].widget
            self.assertEqual(widget.pool_group, "skills")

    def test_knowledge_fields_in_knowledges_group(self):
        """Test knowledge abilities are assigned to knowledges group."""
        form = AbilityForm()

        for field_name in ["academics", "computer", "investigation", "medicine"]:
            widget = form.fields[field_name].widget
            self.assertEqual(widget.pool_group, "knowledges")
