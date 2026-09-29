# Tellurium Games

Tellurium Games (TG) is a Django web application for running *World of Darkness* tabletop
chronicles. Players build and advance characters; Storytellers run chronicles, scenes and
stories, review characters and advancement, and keep the chronicle's items, locations and
reference material in one place.

## Features

- **Characters for eight game lines**: *Vampire: the Masquerade*, *Werewolf: the Apocalypse*
  (with the Fera and Kinfolk), *Mage: the Ascension* (with Sorcerers and Companions), *Wraith:
  the Oblivion*, *Changeling: the Dreaming*, *Demon: the Fallen*, *Mummy: the Resurrection* and
  *Hunter: the Reckoning*, plus mortals. Game lines are at different levels of completeness.
- **Guided character creation**: step-by-step workflows per character type with trait
  allocation, priority ranks and freebie spending, then submission for Storyteller approval.
- **Advancement**: XP earned per week, scene and story; XP and freebie spending requests that
  a Storyteller approves or denies.
- **Chronicles and play**: chronicles with head and gameline Storytellers, stories, weeks,
  journals, and scenes with live chat over WebSockets, dice rolls and unread tracking.
- **Items and locations**: equipment, artifacts, havens, nodes, caerns and more, per game line.
- **Reference data**: clans, tribes, traditions, disciplines, gifts, spheres, merits and
  flaws, and other game material, loaded from scripts and browsable without an account.
- **Access control**: every route has a declared policy, checked by middleware before any view
  runs; object access follows ownership, chronicle roles and visibility.

## Quick start

You need Python 3.10 and Git. Local development uses SQLite, an in-memory cache and an
in-memory channel layer, so no database server or Redis is required.

```bash
git clone https://github.com/charlesmsiegel/tg.git
cd tg
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations   # local apps commit no migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_gamedata   # load the game reference data
python manage.py runserver 7000
```

Open <http://127.0.0.1:7000/>. The local apps keep no migration files in git, so
`makemigrations` generates them for your database first; the full setup is in
[Installation](docs/getting-started/installation.md).

Run the checks and the tests:

```bash
python manage.py check
python manage.py test
```

## Documentation

The documentation lives in [`docs/`](docs/README.md), with a detailed reference for each app
in its own folder.

| Start here | For |
|------------|-----|
| [Installation](docs/getting-started/installation.md), [Local development](docs/getting-started/local-development.md) | Setting up a working copy |
| [Architecture overview](docs/architecture/overview.md) | How the system fits together |
| [Guides](docs/README.md#guides) | Adding character types, views, reference data, schema changes |
| [Testing](docs/development/testing.md), [Code style](docs/development/code-style.md) | Working on the code |
| [Deployment](docs/operations/deployment.md) | Running it in production |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to propose a change |
| [`AGENTS.md`](AGENTS.md) | Instructions for coding agents |

| App | Purpose |
|-----|---------|
| [`accounts`](accounts/README.md) | Sign-up, profiles, the player and Storyteller dashboard |
| [`characters`](characters/README.md) | Character models, sheets, creation workflows, XP and freebie rules |
| [`core`](core/README.md) | Base models, permissions and route policies, view mixins, templates, shared tools |
| [`game`](game/README.md) | Chronicles, scenes and chat, stories, weeks, journals, XP requests |
| [`items`](items/README.md), [`locations`](locations/README.md) | Equipment and places |
| [`widgets`](widgets/README.md) | Reusable form widgets |
| [`tg`](tg/README.md), [`tg_schema`](tg_schema/README.md) | Project settings and URLs; schema patches for existing databases |
| [`populate_db`](populate_db/README.md) | Game reference data scripts |

## Technology

Django 5.2 with [django-polymorphic](https://django-polymorphic.readthedocs.io/) model trees,
Django Channels and Daphne for WebSockets, Redis for the production cache and channel layer,
server-rendered templates in the project's "Spread" design system with htmx and Alpine.js,
black and ruff through pre-commit.

## Contributing and security

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request. Report security
problems privately as described in [`SECURITY.md`](SECURITY.md). Bugs and feature requests go
to [GitHub Issues](https://github.com/charlesmsiegel/tg/issues).
