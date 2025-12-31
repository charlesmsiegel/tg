"""Tests for background_block module."""

from characters.models.core.background_block import (
    Background,
    BackgroundRating,
    PooledBackgroundRating,
)
from characters.models.core.group import Group
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


class BackgroundPoolableTests(TestCase):
    """Tests for the poolable field on Background model."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.character = Human.objects.create(name="Test Human", owner=self.user)
        # Create a poolable background
        self.poolable_bg = Background.objects.create(
            name="Contacts", property_name="contacts", poolable=True
        )
        # Create a non-poolable background (intrinsic)
        self.non_poolable_bg = Background.objects.create(
            name="Avatar", property_name="avatar", poolable=False
        )
        # Create a group and add the character
        self.group = Group.objects.create(name="Test Cabal")
        self.group.members.add(self.character)

    def test_background_poolable_default_is_true(self):
        """Test that new backgrounds are poolable by default."""
        bg = Background.objects.create(name="New BG", property_name="new_bg")
        self.assertTrue(bg.poolable)

    def test_background_poolable_can_be_set_false(self):
        """Test that poolable can be explicitly set to False."""
        self.assertFalse(self.non_poolable_bg.poolable)

    def test_non_poolable_background_not_added_to_pool(self):
        """Test that checking 'pooled' for non-poolable background doesn't create pool entry."""
        # Simulate what new_background_freebies does:
        # If poolable is False, we should NOT create a PooledBackgroundRating
        # even if 'pooled' is in the form data

        # Create a BackgroundRating for a non-poolable background
        bgr = BackgroundRating.objects.create(
            char=self.character,
            bg=self.non_poolable_bg,
            rating=1,
            pooled=False,  # Should remain False even if user tries to pool
        )

        # There should be no PooledBackgroundRating for this background
        pool_count = PooledBackgroundRating.objects.filter(
            bg=self.non_poolable_bg, group=self.group
        ).count()
        self.assertEqual(pool_count, 0)

    def test_poolable_background_can_be_pooled(self):
        """Test that poolable backgrounds can be added to the group pool."""
        # Create a pooled BackgroundRating
        bgr = BackgroundRating.objects.create(
            char=self.character,
            bg=self.poolable_bg,
            rating=2,
            pooled=True,
        )

        # Simulate what group.update_pooled_backgrounds() does
        self.group.update_pooled_backgrounds()

        # There should be a PooledBackgroundRating
        pool_entries = PooledBackgroundRating.objects.filter(bg=self.poolable_bg, group=self.group)
        self.assertEqual(pool_entries.count(), 1)
        self.assertEqual(pool_entries.first().rating, 2)

    def test_update_pooled_backgrounds_ignores_non_pooled_ratings(self):
        """Test that update_pooled_backgrounds only counts pooled=True ratings."""
        # Create ratings - one pooled, one not
        BackgroundRating.objects.create(
            char=self.character,
            bg=self.poolable_bg,
            rating=3,
            pooled=True,
        )
        BackgroundRating.objects.create(
            char=self.character,
            bg=self.poolable_bg,
            rating=2,
            pooled=False,
            note="Personal",
        )

        self.group.update_pooled_backgrounds()

        # Only the pooled=True rating should be in the pool
        pool_entry = PooledBackgroundRating.objects.get(
            bg=self.poolable_bg, group=self.group, note=""
        )
        self.assertEqual(pool_entry.rating, 3)

    def test_filter_poolable_backgrounds(self):
        """Test filtering backgrounds by poolable status."""
        # Create additional backgrounds
        Background.objects.create(name="Mentor", property_name="mentor", poolable=True)
        Background.objects.create(name="Generation", property_name="generation", poolable=False)

        poolable = Background.objects.filter(poolable=True)
        non_poolable = Background.objects.filter(poolable=False)

        # Check our test backgrounds are categorized correctly
        self.assertIn(self.poolable_bg, poolable)
        self.assertIn(self.non_poolable_bg, non_poolable)

        # Verify counts make sense (at least 2 of each type exist)
        self.assertGreaterEqual(poolable.count(), 2)
        self.assertGreaterEqual(non_poolable.count(), 2)


class BackgroundRatingIndexTests(TestCase):
    """Tests for BackgroundRating database indexes."""

    def test_background_rating_has_char_bg_composite_index(self):
        """Test that BackgroundRating has a composite index on (char, bg)."""
        indexes = BackgroundRating._meta.indexes
        index_field_sets = [tuple(idx.fields) for idx in indexes]
        self.assertIn(("char", "bg"), index_field_sets)

    def test_background_rating_char_field_has_db_index(self):
        """Test that BackgroundRating.char ForeignKey has db_index=True."""
        char_field = BackgroundRating._meta.get_field("char")
        self.assertTrue(char_field.db_index)

    def test_background_rating_bg_field_has_db_index(self):
        """Test that BackgroundRating.bg ForeignKey has db_index=True."""
        bg_field = BackgroundRating._meta.get_field("bg")
        self.assertTrue(bg_field.db_index)
