"""Tests for approved_user middleware module."""

from core.middleware.approved_user import UserListMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse
from django.test import RequestFactory, TestCase


class UserListMiddlewareTest(TestCase):
    """Tests for UserListMiddleware."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@test.com", password="testpass123"
        )
        self.staff_user = User.objects.create_user(
            username="staff", email="staff@test.com", password="testpass123", is_staff=True
        )
        self.response_content = "Test Response"
        self.get_response = lambda r: HttpResponse(self.response_content)
        self.middleware = UserListMiddleware(get_response=self.get_response)

    def test_middleware_initialization(self):
        """Test middleware initialization with get_response."""
        get_response = lambda r: HttpResponse("OK")
        middleware = UserListMiddleware(get_response=get_response)

        self.assertEqual(middleware.get_response, get_response)

    def test_sets_is_approved_user_true_for_authenticated_staff(self):
        """Test that is_approved_user is True for authenticated staff user."""
        request = self.factory.get("/")
        request.user = self.staff_user

        response = self.middleware(request)

        self.assertTrue(request.is_approved_user)

    def test_sets_is_approved_user_false_for_authenticated_non_staff(self):
        """Test that is_approved_user is False for authenticated non-staff user."""
        request = self.factory.get("/")
        request.user = self.regular_user

        response = self.middleware(request)

        self.assertFalse(request.is_approved_user)

    def test_sets_is_approved_user_false_for_anonymous_user(self):
        """Test that is_approved_user is False for anonymous user."""
        request = self.factory.get("/")
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertFalse(request.is_approved_user)

    def test_returns_response_from_get_response(self):
        """Test that middleware returns the response from get_response."""
        request = self.factory.get("/")
        request.user = self.regular_user

        response = self.middleware(request)

        self.assertEqual(response.content.decode(), self.response_content)

    def test_calls_get_response_once(self):
        """Test that middleware calls get_response exactly once."""
        call_count = 0

        def counting_get_response(request):
            nonlocal call_count
            call_count += 1
            return HttpResponse("OK")

        middleware = UserListMiddleware(get_response=counting_get_response)
        request = self.factory.get("/")
        request.user = self.regular_user

        middleware(request)

        self.assertEqual(call_count, 1)

    def test_superuser_staff_is_approved(self):
        """Test that superuser with staff status is approved."""
        superuser = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass123"
        )
        request = self.factory.get("/")
        request.user = superuser

        self.middleware(request)

        self.assertTrue(request.is_approved_user)

    def test_superuser_without_staff_is_not_approved(self):
        """Test that superuser without staff status is not approved."""
        # Create superuser and remove staff status
        superuser = User.objects.create_superuser(
            username="admin2", email="admin2@test.com", password="testpass123"
        )
        superuser.is_staff = False
        superuser.save()

        request = self.factory.get("/")
        request.user = superuser

        self.middleware(request)

        self.assertFalse(request.is_approved_user)

    def test_works_with_different_request_methods(self):
        """Test that middleware works with different HTTP methods."""
        methods = [
            self.factory.get,
            self.factory.post,
            self.factory.put,
            self.factory.patch,
            self.factory.delete,
        ]

        for method in methods:
            request = method("/")
            request.user = self.staff_user

            response = self.middleware(request)

            self.assertTrue(request.is_approved_user)
            self.assertEqual(response.status_code, 200)
