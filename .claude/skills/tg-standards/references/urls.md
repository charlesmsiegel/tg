# URLs

Rules for adding a route or a URL name. The full URL map is in
[docs/reference/urls.md](../../../../docs/reference/urls.md). Every new route also needs an
access policy ([permissions.md](permissions.md)).

## Layout

[`tg/urls.py`](../../../../tg/urls.py) mounts each app under an instance namespace:
`core` at `/`, `characters`, `items`, `locations`, `game` and `accounts` under their own
prefix.

`characters`, `items` and `locations` share one structure:

```text
<app>/urls/
├── __init__.py        # root: one include per GameLine.URL_PATTERNS entry + core modules
├── core/              # no __init__.py; create.py, update.py, index.py, detail.py
└── <gameline>/        # vampire, werewolf, mage, wraith, changeling, demon, mummy, hunter
    ├── __init__.py    # urls = [create/, update/, list/ namespaces + detail]
    ├── create.py      # urls = [...]
    ├── update.py
    ├── index.py       # list views
    └── detail.py      # detail views and per-object actions
```

- The root `__init__.py` iterates `core.constants.GameLine.URL_PATTERNS` (`(url_path,
  module_name, namespace)`), the single list of gameline URL modules. A new gameline adds
  an entry there and a package under each app's `urls/`.
- Leaf modules export a plain list named `urls`. They never define `app_name`:
  `core/tests/test_dead_code_removed.py::test_list_included_url_modules_have_no_app_name`
  fails if one does (the namespace comes from the `include((urls, name), namespace=...)`
  tuple). `game/urls.py` is the exception and keeps `app_name = "game"`.
- For items and locations, the leaf modules delegate to the registry:
  `urls = registry.urls("mummy", "detail")`. Add routes on the `ActionSpec.routes`, not
  in the leaf file ([registry.md](registry.md)).
- The root `__init__.py` of `characters`, `items` and `locations` imports every gameline
  module without catching errors, so a broken module fails at startup instead of silently
  dropping its routes (`characters/tests/urls/test_url_patterns.py`).

## Names

| Route | Name |
|-------|------|
| Detail of a gameline model | `<app>:<gameline>:<model>` (detail modules are included without a namespace) |
| Create | `<app>:<gameline>:create:<model>` |
| Update | `<app>:<gameline>:update:<model>` |
| List | `<app>:<gameline>:list:<model>` |
| Core (non-gameline) model | `<app>:<model>`, `<app>:create:<model>`, `<app>:update:<model>`, `<app>:list:<model>` |
| Per-object action | a verb in the detail module: `characters:retire`, `game:scene_close` |

Examples: `characters:vampire:clan`, `characters:vampire:update:clan`,
`items:mummy:create:relic`, `characters:character` (the type router). `<gameline>` is the
namespace from `URL_PATTERNS` (`vampire`, not `vtm`); `<model>` is snake_case and usually
the model's `type` or registry slug.

Keep existing names and paths stable: templates and `get_absolute_url` reverse them, and
`core/tests/fixtures/model_routes.json` pins the registry's names and paths
(`core/tests/test_model_registry.py::test_existing_routes_keep_names_and_paths`).

## Paths

- Object routes use `<int:pk>` in new code. Many older routes use `<pk>`;
  `AuthorizationMiddleware` answers 404 for any `pk` that is not a positive ASCII integer,
  so both are safe, but `<int:pk>` keeps `reverse()` strict.
- Actions: `<int:pk>/<verb>/` (`<int:pk>/retire/`), POST only, one view per verb
  ([views.md](views.md)). A second id is a named kwarg:
  `<int:pk>/xp-requests/<int:request_pk>/approve/`.
- Querystrings select tabs and filters (`?tab=`, `?status=`); they never select an action,
  and pages that read them are not cached ([caching.md](caching.md)).

## Reversing

- Python: `reverse("characters:vampire:clan", kwargs={"pk": obj.pk})`, or the model's
  `get_absolute_url()` / `get_update_url()` / `get_creation_url()`.
- Templates: `{{ object.get_absolute_url }}`, `{{ object|update_url }}` (empty when the
  model has no update route), `{% url 'game:scene_close' scene.pk %}`.
- Redirect to a URL name with `redirect("characters:index")`; `DictView.default_redirect`
  accepts a name or a view.

## Checklist

- [ ] Route added to the right leaf module (or registry `routes`), no `app_name`.
- [ ] Name follows the table; existing names and paths unchanged.
- [ ] `<int:pk>`; actions are POST-only verb routes.
- [ ] Policy declared; `python manage.py check` passes.
- [ ] URL test: `reverse()` resolves and the view answers each audience correctly.

## See also

- [docs/reference/urls.md](../../../../docs/reference/urls.md)
- [`core/constants.py`](../../../../core/constants.py) (`GameLine.URL_PATTERNS`)
- [registry.md](registry.md), [permissions.md](permissions.md), [views.md](views.md)
