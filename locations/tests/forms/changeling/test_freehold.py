"""
Tests for Freehold forms.

Tests cover:
- FreeholdForm: Creating and editing freeholds
- Archetype-specific validation (Academy, Hearth)
- Powers validation (Dual Nature)
- Feature point calculation
- Holdings requirement calculation
"""

from characters.tests.utils import changeling_setup
from django.test import TestCase
from locations.forms.changeling.freehold import FreeholdForm
from locations.models.changeling.freehold import Freehold


class TestFreeholdFormSetup(TestCase):
    """Shared setup for FreeholdForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for FreeholdForm tests."""
        changeling_setup()


class TestFreeholdFormBasics(TestFreeholdFormSetup):
    """Test basic FreeholdForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = FreeholdForm()

        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("archetype", form.fields)
        self.assertIn("aspect", form.fields)
        self.assertIn("quirks", form.fields)
        self.assertIn("balefire", form.fields)
        self.assertIn("size", form.fields)
        self.assertIn("sanctuary", form.fields)
        self.assertIn("resources", form.fields)
        self.assertIn("passages", form.fields)
        self.assertIn("powers", form.fields)

    def test_name_widget_has_placeholder(self):
        """Test that name field has placeholder text."""
        form = FreeholdForm()

        self.assertIn("placeholder", form.fields["name"].widget.attrs)

    def test_description_widget_is_textarea(self):
        """Test that description field is a textarea."""
        form = FreeholdForm()

        self.assertEqual(form.fields["description"].widget.attrs.get("rows"), 4)

    def test_contained_within_not_required(self):
        """Test that contained_within field is not required."""
        form = FreeholdForm()

        self.assertFalse(form.fields["contained_within"].required)

    def test_owned_by_not_required(self):
        """Test that owned_by field is not required."""
        form = FreeholdForm()

        self.assertFalse(form.fields["owned_by"].required)

    def test_balefire_help_text(self):
        """Test that balefire field has help text."""
        form = FreeholdForm()

        self.assertIn("0-5", form.fields["balefire"].help_text)

    def test_powers_widget_is_checkbox_select_multiple(self):
        """Test that powers field uses CheckboxSelectMultiple widget."""
        form = FreeholdForm()

        from django.forms import CheckboxSelectMultiple

        self.assertIsInstance(form.fields["powers"].widget, CheckboxSelectMultiple)


class TestFreeholdFormValidation(TestFreeholdFormSetup):
    """Test FreeholdForm validation logic."""

    def test_valid_basic_form(self):
        """Test that form is valid with basic data."""
        form_data = {
            "name": "Test Freehold",
            "description": "A test freehold",
            "archetype": "homestead",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_academy_requires_ability(self):
        """Test that Academy archetype requires academy_ability."""
        form_data = {
            "name": "Academy Freehold",
            "description": "A test academy",
            "archetype": "academy",
            "academy_ability": "",  # Missing required ability
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_academy_valid_with_ability(self):
        """Test that Academy archetype is valid with ability."""
        form_data = {
            "name": "Academy Freehold",
            "description": "A test academy",
            "archetype": "academy",
            "academy_ability": "Melee",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_hearth_requires_ability(self):
        """Test that Hearth archetype requires hearth_ability."""
        form_data = {
            "name": "Hearth Freehold",
            "description": "A test hearth",
            "archetype": "hearth",
            "hearth_ability": "",  # Missing required ability
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_hearth_valid_with_ability(self):
        """Test that Hearth archetype is valid with ability choice."""
        form_data = {
            "name": "Hearth Freehold",
            "description": "A test hearth",
            "archetype": "hearth",
            "hearth_ability": "leadership",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_dual_nature_requires_second_archetype(self):
        """Test that Dual Nature power requires second archetype."""
        form_data = {
            "name": "Dual Freehold",
            "description": "A test dual nature",
            "archetype": "homestead",
            "dual_nature_archetype": "",  # Missing required second archetype
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "powers": ["dual_nature"],
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_dual_nature_academy_requires_ability(self):
        """Test that Dual Nature with Academy requires ability."""
        form_data = {
            "name": "Dual Freehold",
            "description": "A test dual nature",
            "archetype": "homestead",
            "dual_nature_archetype": "academy",
            "dual_nature_ability": "",  # Missing required ability
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "powers": ["dual_nature"],
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)

        self.assertFalse(form.is_valid())


class TestFreeholdFormFeaturePoints(TestFreeholdFormSetup):
    """Test feature point calculation in FreeholdForm."""

    def test_feature_points_calculated(self):
        """Test that feature points are calculated correctly."""
        form_data = {
            "name": "Test Freehold",
            "description": "A test freehold",
            "archetype": "homestead",
            "balefire": 2,  # 2 points
            "size": 2,  # 2 points
            "sanctuary": 1,  # 1 point
            "resources": 1,  # 1 point
            "passages": 1,  # 0 points (first is free)
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        form.is_valid()

        # Total: 2 + 2 + 1 + 1 = 6
        self.assertEqual(form.feature_points, 6)

    def test_passages_cost_after_first(self):
        """Test that passages after first cost 1 point each."""
        form_data = {
            "name": "Test Freehold",
            "description": "A test freehold",
            "archetype": "homestead",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 3,  # 2 extra passages = 2 points
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        form.is_valid()

        # Total: 1 + 1 + 0 + 0 + 2 = 4
        self.assertEqual(form.feature_points, 4)

    def test_power_costs(self):
        """Test that powers add correct point costs."""
        form_data = {
            "name": "Test Freehold",
            "description": "A test freehold",
            "archetype": "homestead",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "powers": ["warning_call", "glamour_to_dross"],  # 1 + 2 = 3 points
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        form.is_valid()

        # Total: 1 + 1 + 0 + 0 + 0 + 3 = 5
        self.assertEqual(form.feature_points, 5)

    def test_holdings_required_calculation(self):
        """Test that holdings required is calculated correctly."""
        form_data = {
            "name": "Test Freehold",
            "description": "A test freehold",
            "archetype": "homestead",
            "balefire": 3,  # 3 points
            "size": 3,  # 3 points
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        form.is_valid()

        # Total: 6 points. Holdings = (6 + 2) // 3 = 2 (round up from 2.67)
        self.assertEqual(form.holdings_required, 2)


class TestFreeholdFormSave(TestFreeholdFormSetup):
    """Test FreeholdForm save logic."""

    def test_save_creates_freehold(self):
        """Test that saving creates a new Freehold."""
        initial_count = Freehold.objects.count()

        form_data = {
            "name": "New Freehold",
            "description": "A new freehold",
            "archetype": "stronghold",
            "balefire": 2,
            "size": 2,
            "sanctuary": 1,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        freehold = form.save()

        self.assertEqual(Freehold.objects.count(), initial_count + 1)
        self.assertEqual(freehold.name, "New Freehold")
        self.assertEqual(freehold.archetype, "stronghold")

    def test_save_clears_non_applicable_fields(self):
        """Test that save clears archetype-specific fields that don't apply."""
        form_data = {
            "name": "Test Freehold",
            "description": "A test freehold",
            "archetype": "homestead",  # Not academy, not hearth
            "academy_ability": "Melee",  # Should be cleared
            "hearth_ability": "leadership",  # Should be cleared
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        freehold = form.save()

        self.assertEqual(freehold.academy_ability, "")
        self.assertEqual(freehold.hearth_ability, "")

    def test_save_preserves_academy_ability(self):
        """Test that save preserves academy_ability for academy archetype."""
        form_data = {
            "name": "Academy Freehold",
            "description": "A test academy",
            "archetype": "academy",
            "academy_ability": "Kenning",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        freehold = form.save()

        self.assertEqual(freehold.academy_ability, "Kenning")

    def test_save_clears_dual_nature_without_power(self):
        """Test that save clears dual nature fields without the power."""
        form_data = {
            "name": "Test Freehold",
            "description": "A test freehold",
            "archetype": "homestead",
            "dual_nature_archetype": "academy",  # Should be cleared
            "dual_nature_ability": "Melee",  # Should be cleared
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            # No powers - dual_nature cleared because not selected
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        freehold = form.save()

        self.assertEqual(freehold.dual_nature_archetype, "")
        self.assertEqual(freehold.dual_nature_ability, "")


class TestFreeholdFormArchetypes(TestFreeholdFormSetup):
    """Test all archetype choices in FreeholdForm."""

    def test_all_archetypes_valid(self):
        """Test that all archetype choices are valid."""
        archetypes = [
            "academy",
            "hearth",
            "homestead",
            "manor",
            "market",
            "repository",
            "stronghold",
            "thorpe",
            "workshop",
        ]

        for archetype in archetypes:
            form_data = {
                "name": f"{archetype.title()} Freehold",
                "description": "A test freehold",
                "archetype": archetype,
                "balefire": 1,
                "size": 1,
                "sanctuary": 0,
                "resources": 0,
                "passages": 1,
                "gauntlet": 7,
                "shroud": 7,
                "dimension_barrier": 6,
            }

            # Add required fields for special archetypes
            if archetype == "academy":
                form_data["academy_ability"] = "Melee"
            elif archetype == "hearth":
                form_data["hearth_ability"] = "leadership"

            form = FreeholdForm(data=form_data)
            self.assertTrue(
                form.is_valid(), f"Form should be valid for archetype '{archetype}': {form.errors}"
            )


class TestFreeholdFormEditing(TestFreeholdFormSetup):
    """Test FreeholdForm editing existing freeholds."""

    def test_edit_existing_freehold(self):
        """Test editing an existing freehold."""
        freehold = Freehold.objects.create(
            name="Original Freehold",
            description="Original description",
            archetype="homestead",
            balefire=1,
            size=1,
        )

        form_data = {
            "name": "Updated Freehold",
            "description": "Updated description",
            "archetype": "stronghold",
            "balefire": 2,
            "size": 2,
            "sanctuary": 1,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data, instance=freehold)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        updated_freehold = form.save()

        self.assertEqual(updated_freehold.name, "Updated Freehold")
        self.assertEqual(updated_freehold.archetype, "stronghold")
        self.assertEqual(updated_freehold.pk, freehold.pk)

    def test_edit_hides_irrelevant_fields_for_non_academy(self):
        """Test that editing non-academy hides academy_ability field."""
        freehold = Freehold.objects.create(
            name="Test Freehold",
            archetype="homestead",
            balefire=1,
            size=1,
        )

        form = FreeholdForm(instance=freehold)

        # For non-academy, academy_ability should be hidden
        from django.forms import HiddenInput

        self.assertIsInstance(form.fields["academy_ability"].widget, HiddenInput)


class TestFreeholdFormPowers(TestFreeholdFormSetup):
    """Test power selection in FreeholdForm."""

    def test_all_powers_valid(self):
        """Test that all power choices are valid."""
        powers = [
            "warning_call",
            "glamour_to_dross",
            "resonant_dreams",
            "call_forth_flame",
        ]

        for power in powers:
            form_data = {
                "name": "Powered Freehold",
                "description": "A test freehold with power",
                "archetype": "homestead",
                "balefire": 1,
                "size": 1,
                "sanctuary": 0,
                "resources": 0,
                "passages": 1,
                "powers": [power],
                "gauntlet": 7,
                "shroud": 7,
                "dimension_barrier": 6,
            }

            form = FreeholdForm(data=form_data)
            self.assertTrue(
                form.is_valid(), f"Form should be valid with power '{power}': {form.errors}"
            )

    def test_multiple_powers_valid(self):
        """Test that multiple powers can be selected."""
        form_data = {
            "name": "Multi-powered Freehold",
            "description": "A test freehold with multiple powers",
            "archetype": "homestead",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "powers": ["warning_call", "glamour_to_dross", "resonant_dreams"],
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = FreeholdForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        freehold = form.save()
        self.assertEqual(len(freehold.powers), 3)
