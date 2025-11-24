"""
Tests for core utility functions.

Tests cover:
- Dice rolling functions
- File path utilities
- Random selection utilities
"""
import os
import tempfile

from core.utils import dice, filepath
from django.test import TestCase


class TestDiceUtils(TestCase):
    """Test dice rolling utility functions."""

    def test_d10_returns_valid_result(self):
        """Test that d10() returns a value between 1 and 10."""
        for _ in range(100):
            result = dice.d10()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)

    def test_d6_returns_valid_result(self):
        """Test that d6() returns a value between 1 and 6."""
        for _ in range(100):
            result = dice.d6()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)

    def test_d20_returns_valid_result(self):
        """Test that d20() returns a value between 1 and 20."""
        for _ in range(100):
            result = dice.d20()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 20)

    def test_d100_returns_valid_result(self):
        """Test that d100() returns a value between 1 and 100."""
        for _ in range(100):
            result = dice.d100()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 100)

    def test_roll_returns_expected_count(self):
        """Test that roll() returns the correct number of results."""
        results = dice.roll(5, 10)
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)

    def test_roll_with_difficulty(self):
        """Test rolling dice with a difficulty threshold."""
        # Roll enough dice to likely get some successes
        results = dice.roll(10, 10, difficulty=6)
        # Results should all be valid d10 rolls
        for result in results:
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)

    def test_count_successes(self):
        """Test counting successes from a dice roll."""
        rolls = [1, 5, 7, 8, 10, 2, 6, 9]  # Some successes, some failures
        successes = dice.count_successes(rolls, difficulty=6)
        # Should count 7, 8, 10, 6, 9 as successes (5 total)
        self.assertEqual(successes, 5)

    def test_count_successes_with_botch(self):
        """Test counting successes with 1s (botches)."""
        rolls = [1, 1, 1]  # All 1s
        successes = dice.count_successes(rolls, difficulty=6)
        # Should be negative due to botches
        self.assertLess(successes, 0)

    def test_count_successes_tens_count_double(self):
        """Test that 10s count as 2 successes when specialty applies."""
        rolls = [10, 10, 8]
        # Without specialty: 10=1, 10=1, 8=1 = 3 successes
        successes_no_spec = dice.count_successes(rolls, difficulty=6, specialty=False)
        # With specialty: 10=2, 10=2, 8=1 = 5 successes
        successes_with_spec = dice.count_successes(rolls, difficulty=6, specialty=True)

        self.assertEqual(successes_no_spec, 3)
        self.assertEqual(successes_with_spec, 5)


class TestFilepathUtils(TestCase):
    """Test file path utility functions."""

    def test_character_image_upload_path(self):
        """Test that character image paths are generated correctly."""
        # Create a mock character object
        class MockCharacter:
            id = 123
            name = "Test Character"

        character = MockCharacter()
        filename = "portrait.jpg"

        path = filepath.character_image_upload(character, filename)

        # Should be in format: characters/123/portrait.jpg
        self.assertTrue(path.startswith("characters/"))
        self.assertTrue("123" in path)
        self.assertTrue(path.endswith(".jpg"))

    def test_item_image_upload_path(self):
        """Test that item image paths are generated correctly."""
        class MockItem:
            id = 456
            name = "Magic Sword"

        item = MockItem()
        filename = "sword.png"

        path = filepath.item_image_upload(item, filename)

        # Should be in format: items/456/sword.png
        self.assertTrue(path.startswith("items/"))
        self.assertTrue("456" in path)
        self.assertTrue(path.endswith(".png"))

    def test_location_image_upload_path(self):
        """Test that location image paths are generated correctly."""
        class MockLocation:
            id = 789
            name = "Castle"

        location = MockLocation()
        filename = "castle_photo.jpg"

        path = filepath.location_image_upload(location, filename)

        # Should be in format: locations/789/castle_photo.jpg
        self.assertTrue(path.startswith("locations/"))
        self.assertTrue("789" in path)
        self.assertTrue(path.endswith(".jpg"))

    def test_file_extension_preserved(self):
        """Test that file extensions are preserved in upload paths."""
        class MockObject:
            id = 1

        obj = MockObject()

        # Test various extensions
        extensions = [".jpg", ".png", ".gif", ".pdf", ".txt"]
        for ext in extensions:
            path = filepath.character_image_upload(obj, f"file{ext}")
            self.assertTrue(path.endswith(ext))


class TestRandomUtils(TestCase):
    """Test random selection utility functions."""

    def test_random_from_choices(self):
        """Test selecting a random item from a list."""
        choices = ["A", "B", "C", "D", "E"]

        # Run multiple times to ensure it's working
        for _ in range(50):
            result = dice.random_choice(choices)
            self.assertIn(result, choices)

    def test_random_from_weighted_choices(self):
        """Test selecting from weighted choices."""
        # 90% chance of "common", 10% chance of "rare"
        choices = {
            "common": 90,
            "rare": 10,
        }

        results = []
        for _ in range(100):
            result = dice.weighted_choice(choices)
            results.append(result)
            self.assertIn(result, ["common", "rare"])

        # Should get more "common" than "rare" (statistical test)
        common_count = results.count("common")
        rare_count = results.count("rare")
        self.assertGreater(common_count, rare_count)
