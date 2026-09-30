# Script conventions

This page describes the conventions the scripts in `populate_db/` follow: file names
and prefixes, the `_INC` suffix, how imports between scripts decide load order, how
scripts stay safe to rerun, and how they share objects. It is for anyone adding or
editing a data script, human or agent. How the loader runs the files is in
[loading](loading.md).

## File names and folders

- Data shared by every gameline lives at the top level of `populate_db/`; data for one
  gameline lives in that gameline's folder (`vampire/`, `werewolf/`, `mage/`,
  `wraith/`, `changeling/`, `demon/`, `mummy/`). There is no `hunter/` folder.
  `character_templates/` holds `CharacterTemplate` rows. See
  [gamelines](gamelines.md) for the inventory, including the few files whose folder
  does not match the models they load.
- File names are lowercase snake case. Many gameline files repeat the gameline in the
  name (`vampire_clans.py`, `demon_lores.py`, `mage_templates.py`); the loader's
  `--gameline` filter matches the folder and whole words of that name (see
  [loading](loading.md#filtering)).

### Ordering prefixes

The loader sorts top-level files by name before running them, so a prefix moves a
file earlier:

| File | Prefix | Effect |
|------|--------|--------|
| `00_books.py` | `00_` | Runs first. Every `Book` exists before other scripts cite it with `add_source()`. |
| `01_resonance.py` | `01_` | Runs second, creating the Mage Resonance traits. |
| `aa_gamelines.py` | `aa_` | Sorts before `abilities.py`, so the `game.Gameline` rows exist before the other top-level scripts. |

Use a numeric or `aa_` prefix only when a top-level file must run before others and
cannot be imported by them. For anything else, import the script you depend on (see
below); that is explicit and does not rely on names.

### The `_INC` suffix

Nine scripts end in `_INC`: `merits_and_flaws_INC.py`, `mage/effects_INC.py`,
`mage/houses_INC.py`, `mage/instruments_INC.py`, `mage/paradigms_INC.py`,
`mage/practices_INC.py`, `mage/wonders_INC.py`, `werewolf/fomor_powers_INC.py` and
`werewolf/gifts_INC.py`. The loader gives the suffix no meaning: these files are
discovered, sorted, filtered and run like every other script, and nothing else in the
repository defines it. Several of them are imported by other scripts
(`effects_INC`, `practices_INC`, `paradigms_INC`, `instruments_INC`), others are not.
Treat the suffix as part of the file name; keep it when you edit these files so
imports and `--only` filters keep working.

## Imports are load order

A script that needs rows created by another script imports that script:

```python
# populate_db/vampire/vampire_clans.py
from characters.models.vampire.clan import VampireClan
from populate_db.vampire.vampire_disciplines import (
    animalism,
    auspex,
    celerity,
    # ...
)
```

Importing a script executes it (once per process, then it is cached), so the
disciplines exist before the clans that reference them. The imported names are the
objects the other script bound at module level. Imports resolve because
`populate_db` is a namespace package under the repository root, which `manage.py` puts
on `sys.path`.

Imports can appear anywhere in a file, not only at the top. For example
`demon/demon_visages.py` defines a helper function and then imports the Demon houses
it needs. Because each import runs a script, its position in the file is its position
in the load order. The ruff configuration in [`pyproject.toml`](../../pyproject.toml)
exempts `populate_db/**` from `E402` (module-level import not at top of file) for
this reason. See [code style](../../docs/development/code-style.md).

Import chains that exist today include:

- `mage/magefactions.py` imports languages, materials, mediums, spheres, paradigms and
  practices;
- `mage/practices_INC.py` imports abilities and instruments; `mage/paradigms_INC.py`
  imports tenets, which imports practices;
- `vampire/vampire_bloodlines.py` imports clans and disciplines;
- `demon/demon_lores.py`, `demon/demon_rituals*.py`, `demon/demon_relics*.py` and
  `demon/demon_visages.py` import `demon/demon_houses.py`;
- `merits_and_flaws_INC.py` and `demon/demon_merits_and_flaws.py` import the
  `ObjectType` rows from `objects.py`.

[gamelines](gamelines.md) lists every script's imports.

Avoid import cycles: a cycle makes Python import a partially executed module, and the
names it has not bound yet raise `ImportError`.

## Idempotency

`populate_gamedata` runs every script on every load, and a script that others import
runs once on import and again in its own turn. Every script must therefore be safe to
run any number of times:

- Create rows with `get_or_create()` (or `update_or_create()`), never bare
  `create()`.
- `get_or_create(**kwargs)` looks the row up by **all** keyword arguments except
  `defaults`. Put the identifying fields in the lookup and everything else in
  `defaults`:

  ```python
  detective = CharacterTemplate.objects.get_or_create(
      name="Detective",
      gameline="vtm",
      defaults={"character_type": "vampire", "concept": "Detective", ...},
  )
  ```

  Many older scripts pass descriptive fields (descriptions, weaknesses, URLs) in the
  lookup. Changing such a value and reloading adds a second row instead of updating
  the first. When you edit one of those records, move the descriptive fields into
  `defaults` or update the existing row explicitly.
- Many-to-many `.add()`, `add_source()` and `MeritFlaw.add_ratings()` are safe to
  repeat.
- Remember that `defaults` apply only on creation; `get_or_create` never updates an
  existing row. Use `update_or_create` when a reload should change stored values.

## Sharing objects between scripts

Bind any object that another script might need to a module-level name, taking the
instance out of the `(object, created)` tuple:

```python
# populate_db/objects.py
human = ObjectType.objects.get_or_create(name="human", type="char", gameline="wod")[0]
```

Other scripts then `from populate_db.objects import human`. Some scripts bind the whole
tuple instead (for example the effects in `mage/effects_INC.py`); code that imports
those names indexes `[0]` itself. Check which form a script uses before importing from
it.

## Citing sources

Reference objects built on `core.models.Model` (and `core.HouseRule`) have
`add_source(book_title, page_number)`. It calls `Book.objects.get_or_create(name=
book_title)`, then `BookReference.objects.get_or_create(book=..., page=...)`, and adds
the reference to `sources`. It returns the object, so it chains:

```python
Specialty.objects.get_or_create(name="Long Jumping", stat="strength")[0].add_source(
    "Changeling: the Dreaming 20th Anniversary Edition", 160
)
```

The title must match a `name` in `00_books.py` exactly, including capitalisation. A
title that does not match creates a new `Book` with only a name and the model
defaults (`gameline="wod"`, `edition="1e"`), which then appears as a separate book.
`core/tests/management/commands/test_populate_gamedata_sources.py` fails when a cited
title (an `add_source()` argument or a `source_book=` value) names no book in
`00_books.py`; its `AMBIGUOUS_TITLES` lists the few bare Tradition Book titles that do not
say which edition they cite.

## See also

- [Loading](loading.md)
- [Adding data](adding-data.md)
- [Gamelines](gamelines.md)
- [Code style](../../docs/development/code-style.md)
- [populate_db overview](../README.md)
