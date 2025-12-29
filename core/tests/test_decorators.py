"""Tests for permission decorators in core/decorators.py."""

from unittest.mock import Mock, patch

from characters.models.core.character import Character
from core.decorators import (
    require_edit_permission,
    require_model_permission,
    require_permission,
    require_spend_freebies_permission,
    require_spend_xp_permission,
    require_view_permission,
)
from core.permissions import Permission
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory, TestCase
from game.models import Chronicle


class RequirePermissionDecoratorTest(TestCase):
    """Tests for the require_permission decorator."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_require_permission_raises_value_error_when_model_not_specified(self):
        """Test that decorator raises ValueError when model class is not set."""

        @require_permission(Permission.VIEW_FULL)
        def test_view(request, pk):
            return "success"

        request = self.factory.get("/")
        request.user = self.owner

        with self.assertRaises(ValueError) as cm:
            test_view(request, pk=self.character.pk)
        self.assertIn("Model class not specified", str(cm.exception))

    def test_require_permission_raises_404_when_object_not_found(self):
        """Test that decorator raises 404 when object doesn't exist."""

        @require_permission(Permission.VIEW_FULL)
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        with self.assertRaises(Http404):
            test_view(request, pk=99999)

    def test_require_permission_raises_404_when_no_permission_and_raise_404_true(self):
        """Test that decorator raises 404 when permission denied and raise_404=True."""

        @require_permission(Permission.EDIT_FULL, raise_404=True)
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.stranger

        with self.assertRaises(Http404):
            test_view(request, pk=self.character.pk)

    def test_require_permission_raises_403_when_no_permission_and_raise_404_false(self):
        """Test that decorator raises 403 when permission denied and raise_404=False."""

        @require_permission(Permission.EDIT_FULL, raise_404=False)
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.stranger

        with self.assertRaises(PermissionDenied):
            test_view(request, pk=self.character.pk)

    def test_require_permission_allows_access_when_permission_granted(self):
        """Test that decorator allows access when user has permission."""

        @require_permission(Permission.VIEW_FULL)
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, "success")

    def test_require_permission_attaches_object_to_request(self):
        """Test that decorator attaches object to request.permission_object."""

        @require_permission(Permission.VIEW_FULL)
        def test_view(request, pk):
            return request.permission_object

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, self.character)

    def test_require_permission_with_custom_lookup_param(self):
        """Test that decorator works with custom lookup parameter."""

        @require_permission(Permission.VIEW_FULL, lookup="char_id")
        def test_view(request, char_id):
            return request.permission_object

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, char_id=self.character.pk)
        self.assertEqual(result, self.character)

    def test_require_permission_preserves_function_metadata(self):
        """Test that decorator preserves the wrapped function's metadata."""

        @require_permission(Permission.VIEW_FULL)
        def my_test_view(request, pk):
            """My docstring."""
            return "success"

        self.assertEqual(my_test_view.__name__, "my_test_view")
        self.assertEqual(my_test_view.__doc__, "My docstring.")


class RequireViewPermissionDecoratorTest(TestCase):
    """Tests for require_view_permission shortcut decorator."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_require_view_permission_allows_owner(self):
        """Test that view permission allows owner access."""

        @require_view_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, "success")

    def test_require_view_permission_raises_404_for_stranger(self):
        """Test that view permission raises 404 for unauthorized user."""

        @require_view_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.stranger

        with self.assertRaises(Http404):
            test_view(request, pk=self.character.pk)


class RequireEditPermissionDecoratorTest(TestCase):
    """Tests for require_edit_permission shortcut decorator."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_require_edit_permission_allows_head_st(self):
        """Test that edit permission allows head ST access."""

        @require_edit_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.head_st

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, "success")

    def test_require_edit_permission_raises_403_for_owner(self):
        """Test that edit permission raises 403 for owner (no EDIT_FULL)."""

        @require_edit_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        with self.assertRaises(PermissionDenied):
            test_view(request, pk=self.character.pk)


class RequireSpendXPPermissionDecoratorTest(TestCase):
    """Tests for require_spend_xp_permission shortcut decorator."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_require_spend_xp_permission_allows_owner(self):
        """Test that spend XP permission allows owner access on approved character."""

        @require_spend_xp_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, "success")

    def test_require_spend_xp_permission_raises_403_for_stranger(self):
        """Test that spend XP permission raises 403 for unauthorized user."""

        @require_spend_xp_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.stranger

        with self.assertRaises(PermissionDenied):
            test_view(request, pk=self.character.pk)


class RequireSpendFreebiesPermissionDecoratorTest(TestCase):
    """Tests for require_spend_freebies_permission shortcut decorator."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.unfinished_character = Character.objects.create(
            name="Unfinished Character", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        self.approved_character = Character.objects.create(
            name="Approved Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_require_spend_freebies_permission_allows_owner_on_unfinished(self):
        """Test that spend freebies permission allows owner on unfinished character."""

        @require_spend_freebies_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, pk=self.unfinished_character.pk)
        self.assertEqual(result, "success")

    def test_require_spend_freebies_permission_raises_403_on_approved(self):
        """Test that spend freebies permission raises 403 on approved character."""

        @require_spend_freebies_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.owner

        with self.assertRaises(PermissionDenied):
            test_view(request, pk=self.approved_character.pk)

    def test_require_spend_freebies_permission_raises_403_for_stranger(self):
        """Test that spend freebies permission raises 403 for unauthorized user."""

        @require_spend_freebies_permission
        def test_view(request, pk):
            return "success"

        test_view.model = Character
        request = self.factory.get("/")
        request.user = self.stranger

        with self.assertRaises(PermissionDenied):
            test_view(request, pk=self.unfinished_character.pk)


class RequireModelPermissionDecoratorTest(TestCase):
    """Tests for require_model_permission decorator with explicit model class."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_require_model_permission_allows_access_with_permission(self):
        """Test that decorator allows access when user has permission."""

        @require_model_permission(Character, Permission.VIEW_FULL)
        def test_view(request, pk):
            return "success"

        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, "success")

    def test_require_model_permission_raises_404_when_object_not_found(self):
        """Test that decorator raises 404 when object doesn't exist."""

        @require_model_permission(Character, Permission.VIEW_FULL)
        def test_view(request, pk):
            return "success"

        request = self.factory.get("/")
        request.user = self.owner

        with self.assertRaises(Http404):
            test_view(request, pk=99999)

    def test_require_model_permission_raises_404_when_no_permission_and_raise_404_true(self):
        """Test that decorator raises 404 when permission denied and raise_404=True."""

        @require_model_permission(Character, Permission.EDIT_FULL, raise_404=True)
        def test_view(request, pk):
            return "success"

        request = self.factory.get("/")
        request.user = self.stranger

        with self.assertRaises(Http404):
            test_view(request, pk=self.character.pk)

    def test_require_model_permission_raises_403_when_no_permission_and_raise_404_false(self):
        """Test that decorator raises 403 when permission denied and raise_404=False."""

        @require_model_permission(Character, Permission.EDIT_FULL, raise_404=False)
        def test_view(request, pk):
            return "success"

        request = self.factory.get("/")
        request.user = self.stranger

        with self.assertRaises(PermissionDenied):
            test_view(request, pk=self.character.pk)

    def test_require_model_permission_attaches_object_to_request(self):
        """Test that decorator attaches object to request.permission_object."""

        @require_model_permission(Character, Permission.VIEW_FULL)
        def test_view(request, pk):
            return request.permission_object

        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, self.character)

    def test_require_model_permission_with_custom_lookup_param(self):
        """Test that decorator works with custom lookup parameter."""

        @require_model_permission(Character, Permission.VIEW_FULL, lookup="char_id")
        def test_view(request, char_id):
            return request.permission_object

        request = self.factory.get("/")
        request.user = self.owner

        result = test_view(request, char_id=self.character.pk)
        self.assertEqual(result, self.character)

    def test_require_model_permission_preserves_function_metadata(self):
        """Test that decorator preserves the wrapped function's metadata."""

        @require_model_permission(Character, Permission.VIEW_FULL)
        def my_test_view(request, pk):
            """My docstring."""
            return "success"

        self.assertEqual(my_test_view.__name__, "my_test_view")
        self.assertEqual(my_test_view.__doc__, "My docstring.")

    def test_require_model_permission_head_st_can_edit(self):
        """Test that head ST can access with EDIT_FULL permission."""

        @require_model_permission(Character, Permission.EDIT_FULL)
        def test_view(request, pk):
            return "success"

        request = self.factory.get("/")
        request.user = self.head_st

        result = test_view(request, pk=self.character.pk)
        self.assertEqual(result, "success")
