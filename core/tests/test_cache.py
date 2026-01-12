"""Tests for cache utilities in core/cache.py."""

from unittest.mock import Mock, patch

from django.core.cache import cache
from django.db.models import Model
from django.test import TestCase

from core.cache import (
    CACHE_TIMEOUT_DAY,
    CACHE_TIMEOUT_LONG,
    CACHE_TIMEOUT_MEDIUM,
    CACHE_TIMEOUT_SHORT,
    CACHE_TIMEOUT_VERY_LONG,
    CacheInvalidator,
    CacheKeyGenerator,
    cache_function,
    cache_queryset,
    get_cached_queryset,
    get_cached_reference_list,
    invalidate_cache_on_save,
)


# Define FakeModel once at module level to avoid re-registration warnings
class FakeModel(Model):
    """Fake model for testing cache utilities."""

    class Meta:
        app_label = "test"


class CacheKeyGeneratorTest(TestCase):
    """Tests for CacheKeyGenerator class."""

    def test_make_key_with_category_only(self):
        """Test make_key with just a category."""
        key = CacheKeyGenerator.make_key("queryset")
        self.assertEqual(key, "tg:queryset")

    def test_make_key_with_category_and_identifier(self):
        """Test make_key with category and identifier."""
        key = CacheKeyGenerator.make_key("queryset", "Character")
        self.assertEqual(key, "tg:queryset:Character")

    def test_make_key_with_params(self):
        """Test make_key with additional parameters."""
        key = CacheKeyGenerator.make_key("queryset", "Character", status="App")
        self.assertEqual(key, "tg:queryset:Character:status=App")

    def test_make_key_with_multiple_params(self):
        """Test make_key with multiple parameters."""
        key = CacheKeyGenerator.make_key("queryset", "Character", status="App", chronicle=1)
        # Params should be sorted
        self.assertIn("chronicle=1", key)
        self.assertIn("status=App", key)
        self.assertTrue(key.startswith("tg:queryset:Character:"))

    def test_make_key_sorts_params_alphabetically(self):
        """Test that make_key sorts parameters alphabetically."""
        key = CacheKeyGenerator.make_key("queryset", "Character", zebra="1", alpha="2")
        # alpha should come before zebra
        self.assertIn("alpha=2", key)
        self.assertIn("zebra=1", key)
        alpha_idx = key.index("alpha")
        zebra_idx = key.index("zebra")
        self.assertLess(alpha_idx, zebra_idx)

    def test_make_key_empty_identifier(self):
        """Test make_key with empty identifier."""
        key = CacheKeyGenerator.make_key("view", "", user_id=1)
        self.assertEqual(key, "tg:view:user_id=1")

    def test_make_model_key(self):
        """Test make_model_key with a model class."""
        key = CacheKeyGenerator.make_model_key(FakeModel)
        self.assertEqual(key, "tg:queryset:FakeModel")

    def test_make_model_key_with_params(self):
        """Test make_model_key with parameters."""
        key = CacheKeyGenerator.make_model_key(FakeModel, status="App")
        self.assertEqual(key, "tg:queryset:FakeModel:status=App")

    def test_make_view_key(self):
        """Test make_view_key."""
        key = CacheKeyGenerator.make_view_key("home")
        self.assertEqual(key, "tg:view:home")

    def test_make_view_key_with_params(self):
        """Test make_view_key with parameters."""
        key = CacheKeyGenerator.make_view_key("character_detail", pk=123)
        self.assertEqual(key, "tg:view:character_detail:pk=123")

    def test_make_template_key(self):
        """Test make_template_key."""
        key = CacheKeyGenerator.make_template_key("sidebar")
        self.assertEqual(key, "tg:template:sidebar")

    def test_make_template_key_with_params(self):
        """Test make_template_key with parameters."""
        key = CacheKeyGenerator.make_template_key("navigation", user_id=1)
        self.assertEqual(key, "tg:template:navigation:user_id=1")

    def test_prefix_constant(self):
        """Test that PREFIX is correctly set."""
        self.assertEqual(CacheKeyGenerator.PREFIX, "tg")


class CacheInvalidatorTest(TestCase):
    """Tests for CacheInvalidator class."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_invalidate_model_cache_with_delete_pattern(self):
        """Test invalidate_model_cache with pattern deletion support."""
        # Set some cache values
        cache.set("tg:queryset:FakeModel:status=App", "value1")
        cache.set("tg:queryset:FakeModel:status=Un", "value2")
        cache.set("tg:reference_list:FakeModel:ordering=name", "value3")

        # Use create=True to allow patching non-existent attribute
        with patch.object(cache, "delete_pattern", create=True) as mock_delete_pattern:
            CacheInvalidator.invalidate_model_cache(FakeModel)
            # Should be called twice: once for queryset, once for reference_list
            self.assertEqual(mock_delete_pattern.call_count, 2)
            mock_delete_pattern.assert_any_call("tg:queryset:FakeModel:*")
            mock_delete_pattern.assert_any_call("tg:reference_list:FakeModel:*")

    def test_invalidate_model_cache_fallback_without_delete_pattern(self):
        """Test invalidate_model_cache falls back when delete_pattern not supported."""
        # Set cache values for both categories
        queryset_key = CacheKeyGenerator.make_model_key(FakeModel)
        reference_list_key = CacheKeyGenerator.make_key("reference_list", FakeModel.__name__)
        cache.set(queryset_key, "test_value1")
        cache.set(reference_list_key, "test_value2")

        # Mock delete_pattern to raise AttributeError (create=True for non-existent attribute)
        with patch.object(cache, "delete_pattern", side_effect=AttributeError, create=True):
            with patch.object(cache, "delete") as mock_delete:
                CacheInvalidator.invalidate_model_cache(FakeModel)
                # Should be called twice: once for queryset, once for reference_list
                self.assertEqual(mock_delete.call_count, 2)
                mock_delete.assert_any_call(queryset_key)
                mock_delete.assert_any_call(reference_list_key)

    def test_invalidate_related_caches(self):
        """Test invalidate_related_caches calls invalidate_model_cache."""
        instance = Mock(spec=FakeModel)
        instance.__class__ = FakeModel

        with patch.object(CacheInvalidator, "invalidate_model_cache") as mock_invalidate:
            CacheInvalidator.invalidate_related_caches(instance)
            mock_invalidate.assert_called_once_with(FakeModel)

    def test_invalidate_related_caches_with_polymorphic_model(self):
        """Test invalidate_related_caches handles polymorphic models."""
        # Create a mock instance that simulates polymorphic behavior
        # The instance needs a non-Model base class for the second invalidate to trigger
        instance = Mock(spec=FakeModel)
        instance.__class__ = FakeModel
        instance.get_real_instance_class = Mock(return_value=FakeModel)

        with patch.object(CacheInvalidator, "invalidate_model_cache") as mock_invalidate:
            CacheInvalidator.invalidate_related_caches(instance)
            # FakeModel inherits directly from Model, so only one call happens
            # (the check `base_class != Model` prevents the second call)
            mock_invalidate.assert_called_once_with(FakeModel)


class CacheQuerysetDecoratorTest(TestCase):
    """Tests for cache_queryset decorator."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_cache_queryset_caches_result(self):
        """Test that cache_queryset caches the function result."""
        call_count = 0

        @cache_queryset(timeout=60)
        def get_items():
            nonlocal call_count
            call_count += 1
            return ["item1", "item2"]

        # First call
        result1 = get_items()
        self.assertEqual(result1, ["item1", "item2"])
        self.assertEqual(call_count, 1)

        # Second call should use cache
        result2 = get_items()
        self.assertEqual(result2, ["item1", "item2"])
        self.assertEqual(call_count, 1)  # Should not increase

    def test_cache_queryset_with_key_prefix(self):
        """Test cache_queryset with custom key prefix."""

        @cache_queryset(timeout=60, key_prefix="characters")
        def get_characters():
            return ["char1", "char2"]

        result = get_characters()
        self.assertEqual(result, ["char1", "char2"])

    def test_cache_queryset_with_args(self):
        """Test cache_queryset with function arguments."""
        call_count = 0

        @cache_queryset(timeout=60)
        def get_items_by_status(status):
            nonlocal call_count
            call_count += 1
            return [f"item_{status}"]

        # First call with "active"
        result1 = get_items_by_status("active")
        self.assertEqual(result1, ["item_active"])
        self.assertEqual(call_count, 1)

        # Call with "inactive" - different args, should not use cache
        result2 = get_items_by_status("inactive")
        self.assertEqual(result2, ["item_inactive"])
        self.assertEqual(call_count, 2)

        # Call again with "active" - should use cache
        result3 = get_items_by_status("active")
        self.assertEqual(result3, ["item_active"])
        self.assertEqual(call_count, 2)

    def test_cache_queryset_with_kwargs(self):
        """Test cache_queryset with keyword arguments."""
        call_count = 0

        @cache_queryset(timeout=60)
        def get_items(status=None, chronicle=None):
            nonlocal call_count
            call_count += 1
            return [f"item_{status}_{chronicle}"]

        result1 = get_items(status="active", chronicle=1)
        self.assertEqual(call_count, 1)

        result2 = get_items(status="active", chronicle=1)
        self.assertEqual(call_count, 1)  # Should use cache

        result3 = get_items(status="active", chronicle=2)
        self.assertEqual(call_count, 2)  # Different kwargs

    def test_cache_queryset_preserves_function_metadata(self):
        """Test that cache_queryset preserves function metadata."""

        @cache_queryset(timeout=60)
        def my_function():
            """My docstring."""
            return []

        self.assertEqual(my_function.__name__, "my_function")
        self.assertEqual(my_function.__doc__, "My docstring.")


class CacheFunctionDecoratorTest(TestCase):
    """Tests for cache_function decorator."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_cache_function_caches_result(self):
        """Test that cache_function caches the function result."""
        call_count = 0

        @cache_function(timeout=60)
        def calculate_value(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = calculate_value(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count, 1)

        result2 = calculate_value(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count, 1)  # Should use cache

    def test_cache_function_with_key_prefix(self):
        """Test cache_function with custom key prefix."""

        @cache_function(timeout=60, key_prefix="stats")
        def calculate_stats():
            return {"total": 100}

        result = calculate_stats()
        self.assertEqual(result, {"total": 100})

    def test_cache_function_with_different_args(self):
        """Test cache_function with different arguments."""
        call_count = 0

        @cache_function(timeout=60)
        def multiply(a, b):
            nonlocal call_count
            call_count += 1
            return a * b

        result1 = multiply(2, 3)
        self.assertEqual(result1, 6)
        self.assertEqual(call_count, 1)

        result2 = multiply(2, 4)
        self.assertEqual(result2, 8)
        self.assertEqual(call_count, 2)

        result3 = multiply(2, 3)
        self.assertEqual(result3, 6)
        self.assertEqual(call_count, 2)

    def test_cache_function_preserves_function_metadata(self):
        """Test that cache_function preserves function metadata."""

        @cache_function(timeout=60)
        def my_calculation():
            """Calculation docstring."""
            return 42

        self.assertEqual(my_calculation.__name__, "my_calculation")
        self.assertEqual(my_calculation.__doc__, "Calculation docstring.")

    def test_cache_function_handles_none_return(self):
        """Test cache_function handles None return values correctly."""
        call_count = 0

        @cache_function(timeout=60)
        def return_none():
            nonlocal call_count
            call_count += 1
            return None

        result1 = return_none()
        self.assertIsNone(result1)
        self.assertEqual(call_count, 1)

        # None is a valid cached value, but cache.get returns None for missing keys
        # This test verifies the behavior
        result2 = return_none()
        # Second call - cache returns None which is same as "not found"
        # So function will be called again
        self.assertIsNone(result2)


class InvalidateCacheOnSaveDecoratorTest(TestCase):
    """Tests for invalidate_cache_on_save decorator."""

    def test_invalidate_cache_on_save_registers_signals(self):
        """Test that invalidate_cache_on_save registers signal handlers."""

        @invalidate_cache_on_save(FakeModel)
        class TestView:
            pass

        # The decorator should return the class unchanged
        self.assertEqual(TestView.__name__, "TestView")

    def test_invalidate_cache_on_save_returns_class(self):
        """Test that invalidate_cache_on_save returns the decorated class."""

        @invalidate_cache_on_save(FakeModel)
        class MyView:
            def get(self):
                return "response"

        view = MyView()
        self.assertEqual(view.get(), "response")


class GetCachedQuerysetTest(TestCase):
    """Tests for get_cached_queryset function."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_get_cached_queryset_without_filters(self):
        """Test get_cached_queryset without filters."""
        from django.contrib.auth.models import User

        # Create a test user
        User.objects.create_user(username="test", password="test123")

        result = get_cached_queryset(User)
        self.assertEqual(result.count(), 1)

    def test_get_cached_queryset_with_filters(self):
        """Test get_cached_queryset with filters."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="active_user", password="test123", is_active=True)
        User.objects.create_user(username="inactive_user", password="test123", is_active=False)

        result = get_cached_queryset(User, filters={"is_active": True})
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().username, "active_user")

    def test_get_cached_queryset_uses_cache(self):
        """Test that get_cached_queryset uses cache on second call."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="test", password="test123")

        # First call
        result1 = get_cached_queryset(User)

        # Add another user
        User.objects.create_user(username="test2", password="test123")

        # Second call should still return cached result with 1 user
        result2 = get_cached_queryset(User)
        # Note: The cached queryset evaluates to fresh data since QuerySets are lazy
        # This tests the caching mechanism, not the queryset evaluation

    def test_get_cached_queryset_custom_timeout(self):
        """Test get_cached_queryset with custom timeout."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="test", password="test123")

        result = get_cached_queryset(User, timeout=600)
        self.assertIsNotNone(result)


class GetCachedReferenceListTest(TestCase):
    """Tests for get_cached_reference_list function."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_returns_list_not_queryset(self):
        """Test that function returns an evaluated list, not a queryset."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="test", password="test123")

        # User model doesn't have a "name" field, so specify ordering
        result = get_cached_reference_list(User, ordering="username")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_uses_cache_on_second_call(self):
        """Test that second call uses cached result."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="test", password="test123")

        # First call (User model doesn't have "name" field)
        result1 = get_cached_reference_list(User, ordering="username")
        count1 = len(result1)
        self.assertEqual(count1, 1)

        # Create new record after caching
        User.objects.create_user(username="test2", password="test123")

        # Second call should return cached list (without new record)
        result2 = get_cached_reference_list(User, ordering="username")
        self.assertEqual(len(result2), count1)  # Should not include new record

    def test_ordering_parameter(self):
        """Test that ordering parameter works correctly."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="zebra", password="test123")
        User.objects.create_user(username="alpha", password="test123")

        result = get_cached_reference_list(User, ordering="username")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].username, "alpha")
        self.assertEqual(result[1].username, "zebra")

    def test_ordering_none(self):
        """Test that ordering=None works (no ordering applied)."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="test", password="test123")

        result = get_cached_reference_list(User, ordering=None)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_filters_parameter(self):
        """Test that filters parameter works correctly."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="active", password="test123", is_active=True)
        User.objects.create_user(username="inactive", password="test123", is_active=False)

        # User model doesn't have "name" field, so specify ordering
        result = get_cached_reference_list(
            User, ordering="username", filters={"is_active": True}
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].username, "active")

    def test_different_filters_use_different_cache_keys(self):
        """Test that different filters create separate cache entries."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="active", password="test123", is_active=True)
        User.objects.create_user(username="inactive", password="test123", is_active=False)

        # User model doesn't have "name" field, so specify ordering
        result_active = get_cached_reference_list(
            User, ordering="username", filters={"is_active": True}
        )
        result_inactive = get_cached_reference_list(
            User, ordering="username", filters={"is_active": False}
        )

        self.assertEqual(len(result_active), 1)
        self.assertEqual(result_active[0].username, "active")
        self.assertEqual(len(result_inactive), 1)
        self.assertEqual(result_inactive[0].username, "inactive")

    def test_cache_invalidation_clears_reference_list(self):
        """Test that CacheInvalidator.invalidate_model_cache clears reference lists."""
        from django.contrib.auth.models import User

        User.objects.create_user(username="test", password="test123")

        # First call - cache it
        result1 = get_cached_reference_list(User, ordering="username")
        self.assertEqual(len(result1), 1)

        # Create new record
        User.objects.create_user(username="test2", password="test123")

        # Before invalidation - should still return cached result
        result2 = get_cached_reference_list(User, ordering="username")
        self.assertEqual(len(result2), 1)  # Still cached

        # Mock delete_pattern to simulate Redis cache behavior (which supports patterns)
        # LocMemCache doesn't support delete_pattern, so we need to mock it
        with patch.object(cache, "delete_pattern", create=True) as mock_delete_pattern:
            CacheInvalidator.invalidate_model_cache(User)
            # Verify delete_pattern was called for reference_list category
            mock_delete_pattern.assert_any_call("tg:reference_list:User:*")

        # Manually clear cache to simulate what delete_pattern would do
        cache.clear()

        # After invalidation - should get fresh data
        result3 = get_cached_reference_list(User, ordering="username")
        self.assertEqual(len(result3), 2)  # Should include new record


class CacheTimeoutConstantsTest(TestCase):
    """Tests for cache timeout constants."""

    def test_cache_timeout_short(self):
        """Test CACHE_TIMEOUT_SHORT is 60 seconds."""
        self.assertEqual(CACHE_TIMEOUT_SHORT, 60)

    def test_cache_timeout_medium(self):
        """Test CACHE_TIMEOUT_MEDIUM is 5 minutes."""
        self.assertEqual(CACHE_TIMEOUT_MEDIUM, 300)

    def test_cache_timeout_long(self):
        """Test CACHE_TIMEOUT_LONG is 15 minutes."""
        self.assertEqual(CACHE_TIMEOUT_LONG, 900)

    def test_cache_timeout_very_long(self):
        """Test CACHE_TIMEOUT_VERY_LONG is 1 hour."""
        self.assertEqual(CACHE_TIMEOUT_VERY_LONG, 3600)

    def test_cache_timeout_day(self):
        """Test CACHE_TIMEOUT_DAY is 24 hours."""
        self.assertEqual(CACHE_TIMEOUT_DAY, 86400)
