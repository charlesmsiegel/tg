"""Tests for Pact model."""

from characters.models.demon import Demon
from characters.models.demon.pact import Pact
from characters.models.demon.thrall import Thrall
from django.contrib.auth.models import User
from django.test import TestCase


class PactModelTests(TestCase):
    """Tests for Pact model functionality."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)
        self.pact = Pact.objects.create(
            demon=self.demon,
            thrall=self.thrall,
            terms="Power for service",
            faith_payment=2,
            enhancements=["Enhanced Strength", "Quick Healing"],
            active=True,
        )

    def test_str_representation(self):
        """Test string representation."""
        self.assertEqual(str(self.pact), "Pact: Test Demon <-> Test Thrall")

    def test_str_representation_no_demon(self):
        """Test string representation when demon is None."""
        pact = Pact.objects.create(demon=None, thrall=self.thrall)
        self.assertEqual(str(pact), "Pact: No Demon <-> Test Thrall")

    def test_str_representation_no_thrall(self):
        """Test string representation when thrall is None."""
        pact = Pact.objects.create(demon=self.demon, thrall=None)
        self.assertEqual(str(pact), "Pact: Test Demon <-> No Thrall")

    def test_str_representation_no_demon_no_thrall(self):
        """Test string representation when both are None."""
        pact = Pact.objects.create(demon=None, thrall=None)
        self.assertEqual(str(pact), "Pact: No Demon <-> No Thrall")

    def test_default_terms(self):
        """Test default terms is empty string."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        self.assertEqual(pact.terms, "")

    def test_default_faith_payment(self):
        """Test default faith_payment is 0."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        self.assertEqual(pact.faith_payment, 0)

    def test_default_enhancements(self):
        """Test default enhancements is empty list."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        self.assertEqual(pact.enhancements, [])

    def test_default_active(self):
        """Test default active is True."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        self.assertTrue(pact.active)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.pact.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/pact/{self.pact.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.pact.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/pact/{self.pact.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = Pact.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/pact/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.pact.get_heading(), "dtf_heading")


class PactVerboseNameTests(TestCase):
    """Tests for Pact verbose names."""

    def test_verbose_name(self):
        """Test verbose_name is correct."""
        self.assertEqual(Pact._meta.verbose_name, "Pact")

    def test_verbose_name_plural(self):
        """Test verbose_name_plural is correct."""
        self.assertEqual(Pact._meta.verbose_name_plural, "Pacts")


class PactRelationshipTests(TestCase):
    """Tests for Pact relationships with Demon and Thrall."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_demon_can_have_multiple_pacts(self):
        """A demon can have multiple pacts."""
        thrall2 = Thrall.objects.create(name="Second Thrall", owner=self.user)
        pact1 = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        pact2 = Pact.objects.create(demon=self.demon, thrall=thrall2)

        pacts = Pact.objects.filter(demon=self.demon)
        self.assertEqual(pacts.count(), 2)

    def test_thrall_can_have_multiple_pacts(self):
        """A thrall can have multiple pacts (rare but possible)."""
        demon2 = Demon.objects.create(name="Second Demon", owner=self.user)
        pact1 = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        pact2 = Pact.objects.create(demon=demon2, thrall=self.thrall)

        pacts = Pact.objects.filter(thrall=self.thrall)
        self.assertEqual(pacts.count(), 2)

    def test_pact_cascades_on_demon_delete(self):
        """Deleting a demon should delete its pacts."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        pact_id = pact.id
        self.demon.delete()

        self.assertFalse(Pact.objects.filter(id=pact_id).exists())

    def test_pact_cascades_on_thrall_delete(self):
        """Deleting a thrall should delete its pacts."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall)
        pact_id = pact.id
        self.thrall.delete()

        self.assertFalse(Pact.objects.filter(id=pact_id).exists())


class PactEnhancementsTests(TestCase):
    """Tests for Pact enhancements field."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_enhancements_can_store_list(self):
        """Enhancements field can store a list of strings."""
        enhancements = ["Enhanced Strength", "Quick Healing", "Dark Vision"]
        pact = Pact.objects.create(
            demon=self.demon, thrall=self.thrall, enhancements=enhancements
        )
        pact.refresh_from_db()
        self.assertEqual(pact.enhancements, enhancements)

    def test_enhancements_can_be_modified(self):
        """Enhancements list can be modified and saved."""
        pact = Pact.objects.create(
            demon=self.demon, thrall=self.thrall, enhancements=["Strength"]
        )
        pact.enhancements.append("Speed")
        pact.save()
        pact.refresh_from_db()
        self.assertEqual(pact.enhancements, ["Strength", "Speed"])

    def test_enhancements_empty_list(self):
        """Enhancements can be an empty list."""
        pact = Pact.objects.create(
            demon=self.demon, thrall=self.thrall, enhancements=[]
        )
        self.assertEqual(pact.enhancements, [])


class PactActiveStatusTests(TestCase):
    """Tests for Pact active status."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        self.thrall = Thrall.objects.create(name="Test Thrall", owner=self.user)

    def test_pact_can_be_deactivated(self):
        """Pact can be set to inactive."""
        pact = Pact.objects.create(demon=self.demon, thrall=self.thrall, active=True)
        pact.active = False
        pact.save()
        pact.refresh_from_db()
        self.assertFalse(pact.active)

    def test_filter_active_pacts(self):
        """Can filter for only active pacts."""
        active_pact = Pact.objects.create(
            demon=self.demon, thrall=self.thrall, active=True
        )
        thrall2 = Thrall.objects.create(name="Another Thrall", owner=self.user)
        inactive_pact = Pact.objects.create(
            demon=self.demon, thrall=thrall2, active=False
        )

        active_pacts = Pact.objects.filter(demon=self.demon, active=True)
        self.assertEqual(active_pacts.count(), 1)
        self.assertEqual(active_pacts.first(), active_pact)
