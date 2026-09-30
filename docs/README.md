# Tellurium Games documentation

The documentation for Tellurium Games, a Django application for *World of Darkness*
chronicles. It is written for developers and coding agents working on the code and for
operators running it. Pages here cover the project as a whole; each app has its own `README.md`
and `docs/` folder with the detailed reference, listed at the end of this page.

New to the project? Read [Installation](getting-started/installation.md), then the
[Architecture overview](architecture/overview.md), then the architecture page for the area you
will work in.

## Getting started

| Page | Covers |
|------|--------|
| [Installation](getting-started/installation.md) | Prerequisites, virtualenv, database setup, first run |
| [Local development](getting-started/local-development.md) | The dev server, settings selection, debug tools, WebSockets locally |
| [Configuration](getting-started/configuration.md) | Settings modules, environment variables, `.env` |
| [Seed data](getting-started/seed-data.md) | Loading game reference data with `populate_gamedata` |

## Architecture

| Page | Covers |
|------|--------|
| [Architecture overview](architecture/overview.md) | Apps, request and WebSocket paths, front end, caching, repository layout |
| [Data model](architecture/data-model.md) | The polymorphic model trees, game lines, statuses, ownership and visibility |
| [Authorization](architecture/authorization.md) | Route policies, `AuthorizationMiddleware`, `PermissionManager`, roles, limited forms |
| [Schema migrations](architecture/schema-migrations.md) | How schema changes reach fresh and existing databases (`tg_schema`) |
| [Caching](architecture/caching.md) | Per-visitor page caching, cached views, reference lists |
| [Character creation (chargen)](architecture/character-creation.md) | Workflows, steps, allocation rules, htmx steps, submission |
| [XP, freebies and approvals](architecture/xp-and-approvals.md) | Status lifecycle, approval workflow, earning and spending XP and freebies |
| [Scenes and real-time updates](architecture/scenes-and-realtime.md) | Scenes, posts, dice rolls, unread tracking, WebSocket chat |
| [Front end](architecture/frontend.md) | The Spread design system, templates, CSS and JavaScript, htmx and Alpine |

## Guides

Step-by-step procedures for common changes, each ending with a checklist.

| Page | Covers |
|------|--------|
| [Adding a character type](guides/adding-a-character-type.md) | A new character model, from model to sheet, chargen and tests |
| [Adding reference data](guides/adding-reference-data.md) | A new game-data model with public views and loading scripts |
| [Adding a chargen step](guides/adding-a-chargen-step.md) | A new or changed step in a creation workflow |
| [Adding a view](guides/adding-a-view.md) | Mixins, route policy, queries, templates, fragments and tests for a view |
| [Changing the schema](guides/changing-the-schema.md) | Adding or changing fields and constraints so every database gets them |
| [Adding an item or location type](guides/adding-an-item-or-location-type.md) | A new item or location model through the registry |

## Reference

| Page | Covers |
|------|--------|
| [Settings reference](reference/settings.md) | Project settings and per-environment Django settings |
| [Management commands](reference/management-commands.md) | Every management command, its options and side effects |
| [URL reference](reference/urls.md) | URL namespaces, route families and naming conventions |
| [Template tags](reference/template-tags.md) | Every template tag and filter library |
| [Glossary](reference/glossary.md) | Project and *World of Darkness* terms used in the code |

## Development

| Page | Covers |
|------|--------|
| [Testing](development/testing.md) | The test runner, running tests, browser tests, guard tests, helpers |
| [Code style](development/code-style.md) | black, ruff, pre-commit, conventions, commit messages |

Also see [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the pull request process and
[`AGENTS.md`](../AGENTS.md) for coding-agent instructions. The design rules and review
checklists live in the [`tg-standards`](../.claude/skills/tg-standards/SKILL.md) skill.

## Operations

| Page | Covers |
|------|--------|
| [Deployment](operations/deployment.md) | Production settings, Redis, Daphne, static and media, the update procedure |
| [Security](operations/security.md) | Production security settings, sessions, sanitising, uploads, secrets |
| [Logging and monitoring](operations/logging-and-monitoring.md) | Log configuration, error reporting, what to watch, audit commands |
| [Maintenance](operations/maintenance.md) | Backups, caches, logs, data-maintenance commands, releases |

To report a vulnerability, see [`SECURITY.md`](../SECURITY.md).

## App documentation

| App | README | Detailed pages |
|-----|--------|----------------|
| `accounts` | [README](../accounts/README.md) | [models](../accounts/docs/models.md), [authentication](../accounts/docs/authentication.md), [dashboard](../accounts/docs/dashboard.md), [views and URLs](../accounts/docs/views-and-urls.md), [forms](../accounts/docs/forms.md), [templates](../accounts/docs/templates.md) |
| `characters` | [README](../characters/README.md) | [models](../characters/docs/models.md) (per game line: [vampire](../characters/docs/models-vampire.md), [werewolf](../characters/docs/models-werewolf.md), [mage](../characters/docs/models-mage.md), [wraith](../characters/docs/models-wraith.md), [changeling](../characters/docs/models-changeling.md), [demon](../characters/docs/models-demon.md), [mummy](../characters/docs/models-mummy.md), [hunter](../characters/docs/models-hunter.md)), [reference data](../characters/docs/reference-data.md), [chargen](../characters/docs/chargen.md), [forms](../characters/docs/forms.md), [views and URLs](../characters/docs/views-and-urls.md), [services](../characters/docs/services.md), [costs and rules](../characters/docs/costs-and-rules.md), [templates](../characters/docs/templates.md), [admin](../characters/docs/admin.md), [testing](../characters/docs/testing.md) |
| `core` | [README](../core/README.md) | [models](../core/docs/models.md), [permissions and policies](../core/docs/permissions-and-policies.md), [mixins](../core/docs/mixins.md), [views](../core/docs/views.md), [services](../core/docs/services.md), [templates and static](../core/docs/templates-and-static.md), [utilities](../core/docs/utilities.md), [management commands](../core/docs/management-commands.md), [testing](../core/docs/testing.md) |
| `game` | [README](../game/README.md) | [models](../game/docs/models.md), [scenes](../game/docs/scenes.md), [websockets](../game/docs/websockets.md), [XP](../game/docs/xp.md), [access and selectors](../game/docs/access-and-selectors.md), [views and URLs](../game/docs/views-and-urls.md), [forms](../game/docs/forms.md), [templates](../game/docs/templates.md), [admin](../game/docs/admin.md) |
| `items` | [README](../items/README.md) | [models](../items/docs/models.md), [views and URLs](../items/docs/views-and-urls.md), [forms](../items/docs/forms.md), [templates](../items/docs/templates.md) |
| `locations` | [README](../locations/README.md) | [models](../locations/docs/models.md), [chantries](../locations/docs/chantries.md), [nodes](../locations/docs/nodes.md), [realms](../locations/docs/realms.md), [freeholds](../locations/docs/freeholds.md), [views and URLs](../locations/docs/views-and-urls.md), [forms](../locations/docs/forms.md), [templates](../locations/docs/templates.md) |
| `widgets` | [README](../widgets/README.md) | [widgets](../widgets/docs/widgets.md), [chained selects](../widgets/docs/chained-selects.md), [JavaScript](../widgets/docs/javascript.md) |
| `tg` | [README](../tg/README.md) | [settings](../tg/docs/settings.md), [URLs](../tg/docs/urls.md), [ASGI and WSGI](../tg/docs/asgi-and-wsgi.md), [test runner](../tg/docs/test-runner.md) |
| `tg_schema` | [README](../tg_schema/README.md) | [migrations](../tg_schema/docs/migrations.md), [writing a migration](../tg_schema/docs/writing-a-migration.md) |
| `populate_db` | [README](../populate_db/README.md) | [loading](../populate_db/docs/loading.md), [conventions](../populate_db/docs/conventions.md), [adding data](../populate_db/docs/adding-data.md), [game lines](../populate_db/docs/gamelines.md) |
