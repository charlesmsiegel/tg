# tg_schema

`tg_schema` holds the project's committed schema and data migrations. The model-owning
apps (`accounts`, `characters`, `core`, `game`, `items`, `locations`) commit no migration
files, so a database created from an older release has no record of later model changes.
The migrations in this app bring such a database up to date: each one checks the live
database and the current models and changes only what is missing. The app has no models.

Read this before you add or change a model field, constraint or table, or need to fix
existing rows. The concepts are explained in
[schema migrations](../docs/architecture/schema-migrations.md) and the step-by-step
recipe is [changing the schema](../docs/guides/changing-the-schema.md); the pages under
[`docs/`](docs/) are the reference for this app's code.

## Main concepts

- **Guarded migration**: every migration is one `RunPython` operation that inspects the
  database first and does nothing when the change is already there. Fresh and test
  databases get their tables from the current models, so on them every migration is a
  no-op; on an older database it applies the change once.
- **Live lookups**: a migration never imports an app model. It asks
  [`schema.py`](schema.py) for the model or field as the code defines it when the
  migration runs (`live_model`, `live_field`), or uses raw SQL on named tables.
- **Skip what is gone**: when a later release renames or removes a model, field, table or
  column, the older migration finds nothing and returns. The later release's own
  migration owns that change. This keeps every old migration runnable forever.
- **Irreversible by design**: the reverse of every migration is
  `migrations.RunPython.noop`. Unapplying one leaves columns, indexes and fixed data in
  place.

## Key modules

| Path | Responsibility |
|------|----------------|
| [`schema.py`](schema.py) | `live_model`, `live_field`, `table_names`, `table_columns`, `add_missing_columns` |
| [`migrations/`](migrations/) | The chain `0001` to `0008`, one `RunPython` each |
| [`apps.py`](apps.py) | `TGSchemaConfig` (`name = "tg_schema"`) |
| [`tests/`](tests/) | Generic guards for every migration, plus one test module per migration |

### `schema.py` helpers

| Helper | Returns |
|--------|---------|
| `live_model(label)` | `apps.get_model(label)` (the current model class) or `None` if it does not exist |
| `live_field(model, name)` | `model._meta.get_field(name)` or `None` if the field does not exist or `model` is `None` |
| `table_names(connection)` | Set of table names in the database |
| `table_columns(connection, table)` | Set of column names of `table` |
| `add_missing_columns(schema_editor, label, names)` | Runs `schema_editor.add_field(model, field)` for each field in `names` whose column the model's table lacks. Returns the set of names it added; returns an empty set when the model or its table is missing, and skips names that are not fields |

A column added with `add_field` takes the field's default for existing rows, so give new
fields `null=True` or a default.

## How it connects to other apps

- It is in `INSTALLED_APPS` ([`tg/settings/base.py`](../tg/settings/base.py)), so
  `python manage.py migrate` runs its migrations.
- It changes tables of `game`, `characters` and `locations` (see
  [migrations](docs/migrations.md)). Models that rely on a migration say so in a comment:
  `game.models.UserSceneReadStatus` (0008) and
  `locations.models.mage.chantry.ChantryBackgroundRating` (0002).
- The test runner (`tg.test_runner.LocalMigrationTestRunner`, see
  [test runner](../tg/docs/test-runner.md)) builds test tables for the local apps from the
  models, then runs these migrations, which find nothing to do.
- `python manage.py reset_db` (and `setup_db.sh`, which calls it) deletes the generated
  migrations of the local apps but keeps the files in `tg_schema/migrations/`.

## Documentation

| Page | Covers |
|------|--------|
| [migrations.md](docs/migrations.md) | Each migration: what it changes, its guards, its effect on data, its tests |
| [writing-a-migration.md](docs/writing-a-migration.md) | Templates for a new column, a backfill and a raw-SQL constraint, and the checklist |

## See also

- [Schema migrations](../docs/architecture/schema-migrations.md)
- [Changing the schema](../docs/guides/changing-the-schema.md)
- [Data model](../docs/architecture/data-model.md)
- [tg package](../tg/README.md)
