"""
Tests for DynastyForm.

Tests cover:
- Form initialization
- Widget attribute customization
- Form validation
- Form save functionality
"""

from django.test import TestCase

from characters.forms.mummy.dynasty import DynastyForm
from characters.models.mummy.dynasty import Dynasty


class TestDynastyFormInitialization(TestCase):
    """Test form initialization."""

    def test_form_initializes(self):
        """Form initializes correctly."""
        form = DynastyForm()

        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("era", form.fields)
        self.assertIn("favored_hekau", form.fields)

    def test_form_meta_fields(self):
        """Form has correct fields in Meta."""
        form = DynastyForm()

        expected_fields = ["name", "description", "era", "favored_hekau"]
        self.assertEqual(list(form.fields.keys()), expected_fields)


class TestDynastyFormWidgetAttrs(TestCase):
    """Test widget attribute customization."""

    def test_name_placeholder(self):
        """Name field has correct placeholder."""
        form = DynastyForm()
        placeholder = form.fields["name"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter dynasty name")

    def test_description_placeholder(self):
        """Description field has correct placeholder."""
        form = DynastyForm()
        placeholder = form.fields["description"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter description")

    def test_era_placeholder(self):
        """Era field has correct placeholder."""
        form = DynastyForm()
        placeholder = form.fields["era"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "e.g., Old Kingdom, Middle Kingdom")

    def test_favored_hekau_placeholder(self):
        """Favored hekau field has correct placeholder."""
        form = DynastyForm()
        placeholder = form.fields["favored_hekau"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "e.g., Alchemy, Necromancy")


class TestDynastyFormValidation(TestCase):
    """Test form validation."""

    def test_valid_minimal_submission(self):
        """Valid submission with minimal data."""
        form = DynastyForm(
            data={
                "name": "Test Dynasty",
            },
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_complete_submission(self):
        """Valid submission with all fields."""
        form = DynastyForm(
            data={
                "name": "Old Kingdom Dynasty",
                "description": "A dynasty from the Old Kingdom period.",
                "era": "Old Kingdom",
                "favored_hekau": "Necromancy",
            },
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_empty_submission_invalid(self):
        """Empty form submission is invalid."""
        form = DynastyForm(
            data={},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_duplicate_name_invalid(self):
        """Duplicate dynasty name is invalid."""
        Dynasty.objects.create(name="Existing Dynasty")

        form = DynastyForm(
            data={
                "name": "Existing Dynasty",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_optional_fields_blank(self):
        """Optional fields can be blank."""
        form = DynastyForm(
            data={
                "name": "Minimal Dynasty",
                "description": "",
                "era": "",
                "favored_hekau": "",
            },
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")


class TestDynastyFormSave(TestCase):
    """Test form save functionality."""

    def test_save_creates_dynasty(self):
        """Form save creates a new Dynasty."""
        form = DynastyForm(
            data={
                "name": "New Dynasty",
                "era": "New Kingdom",
                "favored_hekau": "Alchemy",
            },
        )

        self.assertTrue(form.is_valid())
        dynasty = form.save()

        self.assertIsNotNone(dynasty.pk)
        self.assertEqual(dynasty.name, "New Dynasty")
        self.assertEqual(dynasty.era, "New Kingdom")
        self.assertEqual(dynasty.favored_hekau, "Alchemy")

    def test_save_updates_dynasty(self):
        """Form save updates an existing Dynasty."""
        dynasty = Dynasty.objects.create(
            name="Old Name",
            era="Old Era",
        )

        form = DynastyForm(
            data={
                "name": "Updated Name",
                "era": "Updated Era",
            },
            instance=dynasty,
        )

        self.assertTrue(form.is_valid())
        updated = form.save()

        self.assertEqual(updated.pk, dynasty.pk)
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.era, "Updated Era")

    def test_save_commit_false(self):
        """Form save with commit=False does not save to database."""
        form = DynastyForm(
            data={
                "name": "Unsaved Dynasty",
            },
        )

        self.assertTrue(form.is_valid())
        dynasty = form.save(commit=False)

        self.assertIsNone(dynasty.pk)
        self.assertEqual(dynasty.name, "Unsaved Dynasty")


class TestDynastyFormWithInstance(TestCase):
    """Test form with existing Dynasty instance."""

    def setUp(self):
        """Create a Dynasty for testing."""
        self.dynasty = Dynasty.objects.create(
            name="Instance Dynasty",
            description="An existing dynasty",
            era="Middle Kingdom",
            favored_hekau="Celestial",
        )

    def test_form_populates_from_instance(self):
        """Form fields are populated from instance."""
        form = DynastyForm(instance=self.dynasty)

        self.assertEqual(form.initial["name"], "Instance Dynasty")
        self.assertEqual(form.initial["description"], "An existing dynasty")
        self.assertEqual(form.initial["era"], "Middle Kingdom")
        self.assertEqual(form.initial["favored_hekau"], "Celestial")

    def test_instance_update_valid(self):
        """Updating an instance with valid data."""
        form = DynastyForm(
            data={
                "name": "Instance Dynasty",  # Same name (unique constraint)
                "description": "Updated description",
                "era": "New Kingdom",
                "favored_hekau": "Effigy",
            },
            instance=self.dynasty,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
