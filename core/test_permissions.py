"""
Unit tests for permissions system.
"""

import pytest
from django.contrib.auth.models import User
from core.permissions import PermissionManager, Permission, Role, VisibilityTier
from core.models import Observer
from characters.models import Character
from game.models import Chronicle


@pytest.mark.django_db
class TestPermissionManager:
    """Tests for PermissionManager core functionality."""

    @pytest.fixture
    def users(self):
        """Create test users."""
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com'),
            'head_st': User.objects.create_user('head_st', 'head_st@test.com'),
            'game_st': User.objects.create_user('game_st', 'game_st@test.com'),
            'player': User.objects.create_user('player', 'player@test.com'),
            'observer': User.objects.create_user('observer', 'observer@test.com'),
            'stranger': User.objects.create_user('stranger', 'stranger@test.com'),
            'admin': User.objects.create_user(
                'admin', 'admin@test.com', is_staff=True
            ),
        }

    @pytest.fixture
    def chronicle(self, users):
        """Create test chronicle."""
        chron = Chronicle.objects.create(
            name="Test Chronicle",
            head_st=users['head_st']
        )
        # Add game ST
        chron.game_storytellers.add(users['game_st'])
        return chron

    @pytest.fixture
    def character(self, users, chronicle):
        """Create test character."""
        char = Character.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App'
        )

        # Add observer
        char.add_observer(users['observer'], users['owner'])

        # Add player character to chronicle
        Character.objects.create(
            name="Player's Character",
            owner=users['player'],
            chronicle=chronicle,
            status='App'
        )

        return char

    # Role Detection Tests

    def test_role_detection_owner(self, users, character):
        """Test that owner role is detected."""
        roles = PermissionManager.get_user_roles(users['owner'], character)
        assert Role.OWNER in roles

    def test_role_detection_head_st(self, users, character):
        """Test that chronicle head ST role is detected."""
        roles = PermissionManager.get_user_roles(users['head_st'], character)
        assert Role.CHRONICLE_HEAD_ST in roles

    def test_role_detection_game_st(self, users, character):
        """Test that game ST role is detected."""
        roles = PermissionManager.get_user_roles(users['game_st'], character)
        assert Role.GAME_ST in roles

    def test_role_detection_player(self, users, character):
        """Test that player role is detected."""
        roles = PermissionManager.get_user_roles(users['player'], character)
        assert Role.PLAYER in roles

    def test_role_detection_observer(self, users, character):
        """Test that observer role is detected."""
        roles = PermissionManager.get_user_roles(users['observer'], character)
        assert Role.OBSERVER in roles

    def test_role_detection_stranger(self, users, character):
        """Test that stranger has no special roles."""
        roles = PermissionManager.get_user_roles(users['stranger'], character)
        assert Role.OWNER not in roles
        assert Role.CHRONICLE_HEAD_ST not in roles
        assert Role.GAME_ST not in roles
        assert Role.PLAYER not in roles
        assert Role.OBSERVER not in roles
        assert Role.AUTHENTICATED in roles

    # Owner Permission Tests

    def test_owner_can_view_full(self, users, character):
        """Test owner has full view permission."""
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.VIEW_FULL
        )

    def test_owner_cannot_edit_full(self, users, character):
        """Test owner does NOT have full edit permission."""
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_FULL
        )

    def test_owner_can_edit_limited(self, users, character):
        """Test owner has limited edit permission (notes/journals)."""
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_LIMITED
        )

    def test_owner_can_spend_xp_when_approved(self, users, character):
        """Test owner can spend XP on approved character."""
        character.status = 'App'
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )

    def test_owner_cannot_spend_xp_when_unfinished(self, users, character):
        """Test owner cannot spend XP on unfinished character."""
        character.status = 'Un'
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )

    def test_owner_can_spend_freebies_when_unfinished(self, users, character):
        """Test owner can spend freebies on unfinished character."""
        character.status = 'Un'
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_FREEBIES
        )

    # ST Permission Tests

    def test_head_st_can_view_full(self, users, character):
        """Test head ST has full view permission."""
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.VIEW_FULL
        )

    def test_head_st_can_edit_full(self, users, character):
        """Test head ST has full edit permission."""
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.EDIT_FULL
        )

    def test_game_st_can_view_full(self, users, character):
        """Test game ST has full view permission."""
        assert PermissionManager.user_has_permission(
            users['game_st'], character, Permission.VIEW_FULL
        )

    def test_game_st_cannot_edit(self, users, character):
        """Test game ST does NOT have edit permission (read-only)."""
        assert not PermissionManager.user_has_permission(
            users['game_st'], character, Permission.EDIT_FULL
        )
        assert not PermissionManager.user_has_permission(
            users['game_st'], character, Permission.EDIT_LIMITED
        )

    def test_head_st_can_approve(self, users, character):
        """Test head ST has approve permission."""
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.APPROVE
        )

    # Player and Observer Permission Tests

    def test_player_can_view_partial(self, users, character):
        """Test player has partial view permission."""
        assert PermissionManager.user_has_permission(
            users['player'], character, Permission.VIEW_PARTIAL
        )

    def test_player_cannot_view_full(self, users, character):
        """Test player does NOT have full view permission."""
        assert not PermissionManager.user_has_permission(
            users['player'], character, Permission.VIEW_FULL
        )

    def test_player_cannot_edit(self, users, character):
        """Test player cannot edit."""
        assert not PermissionManager.user_has_permission(
            users['player'], character, Permission.EDIT_FULL
        )
        assert not PermissionManager.user_has_permission(
            users['player'], character, Permission.EDIT_LIMITED
        )

    def test_observer_can_view_partial(self, users, character):
        """Test observer has partial view permission."""
        assert PermissionManager.user_has_permission(
            users['observer'], character, Permission.VIEW_PARTIAL
        )

    def test_stranger_cannot_view(self, users, character):
        """Test stranger has no view permission."""
        assert not PermissionManager.user_has_permission(
            users['stranger'], character, Permission.VIEW_FULL
        )
        assert not PermissionManager.user_has_permission(
            users['stranger'], character, Permission.VIEW_PARTIAL
        )

    # Admin Permission Tests

    def test_admin_can_do_everything(self, users, character):
        """Test admin has all permissions."""
        admin = users['admin']
        assert PermissionManager.user_has_permission(
            admin, character, Permission.VIEW_FULL
        )
        assert PermissionManager.user_has_permission(
            admin, character, Permission.EDIT_FULL
        )
        assert PermissionManager.user_has_permission(
            admin, character, Permission.DELETE
        )
        assert PermissionManager.user_has_permission(
            admin, character, Permission.APPROVE
        )

    # Visibility Tier Tests

    def test_visibility_tier_owner(self, users, character):
        """Test owner gets FULL visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['owner'], character)
        assert tier == VisibilityTier.FULL

    def test_visibility_tier_game_st(self, users, character):
        """Test game ST gets FULL visibility tier (but can't edit)."""
        tier = PermissionManager.get_visibility_tier(users['game_st'], character)
        assert tier == VisibilityTier.FULL

    def test_visibility_tier_player(self, users, character):
        """Test player gets PARTIAL visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['player'], character)
        assert tier == VisibilityTier.PARTIAL

    def test_visibility_tier_stranger(self, users, character):
        """Test stranger gets NONE visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['stranger'], character)
        assert tier == VisibilityTier.NONE

    # Status-Based Restriction Tests

    def test_status_restriction_submitted(self, users, character):
        """Test owner cannot spend XP/freebies on submitted character."""
        character.status = 'Sub'
        character.save()

        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_FREEBIES
        )

        # But head ST still can
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.EDIT_FULL
        )

    def test_status_restriction_deceased(self, users, character):
        """Test owner cannot edit deceased character, but head ST and admin can."""
        character.status = 'Dec'
        character.save()

        # Owner cannot edit
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_LIMITED
        )

        # Head ST can still edit (configurable)
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.EDIT_FULL
        )

        # Admin can still edit
        assert PermissionManager.user_has_permission(
            users['admin'], character, Permission.EDIT_FULL
        )

    # Observer Management Tests

    def test_add_observer(self, users, character):
        """Test adding an observer."""
        new_observer = User.objects.create_user('new_obs', 'obs@test.com')

        # Add as observer
        character.add_observer(new_observer, users['owner'])

        # Check observer can view
        assert PermissionManager.user_has_permission(
            new_observer, character, Permission.VIEW_PARTIAL
        )

    def test_remove_observer(self, users, character):
        """Test removing an observer."""
        # Remove existing observer
        character.remove_observer(users['observer'])

        # Check observer can no longer view
        assert not PermissionManager.user_has_permission(
            users['observer'], character, Permission.VIEW_PARTIAL
        )

    # Model Method Tests

    def test_model_user_can_view(self, users, character):
        """Test model's user_can_view method."""
        assert character.user_can_view(users['owner'])
        assert character.user_can_view(users['head_st'])
        assert not character.user_can_view(users['stranger'])

    def test_model_user_can_edit(self, users, character):
        """Test model's user_can_edit method (EDIT_FULL)."""
        assert not character.user_can_edit(users['owner'])
        assert character.user_can_edit(users['head_st'])
        assert not character.user_can_edit(users['game_st'])

    def test_model_user_can_spend_xp(self, users, character):
        """Test model's user_can_spend_xp method."""
        character.status = 'App'
        assert character.user_can_spend_xp(users['owner'])
        assert not character.user_can_spend_xp(users['player'])

    def test_model_user_can_spend_freebies(self, users, character):
        """Test model's user_can_spend_freebies method."""
        character.status = 'Un'
        assert character.user_can_spend_freebies(users['owner'])
        character.status = 'App'
        assert not character.user_can_spend_freebies(users['owner'])
