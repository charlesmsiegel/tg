# tg (project package)

`tg` is the Django project package: the settings modules and the logic that picks one,
the root URL configuration, the ASGI and WSGI entry points and the custom test runner.
It holds no models or views of its own. This page maps the package; the pages under
[`docs/`](docs/) describe each part. For the full list of settings and environment
variables see the [settings reference](../docs/reference/settings.md).

## Main concepts

- **One settings entry point.** `DJANGO_SETTINGS_MODULE` is `tg.settings` everywhere
  ([`manage.py`](../manage.py), [`asgi.py`](asgi.py), [`wsgi.py`](wsgi.py)). The package
  [`settings/__init__.py`](settings/__init__.py) imports everything from
  `settings/development.py` or `settings/production.py` according to the environment
  variable `DJANGO_ENVIRONMENT`; both start from `settings/base.py`. See
  [settings](docs/settings.md).
- **ASGI first.** The site is an ASGI application built with Django Channels: HTTP goes
  to Django, WebSockets to the scene chat consumer. `daphne` is the first installed app,
  so `python manage.py runserver` serves it. See [ASGI and WSGI](docs/asgi-and-wsgi.md).
- **App URL namespaces.** Each app's URLs are included under a namespace named after the
  app; `core` sits at the site root. See [URLs](docs/urls.md).
- **Tests build local app tables from the models.** The local apps commit no migration
  files, so `LocalMigrationTestRunner` disables migrations for them in the test database.
  See [test runner](docs/test-runner.md).

## Key modules

| Path | Responsibility |
|------|----------------|
| [`settings/__init__.py`](settings/__init__.py) | Loads `.env`, then chooses development or production settings from `DJANGO_ENVIRONMENT` (default `development`); any other value raises `ValueError` |
| [`settings/base.py`](settings/base.py) | Shared settings: apps, middleware, templates and context processors, SQLite database with `ATOMIC_REQUESTS`, static and media paths, e-mail, `GAMELINES`/`GAMELINE_CHOICES`, logging, channel layer, test runner |
| [`settings/development.py`](settings/development.py) | `DEBUG = True`, default secret key, console e-mail, optional Django Debug Toolbar, SQL logging, local-memory cache |
| [`settings/production.py`](settings/production.py) | `DEBUG = False`, required `SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`, HTTPS and cookie security, Redis cache, sessions and channel layer, hashed static files, rotating log files |
| [`urls.py`](urls.py) | Root URLconf: admin, app includes, password-reset views, media, debug toolbar, error handlers |
| [`asgi.py`](asgi.py) | `application`: `ProtocolTypeRouter` for HTTP and WebSocket |
| [`wsgi.py`](wsgi.py) | `application` for WSGI servers (HTTP only) |
| [`test_runner.py`](test_runner.py) | `LocalMigrationTestRunner` |

`tg/settings.py.backup` is an old single-file settings module kept in the repository. It
is not importable as `tg.settings` (the `settings/` package takes that name) and nothing
loads it.

## How it connects to other apps

- `settings/base.py` installs the project apps (`accounts`, `characters`, `game`,
  `tg_schema`, `items`, `locations`, `core`, `widgets`) with `daphne`, `channels` and
  `polymorphic`, and wires `core`'s middleware (`AuthorizationMiddleware`,
  `AuthErrorHandlerMiddleware`) and context processors from `core` and `accounts`.
- `urls.py` mounts every app and points the 403, 404 and 500 handlers at
  `core.views.errors`.
- `asgi.py` routes WebSockets to `game.routing.websocket_urlpatterns`.
- The `widgets` app adds its chained-select endpoint to the root URLconf at startup (see
  [URLs](docs/urls.md)).

## Documentation

| Page | Covers |
|------|--------|
| [settings.md](docs/settings.md) | How the settings module is chosen, what each module sets, environment variables, gotchas |
| [urls.md](docs/urls.md) | The root URLconf, namespaces, authentication URLs, error handlers |
| [asgi-and-wsgi.md](docs/asgi-and-wsgi.md) | The ASGI application, WebSocket routing and the WSGI entry point |
| [test-runner.md](docs/test-runner.md) | `LocalMigrationTestRunner` and the test database |

## See also

- [Settings reference](../docs/reference/settings.md)
- [Configuration](../docs/getting-started/configuration.md)
- [Deployment](../docs/operations/deployment.md)
- [Architecture overview](../docs/architecture/overview.md)
