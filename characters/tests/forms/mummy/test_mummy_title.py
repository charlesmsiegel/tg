"""
Tests for MummyTitleForm.

Tests cover:
- Form initialization
- Widget attribute customization
- Form validation
- Form save functionality
"""

from django.test import TestCase

from characters.forms.mummy.mummy_title import MummyTitleForm
from characters.models.mummy.mummy_title import MummyTitle


class TestMummyTitleFormInitialization(TestCase):
    """Test form initialization."""

    def test_form_initializes(self):
        """Form initializes correctly."""
        form = MummyTitleForm()

        self.assertIn("name", form.fields)
        self.assertIn("rank_level", form.fields)
        self.assertIn("description", form.fields)

    def test_form_meta_fields(self):
        """Form has correct fields in Meta."""
        form = MummyTitleForm()

        expected_fields = ["name", "rank_level", "description"]
        self.assertEqual(list(form.fields.keys()), expected_fields)


class TestMummyTitleFormWidgetAttrs(TestCase):
    """Test widget attribute customization."""

    def test_name_placeholder(self):
        """Name field has correct placeholder."""
        form = MummyTitleForm()
        placeholder = form.fields["name"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter title name")

    def test_description_placeholder(self):
        """Description field has correct placeholder."""
        form = MummyTitleForm()
        placeholder = form.fields["description"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter description")


class TestMummyTitleFormValidation(TestCase):
    """Test form validation."""

    def test_valid_minimal_submission(self):
        """Valid submission with minimal data."""
        form = MummyTitleForm(
            data={
                "name": "Test Title",
                "rank_level": 0,
            },
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_complete_submission(self):
        """Valid submission with all fields."""
        form = MummyTitleForm(
            data={
                "name": "High Priest",
                "rank_level": 5,
                "description": "The highest rank in the temple hierarchy.",
            },
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_empty_submission_invalid(self):
        """Empty form submission is invalid."""
        form = MummyTitleForm(
            data={},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_duplicate_name_invalid(self):
        """Duplicate title name is invalid."""
        MummyTitle.objects.create(name="Existing Title")

        form = MummyTitleForm(
            data={
                "name": "Existing Title",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_optional_fields_blank(self):
        """Optional fields can be blank."""
        form = MummyTitleForm(
            data={
                "name": "Minimal Title",
                "rank_level": 1,
                "description": "",
            },
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_rank_level_required(self):
        """rank_level is a required field."""
        form = MummyTitleForm(
            data={
                "name": "No Rank Title",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rank_level", form.errors)


class TestMummyTitleFormSave(TestCase):
    """Test form save functionality."""

    def test_save_creates_title(self):
        """Form save creates a new MummyTitle."""
        form = MummyTitleForm(
            data={
                "name": "New Title",
                "rank_level": 3,
                "description": "A new title for testing.",
            },
        )

        self.assertTrue(form.is_valid())
        title = form.save()

        self.assertIsNotNone(title.pk)
        self.assertEqual(title.name, "New Title")
        self.assertEqual(title.rank_level, 3)
        self.assertEqual(title.description, "A new title for testing.")

    def test_save_updates_title(self):
        """Form save updates an existing MummyTitle."""
        title = MummyTitle.objects.create(
            name="Old Name",
            rank_level=1,
        )

        form = MummyTitleForm(
            data={
                "name": "Updated Name",
                "rank_level": 5,
            },
            instance=title,
        )

        self.assertTrue(form.is_valid())
        updated = form.save()

        self.assertEqual(updated.pk, title.pk)
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.rank_level, 5)

    def test_save_commit_false(self):
        """Form save with commit=False does not save to database."""
        form = MummyTitleForm(
            data={
                "name": "Unsaved Title",
                "rank_level": 2,
            },
        )

        self.assertTrue(form.is_valid())
        title = form.save(commit=False)

        self.assertIsNone(title.pk)
        self.assertEqual(title.name, "Unsaved Title")


class TestMummyTitleFormWithInstance(TestCase):
    """Test form with existing MummyTitle instance."""

    def setUp(self):
        """Create a MummyTitle for testing."""
        self.title = MummyTitle.objects.create(
            name="Instance Title",
            rank_level=4,
            description="An existing title",
        )

    def test_form_populates_from_instance(self):
        """Form fields are populated from instance."""
        form = MummyTitleForm(instance=self.title)

        self.assertEqual(form.initial["name"], "Instance Title")
        self.assertEqual(form.initial["rank_level"], 4)
        self.assertEqual(form.initial["description"], "An existing title")

    def test_instance_update_valid(self):
        """Updating an instance with valid data."""
        form = MummyTitleForm(
            data={
                "name": "Instance Title",  # Same name (unique constraint)
                "rank_level": 5,
                "description": "Updated description",
            },
            instance=self.title,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
