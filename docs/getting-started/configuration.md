# Configuration

This page explains how Tellurium Games is configured: which settings module loads, how
environment variables and the `.env` file feed it, every variable the code reads, and
what a production deployment must set. It is for developers setting up a machine and for
whoever deploys the site. The value of every individual setting is listed in the
[Settings reference](../reference/settings.md).

## How configuration works

Configuration is plain Django settings in the [`tg/settings/`](../../tg/settings/)
package, with a small number of values taken from environment variables.

1. `manage.py`, [`tg/asgi.py`](../../tg/asgi.py) and [`tg/wsgi.py`](../../tg/wsgi.py) set
   `DJANGO_SETTINGS_MODULE` to `tg.settings` unless it is already set.
2. [`tg/settings/__init__.py`](../../tg/settings/__init__.py) first calls
   `load_dotenv()` on the `.env` file at the repository root, which copies its variables
   into `os.environ`.
3. It then reads `DJANGO_ENVIRONMENT` (default `development`, compared lower-case) and
   star-imports `development.py` or `production.py`. Any other value, including an empty
   string, raises `ValueError`, so a typo stops the process instead of silently running
   the wrong configuration.
4. Both environment modules begin with `from .base import *`, which defines the shared
   settings, and then override what differs, reading their own variables from
   `os.environ`.

Because `.env` is loaded before anything is read, it can supply every variable,
`DJANGO_ENVIRONMENT` and production secrets included. `load_dotenv()` does not override
variables that are already set, so a value in the real environment (shell, service unit,
container definition) wins over the same line in `.env`. The path is fixed to the
repository root, so the file is found whatever the working directory. It is listed in
[`.gitignore`](../../.gitignore).

Boolean variables are compared with the exact string `"True"`: `True` enables,
anything else (`true`, `1`, `yes`) disables.

## Environment variables read by the settings

### Selection

| Variable | Read in | Default | Purpose |
|----------|---------|---------|---------|
| `DJANGO_SETTINGS_MODULE` | `manage.py`, `tg/asgi.py`, `tg/wsgi.py` | `tg.settings` | Standard Django variable. Leave it at the default and use `DJANGO_ENVIRONMENT`. |
| `DJANGO_ENVIRONMENT` | `tg/settings/__init__.py` | `development` | `development` or `production`. May be set in `.env`. |

### Core

| Variable | Read in | Default | Purpose |
|----------|---------|---------|---------|
| `SECRET_KEY` | `development.py`, `production.py` | development: a fixed insecure key; production: none, required | `SECRET_KEY`. In production a missing or empty key stops startup with `ImproperlyConfigured`. |
| `DJANGO_ALLOWED_HOSTS` | `development.py`, `production.py` | development: `localhost,127.0.0.1`; production: none, required | Comma-separated `ALLOWED_HOSTS`; spaces around entries are trimmed and empty entries dropped. Production raises `ValueError` if no host is left. It also governs the websocket origin check. |

### E-mail (all environments)

Read in `base.py`. Development then forces
`EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"`, so in development
mail always prints to the console whatever these say.

| Variable | Default | Purpose |
|----------|---------|---------|
| `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` | Mail backend. In production, leaving it unset means password-reset mail is printed to the server's stdout, not sent. |
| `EMAIL_HOST` | `localhost` | SMTP host. |
| `EMAIL_PORT` | `25` | SMTP port (integer). |
| `EMAIL_USE_TLS` | `False` | STARTTLS. |
| `EMAIL_USE_SSL` | `False` | Implicit TLS. Do not enable together with `EMAIL_USE_TLS`. |
| `EMAIL_HOST_USER` | empty | SMTP user name. |
| `EMAIL_HOST_PASSWORD` | empty | SMTP password. |
| `EMAIL_TIMEOUT` | `30` | Seconds (integer). |
| `DEFAULT_FROM_EMAIL` | `noreply@tellurian-games.com` | Sender of password-reset and other site mail. |
| `SERVER_EMAIL` | value of `DEFAULT_FROM_EMAIL` | Sender of error mail to `ADMINS`. |
| `PASSWORD_RESET_TIMEOUT` | `3600` | Lifetime of password-reset links, in seconds (integer). |

### Log-in throttle (all environments)

Read in `base.py`; see [Authentication flows](../../accounts/docs/authentication.md#throttling).

| Variable | Default | Purpose |
|----------|---------|---------|
| `AUTH_THROTTLE_LIMIT` | `10` | POSTs to log in, sign up or password reset allowed per client address (and username or email) per window; the next ones get `429`. |
| `AUTH_THROTTLE_WINDOW` | `300` | Length of the throttle window, in seconds. |

### Production only

Read in `production.py`; ignored in development.

| Variable | Default | Purpose |
|----------|---------|---------|
| `REDIS_URL` | cache: `redis://127.0.0.1:6379/1`; channel layer: `redis://127.0.0.1:6379/0` | Redis for the cache (and therefore sessions) and for the Channels layer. When set, **both** use the same URL and database number. |
| `SECURE_SSL_REDIRECT` | `True` | Redirect HTTP to HTTPS. |
| `SECURE_HSTS_SECONDS` | `31536000` | HSTS max-age (integer). `0` disables HSTS. |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `True` | HSTS `includeSubDomains`. |
| `SECURE_HSTS_PRELOAD` | `True` | HSTS `preload`. |
| `CSRF_TRUSTED_ORIGINS` | empty list | Comma-separated origins including the scheme, such as `https://example.com`. |
| `SESSION_COOKIE_AGE` | `1209600` (two weeks) | Session lifetime in seconds (integer). |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | `False` | End the session when the browser closes. |
| `DB_CONN_MAX_AGE` | `600` | `CONN_MAX_AGE` for the default database, in seconds (integer). |
| `ADMIN_EMAILS` | empty | Comma-separated addresses, each plain (`a@example.com`) or named (`Jane Doe <jane@example.com>`). Builds `ADMINS` (a plain address is named `Admin`), who receive an email for every unhandled request error; `MANAGERS` is the same list. |

### Development only

Read in `development.py`; ignored in production.

| Variable | Default | Purpose |
|----------|---------|---------|
| `DJANGO_LOG_SQL` | `False` | `True` prints every SQL query to the console (`django.db.backends` at `DEBUG`). |

### Used by tests and scripts, not by the settings

| Variable | Read in | Purpose |
|----------|---------|---------|
| `TG_BROWSER_BINARY` | browser tests | Path to a Chromium binary. See [Testing](../development/testing.md#browser-tests). |
| `TG_SCREENSHOT_DB` | [`scripts/screenshot_settings.py`](../../scripts/screenshot_settings.py) | SQLite path for `scripts/template_screenshots.py` (default `/tmp/tg-screenshots.sqlite3`). The script sets it itself. |
| `MOZ_HEADLESS`, `DJANGO_ALLOW_ASYNC_UNSAFE` | set by tests | Set by the Selenium and Playwright test modules for their own run; you do not set them. |

## `.env.example`

[`.env.example`](../../.env.example) is a template: copy it to `.env` and edit. Its
entries match the tables above; a few need a note:

| Entry | What actually happens |
|-------|-----------------------|
| `DJANGO_ENVIRONMENT=development` | Selects the settings module; `DEBUG` follows it (`True` in `development.py`, always `False` in `production.py`). There is no separate debug variable. |
| `SECRET_KEY=django-insecure-...` | Overrides the development fallback key with another insecure one. Harmless in development; replace it in production. |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_SSLMODE` (commented out) | Read only by the PostgreSQL and MySQL examples that are commented out in `production.py`. The active configuration is SQLite. |
| `AWS_*`, `MAILGUN_*` (commented out) | Nothing reads them; the packages they refer to are not in `requirements.txt`. |
| `MOZ_HEADLESS` (commented out) | Set by the test module that needs it. |

## What production must set

With `DJANGO_ENVIRONMENT=production`:

| Must set | Why |
|----------|-----|
| `DJANGO_ENVIRONMENT=production` (environment or `.env`) | Otherwise development settings load, with `DEBUG = True`. |
| `SECRET_KEY` | Startup fails without it. |
| `DJANGO_ALLOWED_HOSTS` | Startup fails without it. |
| `REDIS_URL` (or a Redis server at `127.0.0.1:6379`) | Cache, sessions and the websocket channel layer. The cache ignores Redis errors (`IGNORE_EXCEPTIONS`), so a missing Redis does not crash pages, but sessions cannot be stored and live chat cannot broadcast. |
| `EMAIL_BACKEND` and the SMTP variables | The default console backend never delivers password-reset mail. |
| `CSRF_TRUSTED_ORIGINS` | Needed when requests arrive from an origin Django does not see as its own, such as behind a proxy that changes the host or scheme. |
| An `X-Forwarded-Proto: https` header from the proxy | `SECURE_PROXY_SSL_HEADER` is fixed to it. Without it, with `SECURE_SSL_REDIRECT` on, every request looks like plain HTTP and is redirected. |

Production also needs `collectstatic` run before start (the settings use
`ManifestStaticFilesStorage`) and a writable `logs/` directory. Deployment steps are in
[Deployment](../operations/deployment.md).

## Project-specific settings

Beyond Django's own settings the code reads:

| Setting | Defined in | Read by | Purpose |
|---------|-----------|---------|---------|
| `GAMELINES` | `base.py` | many modules (`settings.GAMELINES`) | Code → name, short label and app name for each gameline. |
| `GAMELINE_CHOICES` | `base.py` | `gameline` fields in `core/models.py`, `core.validators`, views | `[(code, name), ...]` built from `GAMELINES`. |
| `CHARGEN_PARTIAL_LIMIT` | not defined; defaults to `60` | `characters.views.core.chargen_mixins` | Per-user, per-character, per-minute cap on character-creation htmx partial requests. Tests override it. |

Use them rather than hard-coded strings:

```python
from django.conf import settings

name = settings.GAMELINES.get("vtm", {}).get("name", "vtm")  # "Vampire: the Masquerade"
gameline = models.CharField(max_length=3, choices=settings.GAMELINE_CHOICES, default="wod")
```

Details and the remaining settings are in the [Settings reference](../reference/settings.md).

## See also

- [Settings reference](../reference/settings.md)
- [Local development](local-development.md)
- [Installation](installation.md)
- [Deployment](../operations/deployment.md)
- [Security operations](../operations/security.md)
