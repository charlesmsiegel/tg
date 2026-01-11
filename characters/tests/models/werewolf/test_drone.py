"""Tests for Drone (Bane-possessed human) module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.drone import Drone


class TestDrone(TestCase):
    """Tests for Drone model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.drone = Drone.objects.create(name="Test Drone", owner=self.player)

    def test_drone_creation(self):
        """Test basic Drone creation."""
        self.assertEqual(self.drone.name, "Test Drone")
        self.assertEqual(self.drone.type, "drone")

    def test_drone_default_values(self):
        """Test default values for Drone."""
        self.assertEqual(self.drone.gnosis, 0)
        self.assertEqual(self.drone.rage, 0)
        self.assertEqual(self.drone.bane_name, "")
        self.assertEqual(self.drone.bane_type, "")
        self.assertEqual(self.drone.willpower_per_turn, 1)

    def test_has_bane(self):
        """Test bane check."""
        self.assertFalse(self.drone.has_bane())
        self.drone.bane_name = "Scryer"
        self.assertTrue(self.drone.has_bane())

    def test_set_bane_with_name_only(self):
        """Test setting bane with name only."""
        self.assertTrue(self.drone.set_bane("Rage Bane"))
        self.assertEqual(self.drone.bane_name, "Rage Bane")
        self.assertEqual(self.drone.bane_type, "")

    def test_set_bane_with_name_and_type(self):
        """Test setting bane with name and type."""
        self.assertTrue(self.drone.set_bane("Scryer", "Watcher Bane"))
        self.assertEqual(self.drone.bane_name, "Scryer")
        self.assertEqual(self.drone.bane_type, "Watcher Bane")

    def test_allowed_backgrounds(self):
        """Test Drone has limited background options."""
        self.assertEqual(self.drone.allowed_backgrounds, ["contacts", "resources"])
        self.assertEqual(len(self.drone.allowed_backgrounds), 2)

    def test_background_points(self):
        """Test Drone has 2 background points."""
        self.assertEqual(self.drone.background_points, 2)

    def test_get_backgrounds(self):
        """Test get_backgrounds returns only allowed backgrounds."""
        self.drone.contacts = 1
        self.drone.resources = 1
        self.drone.allies = 5  # Should not appear in allowed
        self.drone.save()
        backgrounds = self.drone.get_backgrounds()
        self.assertIn("contacts", backgrounds)
        self.assertIn("resources", backgrounds)
        # Allies should not be in allowed_backgrounds but may still be on model
        self.assertEqual(backgrounds["contacts"], 1)
        self.assertEqual(backgrounds["resources"], 1)

    def test_spiritual_stats(self):
        """Test Drone spiritual stats."""
        self.drone.rage = 5
        self.drone.gnosis = 3
        self.drone.willpower_per_turn = 2
        self.drone.save()
        self.drone.refresh_from_db()
        self.assertEqual(self.drone.rage, 5)
        self.assertEqual(self.drone.gnosis, 3)
        self.assertEqual(self.drone.willpower_per_turn, 2)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/drone/{self.drone.pk}/"
        self.assertEqual(self.drone.get_absolute_url(), expected_url)

    def test_verbose_name(self):
        """Test model verbose name."""
        self.assertEqual(Drone._meta.verbose_name, "Drone")
        self.assertEqual(Drone._meta.verbose_name_plural, "Drones")


class TestDroneDetailView(TestCase):
    """Tests for Drone detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.drone = Drone.objects.create(
            name="Test Drone",
            owner=self.player,
            status="App",
        )

    def test_drone_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.drone.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_drone_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.drone.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/drone/detail.html")

    def test_drone_detail_view_requires_login(self):
        """Test detail view requires authentication."""
        response = self.client.get(self.drone.get_absolute_url())
        # Should return 404 (hidden for unauthenticated users)
        self.assertEqual(response.status_code, 404)
