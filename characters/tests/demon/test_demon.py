"""Tests for Demon model."""

from characters.models.demon import Demon
from django.contrib.auth.models import User
from django.test import TestCase


class DemonModelTests(TestCase):
    """Tests for Demon model functionality."""

    def setUp(self):
        """Create a test user for demon ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_name_field_is_primary_identifier(self):
        """The name field should be the primary identifier (host name)."""
        demon = Demon.objects.create(
            name="John Smith",
            celestial_name="Hasmed",
            owner=self.user,
        )
        # __str__ uses the inherited name field
        self.assertEqual(str(demon), "John Smith")

    def test_celestial_name_is_separate(self):
        """Celestial name is stored separately from the name (host identity)."""
        demon = Demon.objects.create(
            name="Jane Doe",
            celestial_name="Ahrimal",
            owner=self.user,
        )
        self.assertEqual(demon.name, "Jane Doe")
        self.assertEqual(demon.celestial_name, "Ahrimal")

    def test_ordering_by_name(self):
        """Demons should be ordered by name by default."""
        # Create demons out of alphabetical order
        demon_c = Demon.objects.create(name="Charlie Brown", owner=self.user)
        demon_a = Demon.objects.create(name="Alice Smith", owner=self.user)
        demon_b = Demon.objects.create(name="Bob Jones", owner=self.user)

        # Query without explicit ordering - should use Meta.ordering
        demons = list(Demon.objects.all())

        # Should be ordered by name alphabetically
        self.assertEqual(demons[0], demon_a)  # Alice
        self.assertEqual(demons[1], demon_b)  # Bob
        self.assertEqual(demons[2], demon_c)  # Charlie

    def test_host_name_field_removed(self):
        """The host_name field should no longer exist."""
        demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.assertFalse(hasattr(demon, "host_name"))
