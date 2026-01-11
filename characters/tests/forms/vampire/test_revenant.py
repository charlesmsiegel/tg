"""
Tests for RevenantCreationForm.

Tests cover:
- Form initialization with user
- Queryset setup for family field
- Field configuration (required fields, placeholders)
- Form validation with valid and invalid data
- Owner assignment on save
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.vampire.revenant import RevenantCreationForm
from characters.models.core.archetype import Archetype
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.revenant import RevenantFamily
from game.models import Chronicle


class RevenantCreationFormTestCase(TestCase):
    """Base test case with common setup for RevenantCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.fortitude = Discipline.objects.create(name="Fortitude", property_name="fortitude")
        cls.vicissitude = Discipline.objects.create(name="Vicissitude", property_name="vicissitude")

        # Create revenant families
        cls.bratovich = RevenantFamily.objects.create(
            name="Bratovich",
            description="Brutal overseers and enforcers",
            weakness="Sadistic tendencies",
        )
        cls.bratovich.disciplines.add(cls.potence, cls.fortitude, cls.vicissitude)

        cls.grimaldi = RevenantFamily.objects.create(
            name="Grimaldi",
            description="Diplomats and spies",
        )

        # Create archetypes
        cls.survivor = Archetype.objects.create(name="Survivor")
        cls.brute = Archetype.objects.create(name="Brute")

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")


class TestRevenantCreationFormInitialization(RevenantCreationFormTestCase):
    """Test form initialization."""

    def test_form_initializes_with_user(self):
        """Form initializes correctly with user parameter."""
        form = RevenantCreationForm(user=self.user)
        self.assertEqual(form.user, self.user)

    def test_form_has_expected_fields(self):
        """Form has all expected fields."""
        form = RevenantCreationForm(user=self.user)
        expected_fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "family",
            "chronicle",
            "image",
            "npc",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_family_queryset_includes_all_families(self):
        """Family queryset includes all revenant families."""
        form = RevenantCreationForm(user=self.user)
        family_qs = form.fields["family"].queryset
        self.assertIn(self.bratovich, family_qs)
        self.assertIn(self.grimaldi, family_qs)


class TestRevenantCreationFormFieldConfiguration(RevenantCreationFormTestCase):
    """Test form field configuration."""

    def test_name_has_placeholder(self):
        """Name field has placeholder."""
        form = RevenantCreationForm(user=self.user)
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Enter name here",
        )

    def test_concept_has_placeholder(self):
        """Concept field has placeholder."""
        form = RevenantCreationForm(user=self.user)
        self.assertEqual(
            form.fields["concept"].widget.attrs.get("placeholder"),
            "Enter concept here",
        )

    def test_image_not_required(self):
        """Image field is not required."""
        form = RevenantCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)

    def test_family_not_required(self):
        """Family field is not required."""
        form = RevenantCreationForm(user=self.user)
        self.assertFalse(form.fields["family"].required)


class TestRevenantCreationFormValidation(RevenantCreationFormTestCase):
    """Test form validation."""

    def test_valid_minimal_submission(self):
        """Valid submission with minimal required data."""
        form = RevenantCreationForm(
            data={
                "name": "Test Revenant",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.brute.pk),
                "concept": "Family Enforcer",
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_with_family(self):
        """Valid submission with family specified."""
        form = RevenantCreationForm(
            data={
                "name": "Test Revenant",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.brute.pk),
                "concept": "Family Enforcer",
                "family": str(self.bratovich.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_invalid_without_name(self):
        """Form is invalid without name."""
        form = RevenantCreationForm(
            data={
                "concept": "Enforcer",
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestRevenantCreationFormSave(RevenantCreationFormTestCase):
    """Test form save functionality."""

    def test_save_assigns_owner(self):
        """Saving form assigns owner to revenant."""
        form = RevenantCreationForm(
            data={
                "name": "Test Revenant",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.brute.pk),
                "concept": "Enforcer",
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        revenant = form.save()
        self.assertEqual(revenant.owner, self.user)

    def test_save_commit_false(self):
        """Saving with commit=False returns unsaved instance."""
        form = RevenantCreationForm(
            data={
                "name": "Test Revenant",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.brute.pk),
                "concept": "Enforcer",
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        revenant = form.save(commit=False)
        self.assertIsNone(revenant.pk)
        self.assertEqual(revenant.owner, self.user)

    def test_save_creates_revenant_with_family(self):
        """Saving form creates revenant with correct family."""
        form = RevenantCreationForm(
            data={
                "name": "Ivan Bratovich",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.brute.pk),
                "concept": "Family Enforcer",
                "family": str(self.bratovich.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        revenant = form.save()

        self.assertEqual(revenant.name, "Ivan Bratovich")
        self.assertEqual(revenant.concept, "Family Enforcer")
        self.assertEqual(revenant.family, self.bratovich)
        self.assertEqual(revenant.owner, self.user)

    def test_save_creates_revenant_without_family(self):
        """Saving form creates revenant without family (orphan)."""
        form = RevenantCreationForm(
            data={
                "name": "Orphan Revenant",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.brute.pk),
                "concept": "Lost One",
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        revenant = form.save()

        self.assertEqual(revenant.name, "Orphan Revenant")
        self.assertIsNone(revenant.family)
