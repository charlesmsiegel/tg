"""Tests for cache utilities in core/cache.py."""

from django.core.cache import cache
from django.db.models import Model
from django.test import TestCase

from core.cache import (
    CACHE_TIMEOUT_DAY,
    CACHE_TIMEOUT_LONG,
    CACHE_TIMEOUT_MEDIUM,
    CACHE_TIMEOUT_SHORT,
    CACHE_TIMEOUT_VERY_LONG,
    CacheKeyGenerator,
    cache_function,
    get_cached_reference_list,
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

    def test_cache_function_caches_none_return(self):
        """A None result is cached, so the function is not called again."""
        call_count = 0

        @cache_function(timeout=60)
        def return_none():
            nonlocal call_count
            call_count += 1
            return None

        self.assertIsNone(return_none())
        self.assertIsNone(return_none())
        self.assertEqual(call_count, 1)

    def test_cache_function_caches_falsy_return(self):
        """Falsy results such as [] are cached too."""
        call_count = 0

        @cache_function(timeout=60)
        def return_empty():
            nonlocal call_count
            call_count += 1
            return []

        self.assertEqual(return_empty(), [])
        self.assertEqual(return_empty(), [])
        self.assertEqual(call_count, 1)

    def test_cache_function_keys_include_falsy_args(self):
        """Falsy arguments are part of the key, so f(0) and f() do not share an entry."""

        @cache_function(timeout=60)
        def echo(*args, **kwargs):
            return args, kwargs

        self.assertEqual(echo(), ((), {}))
        self.assertEqual(echo(0), ((0,), {}))
        self.assertEqual(echo(""), (("",), {}))
        self.assertEqual(echo(1, 0), ((1, 0), {}))
        self.assertEqual(echo(1), ((1,), {}))
        self.assertEqual(echo(flag=False), ((), {"flag": False}))


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
        result = get_cached_reference_list(User, ordering="username", filters={"is_active": True})
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
