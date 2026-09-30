# Logging and monitoring

This page describes where the application writes logs in each environment, which loggers
the code uses, how error notification by email is (and is not) wired, what to watch on a
production host, and the management commands that produce health and audit reports. It is
for operators, and for developers adding log calls.

## Logging configuration

`LOGGING` is defined in [`tg/settings/base.py`](../../tg/settings/base.py) and modified by
[`tg/settings/development.py`](../../tg/settings/development.py) and
[`tg/settings/production.py`](../../tg/settings/production.py). All file handlers write under
`logs/` in the repository root. The directory is kept in git (it holds only a `.gitignore`
that ignores `*.log` and `*.log.*`); the handlers open their files when settings load, so the
process fails to start if `logs/` is missing or not writable.

### Formatters

| Name | Format |
|------|--------|
| `simple` | `[LEVEL] logger - message` |
| `verbose` | `[LEVEL] time logger module.function:line - message` |
| `detailed` | `[LEVEL] time [process:thread] logger path:line - message` |

### Handlers

| Handler | Development | Production |
|---------|-------------|------------|
| `console` | stderr, `INFO`, `simple` | same |
| `console_debug` | stderr, `INFO`, `verbose`, only when `DEBUG` is true | never emits (`require_debug_true`) |
| `file` | `logs/debug.log`, `FileHandler`, `DEBUG`, `verbose` | `logs/app.log`, `RotatingFileHandler`, `INFO`, 10 MB x 10 backups |
| `error_file` | `logs/error.log`, `FileHandler`, `ERROR`, `detailed` | `logs/error.log`, `RotatingFileHandler`, 10 MB x 10 backups |
| `warning_file` | `logs/warning.log`, `FileHandler`, `WARNING` (attached to no logger) | `logs/warning.log`, `RotatingFileHandler`, 5 MB x 5 backups |
| `null` | discards | discards |

In development `logs/warning.log` is created but stays empty, because no logger uses
`warning_file` there. Development log files are never rotated.

### Loggers

Every configured logger has `propagate: False`.

| Logger | Handlers | Level (dev) | Level (prod) |
|--------|----------|-------------|--------------|
| `django` | `console`, `file` | `INFO` | `WARNING` |
| `django.request` | `error_file`, `console` | `ERROR` | `ERROR` |
| `django.security` | `error_file`, `console` | `WARNING` | `WARNING` |
| `django.template` | `console` | `INFO` | `INFO` |
| `django.db.backends` | dev: `console_debug`; prod: `null` | `DEBUG` | `INFO` |
| `tg`, `accounts`, `characters`, `game`, `items`, `locations`, `core` | `console`, `file`, `error_file`; plus `console_debug` in dev, `warning_file` in prod | `DEBUG` | `INFO` |

Consequences worth knowing:

- Django logs suspicious requests (for example a disallowed `Host` header) on
  `django.security.<ExceptionName>` at `ERROR`, so they reach `logs/error.log`. `django.request`
  logs 4xx responses at `WARNING`, below its `ERROR` level, so 403s and 404s are not recorded;
  5xx responses are.
- In development the app loggers have both `console` and `console_debug`, so each `INFO` or
  higher message from them appears twice on the console.
- Development sets `django.db.backends` to `DEBUG` on `console_debug`, but that handler's level
  is `INFO`, so SQL statements (logged at `DEBUG`) are not printed.
- `django.db.backends` also carries errors from `transaction.on_commit(..., robust=True)`
  callbacks (Django logs them on `django.db.backends.base`). In production that logger goes to
  `null`, so a failed scene-chat broadcast after a post
  ([`game/scene_chat.py`](../../game/scene_chat.py)) leaves no log entry.
- Loggers that are not configured (`daphne`, `channels`, `django.server`, third-party
  libraries) propagate to the root logger, which has no handlers; Python then prints their
  `WARNING` and higher records to stderr. Daphne's access log is separate and controlled by its
  `--access-log` option.

### Loggers used in the code

Modules log with `logging.getLogger(__name__)`, so records are handled by the app logger
matching the first component of the module path (`game.consumers` by `game`, and so on).

| Module | Level | What is logged |
|--------|-------|----------------|
| [`game/consumers.py`](../../game/consumers.py) | `INFO` | A user connected to or disconnected from a scene socket |
| [`game/consumers.py`](../../game/consumers.py) | `ERROR` (`exception`) | An unexpected error while handling a scene socket message |
| [`accounts/context_processors.py`](../../accounts/context_processors.py) | `WARNING` | The notification count for the nav could not be computed (the page renders with 0) |
| [`core/views/character_template.py`](../../core/views/character_template.py) | `ERROR` | Character template import failed; creating an NPC from a template failed |
| [`core/utils.py`](../../core/utils.py) | `ERROR` | A registered cleanup handler failed while retiring a character |
| [`core/models.py`](../../core/models.py) | `DEBUG` | An `Observer`'s target object could not be validated |
| [`core/management/commands/populate_gamedata.py`](../../core/management/commands/populate_gamedata.py) | `ERROR` | A `populate_db/` script failed |
| [`core/management/commands/import_chronicle.py`](../../core/management/commands/import_chronicle.py) | `ERROR` | A chronicle import rolled back |
| [`core/management/commands/archive_inactive_chronicles.py`](../../core/management/commands/archive_inactive_chronicles.py) | `ERROR` | Exporting a chronicle before archiving failed |

`game/scene_chat.py` and `characters/views/mage/mage.py` create module loggers but do not log.
Unhandled exceptions in views are logged by Django on `django.request` at `ERROR`, which is what
fills `logs/error.log` in normal operation.

When you add logging, use `logging.getLogger(__name__)` in a module under one of the seven
configured app packages so that the record reaches the files; use `logger.exception(...)` or
`exc_info=True` for errors so the traceback is kept.

## Admins and error email

`production.py` builds `ADMINS` from `ADMIN_EMAILS` (comma-separated) and sets
`MANAGERS = ADMINS`. Each entry is a plain address, which becomes `("Admin", address)`, or
`Name <address>`, which becomes `("Name", address)`.

The project's `LOGGING` replaces Django's default `django` and `django.request` handlers, so
`production.py` adds Django's `mail_admins` handler (`django.utils.log.AdminEmailHandler`,
level `ERROR`, only when `DEBUG` is off) back to both loggers. Every unhandled request error
(a 500) is then emailed to `ADMINS` with its traceback, as well as written to
`logs/error.log` and the console. The mail is sent from `SERVER_EMAIL` through
`EMAIL_BACKEND`, so both must be set for it to arrive; with `ADMIN_EMAILS` empty nothing is
sent.

## What to monitor

The repository has no health-check URL, metrics endpoint or monitoring integration. Watch
these from outside:

| What | Why | How to notice a problem |
|------|-----|-------------------------|
| The ASGI process | Serves all HTTP and WebSocket traffic | HTTP probe of `/` (the public home page, `core:home`) |
| Redis | Cache, sessions and channel layer ([Deployment](deployment.md#redis)) | `redis-cli ping`; users suddenly logged out; scene chat stops updating live. Cache errors are suppressed (`IGNORE_EXCEPTIONS`), so the application logs do not show a Redis outage. |
| WebSockets through the proxy | Live scene chat | Open a scene page: the connection state shows in the page (`data-ws-state`). Handshake failures appear in the proxy and Daphne logs, not in `logs/`. |
| Disk: `db.sqlite3` and its directory | SQLite needs space for the database and its journal | Free space on the volume; write errors in `logs/error.log` |
| Disk: `logs/` | Production rotation bounds `app.log` and `error.log` at about 110 MB each and `warning.log` at about 30 MB; development files grow without limit | Directory size |
| Disk: `media/` | Uploaded images accumulate | Directory size |
| `logs/error.log` | Unhandled exceptions from views (`django.request`) and app errors | New entries |

`RotatingFileHandler` is not safe for several processes writing the same file. If you run
more than one ASGI process, expect occasional lost or misplaced records around a rotation, or
send logs to the console and let your process manager collect them.

## Health and audit commands

These management commands are read-only unless a flag says otherwise. They print to stdout
and can run from cron. The complete option lists are in the
[management commands reference](../reference/management-commands.md).

| Command | Reports | Writes |
|---------|---------|--------|
| `monitor_validation` | Counts of characters with negative XP, invalid status, attributes outside 1–10, abilities outside 0–10, temporary Willpower above permanent; XP spending request totals and approval rate; finished scenes awaiting XP in the last `--period` hours (default 24); character status breakdown. Computes a 0–100 health score (`degraded` below 90). `--json` gives machine-readable output. | Nothing. `--alert` only prints an extra alert block when degraded; it sends nothing. The exit status is 0 either way. |
| `validate_data_integrity` | Negative XP, invalid status, attribute and ability ranges, Willpower constraints, age and apparent age ranges, duplicate `STRelationship` rows; counts of scenes with and awaiting XP | Only with `--fix`, which clamps or nulls out-of-range values (mostly bulk `update()`, bypassing model validation), resets invalid status to `Un`, and deletes duplicate `STRelationship` rows keeping the first |
| `validate_character_data` | Attribute bounds, required fields for the character's status, status consistency; `--status`, `--chronicle` | Only with `--fix`, which sets negative attributes to 1 |
| `audit_user_permissions` | Chronicles and their storytellers, `STRelationship` rows without a chronicle; with `--check-profiles`, how many profiles set lines, veils and Discord ID | A CSV file only with `--export FILE` |
| `audit_xp_spending` | For submitted and approved characters: `xp` compared with the cost of their approved and pending `XPSpendingRequest` rows (negative balance, pending over balance, unusually many spends); unapproved and orphaned weekly and story XP requests. `--pending-days` is accepted but not used. | A CSV file only with `--export FILE` |
| `generate_st_report` | Per chronicle: storytellers, submitted characters, pending images, pending freebies, pending weekly XP requests, open scenes, character status counts. `--st-username` or `--chronicle` narrows it. | A file only with `--output FILE` |
| `generate_chronicle_summary <chronicle_id>` | A summary and statistics for one chronicle, as `text`, `html` or `markdown` | A file only with `--output FILE` |
| `find_duplicate_objects` | Characters, items, locations or effects sharing a name; `--export FILE` writes CSV | **Deletes** with `--auto-merge` or `--delete-empty`; see [Maintenance](maintenance.md#data-maintenance-commands) |
| `archive_inactive_chronicles --list-only` | Chronicles whose newest scene date is older than `--days` (default 90), or that have no dated scene, and that also have no open scene or no submitted or approved character | Nothing with `--list-only`; see [Maintenance](maintenance.md#data-maintenance-commands) for the other flags |

Some of these commands still contain checks written for the per-character `spent_xp` JSON field,
which no longer exists on `Character` (XP spends are `game.models.XPSpendingRequest` rows).
Those checks are skipped because the attribute is absent: `validate_character_data` reports
no XP-consistency or orphaned-spend issues. `monitor_validation` reads `XPSpendingRequest`
directly and is not affected.

## See also

- [Deployment](deployment.md)
- [Maintenance](maintenance.md)
- [Security](security.md)
- [Management commands reference](../reference/management-commands.md)
- [Settings reference](../reference/settings.md)
