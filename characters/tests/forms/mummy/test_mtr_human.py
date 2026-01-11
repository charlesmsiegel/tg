"""
Tests for MtRHumanCreationForm.

Tests cover:
- Form initialization with user parameter
- Widget attribute customization
- Form save with owner assignment
- Required/optional field handling
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.mummy.mtr_human import MtRHumanCreationForm
from game.models import Chronicle


class MtRHumanCreationFormTestCase(TestCase):
    """Base test case with common setup for MtRHumanCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def setUp(self):
        """Set up test users."""
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="testpassword",
        )


class TestMtRHumanCreationFormInitialization(MtRHumanCreationFormTestCase):
    """Test form initialization."""

    def test_form_requires_user(self):
        """Form initialization requires a user parameter."""
        with self.assertRaises(KeyError):
            MtRHumanCreationForm()

    def test_form_initializes_with_user(self):
        """Form initializes correctly with user."""
        form = MtRHumanCreationForm(user=self.user)

        self.assertEqual(form.user, self.user)
        self.assertIn("name", form.fields)
        self.assertIn("nature", form.fields)
        self.assertIn("demeanor", form.fields)
        self.assertIn("concept", form.fields)
        self.assertIn("chronicle", form.fields)
        self.assertIn("image", form.fields)
        self.assertIn("npc", form.fields)

    def test_form_meta_fields(self):
        """Form has correct fields in Meta."""
        form = MtRHumanCreationForm(user=self.user)

        expected_fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "chronicle",
            "image",
            "npc",
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)


class TestMtRHumanCreationFormFields(MtRHumanCreationFormTestCase):
    """Test form field configuration."""

    def test_image_not_required(self):
        """Image field is not required."""
        form = MtRHumanCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)


class TestMtRHumanCreationFormWidgetAttrs(MtRHumanCreationFormTestCase):
    """Test widget attribute customization."""

    def test_name_placeholder(self):
        """Name field has correct placeholder."""
        form = MtRHumanCreationForm(user=self.user)
        placeholder = form.fields["name"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter name here")

    def test_concept_placeholder(self):
        """Concept field has correct placeholder."""
        form = MtRHumanCreationForm(user=self.user)
        placeholder = form.fields["concept"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter concept here")


class TestMtRHumanCreationFormSave(MtRHumanCreationFormTestCase):
    """Test form save functionality."""

    def test_save_assigns_owner(self):
        """Form save assigns the user as owner."""
        form = MtRHumanCreationForm(
            data={
                "name": "Test Human",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        human = form.save()

        self.assertEqual(human.owner, self.user)
        self.assertEqual(human.name, "Test Human")

    def test_save_with_concept(self):
        """Form save with concept."""
        form = MtRHumanCreationForm(
            data={
                "name": "Concept Human",
                "concept": "Egyptian archaeologist",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        human = form.save()

        self.assertEqual(human.concept, "Egyptian archaeologist")

    def test_save_commit_false(self):
        """Form save with commit=False does not save to database."""
        form = MtRHumanCreationForm(
            data={
                "name": "Unsaved Human",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid())
        human = form.save(commit=False)

        self.assertIsNone(human.pk)
        self.assertEqual(human.owner, self.user)

    def test_save_with_chronicle(self):
        """Form save with chronicle assignment."""
        form = MtRHumanCreationForm(
            data={
                "name": "Chronicle Human",
                "chronicle": self.chronicle.pk,
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        human = form.save()

        self.assertEqual(human.chronicle, self.chronicle)

    def test_save_as_npc(self):
        """Form save with NPC flag."""
        form = MtRHumanCreationForm(
            data={
                "name": "NPC Human",
                "npc": True,
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        human = form.save()

        self.assertTrue(human.npc)


class TestMtRHumanCreationFormValidation(MtRHumanCreationFormTestCase):
    """Test form validation."""

    def test_valid_minimal_submission(self):
        """Valid submission with minimal data."""
        form = MtRHumanCreationForm(
            data={
                "name": "Minimal Human",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_complete_submission(self):
        """Valid submission with all fields."""
        form = MtRHumanCreationForm(
            data={
                "name": "Complete Human",
                "concept": "Museum curator",
                "chronicle": self.chronicle.pk,
                "npc": True,
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_empty_submission_invalid(self):
        """Empty form submission is invalid."""
        form = MtRHumanCreationForm(
            data={},
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestMtRHumanCreationFormOwnerAssignment(MtRHumanCreationFormTestCase):
    """Test owner assignment edge cases."""

    def test_save_with_none_user(self):
        """Form save with None user does not set owner."""
        form = MtRHumanCreationForm(
            data={
                "name": "No Owner Human",
            },
            user=None,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        human = form.save()

        self.assertIsNone(human.owner)

    def test_different_user_assignment(self):
        """Each user gets properly assigned as owner."""
        user1 = User.objects.create_user(username="user1", password="pass")
        user2 = User.objects.create_user(username="user2", password="pass")

        form1 = MtRHumanCreationForm(
            data={"name": "User1 Human"},
            user=user1,
        )
        form2 = MtRHumanCreationForm(
            data={"name": "User2 Human"},
            user=user2,
        )

        human1 = form1.save()
        human2 = form2.save()

        self.assertEqual(human1.owner, user1)
        self.assertEqual(human2.owner, user2)
