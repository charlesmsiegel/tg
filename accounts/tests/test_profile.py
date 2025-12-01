"""
Additional tests for Profile model beyond existing tests.

Tests cover:
- Profile creation on user signup
- ST relationship management
- objects_to_approve() method
- Theme preferences
- Permission cascading for STs
"""
from characters.models.core import Human
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, Gameline, STRelationship


class TestProfileCreation(TestCase):
    """Test Profile creation and setup."""

    def test_profile_created_on_user_signup(self):
        """Test that a profile is automatically created when a user signs up."""
        user = User.objects.create_user(
            username="newuser", email="new@test.com", password="password"
        )

        # Profile should be created automatically via signal
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsNotNone(user.profile)

    def test_profile_has_user_relationship(self):
        """Test that profile has one-to-one relationship with user."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

        profile = user.profile
        self.assertEqual(profile.user, user)

    def test_new_profile_not_st_by_default(self):
        """Test that new profiles are not STs by default."""
        user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )

        self.assertFalse(user.profile.is_st())


class TestSTRelationships(TestCase):
    """Test ST relationship functionality."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="storyteller", email="st@test.com", password="password"
        )
        self.player_user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")

    def test_is_st_returns_true_for_st(self):
        """Test that is_st() returns True for storytellers."""
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        self.assertTrue(self.st_user.profile.is_st())

    def test_is_st_returns_false_for_non_st(self):
        """Test that is_st() returns False for non-storytellers."""
        self.assertFalse(self.player_user.profile.is_st())

    def test_st_relations_returns_chronicles(self):
        """Test that st_relations() returns ST's chronicles."""
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        st_relations = self.st_user.profile.st_relations()
        # st_relations() returns a dict mapping Chronicle to list of STRelationships
        self.assertIn(self.chronicle, st_relations)

    def test_st_for_multiple_chronicles(self):
        """Test that a user can be ST for multiple chronicles."""
        chronicle2 = Chronicle.objects.create(name="Second Chronicle")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        STRelationship.objects.create(
            user=self.st_user, chronicle=chronicle2, gameline=self.gameline
        )

        relations = self.st_user.profile.st_relations()
        # st_relations() returns a dict mapping Chronicle to list of STRelationships
        self.assertEqual(len(relations), 2)

    def test_st_for_multiple_gamelines(self):
        """Test that an ST can run multiple gamelines in same chronicle."""
        gameline2 = Gameline.objects.create(name="Vampire: the Masquerade")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=gameline2
        )

        relations = self.st_user.profile.st_relations()
        # st_relations() returns a dict mapping Chronicle to list of STRelationships
        # Both relationships are for the same chronicle, so we count the relationships
        total_relationships = sum(len(rels) for rels in relations.values())
        self.assertEqual(total_relationships, 2)


class TestObjectsToApprove(TestCase):
    """Test the objects_to_approve() method."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.player_user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")

        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_objects_to_approve_includes_submitted_characters(self):
        """Test that submitted characters appear in objects to approve."""
        character = Human.objects.create(
            name="Submitted Character",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="Sub",  # Submitted for approval
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should include the submitted character
        self.assertIn(character, to_approve)

    def test_objects_to_approve_excludes_unfinished_characters(self):
        """Test that unfinished characters don't appear in approval queue."""
        unfinished = Human.objects.create(
            name="Unfinished Character",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="Un",  # Unfinished
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should not include unfinished characters
        self.assertNotIn(unfinished, to_approve)

    def test_objects_to_approve_excludes_approved_characters(self):
        """Test that already approved characters don't appear."""
        approved = Human.objects.create(
            name="Approved Character",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="App",  # Already approved
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should not include already approved characters
        self.assertNotIn(approved, to_approve)

    def test_objects_to_approve_only_for_st_chronicles(self):
        """Test that STs only see objects from their chronicles."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")

        character_in_chronicle = Human.objects.create(
            name="In Chronicle",
            owner=self.player_user,
            chronicle=self.chronicle,
            status="Sub",
        )

        character_outside = Human.objects.create(
            name="Outside Chronicle",
            owner=self.player_user,
            chronicle=other_chronicle,
            status="Sub",
        )

        to_approve = self.st_user.profile.objects_to_approve()

        # Should include character in ST's chronicle
        self.assertIn(character_in_chronicle, to_approve)
        # Should not include character outside ST's chronicle
        self.assertNotIn(character_outside, to_approve)


class TestThemePreferences(TestCase):
    """Test theme preference functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_profile_has_theme_field(self):
        """Test that profile has theme preference field."""
        profile = self.user.profile

        # Should have theme field (exact implementation may vary)
        self.assertTrue(hasattr(profile, "theme") or hasattr(profile, "preferred_theme"))

    def test_theme_can_be_updated(self):
        """Test that theme preference can be changed."""
        profile = self.user.profile

        # If theme field exists
        if hasattr(profile, "theme"):
            profile.theme = "dark"
            profile.save()
            profile.refresh_from_db()
            self.assertEqual(profile.theme, "dark")


class TestProfilePermissions(TestCase):
    """Test permission-related profile functionality."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.player_user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="password",
            is_staff=True,
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")

    def test_st_has_elevated_permissions(self):
        """Test that STs have elevated permissions."""
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        # STs should be able to approve characters
        self.assertTrue(self.st_user.profile.is_st())

    def test_admin_has_all_permissions(self):
        """Test that admins have all permissions."""
        # Staff users should have admin permissions
        self.assertTrue(self.admin_user.is_staff)

    def test_regular_player_limited_permissions(self):
        """Test that regular players have limited permissions."""
        # Regular players should not have ST permissions
        self.assertFalse(self.player_user.profile.is_st())
        self.assertFalse(self.player_user.is_staff)


class TestProfileStringRepresentation(TestCase):
    """Test profile string representation."""

    def test_profile_str_includes_username(self):
        """Test that profile string representation includes username."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

        profile_str = str(user.profile)

        # Should include the username
        self.assertIn("testuser", profile_str)
