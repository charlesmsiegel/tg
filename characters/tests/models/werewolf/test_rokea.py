"""Tests for Rokea (wereshark) module."""

from characters.models.werewolf.rokea import Rokea
from django.contrib.auth.models import User
from django.test import TestCase


class TestRokea(TestCase):
    """Tests for Rokea model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.rokea = Rokea.objects.create(name="Test Rokea", owner=self.player)

    def test_rokea_creation(self):
        """Test basic Rokea creation."""
        self.assertEqual(self.rokea.name, "Test Rokea")
        self.assertEqual(self.rokea.type, "rokea")

    def test_rokea_default_values(self):
        """Test default values for Rokea."""
        self.assertEqual(self.rokea.gnosis, 0)
        self.assertEqual(self.rokea.rage, 0)
        self.assertEqual(self.rokea.valor, 0)
        self.assertEqual(self.rokea.harmony, 0)
        self.assertEqual(self.rokea.innovation, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.rokea.set_breed("homid"))
        self.assertEqual(self.rokea.breed, "homid")
        self.assertEqual(self.rokea.gnosis, 1)
        self.assertEqual(self.rokea.rage, 5)
        self.assertTrue(
            self.rokea.gift_permissions.filter(shifter="rokea", condition="homid").exists()
        )

    def test_set_breed_squamus(self):
        """Test setting squamus (shark) breed."""
        self.assertTrue(self.rokea.set_breed("squamus"))
        self.assertEqual(self.rokea.breed, "squamus")
        self.assertEqual(self.rokea.gnosis, 5)
        self.assertEqual(self.rokea.rage, 5)

    def test_has_auspice(self):
        """Test auspice check."""
        self.assertFalse(self.rokea.has_auspice())
        self.rokea.auspice = "brightwater"
        self.assertTrue(self.rokea.has_auspice())

    def test_set_auspice_brightwater(self):
        """Test setting brightwater auspice."""
        self.assertTrue(self.rokea.set_auspice("brightwater"))
        self.assertEqual(self.rokea.auspice, "brightwater")
        self.assertTrue(
            self.rokea.gift_permissions.filter(shifter="rokea", condition="brightwater").exists()
        )

    def test_set_auspice_darkwater(self):
        """Test setting darkwater auspice."""
        self.assertTrue(self.rokea.set_auspice("darkwater"))
        self.assertEqual(self.rokea.auspice, "darkwater")

    def test_high_starting_rage(self):
        """Test Rokea have high starting rage from all breeds."""
        homid_rokea = Rokea.objects.create(name="Homid Rokea", owner=self.player)
        homid_rokea.set_breed("homid")
        self.assertEqual(homid_rokea.rage, 5)

        squamus_rokea = Rokea.objects.create(name="Squamus Rokea", owner=self.player)
        squamus_rokea.set_breed("squamus")
        self.assertEqual(squamus_rokea.rage, 5)

    def test_no_metis(self):
        """Test Rokea cannot be metis."""
        breeds = dict(Rokea.BREEDS)
        self.assertNotIn("metis", breeds)
        self.assertEqual(len(breeds), 2)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/rokea/{self.rokea.pk}/"
        self.assertEqual(self.rokea.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Rokea.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("squamus", breeds)

    def test_auspices_list(self):
        """Test available auspices."""
        auspices = dict(Rokea.AUSPICES)
        self.assertIn("brightwater", auspices)
        self.assertIn("darkwater", auspices)
        self.assertEqual(len(auspices), 2)


class TestRokeaDetailView(TestCase):
    """Tests for Rokea detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.rokea = Rokea.objects.create(
            name="Test Rokea",
            owner=self.player,
            status="App",
        )

    def test_rokea_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.rokea.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_rokea_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.rokea.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
