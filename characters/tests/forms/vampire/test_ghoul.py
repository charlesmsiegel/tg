"""
Tests for GhoulCreationForm.

Tests cover:
- Form initialization with user
- Queryset setup for domitor field
- Field configuration (required fields, placeholders)
- Form validation with valid and invalid data
- Owner assignment on save
"""

from characters.forms.vampire.ghoul import GhoulCreationForm
from characters.models.core.archetype import Archetype
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class GhoulCreationFormTestCase(TestCase):
    """Base test case with common setup for GhoulCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create a clan
        cls.ventrue = VampireClan.objects.create(
            name="Ventrue",
            nickname="Blue Bloods",
        )

        # Create archetypes
        cls.survivor = Archetype.objects.create(name="Survivor")
        cls.soldier = Archetype.objects.create(name="Soldier")

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create potential domitor
        self.domitor = Vampire.objects.create(
            name="Lord Ventrue",
            owner=self.user,
            clan=self.ventrue,
        )


class TestGhoulCreationFormInitialization(GhoulCreationFormTestCase):
    """Test form initialization."""

    def test_form_initializes_with_user(self):
        """Form initializes correctly with user parameter."""
        form = GhoulCreationForm(user=self.user)
        self.assertEqual(form.user, self.user)

    def test_form_has_expected_fields(self):
        """Form has all expected fields."""
        form = GhoulCreationForm(user=self.user)
        expected_fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "domitor",
            "is_independent",
            "chronicle",
            "image",
            "npc",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_domitor_queryset_empty_initially(self):
        """Domitor queryset is empty when form is not bound."""
        form = GhoulCreationForm(user=self.user)
        domitor_qs = form.fields["domitor"].queryset
        self.assertEqual(domitor_qs.count(), 0)


class TestGhoulCreationFormFieldConfiguration(GhoulCreationFormTestCase):
    """Test form field configuration."""

    def test_name_has_placeholder(self):
        """Name field has placeholder."""
        form = GhoulCreationForm(user=self.user)
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Enter name here",
        )

    def test_concept_has_placeholder(self):
        """Concept field has placeholder."""
        form = GhoulCreationForm(user=self.user)
        self.assertEqual(
            form.fields["concept"].widget.attrs.get("placeholder"),
            "Enter concept here",
        )

    def test_image_not_required(self):
        """Image field is not required."""
        form = GhoulCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)

    def test_domitor_not_required(self):
        """Domitor field is not required."""
        form = GhoulCreationForm(user=self.user)
        self.assertFalse(form.fields["domitor"].required)


class TestGhoulCreationFormBoundData(GhoulCreationFormTestCase):
    """Test form behavior when bound with data."""

    def test_domitor_queryset_populated_when_bound(self):
        """Domitor queryset includes all vampires when form is bound."""
        form = GhoulCreationForm(
            data={
                "name": "New Ghoul",
                "concept": "Bodyguard",
            },
            user=self.user,
        )
        domitor_qs = form.fields["domitor"].queryset
        self.assertIn(self.domitor, domitor_qs)


class TestGhoulCreationFormValidation(GhoulCreationFormTestCase):
    """Test form validation."""

    def test_valid_minimal_submission(self):
        """Valid submission with minimal required data."""
        form = GhoulCreationForm(
            data={
                "name": "Test Ghoul",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.soldier.pk),
                "concept": "Bodyguard",
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_with_domitor(self):
        """Valid submission with domitor specified."""
        form = GhoulCreationForm(
            data={
                "name": "Test Ghoul",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.soldier.pk),
                "concept": "Bodyguard",
                "domitor": str(self.domitor.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_independent_ghoul(self):
        """Valid submission for independent ghoul."""
        form = GhoulCreationForm(
            data={
                "name": "Independent Ghoul",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.soldier.pk),
                "concept": "Survivor",
                "is_independent": True,
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_invalid_without_name(self):
        """Form is invalid without name."""
        form = GhoulCreationForm(
            data={
                "concept": "Bodyguard",
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestGhoulCreationFormSave(GhoulCreationFormTestCase):
    """Test form save functionality."""

    def test_save_assigns_owner(self):
        """Saving form assigns owner to ghoul."""
        form = GhoulCreationForm(
            data={
                "name": "Test Ghoul",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.soldier.pk),
                "concept": "Bodyguard",
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        ghoul = form.save()
        self.assertEqual(ghoul.owner, self.user)

    def test_save_commit_false(self):
        """Saving with commit=False returns unsaved instance."""
        form = GhoulCreationForm(
            data={
                "name": "Test Ghoul",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.soldier.pk),
                "concept": "Bodyguard",
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        ghoul = form.save(commit=False)
        self.assertIsNone(ghoul.pk)
        self.assertEqual(ghoul.owner, self.user)

    def test_save_creates_ghoul_with_domitor(self):
        """Saving form creates ghoul with correct domitor."""
        form = GhoulCreationForm(
            data={
                "name": "Marcus the Guard",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.soldier.pk),
                "concept": "Trusted Bodyguard",
                "domitor": str(self.domitor.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        ghoul = form.save()

        self.assertEqual(ghoul.name, "Marcus the Guard")
        self.assertEqual(ghoul.concept, "Trusted Bodyguard")
        self.assertEqual(ghoul.domitor, self.domitor)
        self.assertEqual(ghoul.owner, self.user)

    def test_save_creates_independent_ghoul(self):
        """Saving form creates independent ghoul correctly."""
        form = GhoulCreationForm(
            data={
                "name": "Ancient Ghoul",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.soldier.pk),
                "concept": "Survivor",
                "is_independent": True,
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        ghoul = form.save()

        self.assertEqual(ghoul.name, "Ancient Ghoul")
        self.assertTrue(ghoul.is_independent)
        self.assertIsNone(ghoul.domitor)
