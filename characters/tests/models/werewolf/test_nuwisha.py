"""Tests for Nuwisha (werecoyote) module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.nuwisha import Nuwisha


class TestNuwisha(TestCase):
    """Tests for Nuwisha model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.nuwisha = Nuwisha.objects.create(name="Test Nuwisha", owner=self.player)

    def test_nuwisha_creation(self):
        """Test basic Nuwisha creation."""
        self.assertEqual(self.nuwisha.name, "Test Nuwisha")
        self.assertEqual(self.nuwisha.type, "nuwisha")

    def test_nuwisha_default_values(self):
        """Test default values for Nuwisha."""
        self.assertEqual(self.nuwisha.gnosis, 0)
        self.assertEqual(self.nuwisha.rage, 0)
        self.assertEqual(self.nuwisha.glory, 0)
        self.assertEqual(self.nuwisha.humor, 0)
        self.assertEqual(self.nuwisha.cunning, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.nuwisha.set_breed("homid"))
        self.assertEqual(self.nuwisha.breed, "homid")
        self.assertEqual(self.nuwisha.gnosis, 2)
        self.assertEqual(self.nuwisha.rage, 3)
        self.assertTrue(
            self.nuwisha.gift_permissions.filter(shifter="nuwisha", condition="homid").exists()
        )
        self.assertTrue(
            self.nuwisha.gift_permissions.filter(shifter="nuwisha", condition="nuwisha").exists()
        )

    def test_set_breed_latrani(self):
        """Test setting latrani (coyote) breed."""
        self.assertTrue(self.nuwisha.set_breed("latrani"))
        self.assertEqual(self.nuwisha.breed, "latrani")
        self.assertEqual(self.nuwisha.gnosis, 5)
        self.assertEqual(self.nuwisha.rage, 3)

    def test_has_role(self):
        """Test role check."""
        self.assertFalse(self.nuwisha.has_role())
        self.nuwisha.role = "kojubat"
        self.assertTrue(self.nuwisha.has_role())

    def test_set_role_kojubat(self):
        """Test setting kojubat role."""
        self.assertTrue(self.nuwisha.set_role("kojubat"))
        self.assertEqual(self.nuwisha.role, "kojubat")
        self.assertTrue(
            self.nuwisha.gift_permissions.filter(shifter="nuwisha", condition="kojubat").exists()
        )

    def test_set_role_kitmoti(self):
        """Test setting kitmoti role."""
        self.assertTrue(self.nuwisha.set_role("kitmoti"))
        self.assertEqual(self.nuwisha.role, "kitmoti")

    def test_set_role_umbagi(self):
        """Test setting umbagi role."""
        self.assertTrue(self.nuwisha.set_role("umbagi"))
        self.assertEqual(self.nuwisha.role, "umbagi")

    def test_humor_unique_field(self):
        """Test Nuwisha unique humor field."""
        self.assertEqual(self.nuwisha.humor, 0)
        self.nuwisha.humor = 3
        self.nuwisha.save()
        self.nuwisha.refresh_from_db()
        self.assertEqual(self.nuwisha.humor, 3)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/nuwisha/{self.nuwisha.pk}/"
        self.assertEqual(self.nuwisha.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Nuwisha.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("latrani", breeds)
        # Nuwisha cannot be metis
        self.assertEqual(len(breeds), 2)

    def test_roles_list(self):
        """Test available roles."""
        roles = dict(Nuwisha.ROLES)
        self.assertIn("kojubat", roles)
        self.assertIn("kitmoti", roles)
        self.assertIn("umbagi", roles)


class TestNuwishaDetailView(TestCase):
    """Tests for Nuwisha detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.nuwisha = Nuwisha.objects.create(
            name="Test Nuwisha",
            owner=self.player,
            status="App",
        )

    def test_nuwisha_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.nuwisha.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_nuwisha_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.nuwisha.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
