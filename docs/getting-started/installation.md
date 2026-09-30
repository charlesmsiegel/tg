# Installation

This page takes you from a fresh clone to a working local copy of Tellurium Games: a
virtual environment, the dependencies, a database with tables, an admin account, game
reference data and static files. It is for developers and coding agents setting up a
machine for the first time. Day-to-day work (running the server, websockets, the debug
toolbar) is in [Local development](local-development.md).

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.10 | The project targets 3.10: [`requirements.txt`](../../requirements.txt) says so in a comment, and black and ruff are configured with `target-version` `py310` in [`pyproject.toml`](../../pyproject.toml). The black pre-commit hook asks for a `python3.10` interpreter (see [Code style](../development/code-style.md)). Write code that runs on 3.10: no syntax or standard-library APIs from later versions. |
| git | To clone and to restore files that `setup_db.sh` deletes (see [Seed data](seed-data.md)). |
| SQLite | Bundled with Python. It is the only database the settings configure. |
| Redis | Not needed for development. The production settings use it for the cache, sessions and the websocket channel layer; see [Redis](#redis) below. |
| A Chromium build, Firefox | Optional, only for the browser tests. See [Testing](../development/testing.md#browser-tests). |

## Create a virtual environment and install dependencies

```bash
git clone <repository-url> tg
cd tg
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.venv/` and `venv/` are both listed in [`.gitignore`](../../.gitignore).

[`requirements.txt`](../../requirements.txt) installs the runtime (Django `>=5.2.9`, django-polymorphic,
Channels, Daphne, django-redis, channels-redis, bleach, Pillow, python-dotenv), the
development toolbar (django-debug-toolbar), and the test and quality tools (pytest,
pytest-django, coverage, selenium, black, ruff, djlint, pre-commit). There is no separate
development requirements file. Playwright, used by some browser tests, is not in the file;
see [Testing](../development/testing.md#browser-tests).

## Optional: create a `.env` file

Settings read environment variables, and [`tg/settings/__init__.py`](../../tg/settings/__init__.py)
calls `load_dotenv()`, so values in a `.env` file at the repository root are picked up.
Development works with no `.env` at all. If you want one:

```bash
cp .env.example .env
```

Read [Configuration](configuration.md#envexample) before relying on it: three entries in
[`.env.example`](../../.env.example) do not behave the way their comments say
(`DJANGO_ENVIRONMENT`, `DJANGO_DEBUG` and `PASSWORD_RESET_TIMEOUT`).

## Create the database

The default database is SQLite at `db.sqlite3` in the repository root
(`DATABASES` in [`tg/settings/base.py`](../../tg/settings/base.py)).

The local apps (`accounts`, `characters`, `core`, `game`, `items`, `locations`) have a
`migrations/` package that contains only `__init__.py`. Their migration files are not
in git: [`.gitignore`](../../.gitignore) ignores `*/migrations/*` and re-includes only
`tg_schema/migrations/`. Because those apps have a migrations package, Django treats them
as migrated apps, and `migrate` alone creates no tables for them. Generate their initial
migrations on your machine first, then apply everything:

```bash
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` writes `accounts/migrations/0001_initial.py`,
`characters/migrations/0001_initial.py` and so on from the current models. These files are
local to your checkout and stay out of git. When you pull model changes later, run
`makemigrations` and `migrate` again ([`update.sh`](../../update.sh) does exactly that).

The committed migrations in [`tg_schema/migrations/`](../../tg_schema/migrations/) are
guarded patches that bring databases created from older models up to date. Each one looks
models and fields up by name when it runs and only adds what is missing
([`tg_schema/schema.py`](../../tg_schema/schema.py)), so on a fresh database they have
nothing to change. The design is described in
[Schema migrations](../architecture/schema-migrations.md).

Tests do not need any of this: while a local app has no migration files, the test runner
builds its tables straight from the models. See
[Testing](../development/testing.md#how-the-test-database-is-built).

## Create an admin account

```bash
python manage.py createsuperuser
```

Every new `User` gets a `Profile` from the `post_save` receiver
`accounts.signals.create_user_profile`, so the superuser is ready to sign in. Being a
superuser does not make you a storyteller: `Profile.is_st()` checks for `STRelationship`
rows ([`accounts/models.py`](../../accounts/models.py)). Create a chronicle and an
`STRelationship` in the Django admin at `/admin/` if you need storyteller pages.

## Load game reference data

```bash
python manage.py populate_gamedata
```

This runs every script under [`populate_db/`](../../populate_db/) to create books,
abilities, clans, spheres, gifts, character templates and the rest. Run it from the
repository root: the command looks for `populate_db/` relative to the current directory.
The scripts use `get_or_create`, so re-running it does not duplicate unchanged rows. See
[Seed data](seed-data.md) for ordering, filters and what each gameline gets.

## Collect static files

Static files come from two kinds of source directory:

| Source | Contents |
|--------|----------|
| [`source_static/`](../../source_static/) (`STATICFILES_DIRS`) | Site-wide assets: `favicon.ico`, `fonts/`, `images/`, and third-party libraries in `vendor/` (`htmx`, `htmx-ext-ws`, `alpinejs-csp`). |
| `<app>/static/<app>/` | Each app's own CSS and JavaScript, found by the app-directories finder. The design system stylesheet is `core/static/core/tl/tl.css`; widget scripts live in `widgets/static/widgets/`. |

`collectstatic` copies both into `STATIC_ROOT`, which is `collected_static/` in the
repository root (gitignored):

```bash
python manage.py collectstatic --noinput
```

In development you can skip this step: with `DEBUG = True` the development server serves
files straight from the source directories. Production needs it, because the production
settings use `ManifestStaticFilesStorage`, which serves content-hashed file names from the
manifest that `collectstatic` writes ([`tg/settings/production.py`](../../tg/settings/production.py)).
Edit files in the source directories, never in `collected_static/`.

## Redis

| Environment | Cache | Sessions | Channel layer (websockets) |
|-------------|-------|----------|----------------------------|
| Development ([`development.py`](../../tg/settings/development.py), [`base.py`](../../tg/settings/base.py)) | `LocMemCache` | Database (Django default) | `InMemoryChannelLayer` |
| Production ([`production.py`](../../tg/settings/production.py)) | `django_redis.cache.RedisCache` | Cache (`SESSION_ENGINE = "django.contrib.sessions.backends.cache"`) | `channels_redis.core.RedisChannelLayer` |

Development and the test suite need no Redis. Production requires it: the cache is
configured with `IGNORE_EXCEPTIONS: True`, so cache reads and writes fail quietly when
Redis is down, but sessions live in that cache and live scene chat needs the channel layer.
Both read `REDIS_URL`; see [Configuration](configuration.md).

## Check the installation

```bash
python manage.py check
python manage.py runserver 7000
```

Open `http://localhost:7000/` or `http://127.0.0.1:7000/`, and `/admin/` to sign in with
the superuser. Use one of those host names rather than `[::1]`: the development
`ALLOWED_HOSTS` does not include it, and the websocket origin check depends on
`ALLOWED_HOSTS` (see [Local development](local-development.md)).

The logging configuration writes to `logs/debug.log`, `logs/error.log` and
`logs/warning.log`. The `logs/` directory is kept in git (it holds only a `.gitignore`);
if it is missing, Django fails to start because the file handlers cannot open their files.

## Reset or update an existing installation

| Script | What it does |
|--------|--------------|
| [`update.sh`](../../update.sh) | `git pull`, `makemigrations`, `migrate`, `collectstatic`. Use it to bring a checkout up to date. |
| [`setup_db.sh`](../../setup_db.sh) | Deletes `db.sqlite3` and every migration file, including the committed `tg_schema` ones (`reset_db --yes`), regenerates and applies migrations, recollects static files and runs `populate_gamedata`. Destructive; read [Seed data](seed-data.md#setup_dbsh-and-reset_db) first. |

## See also

- [Local development](local-development.md)
- [Configuration](configuration.md)
- [Seed data](seed-data.md)
- [Schema migrations](../architecture/schema-migrations.md)
- [Settings reference](../reference/settings.md)
- [`tg/` project package](../../tg/README.md)
