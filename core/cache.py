"""
Cache utilities for the Tellurian Games application.

This module provides utilities for caching expensive operations, particularly
database queries and view rendering. It includes:
- Cache key generation utilities
- A function-result caching decorator
- Cache invalidation helpers
- A cached reference-list helper
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from django.core.cache import cache
from django.db.models import Model


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


class CacheInvalidator:
    """
    Manages cache invalidation for models.

    When a model instance is saved or deleted, this class can invalidate
    related cache entries to ensure data consistency.
    """

    @staticmethod
    def invalidate_model_cache(model_class: type[Model]) -> None:
        """
        Invalidate all cached data for a specific model.

        This invalidates both queryset caches and reference_list caches
        to ensure data consistency when models are updated.

        Args:
            model_class: The model class whose cache should be invalidated
        """
        # Invalidate both queryset and reference_list caches
        for category in ["queryset", "reference_list"]:
            pattern = f"{CacheKeyGenerator.PREFIX}:{category}:{model_class.__name__}:*"
            try:
                cache.delete_pattern(pattern)
            except AttributeError:
                # Fallback for cache backends that don't support delete_pattern
                # In development with LocMemCache, we can't use patterns
                # so we'll just clear the entire cache for that model's base key
                base_key = CacheKeyGenerator.make_key(category, model_class.__name__)
                cache.delete(base_key)

    @staticmethod
    def invalidate_related_caches(model_instance: Model) -> None:
        """
        Invalidate caches related to a specific model instance.

        This is called when a model is saved or deleted.
        Override in subclasses to invalidate additional related caches.

        Args:
            model_instance: The model instance that was saved/deleted
        """
        CacheInvalidator.invalidate_model_cache(model_instance.__class__)

        # Also invalidate any parent model caches if using polymorphic models
        if hasattr(model_instance, "get_real_instance_class"):
            # This is a polymorphic model, invalidate the base class cache too
            base_class = model_instance.__class__.__bases__[0]
            if base_class != Model:
                CacheInvalidator.invalidate_model_cache(base_class)


def cache_function(timeout: int = 300, key_prefix: str = "") -> Callable:
    """
    Decorator to cache the result of any function.

    Works with any function return type.

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

            # Convert args and kwargs to a hashable string
            args_str = ":".join(str(arg) for arg in args if arg)
            kwargs_str = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))

            key_parts = [part for part in [func_name, args_str, kwargs_str] if part]
            cache_key = CacheKeyGenerator.make_key("function", ":".join(key_parts))

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
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
        changes infrequently. CacheInvalidator.invalidate_model_cache() will
        clear both queryset and reference_list caches for a model.

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
    # "reference_list" keys are cleared by CacheInvalidator.invalidate_model_cache()
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
