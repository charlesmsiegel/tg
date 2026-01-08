"""Tests for PermissionManager in core/permissions.py."""

from characters.models.core.character import Character
from core.models import Observer
from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from game.models import Chronicle


class TestRoleEnum(TestCase):
    """Tests for Role enum values."""

    def test_role_values(self):
        """Verify all expected role values exist."""
        self.assertEqual(Role.OWNER.value, "owner")
        self.assertEqual(Role.ADMIN.value, "admin")
        self.assertEqual(Role.CHRONICLE_HEAD_ST.value, "chronicle_head_st")
        self.assertEqual(Role.GAME_ST.value, "game_st")
        self.assertEqual(Role.PLAYER.value, "player")
        self.assertEqual(Role.OBSERVER.value, "observer")
        self.assertEqual(Role.AUTHENTICATED.value, "authenticated")
        self.assertEqual(Role.ANONYMOUS.value, "anonymous")


class TestVisibilityTierEnum(TestCase):
    """Tests for VisibilityTier enum values."""

    def test_visibility_tier_values(self):
        """Verify all expected visibility tier values exist."""
        self.assertEqual(VisibilityTier.FULL.value, "full")
        self.assertEqual(VisibilityTier.PARTIAL.value, "partial")
        self.assertEqual(VisibilityTier.NONE.value, "none")


class TestPermissionEnum(TestCase):
    """Tests for Permission enum values."""

    def test_permission_values(self):
        """Verify all expected permission values exist."""
        self.assertEqual(Permission.VIEW_FULL.value, "view_full")
        self.assertEqual(Permission.VIEW_PARTIAL.value, "view_partial")
        self.assertEqual(Permission.EDIT_FULL.value, "edit_full")
        self.assertEqual(Permission.EDIT_LIMITED.value, "edit_limited")
        self.assertEqual(Permission.SPEND_XP.value, "spend_xp")
        self.assertEqual(Permission.SPEND_FREEBIES.value, "spend_freebies")
        self.assertEqual(Permission.DELETE.value, "delete")
        self.assertEqual(Permission.APPROVE.value, "approve")
        self.assertEqual(Permission.MANAGE_OBSERVERS.value, "manage_observers")


class GetUserRolesTest(TestCase):
    """Tests for PermissionManager.get_user_roles()."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.game_st = User.objects.create_user(
            username="game_st", email="game_st@test.com", password="testpass123"
        )
        self.player = User.objects.create_user(
            username="player", email="player@test.com", password="testpass123"
        )
        self.observer_user = User.objects.create_user(
            username="observer_user", email="observer@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )

        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)
        self.chronicle.game_storytellers.add(self.game_st)

        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

        # Create a character for the player in the same chronicle
        self.player_character = Character.objects.create(
            name="Player Character", owner=self.player, chronicle=self.chronicle, status="App"
        )

        # Add observer
        Observer.objects.create(
            content_object=self.character, user=self.observer_user, granted_by=self.owner
        )

    def test_anonymous_user_gets_anonymous_role(self):
        """Anonymous users should only have ANONYMOUS role."""
        anon = AnonymousUser()
        roles = PermissionManager.get_user_roles(anon, self.character)
        self.assertEqual(roles, {Role.ANONYMOUS})

    def test_authenticated_user_gets_authenticated_role(self):
        """Any authenticated user should have AUTHENTICATED role."""
        roles = PermissionManager.get_user_roles(self.stranger, self.character)
        self.assertIn(Role.AUTHENTICATED, roles)

    def test_admin_user_gets_admin_role(self):
        """Admin users should have ADMIN role."""
        roles = PermissionManager.get_user_roles(self.admin, self.character)
        self.assertIn(Role.ADMIN, roles)
        self.assertIn(Role.AUTHENTICATED, roles)

    def test_staff_user_gets_admin_role(self):
        """Staff users should have ADMIN role."""
        staff_user = User.objects.create_user(
            username="staff", email="staff@test.com", password="testpass123", is_staff=True
        )
        roles = PermissionManager.get_user_roles(staff_user, self.character)
        self.assertIn(Role.ADMIN, roles)

    def test_owner_gets_owner_role(self):
        """Character owner should have OWNER role."""
        roles = PermissionManager.get_user_roles(self.owner, self.character)
        self.assertIn(Role.OWNER, roles)

    def test_head_st_gets_chronicle_head_st_role(self):
        """Chronicle head ST should have CHRONICLE_HEAD_ST role."""
        roles = PermissionManager.get_user_roles(self.head_st, self.character)
        self.assertIn(Role.CHRONICLE_HEAD_ST, roles)

    def test_game_st_gets_game_st_role(self):
        """Chronicle game ST should have GAME_ST role."""
        roles = PermissionManager.get_user_roles(self.game_st, self.character)
        self.assertIn(Role.GAME_ST, roles)

    def test_player_gets_player_role(self):
        """Player with character in same chronicle should have PLAYER role."""
        roles = PermissionManager.get_user_roles(self.player, self.character)
        self.assertIn(Role.PLAYER, roles)

    def test_observer_gets_observer_role(self):
        """User observing character should have OBSERVER role."""
        roles = PermissionManager.get_user_roles(self.observer_user, self.character)
        self.assertIn(Role.OBSERVER, roles)

    def test_stranger_only_has_authenticated_role(self):
        """Stranger should only have AUTHENTICATED role."""
        roles = PermissionManager.get_user_roles(self.stranger, self.character)
        self.assertEqual(roles, {Role.AUTHENTICATED})

    def test_owner_via_user_attribute(self):
        """Test ownership detection via 'user' attribute instead of 'owner'."""

        class MockObjWithUser:
            def __init__(self, user):
                self.user = user
                self.chronicle = None

        mock_obj = MockObjWithUser(self.owner)
        roles = PermissionManager.get_user_roles(self.owner, mock_obj)
        self.assertIn(Role.OWNER, roles)

    def test_owner_via_owned_by_attribute(self):
        """Test ownership detection via 'owned_by.owner' for nested ownership."""

        class MockCharacter:
            def __init__(self, owner):
                self.owner = owner

        class MockObjWithOwnedBy:
            def __init__(self, owned_by):
                self.owned_by = owned_by
                self.chronicle = None

        mock_char = MockCharacter(self.owner)
        mock_obj = MockObjWithOwnedBy(mock_char)
        roles = PermissionManager.get_user_roles(self.owner, mock_obj)
        self.assertIn(Role.OWNER, roles)

    def test_object_without_chronicle(self):
        """Test roles for object without chronicle attribute."""

        class MockObjNoChronicle:
            def __init__(self, owner):
                self.owner = owner

        mock_obj = MockObjNoChronicle(self.owner)
        roles = PermissionManager.get_user_roles(self.owner, mock_obj)
        self.assertIn(Role.OWNER, roles)
        self.assertIn(Role.AUTHENTICATED, roles)
        self.assertNotIn(Role.PLAYER, roles)


class UserHasPermissionTest(TestCase):
    """Tests for PermissionManager.user_has_permission()."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )

        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)

        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_owner_has_view_full_permission(self):
        """Owner should have VIEW_FULL permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(self.owner, self.character, Permission.VIEW_FULL)
        )

    def test_owner_has_edit_limited_permission(self):
        """Owner should have EDIT_LIMITED permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.owner, self.character, Permission.EDIT_LIMITED
            )
        )

    def test_owner_does_not_have_edit_full_permission(self):
        """Owner should NOT have EDIT_FULL permission."""
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, self.character, Permission.EDIT_FULL)
        )

    def test_owner_has_delete_permission(self):
        """Owner should have DELETE permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(self.owner, self.character, Permission.DELETE)
        )

    def test_admin_has_all_permissions(self):
        """Admin should have all permissions."""
        for perm in Permission:
            self.assertTrue(
                PermissionManager.user_has_permission(self.admin, self.character, perm),
                f"Admin should have {perm.value} permission",
            )

    def test_head_st_has_edit_full_permission(self):
        """Head ST should have EDIT_FULL permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.head_st, self.character, Permission.EDIT_FULL
            )
        )

    def test_head_st_has_approve_permission(self):
        """Head ST should have APPROVE permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(self.head_st, self.character, Permission.APPROVE)
        )

    def test_stranger_has_no_permissions(self):
        """Stranger should have no permissions."""
        for perm in Permission:
            self.assertFalse(
                PermissionManager.user_has_permission(self.stranger, self.character, perm),
                f"Stranger should not have {perm.value} permission",
            )

    def test_status_aware_false_bypasses_status_checks(self):
        """When status_aware=False, status restrictions should be bypassed."""
        self.character.status = "Dec"  # Deceased
        self.character.save()

        # With status_aware=True, owner can't delete deceased character
        # Actually per the code, admin and head_st CAN delete deceased characters
        # Let's test that owner can spend XP without status restrictions
        result = PermissionManager.user_has_permission(
            self.owner, self.character, Permission.SPEND_XP, status_aware=False
        )
        self.assertTrue(result)


class StatusRestrictionsTest(TestCase):
    """Tests for PermissionManager._check_status_restrictions()."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )

        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)

    def test_deceased_character_edit_full_blocked_for_owner(self):
        """Deceased characters cannot be edited by owner."""
        character = Character.objects.create(
            name="Deceased Character", owner=self.owner, chronicle=self.chronicle, status="Dec"
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, character, Permission.EDIT_FULL)
        )

    def test_deceased_character_edit_allowed_for_admin(self):
        """Admin can edit deceased characters."""
        character = Character.objects.create(
            name="Deceased Character", owner=self.owner, chronicle=self.chronicle, status="Dec"
        )
        self.assertTrue(
            PermissionManager.user_has_permission(self.admin, character, Permission.EDIT_FULL)
        )

    def test_deceased_character_edit_allowed_for_head_st(self):
        """Head ST can edit deceased characters."""
        character = Character.objects.create(
            name="Deceased Character", owner=self.owner, chronicle=self.chronicle, status="Dec"
        )
        self.assertTrue(
            PermissionManager.user_has_permission(self.head_st, character, Permission.EDIT_FULL)
        )

    def test_submitted_character_owner_cannot_edit(self):
        """Owner cannot edit submitted characters."""
        character = Character.objects.create(
            name="Submitted Character", owner=self.owner, chronicle=self.chronicle, status="Sub"
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, character, Permission.EDIT_LIMITED)
        )

    def test_submitted_character_head_st_can_edit(self):
        """Head ST can edit submitted characters."""
        character = Character.objects.create(
            name="Submitted Character", owner=self.owner, chronicle=self.chronicle, status="Sub"
        )
        self.assertTrue(
            PermissionManager.user_has_permission(self.head_st, character, Permission.EDIT_LIMITED)
        )

    def test_unfinished_character_owner_cannot_spend_xp(self):
        """Owner cannot spend XP on unfinished characters."""
        character = Character.objects.create(
            name="Unfinished Character", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, character, Permission.SPEND_XP)
        )

    def test_unfinished_character_owner_can_spend_freebies(self):
        """Owner can spend freebies on unfinished characters."""
        character = Character.objects.create(
            name="Unfinished Character", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        self.assertTrue(
            PermissionManager.user_has_permission(self.owner, character, Permission.SPEND_FREEBIES)
        )

    def test_approved_character_owner_can_spend_xp(self):
        """Owner can spend XP on approved characters."""
        character = Character.objects.create(
            name="Approved Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )
        self.assertTrue(
            PermissionManager.user_has_permission(self.owner, character, Permission.SPEND_XP)
        )

    def test_approved_character_owner_cannot_spend_freebies(self):
        """Owner cannot spend freebies on approved characters."""
        character = Character.objects.create(
            name="Approved Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, character, Permission.SPEND_FREEBIES)
        )

    def test_retired_character_owner_cannot_edit(self):
        """Owner cannot edit retired characters."""
        character = Character.objects.create(
            name="Retired Character", owner=self.owner, chronicle=self.chronicle, status="Ret"
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, character, Permission.EDIT_LIMITED)
        )

    def test_retired_character_owner_cannot_spend_xp(self):
        """Owner cannot spend XP on retired characters."""
        character = Character.objects.create(
            name="Retired Character", owner=self.owner, chronicle=self.chronicle, status="Ret"
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, character, Permission.SPEND_XP)
        )


class VisibilityTierTest(TestCase):
    """Tests for PermissionManager.get_visibility_tier()."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.player = User.objects.create_user(
            username="player", email="player@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )

        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)

        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

        # Create player's character in same chronicle
        Character.objects.create(
            name="Player Character", owner=self.player, chronicle=self.chronicle, status="App"
        )

    def test_owner_has_full_visibility(self):
        """Owner should have full visibility."""
        tier = PermissionManager.get_visibility_tier(self.owner, self.character)
        self.assertEqual(tier, VisibilityTier.FULL)

    def test_head_st_has_full_visibility(self):
        """Head ST should have full visibility."""
        tier = PermissionManager.get_visibility_tier(self.head_st, self.character)
        self.assertEqual(tier, VisibilityTier.FULL)

    def test_player_has_partial_visibility(self):
        """Player in same chronicle should have partial visibility."""
        tier = PermissionManager.get_visibility_tier(self.player, self.character)
        self.assertEqual(tier, VisibilityTier.PARTIAL)

    def test_stranger_has_no_visibility(self):
        """Stranger should have no visibility."""
        tier = PermissionManager.get_visibility_tier(self.stranger, self.character)
        self.assertEqual(tier, VisibilityTier.NONE)


class ConvenienceMethodsTest(TestCase):
    """Tests for convenience methods on PermissionManager."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )

        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)

        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_user_can_view(self):
        """Test user_can_view convenience method."""
        self.assertTrue(PermissionManager.user_can_view(self.owner, self.character))
        self.assertTrue(PermissionManager.user_can_view(self.head_st, self.character))
        self.assertFalse(PermissionManager.user_can_view(self.stranger, self.character))

    def test_user_can_edit(self):
        """Test user_can_edit convenience method (checks EDIT_FULL only)."""
        self.assertFalse(PermissionManager.user_can_edit(self.owner, self.character))
        self.assertTrue(PermissionManager.user_can_edit(self.head_st, self.character))
        self.assertFalse(PermissionManager.user_can_edit(self.stranger, self.character))

    def test_user_can_spend_xp(self):
        """Test user_can_spend_xp convenience method."""
        self.assertTrue(PermissionManager.user_can_spend_xp(self.owner, self.character))
        self.assertTrue(PermissionManager.user_can_spend_xp(self.head_st, self.character))
        self.assertFalse(PermissionManager.user_can_spend_xp(self.stranger, self.character))

    def test_user_can_spend_freebies(self):
        """Test user_can_spend_freebies convenience method."""
        # For approved character, owner cannot spend freebies
        self.assertFalse(PermissionManager.user_can_spend_freebies(self.owner, self.character))

        # Head ST can spend freebies
        self.assertTrue(PermissionManager.user_can_spend_freebies(self.head_st, self.character))

        # Stranger cannot
        self.assertFalse(PermissionManager.user_can_spend_freebies(self.stranger, self.character))


class CheckPermissionStringMethodTest(TestCase):
    """Tests for PermissionManager.check_permission() instance method."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )
        self.manager = PermissionManager()

    def test_check_permission_with_lowercase_string(self):
        """Test check_permission with lowercase permission string."""
        result = self.manager.check_permission(self.owner, self.character, "view_full")
        self.assertTrue(result)

    def test_check_permission_with_uppercase_string(self):
        """Test check_permission with uppercase permission string."""
        result = self.manager.check_permission(self.owner, self.character, "VIEW_FULL")
        self.assertTrue(result)

    def test_check_permission_with_invalid_string(self):
        """Test check_permission with invalid permission string returns False."""
        result = self.manager.check_permission(self.owner, self.character, "invalid_permission")
        self.assertFalse(result)


class FilterQuerysetForUserTest(TestCase):
    """Tests for PermissionManager.filter_queryset_for_user().

    Note: Some tests use Chronicle model instead of Character to avoid
    polymorphic model issues with the Exists subquery filter.
    """

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_anonymous_user_returns_empty_queryset(self):
        """Anonymous user should get empty queryset."""
        anon = AnonymousUser()
        qs = PermissionManager.filter_queryset_for_user(anon, Chronicle.objects.all())
        self.assertEqual(qs.count(), 0)

    def test_admin_sees_all_chronicles(self):
        """Admin should see all objects."""
        Chronicle.objects.create(name="Chronicle 2")
        qs = PermissionManager.filter_queryset_for_user(self.admin, Chronicle.objects.all())
        self.assertEqual(qs.count(), 2)

    def test_filter_handles_model_without_owner_field(self):
        """Filter should handle models without owner field gracefully."""
        # Chronicle model doesn't have an 'owner' field
        qs = PermissionManager.filter_queryset_for_user(self.stranger, Chronicle.objects.all())
        # Stranger should see nothing for models they don't own
        self.assertEqual(qs.count(), 0)


class HelperMethodsTest(TestCase):
    """Tests for PermissionManager helper methods."""

    def test_model_has_field_true(self):
        """Test _model_has_field returns True for existing field."""
        result = PermissionManager._model_has_field(Character, "owner")
        self.assertTrue(result)

    def test_model_has_field_false(self):
        """Test _model_has_field returns False for non-existing field."""
        result = PermissionManager._model_has_field(Character, "nonexistent_field")
        self.assertFalse(result)

    def test_get_chronicle_related_model(self):
        """Test _get_chronicle_related_model returns Chronicle model."""
        result = PermissionManager._get_chronicle_related_model(Character.objects.all())
        self.assertEqual(result, Chronicle)

    def test_build_owner_filter(self):
        """Test _build_owner_filter returns Q object."""
        user = User.objects.create_user(username="test", password="testpass123")
        q_filter = PermissionManager._build_owner_filter(user, Character)
        self.assertIsNotNone(q_filter)

    def test_build_owner_filter_for_model_without_owner(self):
        """Test _build_owner_filter for model without owner returns Q filter."""
        from django.db.models import Q

        user = User.objects.create_user(username="test2", password="testpass123")
        # Chronicle doesn't have an owner field
        q_filter = PermissionManager._build_owner_filter(user, Chronicle)
        # Should return empty Q object
        self.assertEqual(str(q_filter), str(Q()))


class ObserverFilterTest(TestCase):
    """Tests for PermissionManager._get_observer_filter() and observer queryset filtering."""

    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username="observer_test_owner", email="owner@test.com", password="testpass123"
        )
        self.observer_user = User.objects.create_user(
            username="observer_test_observer",
            email="observer@test.com",
            password="testpass123",
        )
        self.non_observer = User.objects.create_user(
            username="observer_test_non_observer",
            email="non_observer@test.com",
            password="testpass123",
        )

        self.chronicle = Chronicle.objects.create(name="Observer Test Chronicle")

        self.character = Character.objects.create(
            name="Observer Test Character",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

        # Create a second character without observer
        self.character2 = Character.objects.create(
            name="Observer Test Character 2",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

        # Add observer to first character only
        Observer.objects.create(
            content_object=self.character,
            user=self.observer_user,
            granted_by=self.owner,
        )

    def test_get_observer_filter_returns_q_object(self):
        """_get_observer_filter should return a Q object."""
        from django.db.models import Q

        q_filter = PermissionManager._get_observer_filter(self.observer_user, Character)
        self.assertIsInstance(q_filter, Q)

    def test_get_observer_filter_for_model_without_observers(self):
        """_get_observer_filter should return empty Q for models without observers relation."""
        from django.db.models import Q

        # Chronicle doesn't have observers field
        q_filter = PermissionManager._get_observer_filter(self.observer_user, Chronicle)
        # Should return Q(pk__in=[]) which filters nothing
        self.assertEqual(str(q_filter), str(Q(pk__in=[])))

    def test_filter_queryset_includes_observed_characters(self):
        """filter_queryset_for_user should include characters the user is observing."""
        qs = PermissionManager.filter_queryset_for_user(self.observer_user, Character.objects.all())
        # Observer should see the character they're observing
        self.assertIn(self.character, qs)

    def test_filter_queryset_excludes_non_observed_characters(self):
        """filter_queryset_for_user should exclude characters the user is not observing."""
        qs = PermissionManager.filter_queryset_for_user(self.observer_user, Character.objects.all())
        # Observer should NOT see the character they're not observing
        self.assertNotIn(self.character2, qs)

    def test_non_observer_cannot_see_private_characters(self):
        """Users who are not observers should not see characters via observer filter."""
        qs = PermissionManager.filter_queryset_for_user(self.non_observer, Character.objects.all())
        # Non-observer should not see either character
        self.assertNotIn(self.character, qs)
        self.assertNotIn(self.character2, qs)

    def test_observer_filter_uses_generic_relation(self):
        """Verify the observer filter works correctly via GenericRelation."""
        # Create multiple observers
        observer2 = User.objects.create_user(
            username="observer_test_observer2",
            email="observer2@test.com",
            password="testpass123",
        )
        Observer.objects.create(
            content_object=self.character2,
            user=observer2,
            granted_by=self.owner,
        )

        # First observer only sees first character
        qs1 = PermissionManager.filter_queryset_for_user(
            self.observer_user, Character.objects.all()
        )
        self.assertEqual(list(qs1), [self.character])

        # Second observer only sees second character
        qs2 = PermissionManager.filter_queryset_for_user(observer2, Character.objects.all())
        self.assertEqual(list(qs2), [self.character2])
