"""Tests for Ananasi (werespider) module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.ananasi import Ananasi


class TestAnanasi(TestCase):
    """Tests for Ananasi model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.ananasi = Ananasi.objects.create(name="Test Ananasi", owner=self.player)

    def test_ananasi_creation(self):
        """Test basic Ananasi creation."""
        self.assertEqual(self.ananasi.name, "Test Ananasi")
        self.assertEqual(self.ananasi.type, "ananasi")

    def test_ananasi_default_values(self):
        """Test default values for Ananasi."""
        self.assertEqual(self.ananasi.gnosis, 0)
        self.assertEqual(self.ananasi.rage, 0)
        self.assertEqual(self.ananasi.cunning, 0)
        self.assertEqual(self.ananasi.obedience, 0)
        self.assertEqual(self.ananasi.wisdom, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.ananasi.set_breed("homid"))
        self.assertEqual(self.ananasi.breed, "homid")
        self.assertEqual(self.ananasi.gnosis, 1)
        self.assertTrue(
            self.ananasi.gift_permissions.filter(shifter="ananasi", condition="homid").exists()
        )

    def test_set_breed_ananasi(self):
        """Test setting ananasi (metis) breed."""
        self.assertTrue(self.ananasi.set_breed("ananasi"))
        self.assertEqual(self.ananasi.breed, "ananasi")
        self.assertEqual(self.ananasi.gnosis, 3)

    def test_set_breed_lilian(self):
        """Test setting lilian (spider) breed."""
        self.assertTrue(self.ananasi.set_breed("lilian"))
        self.assertEqual(self.ananasi.breed, "lilian")
        self.assertEqual(self.ananasi.gnosis, 5)

    def test_has_aspect(self):
        """Test aspect check."""
        self.assertFalse(self.ananasi.has_aspect())
        self.ananasi.aspect = "tenere"
        self.assertTrue(self.ananasi.has_aspect())

    def test_set_aspect_tenere(self):
        """Test setting tenere aspect."""
        self.assertTrue(self.ananasi.set_aspect("tenere"))
        self.assertEqual(self.ananasi.aspect, "tenere")
        self.assertEqual(self.ananasi.rage, 4)
        self.assertTrue(
            self.ananasi.gift_permissions.filter(shifter="ananasi", condition="tenere").exists()
        )

    def test_set_aspect_kumoti(self):
        """Test setting kumoti aspect."""
        self.assertTrue(self.ananasi.set_aspect("kumoti"))
        self.assertEqual(self.ananasi.aspect, "kumoti")
        self.assertEqual(self.ananasi.rage, 3)

    def test_set_aspect_hatar(self):
        """Test setting hatar aspect."""
        self.assertTrue(self.ananasi.set_aspect("hatar"))
        self.assertEqual(self.ananasi.aspect, "hatar")
        self.assertEqual(self.ananasi.rage, 2)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/ananasi/{self.ananasi.pk}/"
        self.assertEqual(self.ananasi.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Ananasi.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("lilian", breeds)
        self.assertIn("ananasi", breeds)

    def test_aspects_list(self):
        """Test available aspects."""
        aspects = dict(Ananasi.ASPECTS)
        self.assertIn("kumoti", aspects)
        self.assertIn("tenere", aspects)
        self.assertIn("hatar", aspects)


class TestAnansiDetailView(TestCase):
    """Tests for Ananasi detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.ananasi = Ananasi.objects.create(
            name="Test Ananasi",
            owner=self.player,
            status="App",
        )

    def test_ananasi_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.ananasi.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_ananasi_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.ananasi.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
