"""Tests for Ajaba (werehyena) module."""

from characters.models.werewolf.ajaba import Ajaba
from characters.models.werewolf.gift import GiftPermission
from django.contrib.auth.models import User
from django.test import TestCase


class TestAjaba(TestCase):
    """Tests for Ajaba model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.ajaba = Ajaba.objects.create(name="Test Ajaba", owner=self.player)

    def test_ajaba_creation(self):
        """Test basic Ajaba creation."""
        self.assertEqual(self.ajaba.name, "Test Ajaba")
        self.assertEqual(self.ajaba.type, "ajaba")

    def test_ajaba_default_values(self):
        """Test default values for Ajaba."""
        self.assertEqual(self.ajaba.gnosis, 0)
        self.assertEqual(self.ajaba.rage, 0)
        self.assertEqual(self.ajaba.ferocity, 0)
        self.assertEqual(self.ajaba.obligation, 0)
        self.assertEqual(self.ajaba.wisdom, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.ajaba.set_breed("homid"))
        self.assertEqual(self.ajaba.breed, "homid")
        self.assertEqual(self.ajaba.gnosis, 1)
        self.assertTrue(
            self.ajaba.gift_permissions.filter(shifter="ajaba", condition="homid").exists()
        )

    def test_set_breed_crocas(self):
        """Test setting crocas (metis) breed."""
        self.assertTrue(self.ajaba.set_breed("crocas"))
        self.assertEqual(self.ajaba.breed, "crocas")
        self.assertEqual(self.ajaba.gnosis, 3)
        self.assertTrue(
            self.ajaba.gift_permissions.filter(shifter="ajaba", condition="crocas").exists()
        )

    def test_set_breed_ajaba(self):
        """Test setting ajaba (hyena) breed."""
        self.assertTrue(self.ajaba.set_breed("ajaba"))
        self.assertEqual(self.ajaba.breed, "ajaba")
        self.assertEqual(self.ajaba.gnosis, 5)
        self.assertTrue(
            self.ajaba.gift_permissions.filter(shifter="ajaba", condition="ajaba").exists()
        )

    def test_has_auspice(self):
        """Test auspice check."""
        self.assertFalse(self.ajaba.has_auspice())
        self.ajaba.auspice = "full_moon"
        self.assertTrue(self.ajaba.has_auspice())

    def test_set_auspice_full_moon(self):
        """Test setting full moon auspice."""
        self.assertTrue(self.ajaba.set_auspice("full_moon"))
        self.assertEqual(self.ajaba.auspice, "full_moon")
        self.assertEqual(self.ajaba.rage, 5)
        self.assertTrue(
            self.ajaba.gift_permissions.filter(shifter="ajaba", condition="full_moon").exists()
        )

    def test_set_auspice_gibbous_moon(self):
        """Test setting gibbous moon auspice."""
        self.assertTrue(self.ajaba.set_auspice("gibbous_moon"))
        self.assertEqual(self.ajaba.auspice, "gibbous_moon")
        self.assertEqual(self.ajaba.rage, 4)

    def test_set_auspice_half_moon(self):
        """Test setting half moon auspice."""
        self.assertTrue(self.ajaba.set_auspice("half_moon"))
        self.assertEqual(self.ajaba.auspice, "half_moon")
        self.assertEqual(self.ajaba.rage, 3)

    def test_set_auspice_crescent_moon(self):
        """Test setting crescent moon auspice."""
        self.assertTrue(self.ajaba.set_auspice("crescent_moon"))
        self.assertEqual(self.ajaba.auspice, "crescent_moon")
        self.assertEqual(self.ajaba.rage, 2)

    def test_set_auspice_new_moon(self):
        """Test setting new moon auspice."""
        self.assertTrue(self.ajaba.set_auspice("new_moon"))
        self.assertEqual(self.ajaba.auspice, "new_moon")
        self.assertEqual(self.ajaba.rage, 1)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/ajaba/{self.ajaba.pk}/"
        self.assertEqual(self.ajaba.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Ajaba.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("ajaba", breeds)
        self.assertIn("crocas", breeds)

    def test_auspices_list(self):
        """Test available auspices."""
        auspices = dict(Ajaba.AUSPICES)
        self.assertIn("new_moon", auspices)
        self.assertIn("crescent_moon", auspices)
        self.assertIn("half_moon", auspices)
        self.assertIn("gibbous_moon", auspices)
        self.assertIn("full_moon", auspices)


class TestAjabaDetailView(TestCase):
    """Tests for Ajaba detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.ajaba = Ajaba.objects.create(
            name="Test Ajaba",
            owner=self.player,
            status="App",
        )

    def test_ajaba_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.ajaba.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_ajaba_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.ajaba.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
