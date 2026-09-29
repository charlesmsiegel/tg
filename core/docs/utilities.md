# Core utilities

This page covers the smaller modules in `core` that other apps import: caching, htmx and
JSON helpers, linked permanent/temporary stats, forms and widgets, validators, the
context processor, admin registrations and the general helpers in `core/utils.py`. It is
for developers who need one of these building blocks. XP helpers are in
[services](services.md#xp-helpers).

## Caching

[`core/cache.py`](../cache.py). The cache backend is `LocMemCache` in development and
Redis (`django_redis`) in production; see
[caching](../../docs/architecture/caching.md) for the project-wide picture.

### Whole-page caching: `cache_page_per_visitor(timeout)`

Use this instead of Django's `cache_page` on any page view. Pages contain per-user
markup (the nav's username, Edit and staff links, flash messages), and `cache_page`
computes its key before `SessionMiddleware` adds `Vary: Cookie`, so a plain `cache_page`
would serve the first visitor's page to everyone.

```python
from django.utils.decorators import method_decorator
from core.cache import CACHE_TIMEOUT_LONG, cache_page_per_visitor

@method_decorator(cache_page_per_visitor(CACHE_TIMEOUT_LONG), name="dispatch")
class ClanListView(ListView):
    ...
```

It returns a list of decorators for `method_decorator`. Behaviour:

- A request with a query string is never cached (anyone could fill the cache with
  `?x=1`, `?x=2`...).
- An anonymous `GET` or `HEAD` with no session cookie and no messages cookie
  (`shares_anonymous_page()`) shares one cached copy per absolute URL and per
  htmx/full-page variant (`anonymous_page_key()`). A response is stored only if it is a
  non-streaming 200 that set no cookies, did not need a CSRF cookie and is not
  `Cache-Control: private`; it gets `Vary: Cookie, HX-Request`.
- Everyone else gets `cache_page(timeout)` keyed on their cookies (`vary_on_cookie`).

The route policy still runs first (it is middleware), so caching never bypasses access
control. `CachedDetailView` and `CachedListView` apply it for you (see
[views](views.md#cacheddetailview-and-cachedlistview)).

### Data caching

| Helper | Use |
|--------|-----|
| `CacheKeyGenerator.make_key(category, identifier="", **params)` | Builds `tg:<category>:<identifier>:<k=v...>` (params sorted). `make_model_key`, `make_view_key`, `make_template_key` fix the category |
| `cache_function(timeout=300, key_prefix="")` | Decorator that caches a function's return value under a key built from its name and `str()` of its arguments. Falsy positional arguments are left out of the key, and a `None` result is never cached |
| `get_cached_reference_list(model_class, ordering="name", filters=None, timeout=CACHE_TIMEOUT_LONG)` | Evaluates a small reference table once and caches the list. Pass `ordering=None` for models without `name` |
| `CacheInvalidator.invalidate_model_cache(model_class)` | Deletes `queryset` and `reference_list` keys for the model with `cache.delete_pattern` (Redis); on backends without it, deletes only the base key |
| `CacheInvalidator.invalidate_related_caches(instance)` | The above for the instance's class and, for polymorphic models, its first base class |

Timeout constants: `CACHE_TIMEOUT_SHORT` (60 s), `CACHE_TIMEOUT_MEDIUM` (300 s),
`CACHE_TIMEOUT_LONG` (900 s), `CACHE_TIMEOUT_VERY_LONG` (3600 s), `CACHE_TIMEOUT_DAY`
(86400 s).

Nothing invalidates these caches automatically on save; reference data is expected to
change rarely and the cached copy lives until its timeout unless you call
`CacheInvalidator`.

## htmx helpers

[`core/htmx.py`](../htmx.py) implements the small part of the htmx request/response
contract the project uses, without the `django-htmx` package.

| Function | Meaning |
|----------|---------|
| `is_htmx(request)` | `HX-Request: true` |
| `is_fragment_request(request)` | An htmx request that expects a partial: not a history restore (`HX-History-Restore-Request`) and not boosted (`HX-Boosted`). Those two get full pages |
| `hx_redirect(url)` | A 200 with `HX-Redirect`, so htmx navigates the whole page (a 3xx would be followed inside the XHR) |
| `mark_fragment(response, kind)` | Sets the `TG-Fragment` header. Client scripts (`chargen.js`, `scene-chat.js`, `xp-spend.js`) swap a response only when the header names the fragment they asked for |
| `vary_on_htmx(response)` | Adds `Vary` for every header `is_fragment_request` reads (`FRAGMENT_REQUEST_HEADERS`), so a cache cannot serve a fragment as a full page |
| `trigger(response, event, detail, header="HX-Trigger")` | Adds a client event with JSON detail, keeping existing events. Use `header="HX-Trigger-After-Swap"` for events that must follow a completed swap |

The chargen views (`characters/views/core/chargen_mixins.py`) and the scene views
(`game/views.py`) use them. See [scenes and realtime](../../docs/architecture/scenes-and-realtime.md).

## JSON dropdown responses

[`core/ajax.py`](../ajax.py): `dropdown_options_response(queryset, value_attr="pk",
label_attr="name", extra_attrs=None)` returns `JsonResponse({"options": [{"value",
"label", ...}]})`. `label_attr="__str__"` uses `str(obj)`. Returning data rather than
HTML keeps the client from inserting server markup. The Mage chantry views use it.

## Linked stats

[`core/linked_stat.py`](../linked_stat.py) models a permanent rating with a temporary
pool (Willpower, Glamour and Banality, Faith and Torment, Pathos and Angst, Blood
Pool...).

`linked_stat_fields(name, *, default=0, min_permanent=0, max_permanent=10,
min_temporary=0, max_temporary=10, cap_temporary=True, temporary_default=None)` returns
three things to unpack in a model body: the permanent `IntegerField` (`<name>`), the
temporary `IntegerField` (`temporary_<name>`) and a `LinkedStat` descriptor. Both fields
get min/max validators.

```python
# characters/models/wraith/wraith.py
class Wraith(WtOHuman):
    pathos, temporary_pathos, pathos_stat = linked_stat_fields(
        "pathos", default=5, cap_temporary=False
    )
```

The descriptor always refers to the fields `<name>` and `temporary_<name>`. When the two
fields have other names, declare the fields yourself and add `LinkedStat` directly:

```python
# characters/models/vampire/vampire.py
blood = LinkedStat("max_blood_pool", "blood_pool", cap_temporary=False)
```

Reading the descriptor on an instance returns a `LinkedStatAccessor`:

| Member | Meaning |
|--------|---------|
| `permanent`, `max` | Permanent value. Setting it lowers the temporary value to match when capped |
| `temporary`, `current`, `available` | Temporary value. Setting it clamps to `min_temporary` and, when capped, to the permanent value |
| `spend(amount=1)` | Returns `False` if there are not enough points, else subtracts |
| `restore(amount=1)` | Adds (up to permanent when capped); returns the amount restored |
| `restore_full()` | Sets temporary to permanent when capped; returns the amount restored (0 when uncapped) |
| `can_spend(amount=1)`, `is_full`, `is_depleted`, `spent` | Queries |
| `str()`, `int()`, `bool()` | `"temp/perm"`, the temporary value, temporary > 0 |

The accessor changes attributes only; save the model yourself. Assigning to the
descriptor (`character.willpower_stat = 7`) sets the permanent value.

`LinkedStatFields.constraints(prefix)` and `linked_stat_constraints(permanent_field,
temporary_field, *, cap_temporary=True, min_permanent=0, max_permanent=10,
min_temporary=0, max_temporary=10, constraint_prefix="")` build `CheckConstraint`s for
the ranges and, when capped, `temporary <= permanent`. Database constraints need a
schema change (see [changing the schema](../../docs/guides/changing-the-schema.md)).

## Forms and widgets

[`core/forms/`](../forms/):

- `HumanLanguageForm(num_languages=1)`: a plain form with `language_1` ...
  `language_<n>` text fields, each an `AutocompleteTextInput` suggesting every
  `Language` except English, ordered by `frequency`. The human chargen languages step
  uses it.
- `CharacterTemplateForm(user=None)` and `CharacterTemplateImportForm(user=None)`: the
  character template forms (see [views](views.md#character-templates)).

[`core/widgets/autocomplete.py`](../widgets/autocomplete.py):
`AutocompleteTextInput(suggestions=None)` is a `TextInput` followed by a native
`<datalist>` (id `<input id>-suggestions`) with one escaped `<option>` per suggestion. It
needs no JavaScript.

The project's richer form widgets (chained selects, dot ratings, formsets) are in the
[widgets app](../../widgets/README.md).

## Validators

[`core/validators.py`](../validators.py), used in model `clean()` methods:

| Function | Raises `ValidationError` when |
|----------|-------------------------------|
| `validate_non_empty_name(value, field_name="Name")` | `value` is `None` or blank (code `required`) |
| `validate_gameline(value)` | `value` is `None` (code `required`) or not a code in `settings.GAMELINE_CHOICES` (code `invalid_choice`) |

## Helpers in `core/utils.py`

[`core/utils.py`](../utils.py):

| Helper | Behaviour |
|--------|-----------|
| `dice(dicepool, difficulty=6, specialty=False)` | Rolls d10s. Returns `(rolls, total)`: successes minus ones, never below 0 once there is a success; tens count twice with `specialty`. With no successes the raw negative total is returned (a botch) |
| `weighted_choice(dictionary, floor=0, ceiling=5)` | Random key, weighted by `(value + 1)²` after clamping values to `[floor, ceiling]` |
| `add_dot(character, trait, maximum)` | Adds one to an integer attribute below `maximum` and saves; returns whether it did |
| `check_floor_ceiling(x, floor, ceiling)` | Clamp |
| `filepath(instance, filename)` | `upload_to` for `Model.image`: the class's dotted path without `models` as folders, then `<name>.<ext>` (for example `characters/vampire/vampire/vampire/<name>.png`), lowercased, spaces to underscores, `..` and path separators removed from the name |
| `get_gameline_name(code)` | `settings.GAMELINES[code]["name"]`, or the code |
| `get_short_gameline_name(code)` | `settings.GAMELINES[code]["app_name"]` for URL building; `""` for `wod` |
| `display_queryset(objects)` | `<br>`-joined links. It does not escape names; only pass trusted data and mark the result safe deliberately |
| `CharacterOrganizationRegistry` | `register(handler)` and `cleanup_character(character)`. `Character.save()` calls `cleanup_character` when a character becomes retired or deceased; `Group` and `Chantry` register handlers that remove the character from their memberships. A failing handler is logged and does not stop the others |

## Context processor

[`core/context_processors.py`](../context_processors.py): `all_chronicles(request)` adds
`chronicles` (`game.security.readable_chronicles(user)`) and `navigation_chronicles`
(each readable chronicle with its unfinished scenes the user may see) to every template.
`core/tl/nav.html` renders the chronicles menu from it. It is registered in
`TEMPLATES[0]["OPTIONS"]["context_processors"]` next to two `accounts` processors
(`theme_context`, `notification_count`).

## Admin

[`core/admin.py`](../admin.py) registers `NewsItem`, `Book`, `Language`, `HouseRule`,
`BookReference`, `CharacterTemplate` (with list, search and read-only metadata fields)
and `TemplateApplication` with the Django admin at `/admin/`.

## See also

- [Caching](../../docs/architecture/caching.md)
- [Views](views.md)
- [Services](services.md)
- [widgets app](../../widgets/README.md)
- [`core/utils.py`](../utils.py)
