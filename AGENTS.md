# AGENTS.md

Instructions for coding agents (and a quick orientation for human contributors) working in
this repository. Tool-specific files such as `CLAUDE.md` point here.

## The project

Tellurium Games is a Django 5.2 application for *World of Darkness* tabletop chronicles:
characters for eight game lines, character creation workflows, XP and approvals, chronicles,
scenes with live chat, items, locations and game reference data. Server-rendered templates
(the "Spread" design system) with htmx and Alpine.js; Django Channels for WebSockets.

Start with [`docs/architecture/overview.md`](docs/architecture/overview.md). The full
documentation index is [`docs/README.md`](docs/README.md); every app has a `README.md` and a
`docs/` folder with its detailed reference.

## Repository map

| Path | Contents |
|------|----------|
| `tg/` | Project package: `settings/` (`base`, `development`, `production`), URLs, ASGI/WSGI, test runner |
| `accounts/` | Profiles, sign-up and login, the dashboard and Storyteller queues |
| `characters/` | Character models per game line, reference data, chargen workflows, XP/freebie services |
| `core/` | Polymorphic base models, permissions, route policies and middleware, view mixins, templates, caching, management commands |
| `game/` | Chronicles, scenes and chat (HTTP and WebSocket), stories, weeks, journals, XP requests |
| `items/`, `locations/` | Item and location trees, built from a model registry |
| `widgets/` | Reusable form widgets (chained selects and others) |
| `tg_schema/` | Guarded migrations that patch existing databases |
| `populate_db/` | Game reference data scripts, run by `populate_gamedata` |
| `docs/` | Project-wide documentation |
| `.claude/` | Agent skills, sub-agents and commands |

## Commands

```bash
pip install -r requirements.txt
python manage.py makemigrations          # local apps commit no migrations
python manage.py migrate
python manage.py populate_gamedata          # load game reference data
python manage.py runserver 7000

python manage.py check
python manage.py test                       # the whole suite
python manage.py test characters            # one app
python manage.py test game.tests.test_scene_unread   # one module
python manage.py test --parallel 4          # faster; uses db_test_N.sqlite3

pre-commit run --all-files                  # black + ruff, as the hooks run them
```

Browser tests run only when `TG_BROWSER_BINARY` points at a Chromium or Chrome binary;
otherwise they are skipped. See [`docs/development/testing.md`](docs/development/testing.md).

## Rules for changes

Load the **`tg-standards`** skill ([`.claude/skills/tg-standards/SKILL.md`](.claude/skills/tg-standards/SKILL.md))
before you design or review a model, schema change, view, form, URL, template, permission,
cache decorator, management command or test. It holds the project's rules with their
reasons and a review checklist. The most important ones:

- **Schema.** Local apps commit no migrations. A change an existing database needs ships as a
  guarded migration in `tg_schema/` that imports no app model, skips what later releases
  removed, and has its own test. The model declares the same field or constraint.
  See [`docs/guides/changing-the-schema.md`](docs/guides/changing-the-schema.md).
- **Models.** Extend the existing polymorphic trees (`core.models.Model`, `Human`, `ItemModel`,
  `LocationModel`); take game lines from `settings.GAMELINES` / `settings.GAMELINE_CHOICES` and
  statuses from `core.constants`; validate in `clean()`.
- **Authorization.** Every routed view has exactly one access policy, in
  `core/route_policy_manifest.py` or the item/location registry; `AuthorizationMiddleware`
  denies anything undeclared. Object checks go through `core.permissions.PermissionManager`
  and the mixins in `core/mixins.py`. Reference data is public; player data is not.
  See [`docs/architecture/authorization.md`](docs/architecture/authorization.md).
- **Views and forms.** `get_object_or_404`, `select_related` / `prefetch_related`; explicit
  field lists; one POST endpoint per state change; rules in services, not views.
- **Templates.** Extend a Spread shell (`core/tl_base.html`, `core/form.html`,
  `core/object.html`); use the `tl` tags and `core/tl/field.html`; no inline styles or scripts,
  no Bootstrap or jQuery. See [`docs/architecture/frontend.md`](docs/architecture/frontend.md).
- **Caching.** Only `core.cache.cache_page_per_visitor` or `CachedDetailView` /
  `CachedListView`; never Django's `cache_page`.
- **Tests.** Every change ships tests next to the code it covers (`<app>/tests/`, mirroring
  the source path), including a denial test for each new route. Guard files (query ceilings,
  template policy, route policies, import placement, CRUD field baselines) change only on
  purpose.
- **Style.** black and ruff (the only import sorter) at 100 columns, through pre-commit; keep
  `ruff check .` clean.

## Working conventions

- Read the relevant app `README.md` and `docs/` page before changing an app. The code is the
  source of truth; if a document disagrees with it, fix the document in the same change.
- Update the documentation when behaviour, settings, commands or URLs change.
- Keep commits focused, with an imperative subject line and a body that says why. Keep
  branch history linear (rebase or cherry-pick, no merge commits on a feature branch).
- Run the full test suite before opening a pull request, and open it only when the branch is
  complete.
- Never commit secrets, `.env` files, databases or generated migration files for local apps.

## Other skills and agents

`.claude/skills/` also holds `wod-toolkit` (game rules and content creation),
`django-simplifier`, `python-simplifier` and `technical-debt-detector`. `.claude/agents/` holds
content-creation agents for game material (havens, nodes, fetishes, rotes and so on).
