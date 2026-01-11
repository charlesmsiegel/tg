"""Tests for Grondr (wereboar) module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.grondr import Grondr


class TestGrondr(TestCase):
    """Tests for Grondr model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.grondr = Grondr.objects.create(name="Test Grondr", owner=self.player)

    def test_grondr_creation(self):
        """Test basic Grondr creation."""
        self.assertEqual(self.grondr.name, "Test Grondr")
        self.assertEqual(self.grondr.type, "grondr")

    def test_grondr_default_values(self):
        """Test default values for Grondr."""
        self.assertEqual(self.grondr.gnosis, 0)
        self.assertEqual(self.grondr.rage, 0)
        self.assertEqual(self.grondr.glory, 0)
        self.assertEqual(self.grondr.honor, 0)
        self.assertEqual(self.grondr.wisdom, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.grondr.set_breed("homid"))
        self.assertEqual(self.grondr.breed, "homid")
        self.assertEqual(self.grondr.gnosis, 1)
        self.assertTrue(
            self.grondr.gift_permissions.filter(shifter="grondr", condition="homid").exists()
        )

    def test_set_breed_metis(self):
        """Test setting metis breed."""
        self.assertTrue(self.grondr.set_breed("metis"))
        self.assertEqual(self.grondr.breed, "metis")
        self.assertEqual(self.grondr.gnosis, 3)

    def test_set_breed_suidae(self):
        """Test setting suidae (boar) breed."""
        self.assertTrue(self.grondr.set_breed("suidae"))
        self.assertEqual(self.grondr.breed, "suidae")
        self.assertEqual(self.grondr.gnosis, 5)

    def test_has_auspice(self):
        """Test auspice check."""
        self.assertFalse(self.grondr.has_auspice())
        self.grondr.auspice = "summer"
        self.assertTrue(self.grondr.has_auspice())

    def test_set_auspice_summer(self):
        """Test setting summer auspice."""
        self.assertTrue(self.grondr.set_auspice("summer"))
        self.assertEqual(self.grondr.auspice, "summer")
        self.assertEqual(self.grondr.rage, 4)
        self.assertTrue(
            self.grondr.gift_permissions.filter(shifter="grondr", condition="summer").exists()
        )

    def test_set_auspice_autumn(self):
        """Test setting autumn auspice."""
        self.assertTrue(self.grondr.set_auspice("autumn"))
        self.assertEqual(self.grondr.auspice, "autumn")
        self.assertEqual(self.grondr.rage, 3)

    def test_set_auspice_spring(self):
        """Test setting spring auspice."""
        self.assertTrue(self.grondr.set_auspice("spring"))
        self.assertEqual(self.grondr.auspice, "spring")
        self.assertEqual(self.grondr.rage, 2)

    def test_set_auspice_winter(self):
        """Test setting winter auspice."""
        self.assertTrue(self.grondr.set_auspice("winter"))
        self.assertEqual(self.grondr.auspice, "winter")
        self.assertEqual(self.grondr.rage, 2)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/grondr/{self.grondr.pk}/"
        self.assertEqual(self.grondr.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Grondr.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("suidae", breeds)
        self.assertIn("metis", breeds)

    def test_auspices_list(self):
        """Test available auspices."""
        auspices = dict(Grondr.AUSPICES)
        self.assertIn("spring", auspices)
        self.assertIn("summer", auspices)
        self.assertIn("autumn", auspices)
        self.assertIn("winter", auspices)


class TestGrondrDetailView(TestCase):
    """Tests for Grondr detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.grondr = Grondr.objects.create(
            name="Test Grondr",
            owner=self.player,
            status="App",
        )

    def test_grondr_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.grondr.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_grondr_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.grondr.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
