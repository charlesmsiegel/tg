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
        self.artifact = Artifact.objects.create(name="Test Artifact", rank=3, owner=self.user)
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
        for i in range(5, 10):
            resonance = Resonance.objects.create(name=f"Resonance {i}")
            WonderResonanceRating.objects.create(
                wonder=self.artifact, resonance=resonance, rating=1
            )
        with CaptureQueriesContext(connection) as expanded:
            self.client.get(f"/items/mage/artifact/{self.artifact.pk}/")
        self.assertLessEqual(len(expanded.captured_queries), query_count + 2)

    def test_resonance_is_in_context(self):
        """Test that resonance ratings are included in context."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/items/mage/artifact/{self.artifact.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("resonance", response.context)
        self.assertEqual(response.context["resonance"].count(), 5)


class TestArtifactCreateView(TestCase):
    """Test ArtifactCreateView functionality."""

    def test_create_view_redirects_to_saved_object(self):
        from items.models.mage.artifact import Artifact
        from items.views.mage.artifact import ArtifactCreateView

        obj = Artifact.objects.create(name="Saved Artifact")
        view = ArtifactCreateView()
        view.object = obj
        self.assertEqual(view.get_success_url(), obj.get_absolute_url())


class TestArtifactUpdateView(TestCase):
    """Test ArtifactUpdateView functionality."""

    def test_update_view_redirects_to_saved_object(self):
        from items.models.mage.artifact import Artifact
        from items.views.mage.artifact import ArtifactUpdateView

        obj = Artifact.objects.create(name="Saved Artifact")
        view = ArtifactUpdateView()
        view.object = obj
        self.assertEqual(view.get_success_url(), obj.get_absolute_url())
