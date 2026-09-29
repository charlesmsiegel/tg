# Schema migrations

This page explains how database tables are created and changed in this project, which differs
from a standard Django project: the local apps commit no migration history, and a separate app,
`tg_schema`, holds guarded migrations that bring older databases up to date. Read it before you
add or change a model field, constraint, index or table, or write a data fix for existing rows.
The step-by-step recipe is in [Changing the schema](../guides/changing-the-schema.md).

## Where a database's tables come from

| Database | Tables come from |
|----------|------------------|
| Test database | The current models. `tg.test_runner.LocalMigrationTestRunner` disables migrations for local apps that have none, Django creates their tables directly, then the `tg_schema` migrations run and find nothing to do. |
| Fresh installation | [`setup_db.sh`](../../setup_db.sh) runs `reset_db --yes`, `makemigrations` and `migrate`, so each local app gets an initial migration generated from the current models on that machine. |
| Existing installation | [`update.sh`](../../update.sh) runs `git pull`, `makemigrations`, `migrate` and `collectstatic`. Locally generated migrations and the committed `tg_schema` migrations together bring the database up to date. |

## Local apps have no committed migrations

The model-owning apps (`accounts`, `characters`, `core`, `game`, `items`, `locations`) commit
only `migrations/__init__.py`. [`.gitignore`](../../.gitignore) contains:

```text
*/migrations/*
!tg_schema/migrations/__init__.py
!tg_schema/migrations/[0-9]*.py
```

so any migration file generated under a local app stays on the machine that generated it.
Every installation therefore has its own, machine-specific migration files for the local apps,
and a committed change cannot rely on any of them existing or having a particular name. That is
why schema and data changes for existing databases are written as `tg_schema` migrations, which
are committed and identical everywhere.

Do not commit files from a local app's `migrations/` directory.

### The test runner

`TEST_RUNNER` is `tg.test_runner.LocalMigrationTestRunner`
([`tg/test_runner.py`](../../tg/test_runner.py)). Before creating the test databases it looks at
every installed app under `BASE_DIR`; for each one whose `migrations/` directory contains no
`.py` file other than `__init__.py`, it sets `settings.MIGRATION_MODULES[label] = None`. Django
then creates those apps' tables straight from the models, the way it does for apps without
migrations.

Consequences:

- In a clean checkout, test tables always match the current models, including every
  `Meta.constraints` and `Meta.indexes` entry.
- If your working copy contains generated migration files for an app (for example after running
  `setup_db.sh` or `makemigrations`), the runner leaves that app alone and the test database is
  built by running those files. Stale generated files can then make tests fail in ways a clean
  checkout does not.
- `tg_schema` has committed migrations, so they run during test database setup, after the local
  tables exist. Because every one of them is guarded, they make no changes there.

### `reset_db` and `setup_db.sh`

`python manage.py reset_db` ([`core/management/commands/reset_db.py`](../../core/management/commands/reset_db.py))
refuses to run unless `DEBUG` is true. It deletes `db.sqlite3` in the current directory and every
`.py` file except `__init__.py` in every top-level `*/migrations/` directory. That includes the
committed files in `tg_schema/migrations/`. `setup_db.sh` runs it with `--yes`. After running
either, restore the committed migrations before you commit:

```bash
git checkout -- tg_schema/migrations
```

## The `tg_schema` app

[`tg_schema/`](../../tg_schema/) is in `INSTALLED_APPS` and has no models. Its migrations are a
single linear chain of `RunPython` operations that inspect the live database and the current model
classes, and change only what is missing.

### Helpers

[`tg_schema/schema.py`](../../tg_schema/schema.py):

| Helper | Returns |
|--------|---------|
| `live_model("app_label.ModelName")` | The model class as the code defines it now (`apps.get_model`), or `None` if it does not exist. |
| `live_field(model, name)` | The model's field `name`, or `None` if the field does not exist or `model` is `None`. |
| `table_names(connection)` | The set of table names in the database. |
| `table_columns(connection, table)` | The set of column names of `table`. |
| `add_missing_columns(schema_editor, label, names)` | For each field in `names` of model `label` whose column the table lacks, runs `schema_editor.add_field`. Skips a missing model, table or field. Returns the set of field names it added. |

### Rules every `tg_schema` migration follows

| Rule | Why | Enforced by |
|------|-----|-------------|
| Import nothing from the local apps; look models and fields up with `live_model` / `live_field`, or use raw SQL on named tables. | A module-level import of a model breaks every future `migrate` once that model is renamed or removed. | `NoModelImportsTests.test_migrations_import_no_app_models` parses each migration file. |
| Ignore the `apps` argument of the `RunPython` function. | On the databases these migrations serve, the local apps have no migration state, so the historical registry does not contain their models. | `test_every_migration_runs_when_its_models_are_gone` calls each function as `operation.code(None, editor)`. |
| Return early, never fail, when a model, field, table or column is gone. | A later release that renames or removes it owns that change; the old migration must keep running. | `test_every_migration_runs_when_its_models_are_gone` patches `apps.get_model` to raise `LookupError` and runs every migration. |
| Be idempotent: add only missing columns, filter data fixes to rows still in the old state, check for a constraint before creating it. | Fresh and test databases already match the models, and a migration may meet a database that was patched another way. | Per-migration tests ("existing columns are left alone", "a rerun changes nothing"). |
| Run a backfill that depends on a new column only when `add_missing_columns` reports that column as added. | In that release the model matches the data being written; on later releases the model may have moved on. | `0004` and its test. |
| Query through the migration's connection (`.using(schema_editor.connection.alias)`, `schema_editor.connection.cursor()`). | Migrations can run against a non-default database alias. | Code review. |
| In raw SQL, name the table, columns and index as module constants, quote them with `connection.ops.quote_name`, and check them with `table_names` / `table_columns` first. | The live model must not change what an old migration does. | `0008` and its test. |
| Use `migrations.RunPython.noop` as the reverse. | Reversing leaves added columns and fixed data in place. | Code review. |

## Data migrations

A `tg_schema` migration may also rewrite existing rows. The existing ones show the patterns:

- **Backfill a reference field** (`0003`): set `Discipline.property_name` for rows whose
  `name` matches a known discipline field and whose `property_name` is still empty.
- **Backfill with a new column** (`0004`): after adding `UserSceneReadStatus.last_read_post`,
  set the marker for existing rows, only in the run that added the column.
- **Derive a relation** (`0007`): give each unassigned `Story` the chronicle its characters
  share, found through `StoryXPRequest`; stories whose characters span several chronicles, or
  have none, stay unassigned. Assigned stories are never touched.
- **Clean data before a constraint** (`0008`): delete rows whose user or scene is gone, merge
  duplicate `(user, scene)` rows into the oldest (read only if every copy was, with the newest
  marker), then create the unique index unless one exists.

Document the rule a data migration applies in its module docstring.

## The migrations

| Migration | Changes | Kind |
|-----------|---------|------|
| [`0001_scene_visibility`](../../tg_schema/migrations/0001_scene_visibility.py) | Adds `game.Scene.visibility`. | Column |
| [`0002_chantry_rating_linked_object`](../../tg_schema/migrations/0002_chantry_rating_linked_object.py) | Adds `locations.ChantryBackgroundRating.linked_location` and `linked_character`. | Column |
| [`0003_discipline_property_names`](../../tg_schema/migrations/0003_discipline_property_names.py) | Fills empty `characters.Discipline.property_name` from a fixed list of discipline field names (case-insensitive name match). | Data |
| [`0004_scene_rolls_and_read_marker`](../../tg_schema/migrations/0004_scene_rolls_and_read_marker.py) | Adds `game.Post.roll` and `game.UserSceneReadStatus.last_read_post`; when the marker column is new, sets it to the scene's latest post for read rows and to the user's own latest post in the scene for unread rows. | Column and data |
| [`0005_story_chronicle`](../../tg_schema/migrations/0005_story_chronicle.py) | Adds `game.Story.chronicle`. | Column |
| [`0006_sheet_cover_facts`](../../tg_schema/migrations/0006_sheet_cover_facts.py) | Adds `characters.Werewolf.deed_name`. | Column |
| [`0007_assign_story_chronicles`](../../tg_schema/migrations/0007_assign_story_chronicles.py) | Assigns unassigned stories to the one chronicle their `StoryXPRequest` characters share. | Data |
| [`0008_unique_scene_read_status`](../../tg_schema/migrations/0008_unique_scene_read_status.py) | Deletes orphaned `game_userscenereadstatus` rows, merges duplicates, and adds the unique index `unique_user_scene_read_status` on `(user_id, scene_id)`. Raw SQL. | Data and constraint |

Models that rely on a migration say so in a comment, for example
`game.models.UserSceneReadStatus` (0008) and `locations.models.mage.chantry` (0002).

## How `update.sh` interacts with `tg_schema`

`update.sh` runs `makemigrations` before `migrate`. On an installation that keeps generated
migration files for the local apps, a new model field produces two changes in the same
`migrate` run: the locally generated `AddField` migration and the committed `tg_schema`
migration. Django builds its plan from the leaf migration of each app in sorted app-label order,
and every local app with models (`accounts`, `characters`, `core`, `game`, `items`, `locations`)
sorts before `tg_schema`, so the generated migration adds the column first and the guarded
`tg_schema` migration finds it present and does nothing. On a database whose local migration
state does not record the change, the generated migration does not exist or is already marked
applied, and the `tg_schema` migration adds the column.

Run the two commands in that order. If `migrate` runs on its own after a pull that adds a
field, `tg_schema` adds the column; a later `makemigrations` then generates an `AddField` for a
column that already exists, and applying it fails. Mark such a generated migration as applied
with `python manage.py migrate <app_label> <migration_name> --fake`.

The same order matters for a constraint that existing data may violate. The host's generated
migration adds the constraint before the `tg_schema` migration that cleans the data runs, so on
a database with violating rows `migrate` stops at the generated migration. For 0008 (unique
user and scene on `UserSceneReadStatus`) that means duplicate read-status rows. Clean the data
first by calling the `tg_schema` migration's function directly, then run `migrate` as usual;
the migration later finds the data clean and the constraint present. The procedure is in
[Maintenance](../operations/maintenance.md#releasing-a-schema-change).

## Changing the schema: summary

1. Change the model. Give a new column `null=True` or a default so rows that predate it are
   valid. Declare constraints and indexes in `Meta`, because fresh and test databases get them
   from there.
2. Add `tg_schema/migrations/NNNN_<name>.py` with the next number,
   `dependencies = [("tg_schema", "<previous migration>")]` and one `RunPython` operation
   (`add_missing_columns` for new columns; a guarded, idempotent function for data or
   constraints).
3. Add tests in `tg_schema/tests/` (below).
4. Leave a comment on the model pointing at the migration when the model relies on it.
5. A new table (a new model) also needs a guarded migration for existing databases; there is no
   helper for it yet, so guard with `table_names()`.
6. A change that only affects Python (methods, properties, `verbose_name`, `help_text`, choice
   labels) needs no migration.

Renaming a column, table or `db_table` needs a migration that performs the rename on existing
databases; earlier migrations then skip the old name.

## Tests

`tg_schema` tests live in [`tg_schema/tests/`](../../tg_schema/tests/), one module per migration
(`test_<migration name without its number>.py`). Use `TransactionTestCase`, because the tests
run schema editors, and import the migration with
`importlib.import_module("tg_schema.migrations.NNNN_name")`, since the module name starts with a
digit.

| Case | Example |
|------|---------|
| Adds each missing column (remove the field with `schema_editor.remove_field`, run, assert the column exists; restore in `addCleanup`). | `test_story_chronicle.py`, `test_sheet_cover_facts.py`, `test_chantry_rating_linked_object.py` |
| Leaves existing columns alone (run inside `connection.schema_editor(collect_sql=True)` and assert no SQL). | Same modules |
| Backfills the right rows. | `test_scene_rolls_and_read_marker.py`, `test_assign_story_chronicles.py` |
| Cleans data and adds a constraint on a legacy table. | `test_unique_scene_read_status.py` |
| Skips when a column or model has been renamed. | `test_unique_scene_read_status.py`, `test_schema_helpers.py` |

[`tg_schema/tests/test_schema_helpers.py`](../../tg_schema/tests/test_schema_helpers.py) holds
the generic guards (no model imports; every migration runs when its models are gone). They cover
new migrations automatically. See [Testing](../development/testing.md) for how to run them.

## See also

- [Changing the schema](../guides/changing-the-schema.md)
- [Data model](data-model.md)
- [`tg_schema/README.md`](../../tg_schema/README.md)
- [`tg/README.md`](../../tg/README.md)
- [Maintenance](../operations/maintenance.md)
