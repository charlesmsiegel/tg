"""Tests for Wraith model."""

from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import ThornRating, Wraith
from django.contrib.auth.models import User
from django.test import TestCase


class ThornRatingDeleteBehaviorTests(TestCase):
    """Tests for ThornRating SET_NULL behavior when parent objects are deleted."""

    def setUp(self):
        """Create test user, wraith, thorn, and rating."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wraith = Wraith.objects.create(name="Test Wraith", owner=self.user)
        self.thorn = Thorn.objects.create(
            name="Shadow Call",
            point_cost=2,
            activation_cost="1 Angst",
            activation_trigger="When the Wraith experiences strong emotion",
            mechanical_description="The Shadow can speak through the Wraith",
            resistance_system="Willpower roll",
            duration="One scene",
            frequency_limitation="Once per session",
            limitations="Cannot be used in Harrowing",
        )
        self.rating = ThornRating.objects.create(wraith=self.wraith, thorn=self.thorn, rating=3)

    def test_deleting_wraith_sets_null_preserves_rating(self):
        """Deleting a Wraith should set wraith FK to NULL, not delete ThornRating."""
        rating_id = self.rating.id
        self.wraith.delete()

        # ThornRating should still exist
        self.assertTrue(ThornRating.objects.filter(id=rating_id).exists())

        # wraith FK should be NULL
        rating = ThornRating.objects.get(id=rating_id)
        self.assertIsNone(rating.wraith)
        self.assertEqual(rating.thorn, self.thorn)
        self.assertEqual(rating.rating, 3)

    def test_deleting_thorn_sets_null_preserves_rating(self):
        """Deleting a Thorn should set thorn FK to NULL, not delete ThornRating."""
        rating_id = self.rating.id
        self.thorn.delete()

        # ThornRating should still exist
        self.assertTrue(ThornRating.objects.filter(id=rating_id).exists())

        # thorn FK should be NULL
        rating = ThornRating.objects.get(id=rating_id)
        self.assertIsNone(rating.thorn)
        self.assertEqual(rating.wraith, self.wraith)
        self.assertEqual(rating.rating, 3)

    def test_related_name_thorn_ratings_on_wraith(self):
        """Wraith should have thorn_ratings related manager."""
        self.assertIn(self.rating, self.wraith.thorn_ratings.all())

    def test_related_name_wraith_ratings_on_thorn(self):
        """Thorn should have wraith_ratings related manager."""
        self.assertIn(self.rating, self.thorn.wraith_ratings.all())
