# Local development

This page covers day-to-day work on a checkout that is already installed: running the
development server, how the settings module is chosen, the debug toolbar, websockets on
your machine, logging, and the commands and scripts you reach for most often. It assumes
you have followed [Installation](installation.md).

## Run the development server

```bash
python manage.py runserver 7000
```

Port 7000 is the project convention; any free port works.

`daphne` is the first entry in `INSTALLED_APPS`
([`tg/settings/base.py`](../../tg/settings/base.py)), ahead of
`django.contrib.staticfiles`. Daphne ships its own `runserver` command, and because its
app comes first, `manage.py runserver` is Daphne's, not Django's. It serves the ASGI
application named by `ASGI_APPLICATION` (`tg.asgi.application`), so one process handles
both HTTP and websockets. [`tg/asgi.py`](../../tg/asgi.py) routes:

| Protocol | Handled by |
|----------|------------|
| `http` | Django's ASGI handler (all normal views) |
| `websocket` | `AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(game.routing.websocket_urlpatterns)))` |

With `DEBUG = True`, Daphne's `runserver` also serves static files from the source
directories through `ASGIStaticFilesHandler`, so you do not need `collectstatic` during
development.

Options Daphne's `runserver` adds or keeps (from `python manage.py help runserver`):

| Option | Effect |
|--------|--------|
| `addrport` | Port, or `ipaddr:port`. `0.0.0.0:7000` listens on every interface. |
| `--noreload` | Disable the auto-reloader. |
| `--noasgi` | Run Django's old WSGI `runserver` instead. Websockets do not work in this mode; scene pages fall back to plain HTTP posting. |
| `--nostatic` | Do not serve files under `STATIC_URL`. |
| `--insecure` | Serve static files even with `DEBUG = False`. |
| `--http_timeout`, `--websocket_handshake_timeout` | Daphne timeouts, in seconds. |
| `--websocket-max-message-size`, `--websocket-max-frame-size` | Upper limits for incoming websocket data, in bytes. |

Open `http://localhost:7000/` or `http://127.0.0.1:7000/`. Do not use `http://[::1]:7000/`:
the development `ALLOWED_HOSTS` leaves `[::1]` out, and the websocket origin check uses
`ALLOWED_HOSTS`, so scene chat would refuse the connection.

## How settings are selected

`manage.py`, [`tg/asgi.py`](../../tg/asgi.py) and [`tg/wsgi.py`](../../tg/wsgi.py) all
default `DJANGO_SETTINGS_MODULE` to `tg.settings`, the package in
[`tg/settings/`](../../tg/settings/). Its [`__init__.py`](../../tg/settings/__init__.py)
reads the `DJANGO_ENVIRONMENT` environment variable (lower-cased) and star-imports one
module:

| `DJANGO_ENVIRONMENT` | Settings loaded |
|----------------------|-----------------|
| unset | [`development.py`](../../tg/settings/development.py) |
| `development` | `development.py` |
| `production` | [`production.py`](../../tg/settings/production.py) |
| anything else, including an empty string | `ValueError` at import; nothing starts |

Both modules start with `from .base import *`, so [`base.py`](../../tg/settings/base.py)
holds everything shared and the two environment modules only override.

`__init__.py` loads the `.env` file before it reads `DJANGO_ENVIRONMENT`, so the variable
may come from the real process environment or from `.env` (the real environment wins).
See [Configuration](configuration.md) for every variable the settings read.

What development changes compared with production, in short: `DEBUG = True`, a fallback
`SECRET_KEY`, `ALLOWED_HOSTS` of `localhost,127.0.0.1`, the console e-mail backend,
`LocMemCache`, database-backed sessions, the in-memory channel layer and no HTTPS
settings. The full comparison is in the [Settings reference](../reference/settings.md).

## Debug toolbar

`development.py` adds `debug_toolbar` to `INSTALLED_APPS` and puts
`debug_toolbar.middleware.DebugToolbarMiddleware` first in `MIDDLEWARE`, but only if the
package imports (it is in [`requirements.txt`](../../requirements.txt)).
[`tg/urls.py`](../../tg/urls.py) mounts its URLs at `/__debug__/` when `DEBUG` is true.

The toolbar shows only to signed-in staff or superusers:
`DEBUG_TOOLBAR_CONFIG["SHOW_TOOLBAR_CALLBACK"]` points at
`tg.settings.development.show_toolbar_callback`, which replaces the toolbar's default
check. `INTERNAL_IPS` is set to `127.0.0.1` and `::1` but the callback does not consult
it. `IS_RUNNING_TESTS` is `False`, which stops the toolbar from refusing to load while
tests run.

The toolbar's own views live in a third-party module, so the project's
`core.middleware.authorization.AuthorizationMiddleware` does not apply its route policies
to them (it skips views whose module is outside the project's prefixes).

The toolbar also adds a `debugsqlshell` management command: a Django shell that prints
the SQL of every query it runs.

## Websockets locally

Live scene chat is the only websocket feature: `game.consumers.SceneChatConsumer` at
`ws/scene/<scene_id>/` ([`game/routing.py`](../../game/routing.py)). In development the
channel layer is `channels.layers.InMemoryChannelLayer` (from `base.py`), which lives
inside one process. That is enough for `runserver`, where every browser tab talks to the
same process. It is not enough for anything spread over several processes: a second
server or a `runworker` process would not see the first one's group messages. Production
uses Redis for that reason.

No Redis, no extra process and no separate port are needed. If websockets fail locally,
check, in order: that you are not running with `--noasgi`; that the page's host is in
`ALLOWED_HOSTS` (`localhost` or `127.0.0.1`); and the browser console for the close code.
The flow itself is described in
[Scenes and real-time chat](../architecture/scenes-and-realtime.md).

## Logging in development

`base.py` defines the handlers; `development.py` adjusts levels:

- Project loggers (`tg`, `accounts`, `characters`, `game`, `items`, `locations`, `core`)
  log at `DEBUG` to `logs/debug.log`, errors to `logs/error.log`, and `INFO` and above to
  the console. Development adds the verbose `console_debug` handler to each of them, so
  their `INFO` messages appear twice on the console, once per format.
- SQL queries are not printed by default (`django.db.backends` goes to the `null`
  handler). Set `DJANGO_LOG_SQL=True` to print every query to the console at `DEBUG`, or
  use the debug toolbar's SQL panel or `debugsqlshell`.
- `logs/warning.log` is defined but no development logger writes to it.

The `logs/` directory must exist (it is kept in git with its own `.gitignore`).

## Everyday commands

| Task | Command |
|------|---------|
| Check configuration | `python manage.py check` |
| Open a shell with models imported | `python manage.py shell` (Django 5.2 imports every model automatically) |
| Apply model changes to your local database | `python manage.py makemigrations && python manage.py migrate` (the generated files stay local; see [Changing the schema](../guides/changing-the-schema.md)) |
| Pull and update | `bash update.sh` (`git pull`, `makemigrations`, `migrate`, `collectstatic`) |
| Load or refresh game data | `python manage.py populate_gamedata` (see [Seed data](seed-data.md)) |
| Preview which data files would load | `python manage.py populate_gamedata --dry-run` |
| Fill a chronicle with sample characters and scenes | `python manage.py populate_test_chronicle --chronicle <id>` |
| Run the tests | `python manage.py test` (see [Testing](../development/testing.md)) |
| Format and lint | `pre-commit run --all-files` (see [Code style](../development/code-style.md)) |

All project management commands are listed in
[Management commands](../reference/management-commands.md).

### A storyteller account to test with

Storyteller pages need an `STRelationship` row; being a superuser is not enough
(`accounts.models.Profile.is_st`). Either create a chronicle and an `STRelationship` in
`/admin/`, or run `python manage.py reset_demo_data --confirm`, which **deletes all
characters, items, locations, scenes, weeks, XP requests and chronicles** (and every
non-superuser account unless you pass `--preserve-users`) and then creates `demo_st` and
`demo_player` and a demo chronicle with `demo_st` as storyteller. The accounts get the
`--password` you pass, or a random password the command prints. It runs only with
`DEBUG=True`.

### Helper scripts

[`scripts/`](../../scripts/) holds standalone tools; each documents its usage in its
module docstring. Run them from the repository root.

| Script | Purpose |
|--------|---------|
| `scripts/template_screenshots.py capture OUT_DIR` / `compare BEFORE AFTER` | Seed a throwaway database with `core.tests.template_fixtures.seed()`, start `runserver` on it and screenshot every fixture page; then diff two captures. Needs `playwright` and a Chromium build. Uses [`scripts/screenshot_settings.py`](../../scripts/screenshot_settings.py). |
| `scripts/inventory_authorization_routes.py` | Print every URL with its view and authorization policy as Markdown. Read-only. |
| `scripts/build_route_policy_manifest.py` | Generate a starting route-policy manifest when classifying newly routed views. See [Authorization](../architecture/authorization.md). |
| `scripts/find_dead_code.py` | Report dead-code candidates (URL names, views, templates, tags, symbols). |
| `scripts/template_similarity.py` | Report identical and near-identical templates. |
| `scripts/inventory_model_routes.py`, `scripts/inventory_chargen_views.py` | Read-only inventories of item/location routes and character-creation views. |

## See also

- [Installation](installation.md)
- [Configuration](configuration.md)
- [Settings reference](../reference/settings.md)
- [Testing](../development/testing.md)
- [Architecture overview](../architecture/overview.md)
- [Scenes and real-time chat](../architecture/scenes-and-realtime.md)
