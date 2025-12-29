"""
Tests for MummyCreationForm.

Tests cover:
- Form initialization with user parameter
- Dynasty queryset population
- Widget attribute customization
- Form save with owner assignment
- Required/optional field handling
"""

from characters.forms.mummy.mummy import MummyCreationForm
from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mummy import Mummy
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class MummyCreationFormTestCase(TestCase):
    """Base test case with common setup for MummyCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        cls.dynasty_old = Dynasty.objects.create(
            name="Old Kingdom Dynasty",
            era="Old Kingdom",
            favored_hekau="Necromancy",
        )
        cls.dynasty_middle = Dynasty.objects.create(
            name="Middle Kingdom Dynasty",
            era="Middle Kingdom",
            favored_hekau="Alchemy",
        )
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def setUp(self):
        """Set up test users."""
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="testpassword",
        )


class TestMummyCreationFormInitialization(MummyCreationFormTestCase):
    """Test form initialization."""

    def test_form_requires_user(self):
        """Form initialization requires a user parameter."""
        with self.assertRaises(KeyError):
            MummyCreationForm()

    def test_form_initializes_with_user(self):
        """Form initializes correctly with user."""
        form = MummyCreationForm(user=self.user)

        self.assertEqual(form.user, self.user)
        self.assertIn("name", form.fields)
        self.assertIn("nature", form.fields)
        self.assertIn("demeanor", form.fields)
        self.assertIn("concept", form.fields)
        self.assertIn("dynasty", form.fields)
        self.assertIn("web", form.fields)
        self.assertIn("ancient_name", form.fields)
        self.assertIn("chronicle", form.fields)
        self.assertIn("image", form.fields)
        self.assertIn("npc", form.fields)

    def test_dynasty_queryset_populated(self):
        """Dynasty field queryset contains all dynasties."""
        form = MummyCreationForm(user=self.user)

        dynasty_qs = form.fields["dynasty"].queryset
        self.assertIn(self.dynasty_old, dynasty_qs)
        self.assertIn(self.dynasty_middle, dynasty_qs)
        self.assertEqual(dynasty_qs.count(), 2)


class TestMummyCreationFormFields(MummyCreationFormTestCase):
    """Test form field configuration."""

    def test_dynasty_not_required(self):
        """Dynasty field is not required."""
        form = MummyCreationForm(user=self.user)
        self.assertFalse(form.fields["dynasty"].required)

    def test_image_not_required(self):
        """Image field is not required."""
        form = MummyCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)


class TestMummyCreationFormWidgetAttrs(MummyCreationFormTestCase):
    """Test widget attribute customization."""

    def test_name_placeholder(self):
        """Name field has correct placeholder."""
        form = MummyCreationForm(user=self.user)
        placeholder = form.fields["name"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter name here")

    def test_concept_placeholder(self):
        """Concept field has correct placeholder."""
        form = MummyCreationForm(user=self.user)
        placeholder = form.fields["concept"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Enter concept here")

    def test_ancient_name_placeholder(self):
        """Ancient name field has correct placeholder."""
        form = MummyCreationForm(user=self.user)
        placeholder = form.fields["ancient_name"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Name from First Life in ancient Egypt")


class TestMummyCreationFormSave(MummyCreationFormTestCase):
    """Test form save functionality."""

    def test_save_assigns_owner(self):
        """Form save assigns the user as owner."""
        form = MummyCreationForm(
            data={
                "name": "Test Mummy",
                "web": "isis",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        mummy = form.save()

        self.assertEqual(mummy.owner, self.user)
        self.assertEqual(mummy.name, "Test Mummy")
        self.assertEqual(mummy.web, "isis")

    def test_save_with_dynasty(self):
        """Form save with dynasty assignment."""
        form = MummyCreationForm(
            data={
                "name": "Dynasty Mummy",
                "web": "osiris",
                "dynasty": self.dynasty_old.pk,
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        mummy = form.save()

        self.assertEqual(mummy.dynasty, self.dynasty_old)

    def test_save_with_ancient_name(self):
        """Form save with ancient name."""
        form = MummyCreationForm(
            data={
                "name": "Modern Name",
                "ancient_name": "Imhotep",
                "web": "thoth",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        mummy = form.save()

        self.assertEqual(mummy.ancient_name, "Imhotep")

    def test_save_commit_false(self):
        """Form save with commit=False does not save to database."""
        form = MummyCreationForm(
            data={
                "name": "Unsaved Mummy",
                "web": "maat",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid())
        mummy = form.save(commit=False)

        self.assertIsNone(mummy.pk)
        self.assertEqual(mummy.owner, self.user)

    def test_save_with_chronicle(self):
        """Form save with chronicle assignment."""
        form = MummyCreationForm(
            data={
                "name": "Chronicle Mummy",
                "web": "horus",
                "chronicle": self.chronicle.pk,
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        mummy = form.save()

        self.assertEqual(mummy.chronicle, self.chronicle)


class TestMummyCreationFormValidation(MummyCreationFormTestCase):
    """Test form validation."""

    def test_valid_minimal_submission(self):
        """Valid submission with minimal data."""
        form = MummyCreationForm(
            data={
                "name": "Minimal Mummy",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_complete_submission(self):
        """Valid submission with all fields."""
        form = MummyCreationForm(
            data={
                "name": "Complete Mummy",
                "concept": "Ancient guardian",
                "web": "isis",
                "dynasty": self.dynasty_old.pk,
                "ancient_name": "Nefertari",
                "chronicle": self.chronicle.pk,
                "npc": True,
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_all_web_choices_valid(self):
        """All Web choices are valid."""
        web_choices = ["isis", "osiris", "horus", "maat", "thoth"]

        for web in web_choices:
            form = MummyCreationForm(
                data={
                    "name": f"Mummy of {web.title()}",
                    "web": web,
                },
                user=self.user,
            )
            self.assertTrue(
                form.is_valid(),
                f"Web '{web}' should be valid. Errors: {form.errors}",
            )

    def test_empty_submission_invalid(self):
        """Empty form submission is invalid."""
        form = MummyCreationForm(
            data={},
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
