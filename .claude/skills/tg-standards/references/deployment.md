# Deployability

What a change must do so it deploys cleanly: settings, static files, templates, schema,
caching and real-time pieces. How to run a server is in
[docs/operations/deployment.md](../../../../docs/operations/deployment.md); every setting is
in [docs/reference/settings.md](../../../../docs/reference/settings.md).

## How production differs from development

| Aspect | Development (`tg/settings/development.py`) | Production (`tg/settings/production.py`) |
|--------|--------------------------------------------|-------------------------------------------|
| Selection | `DJANGO_ENVIRONMENT` unset or `development` | `DJANGO_ENVIRONMENT=production`; any other value raises `ValueError` |
| `DEBUG` | `True` | `False` |
| Secrets | `SECRET_KEY` has a dev default | `SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` required (import fails without them) |
| Database | SQLite `db.sqlite3`, `ATOMIC_REQUESTS=True` | Same SQLite database with `CONN_MAX_AGE` (`DB_CONN_MAX_AGE`, default 600) |
| Cache | `LocMemCache` | Redis (`REDIS_URL`), key prefix `tg`, `IGNORE_EXCEPTIONS=True` |
| Sessions | Database | Cache (`SESSION_ENGINE = ...backends.cache`) |
| Channel layer | In memory | Redis (`channels_redis`) |
| Static files | `STATICFILES_DIRS = [source_static]` plus app `static/` | `ManifestStaticFilesStorage` (content-hashed names) |
| Security | | HTTPS redirect, secure cookies, HSTS, `X_FRAME_OPTIONS="DENY"`, `CSRF_COOKIE_SAMESITE="Strict"` |

The app is served as ASGI (`tg.asgi.application`, `daphne` first in `INSTALLED_APPS`):
HTTP through Django, WebSockets through `game.routing` behind
`AllowedHostsOriginValidator` and `AuthMiddlewareStack`.

## Rules for a change

- **New setting or environment variable**: read it in `tg/settings/base.py` (or the
  environment module) with `os.environ.get("NAME", <safe default>)`, parse types
  explicitly (`int(...)`, `== "True"`), and add it to `.env.example` and
  `docs/reference/settings.md`. Never read `os.environ` outside the settings package.
  Production-only secrets have no default and fail loudly.
- **Static files**: reference every asset with `{% static %}`. With
  `ManifestStaticFilesStorage` a path missing from the manifest raises at render time
  when `DEBUG` is off, so a typo that works in development breaks production pages. Put
  app assets in `<app>/static/<app>/` and shared ones in `source_static/`; vendored
  libraries go in `source_static/vendor/` with their hashes in `VENDOR.md`.
- **Restart after deploy**: Python changes take effect only in a restarted server
  process.
- **Schema**: an existing database gets new columns, tables, constraints and data fixes
  only from `tg_schema` migrations; `update.sh` runs `git pull`, `makemigrations`,
  `migrate`, `collectstatic`. A change that needs anything else on deploy is not
  deployable as is ([schema-changes.md](schema-changes.md)).
- **Game data**: new reference rows ship as idempotent `populate_db` scripts loaded with
  `python manage.py populate_gamedata`, never as a migration that imports app models.
- **Caching**: pages are shared between anonymous visitors in Redis; follow
  [caching.md](caching.md) so nothing per-user is served from the cache. Redis errors are
  swallowed (`IGNORE_EXCEPTIONS`), so the cache must never be the only copy of data.
- **Real time**: code that broadcasts to scenes goes through `game.scene_chat`; it must
  work with the Redis channel layer (messages are JSON-serializable, no in-process state).
- **Logging**: use the app's logger; files go to `logs/` (`app.log`, `error.log`,
  `warning.log` rotate in production). Never log secrets or passwords.
- **Management commands** that run on a schedule take `--dry-run` and run in a
  transaction ([commands.md](commands.md)).

## Checklist

- [ ] `DJANGO_ENVIRONMENT=production python manage.py check --deploy` passes with the
  required variables set.
- [ ] New settings documented, with safe defaults or a loud failure for secrets.
- [ ] Assets through `{% static %}`; `collectstatic` succeeds.
- [ ] Schema and data changes reach existing databases through `tg_schema` or
  `populate_gamedata`.
- [ ] Nothing per-user cached; Channels messages serializable.

## See also

- [docs/operations/deployment.md](../../../../docs/operations/deployment.md)
- [docs/reference/settings.md](../../../../docs/reference/settings.md)
- [`tg/settings/production.py`](../../../../tg/settings/production.py), [`update.sh`](../../../../update.sh)
- [schema-changes.md](schema-changes.md), [caching.md](caching.md)
