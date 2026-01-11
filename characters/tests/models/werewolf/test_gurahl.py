"""Tests for Gurahl (werebear) module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.gurahl import Gurahl


class TestGurahl(TestCase):
    """Tests for Gurahl model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.gurahl = Gurahl.objects.create(name="Test Gurahl", owner=self.player)

    def test_gurahl_creation(self):
        """Test basic Gurahl creation."""
        self.assertEqual(self.gurahl.name, "Test Gurahl")
        self.assertEqual(self.gurahl.type, "gurahl")

    def test_gurahl_default_values(self):
        """Test default values for Gurahl."""
        self.assertEqual(self.gurahl.gnosis, 0)
        self.assertEqual(self.gurahl.rage, 0)
        self.assertEqual(self.gurahl.honor, 0)
        self.assertEqual(self.gurahl.succor, 0)
        self.assertEqual(self.gurahl.vision, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.gurahl.set_breed("homid"))
        self.assertEqual(self.gurahl.breed, "homid")
        self.assertEqual(self.gurahl.gnosis, 2)
        self.assertTrue(
            self.gurahl.gift_permissions.filter(shifter="gurahl", condition="homid").exists()
        )

    def test_set_breed_arthren(self):
        """Test setting arthren (metis) breed."""
        self.assertTrue(self.gurahl.set_breed("arthren"))
        self.assertEqual(self.gurahl.breed, "arthren")
        self.assertEqual(self.gurahl.gnosis, 4)

    def test_set_breed_ursine(self):
        """Test setting ursine (bear) breed."""
        self.assertTrue(self.gurahl.set_breed("ursine"))
        self.assertEqual(self.gurahl.breed, "ursine")
        self.assertEqual(self.gurahl.gnosis, 6)

    def test_has_auspice(self):
        """Test auspice check."""
        self.assertFalse(self.gurahl.has_auspice())
        self.gurahl.auspice = "arcas"
        self.assertTrue(self.gurahl.has_auspice())

    def test_set_auspice_arcas(self):
        """Test setting arcas (summer) auspice."""
        self.assertTrue(self.gurahl.set_auspice("arcas"))
        self.assertEqual(self.gurahl.auspice, "arcas")
        self.assertEqual(self.gurahl.rage, 4)
        self.assertTrue(
            self.gurahl.gift_permissions.filter(shifter="gurahl", condition="arcas").exists()
        )

    def test_set_auspice_uzmati(self):
        """Test setting uzmati (autumn) auspice."""
        self.assertTrue(self.gurahl.set_auspice("uzmati"))
        self.assertEqual(self.gurahl.auspice, "uzmati")
        self.assertEqual(self.gurahl.rage, 3)

    def test_set_auspice_kojubat(self):
        """Test setting kojubat (winter) auspice."""
        self.assertTrue(self.gurahl.set_auspice("kojubat"))
        self.assertEqual(self.gurahl.auspice, "kojubat")
        self.assertEqual(self.gurahl.rage, 2)

    def test_set_auspice_kieh(self):
        """Test setting kieh (spring) auspice."""
        self.assertTrue(self.gurahl.set_auspice("kieh"))
        self.assertEqual(self.gurahl.auspice, "kieh")
        self.assertEqual(self.gurahl.rage, 1)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/gurahl/{self.gurahl.pk}/"
        self.assertEqual(self.gurahl.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Gurahl.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("ursine", breeds)
        self.assertIn("arthren", breeds)

    def test_auspices_list(self):
        """Test available auspices."""
        auspices = dict(Gurahl.AUSPICES)
        self.assertIn("arcas", auspices)
        self.assertIn("uzmati", auspices)
        self.assertIn("kojubat", auspices)
        self.assertIn("kieh", auspices)


class TestGurahlDetailView(TestCase):
    """Tests for Gurahl detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.gurahl = Gurahl.objects.create(
            name="Test Gurahl",
            owner=self.player,
            status="App",
        )

    def test_gurahl_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.gurahl.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_gurahl_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.gurahl.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
