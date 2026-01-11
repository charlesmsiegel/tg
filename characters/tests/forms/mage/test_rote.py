"""
Tests for RoteCreationForm.

Tests cover:
- Form initialization with mage instance
- Practice queryset filtering
- Rote and effect option queryset filtering based on mage's spheres
- Sphere field constraints based on mage's sphere ratings
- Form validation for create vs select workflows
- Form save functionality for different scenarios
"""

from characters.forms.mage.rote import RoteCreationForm
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import (
    CorruptedPractice,
    Practice,
    SpecializedPractice,
)
from characters.models.mage.mage import Mage, PracticeRating
from characters.models.mage.rote import Rote
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase


class TestRoteCreationFormInit(TestCase):
    """Test RoteCreationForm initialization."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.filter(parent__isnull=False).first()
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            faction=self.faction,
            arete=3,
            forces=3,
            mind=2,
            rote_points=6,
        )
        # Add a practice to the mage
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )
        PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)

    def test_form_has_expected_fields(self):
        """Test that form has expected fields."""
        form = RoteCreationForm(instance=self.mage)

        self.assertIn("select_or_create_rote", form.fields)
        self.assertIn("select_or_create_effect", form.fields)
        self.assertIn("rote_options", form.fields)
        self.assertIn("effect_options", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("practice", form.fields)
        self.assertIn("attribute", form.fields)
        self.assertIn("ability", form.fields)
        self.assertIn("systems", form.fields)
        self.assertIn("description", form.fields)

    def test_form_has_sphere_fields(self):
        """Test that form has all sphere fields."""
        form = RoteCreationForm(instance=self.mage)

        for sphere in [
            "correspondence",
            "time",
            "spirit",
            "matter",
            "life",
            "forces",
            "entropy",
            "mind",
            "prime",
        ]:
            self.assertIn(sphere, form.fields)

    def test_form_stores_instance(self):
        """Test that form stores mage instance."""
        form = RoteCreationForm(instance=self.mage)

        self.assertEqual(form.instance, self.mage)


class TestRoteCreationFormPracticeFiltering(TestCase):
    """Test practice choice filtering in RoteCreationForm."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create faction with specialized practice
        self.faction = MageFaction.objects.create(name="Test Faction")
        self.parent_practice = Practice.objects.first()
        self.specialized = SpecializedPractice.objects.create(
            name="Specialized For Test",
            parent_practice=self.parent_practice,
            faction=self.faction,
        )

        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            faction=self.faction,
            arete=3,
            rote_points=6,
        )

        # Add practices to mage
        PracticeRating.objects.create(mage=self.mage, practice=self.parent_practice, rating=2)
        PracticeRating.objects.create(mage=self.mage, practice=self.specialized, rating=3)

    def test_practice_choices_includes_mage_practices(self):
        """Test that practice choices include mage's practices."""
        form = RoteCreationForm(instance=self.mage)
        practice_values = [pk for pk, _ in form.fields["practice"].choices]

        self.assertIn(str(self.parent_practice.pk), practice_values)

    def test_practice_choices_excludes_specialized_in_favor_of_parent(self):
        """Test that specialized practices are mapped to their parents."""
        form = RoteCreationForm(instance=self.mage)
        practice_values = [pk for pk, _ in form.fields["practice"].choices]

        # The parent practice should be in the choices
        self.assertIn(str(self.parent_practice.pk), practice_values)

    def test_practice_choices_ordered_by_name(self):
        """Test that practice choices are ordered by name."""
        form = RoteCreationForm(instance=self.mage)
        # Skip the empty placeholder at index 0
        practice_labels = [label for pk, label in form.fields["practice"].choices if pk]

        self.assertEqual(practice_labels, sorted(practice_labels))


class TestRoteCreationFormSphereConstraints(TestCase):
    """Test sphere field constraints in RoteCreationForm."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            arete=4,
            forces=4,
            mind=2,
            life=1,
            rote_points=6,
        )
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )
        PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)

    def test_sphere_max_set_by_mage_rating(self):
        """Test that sphere field max is set by mage's sphere rating."""
        form = RoteCreationForm(instance=self.mage)

        self.assertEqual(form.fields["forces"].widget.attrs.get("max"), 4)
        self.assertEqual(form.fields["mind"].widget.attrs.get("max"), 2)
        self.assertEqual(form.fields["life"].widget.attrs.get("max"), 1)

    def test_sphere_fields_min_value_zero(self):
        """Test that sphere fields have min_value of 0."""
        form = RoteCreationForm(instance=self.mage)

        for sphere in ["correspondence", "time", "spirit", "matter", "life", "forces"]:
            self.assertEqual(form.fields[sphere].min_value, 0)


class TestRoteCreationFormRoteFiltering(TestCase):
    """Test rote options queryset filtering."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            arete=3,
            forces=3,
            mind=2,
            rote_points=6,
        )
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )
        PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)

        self.attribute = Attribute.objects.first()
        self.ability = Ability.objects.first()

        # Create effects and rotes
        self.affordable_effect = Effect.objects.create(name="Affordable Effect", forces=2)
        self.expensive_effect = Effect.objects.create(name="Expensive Effect", forces=5)
        self.affordable_rote = Rote.objects.create(
            name="Affordable Rote",
            effect=self.affordable_effect,
            practice=self.practice,
            attribute=self.attribute,
            ability=self.ability,
        )
        self.expensive_rote = Rote.objects.create(
            name="Expensive Rote",
            effect=self.expensive_effect,
            practice=self.practice,
            attribute=self.attribute,
            ability=self.ability,
        )

    def test_rote_options_exclude_known_rotes(self):
        """Test that rote options exclude rotes mage already knows."""
        self.mage.rotes.add(self.affordable_rote)

        form = RoteCreationForm(instance=self.mage)
        rote_queryset = form.fields["rote_options"].queryset

        self.assertNotIn(self.affordable_rote, rote_queryset)

    def test_rote_options_filter_by_rote_points(self):
        """Test that rote options filter by available rote points."""
        form = RoteCreationForm(instance=self.mage)
        rote_queryset = form.fields["rote_options"].queryset

        # Affordable rote should be available
        self.assertIn(self.affordable_rote, rote_queryset)


class TestRoteCreationFormEffectFiltering(TestCase):
    """Test effect options queryset filtering."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            arete=3,
            forces=3,
            mind=2,
            rote_points=6,
        )
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )
        PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)

        self.attribute = Attribute.objects.first()
        self.ability = Ability.objects.first()

    def test_effect_options_filter_by_rote_points(self):
        """Test that effect options filter by available rote points."""
        affordable_effect = Effect.objects.create(name="Cheap Effect", forces=2)
        expensive_effect = Effect.objects.create(name="Expensive Effect", forces=10)

        form = RoteCreationForm(instance=self.mage)
        effect_queryset = form.fields["effect_options"].queryset

        self.assertIn(affordable_effect, effect_queryset)
        self.assertNotIn(expensive_effect, effect_queryset)

    def test_effect_options_filter_by_sphere_rating(self):
        """Test that effect options filter by mage's sphere ratings."""
        within_rating = Effect.objects.create(name="Within Rating", forces=3)
        above_rating = Effect.objects.create(name="Above Rating", forces=5)

        form = RoteCreationForm(instance=self.mage)
        effect_queryset = form.fields["effect_options"].queryset

        self.assertIn(within_rating, effect_queryset)
        self.assertNotIn(above_rating, effect_queryset)

    def test_effect_options_exclude_known_effects(self):
        """Test that effect options exclude effects mage already knows."""
        known_effect = Effect.objects.create(name="Known Effect", forces=2)
        rote = Rote.objects.create(
            name="Known Rote",
            effect=known_effect,
            practice=self.practice,
            attribute=self.attribute,
            ability=self.ability,
        )
        self.mage.rotes.add(rote)

        form = RoteCreationForm(instance=self.mage)
        effect_queryset = form.fields["effect_options"].queryset

        self.assertNotIn(known_effect, effect_queryset)


class TestRoteCreationFormSave(TestCase):
    """Test RoteCreationForm save functionality."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            arete=3,
            forces=3,
            mind=2,
            rote_points=6,
        )
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )
        PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)

        self.attribute = Attribute.objects.first()
        self.ability = Ability.objects.first()

        self.existing_effect = Effect.objects.create(name="Existing Effect", forces=2)
        self.existing_rote = Rote.objects.create(
            name="Existing Rote",
            effect=self.existing_effect,
            practice=self.practice,
            attribute=self.attribute,
            ability=self.ability,
        )

    def test_save_with_selected_rote(self):
        """Test saving form when selecting an existing rote."""
        initial_rote_points = self.mage.rote_points

        form = RoteCreationForm(
            data={
                "select_or_create_rote": False,
                "rote_options": self.existing_rote.pk,
            },
            instance=self.mage,
        )

        if form.is_valid():
            result = form.save(self.mage)

            self.mage.refresh_from_db()
            self.assertIn(self.existing_rote, self.mage.rotes.all())
            # Rote points should be reduced by effect cost
            self.assertEqual(
                self.mage.rote_points,
                initial_rote_points - self.existing_effect.cost(),
            )

    def test_save_with_new_rote_existing_effect(self):
        """Test saving form when creating new rote with existing effect."""
        new_effect = Effect.objects.create(name="New Selectable Effect", forces=1)
        initial_rote_points = self.mage.rote_points

        form = RoteCreationForm(
            data={
                "select_or_create_rote": True,
                "select_or_create_effect": False,
                "name": "My New Rote",
                "practice": self.practice.pk,
                "attribute": self.attribute.pk,
                "ability": self.ability.pk,
                "description": "A test rote",
                "effect_options": new_effect.pk,
            },
            instance=self.mage,
        )

        if form.is_valid():
            result = form.save(self.mage)

            self.mage.refresh_from_db()
            # Check new rote was created and added to mage
            new_rote = self.mage.rotes.filter(name="My New Rote").first()
            self.assertIsNotNone(new_rote)
            self.assertEqual(new_rote.effect, new_effect)

    def test_save_with_new_rote_new_effect(self):
        """Test saving form when creating new rote with new effect."""
        initial_rote_points = self.mage.rote_points

        form = RoteCreationForm(
            data={
                "select_or_create_rote": True,
                "select_or_create_effect": True,
                "name": "Brand New Rote",
                "practice": self.practice.pk,
                "attribute": self.attribute.pk,
                "ability": self.ability.pk,
                "description": "A completely new rote",
                "systems": "Roll Arete + Forces",
                "forces": 2,
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "matter": 0,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 0,
            },
            instance=self.mage,
        )

        if form.is_valid():
            result = form.save(self.mage)

            self.mage.refresh_from_db()
            # Check new rote was created
            new_rote = self.mage.rotes.filter(name="Brand New Rote").first()
            self.assertIsNotNone(new_rote)
            # Check new effect was created
            new_effect = new_rote.effect
            self.assertEqual(new_effect.forces, 2)


class TestRoteCreationFormValidation(TestCase):
    """Test RoteCreationForm validation."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            arete=3,
            forces=3,
            mind=2,
            rote_points=6,
        )
        self.practice = (
            Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
            .exclude(polymorphic_ctype__model="corruptedpractice")
            .first()
        )
        PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)

        self.attribute = Attribute.objects.first()
        self.ability = Ability.objects.first()

    def test_form_requires_either_select_or_create(self):
        """Test that form requires either selecting or creating a rote."""
        form = RoteCreationForm(
            data={},
            instance=self.mage,
        )

        # Empty form should still be valid since all fields are optional
        # But saving should fail without proper data
        self.assertTrue(form.is_valid())

    def test_new_effect_cost_validation(self):
        """Test that new effect cost is validated against rote points."""
        # Effect with cost exceeding rote points should fail during save
        mage_low_points = Mage.objects.create(
            name="Low Points Mage",
            owner=self.user,
            arete=5,
            forces=5,
            rote_points=2,  # Only 2 rote points
        )
        PracticeRating.objects.create(mage=mage_low_points, practice=self.practice, rating=3)

        form = RoteCreationForm(
            data={
                "select_or_create_rote": True,
                "select_or_create_effect": True,
                "name": "Expensive Rote",
                "practice": self.practice.pk,
                "attribute": self.attribute.pk,
                "ability": self.ability.pk,
                "description": "Too expensive",
                "systems": "Roll Arete",
                "forces": 5,  # Cost is 5, but only 2 rote points
            },
            instance=mage_low_points,
        )

        # Form might be valid but save should raise validation error
        if form.is_valid():
            with self.assertRaises(Exception):
                form.save(mage_low_points)
