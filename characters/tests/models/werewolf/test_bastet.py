"""Tests for Bastet (werecat) module."""

from characters.models.werewolf.bastet import Bastet
from django.contrib.auth.models import User
from django.test import TestCase


class TestBastet(TestCase):
    """Tests for Bastet model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.bastet = Bastet.objects.create(name="Test Bastet", owner=self.player)

    def test_bastet_creation(self):
        """Test basic Bastet creation."""
        self.assertEqual(self.bastet.name, "Test Bastet")
        self.assertEqual(self.bastet.type, "bastet")

    def test_bastet_default_values(self):
        """Test default values for Bastet."""
        self.assertEqual(self.bastet.gnosis, 0)
        self.assertEqual(self.bastet.rage, 0)
        self.assertEqual(self.bastet.ferocity, 0)
        self.assertEqual(self.bastet.honor, 0)
        self.assertEqual(self.bastet.cunning, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.bastet.set_breed("homid"))
        self.assertEqual(self.bastet.breed, "homid")
        self.assertEqual(self.bastet.gnosis, 1)
        self.assertTrue(
            self.bastet.gift_permissions.filter(shifter="bastet", condition="homid").exists()
        )

    def test_set_breed_metis(self):
        """Test setting metis breed."""
        self.assertTrue(self.bastet.set_breed("metis"))
        self.assertEqual(self.bastet.breed, "metis")
        self.assertEqual(self.bastet.gnosis, 3)

    def test_set_breed_feline(self):
        """Test setting feline breed."""
        self.assertTrue(self.bastet.set_breed("feline"))
        self.assertEqual(self.bastet.breed, "feline")
        self.assertEqual(self.bastet.gnosis, 5)

    def test_has_tribe(self):
        """Test tribe check."""
        self.assertFalse(self.bastet.has_tribe())
        self.bastet.tribe = "bagheera"
        self.assertTrue(self.bastet.has_tribe())

    def test_set_tribe_bagheera(self):
        """Test setting Bagheera tribe."""
        self.assertTrue(self.bastet.set_tribe("bagheera"))
        self.assertEqual(self.bastet.tribe, "bagheera")
        self.assertTrue(
            self.bastet.gift_permissions.filter(shifter="bastet", condition="bagheera").exists()
        )

    def test_set_tribe_all_tribes(self):
        """Test setting each Bastet tribe."""
        tribes = ["bagheera", "balam", "bubasti", "ceilican", "khan", "pumonca", "qualmi", "simba", "swara"]
        for tribe in tribes:
            bastet = Bastet.objects.create(name=f"Test {tribe}", owner=self.player)
            self.assertTrue(bastet.set_tribe(tribe))
            self.assertEqual(bastet.tribe, tribe)

    def test_has_pryio(self):
        """Test pryio check."""
        self.assertFalse(self.bastet.has_pryio())
        self.bastet.pryio = "daylight"
        self.assertTrue(self.bastet.has_pryio())

    def test_set_pryio_daylight(self):
        """Test setting daylight pryio."""
        self.assertTrue(self.bastet.set_pryio("daylight"))
        self.assertEqual(self.bastet.pryio, "daylight")
        self.assertTrue(
            self.bastet.gift_permissions.filter(shifter="bastet", condition="daylight").exists()
        )

    def test_set_pryio_twilight(self):
        """Test setting twilight pryio."""
        self.assertTrue(self.bastet.set_pryio("twilight"))
        self.assertEqual(self.bastet.pryio, "twilight")

    def test_set_pryio_midnight(self):
        """Test setting midnight pryio."""
        self.assertTrue(self.bastet.set_pryio("midnight"))
        self.assertEqual(self.bastet.pryio, "midnight")

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/bastet/{self.bastet.pk}/"
        self.assertEqual(self.bastet.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Bastet.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("feline", breeds)
        self.assertIn("metis", breeds)

    def test_tribes_list(self):
        """Test available tribes."""
        tribes = dict(Bastet.TRIBES)
        self.assertEqual(len(tribes), 9)
        self.assertIn("bagheera", tribes)
        self.assertIn("khan", tribes)
        self.assertIn("simba", tribes)

    def test_pryio_list(self):
        """Test available pryios."""
        pryio = dict(Bastet.PRYIO)
        self.assertIn("daylight", pryio)
        self.assertIn("twilight", pryio)
        self.assertIn("midnight", pryio)


class TestBastetDetailView(TestCase):
    """Tests for Bastet detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.bastet = Bastet.objects.create(
            name="Test Bastet",
            owner=self.player,
            status="App",
        )

    def test_bastet_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.bastet.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_bastet_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.bastet.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
