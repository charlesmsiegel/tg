# Loading game data

This page explains how the game-data scripts are run: the `populate_gamedata`
management command and its options, how it discovers and orders files, how
transactions and failures behave, what `setup_db.sh` does, and how to debug one
script. It is for developers seeding a database and for agents that run or change the
loader.

## `populate_gamedata`

Source: [`core/management/commands/populate_gamedata.py`](../../core/management/commands/populate_gamedata.py).

```bash
python manage.py populate_gamedata [--gameline TEXT] [--only TEXT] [--skip TEXT] [--dry-run] [--verbose]
```

Run it from the repository root. The command looks for the directory
`Path("populate_db")` relative to the current working directory and raises
`CommandError` ("Directory populate_db not found") when it is missing.

| Option | Effect |
|--------|--------|
| `--gameline TEXT` | Keep files whose name (without `.py`) contains `TEXT`, plus every file whose name contains no gameline word. See [filtering](#filtering). |
| `--only TEXT` | Keep files whose name contains `TEXT` (case-insensitive substring) |
| `--skip TEXT` | Drop files whose name contains `TEXT` (case-insensitive substring) |
| `--dry-run` | Print the files that would load, in order, and stop without touching the database |
| `--verbose` | Print "Loading <file>... ✓" per file and a traceback for each failure |

The options combine: `--gameline` is applied first, then `--only`, then `--skip`.
Django's own `-v/--verbosity` is separate and does not change this command's output.

### Filtering

All three filters compare against the file's stem (its name without directory or
`.py`), lower-cased. They never look at the folder a file is in.

`--gameline` treats a file as gameline-specific when its stem contains any of
`vampire`, `werewolf`, `mage`, `wraith`, `changeling`, `demon`, `vtm`, `wta`, `mta`,
`wto`, `ctd` or `dtf`. It keeps gameline-specific files whose stem contains the value
you pass, and every file that is not gameline-specific. In practice:

- `--gameline mage` keeps `mage/mage_example_rotes.py` and
  `character_templates/mage_templates.py`, drops `vampire/vampire_clans.py` and
  `demon/demon_lores.py`, and still keeps `mage/spheres.py`, `werewolf/tribes.py` and
  every top-level file, because their stems name no gameline.
- The gameline codes in the option's help text (`vtm`, `mta`, ...) appear in no file
  name, so `--gameline mta` drops every file with a gameline word in its stem.

`--only` and `--skip` match substrings too: `--only rotes` selects `mage/rotes.py` and
`mage/mage_example_rotes.py`; `--only practices` selects `practices_INC.py`,
`corruptedpractices.py` and `specializedpractices.py`.

Filters do not follow imports. A selected script that imports another script still
runs that script (see [conventions](conventions.md#imports-are-load-order)).

## Discovery and order

The command collects `populate_db/**/*.py` recursively (so `__init__.py` files and the
`character_templates/` package are included; this `docs/` folder holds no `.py` files)
and sorts them with `get_sort_key()`:

1. Files directly in `populate_db/`, by file name.
2. Files in a subfolder named `core` (priority 1).
3. Files in any other subfolder (priority 500), by folder name and then path.
4. Files in a subfolder named `chronicles` (priority 999).

The repository has no `core` or `chronicles` subfolder, so the order is: the
top-level files, then `changeling/`, `character_templates/`, `demon/`, `mage/`,
`mummy/`, `vampire/`, `werewolf/`, `wraith/`. Names sort as Python strings, so digits
come before letters and `aa_` before `ab...`:

```text
00_books.py
01_resonance.py
aa_gamelines.py
abilities.py
advantages.py
...
weapons.py
changeling/cantrips.py
...
wraith/wraith_thorns.py
```

Run `python manage.py populate_gamedata --dry-run` to see the exact list. The file
sort is only half of the order: a script that imports another script runs it at that
point (see [conventions](conventions.md#imports-are-load-order)).

## Execution, transactions and failures

For each file the command reads the source and runs:

```python
with transaction.atomic():
    exec(code, {"__name__": "__main__"})
```

- Each file runs with a fresh global namespace. Names defined in one file are not
  visible in the next unless the next one imports them.
- Each file runs in its own transaction. If it raises, everything it wrote is rolled
  back, including rows written by other scripts it imported during that run.
- A failure is printed ("✗ <file>: <error>"), logged with its traceback, and counted;
  the command continues with the next file.
- At the end it prints how many files loaded and how many failed. The command exits
  normally even when files failed, so check the summary rather than the exit status.

Imported scripts are cached in `sys.modules` for the rest of the process. If a script
fails after importing another one, that import's rows are rolled back but the module
stays cached, so later imports in the same run do not recreate them. The imported
file's own turn in the sort order runs it again with `exec`, which restores its rows
only if that turn comes later. After fixing a failure, run the command again: every
script is written to be safe to rerun.

## `setup_db.sh`

[`setup_db.sh`](../../setup_db.sh) rebuilds a local development database from
scratch. It runs, in order:

1. `python manage.py reset_db --yes`
   ([`core/management/commands/reset_db.py`](../../core/management/commands/reset_db.py)),
   which refuses to run unless `DEBUG` is true, deletes `db.sqlite3` in the current
   directory, and deletes every `*.py` file except `__init__.py` in each top-level
   `<dir>/migrations/` folder except `tg_schema/migrations/`;
2. `python manage.py makemigrations` and `python manage.py migrate`;
3. `rm -rf collected_static/` and `collectstatic` (answering yes);
4. `python manage.py populate_gamedata`.

Step 1 deletes only the local apps' generated, git-ignored migrations; it keeps
`tg_schema`'s committed numbered migrations. Schema history and why local apps have no
committed migrations are covered in
[schema migrations](../../docs/architecture/schema-migrations.md).

## Debugging one script

- Run only that file (and whatever it imports) with its traceback:

  ```bash
  python manage.py populate_gamedata --only vampire_clans --verbose
  ```

- [`scripts/debug/debug_populate.py`](../../scripts/debug/debug_populate.py) runs one
  file outside a transaction and prints the failing line. It imports `tg.settings`, so
  run it with the repository root on the path:

  ```bash
  PYTHONPATH=. python scripts/debug/debug_populate.py populate_db/vampire/vampire_clans.py
  ```

- To inspect what a script created, open `python manage.py shell` and query the model.

## See also

- [populate_db overview](../README.md)
- [Conventions](conventions.md)
- [Adding data](adding-data.md)
- [Seed data](../../docs/getting-started/seed-data.md)
- [Management commands](../../docs/reference/management-commands.md)
