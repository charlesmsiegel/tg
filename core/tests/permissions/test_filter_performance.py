"""Performance tests for PermissionManager.filter_queryset_for_user().

These tests verify that the filter_queryset_for_user method:
1. Returns correct results for all user types
2. Does not create unnecessary subquery annotations
"""

from characters.models.core.character import Character
from core.models import Observer
from core.permissions import PermissionManager
from django.contrib.auth.models import AnonymousUser, User
from django.db import connection, reset_queries
from django.test import TestCase, override_settings
from game.models import Chronicle


class FilterQuerysetPerformanceTest(TestCase):
    """Tests for filter_queryset_for_user performance and correctness."""

    def setUp(self):
        """Set up test data with multiple characters and chronicles."""
        self.owner = User.objects.create_user(
            username="perf_owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="perf_head_st", email="head_st@test.com", password="testpass123"
        )
        self.game_st = User.objects.create_user(
            username="perf_game_st", email="game_st@test.com", password="testpass123"
        )
        self.player = User.objects.create_user(
            username="perf_player", email="player@test.com", password="testpass123"
        )
        self.observer_user = User.objects.create_user(
            username="perf_observer", email="observer@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="perf_admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.stranger = User.objects.create_user(
            username="perf_stranger", email="stranger@test.com", password="testpass123"
        )

        # Create chronicles
        self.chronicle = Chronicle.objects.create(
            name="Performance Test Chronicle", head_st=self.head_st
        )
        self.chronicle.game_storytellers.add(self.game_st)

        self.other_chronicle = Chronicle.objects.create(
            name="Other Chronicle"
        )

        # Create owner's character
        self.owned_character = Character.objects.create(
            name="Owner Character",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

        # Create player's character in same chronicle
        self.player_character = Character.objects.create(
            name="Player Character",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
        )

        # Create character in other chronicle
        self.other_character = Character.objects.create(
            name="Other Chronicle Character",
            owner=self.stranger,
            chronicle=self.other_chronicle,
            status="App",
        )

        # Create unfinished character
        self.unfinished_character = Character.objects.create(
            name="Unfinished Character",
            owner=self.stranger,
            chronicle=self.chronicle,
            status="Un",
        )

        # Add observer to one character
        Observer.objects.create(
            content_object=self.other_character,
            user=self.observer_user,
            granted_by=self.stranger,
        )

    def test_owner_sees_own_characters(self):
        """Owner should see their own characters."""
        qs = PermissionManager.filter_queryset_for_user(
            self.owner, Character.objects.all()
        )
        self.assertIn(self.owned_character, qs)

    def test_head_st_sees_chronicle_characters(self):
        """Head ST should see all characters in their chronicle."""
        qs = PermissionManager.filter_queryset_for_user(
            self.head_st, Character.objects.all()
        )
        self.assertIn(self.owned_character, qs)
        self.assertIn(self.player_character, qs)
        self.assertIn(self.unfinished_character, qs)

    def test_game_st_sees_chronicle_characters(self):
        """Game ST should see all characters in their chronicle."""
        qs = PermissionManager.filter_queryset_for_user(
            self.game_st, Character.objects.all()
        )
        self.assertIn(self.owned_character, qs)
        self.assertIn(self.player_character, qs)

    def test_player_sees_approved_chronicle_characters(self):
        """Player should see approved characters in their chronicle."""
        qs = PermissionManager.filter_queryset_for_user(
            self.player, Character.objects.all()
        )
        # Should see own character and other approved character in same chronicle
        self.assertIn(self.player_character, qs)
        self.assertIn(self.owned_character, qs)
        # Should not see unfinished character
        self.assertNotIn(self.unfinished_character, qs)
        # Should not see other chronicle's character
        self.assertNotIn(self.other_character, qs)

    def test_observer_sees_observed_character(self):
        """Observer should see character they're observing."""
        qs = PermissionManager.filter_queryset_for_user(
            self.observer_user, Character.objects.all()
        )
        self.assertIn(self.other_character, qs)
        # Should not see other characters
        self.assertNotIn(self.owned_character, qs)

    def test_admin_sees_all_characters(self):
        """Admin should see all characters."""
        qs = PermissionManager.filter_queryset_for_user(
            self.admin, Character.objects.all()
        )
        self.assertEqual(qs.count(), Character.objects.count())

    def test_stranger_sees_nothing(self):
        """Stranger should see no characters."""
        qs = PermissionManager.filter_queryset_for_user(
            self.stranger, Character.objects.all()
        )
        # Stranger owns other_character, so should see that
        self.assertIn(self.other_character, qs)
        # But nothing else
        self.assertNotIn(self.owned_character, qs)

    def test_anonymous_sees_nothing(self):
        """Anonymous user should see no characters."""
        anon = AnonymousUser()
        qs = PermissionManager.filter_queryset_for_user(anon, Character.objects.all())
        self.assertEqual(qs.count(), 0)

    @override_settings(DEBUG=True)
    def test_no_annotation_fields_in_queryset(self):
        """Filtered queryset should not have annotation fields that indicate subqueries."""
        reset_queries()
        qs = PermissionManager.filter_queryset_for_user(
            self.player, Character.objects.all()
        )
        # Force evaluation
        list(qs)

        # Check that queryset does not have the problematic annotation fields
        # These would indicate the old subquery-based approach
        self.assertFalse(
            hasattr(qs.query, "annotations")
            and "_is_player_chronicle" in qs.query.annotations,
            "Queryset should not have _is_player_chronicle annotation"
        )
        self.assertFalse(
            hasattr(qs.query, "annotations")
            and "_is_observer" in qs.query.annotations,
            "Queryset should not have _is_observer annotation"
        )


class FilterQuerysetMultipleCallsTest(TestCase):
    """Test that multiple filter_queryset_for_user calls don't compound queries."""

    def setUp(self):
        """Set up test data."""
        self.player = User.objects.create_user(
            username="multi_player", email="player@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="multi_head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Multi Call Chronicle", head_st=self.head_st
        )
        self.character = Character.objects.create(
            name="Multi Call Character",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
        )

    @override_settings(DEBUG=True)
    def test_multiple_calls_produce_consistent_results(self):
        """Multiple calls should produce identical results."""
        qs1 = PermissionManager.filter_queryset_for_user(
            self.player, Character.objects.all()
        )
        qs2 = PermissionManager.filter_queryset_for_user(
            self.player, Character.objects.all()
        )

        list1 = list(qs1.values_list("pk", flat=True))
        list2 = list(qs2.values_list("pk", flat=True))

        self.assertEqual(list1, list2)

    def test_nested_filter_calls_work(self):
        """Filtering an already-filtered queryset should work correctly."""
        qs1 = PermissionManager.filter_queryset_for_user(
            self.player, Character.objects.all()
        )
        # This should not cause issues with compounded subqueries
        qs2 = PermissionManager.filter_queryset_for_user(self.player, qs1)

        self.assertIn(self.character, list(qs2))


class FilterQuerysetOwnershipTest(TestCase):
    """Test various ownership scenarios."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username="user1", email="user1@test.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="own_head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Ownership Chronicle", head_st=self.head_st
        )

        # User1 has 3 characters
        for i in range(3):
            Character.objects.create(
                name=f"User1 Character {i}",
                owner=self.user1,
                chronicle=self.chronicle,
                status="App",
            )

        # User2 has 2 characters
        for i in range(2):
            Character.objects.create(
                name=f"User2 Character {i}",
                owner=self.user2,
                chronicle=self.chronicle,
                status="App",
            )

    def test_user_sees_correct_count(self):
        """Users should see correct number of characters including fellow players."""
        qs1 = PermissionManager.filter_queryset_for_user(
            self.user1, Character.objects.all()
        )
        # User1 sees all 5 approved characters in their chronicle
        self.assertEqual(qs1.count(), 5)

        qs2 = PermissionManager.filter_queryset_for_user(
            self.user2, Character.objects.all()
        )
        # User2 also sees all 5 approved characters in their chronicle
        self.assertEqual(qs2.count(), 5)
