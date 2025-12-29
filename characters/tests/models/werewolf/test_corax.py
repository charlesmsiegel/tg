"""Tests for Corax (wereraven) module."""

from characters.models.werewolf.corax import Corax
from django.contrib.auth.models import User
from django.test import TestCase


class TestCorax(TestCase):
    """Tests for Corax model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.corax = Corax.objects.create(name="Test Corax", owner=self.player)

    def test_corax_creation(self):
        """Test basic Corax creation."""
        self.assertEqual(self.corax.name, "Test Corax")
        self.assertEqual(self.corax.type, "corax")

    def test_corax_default_values(self):
        """Test default values for Corax."""
        self.assertEqual(self.corax.gnosis, 0)
        self.assertEqual(self.corax.rage, 0)
        self.assertEqual(self.corax.curiosity, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.corax.set_breed("homid"))
        self.assertEqual(self.corax.breed, "homid")
        self.assertEqual(self.corax.gnosis, 3)
        self.assertEqual(self.corax.rage, 1)
        self.assertTrue(
            self.corax.gift_permissions.filter(shifter="corax", condition="homid").exists()
        )
        self.assertTrue(
            self.corax.gift_permissions.filter(shifter="corax", condition="corax").exists()
        )

    def test_set_breed_corvid(self):
        """Test setting corvid breed."""
        self.assertTrue(self.corax.set_breed("corvid"))
        self.assertEqual(self.corax.breed, "corvid")
        self.assertEqual(self.corax.gnosis, 6)
        self.assertEqual(self.corax.rage, 1)
        self.assertTrue(
            self.corax.gift_permissions.filter(shifter="corax", condition="corvid").exists()
        )

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/corax/{self.corax.pk}/"
        self.assertEqual(self.corax.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Corax.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("corvid", breeds)
        # Corax cannot be metis
        self.assertEqual(len(breeds), 2)

    def test_no_tribes(self):
        """Test Corax have no tribes (all are one people)."""
        # Corax has no TRIBES attribute
        self.assertFalse(hasattr(Corax, "TRIBES"))

    def test_curiosity_field(self):
        """Test Corax unique curiosity field."""
        self.corax.curiosity = 3
        self.corax.save()
        self.corax.refresh_from_db()
        self.assertEqual(self.corax.curiosity, 3)


class TestCoraxDetailView(TestCase):
    """Tests for Corax detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.corax = Corax.objects.create(
            name="Test Corax",
            owner=self.player,
            status="App",
        )

    def test_corax_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.corax.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_corax_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.corax.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
