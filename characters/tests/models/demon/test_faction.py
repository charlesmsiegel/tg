"""Tests for DemonFaction model."""

from characters.models.demon.faction import DemonFaction
from django.contrib.auth.models import User
from django.test import TestCase


class DemonFactionModelTests(TestCase):
    """Tests for DemonFaction model functionality."""

    def setUp(self):
        """Create a test user for ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.faction = DemonFaction.objects.create(
            name="Cryptics",
            philosophy="Seek knowledge and understanding",
            goal="Discover the truth about the Fall",
            leadership="Council of wise ones",
            tactics="Research and investigation",
            owner=self.user,
        )

    def test_type_is_demon_faction(self):
        """Test that type is 'demon_faction'."""
        self.assertEqual(self.faction.type, "demon_faction")

    def test_gameline_is_dtf(self):
        """Test that gameline is 'dtf'."""
        self.assertEqual(self.faction.gameline, "dtf")

    def test_str_representation(self):
        """Test string representation is the name."""
        self.assertEqual(str(self.faction), "Cryptics")

    def test_default_philosophy(self):
        """Test default philosophy is empty."""
        faction = DemonFaction.objects.create(name="Test Faction", owner=self.user)
        self.assertEqual(faction.philosophy, "")

    def test_default_goal(self):
        """Test default goal is empty."""
        faction = DemonFaction.objects.create(name="Test Faction 2", owner=self.user)
        self.assertEqual(faction.goal, "")

    def test_default_leadership(self):
        """Test default leadership is empty."""
        faction = DemonFaction.objects.create(name="Test Faction 3", owner=self.user)
        self.assertEqual(faction.leadership, "")

    def test_default_tactics(self):
        """Test default tactics is empty."""
        faction = DemonFaction.objects.create(name="Test Faction 4", owner=self.user)
        self.assertEqual(faction.tactics, "")

    def test_ordering_by_name(self):
        """Factions should be ordered by name by default."""
        faction_c = DemonFaction.objects.create(name="Raveners", owner=self.user)
        faction_a = DemonFaction.objects.create(name="Faustians", owner=self.user)
        faction_b = DemonFaction.objects.create(name="Luciferans", owner=self.user)

        factions = list(
            DemonFaction.objects.filter(pk__in=[faction_a.pk, faction_b.pk, faction_c.pk])
        )

        self.assertEqual(factions[0], faction_a)  # Faustians
        self.assertEqual(factions[1], faction_b)  # Luciferans
        self.assertEqual(factions[2], faction_c)  # Raveners

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.faction.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/faction/{self.faction.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.faction.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/faction/{self.faction.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = DemonFaction.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/faction/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.faction.get_heading(), "dtf_heading")


class DemonFactionVerboseNameTests(TestCase):
    """Tests for DemonFaction verbose names."""

    def test_verbose_name(self):
        """Test verbose_name is correct."""
        self.assertEqual(DemonFaction._meta.verbose_name, "Demon Faction")

    def test_verbose_name_plural(self):
        """Test verbose_name_plural is correct."""
        self.assertEqual(DemonFaction._meta.verbose_name_plural, "Demon Factions")


class DemonFactionFiveFactionsTests(TestCase):
    """Tests for creating all five canonical factions."""

    def setUp(self):
        """Create test user."""
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_can_create_all_five_factions(self):
        """Test that all five canonical factions can be created."""
        factions = [
            "Cryptics",
            "Faustians",
            "Luciferans",
            "Raveners",
            "Reconcilers",
        ]

        created_factions = []
        for name in factions:
            faction = DemonFaction.objects.create(name=name, owner=self.user)
            created_factions.append(faction)

        self.assertEqual(len(created_factions), 5)
        self.assertEqual(DemonFaction.objects.count(), 5)

    def test_factions_have_different_philosophies(self):
        """Test that factions can have unique philosophies."""
        cryptics = DemonFaction.objects.create(
            name="Cryptics",
            philosophy="Seek knowledge",
            owner=self.user,
        )
        raveners = DemonFaction.objects.create(
            name="Raveners",
            philosophy="Destroy humanity",
            owner=self.user,
        )

        self.assertNotEqual(cryptics.philosophy, raveners.philosophy)
