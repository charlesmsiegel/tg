"""
Tests for Sorcerer Artifact forms.

Tests cover:
- SorcererArtifactForm initialization and field configuration
- SorcererArtifactForm validation
- ArtifactCreateOrSelectForm for creating/selecting artifacts
- Save behavior for both form types
"""

from django.test import TestCase

from items.forms.mage.sorcerer_artifact import (
    ArtifactCreateOrSelectForm,
    SorcererArtifactForm,
)
from items.models.mage import SorcererArtifact


class TestSorcererArtifactFormBasics(TestCase):
    """Test basic SorcererArtifactForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = SorcererArtifactForm()

        self.assertIn("name", form.fields)
        self.assertIn("rank", form.fields)
        self.assertIn("description", form.fields)

    def test_name_placeholder(self):
        """Test that name field has correct placeholder."""
        form = SorcererArtifactForm()

        self.assertEqual(form.fields["name"].widget.attrs.get("placeholder"), "Enter name here")

    def test_description_placeholder(self):
        """Test that description field has correct placeholder."""
        form = SorcererArtifactForm()

        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter description here",
        )


class TestSorcererArtifactFormValidation(TestCase):
    """Test SorcererArtifactForm validation."""

    def test_valid_data(self):
        """Test that form validates with valid data."""
        form_data = {
            "name": "Test Artifact",
            "rank": 2,
            "description": "A magical artifact",
        }

        form = SorcererArtifactForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_name_required(self):
        """Test that name is required."""
        form_data = {
            "rank": 2,
            "description": "A magical artifact",
        }

        form = SorcererArtifactForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_empty_description_valid(self):
        """Test that empty description is valid."""
        form_data = {
            "name": "Test Artifact",
            "rank": 2,
            "description": "",
        }

        form = SorcererArtifactForm(data=form_data)

        self.assertTrue(form.is_valid())


class TestSorcererArtifactFormSave(TestCase):
    """Test SorcererArtifactForm save method."""

    def test_save_creates_artifact(self):
        """Test that save creates a sorcerer artifact."""
        form_data = {
            "name": "Test Artifact",
            "rank": 3,
            "description": "A powerful artifact",
        }

        form = SorcererArtifactForm(data=form_data)
        self.assertTrue(form.is_valid())

        artifact = form.save()

        self.assertIsNotNone(artifact)
        self.assertEqual(artifact.name, "Test Artifact")
        self.assertEqual(artifact.rank, 3)
        self.assertEqual(artifact.description, "A powerful artifact")

    def test_save_updates_existing_artifact(self):
        """Test that save updates an existing artifact."""
        existing = SorcererArtifact.objects.create(
            name="Old Name", rank=1, description="Old description"
        )

        form_data = {
            "name": "New Name",
            "rank": 2,
            "description": "New description",
        }

        form = SorcererArtifactForm(data=form_data, instance=existing)
        self.assertTrue(form.is_valid())

        artifact = form.save()

        self.assertEqual(artifact.pk, existing.pk)
        self.assertEqual(artifact.name, "New Name")
        self.assertEqual(artifact.rank, 2)
        self.assertEqual(artifact.description, "New description")

    def test_save_commit_false(self):
        """Test that save(commit=False) does not save to database."""
        form_data = {
            "name": "Test Artifact",
            "rank": 2,
            "description": "A magical artifact",
        }

        form = SorcererArtifactForm(data=form_data)
        self.assertTrue(form.is_valid())

        artifact = form.save(commit=False)

        self.assertIsNone(artifact.pk)


class TestArtifactCreateOrSelectFormBasics(TestCase):
    """Test basic ArtifactCreateOrSelectForm structure."""

    def test_form_has_required_fields(self):
        """Test that form has select_or_create, select, and model fields."""
        form = ArtifactCreateOrSelectForm()

        self.assertIn("select_or_create", form.fields)
        self.assertIn("select", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("rank", form.fields)
        self.assertIn("description", form.fields)

    def test_all_fields_optional(self):
        """Test that all fields are optional."""
        form = ArtifactCreateOrSelectForm()

        for field in form.fields.values():
            self.assertFalse(field.required)

    def test_name_placeholder(self):
        """Test that name field has correct placeholder."""
        form = ArtifactCreateOrSelectForm()

        self.assertEqual(form.fields["name"].widget.attrs.get("placeholder"), "Enter name here")

    def test_description_placeholder(self):
        """Test that description field has correct placeholder."""
        form = ArtifactCreateOrSelectForm()

        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter description here",
        )


class TestArtifactCreateOrSelectFormValidation(TestCase):
    """Test ArtifactCreateOrSelectForm validation."""

    @classmethod
    def setUpTestData(cls):
        """Create artifacts for selection tests."""
        cls.existing_artifact = SorcererArtifact.objects.create(
            name="Existing Artifact", rank=2, description="An existing artifact"
        )

    def test_select_existing_artifact_valid(self):
        """Test that selecting an existing artifact is valid."""
        form_data = {
            "select": str(self.existing_artifact.pk),
            # select_or_create not checked = select mode
        }

        form = ArtifactCreateOrSelectForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_create_new_artifact_valid(self):
        """Test that creating a new artifact is valid."""
        form_data = {
            "select_or_create": "on",
            "name": "New Artifact",
            "rank": "3",
            "description": "A brand new artifact",
        }

        form = ArtifactCreateOrSelectForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_neither_select_nor_create_invalid(self):
        """Test that providing neither select nor create is invalid."""
        form_data = {
            # No select, no select_or_create
        }

        form = ArtifactCreateOrSelectForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("select", form.errors)
        self.assertIn(
            "You must either select an existing Artifact or choose to create a new one",
            str(form.errors),
        )


class TestArtifactCreateOrSelectFormSave(TestCase):
    """Test ArtifactCreateOrSelectForm save method."""

    @classmethod
    def setUpTestData(cls):
        """Create artifact for selection tests."""
        cls.existing_artifact = SorcererArtifact.objects.create(
            name="Existing Artifact", rank=2, description="An existing artifact"
        )

    def test_save_returns_selected_artifact(self):
        """Test that save returns the selected artifact when in select mode."""
        form_data = {
            "select": str(self.existing_artifact.pk),
            # select_or_create not checked = select mode
        }

        form = ArtifactCreateOrSelectForm(data=form_data)
        self.assertTrue(form.is_valid())

        result = form.save()

        self.assertEqual(result, self.existing_artifact)

    def test_save_creates_new_artifact(self):
        """Test that save creates a new artifact when in create mode."""
        form_data = {
            "select_or_create": "on",
            "name": "New Artifact",
            "rank": "4",
            "description": "A powerful new artifact",
        }

        form = ArtifactCreateOrSelectForm(data=form_data)
        self.assertTrue(form.is_valid())

        result = form.save()

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "New Artifact")
        self.assertEqual(result.rank, 4)

    def test_save_commit_false_does_not_save_new(self):
        """Test that save(commit=False) doesn't save new artifact to database."""
        form_data = {
            "select_or_create": "on",
            "name": "Unsaved Artifact",
            "rank": "1",
            "description": "Not yet saved",
        }

        form = ArtifactCreateOrSelectForm(data=form_data)
        self.assertTrue(form.is_valid())

        result = form.save(commit=False)

        self.assertIsNone(result.pk)


class TestArtifactCreateOrSelectFormEdgeCases(TestCase):
    """Test edge cases for ArtifactCreateOrSelectForm."""

    @classmethod
    def setUpTestData(cls):
        """Create artifact for testing."""
        cls.existing_artifact = SorcererArtifact.objects.create(
            name="Existing Artifact", rank=2, description="An existing artifact"
        )

    def test_select_with_create_checked_uses_new(self):
        """Test that when both select and create are provided, create takes precedence."""
        form_data = {
            "select_or_create": "on",  # Create mode
            "select": str(self.existing_artifact.pk),  # Also have select
            "name": "New Artifact",
            "rank": "5",
            "description": "Created artifact",
        }

        form = ArtifactCreateOrSelectForm(data=form_data)
        self.assertTrue(form.is_valid())

        result = form.save()

        # Should create new, not return existing
        self.assertNotEqual(result.pk, self.existing_artifact.pk)
        self.assertEqual(result.name, "New Artifact")

    def test_form_bound_with_data(self):
        """Test that form becomes bound when data is provided."""
        form_data = {
            "select": str(self.existing_artifact.pk),
        }

        form = ArtifactCreateOrSelectForm(data=form_data)

        self.assertTrue(form.is_bound)

    def test_form_unbound_without_data(self):
        """Test that form is unbound when no data is provided."""
        form = ArtifactCreateOrSelectForm()

        self.assertFalse(form.is_bound)


class TestSorcererArtifactFormWithInstance(TestCase):
    """Test SorcererArtifactForm with existing instances."""

    def test_form_populates_from_instance(self):
        """Test that form is populated with instance data."""
        artifact = SorcererArtifact.objects.create(
            name="Instance Artifact", rank=3, description="Instance description"
        )

        form = SorcererArtifactForm(instance=artifact)

        self.assertEqual(form.initial["name"], "Instance Artifact")
        self.assertEqual(form.initial["rank"], 3)
        self.assertEqual(form.initial["description"], "Instance description")

    def test_form_meta_model(self):
        """Test that form's Meta is correctly configured."""
        form = SorcererArtifactForm()

        self.assertEqual(form.Meta.model, SorcererArtifact)
        self.assertEqual(form.Meta.fields, ["name", "rank", "description"])
