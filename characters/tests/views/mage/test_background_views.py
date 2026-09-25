"""Tests for mage background views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from characters.models.core.background_block import Background
from characters.models.mage.mage import Mage
from game.models import Chronicle


class TestBackgroundSkipping(TestCase):
    """Test that background steps are properly skipped when not needed."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.node_bg, _ = Background.objects.get_or_create(
            property_name="node", defaults={"name": "Node"}
        )
        self.library_bg, _ = Background.objects.get_or_create(
            property_name="library", defaults={"name": "Library"}
        )

    def test_skips_node_when_none_purchased(self):
        """Test that node step is skipped when no node background."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=10,  # MageNodeView
            arete=1,
        )
        # No node background rating - should skip
        self.client.login(username="owner", password="password")
        url = mage.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mage.refresh_from_db()
        self.assertEqual(mage.creation_status, 10)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        mage.refresh_from_db()
        self.assertEqual(mage.creation_status, 11)

    def test_skips_library_when_none_purchased(self):
        """Test that library step is skipped when no library background."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=11,  # MageLibraryView
            arete=1,
        )
        # No library background rating - should skip
        self.client.login(username="owner", password="password")
        url = mage.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mage.refresh_from_db()
        self.assertEqual(mage.creation_status, 11)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        mage.refresh_from_db()
        self.assertEqual(mage.creation_status, 12)


class TestEnhancementViewSkipping(TestCase):
    """Test enhancement view skipping when no enhancements purchased."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_enhancement_view_skips_when_no_enhancements(self):
        """Test that enhancement view skips when no enhancement backgrounds."""
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=14,  # MageEnhancementView
            arete=1,
        )
        # No enhancement background rating: GET is read-only; POST advances.
        self.client.login(username="owner", password="password")
        url = mage.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mage.refresh_from_db()
        self.assertEqual(mage.creation_status, 14)
        self.assertEqual(self.client.post(url, {}).status_code, 302)
        mage.refresh_from_db()
        self.assertEqual(mage.creation_status, 15)
