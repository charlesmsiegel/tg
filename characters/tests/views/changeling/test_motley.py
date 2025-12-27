"""Tests for motley module."""

from characters.models.changeling.motley import Motley
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from game.models import Chronicle


class TestMotleyListViewQueryOptimization(TestCase):
    """Test that MotleyListView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        for i in range(3):
            leader = Human.objects.create(
                name=f"Motley Leader {i}",
                owner=self.user,
                chronicle=self.chronicle,
            )
            motley = Motley.objects.create(
                name=f"Motley {i}",
                chronicle=self.chronicle,
                leader=leader,
            )
            for j in range(2):
                member = Human.objects.create(
                    name=f"Motley Member {i}-{j}",
                    owner=self.user,
                    chronicle=self.chronicle,
                )
                motley.members.add(member)

    def test_list_view_query_count_is_bounded(self):
        """Test that list view query count doesn't scale with number of motleys."""
        self.client.login(username="testuser", password="password")

        with CaptureQueriesContext(connection) as context:
            response = self.client.get("/characters/changeling/list/motley/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # Base overhead includes session, user/profile, polymorphic lookups, etc.
        # The optimization ensures queries don't scale with number of motleys
        self.assertLessEqual(
            query_count,
            20,
            f"Too many queries ({query_count}). List view may have N+1 issue.",
        )
