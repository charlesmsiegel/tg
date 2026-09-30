# Core management commands

This page describes every command in
[`core/management/commands/`](../management/commands/): what it reads, what it changes
and which options it takes. It is for operators and developers maintaining data. For the
project-wide command list see
[management commands](../../docs/reference/management-commands.md); for routine
operations see [maintenance](../../docs/operations/maintenance.md).

Run any command with `python manage.py <command> --help` for its full option list.
Commands that change data say so below; most offer `--dry-run` or a list-only mode, and
you should run that first. None of them go through the permission system: they act as
the database owner.

## Summary

| Command | Changes data | Purpose |
|---------|--------------|---------|
| [`populate_gamedata`](#populate_gamedata) | Yes | Load reference data from `populate_db/` |
| [`populate_test_chronicle`](#populate_test_chronicle) | Yes | Fill a chronicle with random test characters and scenes |
| [`reset_demo_data`](#reset_demo_data) | Yes, destructive | Delete game data and load a demo chronicle |
| [`reset_db`](#reset_db) | Yes, destructive | Delete `db.sqlite3` and generated migration files (development only) |
| [`approve_pending_items`](#approve_pending_items) | Yes | Bulk approve submitted characters, images, freebies and XP requests |
| [`process_weekly_xp`](#process_weekly_xp) | Yes | Create a `Week` and weekly XP requests |
| [`sync_character_status`](#sync_character_status) | Yes | Remove retired and deceased characters from groups, chantries and scenes |
| [`cleanup_old_weeks`](#cleanup_old_weeks) | Yes | Delete old `Week` rows |
| [`cleanup_orphaned_data`](#cleanup_orphaned_data) | Yes | Delete unowned drafts, empty scenes, unused setting elements |
| [`find_duplicate_objects`](#find_duplicate_objects) | Optional | Report (and optionally delete) duplicate objects |
| [`archive_inactive_chronicles`](#archive_inactive_chronicles) | Optional | Report, export and rename inactive chronicles |
| [`export_chronicle`](#export_chronicle) | No (writes a file) | Export a chronicle to JSON |
| [`import_chronicle`](#import_chronicle) | Yes | Import the chronicle record from an export |
| [`validate_character_data`](#validate_character_data) | Optional | Check character values |
| [`validate_data_integrity`](#validate_data_integrity) | Optional | Check and fix values that break model constraints |
| [`audit_xp_spending`](#audit_xp_spending) | No | Report XP discrepancies |
| [`audit_user_permissions`](#audit_user_permissions) | No | Report storyteller relationships and profile completeness |
| [`generate_chronicle_summary`](#generate_chronicle_summary) | No | Chronicle statistics as text, Markdown or HTML |
| [`generate_st_report`](#generate_st_report) | No | Storyteller dashboard report |
| [`monitor_validation`](#monitor_validation) | No | Health score for data integrity and XP activity |

## Data loading and resets

### `populate_gamedata`

Runs the Python scripts under `populate_db/` (recursively) with `exec`, each in its own
transaction. Order: files directly in `populate_db/`, then `core/`, then other folders
alphabetically, then `chronicles/` last. A failing file is reported and the rest still
run.

| Option | Effect |
|--------|--------|
| `--gameline CODE` | Keep files whose name contains `CODE`, plus files whose name contains no gameline word (`vampire`, `vtm`, `mage`, `mta`...) |
| `--only TEXT` / `--skip TEXT` | Keep / drop files whose name contains `TEXT` |
| `--dry-run` | List the files and stop |
| `--verbose` | Print each file and tracebacks |

Filtering is by file-name substring, so `--gameline vtm` does not select a file named
`vampire_*.py`. See [seed data](../../docs/getting-started/seed-data.md) and the
[populate_db app](../../populate_db/README.md).

### `populate_test_chronicle`

`--chronicle ID` (required), `--characters N` (default 10), `--scenes N` (default 15).
Creates or reuses a `test_player` user (password `test123` when created), `N` core
`Human` characters with random names, concepts, statuses and XP, and `N` scenes. The
`--gameline` option is accepted but not used: every character is a core `Human`.

### `reset_demo_data`

Refuses to run unless `DEBUG` is true or `--force` is given. Without `--confirm` it only
prints a warning. With it, in one transaction: deletes all weekly and story XP requests,
weeks, scenes, characters, items, locations and chronicles; deletes every non-superuser
account unless `--preserve-users`; then creates `demo_st` and `demo_player` if missing
(with the `--password` value, or a random password it prints once) and a demo chronicle
with `demo_st` as a storyteller. Never run it against a database you want to keep.

### `reset_db`

Refuses to run unless `DEBUG` is true. After a prompt (skip with `--yes`) it deletes
`db.sqlite3` in the working directory and every `*.py` file except `__init__.py` in
every top-level `*/migrations/` folder except `tg_schema/migrations/`, the project's
committed schema migrations (see [tg_schema](../../tg_schema/README.md)), which it
keeps. It then suggests `makemigrations`, `migrate` and `populate_gamedata`.

## Approvals and XP

### `approve_pending_items`

Bulk approval outside the web workflow, with no permission checks and no
`ApprovalService` hooks.

| `--type` | Effect |
|----------|--------|
| `characters` | `status` `Sub` to `App` for submitted characters (queryset `update`, so no model `save()`) |
| `images` | `image_status` `sub` to `app` for characters, locations and items with an image |
| `freebies` | `freebies_approved=True` for submitted characters |
| `xp-spends` | Looks for a `spent_xp` attribute on characters; characters no longer have it (XP spends are `game.XPSpendingRequest` rows), so this finds nothing |
| `xp-requests` | Marks unapproved `WeeklyXPRequest`s approved and adds their XP to the character |
| `all` (default) | All of the above |

Filters: `--chronicle ID`, `--owner USERNAME`. `--list-only` and `--dry-run` change
nothing. `--auto-approve-images` adds the image step whatever `--type` is.

### `process_weekly_xp`

`--week-ending YYYY-MM-DD` (default: the most recent Sunday). Creates the `Week` if it
does not exist, finds non-NPC `Human` characters in scenes finished during the seven
days before (by latest post date), and creates a `WeeklyXPRequest` with `finishing=True`
for each character that has none for the week. `--auto-approve` approves each request
and adds its XP. `--dry-run` creates nothing. `--notify` only prints a message that
notifications are not implemented; nothing is sent.

### `sync_character_status`

For retired (`Ret`) and deceased (`Dec`) characters: removes them from group
memberships, clears group leadership, removes them from chantry memberships, leadership
and positions, and with `--remove-from-scenes` from unfinished scenes. Each character is
processed in its own transaction. `--chronicle ID` narrows the set; `--fix-all` iterates
every character but still changes only retired and deceased ones. `--dry-run` reports
only. The same cleanup runs automatically when a character's status changes to `Ret` or
`Dec` through `Character.save()` (see
[utilities](utilities.md#helpers-in-coreutilspy)); this command repairs older data.

## Cleanup

### `cleanup_old_weeks`

Deletes `Week` rows whose `end_date` is more than `--months` (default 6, counted as
30-day months) ago. `--keep-with-pending` keeps weeks that still have unapproved weekly
XP requests. `--dry-run` reports only.

### `cleanup_orphaned_data`

Deletes characters, items and locations with no owner and status `Un`, and weekly and
story XP requests with no character. `--include-scenes` also deletes unfinished scenes
with no posts and no characters; `--include-setting-elements` also deletes setting
elements used by no chronicle. `--dry-run` reports only.

`--days` (default 30) is parsed but not applied: unowned drafts are deleted whatever
their age. Objects created as shared (owner `None`, see
[mixins](mixins.md#messagemixin-successmessagemixin-errormessagemixin)) that are still
drafts match too. Always run `--dry-run` first.

### `find_duplicate_objects`

Groups objects by lower-cased name, owner and chronicle and reports groups with more
than one member. `--type character|item|location|effect|all`, `--chronicle ID`,
`--owner USERNAME`, `--export FILE.csv`.

- `--auto-merge` deletes all but one object of a group when every member has the same
  status and description. It keeps the one with the highest status priority, then the
  highest id. Related rows are not merged; they go with the deleted objects.
- `--delete-empty` (when `--auto-merge` is not set) deletes every member of a group that
  is `Un` with an empty description, including the last one.

### `archive_inactive_chronicles`

Reports chronicles whose latest scene date is older than `--days` (default 90) and that
have no unfinished scenes or no submitted or approved characters. `--list-only` stops
there. `--export-before-archive` runs `export_chronicle --pretty` for each into
`chronicle_archives/`. `--mark-inactive` prefixes each chronicle's name with
`[ARCHIVED] `. Without those flags it only reports.

## Export and import

### `export_chronicle`

`export_chronicle CHRONICLE_ID [--output FILE] [--pretty] [--exclude-scenes]
[--include-users]`. Writes JSON with the chronicle (Django serializer format, plus the
usernames of its `storytellers`), its characters, items, locations, setting elements,
scenes and journals (unless `--exclude-scenes`) and weekly and story XP requests.
`--include-users` adds the storytellers' and character owners' username, e-mail and
name; password hashes, flags and permissions are never exported. The default file name is
`chronicle_<id>_<name>_<date>.json` in the working directory.

### `import_chronicle`

`import_chronicle FILE [--dry-run] [--skip-users] [--remap-users MAP.json]`. In one
transaction it creates users from the file (with unusable passwords; existing usernames are
skipped; `--remap-users` renames them), creates a new chronicle from the exported name,
theme, mood, year and headings, adds the storytellers, and attaches setting elements
(matched or created by name). Characters, items, locations, scenes, journals and XP
requests are only counted: the command prints that they need manual review and does not
create them.

## Validation and reports

### `validate_character_data`

Checks each character (filter with `--status` and `--chronicle`) for attributes
outside 0-15, XP consistency, required fields for its status and status consistency, and
prints the issues (`--verbose` for detail). `--fix` sets negative attributes to 1 and
saves. Its XP and orphaned-spend checks read a `spent_xp` attribute that characters no
longer have, so they report nothing.

### `validate_data_integrity`

Checks, and with `--fix` repairs with queryset updates: negative XP (set to 0), invalid
status (set to `Un`), attributes outside 1-10 and abilities outside 0-10 (clamped),
Willpower outside 1-10 and temporary Willpower outside 0-10 or above permanent,
negative or excessive ages, and duplicate `STRelationship` rows (keeps the first). It
also prints how many scenes have XP awarded and how many finished scenes await XP, for
information only. `--verbose` lists the affected rows.

### `audit_xp_spending`

For submitted and approved characters (`--chronicle ID` to narrow), compares earned XP
with approved and pending `xp_spendings`, flags pending spends older than
`--pending-days` (default 30) and negative XP, then lists unapproved weekly XP requests
(oldest first) and weekly and story requests with no character.
`--show-all` lists characters without issues; `--export FILE.csv` writes the results.

### `audit_user_permissions`

Prints user, chronicle and storyteller counts, the storyteller relationships of each
chronicle, relationships without a chronicle and, with `--check-profiles`, how many profiles fill in lines, veils and Discord. `--export
FILE.csv` writes one row per user.

### `generate_chronicle_summary`

`generate_chronicle_summary CHRONICLE_ID [--format text|html|markdown] [--output FILE]`.
Scene, character, XP and participation statistics for one chronicle, printed or written
to a file.

### `generate_st_report`

A text report per chronicle (pending approvals, active scenes, XP requests, character
status counts). `--st-username NAME` limits it to chronicles where that user is a
storyteller, `--chronicle ID` to one chronicle; `--output FILE` writes it to a file.

### `monitor_validation`

Computes a health score from data-integrity counts, XP activity and scene XP awards in
the last `--period` hours (default 24) and character statistics; the status is
`healthy` at 90 or more, else `degraded`. `--json` prints the metrics as JSON. `--alert`
prints an alert block when degraded; it does not send e-mail or call any external
service.

## See also

- [Management command reference](../../docs/reference/management-commands.md)
- [Maintenance](../../docs/operations/maintenance.md)
- [Seed data](../../docs/getting-started/seed-data.md)
- [Services](services.md)
- [`core/management/commands/`](../management/commands/)
