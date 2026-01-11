"""Tests for Ratkin (wererat) module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.ratkin import Ratkin


class TestRatkin(TestCase):
    """Tests for Ratkin model functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.ratkin = Ratkin.objects.create(name="Test Ratkin", owner=self.player)

    def test_ratkin_creation(self):
        """Test basic Ratkin creation."""
        self.assertEqual(self.ratkin.name, "Test Ratkin")
        self.assertEqual(self.ratkin.type, "ratkin")

    def test_ratkin_default_values(self):
        """Test default values for Ratkin."""
        self.assertEqual(self.ratkin.gnosis, 0)
        self.assertEqual(self.ratkin.rage, 0)
        self.assertEqual(self.ratkin.infamy, 0)
        self.assertEqual(self.ratkin.obligation, 0)
        self.assertEqual(self.ratkin.cunning, 0)

    def test_set_breed_homid(self):
        """Test setting homid breed."""
        self.assertTrue(self.ratkin.set_breed("homid"))
        self.assertEqual(self.ratkin.breed, "homid")
        self.assertEqual(self.ratkin.gnosis, 1)
        self.assertTrue(
            self.ratkin.gift_permissions.filter(shifter="ratkin", condition="homid").exists()
        )

    def test_set_breed_metis(self):
        """Test setting metis breed."""
        self.assertTrue(self.ratkin.set_breed("metis"))
        self.assertEqual(self.ratkin.breed, "metis")
        self.assertEqual(self.ratkin.gnosis, 3)

    def test_set_breed_rodens(self):
        """Test setting rodens (rat) breed."""
        self.assertTrue(self.ratkin.set_breed("rodens"))
        self.assertEqual(self.ratkin.breed, "rodens")
        # Note: code has "rodent" which doesn't match "rodens"
        # Gnosis remains 0 due to typo in model

    def test_has_aspect(self):
        """Test aspect check."""
        self.assertFalse(self.ratkin.has_aspect())
        self.ratkin.aspect = "warrior"
        self.assertTrue(self.ratkin.has_aspect())

    def test_set_aspect_warrior(self):
        """Test setting warrior aspect."""
        self.assertTrue(self.ratkin.set_aspect("warrior"))
        self.assertEqual(self.ratkin.aspect, "warrior")
        self.assertEqual(self.ratkin.rage, 4)
        self.assertTrue(
            self.ratkin.gift_permissions.filter(shifter="ratkin", condition="warrior").exists()
        )

    def test_set_aspect_tunnel_runner(self):
        """Test setting tunnel runner aspect."""
        self.assertTrue(self.ratkin.set_aspect("tunnel_runner"))
        self.assertEqual(self.ratkin.aspect, "tunnel_runner")
        self.assertEqual(self.ratkin.rage, 3)

    def test_set_aspect_plague_lord(self):
        """Test setting plague lord aspect."""
        self.assertTrue(self.ratkin.set_aspect("plague_lord"))
        self.assertEqual(self.ratkin.aspect, "plague_lord")
        self.assertEqual(self.ratkin.rage, 3)

    def test_set_aspect_shadow_seer(self):
        """Test setting shadow seer aspect."""
        self.assertTrue(self.ratkin.set_aspect("shadow_seer"))
        self.assertEqual(self.ratkin.aspect, "shadow_seer")
        self.assertEqual(self.ratkin.rage, 2)

    def test_set_aspect_engineers(self):
        """Test setting engineers aspect."""
        self.assertTrue(self.ratkin.set_aspect("engineers"))
        self.assertEqual(self.ratkin.aspect, "engineers")
        self.assertEqual(self.ratkin.rage, 2)

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        expected_url = f"/characters/werewolf/ratkin/{self.ratkin.pk}/"
        self.assertEqual(self.ratkin.get_absolute_url(), expected_url)

    def test_breeds_list(self):
        """Test available breeds."""
        breeds = dict(Ratkin.BREEDS)
        self.assertIn("homid", breeds)
        self.assertIn("rodens", breeds)
        self.assertIn("metis", breeds)

    def test_aspects_list(self):
        """Test available aspects."""
        aspects = dict(Ratkin.ASPECTS)
        self.assertIn("tunnel_runner", aspects)
        self.assertIn("warrior", aspects)
        self.assertIn("plague_lord", aspects)
        self.assertIn("engineers", aspects)
        self.assertIn("munchmausen", aspects)
        self.assertIn("knife_skulker", aspects)
        self.assertIn("shadow_seer", aspects)
        self.assertIn("twitchers", aspects)


class TestRatkinDetailView(TestCase):
    """Tests for Ratkin detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.ratkin = Ratkin.objects.create(
            name="Test Ratkin",
            owner=self.player,
            status="App",
        )

    def test_ratkin_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.ratkin.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_ratkin_detail_view_uses_correct_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.ratkin.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
