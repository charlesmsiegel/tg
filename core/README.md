# core

The `core` app holds what every other app builds on: the polymorphic base model and its
queryset, the permission model and the request-time access policy, the shared view mixins
and generic views, the Spread page shell (templates, `tl.css`, `tl.js`), template tag
libraries, caching helpers and a set of operational management commands. This page is the
map; the pages under [`docs/`](docs/) are the detailed reference.

Read it before you add a model, a view, a URL or a template anywhere in the project: most
of the rules those follow are enforced here.

## Main concepts

- **`core.models.Model`**: the abstract polymorphic base of every player-facing object
  (characters, items, locations, character templates). It carries `name`, `owner`,
  `chronicle`, `status`, `visibility`, `image` and sources, and runs `full_clean()` on
  every save. See [models](docs/models.md).
- **`PermissionManager`**: turns a user and an object into roles (owner, chronicle
  storyteller, player, observer, admin...) and roles into permissions (`VIEW_FULL`,
  `EDIT_FULL`, `SPEND_XP`...), with status-based restrictions. See
  [permissions and policies](docs/permissions-and-policies.md).
- **Route policies**: every project view is listed in
  [`route_policy_manifest.py`](route_policy_manifest.py) under one policy name
  (`PUBLIC_READ`, `OBJECT_DETAIL`, `OBJECT_WRITE`, `ACTION`...).
  [`AuthorizationMiddleware`](middleware/authorization.py) evaluates it before the view
  runs; a view without a policy is refused.
- **Spread**: the site's design system. Pages extend
  [`core/tl_base.html`](templates/core/tl_base.html) (or a shell built on it) and use
  the `tl` tag library. See [templates and static files](docs/templates-and-static.md).
- **Action endpoints**: one POST URL per state change, built on
  [`ObjectActionView`](actions.py). Detail views render pages and never handle POST. See
  [views](docs/views.md#action-endpoints).

## Key modules

| Path | Responsibility |
|------|----------------|
| [`models.py`](models.py) | `Model` base, `ModelQuerySet`/`ModelManager`, `Book`, `BookReference`, `Observer`, `NewsItem`, `Language`, `HouseRule`, `CharacterTemplate`, rating base classes |
| [`base.py`](base.py) | `ValidatedSaveMixin` (full_clean on save for non-polymorphic models) |
| [`constants.py`](constants.py) | `GameLine`, `CharacterStatus`, `ImageStatus`, `AbilityFields`, `XPApprovalStatus` and other choice sets |
| [`permissions.py`](permissions.py) | `Role`, `Permission`, `VisibilityTier`, `PermissionManager` |
| [`permission_context.py`](permission_context.py) | `ObjectPermissions` snapshot exposed to templates as `object_perms` |
| [`access_policy.py`](access_policy.py) | `authorize_route()`: evaluates a view's declared policy |
| [`route_policy_manifest.py`](route_policy_manifest.py) | `POLICIES` / `VIEW_POLICIES`: the reviewed view-to-policy list |
| [`middleware/`](middleware/) | `AuthorizationMiddleware`, `AuthErrorHandlerMiddleware` |
| [`mixins.py`](mixins.py) | All class-based-view mixins (permission, message, template, creation scoping) |
| [`model_registry.py`](model_registry.py), [`registry_urls.py`](registry_urls.py) | Declarative CRUD views and URLs for item and location types |
| [`views/`](views/) | Home, books, languages, news, house rules, character templates, public projections, type selection, `DictView`, cached and reference views, registry router, error handlers |
| [`urls.py`](urls.py) | The `core:` URL namespace, mounted at the site root |
| [`create_redirects.py`](create_redirects.py) | `resolve_object_type_url()`: from a chosen object type to its create or list page |
| [`actions.py`](actions.py) | `ObjectActionView`: load, authorize, validate, perform, redirect |
| [`services/`](services/) | `ApprovalService`, `ChronicleDataService` |
| [`cache.py`](cache.py) | Cache keys, `cache_function`, `get_cached_reference_list`, `cache_page_per_visitor` |
| [`htmx.py`](htmx.py), [`ajax.py`](ajax.py) | htmx request/response helpers, JSON dropdown responses |
| [`context_processors.py`](context_processors.py) | `all_chronicles`: readable chronicles and their open scenes for the nav |
| [`template_resolution.py`](template_resolution.py) | `shared_template_names()`: specific template first, shared fallback after |
| [`forms/`](forms/), [`widgets/`](widgets/) | `HumanLanguageForm`, character template forms, `AutocompleteTextInput` |
| [`admin.py`](admin.py) | Django admin registrations for the core models |
| [`linked_stat.py`](linked_stat.py) | Permanent/temporary stat pairs (Willpower, Blood Pool...) |
| [`xp_utils.py`](xp_utils.py), [`utils.py`](utils.py), [`validators.py`](validators.py) | XP awarding, dice and misc helpers, shared validators |
| [`templatetags/`](templatetags/) | `tl`, `tl_forms`, `sanitize_text`, `permissions`, `dots`, `field` and smaller libraries |
| [`templates/core/`](templates/core/) | `tl_base.html`, `form.html`, `misc/form.html`, `object.html`, `tl_auth.html`, error pages, registry fallbacks, `tl/` and `misc/` partials |
| [`static/core/`](static/core/) | `tl/tl.css`, `tl/tl.js`, `js/validation.js` |
| [`management/commands/`](management/commands/) | Data audits, cleanup, export/import, game data loading, resets |
| [`tests/`](tests/) | Unit tests plus project-wide guards (route policies, template policy, query budgets, action endpoints) and shared fixtures (`template_fixtures`, `action_audience`) |

## How it connects to other apps

- `characters`, `items` and `locations` subclass `core.models.Model`; their views use the
  mixins from [`mixins.py`](mixins.py) and list themselves in the route manifest.
  `items` and `locations` declare their CRUD views through
  [`model_registry.py`](model_registry.py) (`items/registry.py`, `locations/registry.py`).
- `game` supplies `Chronicle`, `STRelationship` and the visibility helpers in
  `game/security.py` (`readable_chronicles`, `staffed_chronicles`, `filter_scenes`...)
  that the permission code and the context processor call.
- `accounts` uses `ApprovalService` for submit, return and approve actions and supplies
  two of the template context processors.
- `widgets` provides the form widgets; its `page_media` tag is rendered by
  `tl_base.html`.
- `tg` wires the middleware, context processor and error handlers in its settings and
  URLs.

## Documentation

| Page | Covers |
|------|--------|
| [models.md](docs/models.md) | Base model, queryset, concrete core models, rating bases, constants |
| [permissions-and-policies.md](docs/permissions-and-policies.md) | Roles, permissions, status rules, route policies, middleware, template capabilities |
| [mixins.md](docs/mixins.md) | Every view mixin: what it checks and when to use it |
| [views.md](docs/views.md) | Core URLs and views, `DictView`, cached views, registry views, action endpoints, error views |
| [services.md](docs/services.md) | `ApprovalService`, `ChronicleDataService`, XP helpers |
| [templates-and-static.md](docs/templates-and-static.md) | Spread shells and partials, tag libraries, `tl.css`, `tl.js` |
| [utilities.md](docs/utilities.md) | Cache, htmx, AJAX, linked stats, forms, widgets, validators, context processor, admin, helpers |
| [management-commands.md](docs/management-commands.md) | The commands in `core/management/commands/` |
| [testing.md](docs/testing.md) | Core tests and the project-wide guard tests |

## See also

- [Architecture overview](../docs/architecture/overview.md)
- [Authorization](../docs/architecture/authorization.md)
- [Frontend](../docs/architecture/frontend.md)
- [Adding a view](../docs/guides/adding-a-view.md)
- [Template tag reference](../docs/reference/template-tags.md)
