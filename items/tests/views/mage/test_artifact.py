"""Tests for artifact views."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from characters.models.mage.resonance import Resonance
from items.models.mage import WonderResonanceRating
from items.models.mage.artifact import Artifact


class TestArtifactDetailViewQueryOptimization(TestCase):
    """Test that ArtifactDetailView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.artifact = Artifact.objects.create(name="Test Artifact", rank=3)
        for i in range(5):
            resonance = Resonance.objects.create(name=f"Resonance {i}")
            WonderResonanceRating.objects.create(
                wonder=self.artifact, resonance=resonance, rating=i + 1
            )

    def test_detail_view_query_count_is_bounded(self):
        """Test that detail view query count doesn't scale with number of resonances."""
        self.client.login(username="testuser", password="password")

        with CaptureQueriesContext(connection) as context:
            response = self.client.get(f"/items/mage/artifact/{self.artifact.pk}/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # With select_related on resonance, queries should be bounded
        # regardless of number of resonance ratings
        self.assertLessEqual(
            query_count,
            15,
            f"Too many queries ({query_count}). Detail view may have N+1 issue.",
        )

    def test_resonance_is_in_context(self):
        """Test that resonance ratings are included in context."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/items/mage/artifact/{self.artifact.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("resonance", response.context)
        self.assertEqual(response.context["resonance"].count(), 5)


class TestArtifactCreateView(TestCase):
    """Test ArtifactCreateView functionality."""

    def test_create_view_has_get_success_url_method(self):
        """Test that ArtifactCreateView has explicit get_success_url method."""
        from items.views.mage.artifact import ArtifactCreateView

        self.assertTrue(
            hasattr(ArtifactCreateView, "get_success_url"),
            "ArtifactCreateView should have get_success_url method",
        )
        # Verify it's defined on the class itself, not inherited
        self.assertIn(
            "get_success_url",
            ArtifactCreateView.__dict__,
            "get_success_url should be explicitly defined on ArtifactCreateView",
        )


class TestArtifactUpdateView(TestCase):
    """Test ArtifactUpdateView functionality."""

    def test_update_view_has_get_success_url_method(self):
        """Test that ArtifactUpdateView has explicit get_success_url method."""
        from items.views.mage.artifact import ArtifactUpdateView

        self.assertTrue(
            hasattr(ArtifactUpdateView, "get_success_url"),
            "ArtifactUpdateView should have get_success_url method",
        )
        # Verify it's defined on the class itself, not inherited
        self.assertIn(
            "get_success_url",
            ArtifactUpdateView.__dict__,
            "get_success_url should be explicitly defined on ArtifactUpdateView",
        )
