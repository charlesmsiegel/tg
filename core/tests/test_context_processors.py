"""Tests for context processors in core/context_processors.py."""

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from core.context_processors import all_chronicles
from game.models import Chronicle


class AllChroniclesContextProcessorTest(TestCase):
    """Tests for all_chronicles context processor."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()

    def test_returns_empty_queryset_when_no_chronicles(self):
        """Test that empty queryset is returned when no chronicles exist."""
        request = self.factory.get("/")

        result = all_chronicles(request)

        self.assertIn("chronicles", result)
        self.assertEqual(result["chronicles"].count(), 0)

    def test_returns_all_chronicles_for_staff(self):
        """Staff can navigate every chronicle."""
        Chronicle.objects.create(name="Chronicle 1")
        Chronicle.objects.create(name="Chronicle 2")
        Chronicle.objects.create(name="Chronicle 3")

        request = self.factory.get("/")
        request.user = User.objects.create_user(username="staff", is_staff=True)

        result = all_chronicles(request)

        self.assertIn("chronicles", result)
        self.assertEqual(result["chronicles"].count(), 3)

    def test_returns_chronicles_queryset(self):
        """Anonymous navigation keeps a filtered QuerySet."""
        Chronicle.objects.create(name="Test Chronicle")

        request = self.factory.get("/")

        result = all_chronicles(request)

        from django.db.models import QuerySet

        self.assertIsInstance(result["chronicles"], QuerySet)
        self.assertEqual(result["chronicles"].count(), 0)
