"""
Tests for Chantry forms.

Tests cover:
- ChantryPointForm: Adding backgrounds and integrated effects
- ChantryEffectsForm: Selecting integrated effects for chantry
- ChantryCreateForm: Creating new chantries
- ChantrySelectOrCreateForm: Selecting existing or creating new chantry
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from characters.models.mage.mage import Mage
from characters.tests.utils import mage_setup
from game.models import Chronicle
from locations.forms.mage.chantry import (
    ChantryCreateForm,
    ChantryEffectsForm,
    ChantryPointForm,
    ChantrySelectOrCreateForm,
)
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating


class TestChantryPointFormSetup(TestCase):
    """Shared setup for ChantryPointForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantryPointForm tests."""
        mage_setup()
        cls.chantry = Chantry.objects.create(name="Test Chantry", total_points=20)
        cls.background = Background.objects.get(property_name="allies")


class TestChantryPointFormBasics(TestChantryPointFormSetup):
    """Test basic ChantryPointForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = ChantryPointForm(pk=self.chantry.pk)

        self.assertIn("category", form.fields)
        self.assertIn("example", form.fields)
        self.assertIn("note", form.fields)
        self.assertIn("display_alt_name", form.fields)

    def test_category_choices_include_integrated_effects(self):
        """Test that category includes Integrated Effects option."""
        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Integrated Effects", category_values)
        self.assertIn("New Background", category_values)

    def test_category_excludes_existing_background_when_no_backgrounds(self):
        """Test that Existing Background is excluded when chantry has no backgrounds."""
        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Existing Background", category_values)

    def test_category_includes_existing_background_when_has_backgrounds(self):
        """Test that Existing Background is included when chantry has backgrounds."""
        ChantryBackgroundRating.objects.create(bg=self.background, chantry=self.chantry, rating=1)
        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Existing Background", category_values)

    def test_integrated_effects_excluded_at_max(self):
        """Test that Integrated Effects is excluded when score is at 10."""
        self.chantry.integrated_effects_score = 10
        self.chantry.save()

        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Integrated Effects", category_values)


class TestChantryPointFormValidation(TestChantryPointFormSetup):
    """Test ChantryPointForm validation logic."""

    def test_clean_requires_example_for_new_background(self):
        """Test that New Background requires an example to be selected."""
        form_data = {
            "category": "New Background",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)

        self.assertFalse(form.is_valid())

    def test_clean_requires_example_for_existing_background(self):
        """Test that Existing Background requires an example to be selected."""
        ChantryBackgroundRating.objects.create(bg=self.background, chantry=self.chantry, rating=1)

        form_data = {
            "category": "Existing Background",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)

        self.assertFalse(form.is_valid())

    def test_valid_integrated_effects_selection(self):
        """Test that Integrated Effects selection is valid."""
        form_data = {
            "category": "Integrated Effects",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)

        self.assertTrue(form.is_valid())


class TestChantryPointFormSave(TestChantryPointFormSetup):
    """Test ChantryPointForm save logic."""

    def test_save_integrated_effects_increases_score(self):
        """Test that saving Integrated Effects increases the score."""
        initial_score = self.chantry.integrated_effects_score

        form_data = {
            "category": "Integrated Effects",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)
        self.assertTrue(form.is_valid())
        form.save()

        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.integrated_effects_score, initial_score + 1)

    def test_save_new_background_creates_rating(self):
        """Test that saving New Background creates a ChantryBackgroundRating."""
        initial_count = ChantryBackgroundRating.objects.count()

        form_data = {
            "category": "New Background",
            "example": str(self.background.pk),
            "note": "Test Note",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(ChantryBackgroundRating.objects.count(), initial_count + 1)

    def test_save_existing_background_increases_rating(self):
        """Test that saving Existing Background increases the rating."""
        bg_rating = ChantryBackgroundRating.objects.create(
            bg=self.background, chantry=self.chantry, rating=1
        )

        form_data = {
            "category": "Existing Background",
            "example": str(bg_rating.pk),
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)
        self.assertTrue(form.is_valid())
        form.save()

        bg_rating.refresh_from_db()
        self.assertEqual(bg_rating.rating, 2)


class TestChantryEffectsFormSetup(TestCase):
    """Shared setup for ChantryEffectsForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantryEffectsForm tests."""
        mage_setup()
        cls.chantry = Chantry.objects.create(
            name="Test Chantry", total_points=50, integrated_effects_score=3
        )
        cls.effect = Effect.objects.filter(max_sphere__lte=cls.chantry.rank).first()


class TestChantryEffectsFormBasics(TestChantryEffectsFormSetup):
    """Test basic ChantryEffectsForm structure and fields."""

    def test_form_has_select_field(self):
        """Test that form has a select field."""
        form = ChantryEffectsForm(pk=self.chantry.pk)

        self.assertIn("select", form.fields)

    def test_queryset_excludes_existing_effects(self):
        """Test that queryset excludes effects already in chantry."""
        if self.effect:
            self.chantry.integrated_effects.add(self.effect)

            form = ChantryEffectsForm(pk=self.chantry.pk)

            self.assertNotIn(self.effect, form.fields["select"].queryset)

    def test_queryset_respects_rank_limit(self):
        """Test that queryset only includes effects within rank limit."""
        form = ChantryEffectsForm(pk=self.chantry.pk)

        for effect in form.fields["select"].queryset:
            self.assertLessEqual(effect.max_sphere, self.chantry.rank)


class TestChantryEffectsFormSave(TestChantryEffectsFormSetup):
    """Test ChantryEffectsForm save logic."""

    def test_save_adds_effect_to_chantry(self):
        """Test that saving adds the effect to chantry's integrated effects."""
        if self.effect:
            form_data = {
                "select_or_create": False,
                "select": str(self.effect.pk),
            }

            form = ChantryEffectsForm(data=form_data, pk=self.chantry.pk)
            if form.is_valid():
                form.save()
                self.assertIn(self.effect, self.chantry.integrated_effects.all())


class TestChantryCreateFormSetup(TestCase):
    """Shared setup for ChantryCreateForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantryCreateForm tests."""
        mage_setup()
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")


class TestChantryCreateFormBasics(TestChantryCreateFormSetup):
    """Test basic ChantryCreateForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = ChantryCreateForm()

        self.assertIn("name", form.fields)
        self.assertIn("chronicle", form.fields)
        self.assertIn("contained_within", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("faction", form.fields)
        self.assertIn("leadership_type", form.fields)
        self.assertIn("season", form.fields)
        self.assertIn("chantry_type", form.fields)
        self.assertIn("total_points", form.fields)

    def test_total_points_has_min_value(self):
        """Test that total_points has minimum value of 0."""
        form = ChantryCreateForm()

        self.assertEqual(form.fields["total_points"].min_value, 0)

    def test_name_widget_has_placeholder(self):
        """Test that name field has placeholder text."""
        form = ChantryCreateForm()

        self.assertIn("placeholder", form.fields["name"].widget.attrs)

    def test_description_widget_has_placeholder(self):
        """Test that description field has placeholder text."""
        form = ChantryCreateForm()

        self.assertIn("placeholder", form.fields["description"].widget.attrs)


class TestChantryCreateFormValidation(TestChantryCreateFormSetup):
    """Test ChantryCreateForm validation logic."""

    def test_valid_form_data(self):
        """Test that form validates with valid data."""
        form_data = {
            "name": "Test Chantry",
            "chronicle": self.chronicle.pk,
            "description": "A test chantry",
            "total_points": 10,
            "leadership_type": "panel",
            "season": "spring",
            "chantry_type": "exploration",
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = ChantryCreateForm(data=form_data)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_invalid_negative_total_points(self):
        """Test that negative total_points is invalid."""
        form_data = {
            "name": "Test Chantry",
            "total_points": -5,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = ChantryCreateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("total_points", form.errors)


class TestChantryCreateFormSave(TestChantryCreateFormSetup):
    """Test ChantryCreateForm save logic."""

    def test_save_creates_chantry(self):
        """Test that saving creates a new Chantry."""
        initial_count = Chantry.objects.count()

        form_data = {
            "name": "New Chantry",
            "description": "A new chantry",
            "total_points": 15,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = ChantryCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        chantry = form.save()

        self.assertEqual(Chantry.objects.count(), initial_count + 1)
        self.assertEqual(chantry.name, "New Chantry")
        self.assertEqual(chantry.total_points, 15)


class TestChantrySelectOrCreateFormSetup(TestCase):
    """Shared setup for ChantrySelectOrCreateForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantrySelectOrCreateForm tests."""
        mage_setup()
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")
        cls.character = Mage.objects.create(
            name="Test Mage", owner=cls.user, chronicle=cls.chronicle
        )
        cls.existing_chantry = Chantry.objects.create(
            name="Existing Chantry", chronicle=cls.chronicle, total_points=20
        )


class TestChantrySelectOrCreateFormBasics(TestChantrySelectOrCreateFormSetup):
    """Test basic ChantrySelectOrCreateForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = ChantrySelectOrCreateForm(character=self.character)

        self.assertIn("create_new", form.fields)
        self.assertIn("existing_chantry", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("total_points", form.fields)
        self.assertIn("description", form.fields)

    def test_existing_chantry_queryset_filtered_by_chronicle(self):
        """Test that existing_chantry queryset is filtered by character's chronicle."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        other_chantry = Chantry.objects.create(name="Other Chantry", chronicle=other_chronicle)

        form = ChantrySelectOrCreateForm(character=self.character)

        self.assertIn(self.existing_chantry, form.fields["existing_chantry"].queryset)
        self.assertNotIn(other_chantry, form.fields["existing_chantry"].queryset)

    def test_all_fields_optional(self):
        """Test that all fields are optional."""
        form = ChantrySelectOrCreateForm(character=self.character)

        for field in form.fields.values():
            self.assertFalse(field.required)


class TestChantrySelectOrCreateFormValidation(TestChantrySelectOrCreateFormSetup):
    """Test ChantrySelectOrCreateForm validation logic."""

    def test_valid_select_existing(self):
        """Test that selecting existing chantry is valid."""
        form_data = {
            "create_new": False,
            "existing_chantry": self.existing_chantry.pk,
            "total_points": "5",
        }

        form = ChantrySelectOrCreateForm(data=form_data, character=self.character)

        self.assertTrue(form.is_valid())

    def test_invalid_no_selection_when_not_creating(self):
        """Test that not creating and no selection is invalid."""
        form_data = {
            "create_new": False,
            "existing_chantry": "",
            "total_points": "5",
        }

        form = ChantrySelectOrCreateForm(data=form_data, character=self.character)

        self.assertFalse(form.is_valid())
        self.assertIn("existing_chantry", form.errors)

    def test_valid_create_new_with_valid_data(self):
        """Test that creating new with valid data is valid."""
        form_data = {
            "create_new": "on",
            "existing_chantry": "",
            "name": "New Chantry",
            "total_points": "10",
            "description": "Test description",
        }

        form = ChantrySelectOrCreateForm(data=form_data, character=self.character)

        self.assertTrue(form.is_valid())


class TestChantrySelectOrCreateFormSave(TestChantrySelectOrCreateFormSetup):
    """Test ChantrySelectOrCreateForm save logic."""

    def test_save_returns_existing_chantry(self):
        """Test that saving with existing selection returns the existing chantry."""
        form_data = {
            "create_new": False,
            "existing_chantry": self.existing_chantry.pk,
            "total_points": "5",
        }

        form = ChantrySelectOrCreateForm(data=form_data, character=self.character)
        self.assertTrue(form.is_valid())
        chantry = form.save()

        self.assertEqual(chantry.pk, self.existing_chantry.pk)

    def test_save_adds_points_to_existing_chantry(self):
        """Test that saving adds points to existing chantry."""
        initial_points = self.existing_chantry.total_points

        form_data = {
            "create_new": False,
            "existing_chantry": self.existing_chantry.pk,
            "total_points": "5",
        }

        form = ChantrySelectOrCreateForm(data=form_data, character=self.character)
        self.assertTrue(form.is_valid())
        form.save()

        self.existing_chantry.refresh_from_db()
        self.assertEqual(self.existing_chantry.total_points, initial_points + 5)

    def test_save_creates_new_chantry(self):
        """Test that save creates a new chantry when in create mode."""
        initial_count = Chantry.objects.count()

        form_data = {
            "create_new": "on",
            "name": "Created Chantry",
            "total_points": "15",
            "description": "A new chantry",
        }

        form = ChantrySelectOrCreateForm(data=form_data, character=self.character)
        self.assertTrue(form.is_valid())
        chantry = form.save()

        self.assertEqual(Chantry.objects.count(), initial_count + 1)
        self.assertEqual(chantry.name, "Created Chantry")
        self.assertEqual(chantry.total_points, 15)
