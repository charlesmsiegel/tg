# Root URL configuration

This page describes [`tg/urls.py`](../urls.py), the project's root URLconf: which app is
mounted where and under which namespace, how the authentication URLs are layered, what
is added only in development or at runtime, and the error handlers. It is for developers
adding URLs or reversing them. Each app's own routes are documented in that app; the
project-wide list is the [URL reference](../../docs/reference/urls.md).

## Mounted apps

| Prefix | Included module | Namespace |
|--------|-----------------|-----------|
| `admin/` | `django.contrib.admin.site.urls` | `admin` |
| (root) | `core.urls` | `core` |
| `characters/` | `characters.urls` | `characters` |
| `locations/` | `locations.urls` | `locations` |
| `items/` | `items.urls` | `items` |
| `game/` | `game.urls` | `game` |
| `accounts/` | `accounts.urls` | `accounts` |
| `accounts/` | `django.contrib.auth.urls` | none |

Each app include uses `include((module, app_name), namespace=app_name)`, so reverse app
URLs with the namespace: `reverse("core:home")`, `reverse("characters:index")`,
`{% url "game:chronicles" %}`. Apps nest further namespaces per gameline and per action
(for example `items:mummy:create:relic`); see the app docs.

## Authentication URLs

Three things share the `accounts/` prefix, and Django uses the first pattern that
matches:

1. `accounts.urls` (namespace `accounts`): the site's own views, including
   `accounts:login` (`/accounts/login/`), `accounts:signup` and `accounts:password_reset`.
2. Three password-reset views from `django.contrib.auth.views`, declared in `tg/urls.py`
   with the site's templates so the admin's `registration/` templates are not used:

   | Path | Name | Template |
   |------|------|----------|
   | `accounts/password_reset/done/` | `password_reset_done` | `accounts/auth/password_reset_done.html` |
   | `accounts/reset/<uidb64>/<token>/` | `password_reset_confirm` | `accounts/auth/password_reset_confirm.html` |
   | `accounts/reset/done/` | `password_reset_complete` | `accounts/auth/password_reset_complete.html` |

3. `django.contrib.auth.urls`, which supplies the un-namespaced names Django's auth code
   reverses (`login`, `logout`, `password_change`, `password_reset`...). `LOGIN_URL =
   "login"` reverses to `/accounts/login/`, which the `accounts` include answers first.

## Development and runtime additions

- **Media**: `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` is appended.
  Django's `static()` returns patterns only when `DEBUG` is true, so uploaded media is
  served by Django in development only.
- **Debug toolbar**: when `DEBUG` is true and `debug_toolbar` can be imported,
  `__debug__/` is added in front of the other patterns.
- **Chained-select endpoint**: at startup `widgets.apps.WidgetsConfig.ready()` inserts
  `path("__chained_select__/", auto_chained_ajax_view, name="__chained_select_ajax__")`
  at the start of `urlpatterns`. It does not appear in `tg/urls.py`. See
  [chained selects](../../widgets/docs/chained-selects.md#json-endpoint).

## Error handlers

| Handler | View |
|---------|------|
| `handler403` | `core.views.errors.error_403` |
| `handler404` | `core.views.errors.error_404` |
| `handler500` | `core.views.errors.error_500` |

Django uses them when `DEBUG` is false. See [core views](../../core/docs/views.md#error-views).

## Access control for routes

Every view under a project app must be declared in
[`core/route_policy_manifest.py`](../../core/route_policy_manifest.py) (or in an item or
location registry); `core.middleware.authorization.AuthorizationMiddleware` refuses
undeclared project views. Views from Django itself (`admin`, `django.contrib.auth`) are
outside that check. Adding a URL for a project view therefore also means adding its
policy; see [permissions and policies](../../core/docs/permissions-and-policies.md#declaring-a-policy-for-a-new-view).

## See also

- [URL reference](../../docs/reference/urls.md)
- [Adding a view](../../docs/guides/adding-a-view.md)
- [core views and URLs](../../core/docs/views.md)
- [accounts app](../../accounts/README.md)
- [`tg/urls.py`](../urls.py)
