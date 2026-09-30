# Maintenance

This page covers routine care of a running installation: what to back up and how to restore
it, clearing caches, log rotation, the data-maintenance management commands and how safe each
one is, reloading reference data, upgrading dependencies, and the order of operations for a
release that changes the schema. It is for operators. Install and update steps are in
[Deployment](deployment.md).

## Backups

### What to back up

| Path | Why | Notes |
|------|-----|-------|
| `db.sqlite3` | All application data | Use SQLite's online backup, not `cp`, while the server runs (below). |
| `media/` | Uploaded images | Plain files; copy with `tar` or `rsync`. |
| `<app>/migrations/*.py` for `accounts`, `characters`, `core`, `game`, `items`, `locations` | Generated on this host by `makemigrations`; gitignored; they record which schema the database has | Back up with the database and restore them together. Without them, the next `makemigrations` generates fresh initial migrations that do not match the existing tables. See [Deployment](deployment.md#schema-generated-migrations-and-tg_schema). |
| `.env` | Secrets and configuration | Store the copy as securely as the original. |

Not needed: `collected_static/` (rebuilt by `collectstatic`), `db_test*.sqlite3` (test
databases), and Redis. Redis holds the cache, sessions and the channel layer; losing it logs
everyone out and nothing else. `logs/` is optional.

### SQLite

Take a consistent copy while the application is running with the `sqlite3` command-line tool:

```bash
mkdir -p backups
sqlite3 db.sqlite3 ".backup 'backups/db-$(date +%F-%H%M).sqlite3'"
tar czf "backups/migrations-$(date +%F-%H%M).tgz" \
    accounts/migrations characters/migrations core/migrations \
    game/migrations items/migrations locations/migrations
tar czf "backups/media-$(date +%F-%H%M).tgz" media
```

If the `sqlite3` tool is not installed, Python's `sqlite3` module does the same with
`Connection.backup()`. Keep backups off the host.

If you have enabled one of the commented PostgreSQL or MySQL blocks in `production.py`, use that
database's own dump tool instead; the migration files and `media/` still need backing up.

### Restore

1. Stop every ASGI process.
2. Replace `db.sqlite3` with the backup copy, and delete any `db.sqlite3-journal` or
   `db.sqlite3-wal` file left beside it.
3. Restore the generated migration files from the **same** backup set.
4. Restore `media/`.
5. Check out the code revision the backup was taken with, or a later one, then run
   `python manage.py migrate` to bring the database forward.
6. Start the server. Users must log in again if Redis was also reset.

### Chronicle exports are not backups

`export_chronicle <chronicle_id>` writes one chronicle's chronicle row, characters, items,
locations, setting elements, scenes, journals and XP requests (and, with `--include-users`,
the related users' usernames, e-mail addresses and names, never password hashes) to a JSON file. `import_chronicle <file>` recreates only the chronicle
(name, theme, mood, year, headings), its storytellers, its setting elements and, unless
`--skip-users`, missing users (created with unusable passwords). Characters, items, locations,
scenes, journals and XP requests in the file are counted and reported, not imported. The
import runs in one transaction and has `--dry-run` and `--remap-users FILE`. Use the pair for
inspection or partial migration, never as a substitute for database backups.

## Clearing caches

Cached data expires on its own; nothing invalidates it when the database changes.
`core.cache.CacheInvalidator` exists but is not called anywhere.

| Cache entry | Key | Lifetime |
|-------------|-----|----------|
| Cached reference pages (`cache_page_per_visitor`) | `tg:anonymous_page:*` and `views.decorators.cache.*` | 15 minutes |
| Reference lists (`get_cached_reference_list`) | `tg:reference_list:*` | 15 minutes by default |
| `cache_function` results | `tg:function:*` | As declared |
| Nav notification counts | `notification_count_<user id>` | 60 seconds |
| Sessions (production only) | `django.contrib.sessions.cache*` | Session age |

The keys above are before `django_redis` adds `KEY_PREFIX` and version (`tg:1:`);
`delete_pattern` adds them for you.

Clear everything except sessions after reloading reference data or when a stale page must
disappear at once:

```bash
python manage.py shell -c "from django.core.cache import cache; [cache.delete_pattern(p) for p in ('tg:*', 'views.decorators.cache.*', 'notification_count_*')]"
```

`cache.clear()` also works but, on `django_redis`, runs `FLUSHDB` on the Redis database in
`REDIS_URL`. That deletes every session (everyone is logged out) and, because the channel layer
uses the same Redis database, the group memberships of open scene sockets, which then stop
receiving live posts until the page reconnects.

In development the cache is `LocMemCache`, which lives inside each process: a
`manage.py shell` has its own empty cache and cannot clear the development server's. Restart
the server instead. `delete_pattern` does not exist on `LocMemCache`.

## Log rotation

In production, `RotatingFileHandler` rotates `logs/app.log` and `logs/error.log` at 10 MB
(10 backups) and `logs/warning.log` at 5 MB (5 backups); nothing else is needed. In
development `logs/debug.log`, `logs/error.log` and `logs/warning.log` are plain `FileHandler`
files that grow without limit; truncate them while the server is stopped (`: > logs/debug.log`).
If you use an external rotator such as `logrotate` on the development files or on Daphne's
access log, use copy-and-truncate: the handlers keep their files open. Details are in
[Logging and monitoring](logging-and-monitoring.md).

Development uses database sessions, so `python manage.py clearsessions` removes expired ones
there. Production sessions are cache entries that expire by themselves.

## Data-maintenance commands

All live in [`core/management/commands/`](../../core/management/commands/).
Take a backup before running any command marked as writing. Full options are in the
[management commands reference](../reference/management-commands.md); read-only reports are
listed in [Logging and monitoring](logging-and-monitoring.md#health-and-audit-commands).

| Command | What it changes | Safety |
|---------|-----------------|--------|
| `approve_pending_items` | Approves submitted characters, submitted images, freebies of submitted characters (with no backstory award), and weekly XP requests (adding their XP), through `ApprovalService` and the model methods the storyteller pages use. `--type`, `--chronicle`, `--owner` narrow it. | Approving needs `--chronicle`, `--owner` or `--all`, plus `--approver USERNAME` whose `APPROVE` permission is checked per object, and asks for confirmation unless `--noinput`. Run with `--list-only` or `--dry-run` first. |
| `process_weekly_xp` | Creates the `Week` ending `--week-ending` (default: the last Sunday) and a `WeeklyXPRequest` (finishing XP only) for each non-NPC `Human` in scenes finished that week; `--auto-approve` also awards the XP. | Skips requests that already exist. `--dry-run` available. `--notify` only prints a message. |
| `cleanup_old_weeks` | Deletes `Week` rows older than `--months` (default 6; a month is 30 days). Weekly XP requests keep their row with `week` set to null. | `--dry-run`; `--keep-with-pending` keeps weeks with unapproved requests. |
| `cleanup_orphaned_data` | Deletes weekly and story XP requests with no character; `--include-unowned-drafts` also deletes characters, items and locations in a chronicle with no owner and status `Un` (never reference data, but storytellers' shared drafts match); `--include-scenes` also deletes unfinished scenes with no posts and no characters; `--include-setting-elements` deletes setting elements in no chronicle. | **Deletes by default.** No age threshold (objects have no creation date). Run `--dry-run` first. |
| `find_duplicate_objects` | Reports objects with the same case-insensitive name, owner and chronicle. `--auto-merge` deletes all but one copy when status and description match (keeps the highest status, then highest ID); `--delete-empty` deletes unfinished copies with no description, keeping one per group. | Read-only without those two flags. "Merge" deletes; nothing is combined. |
| `sync_character_status` | For retired and deceased characters, removes them from groups, group leadership and chantry roles; `--remove-from-scenes` also from unfinished scenes. | `--dry-run`. |
| `archive_inactive_chronicles` | `--export-before-archive` runs `export_chronicle` for each inactive chronicle into `chronicle_archives/`; `--mark-inactive` prefixes the name with `[ARCHIVED]`. | Without those flags it only lists. Renaming is the only "archiving"; nothing is hidden or deleted. |
| `validate_data_integrity --fix`, `validate_character_data --fix` | Clamp out-of-range values; see [Logging and monitoring](logging-and-monitoring.md#health-and-audit-commands). | Run without `--fix` first. |
| `export_chronicle`, `import_chronicle` | See [Chronicle exports are not backups](#chronicle-exports-are-not-backups). | Export writes a file in the working directory; import creates rows. |
| `populate_gamedata` | Creates reference data; see [Reloading reference data](#reloading-reference-data). | Re-runnable. |
| `populate_test_chronicle --chronicle ID` | Creates fake characters and scenes in an existing chronicle, and a `test_player` user with password `test123`. | Development and test only. |
| `reset_demo_data --confirm` | In one transaction deletes all weekly and story XP requests, weeks, scenes, characters, items, locations and chronicles, and (unless `--preserve-users`) every non-superuser account; then creates `demo_st` and `demo_player` (with the `--password` value, or a random password it prints) and a demo chronicle. | **Never run on a real installation.** Refuses to run unless `DEBUG` is true or `--force` is given; without `--confirm` it only prints a warning. |
| `reset_db` | Deletes `db.sqlite3` in the working directory and every non-`__init__.py` file in every top-level `*/migrations/` directory except the committed `tg_schema/migrations/`. | Refuses to run unless `DEBUG` is true. Prompts unless `--yes`. |

## Reloading reference data

Reference data (books, abilities, clans, disciplines, spheres, gifts, character templates and
so on) comes from the scripts under [`populate_db/`](../../populate_db/), run by
`python manage.py populate_gamedata`. To reload after a change:

1. Back up the database.
2. Run `python manage.py populate_gamedata --dry-run` (optionally with `--gameline`, `--only` or
   `--skip`, which match substrings of script file names) to see which scripts will run.
3. Run it without `--dry-run`, and read the summary: a failing script is reported and the others
   continue, and the command exits successfully either way.
4. Clear the caches (above) so cached reference pages and lists show the new data.

The scripts use `get_or_create` with the identifying fields as lookup arguments. Re-running
unchanged scripts creates nothing. Values a script assigns after `get_or_create` and saves are
updated in place, but changing a value that is part of the lookup (a name, say) creates a second
row instead of renaming the first. Rename or remove such rows by hand, in the admin or a shell.

Scripts in `populate_db/chronicles/` (gitignored, host-local) run last, if present. See
[Seed data](../getting-started/seed-data.md) and [`populate_db/`](../../populate_db/README.md).

## Upgrading dependencies

Python dependencies are all in [`requirements.txt`](../../requirements.txt); the pinning policy
is in [Security](security.md#dependency-pinning).

1. Edit `requirements.txt`. For a security fix, add or raise the pin with a `# Security:` comment
   naming the advisory.
2. In a development checkout, `pip install -r requirements.txt` (add `--upgrade` to move packages
   pinned with `>=` to their newest releases).
3. Run `python manage.py check` and the test suite ([Testing](../development/testing.md)).
4. Run `python manage.py makemigrations --dry-run`. An upgrade of Django or
   `django-polymorphic` can change the migrations Django generates for the local apps; any
   output here is a schema change that every host will apply on its next update.
5. Deploy as a normal update ([Deployment](deployment.md#updating)), which includes the
   `pip install` step `update.sh` leaves out.

Browser libraries (htmx, its WebSocket extension, Alpine.js) are vendored under
`source_static/vendor/`. Upgrade them as described in
[`source_static/vendor/VENDOR.md`](../../source_static/vendor/VENDOR.md): add the new version
beside the old, update the SRI hash in the table and in
`core/templates/core/includes/interactive_scripts.html`, and delete the old directory.

## Releasing a schema change

A release changes the schema when it alters model fields, constraints or tables, or adds a
`tg_schema` migration. How such a change is written is covered in
[Changing the schema](../guides/changing-the-schema.md). On each production host:

1. **Back up** the database, the generated migration files and `media/`.
2. **Stop** every ASGI process. Old code must not write to tables that are about to change, and
   new code must not run against the old schema.
3. `git pull`, then `pip install -r requirements.txt` if it changed.
4. `python manage.py makemigrations`. Read the list of generated files; answer any rename or
   default-value questions it asks.
5. **If the release adds a constraint that existing rows may violate**, clean the data before
   migrating: the generated migration adds the constraint before `tg_schema` runs, and fails on
   violating rows. For `0008_unique_scene_read_status`, check for duplicate read-status rows
   and, if there are any, run the migration's function on its own; it merges duplicates, deletes
   orphans and adds the unique index, and later runs find nothing to do:

   ```bash
   python manage.py shell -c "
   from django.db.models import Count
   from game.models import UserSceneReadStatus as S
   print(S.objects.values('user', 'scene').annotate(n=Count('id')).filter(n__gt=1).count())"

   python manage.py shell -c "
   import importlib
   from types import SimpleNamespace
   from django.db import connection
   m = importlib.import_module('tg_schema.migrations.0008_unique_scene_read_status')
   m.make_scene_read_status_unique(None, SimpleNamespace(connection=connection))"
   ```

6. `python manage.py migrate --plan` to see what will run, then `python manage.py migrate`. The
   host's generated migrations apply first and `tg_schema` migrations after them, in migration
   graph order; a `tg_schema` migration finds its column already present and does nothing, or
   applies the data fix or constraint it carries.
7. `python manage.py collectstatic --noinput`.
8. `python manage.py populate_gamedata` if reference data changed, then clear the caches.
9. **Start** the ASGI processes and check a character page, a scene and the admin.

To roll back, stop the server, restore the database **and** the generated migration files from
step 1, check out the previous revision, and start again. `tg_schema` migrations reverse as
no-ops (`RunPython.noop`), so `migrate` backwards does not undo them.

## See also

- [Deployment](deployment.md)
- [Logging and monitoring](logging-and-monitoring.md)
- [Schema migrations](../architecture/schema-migrations.md)
- [Management commands reference](../reference/management-commands.md)
- [Caching](../architecture/caching.md)
- [`tg_schema/`](../../tg_schema/README.md)
