# Writing a tg_schema migration

This page is the short reference for adding a migration to `tg_schema`: the file and
naming conventions, which existing migration to copy for each kind of change, and the
review checklist. It is for developers changing a model. The full walkthrough, with
worked examples for a column, a backfill, a constraint, a new table and their tests, is
[changing the schema](../../docs/guides/changing-the-schema.md); the reasons behind the
rules are in [schema migrations](../../docs/architecture/schema-migrations.md).

## When you need one

| Change | Migration |
|--------|-----------|
| New field (column) on an existing model | Yes: add the column if missing |
| New `Meta.constraints` / `Meta.indexes` entry, or `unique=True` | Yes: clean the data, then create it if no equivalent exists |
| Rows that must be rewritten for the new code to work | Yes: a guarded data fix |
| New model (table) | Yes: create the table if missing |
| Rename of a field, column, model or `db_table` | Yes: rename on existing databases; earlier migrations then skip the old name |
| Methods, properties, `verbose_name`, `help_text`, choice labels | No |

Fresh and test databases build tables from the current models, so the migration exists
only for databases created by an older release.

## File conventions

- Path: `tg_schema/migrations/NNNN_<snake_case_name>.py`, the next number after the
  highest existing one.
- `dependencies = [("tg_schema", "<previous migration name>")]`: the chain is linear.
- One operation: `migrations.RunPython(<forward>, migrations.RunPython.noop)`.
- A module docstring that says what the migration adds and, for data changes, which rows
  it rewrites and the rule it applies.
- Imports: `django.db.migrations`, other Django modules and `tg_schema.schema`; never a
  local app (`accounts`, `characters`, `core`, `game`, `items`, `locations`, `widgets`).
- The forward function takes `(apps, schema_editor)`, ignores `apps`, and does all work
  through `schema_editor` or `schema_editor.connection` (querysets use
  `.using(schema_editor.connection.alias)`).

```python
"""Add Scene.summary to databases created before it existed."""

from django.db import migrations

from tg_schema.schema import add_missing_columns


def add_scene_summary(apps, schema_editor):
    add_missing_columns(schema_editor, "game.Scene", ("summary",))


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0008_unique_scene_read_status")]
    operations = [migrations.RunPython(add_scene_summary, migrations.RunPython.noop)]
```

## What to copy

| Kind of change | Copy | Pattern |
|----------------|------|---------|
| New columns | [`0005`](../migrations/0005_story_chronicle.py), [`0006`](../migrations/0006_sheet_cover_facts.py) | `add_missing_columns(schema_editor, label, names)` |
| New column plus backfill | [`0004`](../migrations/0004_scene_rolls_and_read_marker.py) | Backfill only if the returned set contains the column |
| Fix rows of existing columns | [`0003`](../migrations/0003_discipline_property_names.py), [`0007`](../migrations/0007_assign_story_chronicles.py) | `live_model`/`live_field`, return if `None`, filter to rows still in the old state |
| Unique index or constraint | [`0008`](../migrations/0008_unique_scene_read_status.py) | Raw SQL on constant table and column names; check `table_names`/`table_columns`; clean data; create only if introspection finds none |
| New table | none yet | Guard with `table_names()`, then `schema_editor.create_model(live_model(label))`; see the guide |

## Tests

Add `tg_schema/tests/test_<name without the number>.py` using `TransactionTestCase`, and
load the migration with
`importlib.import_module("tg_schema.migrations.NNNN_<name>")` (the module name starts
with a digit). Tests may import models. Cover, as they apply:

- the column is added when missing (remove it with `schema_editor.remove_field`, run the
  forward function with `None` as `apps`, restore it with `addCleanup`);
- no SQL is issued when the column exists (`connection.schema_editor(collect_sql=True)`
  and `collected_sql == []`);
- a backfill or data fix changes exactly the intended rows, and a rerun changes nothing;
- a renamed or missing column or model makes the migration skip.

The generic tests in [`tests/test_schema_helpers.py`](../tests/test_schema_helpers.py)
pick up the new file automatically: it must import no local app and must run with every
model lookup failing.

```bash
python manage.py test tg_schema
```

## Checklist

- [ ] The model change gives new columns `null=True` or a default, and declares
      constraints and indexes in `Meta`.
- [ ] Next number, linear dependency, one `RunPython`, `RunPython.noop` reverse.
- [ ] No imports from local apps; models and fields looked up with `live_model` and
      `live_field`, or raw SQL on constant names.
- [ ] Returns early when anything it needs is gone; never raises for a missing model,
      field, table or column.
- [ ] Idempotent: a second run changes nothing.
- [ ] Docstring explains the change and any data rule.
- [ ] A comment on the model points to the migration when the model relies on it.
- [ ] Tests in `tg_schema/tests/`.

## See also

- [Changing the schema](../../docs/guides/changing-the-schema.md)
- [Schema migrations](../../docs/architecture/schema-migrations.md)
- [Migrations](migrations.md)
- [`tg_schema/schema.py`](../schema.py)
