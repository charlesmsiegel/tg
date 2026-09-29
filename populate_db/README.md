# populate_db

`populate_db/` holds the Python scripts that load World of Darkness reference data into
the database: books, abilities, backgrounds, merits and flaws, Mage Spheres and
effects, Vampire clans and Disciplines, Werewolf Gifts and rites, Changeling Arts,
Demon lores, example items, character templates, and more. This page is the entry
point for developers and coding agents who load, fix or extend that data; the
details live in [`docs/`](docs/).

It is not a Django app. It has no models and no `__init__.py` at its root; the
scripts create rows in other apps' models.

## Main concepts

- **Scripts, not fixtures.** Each `.py` file is ordinary Python that calls the ORM,
  almost always `Model.objects.get_or_create(...)`. There are no JSON fixtures.
- **One command loads everything.** `python manage.py populate_gamedata`
  ([`core/management/commands/populate_gamedata.py`](../core/management/commands/populate_gamedata.py))
  finds every `.py` file under `populate_db/`, sorts them, and runs each one inside
  its own database transaction. See [loading](docs/loading.md).
- **Order comes from file names and imports.** Top-level files run first, in name
  order (so `00_books.py`, `01_resonance.py` and `aa_gamelines.py` lead), then each
  subfolder in name order. A script that needs rows from another script imports it,
  which runs it on the spot. See [conventions](docs/conventions.md).
- **Scripts must be safe to run again.** The command runs every file on every load,
  and imported files run more than once; `get_or_create` keeps that from creating
  duplicates.
- **Citations.** Reference objects record their source book and page with
  `obj.add_source(book_title, page)`, which looks the book up by its exact title.

## Layout

| Path | Contents |
|------|----------|
| Top-level `*.py` (18 files) | Data shared by every gameline: books, resonance, gamelines, attributes, abilities, backgrounds, archetypes, merits and flaws, specialties, derangements, languages, materials, nouns, object types, house rules, news items, weapons, companion advantages |
| [`changeling/`](changeling/) | Cantrips, chimera, kiths, treasures |
| [`character_templates/`](character_templates/) | `CharacterTemplate` rows for each gameline, plus cross-gameline faction templates |
| [`demon/`](demon/) | Houses, factions, lores, rituals, relics, visages, Earthbound data, Demon merits and flaws |
| [`mage/`](mage/) | Spheres, practices, instruments, paradigms, tenets, factions, effects, rotes, wonders, sectors, Sorcerer fellowships, spirits and examples |
| [`mummy/`](mummy/) | Dynasties and titles |
| [`vampire/`](vampire/) | Clans, bloodlines, Disciplines, paths, sects, titles, linear magic |
| [`werewolf/`](werewolf/) | Tribes, camps, Gifts, rites, totems, fetishes, talens, spirits, battle scars, renown incidents, Fomori powers |
| [`wraith/`](wraith/) | Factions, guilds, Shadow archetypes, Thorns |
| [`docs/`](docs/) | This documentation (not loaded; only `.py` files are) |

The full inventory is in [gamelines](docs/gamelines.md).

## Quick start

From the repository root, with migrations applied:

```bash
python manage.py populate_gamedata                 # load everything
python manage.py populate_gamedata --dry-run       # list the files, in load order
python manage.py populate_gamedata --only rotes --verbose   # one kind of file, with tracebacks
```

[`setup_db.sh`](../setup_db.sh) resets a development database and then runs the same
command; read [loading](docs/loading.md#setup_dbsh) before you use it, because it
deletes files.

## How it connects to other apps

The scripts write to models in `core` (`Book`, `Language`, `Noun`, `HouseRule`,
`NewsItem`, `CharacterTemplate`), `game` (`Gameline`, `ObjectType`), `characters`
(statistics, merits and flaws, gameline reference models, example characters),
`items` (`Material`, `Medium`, weapons, Wonders, Demon relics, fetishes, talens,
treasures, Sorcerer artifacts) and `locations` (`Sector`). Models built on
`core.models.Model` or `core.base.ValidatedSaveMixin` run `full_clean()` on save, so a
script that breaks one of their rules fails with a `ValidationError`.

The ruff configuration in [`pyproject.toml`](../pyproject.toml) exempts
`populate_db/**` from `E402` (import not at top of file), because scripts import
other scripts mid-file on purpose.

## Documentation

| Page | Contents |
|------|----------|
| [docs/loading.md](docs/loading.md) | `populate_gamedata` options, discovery and order, transactions and failures, `setup_db.sh`, debugging one script |
| [docs/conventions.md](docs/conventions.md) | File naming and prefixes, the `_INC` suffix, imports as load order, idempotency, exported names |
| [docs/adding-data.md](docs/adding-data.md) | How to add or change records, cite sources, and add a new script or character template |
| [docs/gamelines.md](docs/gamelines.md) | Every script, what it loads and which scripts it imports |

## See also

- [Seed data](../docs/getting-started/seed-data.md)
- [Management commands](../docs/reference/management-commands.md)
- [Adding reference data](../docs/guides/adding-reference-data.md)
- [Code style](../docs/development/code-style.md)
- [core app](../core/README.md)
