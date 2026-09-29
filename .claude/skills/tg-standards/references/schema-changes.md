# Schema changes and tg_schema migrations

How a change to tables, columns, constraints or stored data reaches every database, and
what a `tg_schema` migration must look like. Read this before touching a model field,
`Meta.constraints`, `Meta.indexes`, a table name, or data that existing rows must be
rewritten for. The concepts are explained in
[docs/architecture/schema-migrations.md](../../../../docs/architecture/schema-migrations.md)
and walked through in
[docs/guides/changing-the-schema.md](../../../../docs/guides/changing-the-schema.md).

## How schema reaches a database

| Database | Where its tables come from |
|----------|----------------------------|
| Test database | `tg.test_runner.LocalMigrationTestRunner` sets `MIGRATION_MODULES[label] = None` for every project app whose `migrations/` holds only `__init__.py`, so Django creates those tables from the current models. `tg_schema` migrations then run and find nothing to do. |
| Fresh install | `setup_db.sh` runs `reset_db --yes`, `makemigrations`, `migrate`: the local apps get migrations generated from the current models on that machine. |
| Existing database | `update.sh` runs `git pull`, `makemigrations`, `migrate`. The committed `tg_schema` migrations bring databases whose local-app tables predate a change up to date, each change once. |

Facts behind the rules:

- Local apps (`accounts`, `characters`, `core`, `game`, `items`, `locations`, `widgets`)
  commit only `migrations/__init__.py`. `.gitignore` has `*/migrations/*` with
  exceptions for `tg_schema/migrations/__init__.py` and `tg_schema/migrations/[0-9]*.py`.
- `tg_schema` ([`tg_schema/`](../../../../tg_schema/)) has no models. Its migrations are
  `RunPython` operations that inspect the live database and the current models.
- `core/management/commands/reset_db.py` deletes every non-`__init__.py` file in every
  top-level `*/migrations/` directory, `tg_schema/migrations/` included. After running it
  (or `setup_db.sh`), restore the committed files with
  `git checkout -- tg_schema/migrations` before you commit.

## Which changes need a tg_schema migration

| Change | Needs a migration? | Pattern |
|--------|--------------------|---------|
| New field (column) on an existing model | Yes | `add_missing_columns` ([0001](../../../../tg_schema/migrations/0001_scene_visibility.py), [0005](../../../../tg_schema/migrations/0005_story_chronicle.py), [0006](../../../../tg_schema/migrations/0006_sheet_cover_facts.py)) |
| New column plus values for existing rows | Yes | add, then backfill only if this run added it ([0004](../../../../tg_schema/migrations/0004_scene_rolls_and_read_marker.py)) |
| Data fix or backfill on existing columns | Yes | idempotent filter, skip when a field is gone ([0003](../../../../tg_schema/migrations/0003_discipline_property_names.py), [0007](../../../../tg_schema/migrations/0007_assign_story_chronicles.py)) |
| New unique constraint or index | Yes | clean the data, then raw SQL guarded by introspection ([0008](../../../../tg_schema/migrations/0008_unique_scene_read_status.py)) |
| Renamed or removed field, model or table | Yes | the renaming release owns the change; earlier migrations skip |
| Reordered chargen steps | Yes | move `creation_status` of unfinished characters (the registry docstring in `characters/chargen/registry.py` says so) |
| New model (new table) | Yes, for existing databases | no helper exists yet; guard with `table_names()` and add a helper plus test to `tg_schema/schema.py` |
| Python-only change (method, property, `verbose_name`, `help_text`, choices label) | No | |

## The helpers

[`tg_schema/schema.py`](../../../../tg_schema/schema.py):

| Helper | Returns |
|--------|---------|
| `live_model("app.Model")` | The model as the code defines it now, or `None` if it no longer exists |
| `live_field(model, "name")` | The field, or `None` (also `None` when `model` is `None`) |
| `table_names(connection)` | Set of table names in the database |
| `table_columns(connection, table)` | Set of column names of `table` |
| `add_missing_columns(schema_editor, "app.Model", names)` | Adds each named field whose column the table lacks; skips a missing model, table or field; returns the set of names added |

## Rules for a tg_schema migration

1. **File and chain.** `tg_schema/migrations/NNNN_snake_name.py`, the next number,
   `dependencies = [("tg_schema", "<previous>")]`. One `RunPython` operation with
   `migrations.RunPython.noop` as its reverse (reversing leaves columns in place; say so
   in a comment).
2. **No model imports.** Import nothing from `accounts`, `characters`, `core`, `game`,
   `items`, `locations` or `widgets`. Use `live_model` / `live_field`, or raw SQL on named
   tables. `NoModelImportsTests` parses every migration and fails otherwise.
3. **Ignore the `apps` argument.** Local apps have no migration state on the databases
   these migrations serve, so the historical registry lacks their models. The guard test
   calls each migration's function as `operation.code(None, editor)`.
4. **Skip, never fail, when something is gone.** Return early when `live_model` or
   `live_field` gives `None`, or when the table or a column is missing.
   `test_every_migration_runs_when_its_models_are_gone` patches `apps.get_model` to raise
   `LookupError` and runs every migration.
5. **Idempotent.** Add only missing columns; filter backfills to rows still in the old
   state (`property_name=""`, `chronicle__isnull=True`); check for an existing constraint
   before creating one. Running twice changes nothing the second time.
6. **Backfill in the release that adds the column.** When a backfill depends on the new
   column, run it only if `add_missing_columns` reports that name as added (0004); the
   models then match the data being written.
7. **Use the migration's connection.** Query with `.using(schema_editor.connection.alias)`
   and run DDL through `schema_editor` or `schema_editor.connection.cursor()`.
8. **Raw SQL is self-contained.** Name the table, columns and index as module constants,
   quote with `connection.ops.quote_name`, and check `COLUMNS <= table_columns(...)`
   before touching them (0008). The live model must not change what an old migration does.
9. **Make data safe before a constraint.** Delete or merge rows that would violate it,
   and document the merge rule in the module docstring (0008 keeps the oldest row, read
   only if every copy was, with the newest marker). A host's generated `AddConstraint`
   runs before `tg_schema` (app-label order) and fails on dirty data, so flag the release:
   operators clean the data first ([maintenance](../../../../docs/operations/maintenance.md#releasing-a-schema-change)).
10. **Explain in the docstring** what the migration adds, which rows it rewrites and why.

## Model side of the same change

- Declare the field, index or constraint on the model: fresh and test databases get it
  from there. Example: `game.models.UserSceneReadStatus.Meta.constraints` declares
  `unique_user_scene_read_status`, the name 0008 uses for its index.
- Give new columns `null=True` or a default so rows that existed before the column are
  valid. `UserSceneReadStatus` keeps `user` and `scene` nullable "for legacy databases".
- Leave a one-line comment on the model pointing at the migration when the model relies on
  it (see `locations/models/mage/chantry.py` and `game/models.py`).
- Do not rename a column, table or `db_table` without a migration that performs the
  rename on existing databases.

## Minimal example

```python
"""Add Chronicle.tagline to databases created before it existed."""

from django.db import migrations

from tg_schema.schema import add_missing_columns


def add_chronicle_tagline(apps, schema_editor):
    # ``game`` has no migration state on legacy installations: the live model
    # describes the column (see tg_schema.schema).
    add_missing_columns(schema_editor, "game.Chronicle", ("tagline",))


# Reversing this migration leaves the column in place (RunPython.noop).


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0008_unique_scene_read_status")]
    operations = [migrations.RunPython(add_chronicle_tagline, migrations.RunPython.noop)]
```

`Chronicle.tagline` is a hypothetical field; the pattern is that of 0005 and 0006.

## Tests for a migration

Put them in `tg_schema/tests/test_<migration_name_without_number>.py` and use
`TransactionTestCase` (schema editors need it). Import the module with
`importlib.import_module("tg_schema.migrations.NNNN_name")` because the name starts with a
digit. Cover:

| Case | How the existing tests do it |
|------|------------------------------|
| Adds the column when missing | `editor.remove_field(model, field)`, run the function, assert the column exists; on SQLite drop one column at a time and restore in `addCleanup` (`test_sheet_cover_facts.py`) |
| No SQL when already present | run inside `connection.schema_editor(collect_sql=True)` and assert `editor.collected_sql == []` |
| Backfill result | create rows in the old state, run, assert the rewritten values (`test_scene_rolls_and_read_marker.py`, `test_assign_story_chronicles.py`) |
| Constraint on a legacy table | rebuild the table without the constraint, insert duplicates, run, assert merge and `IntegrityError` afterwards (`test_unique_scene_read_status.py`) |
| Skip on rename | patch the module's column set or lookups and assert nothing changed |

The generic guards in `tg_schema/tests/test_schema_helpers.py` run for every migration
automatically; do not weaken them.

## Review checklist

- [ ] No generated files under a local app's `migrations/`.
- [ ] Next number, linear dependency, single `RunPython` with `noop` reverse.
- [ ] No imports from local apps; `apps` unused; lookups through `tg_schema.schema`.
- [ ] Returns early when its model, field, table or columns are gone.
- [ ] Idempotent: a second run issues no SQL and changes no rows.
- [ ] Backfill scoped to rows still needing it, run only when the column was just added.
- [ ] Raw SQL uses module constants, `quote_name`, and an introspection guard.
- [ ] Model declares the same schema; new columns nullable or defaulted.
- [ ] Test module covers add, no-op, backfill and skip.

## See also

- [docs/architecture/schema-migrations.md](../../../../docs/architecture/schema-migrations.md)
- [docs/guides/changing-the-schema.md](../../../../docs/guides/changing-the-schema.md)
- [tg_schema/README.md](../../../../tg_schema/README.md)
- [`tg/test_runner.py`](../../../../tg/test_runner.py)
- [models.md](models.md), [testing.md](testing.md)
