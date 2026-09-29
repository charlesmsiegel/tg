# Caching

Rules for caching a page, a function result or a reference list. The concepts are in
[docs/architecture/caching.md](../../../../docs/architecture/caching.md); the code is
[`core/cache.py`](../../../../core/cache.py). Development uses `LocMemCache`
(`tg/settings/development.py`), production Redis with the `tg` key prefix and
`IGNORE_EXCEPTIONS` (`tg/settings/production.py`), which also stores sessions in the cache.

## Page caching

- **Only `core.cache.cache_page_per_visitor(timeout)`**, applied with
  `@method_decorator(cache_page_per_visitor(60 * 15), name="dispatch")`, or the
  `core.views.CachedDetailView` / `CachedListView` bases (15 minutes). Never import
  Django's `cache_page` in a view. *Why:* pages render per-user markup (nav username,
  staff links, messages) and `SessionMiddleware` adds `Vary: Cookie` too late for
  `cache_page`'s key, so a plain `cache_page` serves the first visitor's page to everyone.
- What `cache_page_per_visitor` does:
  - a request with a query string is never cached (the view runs every time);
  - an anonymous GET/HEAD with no session and no messages cookie
    (`shares_anonymous_page`) gets one shared copy per absolute URL, kept apart for htmx
    requests; the copy is stored only if the response is a 200, not streaming, sets no
    cookie, is not `Cache-Control: private` and **rendered no CSRF token**;
  - everyone else gets `cache_page` keyed on their cookies (`vary_on_cookie`).
- **Cache only pages that are the same for every visitor apart from the nav**: public
  reference detail and list pages, the home page. Never cache pages gated by object
  permissions, forms, chargen, scenes or anything showing `object_perms`.
- **A cached page must not mint a CSRF token unless it holds a form.** `{% csrf_token %}`
  (or a form rendered for anonymous visitors) sets `CSRF_COOKIE_NEEDS_UPDATE` and keeps
  the page out of the shared anonymous copy, so every anonymous hit renders again. The nav
  only renders its token for signed-in users; keep it that way.
  `widgets.templatetags.widget_media.page_media` skips lazy context values for the same
  reason.
- **Do not read query strings in a cached view**: requests with one bypass the cache, so
  filters and tabs on such a page get no benefit, and a view that relied on caching them
  would be open to cache flooding.

## Function and data caching

| Helper | Use |
|--------|-----|
| `core.cache.cache_function(timeout, key_prefix)` | Memoize a pure function of its arguments (`CharacterDetailView.get_character_scenes`) |
| `core.cache.get_cached_reference_list(Model, ordering="name", filters=None)` | A small reference table as a list, for forms that iterate it often (`chained_freebies.py`) |
| `core.cache.CacheKeyGenerator.make_key(category, identifier, **params)` | Keys of the form `tg:<category>:<identifier>:<k=v...>` for hand-written `cache.get/set` |
| `core.cache.CacheInvalidator.invalidate_model_cache(Model)` | Drop `queryset` and `reference_list` keys for a model (pattern delete on Redis only) |
| Timeouts | `CACHE_TIMEOUT_SHORT` (60), `MEDIUM` (300), `LONG` (900), `VERY_LONG` (3600), `DAY` (86400) |

Rules:

- Cache only data that is the same for every user. Apply the viewer's permissions after
  reading from the cache (the character sheet caches a character's scenes, then filters
  them for the request's audience).
- Key on every argument that changes the result. `cache_function` builds its key from
  `str()` of truthy positional arguments and sorted keyword arguments; pass ids, not model
  instances, and avoid falsy positional arguments (they are left out of the key).
- A cached `None` is treated as a miss.
- Reference lists are stale for up to their timeout after an edit; acceptable for game
  data loaded by `populate_db`, not for player data.
- Do not use template fragment caching (`{% cache %}`) for anything that depends on the
  user.

## Tests

- `core/tests/test_cache_per_visitor.py`: a cached page never shows one user's markup to
  another, anonymous visitors share one copy, CSRF tokens, cookies and sessions prevent
  sharing, query strings are never cached, htmx fragments are cached apart. Add a case
  when you cache a new page type (`assert_not_shared(url)`).
- Use `@override_settings(CACHES={"default": {"BACKEND":
  "django.core.cache.backends.locmem.LocMemCache"}})` and `cache.clear()` in `setUp`.

## Checklist

- [ ] `cache_page_per_visitor` or a cached base class; no `cache_page` import.
- [ ] Page identical for all visitors apart from the nav; no permission-dependent content.
- [ ] No CSRF token on the cached page unless it has a form; no query-string reads.
- [ ] Cached data is audience-independent; keys cover every argument.
- [ ] A test proves the page is not shared between users.

## See also

- [docs/architecture/caching.md](../../../../docs/architecture/caching.md)
- [`core/cache.py`](../../../../core/cache.py), [`core/views/generic.py`](../../../../core/views/generic.py)
- [views.md](views.md), [deployment.md](deployment.md)
