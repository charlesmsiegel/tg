"""
Tests for Practice Rating forms (PracticeRatingForm, PracticeRatingFormSet).

Tests cover:
- PracticeRatingForm initialization and field configuration
- Practice queryset filtering based on mage faction
- Specialized practice handling
- Corrupted practice exclusion
- BasePracticeRatingFormSet behavior
- Practice queryset method
"""

from characters.forms.mage.practiceform import (
    BasePracticeRatingFormSet,
    PracticeRatingForm,
    PracticeRatingFormSet,
)
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import CorruptedPractice, Practice, SpecializedPractice
from characters.models.mage.mage import Mage
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase


class TestPracticeRatingFormInit(TestCase):
    """Test PracticeRatingForm initialization."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.filter(parent__isnull=False).first()
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            faction=self.faction,
        )

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = PracticeRatingForm()

        self.assertIn("practice", form.fields)
        self.assertIn("rating", form.fields)

    def test_rating_field_has_correct_constraints(self):
        """Test that rating field has correct min/max constraints."""
        form = PracticeRatingForm()

        self.assertEqual(form.fields["rating"].min_value, 0)
        self.assertEqual(form.fields["rating"].max_value, 5)

    def test_practice_field_has_empty_label(self):
        """Test that practice field has an empty label option."""
        form = PracticeRatingForm()

        self.assertEqual(form.fields["practice"].empty_label, "Choose a Practice")

    def test_form_without_mage_has_general_practices(self):
        """Test that form without mage has general practices."""
        form = PracticeRatingForm()
        practice_queryset = form.fields["practice"].queryset

        # Should exclude specialized and corrupted practices
        specialized = SpecializedPractice.objects.first()
        if specialized:
            self.assertNotIn(specialized, practice_queryset)

    def test_form_with_mage_filters_practices(self):
        """Test that form with mage filters practices by faction."""
        form = PracticeRatingForm(mage=self.mage)
        practice_queryset = form.fields["practice"].queryset

        # Should have practices ordered by name
        self.assertTrue(practice_queryset.exists())


class TestPracticeRatingFormWithFaction(TestCase):
    """Test PracticeRatingForm with faction-specific practices."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create a faction with specialized practice
        self.faction = MageFaction.objects.create(name="Test Faction With Specialized")
        self.parent_practice = Practice.objects.first()
        self.specialized_practice = SpecializedPractice.objects.create(
            name="Faction Specialized Practice",
            parent_practice=self.parent_practice,
            faction=self.faction,
        )

        self.mage = Mage.objects.create(
            name="Faction Mage",
            owner=self.user,
            faction=self.faction,
        )

    def test_form_includes_faction_specialized_practice(self):
        """Test that form includes specialized practice for mage's faction."""
        form = PracticeRatingForm(mage=self.mage)
        practice_queryset = form.fields["practice"].queryset

        # Specialized practice should be included
        self.assertIn(self.specialized_practice, practice_queryset)

    def test_form_excludes_parent_of_specialized_practice(self):
        """Test that form excludes parent practice when specialized exists."""
        form = PracticeRatingForm(mage=self.mage)
        practice_queryset = form.fields["practice"].queryset

        # Parent practice should be excluded in favor of specialized
        self.assertNotIn(self.parent_practice, practice_queryset)

    def test_form_excludes_other_faction_specialized(self):
        """Test that form excludes specialized practices from other factions."""
        other_faction = MageFaction.objects.create(name="Other Faction")
        other_specialized = SpecializedPractice.objects.create(
            name="Other Faction Practice",
            parent_practice=Practice.objects.last(),
            faction=other_faction,
        )

        form = PracticeRatingForm(mage=self.mage)
        practice_queryset = form.fields["practice"].queryset

        self.assertNotIn(other_specialized, practice_queryset)


class TestPracticeRatingFormExclusions(TestCase):
    """Test that PracticeRatingForm properly excludes certain practice types."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.filter(parent__isnull=False).first()
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            faction=self.faction,
        )

    def test_form_excludes_corrupted_practices(self):
        """Test that form excludes corrupted practices."""
        parent = Practice.objects.first()
        corrupted = CorruptedPractice.objects.create(
            name="Corrupted Test Practice",
            parent_practice=parent,
        )

        form = PracticeRatingForm(mage=self.mage)
        practice_queryset = form.fields["practice"].queryset

        self.assertNotIn(corrupted, practice_queryset)

    def test_form_excludes_specialized_without_faction(self):
        """Test that specialized practices without matching faction are excluded."""
        parent = Practice.objects.first()
        other_faction = MageFaction.objects.create(name="Other Faction")
        specialized = SpecializedPractice.objects.create(
            name="Unrelated Specialized",
            parent_practice=parent,
            faction=other_faction,
        )

        form = PracticeRatingForm(mage=self.mage)
        practice_queryset = form.fields["practice"].queryset

        self.assertNotIn(specialized, practice_queryset)


class TestBasePracticeRatingFormSet(TestCase):
    """Test BasePracticeRatingFormSet behavior."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.filter(parent__isnull=False).first()
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            faction=self.faction,
        )

    def test_formset_stores_mage(self):
        """Test that formset stores mage reference."""
        formset = PracticeRatingFormSet(instance=self.mage, mage=self.mage)

        self.assertEqual(formset.mage, self.mage)

    def test_formset_applies_queryset_to_forms(self):
        """Test that formset applies practice queryset to all forms."""
        formset = PracticeRatingFormSet(instance=self.mage, mage=self.mage)

        for form in formset.forms:
            # Each form should have filtered practice queryset
            self.assertTrue(form.fields["practice"].queryset.exists())

    def test_formset_get_practice_queryset_with_mage(self):
        """Test get_practice_queryset method with mage."""
        formset = PracticeRatingFormSet(instance=self.mage, mage=self.mage)
        queryset = formset.get_practice_queryset()

        # Should return ordered queryset
        self.assertTrue(queryset.exists())

    def test_formset_get_practice_queryset_without_mage(self):
        """Test get_practice_queryset method without mage."""
        formset = PracticeRatingFormSet(instance=self.mage)
        queryset = formset.get_practice_queryset()

        # Should still return valid queryset excluding specialized/corrupted
        specialized = SpecializedPractice.objects.first()
        if specialized:
            self.assertNotIn(specialized, queryset)


class TestBasePracticeRatingFormSetWithSpecialized(TestCase):
    """Test BasePracticeRatingFormSet with specialized practices."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create faction with specialized practice
        self.faction = MageFaction.objects.create(name="Specialized Test Faction")
        self.parent_practice = Practice.objects.first()
        self.specialized = SpecializedPractice.objects.create(
            name="Faction Special",
            parent_practice=self.parent_practice,
            faction=self.faction,
        )

        self.mage = Mage.objects.create(
            name="Specialized Mage",
            owner=self.user,
            faction=self.faction,
        )

    def test_formset_includes_faction_specialized(self):
        """Test that formset includes specialized practice for mage's faction."""
        formset = PracticeRatingFormSet(instance=self.mage, mage=self.mage)
        queryset = formset.get_practice_queryset()

        self.assertIn(self.specialized, queryset)

    def test_formset_excludes_parent_when_specialized_exists(self):
        """Test that formset excludes parent practice when specialized exists."""
        formset = PracticeRatingFormSet(instance=self.mage, mage=self.mage)
        queryset = formset.get_practice_queryset()

        self.assertNotIn(self.parent_practice, queryset)


class TestPracticeRatingFormSetFactory(TestCase):
    """Test the PracticeRatingFormSet factory configuration."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
        )

    def test_formset_has_extra_forms(self):
        """Test that formset has extra forms for new entries."""
        formset = PracticeRatingFormSet(instance=self.mage)

        # Should have at least 1 extra form based on factory config
        self.assertGreaterEqual(len(formset.forms), 1)

    def test_formset_cannot_delete(self):
        """Test that formset is configured to not allow deletion."""
        formset = PracticeRatingFormSet(instance=self.mage)

        # Based on factory config, can_delete=False
        self.assertFalse(formset.can_delete)

    def test_formset_uses_correct_form_class(self):
        """Test that formset uses PracticeRatingForm."""
        formset = PracticeRatingFormSet(instance=self.mage)

        # Check that the form class name matches (comparing by name due to Django formset wrapper)
        self.assertEqual(formset.form.__name__, "PracticeRatingForm")

    def test_formset_queryset_ordered_by_name(self):
        """Test that practice queryset is ordered by name."""
        formset = PracticeRatingFormSet(instance=self.mage, mage=self.mage)
        queryset = formset.get_practice_queryset()

        names = list(queryset.values_list("name", flat=True))
        self.assertEqual(names, sorted(names))


class TestPracticeRatingFormValidation(TestCase):
    """Test PracticeRatingForm validation."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
        )
        self.practice = Practice.objects.exclude(
            polymorphic_ctype__model="specializedpractice"
        ).exclude(polymorphic_ctype__model="corruptedpractice").first()

    def test_form_valid_with_practice_and_rating(self):
        """Test that form is valid with practice and rating."""
        form = PracticeRatingForm(
            data={
                "practice": self.practice.pk,
                "rating": 2,
            },
            mage=self.mage,
        )

        self.assertTrue(form.is_valid())

    def test_form_invalid_with_rating_too_high(self):
        """Test that form is invalid with rating above 5."""
        form = PracticeRatingForm(
            data={
                "practice": self.practice.pk,
                "rating": 6,
            },
            mage=self.mage,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_form_invalid_with_negative_rating(self):
        """Test that form is invalid with negative rating."""
        form = PracticeRatingForm(
            data={
                "practice": self.practice.pk,
                "rating": -1,
            },
            mage=self.mage,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)
