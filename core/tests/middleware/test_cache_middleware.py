"""Tests for cache_middleware module."""

from core.middleware.cache_middleware import PerUserCacheMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils.cache import patch_response_headers


class PerUserCacheMiddlewareTest(TestCase):
    """Tests for PerUserCacheMiddleware."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        self.middleware = PerUserCacheMiddleware(get_response=lambda r: HttpResponse("OK"))

    def test_process_request_sets_cache_update_cache_flag(self):
        """Test that process_request sets _cache_update_cache flag."""
        request = self.factory.get("/")
        request.user = self.user

        result = self.middleware.process_request(request)

        self.assertIsNone(result)
        self.assertTrue(request._cache_update_cache)

    def test_process_request_sets_user_prefix_for_authenticated_user(self):
        """Test that process_request sets user-specific cache key prefix."""
        request = self.factory.get("/")
        request.user = self.user

        self.middleware.process_request(request)

        self.assertEqual(request._cache_key_prefix, f"user_{self.user.id}")

    def test_process_request_sets_anonymous_prefix_for_unauthenticated_user(self):
        """Test that process_request sets anonymous prefix for anonymous user."""
        request = self.factory.get("/")
        request.user = AnonymousUser()

        self.middleware.process_request(request)

        self.assertEqual(request._cache_key_prefix, "anonymous")

    def test_process_request_does_not_override_existing_cache_flag(self):
        """Test that process_request doesn't override existing _cache_update_cache flag."""
        request = self.factory.get("/")
        request.user = self.user
        request._cache_update_cache = False

        self.middleware.process_request(request)

        self.assertFalse(request._cache_update_cache)

    def test_process_response_returns_response_for_non_get_request(self):
        """Test that process_response returns response unchanged for non-GET requests."""
        request = self.factory.post("/")
        request.user = self.user
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result, response)

    def test_process_response_returns_response_for_head_request(self):
        """Test that process_response returns response unchanged for HEAD requests with non-200 status."""
        request = self.factory.head("/")
        request.user = self.user
        response = HttpResponse("Not Found", status=404)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result, response)

    def test_process_response_returns_response_for_non_200_status(self):
        """Test that process_response returns response unchanged for non-200 status."""
        request = self.factory.get("/")
        request.user = self.user
        response = HttpResponse("Error", status=500)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result, response)

    def test_process_response_returns_response_when_cache_update_false(self):
        """Test that process_response returns response when _cache_update_cache is False."""
        request = self.factory.get("/")
        request.user = self.user
        request._cache_update_cache = False
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result, response)

    def test_process_response_returns_response_when_no_cache_flag(self):
        """Test that process_response returns response when _cache_update_cache not set."""
        request = self.factory.get("/")
        request.user = self.user
        # Don't set _cache_update_cache
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result, response)

    def test_process_response_patches_headers_for_cacheable_get_request(self):
        """Test that process_response patches cache headers for cacheable GET requests."""
        request = self.factory.get("/")
        request.user = self.user
        request._cache_update_cache = True
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result, response)
        # Check that cache-control header was set
        self.assertIn("Cache-Control", result)

    def test_process_response_patches_headers_for_cacheable_head_request(self):
        """Test that process_response patches cache headers for cacheable HEAD requests."""
        request = self.factory.head("/")
        request.user = self.user
        request._cache_update_cache = True
        response = HttpResponse("OK", status=200)

        result = self.middleware.process_response(request, response)

        self.assertEqual(result, response)
        # Check that cache-control header was set
        self.assertIn("Cache-Control", result)

    def test_middleware_full_flow_authenticated_user(self):
        """Test the full middleware flow for an authenticated user."""
        request = self.factory.get("/")
        request.user = self.user

        # Process request
        self.middleware.process_request(request)

        # Create response
        response = HttpResponse("OK", status=200)

        # Process response
        result = self.middleware.process_response(request, response)

        # Verify flow
        self.assertTrue(request._cache_update_cache)
        self.assertEqual(request._cache_key_prefix, f"user_{self.user.id}")
        self.assertIn("Cache-Control", result)

    def test_middleware_full_flow_anonymous_user(self):
        """Test the full middleware flow for an anonymous user."""
        request = self.factory.get("/")
        request.user = AnonymousUser()

        # Process request
        self.middleware.process_request(request)

        # Create response
        response = HttpResponse("OK", status=200)

        # Process response
        result = self.middleware.process_response(request, response)

        # Verify flow
        self.assertTrue(request._cache_update_cache)
        self.assertEqual(request._cache_key_prefix, "anonymous")
        self.assertIn("Cache-Control", result)

    def test_middleware_initialization(self):
        """Test middleware initialization with get_response."""
        get_response = lambda r: HttpResponse("OK")
        middleware = PerUserCacheMiddleware(get_response=get_response)

        self.assertEqual(middleware.get_response, get_response)
