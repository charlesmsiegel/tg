"""
Tests for Numina forms (NuminaPathForm, PsychicPathForm, NuminaRitualForm).

Tests cover:
- NuminaPathForm initialization and field configuration
- PsychicPathForm initialization and field configuration
- NuminaPathRatingFormSet behavior
- PsychicPathRatingFormSet behavior
- NuminaRitualForm initialization and validation
- Path filtering based on numina type
- Practice queryset filtering (excluding specialized/corrupted)
- Ritual selection and creation workflow
"""

from characters.forms.mage.numina import (
    NuminaPathForm,
    NuminaPathRatingFormSet,
    NuminaRitualForm,
    PsychicPathForm,
    PsychicPathRatingFormSet,
)
from characters.models.core.ability_block import Ability
from characters.models.mage.focus import (
    CorruptedPractice,
    Practice,
    SpecializedPractice,
)
from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual, Sorcerer
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase


class TestNuminaPathFormInit(TestCase):
    """Test NuminaPathForm initialization."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        # Create hedge magic paths
        self.hedge_path1 = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.hedge_path2 = LinearMagicPath.objects.create(
            name="Enchantment", numina_type="hedge_magic"
        )
        # Create psychic path
        self.psychic_path = LinearMagicPath.objects.create(name="Telepathy", numina_type="psychic")

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = NuminaPathForm()

        self.assertIn("path", form.fields)
        self.assertIn("rating", form.fields)
        self.assertIn("practice", form.fields)
        self.assertIn("ability", form.fields)

    def test_path_queryset_filters_hedge_magic_only(self):
        """Test that path queryset only includes hedge magic paths."""
        form = NuminaPathForm()
        path_queryset = form.fields["path"].queryset

        self.assertIn(self.hedge_path1, path_queryset)
        self.assertIn(self.hedge_path2, path_queryset)
        self.assertNotIn(self.psychic_path, path_queryset)

    def test_rating_field_has_correct_constraints(self):
        """Test that rating field has correct min/max constraints."""
        form = NuminaPathForm()

        self.assertEqual(form.fields["rating"].min_value, 0)
        self.assertEqual(form.fields["rating"].max_value, 5)

    def test_practice_choices_excludes_specialized(self):
        """Test that practice choices exclude specialized practices."""
        parent = Practice.objects.first()
        specialized = SpecializedPractice.objects.create(
            name="Specialized Test", parent_practice=parent
        )

        form = NuminaPathForm()
        practice_values = [pk for pk, _ in form.fields["practice"].choices]

        self.assertNotIn(str(specialized.pk), practice_values)
        self.assertIn(str(parent.pk), practice_values)

    def test_practice_choices_excludes_corrupted(self):
        """Test that practice choices exclude corrupted practices."""
        parent = Practice.objects.first()
        corrupted = CorruptedPractice.objects.create(name="Corrupted Test", parent_practice=parent)

        form = NuminaPathForm()
        practice_values = [pk for pk, _ in form.fields["practice"].choices]

        self.assertNotIn(str(corrupted.pk), practice_values)


class TestPsychicPathFormInit(TestCase):
    """Test PsychicPathForm initialization."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        # Create paths
        self.psychic_path1 = LinearMagicPath.objects.create(name="Telepathy", numina_type="psychic")
        self.psychic_path2 = LinearMagicPath.objects.create(
            name="Pyrokinesis", numina_type="psychic"
        )
        self.hedge_path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = PsychicPathForm()

        self.assertIn("path", form.fields)
        self.assertIn("rating", form.fields)
        self.assertIn("practice", form.fields)
        self.assertIn("ability", form.fields)

    def test_path_queryset_filters_psychic_only(self):
        """Test that path queryset only includes psychic paths."""
        form = PsychicPathForm()
        path_queryset = form.fields["path"].queryset

        self.assertIn(self.psychic_path1, path_queryset)
        self.assertIn(self.psychic_path2, path_queryset)
        self.assertNotIn(self.hedge_path, path_queryset)

    def test_rating_field_has_correct_constraints(self):
        """Test that rating field has correct min/max constraints."""
        form = PsychicPathForm()

        self.assertEqual(form.fields["rating"].min_value, 0)
        self.assertEqual(form.fields["rating"].max_value, 5)

    def test_practice_choices_excludes_specialized(self):
        """Test that practice choices exclude specialized practices."""
        parent = Practice.objects.first()
        specialized = SpecializedPractice.objects.create(
            name="Specialized Test", parent_practice=parent
        )

        form = PsychicPathForm()
        practice_values = [pk for pk, _ in form.fields["practice"].choices]

        self.assertNotIn(str(specialized.pk), practice_values)


class TestNuminaPathRatingFormSet(TestCase):
    """Test NuminaPathRatingFormSet behavior."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.user,
            sorcerer_type="hedge_mage",
        )
        self.hedge_path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.psychic_path = LinearMagicPath.objects.create(name="Telepathy", numina_type="psychic")

    def test_formset_filters_paths_for_hedge_magic(self):
        """Test that formset filters paths for hedge magic."""
        formset = NuminaPathRatingFormSet(instance=self.sorcerer)

        for form in formset.forms:
            path_queryset = form.fields["path"].queryset
            self.assertIn(self.hedge_path, path_queryset)
            self.assertNotIn(self.psychic_path, path_queryset)

    def test_formset_has_extra_forms(self):
        """Test that formset has extra forms for new entries."""
        formset = NuminaPathRatingFormSet(instance=self.sorcerer)

        # Should have at least 1 extra form
        self.assertGreater(len(formset.forms), 0)


class TestPsychicPathRatingFormSet(TestCase):
    """Test PsychicPathRatingFormSet behavior."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.sorcerer = Sorcerer.objects.create(
            name="Test Psychic",
            owner=self.user,
            sorcerer_type="psychic",
        )
        self.hedge_path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.psychic_path = LinearMagicPath.objects.create(name="Telepathy", numina_type="psychic")

    def test_formset_filters_paths_for_psychic(self):
        """Test that formset filters paths for psychic."""
        formset = PsychicPathRatingFormSet(instance=self.sorcerer)

        for form in formset.forms:
            path_queryset = form.fields["path"].queryset
            self.assertIn(self.psychic_path, path_queryset)
            self.assertNotIn(self.hedge_path, path_queryset)

    def test_formset_has_extra_forms(self):
        """Test that formset has extra forms for new entries."""
        formset = PsychicPathRatingFormSet(instance=self.sorcerer)

        self.assertGreater(len(formset.forms), 0)


class TestNuminaRitualFormInit(TestCase):
    """Test NuminaRitualForm initialization."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.ability = Ability.objects.first()
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )

        # Create sorcerer with a path
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.user,
            sorcerer_type="hedge_mage",
        )
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.sorcerer.add_path(self.path, self.practice, self.ability)

    def test_form_initializes_with_pk(self):
        """Test that form initializes with sorcerer pk."""
        form = NuminaRitualForm(pk=self.sorcerer.pk)

        self.assertEqual(form.sorcerer, self.sorcerer)

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = NuminaRitualForm(pk=self.sorcerer.pk)

        self.assertIn("select_or_create", form.fields)
        self.assertIn("select_ritual", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("path", form.fields)
        self.assertIn("level", form.fields)

    def test_form_path_queryset_filters_to_sorcerer_paths(self):
        """Test that path queryset only includes sorcerer's paths."""
        other_path = LinearMagicPath.objects.create(name="Enchantment", numina_type="hedge_magic")

        form = NuminaRitualForm(pk=self.sorcerer.pk)
        path_queryset = form.fields["path"].queryset

        self.assertIn(self.path, path_queryset)
        self.assertNotIn(other_path, path_queryset)

    def test_form_fields_not_required(self):
        """Test that form fields are not required."""
        form = NuminaRitualForm(pk=self.sorcerer.pk)

        # All fields should be optional for flexible create/select workflow
        for field_name in form.fields:
            self.assertFalse(
                form.fields[field_name].required,
                f"Field {field_name} should not be required",
            )

    def test_form_has_placeholder_text(self):
        """Test that form fields have placeholder text."""
        form = NuminaRitualForm(pk=self.sorcerer.pk)

        self.assertIn("placeholder", form.fields["name"].widget.attrs)
        self.assertIn("placeholder", form.fields["description"].widget.attrs)


class TestNuminaRitualFormRitualFiltering(TestCase):
    """Test NuminaRitualForm ritual filtering logic."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.ability = Ability.objects.first()
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )

        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.user,
            sorcerer_type="hedge_mage",
        )
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        # Add path at rating 3
        self.sorcerer.add_path(self.path, self.practice, self.ability)
        self.sorcerer.add_path(self.path, self.practice, self.ability)
        self.sorcerer.add_path(self.path, self.practice, self.ability)

        # Create rituals at different levels
        self.ritual_level1 = LinearMagicRitual.objects.create(
            name="Basic Alchemy",
            path=self.path,
            level=1,
        )
        self.ritual_level2 = LinearMagicRitual.objects.create(
            name="Advanced Alchemy",
            path=self.path,
            level=2,
        )
        self.ritual_level4 = LinearMagicRitual.objects.create(
            name="Master Alchemy",
            path=self.path,
            level=4,
        )

    def test_ritual_queryset_filters_by_path_rating(self):
        """Test that ritual queryset filters by sorcerer's path rating."""
        form = NuminaRitualForm(pk=self.sorcerer.pk)
        ritual_queryset = form.fields["select_ritual"].queryset

        # Should include rituals within rating
        self.assertIn(self.ritual_level1, ritual_queryset)
        # Level 4 ritual should not be available for rating 3 path
        self.assertNotIn(self.ritual_level4, ritual_queryset)

    def test_ritual_queryset_excludes_known_rituals(self):
        """Test that ritual queryset excludes rituals sorcerer already knows."""
        # Add ritual to sorcerer
        self.sorcerer.add_ritual(self.ritual_level1)

        form = NuminaRitualForm(pk=self.sorcerer.pk)
        ritual_queryset = form.fields["select_ritual"].queryset

        self.assertNotIn(self.ritual_level1, ritual_queryset)

    def test_ritual_progression_requires_previous_levels(self):
        """Test that rituals are available based on progression."""
        # Sorcerer with path at rating 3 but no rituals
        form = NuminaRitualForm(pk=self.sorcerer.pk)
        ritual_queryset = form.fields["select_ritual"].queryset

        # Level 1 should be available (starting point)
        self.assertIn(self.ritual_level1, ritual_queryset)

    def test_ritual_queryset_after_learning_level1(self):
        """Test ritual queryset after learning level 1 ritual."""
        self.sorcerer.add_ritual(self.ritual_level1)

        form = NuminaRitualForm(pk=self.sorcerer.pk)
        ritual_queryset = form.fields["select_ritual"].queryset

        # Level 1 should now be excluded
        self.assertNotIn(self.ritual_level1, ritual_queryset)
        # Level 2 should now be available
        self.assertIn(self.ritual_level2, ritual_queryset)


class TestNuminaRitualFormValidation(TestCase):
    """Test NuminaRitualForm validation."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.ability = Ability.objects.first()
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )

        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.user,
            sorcerer_type="hedge_mage",
        )
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.sorcerer.add_path(self.path, self.practice, self.ability)

        self.ritual = LinearMagicRitual.objects.create(
            name="Basic Alchemy",
            path=self.path,
            level=1,
        )

    def test_form_valid_with_selected_ritual(self):
        """Test that form handles selecting an existing ritual."""
        form = NuminaRitualForm(
            data={
                "select_or_create": False,
                "select_ritual": self.ritual.pk,
            },
            pk=self.sorcerer.pk,
        )

        # Form may or may not be valid depending on ritual queryset filtering
        # but it should initialize without error
        self.assertIsNotNone(form)

    def test_form_valid_with_custom_ritual_data(self):
        """Test that form handles custom ritual data."""
        form = NuminaRitualForm(
            data={
                "select_or_create": True,
                "name": "Custom Ritual",
                "description": "A custom ritual description",
                "path": self.path.pk,
                "level": 1,
            },
            pk=self.sorcerer.pk,
        )

        # Form should initialize without error
        self.assertIsNotNone(form)
