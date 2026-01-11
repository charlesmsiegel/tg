"""Tests for coterie module."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from characters.models.core.human import Human
from characters.models.vampire.coterie import Coterie
from game.models import Chronicle


class TestCoterieListViewQueryOptimization(TestCase):
    """Test that CoterieListView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create multiple coteries with leaders and members
        for i in range(3):
            leader = Human.objects.create(
                name=f"Leader {i}",
                owner=self.user,
                chronicle=self.chronicle,
            )
            coterie = Coterie.objects.create(
                name=f"Coterie {i}",
                chronicle=self.chronicle,
                leader=leader,
            )
            # Add some members
            for j in range(2):
                member = Human.objects.create(
                    name=f"Member {i}-{j}",
                    owner=self.user,
                    chronicle=self.chronicle,
                )
                coterie.members.add(member)

    def test_list_view_query_count_is_bounded(self):
        """Test that list view query count doesn't scale with number of coteries."""
        self.client.login(username="testuser", password="password")

        with CaptureQueriesContext(connection) as context:
            response = self.client.get("/characters/vampire/list/coterie/")

        self.assertEqual(response.status_code, 200)
        # Should have a bounded number of queries (session, user, coteries with prefetches)
        # Not one per coterie for leader/members
        query_count = len(context.captured_queries)
        # Base overhead includes session, user/profile, polymorphic lookups, etc.
        # The optimization ensures queries don't scale with number of coteries
        self.assertLessEqual(
            query_count,
            20,
            f"Too many queries ({query_count}). List view may have N+1 issue.",
        )
