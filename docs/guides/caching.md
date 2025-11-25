# Caching Guide

This guide explains the caching implementation in the Tellurian Games application and how to use it effectively.

## Overview

The application uses Django's caching framework with two different backends depending on the environment:

- **Development**: Local memory cache (LocMemCache) - No external dependencies required
- **Production**: Redis cache - Provides distributed caching across multiple servers

## Configuration

### Environment Settings

Caching is configured automatically based on the `DJANGO_ENVIRONMENT` variable:

```bash
# Development (default) - uses local memory cache
DJANGO_ENVIRONMENT=development

# Production - uses Redis cache
DJANGO_ENVIRONMENT=production
REDIS_URL=redis://127.0.0.1:6379/1
```

### Redis Setup for Production

1. Install Redis server:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server

   # macOS
   brew install redis
   ```

2. Start Redis:
   ```bash
   # Ubuntu/Debian
   sudo systemctl start redis

   # macOS
   brew services start redis
   ```

3. Configure the Redis URL in your `.env` file:
   ```bash
   REDIS_URL=redis://127.0.0.1:6379/1
   ```

4. For remote Redis with authentication:
   ```bash
   REDIS_URL=redis://username:password@redis.example.com:6379/1
   ```

## Using the Cache System

### 1. View-Level Caching

Cache entire view responses using the `@cache_page` decorator:

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class MeritFlawListView(ListView):
    model = MeritFlaw
    template_name = "characters/core/meritflaw/list.html"
```

**Best for:**
- List views of static reference data (merits/flaws, archetypes, etc.)
- Detail views of rarely-changing data
- Views that don't depend on user-specific data

**Cache duration guidelines:**
- Static reference data: 15-60 minutes
- Home page/news: 5 minutes
- User-specific data: Don't use view caching (use queryset caching instead)

### 2. Queryset Caching

Cache expensive database queries using the `@cache_function` decorator from `core.cache`:

```python
from core.cache import cache_function, CACHE_TIMEOUT_MEDIUM

class CharacterDetailView(DetailView):
    model = Character

    @staticmethod
    @cache_function(timeout=CACHE_TIMEOUT_MEDIUM, key_prefix="character_scenes")
    def get_character_scenes(character_id):
        """Get scenes for a character with proper prefetching."""
        return list(
            Scene.objects.filter(characters__id=character_id)
            .select_related("chronicle", "location", "st")
            .prefetch_related("characters", "participants")
            .order_by("-date_of_scene")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scenes"] = self.get_character_scenes(self.object.id)
        return context
```

**Best for:**
- Complex queries with multiple joins
- Queries with prefetch_related or select_related
- Aggregation queries
- Queries that are expensive but results don't change frequently

### 3. Function-Level Caching

Cache any function's result using the `@cache_function` decorator:

```python
from core.cache import cache_function, CACHE_TIMEOUT_LONG

@cache_function(timeout=CACHE_TIMEOUT_LONG, key_prefix="character_stats")
def calculate_character_stats(character_id):
    """Perform expensive calculations."""
    # Complex calculation logic here
    return calculated_stats
```

### 4. Manual Cache Access

For fine-grained control, use Django's cache API directly:

```python
from django.core.cache import cache
from core.cache import CacheKeyGenerator

# Store data
key = CacheKeyGenerator.make_model_key(Character, status='App')
cache.set(key, character_data, timeout=300)

# Retrieve data
cached_data = cache.get(key)
if cached_data is None:
    # Cache miss - fetch from database
    cached_data = Character.objects.filter(status='App')
    cache.set(key, cached_data, timeout=300)
```

## Cache Timeout Constants

Use predefined timeout constants from `core.cache`:

```python
from core.cache import (
    CACHE_TIMEOUT_SHORT,      # 60 seconds
    CACHE_TIMEOUT_MEDIUM,     # 300 seconds (5 minutes)
    CACHE_TIMEOUT_LONG,       # 900 seconds (15 minutes)
    CACHE_TIMEOUT_VERY_LONG,  # 3600 seconds (1 hour)
    CACHE_TIMEOUT_DAY,        # 86400 seconds (24 hours)
)
```

## Cache Invalidation

### Automatic Invalidation

The `CacheInvalidator` class automatically invalidates caches when models are saved or deleted.

To use automatic invalidation on a view:

```python
from core.cache import invalidate_cache_on_save
from characters.models.core import Character

@invalidate_cache_on_save(Character)
class CharacterListView(ListView):
    model = Character
    # When a Character is saved/deleted, the cache for this view is invalidated
```

### Manual Invalidation

Invalidate specific caches manually:

```python
from django.core.cache import cache
from core.cache import CacheInvalidator, CacheKeyGenerator

# Invalidate all caches for a model
CacheInvalidator.invalidate_model_cache(Character)

# Invalidate a specific cache key
key = CacheKeyGenerator.make_model_key(Character, status='App')
cache.delete(key)

# Clear all caches (use sparingly!)
cache.clear()
```

### When to Invalidate

- After creating/updating/deleting model instances
- After bulk operations
- When reference data changes
- After migrations that modify data

## Cache Keys

The `CacheKeyGenerator` class creates consistent cache keys:

```python
from core.cache import CacheKeyGenerator

# Model queryset key
key = CacheKeyGenerator.make_model_key(Character, status='App')
# Result: "tg:queryset:Character:status=App"

# View key
key = CacheKeyGenerator.make_view_key("character_list", gameline="vtm")
# Result: "tg:view:character_list:gameline=vtm"

# Template fragment key
key = CacheKeyGenerator.make_template_key("character_card", character_id=123)
# Result: "tg:template:character_card:character_id=123"
```

## Template Fragment Caching

Cache portions of templates using the `{% cache %}` template tag:

```django
{% load cache %}

{% cache 900 character_details character.id %}
    <!-- This section is cached for 15 minutes per character -->
    <div class="character-details">
        {{ character.name }}
        {{ character.description }}
    </div>
{% endcache %}
```

## Performance Tips

1. **Don't over-cache**: Caching adds complexity. Only cache when performance testing shows it's needed.

2. **Use appropriate timeouts**:
   - Static data: Longer timeouts (15-60 minutes)
   - Dynamic data: Shorter timeouts (1-5 minutes)
   - User-specific data: Very short or no caching

3. **Cache at the right level**:
   - Cache database queries, not view responses for user-specific pages
   - Cache view responses for public pages with identical content for all users

4. **Monitor cache hit rates**: In production, monitor Redis to ensure caches are being hit.

5. **Combine with query optimization**:
   ```python
   # Good: Cache an already-optimized query
   @cache_function(timeout=300)
   def get_characters():
       return Character.objects.select_related('owner').prefetch_related('merits_and_flaws')

   # Bad: Caching doesn't fix N+1 queries
   @cache_function(timeout=300)
   def get_characters():
       return Character.objects.all()  # Still causes N+1 queries when accessing relationships
   ```

## Testing Cache Behavior

### In Development

Development uses local memory cache, so caches are cleared when the server restarts.

```bash
# Start server
python manage.py runserver

# Cache persists during this session
# Stop server (Ctrl+C) - cache is cleared
```

### In Production

Production uses Redis, so caches persist across server restarts.

```bash
# Clear all caches
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Or clear Redis directly
redis-cli FLUSHDB
```

### Testing Cache Invalidation

```python
# In your tests
from django.core.cache import cache
from django.test import TestCase

class CacheTestCase(TestCase):
    def setUp(self):
        cache.clear()  # Start with empty cache

    def test_cache_invalidation(self):
        # Create object
        character = Character.objects.create(name="Test")

        # Cache should be invalidated
        key = CacheKeyGenerator.make_model_key(Character)
        self.assertIsNone(cache.get(key))
```

## Troubleshooting

### Cache not working in production

1. Check Redis is running:
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

2. Check Redis connection in Django shell:
   ```python
   python manage.py shell
   >>> from django.core.cache import cache
   >>> cache.set('test', 'value')
   >>> cache.get('test')
   'value'
   ```

3. Check `REDIS_URL` environment variable:
   ```bash
   echo $REDIS_URL
   ```

### Stale cache data

If you're seeing outdated data:

1. Clear the cache:
   ```bash
   redis-cli FLUSHDB
   ```

2. Check cache timeout values aren't too long

3. Verify cache invalidation is working correctly

### Memory issues with LocMemCache

In development, if memory grows too large:

1. The cache is limited to 1000 entries (see `tg/settings/development.py`)
2. Restart the development server to clear the cache
3. Consider using Redis even in development if caching large datasets

## Best Practices

1. **Always use cache constants**: Use `CACHE_TIMEOUT_*` instead of hardcoded values
2. **Document cached functions**: Explain what's being cached and why
3. **Use descriptive key prefixes**: Makes debugging easier
4. **Test cache invalidation**: Ensure caches are cleared when data changes
5. **Monitor in production**: Track cache hit rates and performance impact
6. **Don't cache user-specific data in view caching**: Use queryset caching instead
7. **Combine with query optimization**: Caching doesn't replace proper query optimization

## References

- [Django Caching Documentation](https://docs.djangoproject.com/en/5.0/topics/cache/)
- [Redis Documentation](https://redis.io/documentation)
- [django-redis Documentation](https://github.com/jazzband/django-redis)
