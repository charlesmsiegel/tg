# Adding game data

This page gives step-by-step recipes for changing the reference data in
`populate_db/`: adding a record to an existing script, citing its source, adding a
book, adding a new script, and adding a character template. It is for developers and
agents extending the seed data. It assumes the model already exists; to add a new
reference model first, see
[adding reference data](../../docs/guides/adding-reference-data.md).

## Before you start

- Read [conventions](conventions.md): scripts must be safe to rerun, dependencies are
  expressed as imports, and `add_source()` matches book titles exactly.
- Work against a development database with migrations applied.
- Find the script that already loads the model you are adding to:

  ```bash
  grep -rl "from characters.models.vampire.clan import" populate_db
  ```

  [gamelines](gamelines.md) lists every script and the models it loads.

## Add a record to an existing script

1. Open the script and follow the pattern it already uses. Put the fields that
   identify the record in the lookup and the rest in `defaults`:

   ```python
   from characters.models.core.archetype import Archetype

   visionary = Archetype.objects.get_or_create(
       name="Visionary",
       defaults={"description": "..."},
   )[0]
   ```

   Check the model's fields and `clean()` before choosing values. Models built on
   `core.models.Model` (and those using `core.base.ValidatedSaveMixin`) run
   `full_clean()` on save, so a missing name or an out-of-range rating fails the
   script.
2. If the record references rows from another script, import them from that script
   at the point you need them (see
   [imports are load order](conventions.md#imports-are-load-order)).
3. If other scripts will need the new object, bind it to a module-level name.
4. Cite the source (next section).
5. Load the script and check the result:

   ```bash
   python manage.py populate_gamedata --only archetypes --verbose
   python manage.py shell -c "from characters.models.core.archetype import Archetype; print(Archetype.objects.filter(name='Visionary').count())"
   ```

6. Run the same `populate_gamedata` command a second time and confirm the count has
   not changed. A second row means a lookup field changed between runs; move it into
   `defaults`.

## Cite a source

Call `add_source(book_title, page)` on the object. It is available on every
`core.models.Model` subclass (most reference models, including merits and flaws,
specialties, clans, Gifts, effects and rotes) and on `core.HouseRule`:

```python
# populate_db/archetypes.py
activist = Archetype.objects.get_or_create(
    name="Activist",
    description="...",
)[0].add_source("Mage: the Ascension 20th Anniversary Edition", 268)
```

`add_source()` returns the object, so the call can be chained as above.

Copy the title from a `name=` in [`00_books.py`](../00_books.py). A title that does
not match exactly creates a separate `Book` with default values. `add_source()` is
safe to repeat: it reuses the book and the book reference.

## Add a book

Add a `Book.objects.get_or_create(...)` call to [`00_books.py`](../00_books.py), in
the same shape as the existing entries:

```python
Book.objects.get_or_create(
    name="Book of Secrets",
    edition="20th",
    gameline="mta",
    url="https://www.storytellersvault.com/product/214133/M20-The-Book-of-Secrets",
)
```

`edition` is one of `1e`, `2e`, `Rev`, `20th`, `DA`, `VA`, `WW`, `SC`, `KotE`
(default `1e`); `gameline` is a gameline code from `settings.GAMELINE_CHOICES`
(default `wod`); `storytellers_vault` is an optional flag. `Book.clean()` requires a
non-empty name and a valid gameline. Because the existing calls put every field in the
lookup, changing a URL or edition later adds a second book with the same name; update
the stored row instead (for example in the shell) and change the script to match.

## Add a new script

1. Choose the folder: the top level for data every gameline uses, otherwise the
   gameline's folder. The loader finds every `.py` file under `populate_db/`; no
   registration or `__init__.py` is needed.
2. Name the file in lowercase snake case. Include the gameline word (`vampire`,
   `werewolf`, `mage`, `wraith`, `changeling`, `demon`) in the name if you want
   `--gameline` to treat it as gameline-specific.
3. Start with the model imports, then import the scripts whose rows you need.
4. Write `get_or_create` calls as above, binding shared objects to module-level names.
5. Check where it lands in the order and that it runs:

   ```bash
   python manage.py populate_gamedata --dry-run
   python manage.py populate_gamedata --only <part of the new file name> --verbose
   ```

6. Run it twice and confirm nothing was duplicated.

Do not rely on another top-level script having run because its name sorts
earlier; import it. Use an ordering prefix (`00_`, `01_`, `aa_`) only for a top-level
file that others cannot import.

## Add a character template

Character templates are `core.models.CharacterTemplate` rows, loaded by the scripts in
[`character_templates/`](../character_templates/). Add one to the script for its
gameline (or to `faction_templates.py` for faction-specific templates):

```python
from core.models import CharacterTemplate

detective = CharacterTemplate.objects.get_or_create(
    name="Detective",
    gameline="vtm",
    defaults={
        "character_type": "vampire",
        "description": "...",
        "concept": "Detective",
        "basic_info": {"nature": "FK:Archetype:Judge", "demeanor": "FK:Archetype:Professional"},
        "attributes": {"strength": 2, "dexterity": 2, "stamina": 3},
        "abilities": {"alertness": 2, "investigation": 4},
        "backgrounds": [{"name": "Contacts", "rating": 3}],
        "powers": {"auspex": 2, "fortitude": 1},
        "specialties": ["Investigation (Crime Scenes)"],
        "languages": ["English"],
        "equipment": "Detective's badge, 9mm pistol",
        "suggested_freebie_spending": {"disciplines": 5, "backgrounds": 2},
    },
)
```

Rules from the model:

- `(gameline, character_type, name)` is unique.
- `CharacterTemplate.clean()` requires a `character_type` and accepts only the
  gamelines `wod`, `vtm`, `wta`, `mta`, `wto`, `ctd` and `dtf`.
- JSON shapes, from the field help text: `attributes`, `abilities` and `powers` map a
  property name to a rating; `backgrounds` and `merits_flaws` are lists of
  `{"name": ..., "rating": ...}`; `specialties` are `"Ability (Specialty)"` strings;
  `languages` are language names.
- A `basic_info` value of the form `"FK:Archetype:<name>"` is resolved to the
  `Archetype` with that name when the template is applied; other values are copied
  onto the character as they are.
- `is_official` and `is_public` default to `True`.

How templates are applied to characters is described in
[character creation](../../docs/architecture/character-creation.md).

## See also

- [Conventions](conventions.md)
- [Loading](loading.md)
- [Gamelines](gamelines.md)
- [Adding reference data](../../docs/guides/adding-reference-data.md)
- [populate_db overview](../README.md)
