# Settings reference

This page lists the project's own settings and every Django setting the project sets,
with the module that sets it, its value or default, the environment variable that feeds
it, and what it is for. Where development and production differ, both values are
given. It is a lookup table; how the modules are chosen and loaded is explained in
[Configuration](../getting-started/configuration.md).

Modules, all in [`tg/settings/`](../../tg/settings/):

| Module | Role |
|--------|------|
| [`__init__.py`](../../tg/settings/__init__.py) | Calls `load_dotenv()` on the repository's `.env`, then star-imports `development` or `production` according to `DJANGO_ENVIRONMENT`. |
| [`base.py`](../../tg/settings/base.py) | Shared settings. |
| [`development.py`](../../tg/settings/development.py) | `from .base import *`, then development overrides. |
| [`production.py`](../../tg/settings/production.py) | `from .base import *`, then production overrides. |

In the tables, "base" means the value holds in both environments unless a later row or
column overrides it. "Django default" means the project does not set it.

## Project settings

| Setting | Module | Value | Purpose |
|---------|--------|-------|---------|
| `GAMELINES` | base | dict, below | The gamelines the site knows: code → `name`, `short`, `app_name`. Read throughout the code as `settings.GAMELINES`. |
| `GAMELINE_CHOICES` | base | `[(code, GAMELINES[code]["name"]), ...]` in `GAMELINES` order | Choices for `gameline` model fields and validation (`core.validators`). |
| `CHARGEN_PARTIAL_LIMIT` | not set; default `60` via `getattr` | integer | Maximum character-creation htmx partial requests per user, per character, per minute (`characters.views.core.chargen_mixins`); requests over the limit get an empty 204. Tests override it. |
| `TINYMCE_DEFAULT_CONFIG` | base | editor options dict | Defined for django-tinymce, but `tinymce` is not in `INSTALLED_APPS` and no code reads it. |

`GAMELINES`:

| Code | `name` | `short` | `app_name` |
|------|--------|---------|------------|
| `wod` | World of Darkness | (empty) | `wod` |
| `vtm` | Vampire: the Masquerade | VtM | `vampire` |
| `wta` | Werewolf: the Apocalypse | WtA | `werewolf` |
| `mta` | Mage: the Ascension | MtA | `mage` |
| `wto` | Wraith: the Oblivion | WtO | `wraith` |
| `ctd` | Changeling: the Dreaming | CtD | `changeling` |
| `dtf` | Demon: the Fallen | DtF | `demon` |
| `mtr` | Mummy: the Resurrection | MtR | `mummy` |
| `htr` | Hunter: the Reckoning | HtR | `hunter` |
| `orp` | Orpheus | Orp | `orpheus` |

```python
from django.conf import settings

settings.GAMELINES["mta"]["name"]          # "Mage: the Ascension"
settings.GAMELINES.get(code, {}).get("short", code)
```

## Core

| Setting | Development | Production | Env var | Purpose |
|---------|-------------|------------|---------|---------|
| `SECRET_KEY` | env, else a fixed `django-insecure-...` key | env, required (`KeyError` if missing) | `SECRET_KEY` | Signing key. |
| `DEBUG` | `True` | `False` | none | Debug mode. Not configurable by environment variable. |
| `ALLOWED_HOSTS` | env split on `,`, default `localhost,127.0.0.1` | env split on `,`, required (`ValueError` if empty) | `DJANGO_ALLOWED_HOSTS` | Accepted `Host` headers; also the websocket origin allow-list. `[::1]` is deliberately absent in development. |
| `DEBUG_PROPAGATE_EXCEPTIONS` | `False` | Django default (`False`) | none | |
| `INSTALLED_APPS` | base + `debug_toolbar` (if importable) | base | none | Base order: `daphne`, the `django.contrib` apps (`admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles`), `channels`, `accounts`, `characters`, `game`, `tg_schema`, `items`, `locations`, `polymorphic`, `core`, `widgets`, `django.contrib.humanize`. `daphne` must precede `staticfiles` so its `runserver` wins. |
| `MIDDLEWARE` | `DebugToolbarMiddleware` + base | base | none | Base order: `SecurityMiddleware`, `SessionMiddleware`, `CommonMiddleware`, `CsrfViewMiddleware`, `AuthenticationMiddleware`, `core.middleware.authorization.AuthorizationMiddleware`, `MessageMiddleware`, `XFrameOptionsMiddleware`, `core.middleware.auth_error_handler.AuthErrorHandlerMiddleware`. See [Authorization](../architecture/authorization.md). |
| `ROOT_URLCONF` | `tg.urls` | same | none | See [URLs](urls.md). |
| `WSGI_APPLICATION` | `tg.wsgi.application` | same | none | |
| `ASGI_APPLICATION` | `tg.asgi.application` | same | none | HTTP plus websockets; used by Daphne. |
| `TEST_RUNNER` | `tg.test_runner.LocalMigrationTestRunner` | same | none | See [Testing](../development/testing.md). |
| `DEFAULT_AUTO_FIELD` | `django.db.models.BigAutoField` | same | none | |

## Templates

| Key | Development | Production |
|-----|-------------|------------|
| `BACKEND` | `DjangoTemplates` | same |
| `DIRS` | `[]` | same |
| `APP_DIRS` | `True` | `True` (from base) |
| `OPTIONS["context_processors"]` | `debug`, `request`, `auth`, `messages`, `core.context_processors.all_chronicles`, `accounts.context_processors.theme_context`, `accounts.context_processors.notification_count` | same |
| `OPTIONS["loaders"]` | not set (Django chooses) | `cached.Loader` wrapping `filesystem.Loader` and `app_directories.Loader`, set in a `if not DEBUG:` block at the end of `production.py` |

Templates live in each app's `templates/` directory; there are no project-level template
directories.

## Database

| Setting | Development | Production | Env var |
|---------|-------------|------------|---------|
| `DATABASES["default"]["ENGINE"]` | `django.db.backends.sqlite3` | same | none |
| `DATABASES["default"]["NAME"]` | `BASE_DIR / "db.sqlite3"` | same | none |
| `DATABASES["default"]["TEST"]["NAME"]` | `BASE_DIR / "db_test.sqlite3"` | same | none |
| `DATABASES["default"]["ATOMIC_REQUESTS"]` | `True`: every request runs in one transaction | same | none |
| `DATABASES["default"]["CONN_MAX_AGE"]` | Django default (`0`) | `600` | `DB_CONN_MAX_AGE` |

`production.py` contains commented-out PostgreSQL and MySQL `DATABASES` blocks that read
`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` and `DB_SSLMODE`; they are not
active. `BASE_DIR` is the repository root.

## Uploads

| Setting | Value (both) | Purpose |
|---------|--------------|---------|
| `DATA_UPLOAD_MAX_MEMORY_SIZE` | `5 * 1024 * 1024` (5 MB) | Maximum request body, excluding file uploads. |
| `FILE_UPLOAD_MAX_MEMORY_SIZE` | `5 * 1024 * 1024` (5 MB) | Uploads above this are streamed to a temporary file. |

## Authentication and passwords

| Setting | Value (both) | Env var | Purpose |
|---------|--------------|---------|---------|
| `AUTH_PASSWORD_VALIDATORS` | Django's four: user-attribute similarity, minimum length, common password, numeric | none | |
| `LOGIN_URL` | `"login"` | none | URL name of the login view (from `django.contrib.auth.urls`, mounted under `accounts/`). |
| `LOGIN_REDIRECT_URL` | `"core:home"` | none | |
| `LOGOUT_REDIRECT_URL` | `"core:home"` | none | |
| `PASSWORD_RESET_TIMEOUT` | `3600` (one hour) | `PASSWORD_RESET_TIMEOUT` | Lifetime of password-reset links in seconds. |

## Internationalisation

| Setting | Value (both) |
|---------|--------------|
| `LANGUAGE_CODE` | `en-us` |
| `TIME_ZONE` | `America/Los_Angeles` |
| `USE_I18N` | `True` |
| `USE_TZ` | `True` |

## Static and media files

| Setting | Development | Production | Purpose |
|---------|-------------|------------|---------|
| `STATIC_URL` | `static/` | same | |
| `STATIC_ROOT` | `BASE_DIR / "collected_static"` | same | Where `collectstatic` copies files. Gitignored. |
| `STATICFILES_DIRS` | `[BASE_DIR / "source_static"]` | same | Site-wide assets and vendored libraries; app assets come from `<app>/static/`. |
| `STORAGES` | Django default | `default`: `FileSystemStorage`; `staticfiles`: `ManifestStaticFilesStorage` | Production serves content-hashed file names and needs `collectstatic` before start. |
| `MEDIA_ROOT` | `BASE_DIR / "media"` | same | Uploaded images. `media/*` is gitignored. |
| `MEDIA_URL` | `/media/` | same | [`tg/urls.py`](../../tg/urls.py) appends `static(MEDIA_URL, document_root=MEDIA_ROOT)`, which Django only routes when `DEBUG` is true; in production the web server must serve `/media/`. |

## Cache and sessions

| Setting | Development | Production | Env var |
|---------|-------------|------------|---------|
| `CACHES["default"]["BACKEND"]` | `django.core.cache.backends.locmem.LocMemCache` | `django_redis.cache.RedisCache` | none |
| `CACHES["default"]["LOCATION"]` | `unique-snowflake` | env, default `redis://127.0.0.1:6379/1` | `REDIS_URL` |
| `CACHES["default"]["TIMEOUT"]` | `300` | `300` | none |
| `CACHES["default"]["OPTIONS"]` | `MAX_ENTRIES: 1000` | django-redis `DefaultClient`; pool `max_connections: 50`, `retry_on_timeout: True`; `SOCKET_CONNECT_TIMEOUT: 5`, `SOCKET_TIMEOUT: 5`; zlib compressor; `IGNORE_EXCEPTIONS: True` (cache errors are swallowed) | none |
| `CACHES["default"]["KEY_PREFIX"]` | none | `tg` | none |
| `SESSION_ENGINE` | Django default (database) | `django.contrib.sessions.backends.cache` | none |
| `SESSION_CACHE_ALIAS` | Django default | `default` | none |
| `SESSION_COOKIE_NAME` | Django default (`sessionid`) | `sessionid` | none |
| `SESSION_COOKIE_AGE` | Django default (two weeks) | env, default `1209600` | `SESSION_COOKIE_AGE` |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | Django default (`False`) | env `== "True"`, default `False` | `SESSION_EXPIRE_AT_BROWSER_CLOSE` |
| `SESSION_COOKIE_SECURE` | Django default (`False`) | `True` | none |
| `SESSION_COOKIE_HTTPONLY` | Django default (`True`) | `True` | none |
| `SESSION_COOKIE_SAMESITE` | Django default (`Lax`) | `Lax` | none |

How the site uses the cache is in [Caching](../architecture/caching.md).
`core.cache` reads `SESSION_COOKIE_NAME` to tell anonymous visitors from signed-in ones.

## Channels

| Setting | Development | Production | Env var |
|---------|-------------|------------|---------|
| `CHANNEL_LAYERS["default"]["BACKEND"]` | `channels.layers.InMemoryChannelLayer` (from base) | `channels_redis.core.RedisChannelLayer` | none |
| `CHANNEL_LAYERS["default"]["CONFIG"]` | none | `hosts: [REDIS_URL or "redis://127.0.0.1:6379/0"]`, `capacity: 1500`, `expiry: 10` | `REDIS_URL` |

The in-memory layer works only within one process. When `REDIS_URL` is set, the cache
and the channel layer share the same Redis database. See
[Scenes and real-time chat](../architecture/scenes-and-realtime.md).

## Security (production)

Development sets none of these, so Django's defaults apply there.

| Setting | Production value | Env var |
|---------|------------------|---------|
| `SECURE_SSL_REDIRECT` | env `== "True"`, default `True` | `SECURE_SSL_REDIRECT` |
| `SECURE_PROXY_SSL_HEADER` | `("HTTP_X_FORWARDED_PROTO", "https")` | none |
| `SECURE_HSTS_SECONDS` | env, default `31536000` | `SECURE_HSTS_SECONDS` |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | env `== "True"`, default `True` | `SECURE_HSTS_INCLUDE_SUBDOMAINS` |
| `SECURE_HSTS_PRELOAD` | env `== "True"`, default `True` | `SECURE_HSTS_PRELOAD` |
| `SECURE_CONTENT_TYPE_NOSNIFF` | `True` | none |
| `SECURE_REFERRER_POLICY` | `same-origin` | none |
| `X_FRAME_OPTIONS` | `DENY` | none |
| `CSRF_COOKIE_SECURE` | `True` | none |
| `CSRF_COOKIE_HTTPONLY` | `False`, so page JavaScript can read the token | none |
| `CSRF_COOKIE_SAMESITE` | `Strict` | none |
| `CSRF_COOKIE_NAME` | `csrftoken` | none |
| `CSRF_TRUSTED_ORIGINS` | env split on `,`; empty list when unset | `CSRF_TRUSTED_ORIGINS` |

`SECURE_BROWSER_XSS_FILTER` is deliberately not set;
`core.tests.test_settings` checks that it stays unset or false. More on the security
posture in [Security operations](../operations/security.md).

## E-mail

| Setting | Development | Production | Env var |
|---------|-------------|------------|---------|
| `EMAIL_BACKEND` | always `django.core.mail.backends.console.EmailBackend` | env, default console backend | `EMAIL_BACKEND` |
| `EMAIL_HOST` | env, default `localhost` | same | `EMAIL_HOST` |
| `EMAIL_PORT` | env, default `25` | same | `EMAIL_PORT` |
| `EMAIL_USE_TLS` | env `== "True"`, default `False` | same | `EMAIL_USE_TLS` |
| `EMAIL_USE_SSL` | env `== "True"`, default `False` | same | `EMAIL_USE_SSL` |
| `EMAIL_HOST_USER` | env, default empty | same | `EMAIL_HOST_USER` |
| `EMAIL_HOST_PASSWORD` | env, default empty | same | `EMAIL_HOST_PASSWORD` |
| `EMAIL_TIMEOUT` | env, default `30` | same | `EMAIL_TIMEOUT` |
| `DEFAULT_FROM_EMAIL` | env, default `noreply@tellurian-games.com` | same | `DEFAULT_FROM_EMAIL` |
| `SERVER_EMAIL` | env, default `DEFAULT_FROM_EMAIL` | same | `SERVER_EMAIL` |
| `ADMINS` | Django default (empty) | `("Admin", address)` per comma-separated address | `ADMIN_EMAILS` |
| `MANAGERS` | Django default (empty) | same list as `ADMINS` | `ADMIN_EMAILS` |

## Logging

`LOGGING` is defined in `base.py` and edited in place by both environment modules.

Formatters: `simple` (`[LEVEL] logger - message`), `verbose` (adds time, module,
function and line), `detailed` (adds process, thread and path). Filters:
`require_debug_true`, `require_debug_false`.

Handlers:

| Handler | Development | Production |
|---------|-------------|------------|
| `console` | `StreamHandler`, `INFO`, `simple` | same |
| `console_debug` | `StreamHandler`, `INFO`, `verbose`, only when `DEBUG` | defined, never emits (`DEBUG` is false) |
| `file` | `FileHandler`, `DEBUG`, `logs/debug.log`, `verbose` | `RotatingFileHandler`, `INFO`, `logs/app.log`, 10 MB × 10 |
| `error_file` | `FileHandler`, `ERROR`, `logs/error.log`, `detailed` | `RotatingFileHandler`, `ERROR`, `logs/error.log`, 10 MB × 10 |
| `warning_file` | `FileHandler`, `WARNING`, `logs/warning.log`, `verbose` | `RotatingFileHandler`, `WARNING`, `logs/warning.log`, 5 MB × 5 |
| `null` | `NullHandler` | same |

Loggers (`propagate` is `False` for all):

| Logger | Handlers | Development level | Production level |
|--------|----------|-------------------|------------------|
| `django` | `console`, `file` | `INFO` | `WARNING` |
| `django.request` | `error_file`, `console` | `ERROR` | `ERROR` |
| `django.security` | `error_file`, `console` | `WARNING` | `WARNING` |
| `django.template` | `console` | `INFO` | `INFO` |
| `django.db.backends` | development: `console_debug`; production: `null` | `DEBUG` | `INFO` |
| `tg`, `accounts`, `characters`, `game`, `items`, `locations`, `core` | `console`, `file`, `error_file`, plus `console_debug` in development and `warning_file` in production | `DEBUG` | `INFO` |

Every file handler opens its file when settings load, so the `logs/` directory must
exist and be writable. Operating the logs is covered in
[Logging and monitoring](../operations/logging-and-monitoring.md).

## Debug toolbar (development only)

Set only when `import debug_toolbar` succeeds.

| Setting | Value |
|---------|-------|
| `INTERNAL_IPS` | `["127.0.0.1", "::1"]` |
| `DEBUG_TOOLBAR_CONFIG["SHOW_TOOLBAR_CALLBACK"]` | `"tg.settings.development.show_toolbar_callback"`: signed-in staff or superusers only |
| `DEBUG_TOOLBAR_CONFIG["IS_RUNNING_TESTS"]` | `False` |

## See also

- [Configuration](../getting-started/configuration.md)
- [Local development](../getting-started/local-development.md)
- [Deployment](../operations/deployment.md)
- [Caching](../architecture/caching.md)
- [Logging and monitoring](../operations/logging-and-monitoring.md)
- [`tg/` project package](../../tg/README.md)
