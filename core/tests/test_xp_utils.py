"""Tests for XP awarding utilities in core/xp_utils.py."""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.human import Human
from core.xp_utils import award_xp_atomically, calculate_story_xp
from game.models import Chronicle, Scene, Story
from locations.models import LocationModel


class CalculateStoryXPTests(TestCase):
    """Tests for calculate_story_xp utility function."""

    def test_all_categories_true(self):
        """All boolean categories true should sum correctly."""
        result = calculate_story_xp({
            "success": True,
            "danger": True,
            "growth": True,
            "drama": True,
            "duration": 2,
        })
        # 1 + 1 + 1 + 1 + 2 = 6
        self.assertEqual(result, 6)

    def test_all_categories_false(self):
        """All boolean categories false should return only duration."""
        result = calculate_story_xp({
            "success": False,
            "danger": False,
            "growth": False,
            "drama": False,
            "duration": 3,
        })
        self.assertEqual(result, 3)

    def test_empty_dict(self):
        """Empty dict should return 0."""
        result = calculate_story_xp({})
        self.assertEqual(result, 0)

    def test_missing_keys_default_to_safe_values(self):
        """Missing keys should default to 0 or False."""
        result = calculate_story_xp({"success": True})
        # Only success (1), all others default to 0/False
        self.assertEqual(result, 1)

    def test_partial_categories(self):
        """Partial category dict should calculate correctly."""
        result = calculate_story_xp({
            "success": True,
            "danger": False,
            "duration": 1,
        })
        # success (1) + duration (1) = 2
        self.assertEqual(result, 2)

    def test_zero_duration(self):
        """Zero duration should work correctly."""
        result = calculate_story_xp({
            "success": True,
            "danger": True,
            "growth": False,
            "drama": False,
            "duration": 0,
        })
        # success (1) + danger (1) = 2
        self.assertEqual(result, 2)

    def test_only_duration(self):
        """Only duration specified should return that value."""
        result = calculate_story_xp({"duration": 5})
        self.assertEqual(result, 5)

    def test_none_duration_causes_type_error(self):
        """Explicitly None duration raises TypeError (edge case).

        Note: This documents actual behavior. The function expects duration
        to be an int or omitted (defaults to 0 via .get()). Explicitly passing
        None is not a supported use case - callers should validate input.
        """
        with self.assertRaises(TypeError):
            calculate_story_xp({"success": True, "duration": None})


class AwardXPAtomicallyTests(TestCase):
    """Tests for award_xp_atomically utility function."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )

    def test_award_xp_to_single_character_via_story(self):
        """Test awarding XP to a single character via Story."""
        story = Story.objects.create(name="Test Story")
        character = Human.objects.create(
            name="Test Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )

        initial_xp = character.xp
        count = award_xp_atomically(Story, story.pk, {character: 5})

        character.refresh_from_db()
        story.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(character.xp, initial_xp + 5)
        self.assertTrue(story.xp_given)

    def test_award_xp_to_multiple_characters(self):
        """Test awarding different XP amounts to multiple characters."""
        story = Story.objects.create(name="Group Story")
        char1 = Human.objects.create(
            name="Hero 1",
            owner=self.user,
            chronicle=self.chronicle,
        )
        char2 = Human.objects.create(
            name="Hero 2",
            owner=self.user,
            chronicle=self.chronicle,
        )
        char3 = Human.objects.create(
            name="Hero 3",
            owner=self.user,
            chronicle=self.chronicle,
        )

        count = award_xp_atomically(Story, story.pk, {
            char1: 3,
            char2: 5,
            char3: 1,
        })

        char1.refresh_from_db()
        char2.refresh_from_db()
        char3.refresh_from_db()

        self.assertEqual(count, 3)
        self.assertEqual(char1.xp, 3)
        self.assertEqual(char2.xp, 5)
        self.assertEqual(char3.xp, 1)

    def test_award_xp_with_zero_amount_excluded_from_count(self):
        """Characters with 0 XP should not increment awarded_count."""
        story = Story.objects.create(name="Selective Story")
        char1 = Human.objects.create(
            name="Active Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )
        char2 = Human.objects.create(
            name="Inactive Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )

        count = award_xp_atomically(Story, story.pk, {
            char1: 3,
            char2: 0,  # Should not be counted
        })

        char1.refresh_from_db()
        char2.refresh_from_db()

        self.assertEqual(count, 1)  # Only char1 counted
        self.assertEqual(char1.xp, 3)
        self.assertEqual(char2.xp, 0)  # Unchanged

    def test_award_xp_empty_map_marks_complete(self):
        """Empty character map should still mark parent as complete."""
        story = Story.objects.create(name="Empty Story")

        count = award_xp_atomically(Story, story.pk, {})

        story.refresh_from_db()

        self.assertEqual(count, 0)
        self.assertTrue(story.xp_given)

    def test_award_xp_via_scene(self):
        """Test awarding XP via Scene model."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        character = Human.objects.create(
            name="Scene Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )

        initial_xp = character.xp
        count = award_xp_atomically(Scene, scene.pk, {character: 1})

        character.refresh_from_db()
        scene.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(character.xp, initial_xp + 1)
        self.assertTrue(scene.xp_given)

    def test_prevents_double_award_for_story(self):
        """Test that double-awarding raises ValidationError for Story."""
        story = Story.objects.create(name="One-Time Story")
        character = Human.objects.create(
            name="Test Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )

        award_xp_atomically(Story, story.pk, {character: 3})

        with self.assertRaises(ValidationError) as context:
            award_xp_atomically(Story, story.pk, {character: 2})

        self.assertEqual(context.exception.code, "xp_already_given")
        self.assertIn("story", str(context.exception).lower())

    def test_prevents_double_award_for_scene(self):
        """Test that double-awarding raises ValidationError for Scene."""
        scene = Scene.objects.create(
            name="One-Time Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        character = Human.objects.create(
            name="Test Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )

        award_xp_atomically(Scene, scene.pk, {character: 1})

        with self.assertRaises(ValidationError) as context:
            award_xp_atomically(Scene, scene.pk, {character: 1})

        self.assertEqual(context.exception.code, "xp_already_given")
        self.assertIn("scene", str(context.exception).lower())

    def test_all_zero_xp_still_marks_complete(self):
        """Map with all 0 XP should mark parent complete with 0 count."""
        story = Story.objects.create(name="No Reward Story")
        char1 = Human.objects.create(
            name="Hero 1",
            owner=self.user,
            chronicle=self.chronicle,
        )
        char2 = Human.objects.create(
            name="Hero 2",
            owner=self.user,
            chronicle=self.chronicle,
        )

        count = award_xp_atomically(Story, story.pk, {
            char1: 0,
            char2: 0,
        })

        story.refresh_from_db()

        self.assertEqual(count, 0)
        self.assertTrue(story.xp_given)

    def test_character_xp_accumulates(self):
        """Test that XP adds to existing character XP."""
        character = Human.objects.create(
            name="Experienced Hero",
            owner=self.user,
            chronicle=self.chronicle,
            xp=10,  # Starting with existing XP
        )
        story = Story.objects.create(name="Additional Story")

        award_xp_atomically(Story, story.pk, {character: 5})

        character.refresh_from_db()
        self.assertEqual(character.xp, 15)  # 10 + 5


class AwardXPAtomicallyEdgeCaseTests(TestCase):
    """Edge case tests for award_xp_atomically."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_nonexistent_parent_raises_error(self):
        """Attempting to award for nonexistent parent raises DoesNotExist."""
        character = Human.objects.create(
            name="Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )

        with self.assertRaises(Story.DoesNotExist):
            award_xp_atomically(Story, 99999, {character: 5})

    def test_large_xp_amount(self):
        """Test that large XP amounts work correctly."""
        story = Story.objects.create(name="Epic Story")
        character = Human.objects.create(
            name="Hero",
            owner=self.user,
            chronicle=self.chronicle,
        )

        award_xp_atomically(Story, story.pk, {character: 1000})

        character.refresh_from_db()
        self.assertEqual(character.xp, 1000)
