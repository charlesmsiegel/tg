"""Tests for Kitsune (werefox) module."""

from characters.models.werewolf.kitsune import Kitsune
from django.contrib.auth.models import User
from django.test import TestCase


class TestKitsune(TestCase):
    """Tests for Kitsune model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.kitsune = Kitsune.objects.create(name="Test Kitsune", owner=self.player)

    def test_kitsune_creation(self):
        """Test basic Kitsune creation."""
        self.assertEqual(self.kitsune.name, "Test Kitsune")
        self.assertEqual(self.kitsune.type, "kitsune")

    def test_kitsune_default_values(self):
        """Test default values for Kitsune."""
        self.assertEqual(self.kitsune.gnosis, 0)
        self.assertEqual(self.kitsune.rage, 0)
        self.assertEqual(self.kitsune.chie, 0)
        self.assertEqual(self.kitsune.toku, 0)
        self.assertEqual(self.kitsune.kagayaki, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.kitsune.set_breed("homid"))
        self.assertEqual(self.kitsune.breed, "homid")
        self.assertEqual(self.kitsune.gnosis, 2)
        self.assertEqual(self.kitsune.rage, 1)
        self.assertTrue(
            self.kitsune.gift_permissions.filter(shifter="kitsune", condition="homid").exists()
        )

    def test_set_breed_kitsune(self):
        """Test setting kitsune (fox) breed."""
        self.assertTrue(self.kitsune.set_breed("kitsune"))
        self.assertEqual(self.kitsune.breed, "kitsune")
        self.assertEqual(self.kitsune.gnosis, 4)
        self.assertEqual(self.kitsune.rage, 1)

    def test_set_breed_kojin(self):
        """Test setting kojin (spirit) breed."""
        self.assertTrue(self.kitsune.set_breed("kojin"))
        self.assertEqual(self.kitsune.breed, "kojin")
        self.assertEqual(self.kitsune.gnosis, 6)
        self.assertEqual(self.kitsune.rage, 1)

    def test_has_path(self):
        """Test path check."""
        self.assertFalse(self.kitsune.has_path())
        self.kitsune.path = "doshi"
        self.assertTrue(self.kitsune.has_path())

    def test_set_path_doshi(self):
        """Test setting doshi path."""
        self.assertTrue(self.kitsune.set_path("doshi"))
        self.assertEqual(self.kitsune.path, "doshi")
        self.assertTrue(
            self.kitsune.gift_permissions.filter(shifter="kitsune", condition="doshi").exists()
        )

    def test_set_path_eji(self):
        """Test setting eji path."""
        self.assertTrue(self.kitsune.set_path("eji"))
        self.assertEqual(self.kitsune.path, "eji")

    def test_set_path_gukutsushi(self):
        """Test setting gukutsushi path."""
        self.assertTrue(self.kitsune.set_path("gukutsushi"))
        self.assertEqual(self.kitsune.path, "gukutsushi")

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/kitsune/{self.kitsune.pk}/"
        self.assertEqual(self.kitsune.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Kitsune.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("kitsune", breeds)
        self.assertIn("kojin", breeds)

    def test_paths_list(self):
        """Test available paths."""
        paths = dict(Kitsune.PATHS)
        self.assertIn("doshi", paths)
        self.assertIn("eji", paths)
        self.assertIn("gukutsushi", paths)


class TestKitsuneDetailView(TestCase):
    """Tests for Kitsune detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.kitsune = Kitsune.objects.create(
            name="Test Kitsune",
            owner=self.player,
            status="App",
        )

    def test_kitsune_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.kitsune.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_kitsune_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.kitsune.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
