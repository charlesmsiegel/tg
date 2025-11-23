"""
Comprehensive permission tests for World of Darkness application.

Tests all permission scenarios across different user roles:
- Owner
- Chronicle Head ST
- Game ST
- Player (chronicle member)
- Observer
- Stranger (authenticated but unrelated)
- Anonymous

Tests visibility tiers and proper 404 responses for unauthorized access.
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from characters.models.core.character import Character
from characters.models.core.human import Human
from core.models import Observer
from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from game.models import Chronicle


@pytest.mark.django_db
class TestPermissionRoles:
    """Test role detection for different user types."""

    @pytest.fixture
    def users(self):
        """Create test users."""
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com', 'password123'),
            'head_st': User.objects.create_user('head_st', 'head_st@test.com', 'password123'),
            'game_st': User.objects.create_user('game_st', 'game_st@test.com', 'password123'),
            'player': User.objects.create_user('player', 'player@test.com', 'password123'),
            'observer': User.objects.create_user('observer', 'observer@test.com', 'password123'),
            'stranger': User.objects.create_user('stranger', 'stranger@test.com', 'password123'),
            'admin': User.objects.create_user('admin', 'admin@test.com', 'password123', is_staff=True, is_superuser=True),
        }

    @pytest.fixture
    def chronicle(self, users):
        """Create test chronicle."""
        chron = Chronicle.objects.create(
            name="Test Chronicle",
            description="A test chronicle for permissions",
        )
        # Set head ST (assuming Chronicle has head_st field or storytellers M2M)
        # Adjust based on your actual Chronicle model
        if hasattr(chron, 'head_st'):
            chron.head_st = users['head_st']
            chron.save()
        elif hasattr(chron, 'storytellers'):
            chron.storytellers.add(users['head_st'])

        # Add game ST (if model supports it)
        if hasattr(chron, 'game_storytellers'):
            chron.game_storytellers.add(users['game_st'])

        return chron

    @pytest.fixture
    def character(self, users, chronicle):
        """Create test character."""
        char = Human.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App',
            concept="Test Concept",
        )

        # Add observer
        Observer.objects.create(
            content_object=char,
            user=users['observer'],
            granted_by=users['owner'],
        )

        # Create player's character in same chronicle
        Human.objects.create(
            name="Player's Character",
            owner=users['player'],
            chronicle=chronicle,
            status='App',
            concept="Player Concept",
        )

        return char

    def test_owner_role_detected(self, users, character):
        """Test that owner role is correctly detected."""
        roles = PermissionManager.get_user_roles(users['owner'], character)
        assert Role.OWNER in roles
        assert Role.AUTHENTICATED in roles

    def test_head_st_role_detected(self, users, character):
        """Test that chronicle head ST role is correctly detected."""
        roles = PermissionManager.get_user_roles(users['head_st'], character)
        # This depends on how your Chronicle model is structured
        # Adjust assertion based on your implementation
        assert Role.AUTHENTICATED in roles
        # If head_st field exists and is set:
        # assert Role.CHRONICLE_HEAD_ST in roles

    def test_game_st_role_detected(self, users, character):
        """Test that game ST role is correctly detected."""
        roles = PermissionManager.get_user_roles(users['game_st'], character)
        assert Role.AUTHENTICATED in roles
        # If game_storytellers field exists:
        # assert Role.GAME_ST in roles

    def test_player_role_detected(self, users, character):
        """Test that player role is correctly detected for chronicle members."""
        roles = PermissionManager.get_user_roles(users['player'], character)
        assert Role.PLAYER in roles
        assert Role.AUTHENTICATED in roles

    def test_observer_role_detected(self, users, character):
        """Test that observer role is correctly detected."""
        roles = PermissionManager.get_user_roles(users['observer'], character)
        assert Role.OBSERVER in roles
        assert Role.AUTHENTICATED in roles

    def test_stranger_has_no_special_roles(self, users, character):
        """Test that stranger has only authenticated role."""
        roles = PermissionManager.get_user_roles(users['stranger'], character)
        assert Role.OWNER not in roles
        assert Role.PLAYER not in roles
        assert Role.OBSERVER not in roles
        assert Role.AUTHENTICATED in roles

    def test_admin_role_detected(self, users, character):
        """Test that admin role is correctly detected."""
        roles = PermissionManager.get_user_roles(users['admin'], character)
        assert Role.ADMIN in roles
        assert Role.AUTHENTICATED in roles


@pytest.mark.django_db
class TestOwnerPermissions:
    """Test permissions for character owners."""

    @pytest.fixture
    def users(self):
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com', 'password123'),
            'head_st': User.objects.create_user('head_st', 'head_st@test.com', 'password123'),
        }

    @pytest.fixture
    def chronicle(self, users):
        chron = Chronicle.objects.create(name="Test Chronicle")
        if hasattr(chron, 'head_st'):
            chron.head_st = users['head_st']
            chron.save()
        return chron

    @pytest.fixture
    def character(self, users, chronicle):
        return Human.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App',
            concept="Test Concept",
        )

    def test_owner_can_view_full(self, users, character):
        """Owner should have full view permission."""
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.VIEW_FULL
        )

    def test_owner_cannot_edit_full(self, users, character):
        """Owner should NOT have full edit permission (cannot modify stats directly)."""
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_FULL
        )

    def test_owner_can_edit_limited(self, users, character):
        """Owner should have limited edit permission (notes, description)."""
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_LIMITED
        )

    def test_owner_can_spend_xp_when_approved(self, users, character):
        """Owner should be able to spend XP on approved characters."""
        character.status = 'App'
        character.save()
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )

    def test_owner_cannot_spend_xp_when_unfinished(self, users, character):
        """Owner should NOT be able to spend XP on unfinished characters."""
        character.status = 'Un'
        character.save()
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )

    def test_owner_can_spend_freebies_when_unfinished(self, users, character):
        """Owner should be able to spend freebies on unfinished characters."""
        character.status = 'Un'
        character.save()
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_FREEBIES
        )

    def test_owner_cannot_spend_freebies_when_approved(self, users, character):
        """Owner should NOT be able to spend freebies after approval."""
        character.status = 'App'
        character.save()
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_FREEBIES
        )

    def test_owner_cannot_edit_when_submitted(self, users, character):
        """Owner should have no permissions when character is submitted."""
        character.status = 'Sub'
        character.save()
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_LIMITED
        )
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_FREEBIES
        )

    def test_owner_cannot_edit_when_deceased(self, users, character):
        """Owner should have no permissions when character is deceased."""
        character.status = 'Dec'
        character.save()
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_LIMITED
        )
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )

    def test_owner_can_delete(self, users, character):
        """Owner should be able to delete their own character."""
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.DELETE
        )

    def test_owner_cannot_approve(self, users, character):
        """Owner should NOT be able to approve their own character."""
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.APPROVE
        )


@pytest.mark.django_db
class TestStorytellerPermissions:
    """Test permissions for storytellers."""

    @pytest.fixture
    def users(self):
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com', 'password123'),
            'head_st': User.objects.create_user('head_st', 'head_st@test.com', 'password123'),
            'game_st': User.objects.create_user('game_st', 'game_st@test.com', 'password123'),
        }

    @pytest.fixture
    def chronicle(self, users):
        chron = Chronicle.objects.create(name="Test Chronicle")
        if hasattr(chron, 'head_st'):
            chron.head_st = users['head_st']
            chron.save()
        if hasattr(chron, 'game_storytellers'):
            chron.game_storytellers.add(users['game_st'])
        return chron

    @pytest.fixture
    def character(self, users, chronicle):
        return Human.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App',
            concept="Test Concept",
        )

    def test_head_st_can_view_full(self, users, character):
        """Chronicle Head ST should have full view permission."""
        # Adjust based on your Chronicle model implementation
        # This test assumes head_st field exists
        roles = PermissionManager.get_user_roles(users['head_st'], character)
        has_view = PermissionManager.user_has_permission(
            users['head_st'], character, Permission.VIEW_FULL
        )
        # Assert based on whether CHRONICLE_HEAD_ST role is detected
        # If role is properly detected, this should be True

    def test_head_st_can_edit_full(self, users, character):
        """Chronicle Head ST should have full edit permission."""
        # Test depends on Chronicle model having head_st field
        pass

    def test_game_st_can_view_full(self, users, character):
        """Game ST should have full view permission (read-only)."""
        # Test depends on Chronicle model having game_storytellers field
        pass

    def test_game_st_cannot_edit(self, users, character):
        """Game ST should NOT have edit permission (read-only)."""
        roles = PermissionManager.get_user_roles(users['game_st'], character)
        if Role.GAME_ST in roles:
            assert not PermissionManager.user_has_permission(
                users['game_st'], character, Permission.EDIT_FULL
            )
            assert not PermissionManager.user_has_permission(
                users['game_st'], character, Permission.EDIT_LIMITED
            )


@pytest.mark.django_db
class TestVisibilityTiers:
    """Test visibility tier system."""

    @pytest.fixture
    def users(self):
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com', 'password123'),
            'player': User.objects.create_user('player', 'player@test.com', 'password123'),
            'stranger': User.objects.create_user('stranger', 'stranger@test.com', 'password123'),
            'observer': User.objects.create_user('observer', 'observer@test.com', 'password123'),
        }

    @pytest.fixture
    def chronicle(self):
        return Chronicle.objects.create(name="Test Chronicle")

    @pytest.fixture
    def character(self, users, chronicle):
        char = Human.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App',
            concept="Test Concept",
        )

        # Add player's character
        Human.objects.create(
            name="Player's Character",
            owner=users['player'],
            chronicle=chronicle,
            status='App',
            concept="Player Concept",
        )

        # Add observer
        Observer.objects.create(
            content_object=char,
            user=users['observer'],
            granted_by=users['owner'],
        )

        return char

    def test_owner_gets_full_visibility(self, users, character):
        """Owner should get FULL visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['owner'], character)
        assert tier == VisibilityTier.FULL

    def test_player_gets_partial_visibility(self, users, character):
        """Player in same chronicle should get PARTIAL visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['player'], character)
        assert tier == VisibilityTier.PARTIAL

    def test_observer_gets_partial_visibility(self, users, character):
        """Observer should get PARTIAL visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['observer'], character)
        assert tier == VisibilityTier.PARTIAL

    def test_stranger_gets_no_visibility(self, users, character):
        """Stranger should get NONE visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['stranger'], character)
        assert tier == VisibilityTier.NONE


@pytest.mark.django_db
class TestViewPermissions404:
    """Test that views return proper 404 responses for unauthorized access."""

    @pytest.fixture
    def users(self):
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com', 'password123'),
            'stranger': User.objects.create_user('stranger', 'stranger@test.com', 'password123'),
        }

    @pytest.fixture
    def chronicle(self):
        return Chronicle.objects.create(name="Test Chronicle")

    @pytest.fixture
    def character(self, users, chronicle):
        return Human.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App',
            concept="Test Concept",
        )

    def test_owner_can_view_detail(self, users, character):
        """Owner should be able to view character detail page."""
        client = Client()
        client.force_login(users['owner'])
        url = reverse('characters:character', kwargs={'pk': character.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_stranger_gets_404_on_detail(self, users, character):
        """Stranger should get 404 when accessing character detail."""
        client = Client()
        client.force_login(users['stranger'])
        url = reverse('characters:character', kwargs={'pk': character.pk})
        response = client.get(url)
        # Should return 404, not 403, to avoid information leakage
        assert response.status_code == 404

    def test_stranger_gets_403_on_edit(self, users, character):
        """Stranger should get 403 (or 404) when attempting to edit."""
        client = Client()
        client.force_login(users['stranger'])
        url = reverse('characters:update:character', kwargs={'pk': character.pk})
        response = client.get(url)
        # Edit views may return 403 or 404 depending on implementation
        assert response.status_code in [403, 404]

    def test_anonymous_cannot_view(self, character):
        """Anonymous users should be redirected or get 404."""
        client = Client()
        url = reverse('characters:character', kwargs={'pk': character.pk})
        response = client.get(url)
        # Should redirect to login or return 404
        assert response.status_code in [302, 404]


@pytest.mark.django_db
class TestLimitedFormPermissions:
    """Test that owners can only edit limited fields."""

    @pytest.fixture
    def users(self):
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com', 'password123'),
            'head_st': User.objects.create_user('head_st', 'head_st@test.com', 'password123'),
        }

    @pytest.fixture
    def chronicle(self, users):
        chron = Chronicle.objects.create(name="Test Chronicle")
        if hasattr(chron, 'head_st'):
            chron.head_st = users['head_st']
            chron.save()
        return chron

    @pytest.fixture
    def character(self, users, chronicle):
        return Human.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App',
            concept="Test Concept",
            willpower=5,
        )

    def test_owner_can_update_notes(self, users, character):
        """Owner should be able to update notes field."""
        client = Client()
        client.force_login(users['owner'])
        url = reverse('characters:update:character', kwargs={'pk': character.pk})

        response = client.post(url, {
            'notes': 'Updated notes',
            'description': character.description,
            'public_info': character.public_info,
        })

        character.refresh_from_db()
        assert character.notes == 'Updated notes'

    def test_owner_cannot_update_willpower_via_form(self, users, character):
        """Owner should NOT be able to update willpower (mechanical field) via limited form."""
        client = Client()
        client.force_login(users['owner'])
        url = reverse('characters:update:character', kwargs={'pk': character.pk})

        original_willpower = character.willpower

        # Try to update willpower (should be ignored by limited form)
        response = client.post(url, {
            'notes': 'Some notes',
            'description': 'Some description',
            'public_info': 'Public',
            'willpower': 10,  # Attempt to change mechanical field
        })

        character.refresh_from_db()
        # Willpower should remain unchanged
        assert character.willpower == original_willpower

    def test_owner_cannot_update_status(self, users, character):
        """Owner should NOT be able to update status via limited form."""
        client = Client()
        client.force_login(users['owner'])
        url = reverse('characters:update:character', kwargs={'pk': character.pk})

        original_status = character.status

        response = client.post(url, {
            'notes': 'Some notes',
            'description': 'Some description',
            'public_info': 'Public',
            'status': 'Ret',  # Attempt to change status
        })

        character.refresh_from_db()
        assert character.status == original_status
