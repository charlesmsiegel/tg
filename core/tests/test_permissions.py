"""
Unit tests for permissions system.
"""

from characters.models import Character
from core.models import Observer
from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class TestPermissionManager(TestCase):
    """Tests for PermissionManager core functionality."""

    def setUp(self):
        """Create test users and data."""
        self.users = {
            "owner": User.objects.create_user("owner", "owner@test.com"),
            "head_st": User.objects.create_user("head_st", "head_st@test.com"),
            "game_st": User.objects.create_user("game_st", "game_st@test.com"),
            "player": User.objects.create_user("player", "player@test.com"),
            "observer": User.objects.create_user("observer", "observer@test.com"),
            "stranger": User.objects.create_user("stranger", "stranger@test.com"),
            "admin": User.objects.create_user("admin", "admin@test.com", is_staff=True),
        }

        # Create test chronicle
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle", head_st=self.users["head_st"]
        )
        # Add game ST
        self.chronicle.game_storytellers.add(self.users["game_st"])

        # Create test character
        self.character = Character.objects.create(
            name="Test Character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
        )

        # Add observer
        self.character.add_observer(self.users["observer"], self.users["owner"])

        # Add player character to chronicle
        Character.objects.create(
            name="Player's Character",
            owner=self.users["player"],
            chronicle=self.chronicle,
            status="App",
        )

    # Role Detection Tests

    def test_role_detection_owner(self):
        """Test that owner role is detected."""
        roles = PermissionManager.get_user_roles(self.users["owner"], self.character)
        self.assertIn(Role.OWNER, roles)

    def test_role_detection_head_st(self):
        """Test that chronicle head ST role is detected."""
        roles = PermissionManager.get_user_roles(self.users["head_st"], self.character)
        self.assertIn(Role.CHRONICLE_HEAD_ST, roles)

    def test_role_detection_game_st(self):
        """Test that game ST role is detected."""
        roles = PermissionManager.get_user_roles(self.users["game_st"], self.character)
        self.assertIn(Role.GAME_ST, roles)

    def test_role_detection_player(self):
        """Test that player role is detected."""
        roles = PermissionManager.get_user_roles(self.users["player"], self.character)
        self.assertIn(Role.PLAYER, roles)

    def test_role_detection_observer(self):
        """Test that observer role is detected."""
        roles = PermissionManager.get_user_roles(self.users["observer"], self.character)
        self.assertIn(Role.OBSERVER, roles)

    def test_role_detection_stranger(self):
        """Test that stranger has no special roles."""
        roles = PermissionManager.get_user_roles(self.users["stranger"], self.character)
        self.assertNotIn(Role.OWNER, roles)
        self.assertNotIn(Role.CHRONICLE_HEAD_ST, roles)
        self.assertNotIn(Role.GAME_ST, roles)
        self.assertNotIn(Role.PLAYER, roles)
        self.assertNotIn(Role.OBSERVER, roles)
        self.assertIn(Role.AUTHENTICATED, roles)

    # Owner Permission Tests

    def test_owner_can_view_full(self):
        """Test owner has full view permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.VIEW_FULL
            )
        )

    def test_owner_cannot_edit_full(self):
        """Test owner does NOT have full edit permission."""
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.EDIT_FULL
            )
        )

    def test_owner_can_edit_limited(self):
        """Test owner has limited edit permission (notes/journals)."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.EDIT_LIMITED
            )
        )

    def test_owner_can_spend_xp_when_approved(self):
        """Test owner can spend XP on approved character."""
        self.character.status = "App"
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )

    def test_owner_cannot_spend_xp_when_unfinished(self):
        """Test owner cannot spend XP on unfinished character."""
        self.character.status = "Un"
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )

    def test_owner_can_spend_freebies_when_unfinished(self):
        """Test owner can spend freebies on unfinished character."""
        self.character.status = "Un"
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_FREEBIES
            )
        )

    # ST Permission Tests

    def test_head_st_can_view_full(self):
        """Test head ST has full view permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["head_st"], self.character, Permission.VIEW_FULL
            )
        )

    def test_head_st_can_edit_full(self):
        """Test head ST has full edit permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["head_st"], self.character, Permission.EDIT_FULL
            )
        )

    def test_game_st_can_view_full(self):
        """Test game ST has full view permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["game_st"], self.character, Permission.VIEW_FULL
            )
        )

    def test_game_st_cannot_edit(self):
        """Test game ST does NOT have edit permission (read-only)."""
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["game_st"], self.character, Permission.EDIT_FULL
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["game_st"], self.character, Permission.EDIT_LIMITED
            )
        )

    def test_head_st_can_approve(self):
        """Test head ST has approve permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["head_st"], self.character, Permission.APPROVE
            )
        )

    # Player and Observer Permission Tests

    def test_player_can_view_partial(self):
        """Test player has partial view permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["player"], self.character, Permission.VIEW_PARTIAL
            )
        )

    def test_player_cannot_view_full(self):
        """Test player does NOT have full view permission."""
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["player"], self.character, Permission.VIEW_FULL
            )
        )

    def test_player_cannot_edit(self):
        """Test player cannot edit."""
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["player"], self.character, Permission.EDIT_FULL
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["player"], self.character, Permission.EDIT_LIMITED
            )
        )

    def test_observer_can_view_partial(self):
        """Test observer has partial view permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["observer"], self.character, Permission.VIEW_PARTIAL
            )
        )

    def test_stranger_cannot_view(self):
        """Test stranger has no view permission."""
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["stranger"], self.character, Permission.VIEW_FULL
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["stranger"], self.character, Permission.VIEW_PARTIAL
            )
        )

    # Admin Permission Tests

    def test_admin_can_do_everything(self):
        """Test admin has all permissions."""
        admin = self.users["admin"]
        self.assertTrue(
            PermissionManager.user_has_permission(admin, self.character, Permission.VIEW_FULL)
        )
        self.assertTrue(
            PermissionManager.user_has_permission(admin, self.character, Permission.EDIT_FULL)
        )
        self.assertTrue(
            PermissionManager.user_has_permission(admin, self.character, Permission.DELETE)
        )
        self.assertTrue(
            PermissionManager.user_has_permission(admin, self.character, Permission.APPROVE)
        )

    # Visibility Tier Tests

    def test_visibility_tier_owner(self):
        """Test owner gets FULL visibility tier."""
        tier = PermissionManager.get_visibility_tier(self.users["owner"], self.character)
        self.assertEqual(tier, VisibilityTier.FULL)

    def test_visibility_tier_game_st(self):
        """Test game ST gets FULL visibility tier (but can't edit)."""
        tier = PermissionManager.get_visibility_tier(self.users["game_st"], self.character)
        self.assertEqual(tier, VisibilityTier.FULL)

    def test_visibility_tier_player(self):
        """Test player gets PARTIAL visibility tier."""
        tier = PermissionManager.get_visibility_tier(self.users["player"], self.character)
        self.assertEqual(tier, VisibilityTier.PARTIAL)

    def test_visibility_tier_stranger(self):
        """Test stranger gets NONE visibility tier."""
        tier = PermissionManager.get_visibility_tier(self.users["stranger"], self.character)
        self.assertEqual(tier, VisibilityTier.NONE)

    # Status-Based Restriction Tests

    def test_status_restriction_submitted(self):
        """Test owner cannot spend XP/freebies on submitted character."""
        self.character.status = "Sub"
        self.character.save()

        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_FREEBIES
            )
        )

        # But head ST still can
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["head_st"], self.character, Permission.EDIT_FULL
            )
        )

    def test_status_restriction_deceased(self):
        """Test owner cannot edit deceased character, but head ST and admin can."""
        self.character.status = "Dec"
        self.character.save()

        # Owner cannot edit
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.EDIT_LIMITED
            )
        )

        # Head ST can still edit (configurable)
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["head_st"], self.character, Permission.EDIT_FULL
            )
        )

        # Admin can still edit
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["admin"], self.character, Permission.EDIT_FULL
            )
        )

    # Observer Management Tests

    def test_add_observer(self):
        """Test adding an observer."""
        new_observer = User.objects.create_user("new_obs", "obs@test.com")

        # Add as observer
        self.character.add_observer(new_observer, self.users["owner"])

        # Check observer can view
        self.assertTrue(
            PermissionManager.user_has_permission(
                new_observer, self.character, Permission.VIEW_PARTIAL
            )
        )

    def test_remove_observer(self):
        """Test removing an observer."""
        # Remove existing observer
        self.character.remove_observer(self.users["observer"])

        # Check observer can no longer view
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["observer"], self.character, Permission.VIEW_PARTIAL
            )
        )

    # Model Method Tests

    def test_model_user_can_view(self):
        """Test model's user_can_view method."""
        self.assertTrue(self.character.user_can_view(self.users["owner"]))
        self.assertTrue(self.character.user_can_view(self.users["head_st"]))
        self.assertFalse(self.character.user_can_view(self.users["stranger"]))

    def test_model_user_can_edit(self):
        """Test model's user_can_edit method (EDIT_FULL)."""
        self.assertFalse(self.character.user_can_edit(self.users["owner"]))
        self.assertTrue(self.character.user_can_edit(self.users["head_st"]))
        self.assertFalse(self.character.user_can_edit(self.users["game_st"]))

    def test_model_user_can_spend_xp(self):
        """Test model's user_can_spend_xp method."""
        self.character.status = "App"
        self.assertTrue(self.character.user_can_spend_xp(self.users["owner"]))
        self.assertFalse(self.character.user_can_spend_xp(self.users["player"]))

    def test_model_user_can_spend_freebies(self):
        """Test model's user_can_spend_freebies method."""
        self.character.status = "Un"
        self.assertTrue(self.character.user_can_spend_freebies(self.users["owner"]))
        self.character.status = "App"
        self.assertFalse(self.character.user_can_spend_freebies(self.users["owner"]))
