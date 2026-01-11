"""Tests for LoreBlock mixin."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.demon import Demon


class LoreBlockTests(TestCase):
    """Tests for LoreBlock mixin functionality via Demon model."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_all_lores_default_to_zero(self):
        """All lore fields should default to 0."""
        lores = self.demon.get_lores()
        for lore_name, value in lores.items():
            self.assertEqual(value, 0, f"{lore_name} should default to 0")

    def test_get_lores_returns_all_23_lores(self):
        """get_lores should return all 23 lore types."""
        lores = self.demon.get_lores()
        self.assertEqual(len(lores), 23)

    def test_get_lores_contains_expected_lores(self):
        """get_lores should contain all expected lore types."""
        lores = self.demon.get_lores()
        expected_lores = [
            "lore_of_awakening",
            "lore_of_the_beast",
            "lore_of_the_celestials",
            "lore_of_death",
            "lore_of_the_earth",
            "lore_of_flame",
            "lore_of_the_firmament",
            "lore_of_the_flesh",
            "lore_of_the_forge",
            "lore_of_the_fundament",
            "lore_of_humanity",
            "lore_of_light",
            "lore_of_longing",
            "lore_of_paths",
            "lore_of_patterns",
            "lore_of_portals",
            "lore_of_radiance",
            "lore_of_the_realms",
            "lore_of_the_spirit",
            "lore_of_storms",
            "lore_of_transfiguration",
            "lore_of_the_wild",
            "lore_of_the_winds",
        ]
        for expected in expected_lores:
            self.assertIn(expected, lores, f"{expected} should be in lores")


class LoreBlockTotalLoresTests(TestCase):
    """Tests for total_lores method."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_total_lores_zero_initially(self):
        """total_lores should return 0 when no lores are set."""
        self.assertEqual(self.demon.total_lores(), 0)

    def test_total_lores_single_lore(self):
        """total_lores should count a single lore rating."""
        self.demon.lore_of_flame = 3
        self.demon.save()
        self.assertEqual(self.demon.total_lores(), 3)

    def test_total_lores_multiple_lores(self):
        """total_lores should sum all lore ratings."""
        self.demon.lore_of_flame = 3
        self.demon.lore_of_light = 2
        self.demon.lore_of_the_fundament = 1
        self.demon.save()
        self.assertEqual(self.demon.total_lores(), 6)

    def test_total_lores_all_lores_set(self):
        """total_lores should correctly sum all lores when all are set."""
        # Set each lore to 1
        lores = self.demon.get_lores()
        for lore_name in lores.keys():
            setattr(self.demon, lore_name, 1)
        self.demon.save()
        self.assertEqual(self.demon.total_lores(), 23)


class LoreBlockAddLoreTests(TestCase):
    """Tests for add_lore method."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_add_lore_increases_rating(self):
        """add_lore should increase lore rating by 1."""
        initial = self.demon.lore_of_flame
        result = self.demon.add_lore("lore_of_flame")
        self.assertTrue(result)
        self.assertEqual(self.demon.lore_of_flame, initial + 1)

    def test_add_lore_from_zero_to_one(self):
        """add_lore should increase from 0 to 1."""
        self.assertEqual(self.demon.lore_of_death, 0)
        self.demon.add_lore("lore_of_death")
        self.assertEqual(self.demon.lore_of_death, 1)

    def test_add_lore_multiple_times(self):
        """add_lore can be called multiple times."""
        for i in range(3):
            self.demon.add_lore("lore_of_patterns")
        self.assertEqual(self.demon.lore_of_patterns, 3)

    def test_add_lore_respects_maximum(self):
        """add_lore should not exceed the maximum."""
        self.demon.lore_of_flame = 5
        result = self.demon.add_lore("lore_of_flame")
        self.assertFalse(result)
        self.assertEqual(self.demon.lore_of_flame, 5)

    def test_add_lore_custom_maximum(self):
        """add_lore can have a custom maximum."""
        self.demon.lore_of_flame = 3
        result = self.demon.add_lore("lore_of_flame", maximum=3)
        self.assertFalse(result)
        self.assertEqual(self.demon.lore_of_flame, 3)


class LoreBlockFilterLoresTests(TestCase):
    """Tests for filter_lores method."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)
        # Set up some lores with various ratings
        self.demon.lore_of_flame = 3
        self.demon.lore_of_light = 2
        self.demon.lore_of_death = 5
        self.demon.lore_of_patterns = 1
        self.demon.save()

    def test_filter_lores_default_returns_all(self):
        """filter_lores with defaults returns all lores."""
        filtered = self.demon.filter_lores()
        self.assertEqual(len(filtered), 23)

    def test_filter_lores_minimum_one(self):
        """filter_lores with minimum=1 returns only lores >= 1."""
        filtered = self.demon.filter_lores(minimum=1)
        self.assertEqual(len(filtered), 4)
        self.assertIn("lore_of_flame", filtered)
        self.assertIn("lore_of_light", filtered)
        self.assertIn("lore_of_death", filtered)
        self.assertIn("lore_of_patterns", filtered)

    def test_filter_lores_minimum_three(self):
        """filter_lores with minimum=3 returns only lores >= 3."""
        filtered = self.demon.filter_lores(minimum=3)
        self.assertEqual(len(filtered), 2)
        self.assertIn("lore_of_flame", filtered)
        self.assertIn("lore_of_death", filtered)

    def test_filter_lores_maximum_two(self):
        """filter_lores with maximum=2 returns only lores <= 2."""
        filtered = self.demon.filter_lores(maximum=2)
        # All 0-rated lores (19) + lore_of_light (2) + lore_of_patterns (1) = 21
        self.assertEqual(len(filtered), 21)
        self.assertNotIn("lore_of_flame", filtered)
        self.assertNotIn("lore_of_death", filtered)

    def test_filter_lores_range(self):
        """filter_lores with minimum and maximum returns lores in range."""
        filtered = self.demon.filter_lores(minimum=2, maximum=4)
        self.assertEqual(len(filtered), 2)
        self.assertIn("lore_of_flame", filtered)
        self.assertIn("lore_of_light", filtered)

    def test_filter_lores_empty_range(self):
        """filter_lores with impossible range returns empty dict."""
        filtered = self.demon.filter_lores(minimum=4, maximum=4)
        self.assertEqual(len(filtered), 0)

    def test_filter_lores_preserves_values(self):
        """filter_lores returns correct values for each lore."""
        filtered = self.demon.filter_lores(minimum=1)
        self.assertEqual(filtered["lore_of_flame"], 3)
        self.assertEqual(filtered["lore_of_light"], 2)
        self.assertEqual(filtered["lore_of_death"], 5)
        self.assertEqual(filtered["lore_of_patterns"], 1)


class LoreBlockFieldAccessTests(TestCase):
    """Tests for direct lore field access."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(name="Test Demon", owner=self.user)

    def test_lore_of_awakening_can_be_set(self):
        """lore_of_awakening can be set and retrieved."""
        self.demon.lore_of_awakening = 4
        self.demon.save()
        self.demon.refresh_from_db()
        self.assertEqual(self.demon.lore_of_awakening, 4)

    def test_lore_of_the_beast_can_be_set(self):
        """lore_of_the_beast can be set and retrieved."""
        self.demon.lore_of_the_beast = 3
        self.demon.save()
        self.demon.refresh_from_db()
        self.assertEqual(self.demon.lore_of_the_beast, 3)

    def test_lore_of_the_celestials_can_be_set(self):
        """lore_of_the_celestials can be set and retrieved."""
        self.demon.lore_of_the_celestials = 2
        self.demon.save()
        self.demon.refresh_from_db()
        self.assertEqual(self.demon.lore_of_the_celestials, 2)

    def test_lore_of_death_can_be_set(self):
        """lore_of_death can be set and retrieved."""
        self.demon.lore_of_death = 5
        self.demon.save()
        self.demon.refresh_from_db()
        self.assertEqual(self.demon.lore_of_death, 5)

    def test_lore_of_the_earth_can_be_set(self):
        """lore_of_the_earth can be set and retrieved."""
        self.demon.lore_of_the_earth = 1
        self.demon.save()
        self.demon.refresh_from_db()
        self.assertEqual(self.demon.lore_of_the_earth, 1)
