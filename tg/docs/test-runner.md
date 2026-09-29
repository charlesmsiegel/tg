# Test runner

This page describes `tg.test_runner.LocalMigrationTestRunner`
([`tg/test_runner.py`](../test_runner.py)), the project's `TEST_RUNNER`: why it exists,
what it does to the test database and what that means when you run tests. It is for
anyone running or debugging the test suite. How to write and organise tests is in
[testing](../../docs/development/testing.md).

## Why a custom runner

The model-owning apps commit no migration files (only `migrations/__init__.py`; see
[schema migrations](../../docs/architecture/schema-migrations.md)). Django treats an app
that has a `migrations` package as migrated, so with the default runner the test
database would get no tables for them. The custom runner makes Django build those tables
directly from the current models.

## What it does

`LocalMigrationTestRunner` subclasses Django's `DiscoverRunner` and overrides only
`setup_databases()`. Before calling the parent method it:

1. copies `settings.MIGRATION_MODULES` (empty unless configured);
2. for each installed app whose path is inside `BASE_DIR` (so Django's and third-party
   apps are skipped), looks at its `migrations/` directory;
3. if that directory exists and holds no `.py` file other than `__init__.py`, sets
   `MIGRATION_MODULES[app.label] = None`, which tells Django the app has no migrations;
4. assigns the result back to `settings.MIGRATION_MODULES`.

Django then creates the tables of those apps from their models (with every
`Meta.constraints` and `Meta.indexes` entry) and runs the migrations of the apps that
have them, including `tg_schema`, whose guarded migrations find nothing to change.

```bash
python manage.py test                 # whole suite
python manage.py test core tg_schema  # selected apps
```

The test database is SQLite, named by `DATABASES["default"]["TEST"]["NAME"]`
(`db_test.sqlite3` under `BASE_DIR`).

## Things to know

- **Generated migration files change the behaviour.** If your working copy contains
  migration files for a local app (for example after `setup_db.sh` or `makemigrations`),
  the runner leaves that app alone and Django builds its test tables by running those
  files. Stale files can then make tests fail where a clean checkout passes. Delete them,
  or run tests from a clean checkout.
- **Only the test database is affected.** The runner changes `MIGRATION_MODULES` inside
  the test process; `migrate` on a real database is unaffected.
- **Apps without a `migrations/` directory** (such as `widgets`) are not touched; Django
  already treats them as unmigrated.

## See also

- [Testing](../../docs/development/testing.md)
- [Schema migrations](../../docs/architecture/schema-migrations.md)
- [tg_schema app](../../tg_schema/README.md)
- [Core tests](../../core/docs/testing.md)
- [`tg/test_runner.py`](../test_runner.py)
