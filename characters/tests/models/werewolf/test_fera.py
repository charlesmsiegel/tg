"""Tests for Fera base class module."""

from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gift import Gift, GiftPermission
from characters.models.werewolf.rite import Rite
from django.contrib.auth.models import User
from django.test import TestCase
from items.models.werewolf.fetish import Fetish


class TestFera(TestCase):
    """Tests for Fera base class functionality."""

    def setUp(self):
        self.player = User.objects.create_user(username="TestPlayer")
        self.fera = Fera.objects.create(name="Test Fera", owner=self.player)

    def test_fera_creation(self):
        """Test basic Fera creation."""
        self.assertEqual(self.fera.name, "Test Fera")
        self.assertEqual(self.fera.type, "fera")
        self.assertEqual(self.fera.freebie_step, 8)

    def test_fera_default_values(self):
        """Test default values for Fera."""
        self.assertEqual(self.fera.gnosis, 0)
        self.assertEqual(self.fera.rage, 0)
        self.assertEqual(self.fera.renown, 0)
        self.assertEqual(self.fera.temporary_renown, 0)
        self.assertEqual(self.fera.breed, "")
        self.assertEqual(self.fera.faction, "")

    def test_add_gnosis(self):
        """Test adding gnosis."""
        self.assertEqual(self.fera.gnosis, 0)
        self.assertTrue(self.fera.add_gnosis())
        self.assertEqual(self.fera.gnosis, 1)
        # Add up to 10
        for _ in range(9):
            self.fera.add_gnosis()
        self.assertEqual(self.fera.gnosis, 10)
        # Cannot exceed 10
        self.assertFalse(self.fera.add_gnosis())
        self.assertEqual(self.fera.gnosis, 10)

    def test_set_gnosis(self):
        """Test setting gnosis directly."""
        self.assertTrue(self.fera.set_gnosis(5))
        self.assertEqual(self.fera.gnosis, 5)

    def test_add_rage(self):
        """Test adding rage."""
        self.assertEqual(self.fera.rage, 0)
        self.assertTrue(self.fera.add_rage())
        self.assertEqual(self.fera.rage, 1)
        # Add up to 10
        for _ in range(9):
            self.fera.add_rage()
        self.assertEqual(self.fera.rage, 10)
        # Cannot exceed 10
        self.assertFalse(self.fera.add_rage())
        self.assertEqual(self.fera.rage, 10)

    def test_set_rage(self):
        """Test setting rage directly."""
        self.assertTrue(self.fera.set_rage(5))
        self.assertEqual(self.fera.rage, 5)

    def test_has_breed(self):
        """Test breed check."""
        self.assertFalse(self.fera.has_breed())
        self.fera.breed = "homid"
        self.fera.save()
        self.assertTrue(self.fera.has_breed())

    def test_has_faction(self):
        """Test faction check."""
        self.assertFalse(self.fera.has_faction())
        self.fera.faction = "test_faction"
        self.fera.save()
        self.assertTrue(self.fera.has_faction())

    def test_add_gift(self):
        """Test adding gifts."""
        gift = Gift.objects.create(name="Test Fera Gift", rank=1)
        self.assertEqual(self.fera.gifts.count(), 0)
        self.assertTrue(self.fera.add_gift(gift))
        self.assertEqual(self.fera.gifts.count(), 1)
        self.assertIn(gift, self.fera.gifts.all())
        # Cannot add same gift twice
        self.assertFalse(self.fera.add_gift(gift))
        self.assertEqual(self.fera.gifts.count(), 1)

    def test_filter_gifts(self):
        """Test filtering available gifts."""
        permission = GiftPermission.objects.create(shifter="fera", condition="test")
        gift1 = Gift.objects.create(name="Available Gift", rank=1)
        gift1.allowed.add(permission)
        gift2 = Gift.objects.create(name="Unavailable Gift", rank=1)
        self.fera.gift_permissions.add(permission)

        available = self.fera.filter_gifts()
        self.assertIn(gift1, available)
        self.assertNotIn(gift2, available)

        # After adding gift, it should no longer appear
        self.fera.add_gift(gift1)
        available = self.fera.filter_gifts()
        self.assertNotIn(gift1, available)

    def test_add_rite(self):
        """Test adding rites."""
        rite = Rite.objects.create(name="Test Fera Rite", level=1)
        self.assertEqual(self.fera.rites_known.count(), 0)
        self.assertTrue(self.fera.add_rite(rite))
        self.assertEqual(self.fera.rites_known.count(), 1)
        self.assertIn(rite, self.fera.rites_known.all())

    def test_filter_rites(self):
        """Test filtering available rites."""
        rite1 = Rite.objects.create(name="Rite A", level=1)
        rite2 = Rite.objects.create(name="Rite B", level=2)

        available = self.fera.filter_rites()
        self.assertIn(rite1, available)
        self.assertIn(rite2, available)

        self.fera.add_rite(rite1)
        available = self.fera.filter_rites()
        self.assertNotIn(rite1, available)
        self.assertIn(rite2, available)

    def test_add_fetish(self):
        """Test adding fetishes."""
        fetish = Fetish.objects.create(name="Test Fetish", rank=1, gnosis=1)
        self.assertEqual(self.fera.fetishes_owned.count(), 0)
        self.assertTrue(self.fera.add_fetish(fetish))
        self.assertEqual(self.fera.fetishes_owned.count(), 1)
        # Cannot add same fetish twice
        self.assertFalse(self.fera.add_fetish(fetish))
        self.assertEqual(self.fera.fetishes_owned.count(), 1)

    def test_filter_fetishes(self):
        """Test filtering available fetishes by rating."""
        fetish1 = Fetish.objects.create(name="Rank 1 Fetish", rank=1, gnosis=1)
        fetish2 = Fetish.objects.create(name="Rank 3 Fetish", rank=3, gnosis=3)
        fetish3 = Fetish.objects.create(name="Rank 5 Fetish", rank=5, gnosis=5)

        # Filter by range
        available = self.fera.filter_fetishes(min_rating=1, max_rating=3)
        self.assertIn(fetish1, available)
        self.assertIn(fetish2, available)
        self.assertNotIn(fetish3, available)

        # Owned fetishes excluded
        self.fera.add_fetish(fetish1)
        available = self.fera.filter_fetishes(min_rating=0, max_rating=5)
        self.assertNotIn(fetish1, available)

    def test_total_fetish_rating(self):
        """Test calculating total fetish rating."""
        self.assertEqual(self.fera.total_fetish_rating(), 0)

        fetish1 = Fetish.objects.create(name="Rank 2 Fetish", rank=2, gnosis=2)
        fetish2 = Fetish.objects.create(name="Rank 3 Fetish", rank=3, gnosis=3)

        self.fera.add_fetish(fetish1)
        self.assertEqual(self.fera.total_fetish_rating(), 2)

        self.fera.add_fetish(fetish2)
        self.assertEqual(self.fera.total_fetish_rating(), 5)
