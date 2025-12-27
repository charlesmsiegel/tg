"""
Tests for core utility functions.

Tests cover:
- Dice rolling functions
- File path utilities
- Random selection utilities
"""

from unittest import mock
from unittest.mock import Mock

from characters.models.core import Human
from core.utils import dice, filepath, weighted_choice
from django.test import TestCase


class TestDiceUtils(TestCase):
    """Test dice rolling utility functions."""

    def test_dice_returns_tuple(self):
        """Test that dice() returns a tuple of (rolls, successes)."""
        rolls, successes = dice(5)
        self.assertIsInstance(rolls, list)
        self.assertIsInstance(successes, int)
        self.assertEqual(len(rolls), 5)

    def test_dice_rolls_valid_d10s(self):
        """Test that dice() returns valid d10 results."""
        for _ in range(50):
            rolls, _ = dice(5)
            for roll in rolls:
                self.assertGreaterEqual(roll, 1)
                self.assertLessEqual(roll, 10)

    def test_dice_with_difficulty(self):
        """Test dice rolling with custom difficulty."""
        mocker = Mock()
        mocker.side_effect = [4, 5, 6, 7, 8]
        with mock.patch("random.randint", mocker):
            rolls, successes = dice(5, difficulty=5)
            # 5, 6, 7, 8 are >= 5, so 4 successes
            self.assertEqual(successes, 4)

    def test_dice_botch(self):
        """Test that dice handles botches (all 1s with no successes)."""
        mocker = Mock()
        mocker.side_effect = [1, 1, 3, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            # 0 successes (3,4,5 < 6), 2 ones = -2
            self.assertEqual(successes, -2)

    def test_dice_failure_with_ones(self):
        """Test failure with ones that cancel successes."""
        mocker = Mock()
        mocker.side_effect = [1, 1, 7, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            # 1 success (7), 2 ones, but successes > 0 so capped at 0
            self.assertEqual(successes, 0)

    def test_dice_success(self):
        """Test successful dice roll."""
        mocker = Mock()
        mocker.side_effect = [6, 7, 3, 4, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            # 6, 7 are successes
            self.assertEqual(successes, 2)

    def test_dice_specialty(self):
        """Test that specialty doubles 10s."""
        mocker = Mock()
        mocker.side_effect = [10, 10, 3, 6, 5]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5, specialty=True)
            # 10, 10, 6 are successes = 3, plus 2 extra for specialty = 5
            self.assertEqual(successes, 5)

    def test_dice_default_difficulty(self):
        """Test that default difficulty is 6."""
        mocker = Mock()
        mocker.side_effect = [5, 6, 7, 8, 9]
        with mock.patch("random.randint", mocker):
            _, successes = dice(5)
            # 6, 7, 8, 9 are >= 6, so 4 successes
            self.assertEqual(successes, 4)

    def test_dice_empty_pool(self):
        """Test dice with zero dice pool."""
        rolls, successes = dice(0)
        self.assertEqual(len(rolls), 0)
        self.assertEqual(successes, 0)


class TestFilepathUtils(TestCase):
    """Test file path utility functions."""

    def test_filepath_basic(self):
        """Test basic filepath generation."""
        human = Human.objects.create(name="Test Character")
        path = filepath(human, "portrait.jpg")

        # Should contain the model path and filename
        self.assertTrue(path.endswith(".jpg"))
        self.assertIn("test_character", path)  # Name is lowercased and spaces replaced

    def test_filepath_preserves_extension(self):
        """Test that file extensions are preserved."""
        human = Human.objects.create(name="Test")

        extensions = [".jpg", ".png", ".gif", ".pdf"]
        for ext in extensions:
            path = filepath(human, f"file{ext}")
            self.assertTrue(path.endswith(ext), f"Expected path to end with {ext}, got {path}")

    def test_filepath_sanitizes_path_traversal(self):
        """Test that path traversal attempts are sanitized."""
        human = Human.objects.create(name="../../etc/passwd")
        path = filepath(human, "test.jpg")
        self.assertNotIn("..", path)
        self.assertNotIn("/etc/", path)

    def test_filepath_sanitizes_slashes(self):
        """Test that slashes in names are replaced."""
        human = Human.objects.create(name="path/to/evil")
        path = filepath(human, "test.jpg")
        # Only the model path should have slashes, not the name part
        # The name "path/to/evil" should become "path_to_evil"
        self.assertIn("path_to_evil", path)


class TestWeightedChoice(TestCase):
    """Test weighted_choice utility function."""

    def test_weighted_choice_returns_valid_key(self):
        """Test that weighted_choice returns a valid key."""
        choices = {"a": 3, "b": 2, "c": 1}
        for _ in range(50):
            result = weighted_choice(choices)
            self.assertIn(result, choices.keys())

    def test_weighted_choice_respects_weights(self):
        """Test that weighted_choice respects weight distribution."""
        # Higher weight should appear more often
        choices = {"common": 5, "rare": 0}
        results = [weighted_choice(choices) for _ in range(100)]
        common_count = results.count("common")
        rare_count = results.count("rare")
        # With weight 5 vs 0, common should dominate
        self.assertGreater(common_count, rare_count)


class TestNewsItemStr(TestCase):
    """Test NewsItem __str__ method."""

    def test_newsitem_str_returns_title(self):
        """Test NewsItem __str__ returns the title."""
        from core.models import NewsItem

        news = NewsItem.objects.create(
            title="Important Announcement",
            content="This is the content of the news item.",
        )

        self.assertEqual(str(news), "Important Announcement")

    def test_newsitem_str_with_empty_title(self):
        """Test NewsItem __str__ with empty title."""
        from core.models import NewsItem

        # Create with empty title (validation will fail, so don't save)
        news = NewsItem(
            title="",
            content="Content here",
        )

        # __str__ should still work and return empty string
        self.assertEqual(str(news), "")
