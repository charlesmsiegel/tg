# Seed data

This page explains how the game reference data (books, abilities, clans, spheres, gifts,
character templates and so on) gets into a database: the `populate_gamedata` command,
the scripts under [`populate_db/`](../../populate_db/), the order they run in, what each
gameline receives, how to re-run them safely, and the destructive reset script. It is
for anyone setting up a database or adding reference data. How to write a new data
script is in [Adding reference data](../guides/adding-reference-data.md).

## Load everything

From the repository root:

```bash
python manage.py populate_gamedata
```

The command is `core/management/commands/populate_gamedata.py`
([source](../../core/management/commands/populate_gamedata.py)). It finds every `*.py`
file under `populate_db/` recursively, sorts them, and executes each one. It looks for
`populate_db` relative to the current working directory, so it fails with
`Directory populate_db not found` anywhere else.

Tests do not use this data: they create the objects they need (see
[Testing](../development/testing.md)).

## How a script runs

Each data script is a flat Python file of ORM calls, typically:

```python
from core.models import Book

Book.objects.get_or_create(
    name="Mage: the Ascension 20th Anniversary Edition",
    edition="20th",
    gameline="mta",
    url="https://www.storytellersvault.com/product/149562/...",
)
```

`populate_gamedata` reads the file and runs it with
`exec(code, {"__name__": "__main__"})` inside `transaction.atomic()`. So:

- A script that raises rolls back only its own writes. The command prints
  `✗ <path>: <error>`, logs the traceback to the `core.management.commands.populate_gamedata`
  logger, and **carries on** with the next file. The summary at the end counts successes
  and failures, and the command then exits with an error when any file failed.
- `--verbose` prints the traceback of each failure as well.

### Scripts that import other scripts

Some scripts import names from others, for example
`from populate_db.mage.practices_INC import ...` in
[`populate_db/mage/rotes.py`](../../populate_db/mage/rotes.py). A Python import executes
the imported script's module body the first time it is imported in the process, so an
imported script runs once through the import and once more when `populate_gamedata`
reaches it in its own turn. This is why every script must be idempotent, and why
[`pyproject.toml`](../../pyproject.toml) exempts `populate_db/**` from ruff's E402
(imports not at the top): the position of an import is the point at which that other
script runs.

Imports between scripts:

| Imported script | Imported by |
|-----------------|-------------|
| `abilities.py`, `objects.py` and other top-level files | many scripts, for the rows they create |
| `mage/effects_INC.py` | `mage/rotes.py`, `mage/mage_example_rotes.py`, `mage/mage_example_items.py`, `mage/wonders_INC.py` |
| `mage/practices_INC.py` | `mage/rotes.py`, `mage/mage_example_rotes.py`, `mage/corruptedpractices.py`, `mage/specializedpractices.py`, `mage/tenets.py`, `mage/magefactions.py` |
| `mage/instruments_INC.py` | `mage/practices_INC.py` |
| `mage/paradigms_INC.py` | `mage/magefactions.py` |
| `demon/demon_houses.py`, `demon/demon_lores.py`, `demon/demon_earthbound_lores.py` | the Demon relic, ritual and visage scripts |

### The `_INC` suffix

Nine files end in `_INC`: `merits_and_flaws_INC.py`, `mage/effects_INC.py`,
`mage/houses_INC.py`, `mage/instruments_INC.py`, `mage/paradigms_INC.py`,
`mage/practices_INC.py`, `mage/wonders_INC.py`, `werewolf/fomor_powers_INC.py` and
`werewolf/gifts_INC.py`. The loader gives the suffix no meaning: these files are
discovered, filtered and sorted like any other. Four of them are imported by other
scripts (table above); the rest are not.

## Load order

`Command.get_sort_key` sorts paths relative to `populate_db/`:

| Priority | Files | Order within the group |
|----------|-------|------------------------|
| 0 | Files directly in `populate_db/` | Alphabetical by file name |
| 1 | Files in a `core/` subdirectory (none exists) | Alphabetical by path |
| 500 | Files in every other subdirectory | Alphabetical by directory, then path |
| 999 | Files in a `chronicles/` subdirectory | Alphabetical by path |

The top-level files are named so the alphabet gives the right order:
`00_books.py`, `01_resonance.py` and `aa_gamelines.py` sort first, then `abilities.py`,
`advantages.py`, `archetypes.py`, `attributes.py`, `backgrounds.py` and the rest. The
subdirectories then load as `changeling/`, `character_templates/`, `demon/`, `mage/`,
`mummy/`, `vampire/`, `werewolf/`, `wraith/`.

`populate_db/chronicles/` is listed in [`.gitignore`](../../.gitignore). It is the place
for data specific to your own chronicles; it loads last, after all reference data exists.

`__init__.py` files are loaded too; `character_templates/__init__.py` and
`mummy/__init__.py` contain only a docstring and create nothing.

To see the exact order on your checkout:

```bash
python manage.py populate_gamedata --dry-run
```

## Options

| Option | Effect |
|--------|--------|
| `--dry-run` | List the files that would load, in order, and stop. |
| `--verbose` | Print `Loading <path>... ✓` per file and a traceback for each failure. |
| `--only TEXT` | Keep only files whose **file stem** contains `TEXT` (case-insensitive). |
| `--skip TEXT` | Drop files whose file stem contains `TEXT` (case-insensitive). |
| `--gameline GAMELINE` | Keep the files of one gameline plus every shared file (below). Takes a code or its name. |

`--only` and `--skip` look only at the file name without `.py`, never at the directory.
`--only rituals`, for example, loads the nine Demon ritual scripts and
`vampire/linear_magic_rituals.py`. The filters apply in the order `--gameline`, `--only`,
`--skip`. Filtering does not stop imports: a kept script still runs any script it
imports.

A file belongs to a gameline when it sits in that gameline's folder (`vampire/`,
`mummy/`...) or a word of its name, split on `_`, is the gameline's code or name
(`character_templates/vampire_templates.py`). The codes and names come from
`settings.GAMELINES` (`Command.file_gamelines`). Every other file is shared and always
kept. So `--gameline vtm` and `--gameline vampire` both keep everything under `vampire/`
and `character_templates/vampire_templates.py`, drop `mage/spheres.py` and the other
gamelines' folders, and keep the top-level files and `character_templates/__init__.py`.

For a partial reload, `--only` with a distinctive stem is the more predictable filter:

```bash
python manage.py populate_gamedata --only vampire_disciplines
python manage.py populate_gamedata --skip news_items
```

## What each gameline gets

| Directory or file | Creates |
|-------------------|---------|
| `00_books.py` | `core.models.Book` rows for the sourcebooks. |
| `01_resonance.py` | Mage `Resonance`. |
| `aa_gamelines.py` | `game.models.Gameline` rows for World of Darkness and the eight gamelines. |
| `abilities.py`, `attributes.py`, `backgrounds.py`, `archetypes.py`, `specialties.py`, `derangements.py`, `merits_and_flaws_INC.py` | Shared character traits (`Ability`, `Attribute`, `Background`, `Archetype`, `Specialty`, `Derangement`, `MeritFlaw` with the character types each is allowed for). |
| `advantages.py` | Companion `Advantage` rows. |
| `objects.py` | `game.models.ObjectType` rows naming each character, item and location type per gameline; other scripts import them (for example to set which types a merit or flaw is allowed for). |
| `weapons.py`, `materials.py` | `MeleeWeapon`, `RangedWeapon`, `ThrownWeapon`; item `Material`. |
| `languages.py`, `nouns.py`, `house_rules.py`, `news_items.py` | `core.models.Language`, `Noun`, `HouseRule`, `NewsItem`. |
| `character_templates/` | `core.models.CharacterTemplate` rows: pre-built concepts for Vampire, Werewolf, Mage, Wraith, Changeling and Demon, plus faction templates (Vampire, Werewolf, Mage). |
| `vampire/` | Clans and bloodlines (`VampireClan`), `Discipline`, `Path`, `VampireSect`, `VampireTitle`, and linear-magic paths and rituals (`LinearMagicPath`, `LinearMagicRitual`). |
| `werewolf/` | `Tribe`, `Camp`, `Gift` and `GiftPermission` (Garou and Fera), `Rite`, `Totem`, `SpiritCharm`, `SpiritCharacter` spirits, `Fetish`, `Talen`, `BattleScar`, `RenownIncident`, `FomoriPower`. |
| `mage/` | `Sphere`, `MageFaction`, `Paradigm`, `Practice`, `SpecializedPractice`, `CorruptedPractice`, `Instrument`, `Tenet`, `Effect`, `Rote`, `Wonder` items (`Artifact`, `Grimoire`, `Charm`), `SorcererArtifact`, `SorcererFellowship`, `Medium`, `Sector` locations, example companions and spirits. `mage/houses_INC.py` and `mage/legacies.py` create **Changeling** `House`, `HouseFaction` and `Legacy` rows despite their directory. |
| `changeling/` | `Kith`, `Cantrip`, `Chimera`, `Treasure`. |
| `wraith/` | `WraithFaction`, `Guild`, `ShadowArchetype`, `Thorn`. |
| `demon/` | `DemonFaction`, `DemonHouse`, `Lore`, `Ritual`, `Relic` (including the House of the Fallen sets and Earthbound material), `Visage` and apocalyptic-form traits, Demon merits and flaws, and Earthbound abilities, archetypes and backgrounds. |
| `mummy/` | `Dynasty`, `MummyTitle`. |

Hunter and Orpheus have no seed scripts.

## Re-running safely

Every data script except the two `__init__.py` files uses `get_or_create` (some then
set more fields and `save()`), so running `populate_gamedata` again over a populated
database creates no duplicates of unchanged rows. Keep that in mind when you edit a
script:

- `get_or_create(**kwargs)` looks rows up by **all** its keyword arguments except
  `defaults`. If you change a value that is part of the lookup (a book's `url`, a merit's
  `name`), the next run finds no match and creates a second row; the old one stays. Move
  descriptive fields into `defaults=` or into a follow-up assignment and `save()` when
  they may change, and delete or rename the old row by hand when you change an identity
  field.
- The loader never deletes rows. Removing a script, or an entry from one, does not
  remove what it created earlier.
- Each file is its own transaction, so a failed file leaves the others' data in place.
  Fix the script and re-run only that file with `--only`.

## `setup_db.sh` and `reset_db`

[`setup_db.sh`](../../setup_db.sh) rebuilds a development database from nothing:

```bash
python manage.py reset_db --yes
python manage.py makemigrations
python manage.py migrate
rm -rf collected_static/
yes yes | python manage.py collectstatic
python manage.py populate_gamedata
```

`reset_db` ([source](../../core/management/commands/reset_db.py)) is destructive:

- It refuses to run unless `DEBUG` is true (`CommandError`), so it only works with the
  development settings.
- It deletes `db.sqlite3` in the current directory (the path is fixed; it does not read
  `DATABASES`).
- For every top-level directory that has a `migrations/` folder, it deletes every
  `*.py` file in that folder except `__init__.py`, the local apps' generated
  migrations. It keeps the **committed** migrations in `tg_schema/migrations/`, which
  the following `migrate` applies (on a fresh database they change nothing).
- Without `--yes` it asks for confirmation (`y` or `yes`).

Everything in the old `db.sqlite3` is lost: users, chronicles, characters and all game
data.

## Sample play data

Two commands create non-reference data for trying the site out; both are described in
[Management commands](../reference/management-commands.md):

- `populate_test_chronicle --chronicle <id>` adds a `test_player` user, `Human`
  characters and scenes to an existing chronicle.
- `reset_demo_data --confirm` deletes all game data and creates a demo storyteller,
  player and chronicle.

## See also

- [Installation](installation.md)
- [Adding reference data](../guides/adding-reference-data.md)
- [Management commands](../reference/management-commands.md)
- [`populate_db/` package](../../populate_db/README.md)
- [Schema migrations](../architecture/schema-migrations.md)
