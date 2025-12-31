"""Tests for context processors in core/context_processors.py."""

from unittest.mock import Mock, patch

from core.context_processors import add_special_user_flag, all_chronicles, permissions
from core.permissions import Permission, Role, VisibilityTier
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from game.models import Chronicle


class AllChroniclesContextProcessorTest(TestCase):
    """Tests for all_chronicles context processor."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()

    def test_returns_empty_queryset_when_no_chronicles(self):
        """Test that empty queryset is returned when no chronicles exist."""
        request = self.factory.get("/")

        result = all_chronicles(request)

        self.assertIn("chronicles", result)
        self.assertEqual(result["chronicles"].count(), 0)

    def test_returns_all_chronicles(self):
        """Test that all chronicles are returned."""
        Chronicle.objects.create(name="Chronicle 1")
        Chronicle.objects.create(name="Chronicle 2")
        Chronicle.objects.create(name="Chronicle 3")

        request = self.factory.get("/")

        result = all_chronicles(request)

        self.assertIn("chronicles", result)
        self.assertEqual(result["chronicles"].count(), 3)

    def test_returns_chronicles_queryset(self):
        """Test that the result is a QuerySet."""
        Chronicle.objects.create(name="Test Chronicle")

        request = self.factory.get("/")

        result = all_chronicles(request)

        from django.db.models import QuerySet

        self.assertIsInstance(result["chronicles"], QuerySet)


class AddSpecialUserFlagContextProcessorTest(TestCase):
    """Tests for add_special_user_flag context processor."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()

    def test_returns_true_when_is_approved_user_true(self):
        """Test that True is returned when request.is_approved_user is True."""
        request = self.factory.get("/")
        request.is_approved_user = True

        result = add_special_user_flag(request)

        self.assertIn("is_approved_user", result)
        self.assertTrue(result["is_approved_user"])

    def test_returns_false_when_is_approved_user_false(self):
        """Test that False is returned when request.is_approved_user is False."""
        request = self.factory.get("/")
        request.is_approved_user = False

        result = add_special_user_flag(request)

        self.assertIn("is_approved_user", result)
        self.assertFalse(result["is_approved_user"])

    def test_returns_false_when_is_approved_user_not_set(self):
        """Test that False is returned when request.is_approved_user is not set."""
        request = self.factory.get("/")
        # Don't set is_approved_user attribute

        result = add_special_user_flag(request)

        self.assertIn("is_approved_user", result)
        self.assertFalse(result["is_approved_user"])


class PermissionsContextProcessorTest(TestCase):
    """Tests for permissions context processor."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

    def test_returns_visibility_tier_enum(self):
        """Test that VisibilityTier enum is in context."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        self.assertIn("VisibilityTier", result)
        self.assertEqual(result["VisibilityTier"], VisibilityTier)

    def test_returns_permission_enum(self):
        """Test that Permission enum is in context."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        self.assertIn("Permission", result)
        self.assertEqual(result["Permission"], Permission)

    def test_returns_role_enum(self):
        """Test that Role enum is in context."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        self.assertIn("Role", result)
        self.assertEqual(result["Role"], Role)

    def test_returns_user_can_view_callable(self):
        """Test that user_can_view callable is in context."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        self.assertIn("user_can_view", result)
        self.assertTrue(callable(result["user_can_view"]))

    def test_returns_user_can_edit_callable(self):
        """Test that user_can_edit callable is in context."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        self.assertIn("user_can_edit", result)
        self.assertTrue(callable(result["user_can_edit"]))

    def test_user_can_view_returns_true_when_object_has_method_returning_true(self):
        """Test that user_can_view returns True when object.user_can_view returns True."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        mock_obj = Mock()
        mock_obj.user_can_view = Mock(return_value=True)

        can_view = result["user_can_view"](mock_obj)
        self.assertTrue(can_view)
        mock_obj.user_can_view.assert_called_once_with(self.user)

    def test_user_can_view_returns_false_when_object_has_method_returning_false(self):
        """Test that user_can_view returns False when object.user_can_view returns False."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        mock_obj = Mock()
        mock_obj.user_can_view = Mock(return_value=False)

        can_view = result["user_can_view"](mock_obj)
        self.assertFalse(can_view)

    def test_user_can_view_returns_false_when_object_has_no_method(self):
        """Test that user_can_view returns False when object has no user_can_view method."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        mock_obj = object()  # Plain object with no user_can_view method

        can_view = result["user_can_view"](mock_obj)
        self.assertFalse(can_view)

    def test_user_can_edit_returns_true_when_object_has_method_returning_true(self):
        """Test that user_can_edit returns True when object.user_can_edit returns True."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        mock_obj = Mock()
        mock_obj.user_can_edit = Mock(return_value=True)

        can_edit = result["user_can_edit"](mock_obj)
        self.assertTrue(can_edit)
        mock_obj.user_can_edit.assert_called_once_with(self.user)

    def test_user_can_edit_returns_false_when_object_has_method_returning_false(self):
        """Test that user_can_edit returns False when object.user_can_edit returns False."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        mock_obj = Mock()
        mock_obj.user_can_edit = Mock(return_value=False)

        can_edit = result["user_can_edit"](mock_obj)
        self.assertFalse(can_edit)

    def test_user_can_edit_returns_false_when_object_has_no_method(self):
        """Test that user_can_edit returns False when object has no user_can_edit method."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        mock_obj = object()  # Plain object with no user_can_edit method

        can_edit = result["user_can_edit"](mock_obj)
        self.assertFalse(can_edit)

    def test_visibility_tier_enum_values_accessible(self):
        """Test that VisibilityTier enum values are accessible."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        VT = result["VisibilityTier"]
        self.assertEqual(VT.FULL, VisibilityTier.FULL)
        self.assertEqual(VT.PARTIAL, VisibilityTier.PARTIAL)
        self.assertEqual(VT.NONE, VisibilityTier.NONE)

    def test_permission_enum_values_accessible(self):
        """Test that Permission enum values are accessible."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        P = result["Permission"]
        self.assertEqual(P.VIEW_FULL, Permission.VIEW_FULL)
        self.assertEqual(P.EDIT_FULL, Permission.EDIT_FULL)

    def test_role_enum_values_accessible(self):
        """Test that Role enum values are accessible."""
        request = self.factory.get("/")
        request.user = self.user

        result = permissions(request)

        R = result["Role"]
        self.assertEqual(R.OWNER, Role.OWNER)
        self.assertEqual(R.ADMIN, Role.ADMIN)
