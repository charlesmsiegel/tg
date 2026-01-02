"""
Deployment verification tests for the permissions system.

These tests verify that the permissions system is correctly configured
and functioning before deployment to staging/production.

Run with: python manage.py test core.tests.permissions.test_permissions_deployment -v 2
Expected: 37 tests passing
"""

from characters.models.core.character import Character
from core.mixins import (
    EditPermissionMixin,
    OwnerRequiredMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    STRequiredMixin,
    ViewPermissionMixin,
    VisibilityFilterMixin,
)
from core.models import Observer
from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from game.models import Chronicle


class DeploymentRoleEnumTest(TestCase):
    """Verify Role enum is properly configured for deployment."""

    def test_all_roles_exist(self):
        """All expected roles must exist in the enum."""
        expected_roles = [
            "owner",
            "admin",
            "chronicle_head_st",
            "game_st",
            "player",
            "observer",
            "authenticated",
            "anonymous",
        ]
        actual_roles = [r.value for r in Role]
        for role in expected_roles:
            self.assertIn(role, actual_roles, f"Missing role: {role}")

    def test_role_count(self):
        """Verify expected number of roles."""
        self.assertEqual(len(Role), 8)


class DeploymentPermissionEnumTest(TestCase):
    """Verify Permission enum is properly configured for deployment."""

    def test_all_permissions_exist(self):
        """All expected permissions must exist in the enum."""
        expected_permissions = [
            "view_full",
            "view_partial",
            "edit_full",
            "edit_limited",
            "spend_xp",
            "spend_freebies",
            "delete",
            "approve",
            "manage_observers",
        ]
        actual_permissions = [p.value for p in Permission]
        for perm in expected_permissions:
            self.assertIn(perm, actual_permissions, f"Missing permission: {perm}")

    def test_permission_count(self):
        """Verify expected number of permissions."""
        self.assertEqual(len(Permission), 9)


class DeploymentVisibilityTierTest(TestCase):
    """Verify VisibilityTier enum is properly configured."""

    def test_all_tiers_exist(self):
        """All visibility tiers must exist."""
        expected_tiers = ["full", "partial", "none"]
        actual_tiers = [t.value for t in VisibilityTier]
        for tier in expected_tiers:
            self.assertIn(tier, actual_tiers, f"Missing tier: {tier}")

    def test_tier_count(self):
        """Verify expected number of tiers."""
        self.assertEqual(len(VisibilityTier), 3)


class DeploymentRolePermissionMatrixTest(TestCase):
    """Verify the role-permission matrix is correctly configured."""

    def test_admin_has_all_permissions(self):
        """Admin role must have all permissions."""
        admin_perms = PermissionManager.ROLE_PERMISSIONS[Role.ADMIN]
        for perm in Permission:
            self.assertIn(perm, admin_perms, f"Admin missing permission: {perm.value}")

    def test_chronicle_head_st_has_full_access(self):
        """Chronicle Head ST must have full edit and approve permissions."""
        head_st_perms = PermissionManager.ROLE_PERMISSIONS[Role.CHRONICLE_HEAD_ST]
        required = [
            Permission.VIEW_FULL,
            Permission.EDIT_FULL,
            Permission.APPROVE,
            Permission.DELETE,
        ]
        for perm in required:
            self.assertIn(perm, head_st_perms, f"Head ST missing: {perm.value}")

    def test_game_st_is_read_only(self):
        """Game ST must have view only, no edit permissions."""
        game_st_perms = PermissionManager.ROLE_PERMISSIONS[Role.GAME_ST]
        self.assertIn(Permission.VIEW_FULL, game_st_perms)
        self.assertNotIn(Permission.EDIT_FULL, game_st_perms)
        self.assertNotIn(Permission.EDIT_LIMITED, game_st_perms)
        self.assertNotIn(Permission.DELETE, game_st_perms)

    def test_owner_cannot_edit_full(self):
        """Owner must not have EDIT_FULL (only EDIT_LIMITED)."""
        owner_perms = PermissionManager.ROLE_PERMISSIONS[Role.OWNER]
        self.assertNotIn(Permission.EDIT_FULL, owner_perms)
        self.assertIn(Permission.EDIT_LIMITED, owner_perms)

    def test_owner_has_spending_permissions(self):
        """Owner must have XP and freebie spending permissions."""
        owner_perms = PermissionManager.ROLE_PERMISSIONS[Role.OWNER]
        self.assertIn(Permission.SPEND_XP, owner_perms)
        self.assertIn(Permission.SPEND_FREEBIES, owner_perms)

    def test_player_has_partial_view_only(self):
        """Player role must have only VIEW_PARTIAL."""
        player_perms = PermissionManager.ROLE_PERMISSIONS[Role.PLAYER]
        self.assertEqual(player_perms, {Permission.VIEW_PARTIAL})

    def test_observer_has_partial_view_only(self):
        """Observer role must have only VIEW_PARTIAL."""
        observer_perms = PermissionManager.ROLE_PERMISSIONS[Role.OBSERVER]
        self.assertEqual(observer_perms, {Permission.VIEW_PARTIAL})

    def test_authenticated_has_no_permissions(self):
        """Authenticated role must have no permissions by default."""
        auth_perms = PermissionManager.ROLE_PERMISSIONS[Role.AUTHENTICATED]
        self.assertEqual(auth_perms, set())

    def test_anonymous_has_no_permissions(self):
        """Anonymous role must have no permissions."""
        anon_perms = PermissionManager.ROLE_PERMISSIONS[Role.ANONYMOUS]
        self.assertEqual(anon_perms, set())


class DeploymentRoleAssignmentTest(TestCase):
    """Verify role assignment logic works correctly."""

    def setUp(self):
        """Create test fixtures."""
        self.owner = User.objects.create_user(
            username="deploy_owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="deploy_head_st", email="head_st@test.com", password="testpass123"
        )
        self.game_st = User.objects.create_user(
            username="deploy_game_st", email="game_st@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="deploy_admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.stranger = User.objects.create_user(
            username="deploy_stranger", email="stranger@test.com", password="testpass123"
        )

        self.chronicle = Chronicle.objects.create(
            name="Deployment Test Chronicle", head_st=self.head_st
        )
        self.chronicle.game_storytellers.add(self.game_st)

        self.character = Character.objects.create(
            name="Deployment Test Character",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_admin_gets_admin_role(self):
        """Admin users get ADMIN role."""
        roles = PermissionManager.get_user_roles(self.admin, self.character)
        self.assertIn(Role.ADMIN, roles)

    def test_owner_gets_owner_role(self):
        """Owners get OWNER role."""
        roles = PermissionManager.get_user_roles(self.owner, self.character)
        self.assertIn(Role.OWNER, roles)

    def test_head_st_gets_chronicle_head_st_role(self):
        """Head ST gets CHRONICLE_HEAD_ST role."""
        roles = PermissionManager.get_user_roles(self.head_st, self.character)
        self.assertIn(Role.CHRONICLE_HEAD_ST, roles)

    def test_game_st_gets_game_st_role(self):
        """Game ST gets GAME_ST role."""
        roles = PermissionManager.get_user_roles(self.game_st, self.character)
        self.assertIn(Role.GAME_ST, roles)

    def test_stranger_gets_only_authenticated(self):
        """Strangers only get AUTHENTICATED role."""
        roles = PermissionManager.get_user_roles(self.stranger, self.character)
        self.assertEqual(roles, {Role.AUTHENTICATED})

    def test_anonymous_gets_anonymous_role(self):
        """Anonymous users get ANONYMOUS role only."""
        anon = AnonymousUser()
        roles = PermissionManager.get_user_roles(anon, self.character)
        self.assertEqual(roles, {Role.ANONYMOUS})


class DeploymentStatusRestrictionsTest(TestCase):
    """Verify status-based restrictions work correctly."""

    def setUp(self):
        """Create test fixtures."""
        self.owner = User.objects.create_user(
            username="status_owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="status_head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Status Test Chronicle", head_st=self.head_st
        )

    def test_unfinished_owner_can_spend_freebies(self):
        """Owner can spend freebies on unfinished characters."""
        char = Character.objects.create(
            name="Unfinished Char",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.assertTrue(
            PermissionManager.user_has_permission(self.owner, char, Permission.SPEND_FREEBIES)
        )

    def test_unfinished_owner_cannot_spend_xp(self):
        """Owner cannot spend XP on unfinished characters."""
        char = Character.objects.create(
            name="Unfinished Char 2",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, char, Permission.SPEND_XP)
        )

    def test_approved_owner_can_spend_xp(self):
        """Owner can spend XP on approved characters."""
        char = Character.objects.create(
            name="Approved Char",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )
        self.assertTrue(
            PermissionManager.user_has_permission(self.owner, char, Permission.SPEND_XP)
        )

    def test_approved_owner_cannot_spend_freebies(self):
        """Owner cannot spend freebies on approved characters."""
        char = Character.objects.create(
            name="Approved Char 2",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, char, Permission.SPEND_FREEBIES)
        )

    def test_submitted_owner_cannot_edit(self):
        """Owner cannot edit submitted characters."""
        char = Character.objects.create(
            name="Submitted Char",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Sub",
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, char, Permission.EDIT_LIMITED)
        )

    def test_retired_owner_cannot_spend_xp(self):
        """Owner cannot spend XP on retired characters."""
        char = Character.objects.create(
            name="Retired Char",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Ret",
        )
        self.assertFalse(
            PermissionManager.user_has_permission(self.owner, char, Permission.SPEND_XP)
        )


class DeploymentVisibilityTest(TestCase):
    """Verify visibility tier logic works correctly."""

    def setUp(self):
        """Create test fixtures."""
        self.owner = User.objects.create_user(
            username="vis_owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="vis_head_st", email="head_st@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="vis_stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(
            name="Visibility Test Chronicle", head_st=self.head_st
        )
        self.character = Character.objects.create(
            name="Visibility Test Char",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_owner_has_full_visibility(self):
        """Owner gets FULL visibility."""
        tier = PermissionManager.get_visibility_tier(self.owner, self.character)
        self.assertEqual(tier, VisibilityTier.FULL)

    def test_head_st_has_full_visibility(self):
        """Head ST gets FULL visibility."""
        tier = PermissionManager.get_visibility_tier(self.head_st, self.character)
        self.assertEqual(tier, VisibilityTier.FULL)

    def test_stranger_has_no_visibility(self):
        """Stranger gets NONE visibility."""
        tier = PermissionManager.get_visibility_tier(self.stranger, self.character)
        self.assertEqual(tier, VisibilityTier.NONE)


class DeploymentQueryFilterTest(TestCase):
    """Verify queryset filtering works correctly."""

    def setUp(self):
        """Create test fixtures."""
        self.admin = User.objects.create_user(
            username="filter_admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.stranger = User.objects.create_user(
            username="filter_stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Filter Test Chronicle")

    def test_admin_sees_all(self):
        """Admin sees all chronicles."""
        Chronicle.objects.create(name="Filter Chronicle 2")
        qs = PermissionManager.filter_queryset_for_user(self.admin, Chronicle.objects.all())
        self.assertEqual(qs.count(), 2)

    def test_anonymous_sees_none(self):
        """Anonymous users see no chronicles."""
        anon = AnonymousUser()
        qs = PermissionManager.filter_queryset_for_user(anon, Chronicle.objects.all())
        self.assertEqual(qs.count(), 0)


class DeploymentMixinExistenceTest(TestCase):
    """Verify all required view mixins exist and are configured."""

    def test_view_permission_mixin_exists(self):
        """ViewPermissionMixin exists and has correct permission."""
        self.assertEqual(ViewPermissionMixin.required_permission, Permission.VIEW_FULL)

    def test_edit_permission_mixin_exists(self):
        """EditPermissionMixin exists and has correct permission."""
        self.assertEqual(EditPermissionMixin.required_permission, Permission.EDIT_FULL)

    def test_spend_xp_mixin_exists(self):
        """SpendXPPermissionMixin exists and has correct permission."""
        self.assertEqual(SpendXPPermissionMixin.required_permission, Permission.SPEND_XP)

    def test_spend_freebies_mixin_exists(self):
        """SpendFreebiesPermissionMixin exists and has correct permission."""
        self.assertEqual(
            SpendFreebiesPermissionMixin.required_permission, Permission.SPEND_FREEBIES
        )

    def test_visibility_filter_mixin_exists(self):
        """VisibilityFilterMixin exists."""
        self.assertTrue(hasattr(VisibilityFilterMixin, "get_queryset"))

    def test_owner_required_mixin_exists(self):
        """OwnerRequiredMixin exists."""
        self.assertTrue(hasattr(OwnerRequiredMixin, "dispatch"))

    def test_st_required_mixin_exists(self):
        """STRequiredMixin exists."""
        self.assertTrue(hasattr(STRequiredMixin, "dispatch"))
