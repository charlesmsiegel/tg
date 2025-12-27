"""Tests for background_block module."""

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase


class BackgroundBlockQueryTests(TestCase):
    """Tests for BackgroundBlock query optimization."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.character = Human.objects.create(name="Test Human", owner=self.user)
        self.background = Background.objects.create(name="Contacts", property_name="contacts")

    def test_total_background_rating_uses_aggregation(self):
        """Test that total_background_rating uses a single aggregated query."""
        # Create multiple background ratings
        BackgroundRating.objects.create(char=self.character, bg=self.background, rating=3)
        BackgroundRating.objects.create(
            char=self.character, bg=self.background, rating=2, note="Work"
        )

        # Verify the aggregation works correctly
        with self.assertNumQueries(1):
            total = self.character.total_background_rating("contacts")

        self.assertEqual(total, 5)

    def test_total_background_rating_returns_zero_for_no_ratings(self):
        """Test that total_background_rating returns 0 when no ratings exist."""
        total = self.character.total_background_rating("nonexistent")
        self.assertEqual(total, 0)

    def test_add_background_string_uses_optimized_query(self):
        """Test that add_background with string uses optimized query."""
        # First call creates the background, which needs multiple queries
        self.character.add_background("contacts")

        # Subsequent calls: get_or_create (1), filter/first (1), save (1) = 3 queries
        # This is optimal - no COUNT() query anymore
        with self.assertNumQueries(3):
            self.character.add_background("contacts")

    def test_add_background_object_uses_single_query(self):
        """Test that add_background with Background object uses optimized query."""
        # First call
        self.character.add_background(self.background)

        # Subsequent calls should use single query for finding rating
        with self.assertNumQueries(2):  # filter/first + save
            self.character.add_background(self.background)

    def test_add_background_returns_false_when_at_max(self):
        """Test add_background returns False when rating is already at 5."""
        BackgroundRating.objects.create(char=self.character, bg=self.background, rating=5)
        # Should create a new rating since existing one is at max
        result = self.character.add_background(self.background)
        self.assertTrue(result)

    def test_add_background_increments_existing_rating(self):
        """Test add_background increments an existing rating below 5."""
        rating = BackgroundRating.objects.create(char=self.character, bg=self.background, rating=2)
        self.character.add_background(self.background)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)

    def test_add_background_creates_new_when_all_at_max(self):
        """Test add_background creates new rating when all existing are at 5."""
        BackgroundRating.objects.create(char=self.character, bg=self.background, rating=5)
        initial_count = BackgroundRating.objects.filter(
            char=self.character, bg=self.background
        ).count()

        self.character.add_background(self.background)

        final_count = BackgroundRating.objects.filter(
            char=self.character, bg=self.background
        ).count()
        self.assertEqual(final_count, initial_count + 1)

    def test_add_background_invalid_type_raises_error(self):
        """Test add_background raises ValueError for invalid types."""
        with self.assertRaises(ValueError):
            self.character.add_background(123)
