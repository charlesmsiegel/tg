"""
Tests for ModelManager and ModelQuerySet performance optimizations.

Tests verify that:
- ModelManager does NOT automatically add select_related('polymorphic_ctype')
- with_polymorphic_ctype() method explicitly adds the optimization
- pending_approval_for_user() includes polymorphic_ctype

See issue #1350: Polymorphic select_related on every query adds 20-30% overhead
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.character import Character
from characters.models.core.human import Human
from game.models import Chronicle


class ModelManagerTests(TestCase):
    """Tests for ModelManager without automatic polymorphic_ctype."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass")
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")
        cls.human = Human.objects.create(
            name="Test Character",
            owner=cls.user,
            chronicle=cls.chronicle,
            status="Un",
        )

    def test_manager_does_not_auto_include_polymorphic_ctype(self):
        """Test that ModelManager does NOT auto-include polymorphic_ctype."""
        # Get a queryset without explicit with_polymorphic_ctype()
        qs = Character.objects.all()

        # Check the query does NOT include polymorphic_ctype in select_related
        # This is the fix for issue #1350
        query_str = str(qs.query)
        # The query should be a simple SELECT without JOIN on content_type
        # (unless with_polymorphic_ctype() is called)
        self.assertNotIn("django_content_type", query_str.lower())

    def test_with_polymorphic_ctype_method_exists(self):
        """Test that with_polymorphic_ctype() method exists on queryset."""
        qs = Character.objects.all()
        self.assertTrue(hasattr(qs, "with_polymorphic_ctype"))

    def test_with_polymorphic_ctype_returns_queryset(self):
        """Test that with_polymorphic_ctype() returns a queryset."""
        qs = Character.objects.all().with_polymorphic_ctype()
        # Should be able to iterate
        list(qs)
        self.assertEqual(qs.count(), 1)

    def test_with_polymorphic_ctype_includes_join(self):
        """Test that with_polymorphic_ctype() includes polymorphic_ctype join."""
        qs = Character.objects.all().with_polymorphic_ctype()
        query_str = str(qs.query)
        # The query SHOULD include JOIN on content_type
        self.assertIn("django_content_type", query_str.lower())

    def test_count_works_without_polymorphic_ctype(self):
        """Test that .count() works efficiently without polymorphic dispatch."""
        # This should NOT include the content_type join
        count = Character.objects.filter(chronicle=self.chronicle).count()
        self.assertEqual(count, 1)

    def test_exists_works_without_polymorphic_ctype(self):
        """Test that .exists() works efficiently without polymorphic dispatch."""
        # This should NOT include the content_type join
        exists = Character.objects.filter(chronicle=self.chronicle).exists()
        self.assertTrue(exists)

    def test_values_works_without_polymorphic_ctype(self):
        """Test that .values() works efficiently without polymorphic dispatch."""
        # This should NOT include the content_type join
        values = list(Character.objects.filter(chronicle=self.chronicle).values("name"))
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0]["name"], "Test Character")


class ModelQuerySetMethodsTests(TestCase):
    """Tests for ModelQuerySet methods that need polymorphic_ctype."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass")
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")
        cls.chronicle.storytellers.add(cls.user)
        cls.human = Human.objects.create(
            name="Test Character",
            owner=cls.user,
            chronicle=cls.chronicle,
            status="Sub",  # Submitted for approval (Character uses Sub, not Un)
        )

    def test_pending_approval_includes_polymorphic_ctype(self):
        """Test that pending_approval_for_user() includes polymorphic_ctype."""
        qs = Character.objects.pending_approval_for_user(self.user)
        query_str = str(qs.query)
        # Should include polymorphic_ctype join for template rendering
        self.assertIn("django_content_type", query_str.lower())

    def test_pending_approval_returns_characters(self):
        """Test that pending_approval_for_user() returns pending characters."""
        qs = Character.objects.pending_approval_for_user(self.user)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().name, "Test Character")

    def test_visible_can_chain_with_polymorphic_ctype(self):
        """Test that visible() can chain with with_polymorphic_ctype()."""
        # Create a visible character
        Human.objects.create(
            name="Visible Character",
            owner=self.user,
            chronicle=self.chronicle,
            display=True,
        )
        qs = Character.objects.visible().with_polymorphic_ctype()
        # Should work and include the join
        query_str = str(qs.query)
        self.assertIn("django_content_type", query_str.lower())
        self.assertGreaterEqual(qs.count(), 1)

    def test_for_chronicle_can_chain_with_polymorphic_ctype(self):
        """Test that for_chronicle() can chain with with_polymorphic_ctype()."""
        qs = Character.objects.for_chronicle(self.chronicle).with_polymorphic_ctype()
        # Should work and include the join
        query_str = str(qs.query)
        self.assertIn("django_content_type", query_str.lower())
        self.assertEqual(qs.count(), 1)

    def test_owned_by_can_chain_with_polymorphic_ctype(self):
        """Test that owned_by() can chain with with_polymorphic_ctype()."""
        qs = Character.objects.owned_by(self.user).with_polymorphic_ctype()
        # Should work and include the join
        query_str = str(qs.query)
        self.assertIn("django_content_type", query_str.lower())
        self.assertEqual(qs.count(), 1)
