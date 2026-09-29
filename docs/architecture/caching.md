# Caching

This page describes every cache the project uses: full-page caching of reference pages, the
helpers in `core.cache`, the per-user and per-request caches elsewhere, how and when cached data
is invalidated, the cache backends per environment, and the two places where page output and
caching interact (the Known-by section and the CSRF token). Read it before you cache a view or a
query, or change a template that cached pages render.

## What is cached

| Cache | Where | Key | Lifetime | Invalidation |
|-------|-------|-----|----------|--------------|
| Reference pages | `core.cache.cache_page_per_visitor` on reference detail and list views and the home page | URL, plus the visitor's cookies unless the visitor shares the anonymous copy | 15 minutes (home page: 5) | None; entries expire |
| Chargen reference lists | `core.cache.get_cached_reference_list` in [`characters/forms/core/chained_freebies.py`](../../characters/forms/core/chained_freebies.py) | `tg:reference_list:<Model>:ordering=…` | 15 minutes | `CacheInvalidator.invalidate_model_cache`, which nothing calls automatically |
| A character's scenes | `core.cache.cache_function` on `get_character_scenes` in [`characters/views/core/character.py`](../../characters/views/core/character.py) | `tg:function:character_scenes:get_character_scenes:<id>` | 5 minutes | None |
| Notification count | `accounts.context_processors.notification_count` | `notification_count_<user id>` | 60 seconds | None |
| Chargen partial throttle | `characters.views.core.chargen_mixins.ChargenStepMixin.partial_throttled` | `chargen-partial:<user>:<character>:<minute>` | 120 seconds | Not needed: a per-minute counter; above `CHARGEN_PARTIAL_LIMIT` (read with `getattr`, default 60, not set in the settings files) partial requests get `204` |
| Sessions (production only) | `SESSION_ENGINE = "django.contrib.sessions.backends.cache"` | Django's | Session age | Logout |

Permission roles and resolved polymorphic objects are cached on the **request object**, not in
the cache backend; see [Authorization](authorization.md#request-caching).

## Full-page caching: `cache_page_per_visitor`

[`core/cache.py`](../../core/cache.py) defines `cache_page_per_visitor(timeout)`. It returns a
**list** containing one decorator, which is the form `method_decorator` accepts:

```python
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from core.cache import cache_page_per_visitor


@method_decorator(cache_page_per_visitor(60 * 15), name="dispatch")
class VampireSectDetailView(DetailView):
    ...
```

### Why not Django's `cache_page`

Every page renders per-user markup: the navigation shows the username, and pages include Edit
and staff links and flash messages. Django's `cache_page` builds its cache key from the URL and
the response's `Vary` headers. `SessionMiddleware` adds `Vary: Cookie` only after the view
returns, which is too late for `cache_page`'s key, so a plain `cache_page` stores the first
visitor's page and serves it to everyone. [`core/tests/test_cache_per_visitor.py`](../../core/tests/test_cache_per_visitor.py)
checks that a staff user's name never appears in a page served to an anonymous visitor
afterwards. Do not use `django.views.decorators.cache.cache_page` directly.

### What the decorator does

For each request, in this order:

1. **A query string disables caching.** If `QUERY_STRING` is non-empty the view runs uncached.
   The cached views read no query parameters, and caching each variant would let anyone fill
   the cache with `?x=1`, `?x=2`, and so on.
2. **Anonymous visitors share one copy per URL.** `shares_anonymous_page(request)` is true for a
   `GET` or `HEAD` from a user who is not signed in and sends neither a session cookie
   (`SESSION_COOKIE_NAME`) nor a messages cookie. A `csrftoken` cookie alone does not count. The
   key is `anonymous_page_key(request)`: `tg:anonymous_page`, then `htmx` or `page` (from the
   `HX-Request` header, so fragments and full pages are stored apart), then a SHA-256 of the
   absolute URL. `GET` and `HEAD` share the entry.
3. **A shared copy is stored only if it holds nothing per-visitor.** After rendering, the
   response is cached only if it is a `200`, not streaming, sets no cookies, did not use the
   CSRF token (`request.META["CSRF_COOKIE_NEEDS_UPDATE"]` unset) and has no `private` in
   `Cache-Control`. The stored response gets `Vary: Cookie, HX-Request`. Otherwise the fresh
   response is returned and nothing is stored.
4. **Everyone else gets a per-visitor copy.** Signed-in users and anonymous visitors with a
   session or messages go through `cache_page(timeout)` wrapped around `vary_on_cookie(view)`,
   so the key includes their `Cookie` header. Django's cache middleware does not store responses
   marked `private`, `no-cache` or `no-store`, or ones that set a cookie while varying on
   `Cookie`.

### `CachedDetailView` and `CachedListView`

[`core/views/generic.py`](../../core/views/generic.py) defines `CachedDetailView` and
`CachedListView`: `DetailView` and `ListView` with `cache_page_per_visitor(CACHE_TIMEOUT_LONG)`
(15 minutes) applied to `dispatch`. Reference views subclass them, for example
`characters.views.vampire.discipline.DisciplineDetailView`,
`characters.views.vampire.clan.VampireClanListView`, and the sphere, resonance, gift and tribe
views.

Other reference views apply the decorator directly (15 minutes): archetypes, derangements and
merits and flaws in `characters/views/core/`, vampire paths, sects and titles, wraith arcanoi,
factions, guilds and shadow archetypes, demon apocalyptic form traits, and
`core.views.book`. `core.views.home.HomeListView` uses it with a 5-minute timeout.

Only use these on pages whose content is the same for every viewer apart from the page chrome,
and whose route policy is `PUBLIC_READ` or `PUBLIC_INDEX`.

## Data helpers

### `get_cached_reference_list`

`get_cached_reference_list(model_class, ordering="name", filters=None, timeout=CACHE_TIMEOUT_LONG)`
evaluates `model_class.objects.filter(**filters)`, ordered by `ordering` (pass `None` for no
ordering, for models without a `name` field), and caches the resulting **list** under
`tg:reference_list:<ModelName>:ordering=<ordering or "none">[:<filter>=<value>…]`. Use it for
small reference tables that a form iterates over several times. The chained freebie forms load
`Attribute` and `Ability` this way and filter the list in memory.

### `cache_function`

`cache_function(timeout=300, key_prefix="")` caches a function's return value under
`tg:function:[<key_prefix>:]<function name>[:<args>][:<kwargs>]`, built from `str()` of each
argument. Keep in mind:

- Falsy positional arguments (`0`, `""`, `None`) are left out of the key.
- A `None` result is never served from cache, because `None` is how a miss is detected.
- Cache only data that is safe to share between users. `CharacterDetailView.get_character_scenes`
  caches the list of scenes a character appears in, then filters it for the current viewer with
  `game.security.filter_scenes` on every request, so a cached list never widens what a viewer
  can see. New scenes can take up to 5 minutes to appear.

### Keys and timeouts

`CacheKeyGenerator.make_key(category, identifier="", **params)` builds keys of the form
`tg:<category>:<identifier>:<k>=<v>:…` with parameters sorted; `make_model_key`,
`make_view_key` and `make_template_key` fix the category. Timeout constants:
`CACHE_TIMEOUT_SHORT` (60 s), `CACHE_TIMEOUT_MEDIUM` (300 s), `CACHE_TIMEOUT_LONG` (900 s),
`CACHE_TIMEOUT_VERY_LONG` (3600 s) and `CACHE_TIMEOUT_DAY` (86400 s).

## Invalidation

`CacheInvalidator` in [`core/cache.py`](../../core/cache.py) provides:

- `invalidate_model_cache(model_class)`: deletes keys matching
  `tg:queryset:<ModelName>:*` and `tg:reference_list:<ModelName>:*` with the backend's
  `delete_pattern` (available on `django_redis`). On a backend without `delete_pattern`, such as
  `LocMemCache`, it deletes only the exact keys `tg:queryset:<ModelName>` and
  `tg:reference_list:<ModelName>`, which `get_cached_reference_list` never writes, so in
  development cached reference lists stay until they expire.
- `invalidate_related_caches(instance)`: `invalidate_model_cache` for the instance's class and,
  for polymorphic instances, its immediate parent class.

No signal handler or service calls either method. The project's signal handlers
([`accounts/signals.py`](../../accounts/signals.py), [`game/signals.py`](../../game/signals.py))
create profiles and journals and do not touch the cache. All cached data therefore lives until
its timeout: an edit to a reference page shows up within 15 minutes, a chargen reference list
within 15 minutes, a new scene on a character sheet within 5 minutes, and a notification count
within 60 seconds.

## Backends per environment

| Environment | `CACHES["default"]` |
|-------------|---------------------|
| Development ([`tg/settings/development.py`](../../tg/settings/development.py)) | `LocMemCache`, `LOCATION "unique-snowflake"`, `TIMEOUT` 300, `MAX_ENTRIES` 1000. Per process: each worker has its own cache. |
| Production ([`tg/settings/production.py`](../../tg/settings/production.py)) | `django_redis.cache.RedisCache` at `REDIS_URL` (default `redis://127.0.0.1:6379/1`), `KEY_PREFIX "tg"`, `TIMEOUT` 300, zlib compression, a pool of up to 50 connections, 5-second socket timeouts and `IGNORE_EXCEPTIONS: True`. |
| Tests | The development settings (`LocMemCache`). The per-visitor tests override `CACHES` with a plain `LocMemCache`, and the cache tests call `cache.clear()` in `setUp`. |

Production consequences:

- `IGNORE_EXCEPTIONS` makes cache errors behave as misses, so the site keeps working if Redis is
  down. Sessions use the same cache (`SESSION_ENGINE` is the cache backend), so while Redis is
  unavailable sessions are not persisted and users are signed out.
- Clearing the Redis database signs everyone out.
- The production channel layer reads the same `REDIS_URL` (default database `0` there). When
  `REDIS_URL` is set, cache, sessions and channel layer share one Redis database. See
  [Scenes and real-time chat](scenes-and-realtime.md).

## The Known-by section

Several reference detail pages (disciplines, gifts, spheres, merits and flaws, arcanoi, lores,
rites, rotes and others) list the characters that hold the trait. The list depends on the
viewer: it shows only characters whose full sheet the viewer may read, and nothing for anonymous
visitors. It comes from `known_by()` in
[`characters/views/core/known_by.py`](../../characters/views/core/known_by.py) through
`KnownByMixin`, and some of those views are cached (`DisciplineDetailView`,
`SphereDetailView` and `GiftDetailView` are `CachedDetailView`s; the merit-and-flaw and arcanos
detail views use `cache_page_per_visitor`).

`KnownByMixin.render_to_response` makes this safe:

- It always adds `Vary: Cookie`.
- For a signed-in viewer it adds `Cache-Control: private`. `cache_page_per_visitor` never stores
  a private response as the shared anonymous copy, and Django's cache middleware never stores it
  in the per-visitor cache either. Signed-in viewers of these pages are therefore always served
  a fresh render.
- Anonymous visitors, who see no list, still share one cached copy.

Follow the same pattern for any other per-user section on a cached page: mark the response
`private` for viewers whose content differs.

## `page_media` and the CSRF token

[`core/templates/core/tl_base.html`](../../core/templates/core/tl_base.html) calls the
`{% page_media %}` tag ([`widgets/templatetags/widget_media.py`](../../widgets/templatetags/widget_media.py))
on every page to collect the scripts and styles of the forms and formsets in the context. It
walks the context values and skips any `LazyObject` **before** testing its type. Django's
`csrf_token` context value is lazy; an `isinstance` check on it would evaluate it, which calls
`get_token()`, sets `CSRF_COOKIE_NEEDS_UPDATE` and makes the response set a CSRF cookie. Every
page would then look per-visitor to `cache_page_per_visitor`, no anonymous page could be shared,
and every anonymous visitor would receive a CSRF cookie.

The same rule applies to any template code on a cached page: do not touch `csrf_token` (or
render `{% csrf_token %}`) unless the page has a form. A page that does render the token is
still correct; it is simply not shared between anonymous visitors.

## Rules for adding caching

- Cache full pages only with `cache_page_per_visitor` (or `CachedDetailView` /
  `CachedListView`), and only for public reference or index pages. Never cache a view whose
  route policy is an `OBJECT_*`, `GAME`, `ACCOUNT` or `LOGIN` policy.
- Do not read query parameters in a cached view; requests with a query string bypass the cache
  anyway.
- Mark per-viewer fragments of a cached page `Cache-Control: private`, as `KnownByMixin` does.
- Cache data, not permission decisions. When a cached result feeds a page, apply the viewer's
  permission filter after reading it from the cache, as `get_character_scenes` does.
- Build keys with `CacheKeyGenerator` so they follow the `tg:<category>:…` scheme that
  `CacheInvalidator` understands.
- Choose a timeout you can live with as the staleness bound, because nothing invalidates cached
  data on save.
- Add a test in the style of `core/tests/test_cache_per_visitor.py` that renders the page as one
  user and checks another user does not receive their content.

## See also

- [Architecture overview](overview.md)
- [Authorization](authorization.md)
- [Front end](frontend.md)
- [Settings reference](../reference/settings.md)
- [`core/README.md`](../../core/README.md)
- [`core/cache.py`](../../core/cache.py)
