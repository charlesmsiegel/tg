"""Integration tests for the accounts app.

Tests cover signal handlers and cross-component interactions.
"""

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile


class TestProfileSignal(TestCase):
    """Test that Profile is automatically created when User is created."""

    def test_profile_created_on_user_creation(self):
        """Test that creating a user automatically creates a profile."""
        user = User.objects.create_user("testuser", "test@test.com", "password")
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.profile.user, user)

    def test_profile_has_default_values(self):
        """Test that new profile has correct default values."""
        user = User.objects.create_user("testuser", "test@test.com", "password")
        profile = user.profile
        self.assertEqual(profile.theme, "light")
        self.assertEqual(profile.preferred_heading, "wod_heading")
        self.assertTrue(profile.highlight_text)
        self.assertEqual(profile.discord_id, "")
        self.assertFalse(profile.discord_toggle)
        self.assertFalse(profile.lines_toggle)
        self.assertFalse(profile.veils_toggle)

    def test_multiple_users_get_separate_profiles(self):
        """Test that each user gets their own profile."""
        user1 = User.objects.create_user("user1", "user1@test.com", "password")
        user2 = User.objects.create_user("user2", "user2@test.com", "password")
        self.assertNotEqual(user1.profile.pk, user2.profile.pk)

    def test_profile_str_representation(self):
        """Test profile string representation."""
        user = User.objects.create_user("testuser", "test@test.com", "password")
        self.assertEqual(str(user.profile), "testuser")
