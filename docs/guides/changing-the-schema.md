# Changing the schema

This guide is the procedure for adding or changing a model field, constraint, index or table,
or rewriting stored data, so that the change reaches fresh databases, test databases and
databases that already exist. It is for anyone editing a model in `accounts`, `characters`,
`core`, `game`, `items` or `locations`. The concepts behind it (why local apps have
no committed migrations, how `update.sh` and the test runner build tables) are in
[Schema migrations](../architecture/schema-migrations.md); read that page first if the rules
below look unusual.

## Prerequisites

- You know which model changes and whether existing rows need new values.
- You have read [`tg_schema/schema.py`](../../tg_schema/schema.py) (five helpers, about 60
  lines) and one existing migration of the same kind (table below).

## Decide what the change needs

| Change | Model edit | `tg_schema` migration | Pattern to copy |
|--------|------------|-----------------------|-----------------|
| New field (column) on an existing model | Yes | Yes: add the column | [`0005_story_chronicle.py`](../../tg_schema/migrations/0005_story_chronicle.py), [`0006_sheet_cover_facts.py`](../../tg_schema/migrations/0006_sheet_cover_facts.py) |
| New field whose existing rows need computed values | Yes | Yes: add, then backfill in the same function | [`0004_scene_rolls_and_read_marker.py`](../../tg_schema/migrations/0004_scene_rolls_and_read_marker.py) |
| Data fix on columns that already exist | No | Yes: filtered, idempotent update | [`0003_discipline_property_names.py`](../../tg_schema/migrations/0003_discipline_property_names.py), [`0007_assign_story_chronicles.py`](../../tg_schema/migrations/0007_assign_story_chronicles.py) |
| New unique constraint or index | Yes (`Meta.constraints` / `Meta.indexes`) | Yes: clean the data, then raw SQL guarded by introspection | [`0008_unique_scene_read_status.py`](../../tg_schema/migrations/0008_unique_scene_read_status.py) |
| New model (new table) | Yes | Yes: create the table when it is missing (no helper exists; see [below](#a-new-table)) | none yet |
| Renamed or removed field, model or table | Yes | Yes: the migration of that release performs the rename; older migrations skip the old name | none yet |
| Reordered chargen steps of a workflow | No (`characters/chargen/definitions.py`) | Yes: move `creation_status` of unfinished characters | see [Adding a chargen step](adding-a-chargen-step.md) |
| Python only: a method, property, `verbose_name`, `help_text`, choice label | Yes | No | |

Never commit a file from a local app's `migrations/` directory. `.gitignore` ignores
`*/migrations/*` except `tg_schema/migrations/__init__.py` and `tg_schema/migrations/[0-9]*.py`,
so `makemigrations` output stays on your machine.

## Steps

The running example adds a nullable text column `summary` to `game.Scene`. It is illustrative:
`Scene` has no such field.

### 1. Change the model

Declare the field on the model. Fresh and test databases get their tables from the models, so
the model is the source of truth for them.

```python
# game/models.py, class Scene
summary = models.TextField(default="", blank=True)  # legacy databases: tg_schema 0009
```

- Give every new column `null=True` or a default, so rows that existed before the column
  are valid.
- Declare constraints and indexes in `Meta` with a `name`; a raw-SQL migration uses the same
  name (`game.models.UserSceneReadStatus.Meta.constraints` declares
  `unique_user_scene_read_status`, the index name
  [0008](../../tg_schema/migrations/0008_unique_scene_read_status.py) creates).
- When the model relies on the migration, leave a one-line comment pointing at it, as
  [`locations/models/mage/chantry.py`](../../locations/models/mage/chantry.py) (0002) and
  `game.models.UserSceneReadStatus` (0008) do.
- If the field is editable, add it to the explicit field list of the form or view that edits
  it. Character CRUD field lists live in
  [`characters/forms/core/crud_fields.py`](../../characters/forms/core/crud_fields.py) and are
  pinned by a baseline test (see [Adding a character type](adding-a-character-type.md#3-forms)).

### 2. Write the `tg_schema` migration

Create `tg_schema/migrations/NNNN_<snake_name>.py` with the next number. Today the last one is
`0008_unique_scene_read_status`.

```python
"""Add Scene.summary to databases created before it existed."""

from django.db import migrations

from tg_schema.schema import add_missing_columns


def add_scene_summary(apps, schema_editor):
    # ``game`` has no migration state on legacy installations: the live model
    # describes the column (see tg_schema.schema).
    add_missing_columns(schema_editor, "game.Scene", ("summary",))


# Reversing this migration leaves the column in place (RunPython.noop).


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0008_unique_scene_read_status")]
    operations = [migrations.RunPython(add_scene_summary, migrations.RunPython.noop)]
```

Rules every migration follows (the first three are enforced by
[`tg_schema/tests/test_schema_helpers.py`](../../tg_schema/tests/test_schema_helpers.py)):

1. **Import no app model.** No `from game...`, `from characters...` or any other local app
   (`NoModelImportsTests` parses the file). Look models and fields up when the function runs
   with `live_model("app.Model")` and `live_field(model, "name")`, or name the table in raw
   SQL. A later release that renames the model must be able to skip this migration instead
   of crashing every `migrate`.
2. **Ignore the `apps` argument.** Local apps have no migration state on the databases these
   migrations serve, so the historical registry lacks their models. The guard test calls every
   migration as `operation.code(None, editor)`.
3. **Skip, never fail, when something is gone.** Return early when `live_model` or
   `live_field` returns `None`, or the table or a column is missing.
   `test_every_migration_runs_when_its_models_are_gone` runs each migration with every model
   lookup failing.
4. **One `RunPython` operation, `migrations.RunPython.noop` as the reverse**, and a linear
   `dependencies` entry on the previous migration.
5. **Use the migration's connection**: `schema_editor` for DDL,
   `.using(schema_editor.connection.alias)` for querysets, `schema_editor.connection.cursor()`
   for raw SQL.
6. **Explain the change in the module docstring**: what it adds, which rows it rewrites and
   why, and any merge rule it applies.

#### The helpers

| Helper ([`tg_schema/schema.py`](../../tg_schema/schema.py)) | Returns |
|--------|---------|
| `live_model("app.Model")` | The model as the code defines it now, or `None` |
| `live_field(model, "name")` | The field, or `None` (also when `model` is `None`) |
| `table_names(connection)` | Set of table names in the database |
| `table_columns(connection, table)` | Set of column names of `table` |
| `add_missing_columns(schema_editor, "app.Model", names)` | Adds each named field whose column the table lacks; skips a missing model, table or field; returns the set of names it added |

#### A backfill

When existing rows need values computed from other data, backfill in the same function and
only when this run added the column, as
[0004](../../tg_schema/migrations/0004_scene_rolls_and_read_marker.py) does. The live model then
matches the data being written.

```python
def add_scene_summary(apps, schema_editor):
    added = add_missing_columns(schema_editor, "game.Scene", ("summary",))
    if "summary" in added:
        Scene = live_model("game.Scene")
        Scene.objects.using(schema_editor.connection.alias).filter(summary="").update(
            summary="Imported scene"
        )
```

A data fix on columns that already exist filters to rows still in the old state, so a second
run changes nothing: [0003](../../tg_schema/migrations/0003_discipline_property_names.py)
updates only `property_name=""`, and
[0007](../../tg_schema/migrations/0007_assign_story_chronicles.py) only stories with
`chronicle__isnull=True`. Both return first when a field they need is gone.

#### A constraint or index

Follow [0008](../../tg_schema/migrations/0008_unique_scene_read_status.py):

1. Name the table, the columns it touches and the index as module constants
   (`TABLE`, `COLUMNS`, `INDEX`), so later model changes cannot change what the migration does.
2. Return unless `TABLE in table_names(connection)` and `COLUMNS <= table_columns(connection, TABLE)`.
3. Quote identifiers with `connection.ops.quote_name`.
4. Make the data valid first (0008 deletes orphan rows and merges duplicates into the oldest
   row) and document the rule in the docstring.
5. Create the constraint only if introspection (`connection.introspection.get_constraints`)
   finds no equivalent one; a fresh database already has it from `Meta.constraints`.

On a host that keeps generated migrations, the generated `AddConstraint` runs before your
migration and fails on data your migration would have cleaned. Say so in the pull request, so
the release follows the cleanup step in
[Maintenance](../operations/maintenance.md#releasing-a-schema-change).

#### A new table

`tg_schema/schema.py` has no helper for creating a table. Guard with `table_names()` and create
the table from the live model:

```python
def add_example_table(apps, schema_editor):
    model = live_model("game.Example")
    if model is None or model._meta.db_table in table_names(schema_editor.connection):
        return
    schema_editor.create_model(model)
```

`schema_editor.create_model` is Django's schema-editor API; it also creates the tables of the
model's automatic many-to-many fields. If you turn this into a helper in `tg_schema/schema.py`,
test it in `tg_schema/tests/test_schema_helpers.py`.

### 3. Test the migration

Add `tg_schema/tests/test_<name without number>.py`. Use `TransactionTestCase` (schema editors
need it) and import the module by name, because it starts with a digit. Model imports are
allowed in tests.

```python
"""tg_schema 0009 adds Scene.summary exactly once."""

import importlib

from django.db import connection
from django.test import TransactionTestCase

from game.models import Scene

migration = importlib.import_module("tg_schema.migrations.0009_scene_summary")


def scene_columns():
    with connection.cursor() as cursor:
        return {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, Scene._meta.db_table
            )
        }


class SceneSummaryMigrationTests(TransactionTestCase):
    def field(self):
        return Scene._meta.get_field("summary")

    def restore_column(self):
        if self.field().column not in scene_columns():
            with connection.schema_editor() as editor:
                editor.add_field(Scene, self.field())

    def test_adds_the_missing_column(self):
        self.addCleanup(self.restore_column)
        with connection.schema_editor() as editor:
            editor.remove_field(Scene, self.field())
        with connection.schema_editor() as editor:
            migration.add_scene_summary(None, editor)
        self.assertIn("summary", scene_columns())

    def test_existing_column_is_left_alone(self):
        with connection.schema_editor(collect_sql=True) as editor:
            migration.add_scene_summary(None, editor)
            self.assertEqual(editor.collected_sql, [])
```

Cover every case that applies:

| Case | Existing example |
|------|------------------|
| Adds the column when missing (on SQLite, drop and re-add one column at a time: removing a field rebuilds the table from the live model) | [`test_story_chronicle.py`](../../tg_schema/tests/test_story_chronicle.py), [`test_sheet_cover_facts.py`](../../tg_schema/tests/test_sheet_cover_facts.py) |
| Issues no SQL when the column exists (`collect_sql=True`, `collected_sql == []`) | same modules |
| Backfills the right rows and leaves the rest | [`test_scene_rolls_and_read_marker.py`](../../tg_schema/tests/test_scene_rolls_and_read_marker.py), [`test_assign_story_chronicles.py`](../../tg_schema/tests/test_assign_story_chronicles.py) |
| A second run changes nothing | `test_assign_story_chronicles.py` |
| Cleans data and adds a constraint on a legacy table | [`test_unique_scene_read_status.py`](../../tg_schema/tests/test_unique_scene_read_status.py) (rebuilds the table without the constraint first) |
| Skips when a column or model is renamed (patch the module constant or lookup) | `test_unique_scene_read_status.py` |

A data-only migration can be called with a stand-in editor,
`migration.assign_story_chronicles(None, SimpleNamespace(connection=connection))`, as
`test_assign_story_chronicles.py` does.

Run the app's tests with `python manage.py test tg_schema`.

### 4. Check the rest of the change

- Model, form and view tests for the new field (see [Testing](../development/testing.md)).
- A new character model or item/location model has more to register; follow
  [Adding a character type](adding-a-character-type.md) or
  [Adding an item or location type](adding-an-item-or-location-type.md).
- After `setup_db.sh` or `python manage.py reset_db`, which delete every non-`__init__.py`
  file in every `*/migrations/` directory including `tg_schema/migrations/`, restore the
  committed migrations with `git checkout -- tg_schema/migrations` before you commit.

## Checklist

- [ ] The model declares the field, constraint or index; new columns are nullable or defaulted.
- [ ] No file under a local app's `migrations/` besides `__init__.py` is staged.
- [ ] `tg_schema/migrations/NNNN_<name>.py`: next number, linear dependency, one `RunPython`
  with a `noop` reverse, docstring explains the change.
- [ ] No imports from local apps; `apps` unused; lookups through `tg_schema.schema`.
- [ ] Returns early when its model, field, table or columns are gone.
- [ ] A second run issues no SQL and rewrites no rows (or, for a positional remap, see
  [Adding a chargen step](adding-a-chargen-step.md#reordering-steps)).
- [ ] Backfills touch only rows still in the old state.
- [ ] Raw SQL uses module constants, `quote_name` and an introspection guard.
- [ ] `tg_schema/tests/test_<name>.py` covers add, no-op, backfill and skip as applicable.
- [ ] Model comment points at the migration where the model relies on it.

## See also

- [Schema migrations](../architecture/schema-migrations.md)
- [`tg_schema/schema.py`](../../tg_schema/schema.py)
- [`tg_schema/migrations/`](../../tg_schema/migrations/)
- [Data model](../architecture/data-model.md)
- [Testing](../development/testing.md)
