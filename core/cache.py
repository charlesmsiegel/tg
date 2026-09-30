"""
Cache utilities for the Tellurian Games application.

This module provides utilities for caching expensive operations, particularly
database queries and view rendering. It includes:
- Cache key generation utilities
- A function-result caching decorator
- A cached reference-list helper
- Per-visitor page caching

Nothing here invalidates entries early: cached values live until their timeout expires.
"""

import hashlib
from collections.abc import Callable
from functools import wraps
from typing import Any

from django.conf import settings
from django.contrib.messages.storage.cookie import CookieStorage
from django.core.cache import cache
from django.db.models import Model
from django.utils.cache import patch_vary_headers
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

# Default for cache.get(): a miss returns this, so a cached None counts as a hit.
_MISSING = object()


class CacheKeyGenerator:
    """
    Generates consistent cache keys for the application.

    Cache keys follow the pattern: tg:{category}:{identifier}:{params}
    """

    PREFIX = "tg"

    @classmethod
    def make_key(cls, category: str, identifier: str = "", **params) -> str:
        """
        Generate a cache key.

        Args:
            category: The type of cached data (e.g., 'queryset', 'view', 'template')
            identifier: Specific identifier (e.g., model name, view name)
            **params: Additional parameters to include in the key

        Returns:
            A consistent cache key string

        Examples:
            >>> CacheKeyGenerator.make_key('queryset', 'Character', status='App')
            'tg:queryset:Character:status=App'
        """
        parts = [cls.PREFIX, category]

        if identifier:
            parts.append(identifier)

        if params:
            param_str = ":".join(f"{k}={v}" for k, v in sorted(params.items()))
            parts.append(param_str)

        return ":".join(parts)

    @classmethod
    def make_model_key(cls, model_class: type[Model], **params) -> str:
        """Generate a cache key for a model queryset."""
        return cls.make_key("queryset", model_class.__name__, **params)

    @classmethod
    def make_view_key(cls, view_name: str, **params) -> str:
        """Generate a cache key for a view."""
        return cls.make_key("view", view_name, **params)

    @classmethod
    def make_template_key(cls, template_name: str, **params) -> str:
        """Generate a cache key for a template fragment."""
        return cls.make_key("template", template_name, **params)


def cache_function(timeout: int = 300, key_prefix: str = "") -> Callable:
    """
    Decorator to cache the result of any function.

    Works with any function return type. Every positional and keyword argument is part
    of the key, falsy ones (``0``, ``""``, ``None``) included, each rendered with ``str()``.
    A ``None`` result is cached like any other value.

    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
        key_prefix: Optional prefix to add to the cache key

    Returns:
        Decorated function that caches its result

    Example:
        @cache_function(timeout=3600, key_prefix="stats")
        def calculate_character_stats(character_id):
            # Expensive calculation
            return stats
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate cache key based on function name and arguments
            func_name = f"{key_prefix}:{func.__name__}" if key_prefix else func.__name__

            key_parts = [func_name, *(str(arg) for arg in args)]
            key_parts += [f"{k}={v}" for k, v in sorted(kwargs.items())]
            cache_key = CacheKeyGenerator.make_key("function", ":".join(key_parts))

            cached_result = cache.get(cache_key, _MISSING)
            if cached_result is not _MISSING:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)

            return result

        return wrapper

    return decorator


# Cache timeout constants (in seconds)
CACHE_TIMEOUT_SHORT = 60  # 1 minute
CACHE_TIMEOUT_MEDIUM = 300  # 5 minutes
CACHE_TIMEOUT_LONG = 900  # 15 minutes
CACHE_TIMEOUT_VERY_LONG = 3600  # 1 hour
CACHE_TIMEOUT_DAY = 86400  # 24 hours


def get_cached_reference_list(
    model_class: type[Model],
    ordering: str | None = "name",
    filters: dict | None = None,
    timeout: int = CACHE_TIMEOUT_LONG,
) -> list:
    """
    Get a cached list of reference model objects.

    The queryset is evaluated immediately and the resulting list is cached.
    This is useful for forms that iterate over reference data multiple times,
    as it avoids repeated database queries.

    This function is designed for small reference tables (typically <100 records)
    like Attributes, Abilities, Backgrounds, etc. Avoid it for large tables,
    because the whole list is held in the cache.

    Args:
        model_class: The model class to query (e.g., Attribute, Ability)
        ordering: Field name to order by, or None for no ordering. Default is
            "name", which assumes the model has a `name` field. For models
            without a `name` field, explicitly pass the correct field name
            or None.
        filters: Optional dictionary of filters to apply
        timeout: Cache timeout in seconds (default: 15 minutes)

    Returns:
        List of model instances

    Note:
        Cached data will persist for the timeout duration even if the underlying
        database records change. This is appropriate for reference data that
        changes infrequently; nothing clears the entry early.

    Example:
        from core.cache import get_cached_reference_list
        from characters.models.core.attribute import Attribute

        # For models with a "name" field (uses default ordering):
        all_abilities = get_cached_reference_list(Ability)

        # For models without a "name" field, specify ordering:
        all_attributes = get_cached_reference_list(Attribute, ordering=None)

        # Then filter in memory:
        attrs = [a for a in all_attributes if getattr(instance, a.property_name, 0) < 5]
    """
    filters = filters or {}
    cache_key = CacheKeyGenerator.make_key(
        "reference_list", model_class.__name__, ordering=ordering or "none", **filters
    )

    # Try to get from cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    # Query database, evaluate to list, and cache result
    queryset = model_class.objects.filter(**filters)
    if ordering:
        queryset = queryset.order_by(ordering)
    result = list(queryset)
    cache.set(cache_key, result, timeout)

    return result


ANONYMOUS_PAGE_PREFIX = CacheKeyGenerator.make_key("anonymous_page")


def shares_anonymous_page(request) -> bool:
    """Whether ``request`` may get the page every anonymous visitor shares: a GET
    from a visitor with no session and no pending messages (so nothing per-visitor
    can be on the page). A ``csrftoken`` cookie alone doesn't count."""
    return (
        request.method in ("GET", "HEAD")
        and settings.SESSION_COOKIE_NAME not in request.COOKIES
        and CookieStorage.cookie_name not in request.COOKIES
        and not request.user.is_authenticated
    )


def anonymous_page_key(request) -> str:
    path = hashlib.sha256(request.build_absolute_uri().encode()).hexdigest()
    htmx = "htmx" if request.headers.get("HX-Request") else "page"
    return f"{ANONYMOUS_PAGE_PREFIX}:{htmx}:{path}"


def cache_page_per_visitor(timeout: int) -> list[Callable]:
    """Page caching that never serves one visitor's page to another, for
    ``method_decorator``: ``@method_decorator(cache_page_per_visitor(60 * 15),
    name="dispatch")``.

    Pages render per-user markup (nav username, Edit and staff links, messages).
    SessionMiddleware only adds ``Vary: Cookie`` after the view returns, too late
    for ``cache_page``'s key, so a plain ``cache_page`` serves the first visitor's
    page to everyone.

    - A request with a query string is never cached: these views read none, and
      caching each variant would let anyone fill the cache with ``?x=1``, ``?x=2``...
    - Anonymous visitors (see ``shares_anonymous_page``) share one copy per URL
      (GET and HEAD alike). A page is stored only if it holds nothing per-visitor:
      it rendered no CSRF token, set no cookie and is a 200.
    - Everyone else gets ``cache_page`` keyed on their cookies (``vary_on_cookie``).
    """
    per_visitor = cache_page(timeout)

    def decorator(view: Callable) -> Callable:
        cached_per_visitor = per_visitor(vary_on_cookie(view))

        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.META.get("QUERY_STRING"):
                return view(request, *args, **kwargs)
            if not shares_anonymous_page(request):
                return cached_per_visitor(request, *args, **kwargs)
            key = anonymous_page_key(request)
            response = cache.get(key)
            if response is not None:
                return response
            response = view(request, *args, **kwargs)
            if hasattr(response, "render") and not response.is_rendered:
                response.render()
            if (
                response.status_code == 200
                and not response.streaming
                and not response.cookies
                and not request.META.get("CSRF_COOKIE_NEEDS_UPDATE")
                and "private" not in response.get("Cache-Control", "")
            ):
                patch_vary_headers(response, ("Cookie", "HX-Request"))
                cache.set(key, response, timeout)
            return response

        return wrapper

    return [decorator]
