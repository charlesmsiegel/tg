# Security

This page covers the security-relevant configuration and behaviour of a running
installation: HTTPS and response headers, cookies and CSRF, authentication and sessions, how
authorization and page caching keep one user's data from another, how user-written text and
uploaded images are handled, secrets, dependency pinning, and where to report a
vulnerability. It is for operators and for developers changing any of these areas. Access
control is summarised here and specified in [Authorization](../architecture/authorization.md).

## Production security settings

All of these are set in [`tg/settings/production.py`](../../tg/settings/production.py) unless
the table says otherwise. Development ([`tg/settings/development.py`](../../tg/settings/development.py))
sets none of the HTTPS or cookie options.

| Setting | Value | Why |
|---------|-------|-----|
| `DEBUG` | `False` (hard-coded) | No debug pages or settings leaks. |
| `SECRET_KEY` | `os.environ["SECRET_KEY"]` | No default in production; startup fails without it. |
| `ALLOWED_HOSTS` | from `DJANGO_ALLOWED_HOSTS` | Host-header validation; empty raises `ValueError`. Also gates WebSocket origins. |
| `SECURE_SSL_REDIRECT` | env, default `True` | Redirect HTTP to HTTPS. |
| `SECURE_PROXY_SSL_HEADER` | `("HTTP_X_FORWARDED_PROTO", "https")` | Trust the proxy's scheme header; see [Deployment](deployment.md#reverse-proxy-requirements). |
| `SECURE_HSTS_SECONDS` | env, default `31536000` | One year of HSTS. |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | env, default `True` | |
| `SECURE_HSTS_PRELOAD` | env, default `True` | |
| `SECURE_CONTENT_TYPE_NOSNIFF` | `True` | `X-Content-Type-Options: nosniff`. |
| `SECURE_REFERRER_POLICY` | `"same-origin"` | No referrer sent to other sites. |
| `X_FRAME_OPTIONS` | `"DENY"` | With `XFrameOptionsMiddleware` (in `base.py`): no framing, against clickjacking. |
| `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` | `True` | Cookies only over HTTPS. |
| `SESSION_COOKIE_HTTPONLY` | `True` | Scripts cannot read the session cookie. |
| `SESSION_COOKIE_SAMESITE` | `"Lax"` | Session sent on top-level navigation from other sites, not on cross-site subrequests or POSTs. |
| `CSRF_COOKIE_SAMESITE` | `"Strict"` | CSRF cookie never sent on cross-site requests. |
| `CSRF_COOKIE_HTTPONLY` | `False` | See below. |
| `CSRF_TRUSTED_ORIGINS` | from env | Extra origins allowed to POST. |
| `DATA_UPLOAD_MAX_MEMORY_SIZE` | 5 MB (`base.py`) | Caps non-file request data; also the scene WebSocket message limit. |

Run `python manage.py check --deploy` with the production environment to have Django check
these; see the [deployment checklist](deployment.md#pre-deploy-checklist).

### HTTPS and HSTS

With the defaults, the first HTTPS response tells browsers to use HTTPS for the domain and all
its subdomains for a year, and marks the domain as eligible for browser preload lists. Once a
domain is on a preload list, removal is slow. Before the first production deploy, decide
whether every subdomain can serve HTTPS; if not, set `SECURE_HSTS_INCLUDE_SUBDOMAINS=False` and
`SECURE_HSTS_PRELOAD=False`, or start with a small `SECURE_HSTS_SECONDS`.

### CSRF

`CsrfViewMiddleware` is in the middleware stack ([`tg/settings/base.py`](../../tg/settings/base.py)),
so every unsafe request needs a token. Pages carry the token themselves: forms render
`{% csrf_token %}`, and htmx requests send it as a header rendered into the page, for example
`hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` in
[`characters/templates/characters/core/chargen/interactive.html`](../../characters/templates/characters/core/chargen/interactive.html).

`CSRF_COOKIE_HTTPONLY` is `False`; the comment in `production.py` says scripts must be able to
read the cookie. No script in the repository reads it, since the token is always in the page,
so the setting has no functional effect today. It is also not a weakness: the token a script
could read from the cookie is the same one it can already read from the page, which is why
Django's documentation notes that marking the CSRF cookie `HttpOnly` gives little practical
protection. Keep the cookie readable if you add JavaScript that sends the token from the cookie.

`CSRF_COOKIE_SAMESITE = "Strict"` means a visitor who arrives from another site gets a fresh
CSRF cookie on that first request; forms on the page they land on still work because the
token in the page matches the new cookie.

### Content Security Policy

The application does not send a `Content-Security-Policy` header. The front end is written so
that a strict policy is possible: vendored htmx and the Alpine.js **CSP build** are loaded
from `/static/` with `integrity` (SRI) attributes, and htmx is configured with
`allowEval: false` and `selfRequestsOnly: true`
([`core/templates/core/includes/interactive_scripts.html`](../../core/templates/core/includes/interactive_scripts.html),
versions and hashes in [`source_static/vendor/VENDOR.md`](../../source_static/vendor/VENDOR.md)).
A policy, if you add one at the proxy, needs `connect-src` to allow the site's own `wss:` origin
for scene chat.

## Authentication and sessions

- Accounts are `django.contrib.auth` users with a one-to-one `accounts.Profile`. Anyone can
  register at `accounts/signup/` (`accounts.views.SignUp`); login is
  `accounts.views.CustomLoginView` at `accounts/login/`, and password reset uses Django's
  views with the site's templates ([`tg/urls.py`](../../tg/urls.py)).
- Passwords are checked by Django's four standard validators (user-attribute similarity,
  minimum length, common passwords, all-numeric), configured in `base.py`.
- Password-reset links expire after `PASSWORD_RESET_TIMEOUT` seconds (default 3600).
- POSTs to `accounts/login/`, `accounts/signup/` and `accounts/password_reset/` are throttled
  in the cache: by default 10 per client address (and username or email) per five minutes,
  then `429` until the window ends (`AUTH_THROTTLE_LIMIT`, `AUTH_THROTTLE_WINDOW`; see
  [Authentication flows](../../accounts/docs/authentication.md#throttling)). The client
  address is only the visitor's if Daphne runs with `--proxy-headers` behind the proxy.
  There is no account lockout, and `admin/login/` is not throttled; rate-limit it at the
  proxy if the admin is exposed.
- Sessions: development uses Django's default database sessions. Production uses
  `django.contrib.sessions.backends.cache` on the Redis cache, so sessions disappear if Redis
  is flushed, restarted without persistence or unreachable (every user is logged out). Session
  lifetime is `SESSION_COOKIE_AGE` (default two weeks), optionally ending at browser close.
- An anonymous request to a login-protected view gets a 401 page instead of a login redirect,
  and a `PermissionDenied` gets a 403 page
  (`core.middleware.auth_error_handler.AuthErrorHandlerMiddleware`).
- The WebSocket route authenticates from the same session cookie through Channels'
  `AuthMiddlewareStack` ([`tg/asgi.py`](../../tg/asgi.py)).

Staff and superuser accounts are powerful beyond `/admin/`: `PermissionManager` gives them the
`ADMIN` role on every object and lets them manage every chronicle
([`core/permissions.py`](../../core/permissions.py)). Grant `is_staff` sparingly.

## Authorization

Access is checked in two layers, described fully in
[Authorization](../architecture/authorization.md):

1. **Route policy.** `core.middleware.authorization.AuthorizationMiddleware` evaluates the
   policy declared for every project view before the view runs. A view with no declared
   policy is denied, so a new view is closed until someone reviews it. Non-numeric or
   non-positive `pk` values get a 404 before any lookup.
2. **Object permission.** Views, services and templates ask
   `core.permissions.PermissionManager` whether the user's roles on an object (owner, chronicle
   storyteller, admin and so on) grant a permission in the object's current status.

WebSocket connections do not pass through Django middleware, so
`game.consumers.SceneChatConsumer` checks `game.security.can_view_scene` before joining a
scene's group and re-checks access for each event it renders
([Scenes and real-time chat](../architecture/scenes-and-realtime.md)).

Game reference data (clans, disciplines, spheres and similar) is public by design; player
data requires login.

## Page caching

A cached page must never be served to a different user. Views that cache whole pages use
`core.cache.cache_page_per_visitor` ([`core/cache.py`](../../core/cache.py)), not Django's
`cache_page` directly, because the pages contain per-user markup and `cache_page` keys on the
URL alone. The decorator:

- never caches a request with a query string;
- lets anonymous visitors with no session or message cookie share one copy per URL, and stores
  that copy only if it is a 200 with no cookies set, no CSRF token rendered and no `private`
  cache-control;
- caches everyone else per cookie set (`vary_on_cookie`).

Rendered pages and sessions both live in Redis, so protect Redis like the database: bind it to
a private interface and require a password (in `REDIS_URL`). Rules for new cached views are in
[Caching](../architecture/caching.md).

## User-written content

Django templates escape variables by default. Where user text is rendered with markup, use
the filters in [`core/templatetags/sanitize_text.py`](../../core/templatetags/sanitize_text.py)
(`{% load sanitize_text %}`), never `|safe`:

| Filter | Output |
|--------|--------|
| `sanitize_html` | [bleach](https://pypi.org/project/bleach/) allowlist: `a` (with `href` only), `b`, `i`, `em`, `strong`, `u`, `p`, `br`, `strike`, `ul`, `li`, `span` (only `class="quote"`); link protocols `http`, `https`, `mailto`; disallowed tags are stripped. |
| `safe_post` | `sanitize_html`'s cleaning, then wraps `"quoted text"` outside tags in `<span class="quote">`. Used for scene posts ([`game/templates/game/scene/_post.html`](../../game/templates/game/scene/_post.html)). |
| `quote_tag` | Escapes everything, then wraps quoted text in `<span class="quote">`. |
| `simple_markdown` | Escapes everything, then converts `**bold**`, `*italic*`, line breaks and paragraphs. |

The template tags are documented in the [template tags reference](../reference/template-tags.md).

## Uploads

Characters, items and locations share an `image` field and an `image_status` field defined on
the abstract base in [`core/models.py`](../../core/models.py):

- Files are validated by Django's `ImageField` (Pillow must be able to open them, and the
  extension must be an image type Pillow supports).
- The stored path comes from `core.utils.filepath`: the model's module path plus the object's
  name, with `..`, `/` and `\` removed from the name, lower-cased, keeping the uploaded
  extension. Django's storage adds a suffix if the name is taken.
- `image_status` is `sub` (Submitted) by default, `app` once a storyteller approves it through
  `accounts.views.ImageApprovalView` (which calls `verify_st_for_chronicle`, then
  `core.services.approval.ApprovalService.approve_image`). Templates show an image only when
  `image_status == "app"`.
- Approval controls display, not access to the file. Files are written to `media/` as soon as
  they are uploaded, and the proxy serves everything under `/media/`, so an unapproved image is
  reachable by anyone who knows or guesses its path. Replacing an object's image does not reset
  `image_status`.
- Django applies no size limit to uploaded files; set one at the proxy.

Character-template import (`core.forms.character_template`) accepts a JSON file upload; it is
parsed, not stored in `media/`.

## Secrets

| Secret | Where it goes |
|--------|---------------|
| `SECRET_KEY` | Environment or `.env`. Rotating it logs everyone out and invalidates password-reset links. |
| `EMAIL_HOST_PASSWORD` | Environment or `.env`. |
| Redis password | Inside `REDIS_URL`. |
| Database password | `DB_PASSWORD`, only if you enable a PostgreSQL or MySQL block. |

`.env`, `tg/secrets.py`, `local_settings.py`, `db.sqlite3` and `*.log` are gitignored. Keep
`.env` readable only by the account that runs the server. Logs can contain user names and
exception details; treat `logs/` as sensitive. Never run `reset_demo_data` on a real
installation: it creates accounts with published passwords
([Maintenance](maintenance.md#data-maintenance-commands)).

## Dependency pinning

[`requirements.txt`](../../requirements.txt) is the only dependency file. It holds runtime,
test and lint tools together, and uses two kinds of specifier:

- **Exact pins (`==`)** for most packages, including `django-polymorphic`, `channels`,
  `channels-redis`, `daphne`, `django-redis`, `redis` and `bleach`. These change only when
  someone edits the file.
- **Minimum versions (`>=`)** for Django itself and for packages raised to fix a vulnerability
  (`requests`, `pillow`, `pytest`, `python-dotenv`, `setuptools`, `cryptography`, `urllib3`,
  `h11`, `tornado`, `black`). A fresh install takes the newest release above the floor.

Every security-motivated pin or floor has a `# Security:` comment above it naming the advisory
(CVE or GHSA identifier). Follow the same convention when you raise a version for a
vulnerability, and pin transitive dependencies here when an advisory affects them. Browser
libraries are vendored under `source_static/vendor/` and upgraded as described in
`VENDOR.md`. Upgrade steps are in [Maintenance](maintenance.md#upgrading-dependencies).

## Reporting a vulnerability

Report vulnerabilities privately as described in [`SECURITY.md`](../../SECURITY.md). Do not open
a public issue for a security problem.

## See also

- [Authorization](../architecture/authorization.md)
- [Caching](../architecture/caching.md)
- [Deployment](deployment.md)
- [Logging and monitoring](logging-and-monitoring.md)
- [`SECURITY.md`](../../SECURITY.md)
