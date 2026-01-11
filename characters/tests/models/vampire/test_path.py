"""
Tests for Path of Enlightenment model.

Tests cover:
- Path creation and basic attributes
- Virtue requirements (Conviction/Conscience, Instinct/Self-Control)
- Character virtue checking
- Character virtue updating
- Virtue display methods
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.vampire.path import Path
from characters.models.vampire.vampire import Vampire


class PathModelTestCase(TestCase):
    """Base test case with common setup for Path model tests."""

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )


class TestPathCreation(PathModelTestCase):
    """Test Path model creation and basic attributes."""

    def test_path_creation_basic(self):
        """Test basic path creation."""
        path = Path.objects.create(
            name="Path of Caine",
            ethics="Follow the ways of the First Vampire",
        )
        self.assertEqual(path.name, "Path of Caine")
        self.assertEqual(path.ethics, "Follow the ways of the First Vampire")
        self.assertEqual(path.type, "path")
        self.assertEqual(path.gameline, "vtm")

    def test_path_requires_conviction_default(self):
        """Test that requires_conviction defaults to True."""
        path = Path.objects.create(name="Test Path")
        self.assertTrue(path.requires_conviction)

    def test_path_requires_instinct_default(self):
        """Test that requires_instinct defaults to True."""
        path = Path.objects.create(name="Test Path")
        self.assertTrue(path.requires_instinct)

    def test_path_str(self):
        """Test path string representation."""
        path = Path.objects.create(name="Path of Honorable Accord")
        self.assertEqual(str(path), "Path of Honorable Accord")

    def test_path_get_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        path = Path.objects.create(name="Test Path")
        expected_url = f"/characters/vampire/path/{path.id}/"
        self.assertEqual(path.get_absolute_url(), expected_url)

    def test_path_get_update_url(self):
        """Test that get_update_url returns correct path."""
        path = Path.objects.create(name="Test Path")
        expected_url = f"/characters/vampire/update/path/{path.pk}/"
        self.assertEqual(path.get_update_url(), expected_url)

    def test_path_get_creation_url(self):
        """Test that get_creation_url returns correct path."""
        expected_url = "/characters/vampire/create/path/"
        self.assertEqual(Path.get_creation_url(), expected_url)

    def test_path_get_heading(self):
        """Test that get_heading returns vtm_heading."""
        path = Path.objects.create(name="Test Path")
        self.assertEqual(path.get_heading(), "vtm_heading")


class TestPathVirtueConfigurations(PathModelTestCase):
    """Test different virtue requirement configurations."""

    def test_path_conviction_instinct(self):
        """Test path requiring Conviction and Instinct."""
        path = Path.objects.create(
            name="Path of Caine",
            requires_conviction=True,
            requires_instinct=True,
        )
        self.assertTrue(path.requires_conviction)
        self.assertTrue(path.requires_instinct)

    def test_path_conviction_self_control(self):
        """Test path requiring Conviction and Self-Control."""
        path = Path.objects.create(
            name="Path of the Feral Heart",
            requires_conviction=True,
            requires_instinct=False,
        )
        self.assertTrue(path.requires_conviction)
        self.assertFalse(path.requires_instinct)

    def test_path_conscience_instinct(self):
        """Test path requiring Conscience and Instinct."""
        path = Path.objects.create(
            name="Path of Cathari",
            requires_conviction=False,
            requires_instinct=True,
        )
        self.assertFalse(path.requires_conviction)
        self.assertTrue(path.requires_instinct)

    def test_path_conscience_self_control(self):
        """Test path requiring Conscience and Self-Control (like Humanity)."""
        path = Path.objects.create(
            name="Path of Humanity",
            requires_conviction=False,
            requires_instinct=False,
        )
        self.assertFalse(path.requires_conviction)
        self.assertFalse(path.requires_instinct)


class TestPathCheckCharacterVirtues(PathModelTestCase):
    """Test check_character_virtues method."""

    def test_check_virtues_matching_conviction_instinct(self):
        """Test check_character_virtues returns True when virtues match."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=True,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=True,
            has_instinct=True,
        )
        self.assertTrue(path.check_character_virtues(vampire))

    def test_check_virtues_matching_conscience_self_control(self):
        """Test check_character_virtues for Humanity-like path."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=False,
            requires_instinct=False,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,
            has_instinct=False,
        )
        self.assertTrue(path.check_character_virtues(vampire))

    def test_check_virtues_mismatched_first_virtue(self):
        """Test check_character_virtues returns False when first virtue mismatched."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=True,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,  # Mismatch
            has_instinct=True,
        )
        self.assertFalse(path.check_character_virtues(vampire))

    def test_check_virtues_mismatched_second_virtue(self):
        """Test check_character_virtues returns False when second virtue mismatched."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=True,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=True,
            has_instinct=False,  # Mismatch
        )
        self.assertFalse(path.check_character_virtues(vampire))

    def test_check_virtues_both_mismatched(self):
        """Test check_character_virtues returns False when both virtues mismatched."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=True,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,
            has_instinct=False,
        )
        self.assertFalse(path.check_character_virtues(vampire))


class TestPathUpdateCharacterVirtues(PathModelTestCase):
    """Test update_character_virtues method."""

    def test_update_virtues_to_conviction(self):
        """Test updating character from Conscience to Conviction."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=False,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,
            conscience=3,
        )

        changed = path.update_character_virtues(vampire)

        self.assertTrue(changed)
        self.assertTrue(vampire.has_conviction)
        self.assertEqual(vampire.conscience, 0)  # Reset

    def test_update_virtues_to_conscience(self):
        """Test updating character from Conviction to Conscience."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=False,
            requires_instinct=False,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=True,
            conviction=4,
        )

        changed = path.update_character_virtues(vampire)

        self.assertTrue(changed)
        self.assertFalse(vampire.has_conviction)
        self.assertEqual(vampire.conviction, 0)  # Reset

    def test_update_virtues_to_instinct(self):
        """Test updating character from Self-Control to Instinct."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=False,
            requires_instinct=True,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_instinct=False,
            self_control=3,
        )

        changed = path.update_character_virtues(vampire)

        self.assertTrue(changed)
        self.assertTrue(vampire.has_instinct)
        self.assertEqual(vampire.self_control, 0)  # Reset

    def test_update_virtues_to_self_control(self):
        """Test updating character from Instinct to Self-Control."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=False,
            requires_instinct=False,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_instinct=True,
            instinct=4,
        )

        changed = path.update_character_virtues(vampire)

        self.assertTrue(changed)
        self.assertFalse(vampire.has_instinct)
        self.assertEqual(vampire.instinct, 0)  # Reset

    def test_update_virtues_no_change_needed(self):
        """Test update_character_virtues returns False when no change needed."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=True,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=True,
            has_instinct=True,
        )

        changed = path.update_character_virtues(vampire)

        self.assertFalse(changed)

    def test_update_virtues_both_changed(self):
        """Test updating both virtue pairs."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=True,
        )
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,
            has_instinct=False,
            conscience=3,
            self_control=4,
        )

        changed = path.update_character_virtues(vampire)

        self.assertTrue(changed)
        self.assertTrue(vampire.has_conviction)
        self.assertTrue(vampire.has_instinct)
        self.assertEqual(vampire.conscience, 0)
        self.assertEqual(vampire.self_control, 0)


class TestPathGetVirtuesDisplay(PathModelTestCase):
    """Test get_virtues_display method."""

    def test_get_virtues_display_conviction_instinct(self):
        """Test virtue display for Conviction and Instinct."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=True,
        )
        self.assertEqual(path.get_virtues_display(), "Conviction and Instinct")

    def test_get_virtues_display_conviction_self_control(self):
        """Test virtue display for Conviction and Self-Control."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=True,
            requires_instinct=False,
        )
        self.assertEqual(path.get_virtues_display(), "Conviction and Self-Control")

    def test_get_virtues_display_conscience_instinct(self):
        """Test virtue display for Conscience and Instinct."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=False,
            requires_instinct=True,
        )
        self.assertEqual(path.get_virtues_display(), "Conscience and Instinct")

    def test_get_virtues_display_conscience_self_control(self):
        """Test virtue display for Conscience and Self-Control."""
        path = Path.objects.create(
            name="Test",
            requires_conviction=False,
            requires_instinct=False,
        )
        self.assertEqual(path.get_virtues_display(), "Conscience and Self-Control")


class TestPathOrdering(PathModelTestCase):
    """Test Path model ordering."""

    def test_paths_ordered_by_name(self):
        """Test that paths are ordered by name."""
        path_c = Path.objects.create(name="Path of Cathari")
        path_a = Path.objects.create(name="Path of Asakku")
        path_b = Path.objects.create(name="Path of Blood")

        paths = list(Path.objects.all())
        self.assertEqual(paths[0], path_a)
        self.assertEqual(paths[1], path_b)
        self.assertEqual(paths[2], path_c)


class TestPathFollowers(PathModelTestCase):
    """Test followers relationship."""

    def test_path_can_have_followers(self):
        """Test that followers relationship is accessible."""
        path = Path.objects.create(name="Path of Caine")

        vampire1 = Vampire.objects.create(
            name="Follower 1",
            owner=self.user,
            path=path,
            path_rating=4,
            conscience=1,
            self_control=1,
            courage=1,
        )
        vampire2 = Vampire.objects.create(
            name="Follower 2",
            owner=self.user,
            path=path,
            path_rating=4,
            conscience=1,
            self_control=1,
            courage=1,
        )

        followers = list(path.followers.all())
        self.assertEqual(len(followers), 2)
        self.assertIn(vampire1, followers)
        self.assertIn(vampire2, followers)
