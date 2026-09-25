# Tellurium Games (TG)

TG is a Django application for running *World of Darkness* tabletop chronicles. Players can create and advance characters; Storytellers can organize chronicles, scenes, stories, journals, items, and locations in the same place. The site is in beta, and the depth of support varies by game line.

## What is here

- Character sheets and creation flows with game-specific traits, plus experience and freebie spending.
- Chronicles with player and Storyteller roles, scenes, stories, journals, and house rules.
- Review and approval workflows for characters and advancement.
- Reference data for abilities, powers, factions, and other game material, loaded from `populate_db/`.
- Scene chat over Django Channels.

The character code includes **Vampire: the Masquerade**, **Werewolf: the Apocalypse**, **Mage: the Ascension**, **Wraith: the Oblivion**, **Changeling: the Dreaming**, **Demon: the Fallen**, **Mummy: the Resurrection**, and **Hunter: the Reckoning**. These game lines are at different stages of development.

## Run locally

You need Python 3.10 or newer and Git. The commands below use a macOS or Linux shell. Local development uses SQLite and an in-memory channel layer, so it does not require PostgreSQL or Redis.

```bash
git clone https://github.com/charlesmsiegel/tg.git
cd tg
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 7000
```

Open <http://127.0.0.1:7000/>. You can sign in with the superuser you created or make a player account at `/accounts/signup/`.

Development settings are selected by default. You can copy [`.env.example`](.env.example) to `.env` to change local settings; the app reads it with `python-dotenv`. In particular, `SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` are recognized. The database defaults to `db.sqlite3` in the project root.

### Load game data

To populate a **fresh local database** with the bundled game data, run this from the repository root:

```bash
python manage.py populate_gamedata --dry-run  # Preview the scripts
python manage.py populate_gamedata            # Load them
```

Check the command's final success and failure counts. It executes the Python files in `populate_db/` and reports errors per file. The `setup_db.sh` script is for a full reset: it calls `reset_db --yes`, deleting the existing local database and app migration files. Do not use it to add data to a database you want to keep.

## Work on the project

```bash
python manage.py check
python manage.py test
```

The main areas of the codebase are:

| Path | Purpose |
| --- | --- |
| `characters/` | Character models, sheets, creation flows, and game-specific rules |
| `game/` | Chronicles, scenes, stories, journals, XP requests, and scene chat |
| `accounts/` | Sign-up, profiles, and player/Storyteller relationships |
| `items/`, `locations/` | Chronicle equipment and places |
| `core/` | Shared models, permissions, views, and template components |
| `populate_db/` | Scripts that load game reference data |
| `tg/settings/` | Development and production Django settings |

For implementation conventions, see [`CLAUDE.md`](CLAUDE.md). The [`characters/`](characters/README.md), [`game/`](game/README.md), and [`core/`](core/README.md) guides describe the main apps. Bugs and feature requests go in [GitHub Issues](https://github.com/charlesmsiegel/tg/issues).
