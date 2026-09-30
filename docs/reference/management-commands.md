# Management commands

This page lists every management command the project defines: what it does, its
options, what it changes in the database or on disk, and when to use it. It is for
developers and operators running maintenance by hand or from a scheduler. Options were
checked against `python manage.py help <command>`; the standard Django options
(`--settings`, `--verbosity`, `--traceback`, `--no-color` and so on) are omitted.

All twenty-one live in [`core/management/commands/`](../../core/management/commands/).

Things that hold for all of them:

- They act on the database of the active settings (`DJANGO_ENVIRONMENT`, see
  [Configuration](../getting-started/configuration.md)) with no permission checks: the
  person at the shell is trusted.
- Files they write (`--output`, `--export`) are written relative to the current
  directory unless you give an absolute path.
- Several write with `QuerySet.update()` or `delete()`, which skips model `save()`,
  `clean()` and signals. The per-command notes say where.
- Run them from the repository root; `populate_gamedata` and `reset_db` depend on it.

## Summary

| Command | App | Writes? | Purpose |
|---------|-----|---------|---------|
| [`populate_gamedata`](#populate_gamedata) | core | yes | Load game reference data from `populate_db/`. |
| [`reset_db`](#reset_db) | core | deletes files | Delete `db.sqlite3` and the generated migration files of local apps (development only). |
| [`reset_demo_data`](#reset_demo_data) | core | yes, destructive | Delete all game data and create a demo storyteller, player and chronicle. |
| [`populate_test_chronicle`](#populate_test_chronicle) | core | yes | Add sample characters and scenes to a chronicle. |
| [`approve_pending_items`](#approve_pending_items) | core | yes | Bulk-approve submitted characters, images, freebies and weekly XP requests. |
| [`process_weekly_xp`](#process_weekly_xp) | core | yes | Create a `Week` and a `WeeklyXPRequest` for each character who played that week. |
| [`audit_xp_spending`](#audit_xp_spending) | core | CSV only | Report characters whose approved or pending XP spends exceed their XP. |
| [`cleanup_old_weeks`](#cleanup_old_weeks) | core | yes | Delete old `Week` rows. |
| [`cleanup_orphaned_data`](#cleanup_orphaned_data) | core | yes | Delete XP requests without a character and, optionally, unowned drafts, empty scenes and unused setting elements. |
| [`archive_inactive_chronicles`](#archive_inactive_chronicles) | core | optional | List inactive chronicles; optionally export and rename them. |
| [`sync_character_status`](#sync_character_status) | core | yes | Remove retired and deceased characters from groups, chantries and scenes. |
| [`find_duplicate_objects`](#find_duplicate_objects) | core | optional | Find same-name objects; optionally delete duplicates. |
| [`validate_character_data`](#validate_character_data) | core | optional | Report character data problems. |
| [`validate_data_integrity`](#validate_data_integrity) | core | optional | Check ranges, statuses and duplicate ST relationships; optionally fix them. |
| [`monitor_validation`](#monitor_validation) | core | no | Print a health score from integrity, XP and scene checks. |
| [`audit_user_permissions`](#audit_user_permissions) | core | CSV only | Report storyteller relationships and profile completeness. |
| [`generate_chronicle_summary`](#generate_chronicle_summary) | core | file only | Statistics for one chronicle as text, Markdown or HTML. |
| [`generate_st_report`](#generate_st_report) | core | file only | Pending approvals, active scenes and character counts per chronicle. |
| [`export_chronicle`](#export_chronicle) | core | file only | Export a chronicle and related rows to JSON. |
| [`import_chronicle`](#import_chronicle) | core | yes | Create a chronicle (and optionally users) from an export file. |

Commands from installed packages that you may also use: `runserver` (replaced by
Daphne's ASGI server, see [Local development](../getting-started/local-development.md)),
`runworker` (Channels) and, in development, `debugsqlshell` (django-debug-toolbar).

## Setup and sample data

### `populate_gamedata`

Loads the reference data by executing every script under `populate_db/` in a fixed
order, each in its own transaction. Full description, ordering and filter behaviour:
[Seed data](../getting-started/seed-data.md).

| Option | Effect |
|--------|--------|
| `--gameline TEXT` | Keep scripts whose file stem contains `TEXT`, plus scripts whose stem names no gameline. Matches the long names (`vampire`, `mage`...); the short codes in the help text match no file names. |
| `--only TEXT` | Keep scripts whose file stem contains `TEXT`. |
| `--skip TEXT` | Drop scripts whose file stem contains `TEXT`. |
| `--dry-run` | List the scripts that would run, in order. |
| `--verbose` | Per-file progress and a traceback for each failure. |

Side effects: creates and updates reference rows; never deletes. A failing script is
reported and skipped; the command still exits with status 0.

When: after creating a database, and after pulling changes to `populate_db/`.

### `reset_db`

Deletes `db.sqlite3` in the current directory and every `*.py` file except `__init__.py`
in each top-level `*/migrations/` directory except `tg_schema/migrations/`, whose
committed migrations it keeps. Refuses to run unless `DEBUG` is true.

| Option | Effect |
|--------|--------|
| `--yes` | Skip the `[y/N]` confirmation. |

When: only in development, normally through [`setup_db.sh`](../../setup_db.sh) (see
[Seed data](../getting-started/seed-data.md#setup_dbsh-and-reset_db)).

### `reset_demo_data`

Raises `CommandError` unless `DEBUG` is true or `--force` is given. Without `--confirm`
it prints a warning and exits. With it, inside one transaction: deletes every
`WeeklyXPRequest`, `StoryXPRequest`, `Week`, `Scene`, character, item, location and
`Chronicle`; deletes every non-superuser `User` unless `--preserve-users`; then creates
users `demo_st` and `demo_player` if they do not exist, and the chronicle "Demo
Chronicle: Nights of Seattle" with `demo_st` as storyteller. New demo accounts get the
`--password` value or, by default, a random password that the command prints once;
existing accounts keep theirs.

| Option | Effect |
|--------|--------|
| `--confirm` | Required to do anything. |
| `--preserve-users` | Keep existing user accounts. |
| `--password TEXT` | Password for newly created demo accounts (default: random, printed). |
| `--force` | Run even when `DEBUG` is false. Never use it on a real installation. |

Reference data (loaded by `populate_gamedata`) is kept.

When: resetting a development or demo instance.

### `populate_test_chronicle`

Adds sample play data to an existing chronicle: gets or creates user `test_player`
(password `test123` when created), creates `--characters` mortal characters of the
`--gameline`'s model (`VtMHuman` for `vtm`, `MtAHuman` for `mta`, core `Human` for `wod`
and so on) owned by that user with random names, concepts, statuses (weighted to `App`) and 0–50 XP, gets or
creates a location "The Elysium" in the chronicle, and creates `--scenes` scenes on
consecutive past days, each with two to five of the new characters. All but the last
three scenes are marked finished with `xp_given=True`.

| Option | Effect |
|--------|--------|
| `--chronicle ID` | Required. The chronicle to fill. |
| `--characters N` | Number of characters (default 10). |
| `--scenes N` | Number of scenes (default 15). |
| `--gameline {ctd,dtf,htr,mta,mtr,vtm,wod,wta,wto}` | Model of the characters (default `vtm`). |

When: trying out chronicle, scene and XP pages locally.

## Approvals and XP

See [XP and approvals](../architecture/xp-and-approvals.md) for the normal, in-app flow
these commands shortcut.

### `approve_pending_items`

Lists pending items and approves them through the same services and model methods as
the storyteller pages. Listing (`--list-only`, `--dry-run`) works site-wide with no
further options. Approving needs a scope (`--chronicle`, `--owner` or `--all`) and an
`--approver`, and asks `Approve N item(s) as USER? [y/N]` unless `--noinput`; otherwise
it raises `CommandError`. Each object is checked against the approver's `APPROVE`
permission (staff, or a storyteller of the object's chronicle and gameline); objects the
approver may not approve, or that fail validation, are skipped and listed in the
summary.

| Option | Effect |
|--------|--------|
| `--type {characters,images,freebies,xp-requests,all}` | What to process (default `all`). |
| `--chronicle ID` | Only objects in this chronicle. |
| `--owner USERNAME` | Only objects owned by this user. An unknown user is a `CommandError`. |
| `--all` | Approve across every chronicle and owner. |
| `--approver USERNAME` | The user approving; required to approve. |
| `--noinput`, `--no-input` | Skip the confirmation. |
| `--auto-approve-images` | Also process images whatever `--type` says. |
| `--list-only` | List pending items; change nothing. |
| `--dry-run` | Say what would be approved; change nothing. |

What each type does:

| Type | Action |
|------|--------|
| `characters` | Submitted characters, through `ApprovalService.approve_object` (status `Sub` → `App`, group pooled backgrounds updated). |
| `images` | Characters, items and locations with `image_status="sub"` and an image, through `ApprovalService.approve_image`. |
| `freebies` | Submitted `Human` characters with `freebies_approved=False`, through `award_backstory_freebies(0)`: approved with no backstory freebies. Award freebies from the storyteller page instead when some are due. |
| `xp-requests` | Unapproved `WeeklyXPRequest` rows, through `WeeklyXPRequest.approve()`, which awards the XP. Story XP requests are not processed. |

XP spends (`XPSpendingRequest`) are not bulk-approved: each needs a storyteller decision
on the trait. When: clearing a backlog by hand, with `--list-only` first.

### `process_weekly_xp`

Creates the `Week` ending on the given Sunday if it does not exist, finds the non-NPC
`Human` characters in finished scenes whose latest post is dated between seven days
before the end date and the end date (both inclusive), and creates a `WeeklyXPRequest` (`finishing=True`) for each one
that has none for that week.

| Option | Effect |
|--------|--------|
| `--week-ending YYYY-MM-DD` | The week's end date. Default: `game.models.get_next_sunday(today)`, which is the coming Sunday, or today when today is a Sunday (the help text says "last Sunday"). Pass the date explicitly to process a finished week. |
| `--auto-approve` | Create the requests approved and call `character.add_xp()` with each request's total. |
| `--notify` | Prints that notifications are not implemented; sends nothing. |
| `--dry-run` | Report without creating the week or requests. |

For an existing week it uses `Week.weekly_characters()`. Safe to re-run: existing
requests are skipped.

When: weekly, by hand or from a scheduler, if requests are not created in the app.

### `audit_xp_spending`

Read-only report over characters with status `Sub` or `App` (optionally one chronicle).
For each character with an `xp` field it sums `XPSpendingRequest` costs by status and
reports:

- an issue when approved spends exceed earned XP;
- warnings when pending spends exceed the remaining XP, when pending spends are older than
  `--pending-days`, when a character has more than 15 pending or more than 100 approved
  spends.

It then lists unapproved `WeeklyXPRequest` rows (oldest ten by week) and XP requests
with no character.

| Option | Effect |
|--------|--------|
| `--chronicle ID` | Only this chronicle. |
| `--show-all` | Include characters with no issues (first ten shown). |
| `--export FILE` | Also write the per-character results to CSV. |
| `--pending-days N` | Warn about pending spends created more than `N` days ago (default 30). |

## Maintenance

### `cleanup_old_weeks`

Deletes `Week` rows whose `end_date` is more than `--months × 30` days ago. Their
`WeeklyXPRequest` rows remain with `week` set to null (`on_delete=SET_NULL`); characters'
XP is unaffected.

| Option | Effect |
|--------|--------|
| `--months N` | Age threshold (default 6). |
| `--keep-with-pending` | Keep weeks that have an unapproved `WeeklyXPRequest`. |
| `--dry-run` | List without deleting. |

### `cleanup_orphaned_data`

By default deletes every `WeeklyXPRequest` and `StoryXPRequest` with no character.

| Option | Effect |
|--------|--------|
| `--include-unowned-drafts` | Also delete characters, items and locations that belong to a chronicle and have no owner and status `Un`. |
| `--include-scenes` | Also delete unfinished scenes with no posts and no characters. |
| `--include-setting-elements` | Also delete `SettingElement` rows linked to no chronicle. |
| `--dry-run` | List without deleting. |

`--include-unowned-drafts` never touches reference data (weapons, talismans, fetishes and
other items loaded by `populate_gamedata` have no owner and status `Un` but no
chronicle). It does match drafts whose owner account was deleted **and** a storyteller's
shared drafts, which are created with no owner. Objects have no creation date, so there
is no age threshold. Run it with `--dry-run` first.

### `archive_inactive_chronicles`

Finds chronicles whose most recent scene (`date_of_scene`) is older than `--days`, or
that have no dated scene, **and** that have either no unfinished scene or no character
with status `Sub` or `App`. Lists them with storytellers and counts. Nothing is deleted.

| Option | Effect |
|--------|--------|
| `--days N` | Inactivity threshold (default 90). |
| `--list-only` | Only list, even if other options are given. |
| `--export-before-archive` | Run `export_chronicle --pretty` for each into `chronicle_archives/archive_<id>_<name>.json` (directory created in the current directory). |
| `--mark-inactive` | Prefix each chronicle's name with `[ARCHIVED] ` (skipped if already prefixed). |

Without `--export-before-archive` or `--mark-inactive` it only lists.

### `sync_character_status`

For each character with status `Ret` or `Dec`: removes it from every `Group`'s members,
clears it as group leader, and, for characters with chantry relations, removes it from
chantry membership, leadership, investigator, guardian and teacher roles and clears it
as ambassador or node tender. Each character is processed in its own transaction.

| Option | Effect |
|--------|--------|
| `--chronicle ID` | Only this chronicle. |
| `--remove-from-scenes` | Also remove the character from unfinished scenes. |
| `--dry-run` | Report without changing anything. |

When: after retiring or killing characters in bulk.

### `find_duplicate_objects`

Groups objects by lower-cased, trimmed name plus owner plus chronicle and reports every
group with more than one member, for `CharacterModel`, `ItemModel`, `LocationModel`
and Mage `Effect`.

| Option | Effect |
|--------|--------|
| `--type {character,item,location,effect,all}` | Which models (default `all`). |
| `--chronicle ID` | Only this chronicle. |
| `--owner USERNAME` | Only this owner's objects. |
| `--auto-merge` | In each group, keep the object with the highest status (`App` > `Sub` > `Un` > others, ties to the highest ID) and **delete** the others, but only when every other member has the same status and description as the keeper. Nothing is merged: related rows of the deleted objects go with them according to their `on_delete`. |
| `--delete-empty` | In each group, delete members with status `Un` and an empty description, keeping the oldest when every member is empty. Ignored when `--auto-merge` is given. |
| `--export FILE` | Write the groups to CSV. |

Without `--auto-merge` or `--delete-empty` it is read-only.

## Integrity checks

### `validate_character_data`

Checks every character (optionally filtered) and reports:

- attributes (`strength` ... `appearance`) outside 0–15;
- missing name; missing concept on `Sub` or `App` characters; missing owner on `App`
  characters;
- retired or deceased characters still in unfinished scenes;
- a negative `xp` balance (`xp` is the unspent balance: a spend deducts its cost when it
  is requested);
- more than 20 pending `XPSpendingRequest` rows on one character.

| Option | Effect |
|--------|--------|
| `--status CODE` | Only characters with this status (`Un`, `Sub`, `App`, `Ret`, `Dec`, `Rev`). |
| `--chronicle ID` | Only this chronicle. |
| `--verbose` | Show sub-issues and fixes. |
| `--fix` | Set negative attributes to 1 and save. Nothing else is fixed. |

### `validate_data_integrity`

Runs eight numbered checks and prints what it finds. With `--fix` it repairs them with
`QuerySet.update()` (except where noted):

| Check | Fix |
|-------|-----|
| `Character.xp` below 0 | Set to 0. |
| `status` not a `core.constants.CharacterStatus` code (`Un`, `Rev`, `Sub`, `App`, `Dec`, `Ret`) | Set to `Un`. |
| `Human` attributes outside 1–10 | Clamp to 1 or 10. |
| 19 `Human` abilities (`alertness` ... `science`) outside 0–10 | Clamp to 0 or 10. |
| `willpower` outside 1–10, `temporary_willpower` outside 0–10, temporary above permanent | Clamp; temporary above permanent is set equal to permanent with `save()`. |
| `age` below 0 or above 500; `apparent_age` below 0 or above 200 | Negative values set to null; high values clamped. |
| Duplicate `STRelationship` for the same user, chronicle and gameline | Keep the first, delete the rest. |
| Scenes with XP given / finished scenes awaiting XP | Information only. |

| Option | Effect |
|--------|--------|
| `--fix` | Apply the fixes above. |
| `--verbose` | List each offending row. |

### `monitor_validation`

Read-only. Collects: integrity counts (characters with negative XP; with a status
that is not a `CharacterStatus` code; `Human` attributes
outside 1–10 and abilities outside 0–10; temporary willpower above permanent),
`XPSpendingRequest`
totals and approval rate (all time), scenes played within `--period` hours and how many
await XP, and character totals by status. Computes a health score from 100: minus 5 per
integrity issue (at most 50), minus 10 if the XP approval rate is below 80 %, minus 10 if
more than 10 scenes await XP. A score of 90 or more is `healthy`, otherwise `degraded`.

| Option | Effect |
|--------|--------|
| `--period HOURS` | Window for the scene checks (default 24). |
| `--json` | Print the metrics as JSON. |
| `--alert` | When degraded, also print an alert block to stdout. Nothing is sent. |

## Reports

### `audit_user_permissions`

Read-only. Prints user, chronicle and storyteller counts, each chronicle's storytellers,
and users with an `STRelationship` whose chronicle is null.

| Option | Effect |
|--------|--------|
| `--check-profiles` | Also report how many profiles set lines, veils and a Discord ID, and how many show them. |
| `--export FILE` | Write one CSV row per user: username, e-mail, whether they are an ST, their chronicles, and profile flags. |

### `generate_chronicle_summary`

Read-only. Statistics for one chronicle: storytellers, theme, mood and year; scene
counts; character counts by status and PC/NPC; total and average XP of approved
characters and their pending weekly XP requests; unique players; the five characters in
the most scenes.

| Option | Effect |
|--------|--------|
| `chronicle_id` | Required positional argument. |
| `--format {text,html,markdown}` | Output format (default `text`). |
| `--output FILE` | Write to a file instead of stdout (any format). |

### `generate_st_report`

Read-only. For each chronicle in scope: storytellers; counts of submitted characters,
pending images, pending freebies and unapproved weekly XP requests; active scenes (first
five listed); characters by status and PC/NPC.

| Option | Effect |
|--------|--------|
| `--st-username USERNAME` | Chronicles where this user is in `storytellers`. Takes precedence over `--chronicle`. |
| `--chronicle ID` | One chronicle. |
| `--output FILE` | Write to a file instead of stdout. |

Without either scope option it covers every chronicle.

## Export and import

### `export_chronicle`

Writes one JSON file with `export_date`, `export_version` (`"1.0"`), the chronicle
(Django-serialized, plus a list of storyteller usernames), and Django-serialized lists
of the chronicle's characters, items, locations, common-knowledge setting elements,
scenes, journals of its characters, and weekly and story XP requests of its characters.

| Option | Effect |
|--------|--------|
| `chronicle_id` | Required positional argument. |
| `--output FILE` | Output path. Default: `chronicle_<id>_<name with non-alphanumerics as _>_<YYYY-MM-DD>.json` in the current directory. |
| `--pretty` | Indent the JSON. |
| `--exclude-scenes` | Leave out scenes and journals. |
| `--include-users` | Add the chronicle's storytellers and character owners as serialized `User` rows with only `username`, `email`, `first_name` and `last_name` (no password hashes, flags or permissions). The file still holds e-mail addresses; treat it as personal data. |

### `import_chronicle`

Reads an `export_chronicle` file, prints a summary and, unless `--dry-run`, in one
transaction:

- creates users from the `users` section that do not exist yet (username, e-mail, first
  and last name only, with an unusable password: they reset it to log in), unless
  `--skip-users`;
- creates a new `Chronicle` from the name, theme, mood, year and headings, and adds the
  listed storytellers that exist;
- gets or creates `SettingElement` rows by name and links them to the chronicle.

Characters, items, locations, scenes, journals and XP requests in the file are counted
and reported but **not imported**.

| Option | Effect |
|--------|--------|
| `filename` | Required positional argument. |
| `--dry-run` | Print the summary only. |
| `--skip-users` | Do not create users. |
| `--remap-users FILE` | JSON object mapping old usernames to new ones, applied to created users and storytellers. |

## See also

- [Seed data](../getting-started/seed-data.md)
- [XP and approvals](../architecture/xp-and-approvals.md)
- [Maintenance](../operations/maintenance.md)
- [`core/` app](../../core/README.md)
- [`game/` app](../../game/README.md)
