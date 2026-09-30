# Management commands

Rules for writing or changing a management command. The existing commands are listed with
their options in [docs/reference/management-commands.md](../../../../docs/reference/management-commands.md).

## Where they live

- `<app>/management/commands/<command_name>.py`, one `Command(BaseCommand)` per file,
  with `__init__.py` in `management/` and `commands/`. Project-wide maintenance commands
  live in `core/management/commands/` (for example `populate_gamedata`,
  `validate_data_integrity`, `cleanup_orphaned_data`, `export_chronicle`,
  `reset_db`); an app-specific command goes in that app's `management/commands/`.
- Name it `verb_object` in snake_case (`cleanup_old_weeks`, `audit_xp_spending`).

## Shape

```python
"""Delete Week objects older than a threshold."""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from game.models import Week


class Command(BaseCommand):
    help = "Clean up old Week objects to prevent unbounded growth"

    def add_arguments(self, parser):
        parser.add_argument("--months", type=int, default=6, help="Age threshold in months")
        parser.add_argument("--dry-run", action="store_true", help="Report without writing")

    def handle(self, *args, **options):
        if options["months"] < 1:
            raise CommandError("--months must be at least 1")
        weeks = Week.objects.filter(...)
        self.stdout.write(f"Found {weeks.count()} week(s)")
        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("[DRY RUN] Nothing deleted"))
            return
        with transaction.atomic():
            weeks.delete()
        self.stdout.write(self.style.SUCCESS("Done"))
```

## Rules

- **`help` and a module docstring** that say what the command changes.
- **Every command that writes has `--dry-run`** (`store_true`, dest `dry_run`) that
  reports what it would do and writes nothing.
- **Wrap writes in `transaction.atomic()`.** Commands are not requests, so
  `ATOMIC_REQUESTS` does not apply. Lock rows with `select_for_update()` when the command
  changes points (XP, freebies).
- **Go through services and model methods** (`ApprovalService`,
  `Character.add_xp`, `change_character_status`) rather than setting `status`, `xp` or
  approval fields directly. Save with validation; use `skip_validation=True` or
  `update()` only for documented bulk repairs.
- **Report with `self.stdout.write` and `self.style.SUCCESS` / `WARNING` / `ERROR`**,
  never `print()`. Fail with `CommandError` (non-zero exit), not `sys.exit` or a bare
  exception.
- **Bound the work**: iterate large querysets with `.iterator()` or in batches, and join
  what the loop reads (`select_related`, `prefetch_related`).
- **Destructive commands** refuse in production: `reset_db` and `reset_demo_data` raise
  `CommandError` unless `settings.DEBUG` (`reset_demo_data --force` overrides), and they
  ask for confirmation (`--yes`, `--confirm`). Bulk writes that bypass a storyteller
  (`approve_pending_items`) need an explicit scope and confirmation (`--noinput`).
- **Never change the schema in a command.** Columns, tables, constraints and backfills that
  existing databases need are `tg_schema` migrations ([schema-changes.md](schema-changes.md)).
- **Game data** loads through `populate_gamedata`, which runs every script under
  `populate_db/` (recursively, top-level files first, `chronicles/` last). Add data as a
  `populate_db` script that uses `get_or_create` so a rerun changes nothing; see
  [docs/guides/adding-reference-data.md](../../../../docs/guides/adding-reference-data.md).

## Tests

Put them in `<app>/tests/` (the core commands are tested in
`core/tests/test_management_commands.py`):

```python
out = StringIO()
call_command("cleanup_old_weeks", "--dry-run", stdout=out)
self.assertIn("[DRY RUN]", out.getvalue())
self.assertTrue(Week.objects.filter(pk=old.pk).exists())
```

Cover: the normal run changes what it should, `--dry-run` changes nothing, bad input
raises `CommandError`, and output names what was changed.

## Checklist

- [ ] Correct location and name; `help` and docstring.
- [ ] `--dry-run` for any write; writes in `transaction.atomic()`.
- [ ] Uses services for status, XP and approvals; no schema changes.
- [ ] Output through `self.stdout` and `self.style`; errors as `CommandError`.
- [ ] Tests for run, dry run and errors.

## See also

- [docs/reference/management-commands.md](../../../../docs/reference/management-commands.md)
- [docs/getting-started/seed-data.md](../../../../docs/getting-started/seed-data.md)
- [`core/management/commands/`](../../../../core/management/commands/)
- [validation.md](validation.md), [schema-changes.md](schema-changes.md)
