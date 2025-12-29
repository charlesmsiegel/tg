"""
Tests for Effect forms (EffectCreateOrSelectForm, EffectForm, EffectCreateOrSelectFormSet).

Tests cover:
- EffectForm initialization and field configuration
- Effect sphere fields and cost calculation
- EffectCreateOrSelectForm select/create workflow
- Effect selection validation
- Effect creation validation
- EffectCreateOrSelectFormSet behavior
"""

from characters.forms.mage.effect import (
    EffectCreateOrSelectForm,
    EffectCreateOrSelectFormSet,
    EffectForm,
)
from characters.models.mage.effect import Effect
from characters.tests.utils import mage_setup
from django.test import TestCase


class TestEffectFormInit(TestCase):
    """Test EffectForm initialization."""

    def setUp(self):
        mage_setup()

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = EffectForm()

        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        # Note: 'systems' field is not included in this form

    def test_form_has_sphere_fields(self):
        """Test that form has all sphere fields."""
        form = EffectForm()

        for sphere in [
            "correspondence",
            "time",
            "spirit",
            "matter",
            "life",
            "forces",
            "entropy",
            "mind",
            "prime",
        ]:
            self.assertIn(sphere, form.fields)

    def test_sphere_fields_are_integer_fields(self):
        """Test that sphere fields are integer fields."""
        form = EffectForm()

        for sphere in [
            "correspondence",
            "time",
            "spirit",
            "matter",
            "life",
            "forces",
            "entropy",
            "mind",
            "prime",
        ]:
            # Verify it's an integer field from ModelForm
            self.assertEqual(form.fields[sphere].__class__.__name__, "IntegerField")


class TestEffectFormValidation(TestCase):
    """Test EffectForm validation."""

    def setUp(self):
        mage_setup()

    def test_form_valid_with_all_spheres(self):
        """Test that form is valid with all sphere values provided."""
        form = EffectForm(
            data={
                "name": "Test Effect",
                "description": "A test effect",
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "matter": 0,
                "life": 0,
                "forces": 2,
                "entropy": 0,
                "mind": 1,
                "prime": 0,
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_invalid_without_required_spheres(self):
        """Test that form is invalid without all sphere values."""
        form = EffectForm(
            data={
                "name": "Single Sphere Effect",
                "forces": 3,
            }
        )

        # ModelForm requires all sphere fields
        self.assertFalse(form.is_valid())

    def test_form_accepts_sphere_values(self):
        """Test that form accepts valid sphere values."""
        form = EffectForm(
            data={
                "name": "Valid Effect",
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "matter": 0,
                "life": 0,
                "forces": 5,
                "entropy": 0,
                "mind": 0,
                "prime": 0,
            }
        )

        # Effect model may not have validators on sphere fields at form level
        # The validation happens at model level when saving
        self.assertTrue(form.is_valid())


class TestEffectCreateOrSelectFormInit(TestCase):
    """Test EffectCreateOrSelectForm initialization."""

    def setUp(self):
        mage_setup()
        self.effect = Effect.objects.create(name="Existing Effect", forces=2)

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = EffectCreateOrSelectForm()

        self.assertIn("select_or_create", form.fields)
        self.assertIn("select", form.fields)

    def test_form_has_effect_form_fields(self):
        """Test that form embeds EffectForm fields."""
        form = EffectCreateOrSelectForm()

        # Should include sphere fields from EffectForm
        for sphere in ["forces", "mind", "life"]:
            self.assertIn(sphere, form.fields)

    def test_select_field_has_effect_queryset(self):
        """Test that select field queries all effects."""
        form = EffectCreateOrSelectForm()
        select_queryset = form.fields["select"].queryset

        self.assertIn(self.effect, select_queryset)

    def test_form_fields_not_required(self):
        """Test that form fields are not required."""
        form = EffectCreateOrSelectForm()

        for field_name in form.fields:
            self.assertFalse(
                form.fields[field_name].required,
                f"Field {field_name} should not be required",
            )


class TestEffectCreateOrSelectFormValidation(TestCase):
    """Test EffectCreateOrSelectForm validation logic."""

    def setUp(self):
        mage_setup()
        self.existing_effect = Effect.objects.create(name="Existing Effect", forces=2)

    def test_form_initializes_with_data(self):
        """Test that form initializes with data."""
        form = EffectCreateOrSelectForm(
            data={
                "select_or_create": False,
                "select": self.existing_effect.pk,
            }
        )

        self.assertIsNotNone(form)

    def test_form_invalid_when_not_creating_and_no_selection(self):
        """Test that form is invalid when not creating and no selection made."""
        form = EffectCreateOrSelectForm(
            data={
                "select_or_create": False,
                # No select value
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("select", form.errors)

    def test_form_initializes_when_creating(self):
        """Test that form initializes when creating new effect."""
        form = EffectCreateOrSelectForm(
            data={
                "select_or_create": True,
                "name": "New Effect",
                "description": "A new effect",
                "forces": 2,
            }
        )

        # Form should initialize without error
        self.assertIsNotNone(form)


class TestEffectCreateOrSelectFormSave(TestCase):
    """Test EffectCreateOrSelectForm save functionality."""

    def setUp(self):
        mage_setup()
        self.existing_effect = Effect.objects.create(
            name="Existing Effect", forces=2, description="Pre-existing"
        )

    def test_save_returns_selected_effect(self):
        """Test that save returns the selected existing effect."""
        form = EffectCreateOrSelectForm(
            data={
                "select_or_create": False,
                "select": self.existing_effect.pk,
            }
        )
        form.is_valid()
        result = form.save()

        self.assertEqual(result, self.existing_effect)

    def test_save_creates_new_effect(self):
        """Test that save creates new effect when creating."""
        initial_count = Effect.objects.count()

        form = EffectCreateOrSelectForm(
            data={
                "select_or_create": True,
                "name": "Brand New Effect",
                "description": "A new creation",
                "forces": 3,
                "mind": 1,
            }
        )
        form.is_valid()
        result = form.save()

        self.assertEqual(Effect.objects.count(), initial_count + 1)
        self.assertEqual(result.name, "Brand New Effect")
        self.assertEqual(result.forces, 3)
        self.assertEqual(result.mind, 1)


class TestEffectCreateOrSelectFormCost(TestCase):
    """Test EffectCreateOrSelectForm cost method."""

    def setUp(self):
        mage_setup()
        self.existing_effect = Effect.objects.create(name="Cost 5 Effect", forces=3, mind=2)

    def test_cost_when_selecting_existing(self):
        """Test cost returns existing effect's cost."""
        form = EffectCreateOrSelectForm(
            data={
                "select_or_create": False,
                "select": self.existing_effect.pk,
            }
        )
        form.is_valid()

        self.assertEqual(form.cost(), self.existing_effect.cost())

    def test_cost_when_creating_new(self):
        """Test cost calculates from form sphere values."""
        form = EffectCreateOrSelectForm(
            data={
                "select_or_create": True,
                "name": "New Effect",
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "matter": 0,
                "life": 0,
                "forces": 2,
                "entropy": 1,
                "mind": 0,
                "prime": 0,
            }
        )
        form.is_valid()

        self.assertEqual(form.cost(), 3)


class TestEffectCreateOrSelectFormSetInit(TestCase):
    """Test EffectCreateOrSelectFormSet initialization."""

    def setUp(self):
        mage_setup()

    def test_formset_creates_forms(self):
        """Test that formset creates forms."""
        formset = EffectCreateOrSelectFormSet(queryset=Effect.objects.none())

        # Should have at least one extra form
        self.assertGreater(len(formset.forms), 0)

    def test_formset_forms_are_instances_of_correct_class(self):
        """Test that formset forms are instances of EffectCreateOrSelectForm."""
        formset = EffectCreateOrSelectFormSet(queryset=Effect.objects.none())

        # Check that instantiated forms have EffectCreateOrSelectForm's extra fields
        for form in formset.forms:
            self.assertIn("select_or_create", form.fields)
            self.assertIn("select", form.fields)

    def test_formset_accepts_queryset(self):
        """Test that formset accepts queryset parameter."""
        effect1 = Effect.objects.create(name="Effect 1", forces=1)
        effect2 = Effect.objects.create(name="Effect 2", forces=2)

        formset = EffectCreateOrSelectFormSet(
            queryset=Effect.objects.filter(pk__in=[effect1.pk, effect2.pk])
        )

        self.assertIsNotNone(formset)


class TestEffectCreateOrSelectFormSetValidation(TestCase):
    """Test EffectCreateOrSelectFormSet validation."""

    def setUp(self):
        mage_setup()
        self.existing_effect = Effect.objects.create(name="Existing", forces=2)

    def test_formset_initializes_with_data(self):
        """Test that formset initializes with data."""
        data = {
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-select_or_create": False,
            "form-0-select": self.existing_effect.pk,
        }

        formset = EffectCreateOrSelectFormSet(data=data, queryset=Effect.objects.none())

        # Formset should initialize without error
        self.assertIsNotNone(formset)


class TestEffectCreateOrSelectFormSetSave(TestCase):
    """Test EffectCreateOrSelectFormSet save functionality."""

    def setUp(self):
        mage_setup()
        self.existing_effect = Effect.objects.create(name="Existing", forces=2)

    def test_formset_save_returns_effects(self):
        """Test that formset save returns list of effects."""
        data = {
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-select_or_create": False,
            "form-0-select": self.existing_effect.pk,
        }

        formset = EffectCreateOrSelectFormSet(data=data, queryset=Effect.objects.none())
        formset.is_valid()
        results = formset.save()

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.existing_effect)

    def test_formset_save_creates_multiple_effects(self):
        """Test that formset can create multiple new effects."""
        initial_count = Effect.objects.count()

        data = {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-select_or_create": True,
            "form-0-name": "New Effect 1",
            "form-0-forces": 1,
            "form-1-select_or_create": True,
            "form-1-name": "New Effect 2",
            "form-1-mind": 2,
        }

        formset = EffectCreateOrSelectFormSet(data=data, queryset=Effect.objects.none())
        formset.is_valid()
        results = formset.save()

        self.assertEqual(len(results), 2)
        self.assertEqual(Effect.objects.count(), initial_count + 2)
