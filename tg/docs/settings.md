# Settings modules

This page explains how the project's Django settings are organised: how the settings
module is chosen, what `base.py`, `development.py` and `production.py` each set, which
environment variables they read, and the behaviours that commonly cause surprises. It is for
developers running the project and operators deploying it. The complete table of
settings and variables is the [settings reference](../../docs/reference/settings.md).

## How the module is chosen

Every entry point sets `DJANGO_SETTINGS_MODULE=tg.settings` if it is not already set
(`manage.py`, `tg/asgi.py`, `tg/wsgi.py`). `tg.settings` is a package whose
[`__init__.py`](../settings/__init__.py) loads the `.env` file, then reads
`DJANGO_ENVIRONMENT`, lower-cases it and:

| `DJANGO_ENVIRONMENT` | Result |
|----------------------|--------|
| unset or `development` | `from .development import *` |
| `production` | `from .production import *` |
| anything else | `ValueError("Unknown DJANGO_ENVIRONMENT value: ...")` at startup |

Both environment modules begin with `from .base import *` and then override or extend
what they need.

```bash
export DJANGO_ENVIRONMENT=production   # or a DJANGO_ENVIRONMENT=production line in .env
```

### `.env` files

[`__init__.py`](../settings/__init__.py) calls `python-dotenv`'s `load_dotenv()` on the
`.env` file at the repository root (see [`.env.example`](../../.env.example)) before it
reads anything, so every variable, `DJANGO_ENVIRONMENT` included, may be set there. It
does not override variables that are already set, so the real environment wins over
`.env`.

## `base.py`

Settings shared by both environments. The main groups:

| Group | Settings |
|-------|----------|
| Paths | `BASE_DIR` (the repository root) |
| Apps | `INSTALLED_APPS`: `daphne` first (its `runserver` serves ASGI), Django contrib apps, `channels`, the project apps, `polymorphic`, `django.contrib.humanize` |
| Request pipeline | `MIDDLEWARE` including `core.middleware.authorization.AuthorizationMiddleware` right after `AuthenticationMiddleware` and `core.middleware.auth_error_handler.AuthErrorHandlerMiddleware` last; `ROOT_URLCONF = "tg.urls"`; `WSGI_APPLICATION`, `ASGI_APPLICATION` |
| Templates | `DjangoTemplates` with `APP_DIRS = True` and the context processors `core.context_processors.all_chronicles`, `accounts.context_processors.theme_context`, `accounts.context_processors.notification_count` |
| Database | SQLite at `BASE_DIR / "db.sqlite3"`, test database `db_test.sqlite3`, `ATOMIC_REQUESTS = True` (each request runs in a transaction) |
| Uploads | `DATA_UPLOAD_MAX_MEMORY_SIZE` and `FILE_UPLOAD_MAX_MEMORY_SIZE` 5 MB |
| Static and media | `STATIC_URL = "static/"`, `STATIC_ROOT = collected_static/`, `STATICFILES_DIRS = [source_static/]`, `MEDIA_ROOT = media/`, `MEDIA_URL = "/media/"` |
| Auth | `LOGIN_URL = "login"`, `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` `"core:home"`, four password validators, `PASSWORD_RESET_TIMEOUT` (default 3600 s), `AUTH_THROTTLE_LIMIT` / `AUTH_THROTTLE_WINDOW` (10 posts per 300 s to log in, sign up, password reset) |
| E-mail | `EMAIL_BACKEND` (default console), `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_TIMEOUT`, `DEFAULT_FROM_EMAIL`, `SERVER_EMAIL`, all from the environment |
| Gamelines | `GAMELINES` (code to `name`, `short`, `app_name` for `wod`, `vtm`, `wta`, `mta`, `wto`, `ctd`, `dtf`, `mtr`, `htr`, `orp`) and `GAMELINE_CHOICES` built from it |
| Logging | Formatters, handlers writing to `logs/debug.log`, `logs/error.log`, `logs/warning.log`, and loggers for Django and each project app |
| Channels | `CHANNEL_LAYERS` with `InMemoryChannelLayer` |
| Tests | `TEST_RUNNER = "tg.test_runner.LocalMigrationTestRunner"` |
| Other | `LANGUAGE_CODE = "en-us"`, `TIME_ZONE = "America/Los_Angeles"`, `USE_TZ = True`, `DEFAULT_AUTO_FIELD = BigAutoField`, `TINYMCE_DEFAULT_CONFIG` (no installed app reads it) |

`base.py` sets no `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` or `CACHES`; the environment
modules do.

Read gameline data from settings rather than hard-coding it:

```python
from django.conf import settings

name = settings.GAMELINES.get(code, {}).get("name", code)
gameline = models.CharField(max_length=3, choices=settings.GAMELINE_CHOICES, default="wod")
```

## `development.py`

- `SECRET_KEY` from the environment, with an insecure fallback.
- `DEBUG = True`; `ALLOWED_HOSTS` from `DJANGO_ALLOWED_HOSTS` (default
  `localhost,127.0.0.1`).
- `EMAIL_BACKEND` forced to the console backend, whatever the environment says.
- If `debug_toolbar` can be imported: adds it to `INSTALLED_APPS` and its middleware
  first, sets `INTERNAL_IPS`, and shows the toolbar only to signed-in staff or superusers
  (`show_toolbar_callback`).
- Logging: project loggers at `DEBUG` with the verbose console handler; SQL queries
  (`django.db.backends`) to the console only when `DJANGO_LOG_SQL=True`.
- `CACHES`: `LocMemCache`, 5-minute default timeout, 1000 entries.

## `production.py`

- `SECRET_KEY` from the environment: a missing or empty key fails with
  `ImproperlyConfigured` at startup.
- `DEBUG = False`; `DJANGO_ALLOWED_HOSTS` is required (else `ValueError`). Comma-separated
  lists (`DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `ADMIN_EMAILS`) are split with
  `env_list()` from `base.py`, which trims spaces and drops empty items.
- HTTPS: `SECURE_SSL_REDIRECT` (default on), `SECURE_PROXY_SSL_HEADER` for
  `X-Forwarded-Proto`, HSTS (`SECURE_HSTS_SECONDS` default one year, subdomains and
  preload on by default), secure session and CSRF cookies, `X_FRAME_OPTIONS = "DENY"`,
  `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_REFERRER_POLICY = "same-origin"`.
- CSRF: `CSRF_COOKIE_SAMESITE = "Strict"`, `CSRF_TRUSTED_ORIGINS` from the environment.
- Sessions: stored in the cache (`SESSION_ENGINE = "django.contrib.sessions.backends.cache"`),
  `SESSION_COOKIE_AGE` (default two weeks), `SESSION_EXPIRE_AT_BROWSER_CLOSE`.
- Database: the base SQLite database with `CONN_MAX_AGE` from `DB_CONN_MAX_AGE` (default
  600). PostgreSQL and MySQL blocks are present as comments only.
- Static files: `ManifestStaticFilesStorage` (content-hashed names; run `collectstatic`).
- Cache: Redis through `django_redis` at `REDIS_URL` (default
  `redis://127.0.0.1:6379/1`), key prefix `tg`, `IGNORE_EXCEPTIONS = True` so a Redis
  outage does not raise.
- Channel layer: `channels_redis` at `REDIS_URL` (default database 0).
- Logging: rotating files `logs/app.log`, `logs/error.log`, `logs/warning.log`; Django
  at `WARNING`, project loggers at `INFO`; a `mail_admins` handler
  (`AdminEmailHandler`, `ERROR`) on the `django` and `django.request` loggers, so
  unhandled request errors are mailed to `ADMINS`.
- `ADMINS` and `MANAGERS` from `ADMIN_EMAILS` (comma-separated). Each entry is
  `address` or `Name <address>`; a plain address becomes `("Admin", address)`.
- Template loaders: not set. With `DEBUG = False` Django wraps the filesystem and
  app-directories loaders in the cached loader itself. (Setting `loaders` beside
  `APP_DIRS = True` raises `ImproperlyConfigured`.)

The file handlers need a `logs/` directory under `BASE_DIR`.

## Environment variables

| Variable | Read by | Default |
|----------|---------|---------|
| `DJANGO_ENVIRONMENT` | `__init__.py` (after loading `.env`) | `development` |
| `SECRET_KEY` | development (optional), production (required) | insecure key in development |
| `DJANGO_ALLOWED_HOSTS` | both | `localhost,127.0.0.1` in development; required in production |
| `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_TIMEOUT`, `DEFAULT_FROM_EMAIL`, `SERVER_EMAIL`, `PASSWORD_RESET_TIMEOUT`, `AUTH_THROTTLE_LIMIT`, `AUTH_THROTTLE_WINDOW` | base | see `base.py` |
| `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`, `CSRF_TRUSTED_ORIGINS`, `SESSION_COOKIE_AGE`, `SESSION_EXPIRE_AT_BROWSER_CLOSE`, `DB_CONN_MAX_AGE`, `ADMIN_EMAILS`, `REDIS_URL` | production | see `production.py` |
| `DJANGO_LOG_SQL` | development | `False` |

Boolean variables are true only when their value is exactly `True`. The
[settings reference](../../docs/reference/settings.md) describes each one.

## See also

- [Settings reference](../../docs/reference/settings.md)
- [Configuration](../../docs/getting-started/configuration.md)
- [Deployment](../../docs/operations/deployment.md)
- [Logging and monitoring](../../docs/operations/logging-and-monitoring.md)
- [`tg/settings/`](../settings/)
