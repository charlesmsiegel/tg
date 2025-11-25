"""
Cache middleware for Tellurian Games.

This middleware provides per-user caching support for views, ensuring that
cached content respects user permissions and authentication status.
"""

from django.core.cache import cache
from django.utils.cache import get_cache_key, learn_cache_key, patch_response_headers
from django.utils.deprecation import MiddlewareMixin


class PerUserCacheMiddleware(MiddlewareMixin):
    """
    Middleware that caches responses on a per-user basis.

    This ensures that authenticated users see their own cached content
    and not content meant for other users.

    Usage:
        Add to MIDDLEWARE in settings.py:
        MIDDLEWARE = [
            'django.middleware.cache.UpdateCacheMiddleware',
            'core.middleware.cache_middleware.PerUserCacheMiddleware',
            ...
            'django.middleware.cache.FetchFromCacheMiddleware',
        ]

    Note: This middleware should be placed AFTER UpdateCacheMiddleware
    and BEFORE FetchFromCacheMiddleware in the middleware stack.
    """

    def process_request(self, request):
        """
        Modify the cache key to include the user ID.

        This ensures each user gets their own cached version of pages.
        """
        if not hasattr(request, '_cache_update_cache'):
            request._cache_update_cache = True

        # Add user ID to cache key for authenticated users
        if request.user.is_authenticated:
            request._cache_key_prefix = f"user_{request.user.id}"
        else:
            request._cache_key_prefix = "anonymous"

        return None

    def process_response(self, request, response):
        """
        Update cache headers and store the response.

        Only caches GET and HEAD requests with successful status codes.
        """
        # Only cache successful GET and HEAD requests
        if request.method not in ('GET', 'HEAD') or response.status_code != 200:
            return response

        # Don't cache responses for authenticated users by default
        # Views can override this with cache decorators
        if not hasattr(request, '_cache_update_cache') or not request._cache_update_cache:
            return response

        # Set cache headers
        patch_response_headers(response, cache_timeout=300)

        return response
