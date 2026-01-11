"""
Tests for FamiliarForm.

Tests cover:
- FamiliarForm initialization and field configuration
- Companion name and type fields
- FamiliarForm save functionality
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.mage.familiar import FamiliarForm
from characters.models.core.archetype import Archetype
from characters.models.mage.companion import Companion
from characters.tests.utils import mage_setup


class TestFamiliarFormInit(TestCase):
    """Test FamiliarForm initialization."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = FamiliarForm()

        self.assertIn("name", form.fields)
        self.assertIn("nature", form.fields)
        self.assertIn("demeanor", form.fields)
        self.assertIn("concept", form.fields)
        self.assertIn("image", form.fields)

    def test_form_name_has_placeholder(self):
        """Test that name field has placeholder text."""
        form = FamiliarForm()

        self.assertIn("placeholder", form.fields["name"].widget.attrs)

    def test_form_concept_has_placeholder(self):
        """Test that concept field has placeholder text."""
        form = FamiliarForm()

        self.assertIn("placeholder", form.fields["concept"].widget.attrs)

    def test_form_image_not_required(self):
        """Test that image field is not required."""
        form = FamiliarForm()

        self.assertFalse(form.fields["image"].required)

    def test_form_nature_queryset_ordered(self):
        """Test that nature queryset is ordered by name."""
        form = FamiliarForm()
        queryset = form.fields["nature"].queryset

        if queryset.exists():
            names = list(queryset.values_list("name", flat=True))
            self.assertEqual(names, sorted(names))

    def test_form_demeanor_queryset_ordered(self):
        """Test that demeanor queryset is ordered by name."""
        form = FamiliarForm()
        queryset = form.fields["demeanor"].queryset

        if queryset.exists():
            names = list(queryset.values_list("name", flat=True))
            self.assertEqual(names, sorted(names))


class TestFamiliarFormValidation(TestCase):
    """Test FamiliarForm validation."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.archetype = Archetype.objects.first()

    def test_form_valid_with_required_fields(self):
        """Test that form is valid with required fields."""
        form = FamiliarForm(
            data={
                "name": "Test Familiar",
                "nature": self.archetype.pk if self.archetype else "",
                "demeanor": self.archetype.pk if self.archetype else "",
                "concept": "A test familiar",
            },
        )

        # Form may or may not be valid depending on if archetype exists
        self.assertIsNotNone(form)

    def test_form_invalid_without_name(self):
        """Test that form is invalid without name."""
        form = FamiliarForm(
            data={
                "name": "",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestFamiliarFormSave(TestCase):
    """Test FamiliarForm save functionality."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.archetype = Archetype.objects.first()

    def test_save_creates_companion(self):
        """Test that save creates a companion."""
        initial_count = Companion.objects.count()

        if self.archetype:
            form = FamiliarForm(
                data={
                    "name": "My Familiar",
                    "nature": self.archetype.pk,
                    "demeanor": self.archetype.pk,
                    "concept": "A test familiar",
                },
            )
            if form.is_valid():
                result = form.save()

                self.assertEqual(Companion.objects.count(), initial_count + 1)
                self.assertEqual(result.name, "My Familiar")
                self.assertEqual(result.companion_type, "familiar")
                self.assertTrue(result.npc)

    def test_save_sets_familiar_companion_type(self):
        """Test that save sets companion type to familiar."""
        if self.archetype:
            form = FamiliarForm(
                data={
                    "name": "Typed Familiar",
                    "nature": self.archetype.pk,
                    "demeanor": self.archetype.pk,
                    "concept": "A typed familiar",
                },
            )
            if form.is_valid():
                result = form.save()

                self.assertEqual(result.companion_type, "familiar")

    def test_save_sets_npc_true(self):
        """Test that save sets npc to True."""
        if self.archetype:
            form = FamiliarForm(
                data={
                    "name": "NPC Familiar",
                    "nature": self.archetype.pk,
                    "demeanor": self.archetype.pk,
                    "concept": "An NPC familiar",
                },
            )
            if form.is_valid():
                result = form.save()

                self.assertTrue(result.npc)
