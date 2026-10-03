# Deployment

This page describes what a production installation of the site needs and how to install
and update one: settings selection, environment variables, the database, Redis, the ASGI
server, static and media files, and the order of commands for a first deploy and for an
update. It is for whoever runs the server. For a fresh Ubuntu Server host,
[`clean_install.sh`](../../clean_install.sh) provides a complete nginx, systemd, Redis and
Daphne installation. The rest of this page documents the individual pieces and the manual
equivalents.

## What a production host runs

| Component | Provided by the repo | Role |
|-----------|----------------------|------|
| Django application under an ASGI server | [`tg/asgi.py`](../../tg/asgi.py), `daphne` in [`requirements.txt`](../../requirements.txt) | HTTP pages and the scene-chat WebSocket |
| Redis | Settings only ([`tg/settings/production.py`](../../tg/settings/production.py)) | Cache, sessions and the Channels layer |
| Database | SQLite by default ([`tg/settings/base.py`](../../tg/settings/base.py)) | All application data |
| Reverse proxy | [`clean_install.sh`](../../clean_install.sh) installs nginx | TLS, `/static/` and `/media/`, WebSocket upgrade, request size limits |
| Process manager | [`clean_install.sh`](../../clean_install.sh) installs `tg.service` | Starts, restarts and supervises the ASGI server |

Writable paths under the repository root: `db.sqlite3` and its directory (SQLite writes
journal files beside it), `logs/`, `media/` (uploads) and `collected_static/` (written by
`collectstatic`).

## Automated clean Ubuntu Server install

For a new Ubuntu Server VM, clone the repository, copy your production `.env` into the
repository root, and run:

```bash
./clean_install.sh
```

Run it as the normal login user, **not** with `sudo`; it asks for sudo authorization
immediately and keeps that authorization alive for the install. The script never rewrites
`.env`. It requires `DJANGO_ENVIRONMENT=production`, a real `SECRET_KEY`, and at least one
`DJANGO_ALLOWED_HOSTS` entry.

The installer:

- installs Python build dependencies, nginx, Redis, SQLite tools, TLS tools and ACL support;
- creates/reuses `.venv` and installs `requirements.txt`;
- runs `makemigrations`, `migrate`, `collectstatic`, `populate_gamedata`, and
  `check --deploy`;
- installs and enables `tg.service`, running Daphne on `127.0.0.1:8000`;
- configures nginx on ports 80 and 443, including WebSocket proxying and direct static/media
  serving;
- creates a self-signed first-boot TLS certificate so HTTPS works immediately, then performs
  an HTTPS smoke test through nginx.

The self-signed certificate is intentionally only a bootstrap certificate. Replace
`/etc/ssl/tg/tg-selfsigned.crt` and `/etc/ssl/tg/tg-selfsigned.key` (or update the nginx
site) with a trusted certificate for normal public use. The script is safe to rerun: it does
not reset or delete the database, and the game-data loader is designed to be rerunnable.

It deliberately does not create a superuser because that would make the otherwise
non-interactive install stop for account credentials. After installation, run
`.venv/bin/python manage.py createsuperuser` if the host needs an admin account.

## Selecting the production settings

`DJANGO_SETTINGS_MODULE` is `tg.settings` (set by [`manage.py`](../../manage.py),
[`tg/asgi.py`](../../tg/asgi.py) and [`tg/wsgi.py`](../../tg/wsgi.py)). That package,
[`tg/settings/__init__.py`](../../tg/settings/__init__.py), reads `DJANGO_ENVIRONMENT`:

| Value | Module loaded |
|-------|---------------|
| unset or `development` | [`tg/settings/development.py`](../../tg/settings/development.py) (`DEBUG = True`) |
| `production` | [`tg/settings/production.py`](../../tg/settings/production.py) (`DEBUG = False`) |
| anything else | `ValueError` at import |

The value is compared case-insensitively.

`DJANGO_ENVIRONMENT` may be set in the process environment or in `.env`: `__init__.py`
loads the `.env` file at the repository root with `load_dotenv()` before it reads any
variable, so every variable on this page can live there. `load_dotenv()` does not override
variables already present in the environment, so values set by the process manager win
over `.env`.

Both environment modules start with `from .base import *`, so everything in `base.py`
applies to production unless `production.py` overrides it.

## Environment variables

[`.env.example`](../../.env.example) is the template: copy it to `.env` in the repository
root (gitignored) and fill it in. The variables the settings read in production:

| Variable | Read in | Required | Default | Effect |
|----------|---------|----------|---------|--------|
| `DJANGO_ENVIRONMENT` | `settings/__init__.py` | Yes | `development` | Selects the settings module (above). |
| `SECRET_KEY` | `production.py` | Yes | none | A missing or empty value raises `ImproperlyConfigured` at startup. |
| `DJANGO_ALLOWED_HOSTS` | `production.py` | Yes | none | Comma-separated host names (spaces trimmed). Empty raises `ValueError`. Also used by the WebSocket origin check. |
| `CSRF_TRUSTED_ORIGINS` | `production.py` | No | empty list | Comma-separated origins with scheme, e.g. `https://example.com`. |
| `SECURE_SSL_REDIRECT` | `production.py` | No | `True` | Redirect HTTP to HTTPS. Only the exact string `True` enables it. |
| `SECURE_HSTS_SECONDS` | `production.py` | No | `31536000` | HSTS max-age; `0` disables HSTS. |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `production.py` | No | `True` | |
| `SECURE_HSTS_PRELOAD` | `production.py` | No | `True` | |
| `SESSION_COOKIE_AGE` | `production.py` | No | `1209600` (2 weeks) | Seconds. |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | `production.py` | No | `False` | |
| `ADMIN_EMAILS` | `production.py` | No | empty | Builds `ADMINS` and `MANAGERS`; see [Logging and monitoring](logging-and-monitoring.md#admins-and-error-email). |
| `REDIS_URL` | `production.py` | Yes, in practice | `redis://127.0.0.1:6379/1` (cache), `redis://127.0.0.1:6379/0` (channels) | One URL for cache, sessions and channel layer. |
| `DB_CONN_MAX_AGE` | `production.py` | No | `600` | Persistent connection lifetime for the default database. |
| `EMAIL_BACKEND` | `base.py` | Yes, for mail | console backend | Neither `base.py` nor `production.py` changes the default, so without this variable password-reset mail is printed to the server's stdout. |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_TIMEOUT` | `base.py` | For SMTP | `localhost`, `25`, `False`, `False`, empty, empty, `30` | Boolean flags are enabled only by the string `True`. |
| `DEFAULT_FROM_EMAIL`, `SERVER_EMAIL` | `base.py` | No | `noreply@tellurian-games.com`; `SERVER_EMAIL` defaults to `DEFAULT_FROM_EMAIL` | |
| `PASSWORD_RESET_TIMEOUT` | `base.py` | No | `3600` | Seconds a reset link stays valid. |

Notes on `.env.example`:

- There is no debug variable: development always has `DEBUG = True`; production always has
  `DEBUG = False`.
- The `DB_*` variables other than `DB_CONN_MAX_AGE`, and the AWS and Mailgun variables, are read
  only by commented-out code or by packages that are not in `requirements.txt`
  (`django-ses`, `django-anymail`, `django-storages`, `boto3`).

The full list of settings, including non-environment ones, is in the
[settings reference](../reference/settings.md).

## Database

`base.py` defines one database:

| Key | Value |
|-----|-------|
| `ENGINE` | `django.db.backends.sqlite3` |
| `NAME` | `BASE_DIR / "db.sqlite3"` (repository root) |
| `ATOMIC_REQUESTS` | `True`: each request runs in one transaction |
| `TEST.NAME` | `db_test.sqlite3` |

`production.py` keeps SQLite and adds `CONN_MAX_AGE` from `DB_CONN_MAX_AGE` (default 600
seconds); `DB_CONN_MAX_AGE=0` closes the connection at the end of each request.

`production.py` also contains **commented-out** PostgreSQL and MySQL `DATABASES` blocks that
read `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_CONN_MAX_AGE` and (PostgreSQL)
`DB_SSLMODE`, with `ATOMIC_REQUESTS = True`. They are examples, not active configuration. To
use one, uncomment it and install the database driver yourself: no PostgreSQL or MySQL driver
is in `requirements.txt`. Tables are created the same way on any backend (see
[First deploy](#first-deploy)).

With SQLite, the application, every management command and every ASGI process must run on
the same host and see the same file. Back it up as described in
[Maintenance](maintenance.md#backups).

## Redis

Production uses one Redis server for three things, all configured in `production.py`:

| Use | Setting | Configuration |
|-----|---------|---------------|
| Cache | `CACHES["default"]` | `django_redis.cache.RedisCache` at `REDIS_URL`; `KEY_PREFIX = "tg"`; `TIMEOUT = 300`; zlib compression; `SOCKET_CONNECT_TIMEOUT` and `SOCKET_TIMEOUT` 5 s; pool of 50 connections; `IGNORE_EXCEPTIONS = True` |
| Sessions | `SESSION_ENGINE = "django.contrib.sessions.backends.cache"`, `SESSION_CACHE_ALIAS = "default"` | Sessions live only in the cache above |
| Channel layer | `CHANNEL_LAYERS["default"]` | `channels_redis.core.RedisChannelLayer` at `REDIS_URL`, `capacity` 1500, `expiry` 10 |

When `REDIS_URL` is set, cache, sessions and the channel layer share that one Redis database.
The two different defaults (`/1` for the cache, `/0` for channels) apply only when the
variable is unset.

What happens when Redis is unavailable:

- Cache reads miss and writes are dropped silently (`IGNORE_EXCEPTIONS`), so pages still render,
  more slowly.
- Sessions cannot be read or stored: every visitor is anonymous and logins do not persist.
- The scene-chat WebSocket cannot join or broadcast to its group. A post saved over HTTP still
  commits; its broadcast runs in a `transaction.on_commit` callback
  ([`game/scene_chat.py`](../../game/scene_chat.py)) whose failure is logged to
  `logs/error.log` and does not fail the post.

Development needs no Redis: it uses `LocMemCache`, database sessions and
`InMemoryChannelLayer` ([Installation](../getting-started/installation.md#redis)).

## Application server

Serve the site with an ASGI server so that one process handles both HTTP and WebSockets.
[`tg/asgi.py`](../../tg/asgi.py) builds a `ProtocolTypeRouter`:

- `http` goes to Django's ASGI handler and the normal middleware stack;
- `websocket` goes through `AllowedHostsOriginValidator` and `AuthMiddlewareStack` to the
  routes in [`game/routing.py`](../../game/routing.py): one route, `ws/scene/<scene_id>/`,
  served by `game.consumers.SceneChatConsumer`.

`daphne` is pinned in `requirements.txt` and listed first in `INSTALLED_APPS` (so
`manage.py runserver` is the Daphne development server). A production invocation from the
repository root looks like:

```bash
DJANGO_ENVIRONMENT=production daphne -b 127.0.0.1 -p 8000 tg.asgi:application
```

Useful Daphne options (from `daphne --help`): `-u/--unix-socket` to bind a socket instead of
a port, `--proxy-headers` to take the client address from `X-Forwarded-For` (use it behind
a proxy: the log-in throttle counts attempts per client address, see
[Security](security.md)),
`--access-log` to choose where the access log goes, and `--websocket-max-message-size` /
`--websocket-max-frame-size`.

Run the server from the repository root: `populate_gamedata`, `reset_db` and the Python
import path all assume it as the working directory.

`WSGI_APPLICATION = "tg.wsgi.application"` also exists ([`tg/wsgi.py`](../../tg/wsgi.py)). It
serves HTTP only; under a WSGI server there is no WebSocket endpoint, so scene pages lose
live updates.

You can run more than one ASGI process: the Redis channel layer and Redis-backed sessions are
shared between them. Each process loads the static-file manifest and Python code at start, so
restart every process after an update.

## Reverse proxy requirements

The repository contains no proxy configuration. Whatever you use must:

- **Terminate TLS and set `X-Forwarded-Proto`.** `SECURE_PROXY_SSL_HEADER` is
  `("HTTP_X_FORWARDED_PROTO", "https")`. Without the header Django treats every request as
  plain HTTP and, with `SECURE_SSL_REDIRECT` on, redirects forever. Overwrite any
  `X-Forwarded-Proto` sent by clients.
- **Pass the original `Host`.** It must match `DJANGO_ALLOWED_HOSTS`. The WebSocket route's
  `AllowedHostsOriginValidator` also checks the browser's `Origin` header against
  `ALLOWED_HOSTS`, so pass `Origin` through unchanged.
- **Upgrade WebSockets** on `/ws/` (the client connects to `/ws/scene/<id>/?v=2` with `wss://`
  when the page is HTTPS).
- **Serve `/static/`** from `collected_static/` and **`/media/`** from `media/`. Django does
  not serve either in production: [`tg/urls.py`](../../tg/urls.py) appends
  `static(settings.MEDIA_URL, ...)`, which returns no patterns when `DEBUG` is `False`, and
  nothing in the project serves static files outside the development server.
- **Limit request body size.** `DATA_UPLOAD_MAX_MEMORY_SIZE` (5 MB) caps non-file form data,
  and the scene consumer uses the same value as its message limit. Image uploads larger than
  `MAX_IMAGE_UPLOAD_SIZE` (5 MB) fail validation, but only after Django has received them
  (`FILE_UPLOAD_MAX_MEMORY_SIZE` only decides when an upload spills to a temporary file), so
  cap the request body at the proxy too.
- If the public origin differs from the `Host` the application sees, list it in
  `CSRF_TRUSTED_ORIGINS`.

## Static and media files

| Setting | Value | Notes |
|---------|-------|-------|
| `STATIC_URL` | `static/` | |
| `STATICFILES_DIRS` | `source_static/` | Site-wide assets and vendored libraries |
| `STATIC_ROOT` | `collected_static/` | Written by `collectstatic`; gitignored |
| `STORAGES["staticfiles"]` (production) | `ManifestStaticFilesStorage` | Hashed file names from `collected_static/staticfiles.json` |
| `STORAGES["default"]` (production) | `FileSystemStorage` | Uploads |
| `MEDIA_ROOT` | `media/` | Gitignored |
| `MEDIA_URL` | `/media/` | |

Because production uses `ManifestStaticFilesStorage`, run `collectstatic` before starting the
server and after every update that changes a static file; a template that references a file
missing from the manifest fails to render. Edit static files in `source_static/` or
`<app>/static/`, never in `collected_static/`.

Uploaded images are stored under `media/` at a path built by `core.utils.filepath` from the
model's module path, a random token and the object's name (see [Security](security.md#uploads)).

`production.py` has a commented-out S3 example that configures `STORAGES` for
`django-storages` (not in `requirements.txt`).

## Schema: generated migrations and `tg_schema`

The local apps (`accounts`, `characters`, `core`, `game`, `items`, `locations`) commit only an
empty `migrations/__init__.py`; `.gitignore` excludes everything else under `*/migrations/`
except the numbered files in `tg_schema/migrations/`. On each host:

- `python manage.py makemigrations` generates the local apps' migrations from the current
  models. These files exist only on that host and record which schema its database has.
- `python manage.py migrate` applies them, then the committed
  [`tg_schema`](../../tg_schema/) migrations. Those are guarded `RunPython` patches that add
  columns, backfill data and create constraints on databases whose tables predate a model
  change, and do nothing where the change is already present.

Treat the generated files under `<app>/migrations/` on a production host as part of the
database: never delete them (`reset_db` does), and back them up with the database. The design
is explained in [Schema migrations](../architecture/schema-migrations.md).

## First deploy

Run from the repository root with `DJANGO_ENVIRONMENT=production` exported and the other
variables in `.env` or the environment:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations          # generates the local apps' initial migrations
python manage.py migrate                 # creates tables; tg_schema migrations find nothing to do
python manage.py collectstatic --noinput
python manage.py populate_gamedata       # reference data, see below
python manage.py createsuperuser
python manage.py check --deploy
```

Then start the ASGI server under your process manager.

Do not use [`setup_db.sh`](../../setup_db.sh) on a production host. It starts with
`reset_db --yes`, which deletes `db.sqlite3` and every generated migration file; `reset_db` refuses to
run when `DEBUG` is `False`, so under production settings the script fails at its first step.

## Updating

[`update.sh`](../../update.sh) is the repository's update procedure:

```bash
git pull
python manage.py makemigrations
python manage.py migrate
yes yes | python manage.py collectstatic
```

`makemigrations` generates the host's migrations for any model changes in the pulled code, and
may stop to ask a question (for example about a renamed field or a new non-nullable field);
`update.sh` runs it interactively for that reason. `yes yes |` answers `collectstatic`'s
overwrite prompt.

The script does not back up, install dependencies or restart anything. A complete update is:

1. Back up the database, `media/` and the generated migration files
   ([Maintenance](maintenance.md#backups)).
2. `git pull`
3. `pip install -r requirements.txt` if `requirements.txt` changed.
4. `python manage.py makemigrations`, then `python manage.py migrate`.
5. `python manage.py collectstatic --noinput`
6. `python manage.py populate_gamedata` if reference data under `populate_db/` changed.
7. Restart every ASGI process.
8. Load a page and open a scene to confirm HTTP and WebSockets work.

[Maintenance](maintenance.md#releasing-a-schema-change) gives the order of operations for a
release that changes the schema.

## Loading game data

`python manage.py populate_gamedata` executes every `.py` script under
[`populate_db/`](../../populate_db/) (top-level files first, then `core/`, then other
directories alphabetically), each in its own transaction. The scripts create reference data
(books, abilities, clans, spheres, templates and so on) with `get_or_create`, so re-running is
safe for unchanged data. A failing script is reported and logged and the rest continue; the
command then exits with an error. Options (`--gameline`, `--only`,
`--skip`, `--dry-run`, `--verbose`) are in the
[management commands reference](../reference/management-commands.md), and the data itself in
[Seed data](../getting-started/seed-data.md).

## Pre-deploy checklist

- [ ] `DJANGO_ENVIRONMENT=production` is set in the server process's environment or `.env`.
- [ ] `SECRET_KEY` is a new random value (generate one with
      `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`).
- [ ] `DJANGO_ALLOWED_HOSTS` lists every public host name; `CSRF_TRUSTED_ORIGINS` is set if the
      public origin differs from the proxied host.
- [ ] `REDIS_URL` points at a reachable Redis that is not exposed to the internet.
- [ ] `EMAIL_BACKEND` and SMTP variables are set, so password resets are delivered.
- [ ] `ADMIN_EMAILS` lists who should receive error email, and `SERVER_EMAIL` is a sender the
      mail server accepts (see
      [Logging and monitoring](logging-and-monitoring.md#admins-and-error-email)).
- [ ] The proxy sets `X-Forwarded-Proto`, preserves `Host` and `Origin`, upgrades `/ws/`, serves
      `/static/` and `/media/`, and caps upload size.
- [ ] You understand HSTS preload before leaving `SECURE_HSTS_PRELOAD` and
      `SECURE_HSTS_INCLUDE_SUBDOMAINS` at `True` ([Security](security.md#https-and-hsts)).
- [ ] `logs/` exists and is writable: the file handlers open their files when settings load, and
      Django will not start without them.
- [ ] `python manage.py check --deploy` under the production environment reports no errors.
      It loads the template engines, so it also catches template configuration errors that
      would otherwise appear only on the first page render.
- [ ] `collectstatic` has run for this release, and the database, `media/` and generated
      migrations are backed up.

## See also

- [Security](security.md)
- [Logging and monitoring](logging-and-monitoring.md)
- [Maintenance](maintenance.md)
- [Configuration](../getting-started/configuration.md)
- [Settings reference](../reference/settings.md)
- [`tg/` project package](../../tg/README.md)
