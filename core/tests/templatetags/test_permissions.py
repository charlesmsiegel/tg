"""Tests for permissions template tags."""

from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from core.permissions import Role, VisibilityTier
from core.templatetags.permissions import (
    is_full,
    is_game_st,
    is_none,
    is_owner,
    is_partial,
    is_st,
    user_can_edit,
    user_can_spend_freebies,
    user_can_spend_xp,
    user_can_view,
    user_has_permission,
    user_roles,
    visibility_tier,
)


class MockObject:
    """Mock object for testing permission checks."""

    def __init__(self, owner=None, chronicle=None, visibility_tier=None):
        self.owner = owner
        self.chronicle = chronicle
        self._visibility_tier = visibility_tier or VisibilityTier.FULL
        self._can_view = True
        self._can_edit = True
        self._can_spend_xp = True
        self._can_spend_freebies = True
        self._roles = set()

    def user_can_view(self, user):
        return self._can_view

    def user_can_edit(self, user):
        return self._can_edit

    def user_can_spend_xp(self, user):
        return self._can_spend_xp

    def user_can_spend_freebies(self, user):
        return self._can_spend_freebies

    def get_visibility_tier(self, user):
        return self._visibility_tier

    def get_user_roles(self, user):
        return self._roles


class MockChronicle:
    """Mock chronicle for testing ST relationships."""

    def __init__(self):
        self._game_storytellers = []

    @property
    def game_storytellers(self):
        return MockQuerySet(self._game_storytellers)


class MockQuerySet:
    """Mock queryset for testing filter/exists."""

    def __init__(self, items):
        self._items = items

    def filter(self, **kwargs):
        id_val = kwargs.get("id")
        if id_val is not None:
            return MockQuerySet([i for i in self._items if i.id == id_val])
        return self

    def exists(self):
        return len(self._items) > 0


class UserCanViewTagTest(TestCase):
    """Tests for user_can_view template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    @patch("core.templatetags.permissions.PermissionManager.user_can_view")
    def test_returns_true_when_user_can_view(self, mock_perm):
        """Test tag returns True when PermissionManager allows viewing."""
        mock_perm.return_value = True
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_view(context, obj)
        self.assertTrue(result)
        mock_perm.assert_called_once_with(self.user, obj)

    @patch("core.templatetags.permissions.PermissionManager.user_can_view")
    def test_returns_false_when_user_cannot_view(self, mock_perm):
        """Test tag returns False when PermissionManager denies viewing."""
        mock_perm.return_value = False
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_view(context, obj)
        self.assertFalse(result)
        mock_perm.assert_called_once_with(self.user, obj)


class UserCanEditTagTest(TestCase):
    """Tests for user_can_edit template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    @patch("core.templatetags.permissions.PermissionManager.user_can_edit")
    def test_returns_true_when_user_can_edit(self, mock_perm):
        """Test tag returns True when PermissionManager allows editing."""
        mock_perm.return_value = True
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_edit(context, obj)
        self.assertTrue(result)
        mock_perm.assert_called_once_with(self.user, obj)

    @patch("core.templatetags.permissions.PermissionManager.user_can_edit")
    def test_returns_false_when_user_cannot_edit(self, mock_perm):
        """Test tag returns False when PermissionManager denies editing."""
        mock_perm.return_value = False
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_edit(context, obj)
        self.assertFalse(result)
        mock_perm.assert_called_once_with(self.user, obj)


class UserCanSpendXPTagTest(TestCase):
    """Tests for user_can_spend_xp template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    @patch("core.templatetags.permissions.PermissionManager.user_can_spend_xp")
    def test_returns_true_when_user_can_spend_xp(self, mock_perm):
        """Test tag returns True when PermissionManager allows XP spending."""
        mock_perm.return_value = True
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_spend_xp(context, obj)
        self.assertTrue(result)
        mock_perm.assert_called_once_with(self.user, obj)

    @patch("core.templatetags.permissions.PermissionManager.user_can_spend_xp")
    def test_returns_false_when_user_cannot_spend_xp(self, mock_perm):
        """Test tag returns False when PermissionManager denies XP spending."""
        mock_perm.return_value = False
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_spend_xp(context, obj)
        self.assertFalse(result)
        mock_perm.assert_called_once_with(self.user, obj)


class UserCanSpendFreebiesTagTest(TestCase):
    """Tests for user_can_spend_freebies template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    @patch("core.templatetags.permissions.PermissionManager.user_can_spend_freebies")
    def test_returns_true_when_user_can_spend_freebies(self, mock_perm):
        """Test tag returns True when PermissionManager allows freebie spending."""
        mock_perm.return_value = True
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_spend_freebies(context, obj)
        self.assertTrue(result)
        mock_perm.assert_called_once_with(self.user, obj)

    @patch("core.templatetags.permissions.PermissionManager.user_can_spend_freebies")
    def test_returns_false_when_user_cannot_spend_freebies(self, mock_perm):
        """Test tag returns False when PermissionManager denies freebie spending."""
        mock_perm.return_value = False
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_can_spend_freebies(context, obj)
        self.assertFalse(result)
        mock_perm.assert_called_once_with(self.user, obj)


class UserHasPermissionTagTest(TestCase):
    """Tests for user_has_permission template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

    def test_returns_true_for_valid_permission(self):
        """Test tag returns True for valid permission the user has."""
        request = self.factory.get("/")
        request.user = self.admin
        context = {"request": request}

        obj = MockObject(owner=self.user)

        result = user_has_permission(context, obj, "EDIT_FULL")
        self.assertTrue(result)

    def test_returns_false_for_permission_user_lacks(self):
        """Test tag returns False for permission user doesn't have."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        # Object not owned by user, no admin rights
        obj = MockObject()

        result = user_has_permission(context, obj, "DELETE")
        self.assertFalse(result)

    def test_returns_false_for_invalid_permission_name(self):
        """Test tag returns False for invalid permission names."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = MockObject()

        result = user_has_permission(context, obj, "INVALID_PERMISSION")
        self.assertFalse(result)

    def test_handles_various_permission_names(self):
        """Test tag handles various permission name formats."""
        request = self.factory.get("/")
        request.user = self.admin
        context = {"request": request}

        obj = MockObject()

        # Valid permission names
        for perm in ["VIEW_FULL", "VIEW_PARTIAL", "EDIT_FULL", "EDIT_LIMITED"]:
            result = user_has_permission(context, obj, perm)
            self.assertIsInstance(result, bool)


class VisibilityTierTagTest(TestCase):
    """Tests for visibility_tier template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    @patch("core.templatetags.permissions.PermissionManager.get_visibility_tier")
    def test_returns_full_visibility_tier(self, mock_perm):
        """Test tag returns FULL visibility tier."""
        mock_perm.return_value = VisibilityTier.FULL
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = visibility_tier(context, obj)
        self.assertEqual(result, VisibilityTier.FULL)
        mock_perm.assert_called_once_with(self.user, obj)

    @patch("core.templatetags.permissions.PermissionManager.get_visibility_tier")
    def test_returns_partial_visibility_tier(self, mock_perm):
        """Test tag returns PARTIAL visibility tier."""
        mock_perm.return_value = VisibilityTier.PARTIAL
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = visibility_tier(context, obj)
        self.assertEqual(result, VisibilityTier.PARTIAL)
        mock_perm.assert_called_once_with(self.user, obj)

    @patch("core.templatetags.permissions.PermissionManager.get_visibility_tier")
    def test_returns_none_visibility_tier(self, mock_perm):
        """Test tag returns NONE visibility tier."""
        mock_perm.return_value = VisibilityTier.NONE
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = visibility_tier(context, obj)
        self.assertEqual(result, VisibilityTier.NONE)
        mock_perm.assert_called_once_with(self.user, obj)


class UserRolesTagTest(TestCase):
    """Tests for user_roles template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    @patch("core.templatetags.permissions.PermissionManager.get_user_roles")
    def test_returns_user_roles(self, mock_perm):
        """Test tag returns set of user roles."""
        mock_perm.return_value = {Role.OWNER, Role.AUTHENTICATED}
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_roles(context, obj)
        self.assertEqual(result, {Role.OWNER, Role.AUTHENTICATED})
        mock_perm.assert_called_once_with(self.user, obj)

    @patch("core.templatetags.permissions.PermissionManager.get_user_roles")
    def test_returns_empty_set_when_no_roles(self, mock_perm):
        """Test tag returns empty set when user has no roles."""
        mock_perm.return_value = set()
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = Mock()
        result = user_roles(context, obj)
        self.assertEqual(result, set())
        mock_perm.assert_called_once_with(self.user, obj)


class IsFullFilterTest(TestCase):
    """Tests for is_full filter."""

    def test_returns_true_for_full_tier(self):
        """Test filter returns True for FULL tier."""
        self.assertTrue(is_full(VisibilityTier.FULL))

    def test_returns_false_for_partial_tier(self):
        """Test filter returns False for PARTIAL tier."""
        self.assertFalse(is_full(VisibilityTier.PARTIAL))

    def test_returns_false_for_none_tier(self):
        """Test filter returns False for NONE tier."""
        self.assertFalse(is_full(VisibilityTier.NONE))


class IsPartialFilterTest(TestCase):
    """Tests for is_partial filter."""

    def test_returns_true_for_partial_tier(self):
        """Test filter returns True for PARTIAL tier."""
        self.assertTrue(is_partial(VisibilityTier.PARTIAL))

    def test_returns_false_for_full_tier(self):
        """Test filter returns False for FULL tier."""
        self.assertFalse(is_partial(VisibilityTier.FULL))

    def test_returns_false_for_none_tier(self):
        """Test filter returns False for NONE tier."""
        self.assertFalse(is_partial(VisibilityTier.NONE))


class IsNoneFilterTest(TestCase):
    """Tests for is_none filter."""

    def test_returns_true_for_none_tier(self):
        """Test filter returns True for NONE tier."""
        self.assertTrue(is_none(VisibilityTier.NONE))

    def test_returns_false_for_full_tier(self):
        """Test filter returns False for FULL tier."""
        self.assertFalse(is_none(VisibilityTier.FULL))

    def test_returns_false_for_partial_tier(self):
        """Test filter returns False for PARTIAL tier."""
        self.assertFalse(is_none(VisibilityTier.PARTIAL))


class IsOwnerTagTest(TestCase):
    """Tests for is_owner template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="password"
        )

    def test_returns_true_when_user_is_owner(self):
        """Test tag returns True when user is owner of object."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = MockObject(owner=self.user)

        result = is_owner(context, obj)
        self.assertTrue(result)

    def test_returns_false_when_user_is_not_owner(self):
        """Test tag returns False when user is not owner of object."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = MockObject(owner=self.other_user)

        result = is_owner(context, obj)
        self.assertFalse(result)

    def test_returns_false_when_object_has_no_owner(self):
        """Test tag returns False when object has no owner attribute."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        class NoOwnerObject:
            pass

        obj = NoOwnerObject()

        result = is_owner(context, obj)
        self.assertFalse(result)

    def test_checks_user_attribute_as_fallback(self):
        """Test tag checks user attribute if owner not present."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        class UserObject:
            def __init__(self, user):
                self.user = user

        obj = UserObject(self.user)

        result = is_owner(context, obj)
        self.assertTrue(result)


class IsSTTagTest(TestCase):
    """Tests for is_st template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    def test_returns_false_for_anonymous_user(self):
        """Test tag returns False for anonymous users."""
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get("/")
        request.user = AnonymousUser()
        context = {"request": request}

        result = is_st(context)
        self.assertFalse(result)

    def test_returns_true_for_superuser(self):
        """Test tag returns True for superuser."""
        admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

        request = self.factory.get("/")
        request.user = admin
        context = {"request": request}

        result = is_st(context)
        self.assertTrue(result)

    def test_returns_true_for_staff_user(self):
        """Test tag returns True for staff user."""
        staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password",
            is_staff=True,
        )

        request = self.factory.get("/")
        request.user = staff
        context = {"request": request}

        result = is_st(context)
        self.assertTrue(result)

    def test_delegates_to_profile_is_st(self):
        """Test tag delegates to profile.is_st() for regular users."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        # Result depends on user's ST relationships
        result = is_st(context)
        self.assertIsInstance(result, bool)


class IsGameSTTagTest(TestCase):
    """Tests for is_game_st template tag."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

    def test_returns_false_when_no_chronicle(self):
        """Test tag returns False when object has no chronicle."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        obj = MockObject(chronicle=None)

        result = is_game_st(context, obj)
        self.assertFalse(result)

    def test_returns_true_when_user_is_game_st(self):
        """Test tag returns True when user is game ST of chronicle."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        chronicle = MockChronicle()
        chronicle._game_storytellers = [self.user]
        obj = MockObject(chronicle=chronicle)

        result = is_game_st(context, obj)
        self.assertTrue(result)

    def test_returns_false_when_user_is_not_game_st(self):
        """Test tag returns False when user is not game ST of chronicle."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        chronicle = MockChronicle()
        chronicle._game_storytellers = []
        obj = MockObject(chronicle=chronicle)

        result = is_game_st(context, obj)
        self.assertFalse(result)

    def test_returns_false_when_chronicle_has_no_game_storytellers_attr(self):
        """Test tag returns False when chronicle lacks game_storytellers."""
        request = self.factory.get("/")
        request.user = self.user
        context = {"request": request}

        class SimpleChronicle:
            pass

        obj = MockObject()
        obj.chronicle = SimpleChronicle()

        result = is_game_st(context, obj)
        self.assertFalse(result)
