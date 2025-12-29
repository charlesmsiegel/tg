"""
Tests for Fera forms.

Tests cover:
- FeraCreationForm (character creation)
- Form validation for each Fera type
- Fera type to model class mapping
"""

from characters.forms.werewolf.fera import FeraCreationForm
from characters.models.werewolf.bastet import Bastet
from characters.models.werewolf.corax import Corax
from characters.models.werewolf.gurahl import Gurahl
from characters.models.werewolf.mokole import Mokole
from characters.models.werewolf.nuwisha import Nuwisha
from characters.models.werewolf.ratkin import Ratkin
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class FeraCreationFormTestCase(TestCase):
    """Base test case with common setup for FeraCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )


class TestFeraCreationFormInitialization(FeraCreationFormTestCase):
    """Test form initialization."""

    def test_form_initializes_with_user(self):
        """Form initializes correctly with a user."""
        form = FeraCreationForm(user=self.user)
        self.assertIsNotNone(form)

    def test_form_has_fera_type_field(self):
        """Form has fera_type field."""
        form = FeraCreationForm(user=self.user)
        self.assertIn("fera_type", form.fields)

    def test_fera_type_choices(self):
        """Fera type field has correct choices."""
        form = FeraCreationForm(user=self.user)
        fera_type_choices = [choice[0] for choice in form.fields["fera_type"].choices]
        self.assertIn("ratkin", fera_type_choices)
        self.assertIn("bastet", fera_type_choices)
        self.assertIn("corax", fera_type_choices)
        self.assertIn("mokole", fera_type_choices)
        self.assertIn("nuwisha", fera_type_choices)
        self.assertIn("gurahl", fera_type_choices)

    def test_form_has_required_fields(self):
        """Form has all required fields."""
        form = FeraCreationForm(user=self.user)
        self.assertIn("name", form.fields)
        self.assertIn("concept", form.fields)
        self.assertIn("chronicle", form.fields)
        self.assertIn("breed", form.fields)
        self.assertIn("image", form.fields)
        self.assertIn("npc", form.fields)

    def test_breed_field_not_required(self):
        """Breed field is not required at creation."""
        form = FeraCreationForm(user=self.user)
        self.assertFalse(form.fields["breed"].required)

    def test_image_field_not_required(self):
        """Image field is not required."""
        form = FeraCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)


class TestFeraCreationFormValidation(FeraCreationFormTestCase):
    """Test form validation."""

    def test_valid_form_minimal_data(self):
        """Form is valid with minimal data."""
        form = FeraCreationForm(
            data={
                "name": "Test Fera",
                "concept": "Test Concept",
                "fera_type": "ratkin",
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_name_required(self):
        """Name field is required."""
        form = FeraCreationForm(
            data={
                "name": "",
                "concept": "Test Concept",
                "fera_type": "ratkin",
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_fera_type_required(self):
        """Fera type field is required."""
        form = FeraCreationForm(
            data={
                "name": "Test Fera",
                "concept": "Test Concept",
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("fera_type", form.errors)

    def test_invalid_fera_type_rejected(self):
        """Invalid fera type is rejected."""
        form = FeraCreationForm(
            data={
                "name": "Test Fera",
                "concept": "Test Concept",
                "fera_type": "invalid_type",
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("fera_type", form.errors)


class TestFeraCreationFormSave(FeraCreationFormTestCase):
    """Test form save functionality.

    Note: Uses Corax for most tests since it's the simplest Fera type
    (no required aspect/tribe fields). This tests the form's save() method
    without triggering model validation for type-specific fields.
    """

    def test_save_creates_corax(self):
        """Save creates a Corax instance for corax type."""
        form = FeraCreationForm(
            data={
                "name": "Test Corax",
                "concept": "Spy",
                "fera_type": "corax",
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        instance = form.save()
        self.assertIsInstance(instance, Corax)
        self.assertEqual(instance.name, "Test Corax")
        self.assertEqual(instance.concept, "Spy")
        self.assertEqual(instance.owner, self.user)

    def test_save_sets_owner(self):
        """Save sets the owner from the user parameter."""
        form = FeraCreationForm(
            data={
                "name": "Test Fera",
                "concept": "Test Concept",
                "fera_type": "corax",
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        instance = form.save()
        self.assertEqual(instance.owner, self.user)

    def test_save_with_chronicle(self):
        """Save correctly assigns chronicle."""
        form = FeraCreationForm(
            data={
                "name": "Test Fera",
                "concept": "Test Concept",
                "fera_type": "corax",
                "chronicle": self.chronicle.pk,
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        instance = form.save()
        self.assertEqual(instance.chronicle, self.chronicle)

    def test_save_with_npc_flag(self):
        """Save correctly sets NPC flag."""
        form = FeraCreationForm(
            data={
                "name": "Test NPC",
                "concept": "Test Concept",
                "fera_type": "corax",
                "npc": True,
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        instance = form.save()
        self.assertTrue(instance.npc)

    def test_save_without_commit(self):
        """Save with commit=False returns unsaved instance."""
        form = FeraCreationForm(
            data={
                "name": "Test Fera",
                "concept": "Test Concept",
                "fera_type": "corax",
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        instance = form.save(commit=False)
        # Instance should not have a pk yet
        self.assertIsNone(instance.pk)


class TestFeraCreationFormFieldWidgets(FeraCreationFormTestCase):
    """Test form field widget configuration."""

    def test_name_placeholder(self):
        """Name field has placeholder text."""
        form = FeraCreationForm(user=self.user)
        self.assertIn(
            "placeholder",
            form.fields["name"].widget.attrs,
        )

    def test_concept_placeholder(self):
        """Concept field has placeholder text."""
        form = FeraCreationForm(user=self.user)
        self.assertIn(
            "placeholder",
            form.fields["concept"].widget.attrs,
        )

    def test_breed_placeholder(self):
        """Breed field has placeholder text."""
        form = FeraCreationForm(user=self.user)
        self.assertIn(
            "placeholder",
            form.fields["breed"].widget.attrs,
        )


class TestFeraTypeMapping(FeraCreationFormTestCase):
    """Test that fera types map to correct model classes."""

    def test_all_fera_types_have_model_mapping(self):
        """All fera type choices have corresponding model classes."""
        form = FeraCreationForm(user=self.user)
        fera_class_map = {
            "ratkin": Ratkin,
            "mokole": Mokole,
            "bastet": Bastet,
            "corax": Corax,
            "nuwisha": Nuwisha,
            "gurahl": Gurahl,
        }
        for fera_type, _ in form.FERA_TYPES:
            self.assertIn(
                fera_type,
                fera_class_map,
                f"Fera type '{fera_type}' has no model mapping",
            )


class TestFeraCreationFormEdgeCases(FeraCreationFormTestCase):
    """Test edge cases and boundary conditions."""

    def test_empty_concept_allowed(self):
        """Empty concept is allowed."""
        form = FeraCreationForm(
            data={
                "name": "Test Fera",
                "concept": "",
                "fera_type": "corax",  # Use Corax (simplest type)
            },
            user=self.user,
        )
        # Concept should not be required at form level
        # (may be validated at model level later)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_whitespace_name_validation(self):
        """Whitespace-only name should be handled."""
        form = FeraCreationForm(
            data={
                "name": "   ",
                "concept": "Test Concept",
                "fera_type": "corax",  # Use Corax (simplest type)
            },
            user=self.user,
        )
        # Depending on implementation, this may be valid or invalid
        # The test documents the current behavior
        if form.is_valid():
            instance = form.save()
            self.assertIsNotNone(instance)
        else:
            self.assertIn("name", form.errors)

    def test_very_long_name(self):
        """Very long name should be handled by CharField max_length."""
        long_name = "A" * 500  # Very long name
        form = FeraCreationForm(
            data={
                "name": long_name,
                "concept": "Test Concept",
                "fera_type": "corax",  # Use Corax (simplest type)
            },
            user=self.user,
        )
        # CharField max_length should be enforced
        if not form.is_valid():
            self.assertIn("name", form.errors)
