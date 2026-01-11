"""Tests for node views."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from characters.models.core import MeritFlaw
from characters.models.mage.resonance import Resonance
from game.models import ObjectType
from locations.models.mage import Node, NodeMeritFlawRating, NodeResonanceRating


class TestNodeDetailViewQueryOptimization(TestCase):
    """Test that NodeDetailView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password", is_staff=True
        )
        self.node = Node.objects.create(name="Test Node", rank=3)

        for i in range(5):
            resonance = Resonance.objects.create(name=f"Resonance {i}")
            NodeResonanceRating.objects.create(node=self.node, resonance=resonance, rating=i + 1)

        node_type = ObjectType.objects.create(name="node", type="loc", gameline="mta")
        for i in range(3):
            mf = MeritFlaw.objects.create(
                name=f"Merit {i}",
                max_rating=i + 1,
                min_rating=i + 1,
            )
            mf.allowed_types.add(node_type)
            NodeMeritFlawRating.objects.create(node=self.node, mf=mf, rating=i + 1)

    def test_detail_view_query_count_is_bounded(self):
        """Test that detail view query count doesn't scale with related objects."""
        self.client.login(username="testuser", password="password")

        with CaptureQueriesContext(connection) as context:
            response = self.client.get(f"/locations/mage/node/{self.node.pk}/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # With select_related on resonance and mf, queries should be bounded
        # Base queries include session, user, permissions checks, and template rendering
        self.assertLessEqual(
            query_count,
            35,
            f"Too many queries ({query_count}). Detail view may have N+1 issue.",
        )

    def test_resonance_is_in_context(self):
        """Test that resonance ratings are included in context."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/locations/mage/node/{self.node.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("resonance", response.context)
        self.assertEqual(response.context["resonance"].count(), 5)

    def test_merits_and_flaws_is_in_context(self):
        """Test that merits and flaws are included in context."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/locations/mage/node/{self.node.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("merits_and_flaws", response.context)
        self.assertEqual(response.context["merits_and_flaws"].count(), 3)
