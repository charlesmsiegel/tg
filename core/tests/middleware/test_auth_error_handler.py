"""Tests for auth_error_handler middleware module."""


from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from core.middleware.auth_error_handler import AuthErrorHandlerMiddleware


class AuthErrorHandlerMiddlewareTest(TestCase):
    """Tests for AuthErrorHandlerMiddleware."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        self.get_response = lambda r: HttpResponse("OK")
        self.middleware = AuthErrorHandlerMiddleware(get_response=self.get_response)

    def test_middleware_initialization(self):
        """Test middleware initialization with get_response."""
        get_response = lambda r: HttpResponse("OK")
        middleware = AuthErrorHandlerMiddleware(get_response=get_response)

        self.assertEqual(middleware.get_response, get_response)

    def test_returns_normal_response_unchanged(self):
        """Test that normal responses are returned unchanged."""
        request = self.factory.get("/")
        request.user = self.user

        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")

    def test_returns_non_redirect_response_unchanged(self):
        """Test that non-redirect responses are returned unchanged."""
        middleware = AuthErrorHandlerMiddleware(
            get_response=lambda r: HttpResponse("Not Found", status=404)
        )
        request = self.factory.get("/")
        request.user = self.user

        response = middleware(request)

        self.assertEqual(response.status_code, 404)

    @override_settings(LOGIN_URL="login")
    def test_returns_401_when_redirecting_to_login_for_anonymous(self):
        """Test that 401 is returned when anonymous user is redirected to login."""
        login_url = reverse("login")
        middleware = AuthErrorHandlerMiddleware(
            get_response=lambda r: HttpResponseRedirect(login_url)
        )
        request = self.factory.get("/protected/")
        request.user = AnonymousUser()

        response = middleware(request)

        self.assertEqual(response.status_code, 401)

    @override_settings(LOGIN_URL="login")
    def test_returns_redirect_when_authenticated_user_redirected_to_login(self):
        """Test that redirect is preserved when authenticated user is redirected to login."""
        login_url = reverse("login")
        middleware = AuthErrorHandlerMiddleware(
            get_response=lambda r: HttpResponseRedirect(login_url)
        )
        request = self.factory.get("/")
        request.user = self.user

        response = middleware(request)

        # Should return redirect since user is authenticated
        self.assertIsInstance(response, HttpResponseRedirect)

    @override_settings(LOGIN_URL="login")
    def test_returns_redirect_when_redirecting_elsewhere(self):
        """Test that redirects to non-login URLs are preserved."""
        middleware = AuthErrorHandlerMiddleware(
            get_response=lambda r: HttpResponseRedirect("/other/")
        )
        request = self.factory.get("/")
        request.user = AnonymousUser()

        response = middleware(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "/other/")

    def test_process_exception_handles_permission_denied(self):
        """Test that process_exception returns 403 for PermissionDenied."""
        request = self.factory.get("/")
        request.user = self.user
        exception = PermissionDenied("Access denied")

        response = self.middleware.process_exception(request, exception)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 403)

    def test_process_exception_returns_none_for_other_exceptions(self):
        """Test that process_exception returns None for non-PermissionDenied exceptions."""
        request = self.factory.get("/")
        request.user = self.user
        exception = ValueError("Some error")

        response = self.middleware.process_exception(request, exception)

        self.assertIsNone(response)

    def test_process_exception_returns_none_for_generic_exception(self):
        """Test that process_exception returns None for generic Exception."""
        request = self.factory.get("/")
        request.user = self.user
        exception = Exception("Generic error")

        response = self.middleware.process_exception(request, exception)

        self.assertIsNone(response)

    def test_process_exception_returns_none_for_type_error(self):
        """Test that process_exception returns None for TypeError."""
        request = self.factory.get("/")
        request.user = self.user
        exception = TypeError("Type error")

        response = self.middleware.process_exception(request, exception)

        self.assertIsNone(response)

    def test_middleware_with_anonymous_user_non_login_redirect(self):
        """Test that anonymous user redirected elsewhere gets redirect response."""
        middleware = AuthErrorHandlerMiddleware(
            get_response=lambda r: HttpResponseRedirect("/dashboard/")
        )
        request = self.factory.get("/")
        request.user = AnonymousUser()

        response = middleware(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "/dashboard/")


@override_settings(LOGIN_URL="login")
class AuthErrorHandlerMiddlewareLoginRedirectTest(TestCase):
    """Tests specifically for login redirect behavior."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.login_url = reverse("login")
        self.middleware = AuthErrorHandlerMiddleware(
            get_response=lambda r: HttpResponseRedirect(self.login_url)
        )

    def test_anonymous_user_gets_401_on_login_redirect(self):
        """Test that anonymous users get 401 on login redirect."""
        request = self.factory.get("/protected/")
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_preserves_login_redirect(self):
        """Test that authenticated users preserve login redirects."""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        request = self.factory.get("/")
        request.user = user

        response = self.middleware(request)

        self.assertIsInstance(response, HttpResponseRedirect)

    def test_login_redirect_with_next_param_still_returns_401(self):
        """Test that login redirect with next parameter still returns 401 for anonymous."""
        middleware = AuthErrorHandlerMiddleware(
            get_response=lambda r: HttpResponseRedirect(f"{self.login_url}?next=/dashboard/")
        )
        request = self.factory.get("/dashboard/")
        request.user = AnonymousUser()

        response = middleware(request)

        self.assertEqual(response.status_code, 401)
