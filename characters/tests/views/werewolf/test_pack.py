"""Tests for pack module."""

from characters.models.core.human import Human
from characters.models.werewolf.pack import Pack
from characters.models.werewolf.totem import Totem
from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from game.models import Chronicle


class TestPackListViewQueryOptimization(TestCase):
    """Test that PackListView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create totems and packs
        for i in range(3):
            totem = Totem.objects.create(name=f"Totem {i}")
            leader = Human.objects.create(
                name=f"Alpha {i}",
                owner=self.user,
                chronicle=self.chronicle,
            )
            pack = Pack.objects.create(
                name=f"Pack {i}",
                chronicle=self.chronicle,
                leader=leader,
                totem=totem,
            )
            for j in range(2):
                member = Human.objects.create(
                    name=f"Packmate {i}-{j}",
                    owner=self.user,
                    chronicle=self.chronicle,
                )
                pack.members.add(member)

    def test_list_view_query_count_is_bounded(self):
        """Test that list view query count doesn't scale with number of packs."""
        self.client.login(username="testuser", password="password")

        with CaptureQueriesContext(connection) as context:
            response = self.client.get("/characters/werewolf/list/pack/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # Base overhead includes session, user/profile, polymorphic lookups, etc.
        # The optimization ensures queries don't scale with number of packs
        self.assertLessEqual(
            query_count,
            20,
            f"Too many queries ({query_count}). List view may have N+1 issue.",
        )
