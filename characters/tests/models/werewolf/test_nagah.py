"""Tests for Nagah (wereserpent) module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.nagah import Nagah


class TestNagah(TestCase):
    """Tests for Nagah model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.nagah = Nagah.objects.create(name="Test Nagah", owner=self.player)

    def test_nagah_creation(self):
        """Test basic Nagah creation."""
        self.assertEqual(self.nagah.name, "Test Nagah")
        self.assertEqual(self.nagah.type, "nagah")

    def test_nagah_default_values(self):
        """Test default values for Nagah."""
        self.assertEqual(self.nagah.gnosis, 0)
        self.assertEqual(self.nagah.rage, 0)
        self.assertEqual(self.nagah.obligation, 0)
        self.assertEqual(self.nagah.wisdom, 0)
        self.assertEqual(self.nagah.subtlety, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.nagah.set_breed("homid"))
        self.assertEqual(self.nagah.breed, "homid")
        self.assertEqual(self.nagah.gnosis, 2)
        self.assertTrue(
            self.nagah.gift_permissions.filter(shifter="nagah", condition="homid").exists()
        )

    def test_set_breed_vasuki(self):
        """Test setting vasuki (naga) breed."""
        self.assertTrue(self.nagah.set_breed("vasuki"))
        self.assertEqual(self.nagah.breed, "vasuki")
        self.assertEqual(self.nagah.gnosis, 4)

    def test_set_breed_balaram(self):
        """Test setting balaram (cobra) breed."""
        self.assertTrue(self.nagah.set_breed("balaram"))
        self.assertEqual(self.nagah.breed, "balaram")
        self.assertEqual(self.nagah.gnosis, 6)

    def test_has_auspice(self):
        """Test auspice check."""
        self.assertFalse(self.nagah.has_auspice())
        self.nagah.auspice = "kamakshi"
        self.assertTrue(self.nagah.has_auspice())

    def test_set_auspice_kamakshi(self):
        """Test setting kamakshi auspice."""
        self.assertTrue(self.nagah.set_auspice("kamakshi"))
        self.assertEqual(self.nagah.auspice, "kamakshi")
        self.assertEqual(self.nagah.rage, 4)
        self.assertTrue(
            self.nagah.gift_permissions.filter(shifter="nagah", condition="kamakshi").exists()
        )

    def test_set_auspice_kali(self):
        """Test setting kali auspice."""
        self.assertTrue(self.nagah.set_auspice("kali"))
        self.assertEqual(self.nagah.auspice, "kali")
        self.assertEqual(self.nagah.rage, 3)

    def test_set_auspice_kartikeya(self):
        """Test setting kartikeya auspice."""
        self.assertTrue(self.nagah.set_auspice("kartikeya"))
        self.assertEqual(self.nagah.auspice, "kartikeya")
        self.assertEqual(self.nagah.rage, 2)

    def test_set_auspice_kamsa(self):
        """Test setting kamsa auspice."""
        self.assertTrue(self.nagah.set_auspice("kamsa"))
        self.assertEqual(self.nagah.auspice, "kamsa")
        self.assertEqual(self.nagah.rage, 1)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/nagah/{self.nagah.pk}/"
        self.assertEqual(self.nagah.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Nagah.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("balaram", breeds)
        self.assertIn("vasuki", breeds)

    def test_auspices_list(self):
        """Test available auspices."""
        auspices = dict(Nagah.AUSPICES)
        self.assertIn("kamakshi", auspices)
        self.assertIn("kartikeya", auspices)
        self.assertIn("kamsa", auspices)
        self.assertIn("kali", auspices)


class TestNagahDetailView(TestCase):
    """Tests for Nagah detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.nagah = Nagah.objects.create(
            name="Test Nagah",
            owner=self.player,
            status="App",
        )

    def test_nagah_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.nagah.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_nagah_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.nagah.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
