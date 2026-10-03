# tg_schema migrations

This page describes each migration in [`tg_schema/migrations/`](../migrations/): the
change it makes, the guards that make it safe to run on any database, what it does to
existing data, and the tests that cover it. It is for anyone upgrading an older database
or reading a migration before changing the models it touches. The general rules are in
[schema migrations](../../docs/architecture/schema-migrations.md).

## Common properties

All migrations share these properties:

- one `migrations.RunPython(forward, migrations.RunPython.noop)` operation, in a single
  linear chain (`0001` has `initial = True`; each later one depends on the previous);
- the forward function ignores its `apps` argument (the historical registry has no models
  for the local apps) and uses the helpers in [`schema.py`](../schema.py) or raw SQL;
- it imports nothing from the local apps;
- it returns without error when its model, field, table or column no longer exists;
- the reverse is a no-op: unapplying leaves the schema and data as they are;
- on a fresh or test database (tables built from the current models) it changes nothing.

Two generic tests in
[`tests/test_schema_helpers.py`](../tests/test_schema_helpers.py) cover every migration:
`test_migrations_import_no_app_models` parses each file for imports from the local apps,
and `test_every_migration_runs_when_its_models_are_gone` runs each forward function with
`apps.get_model` patched to raise `LookupError`.

## Summary

| Migration | Tables | Kind |
|-----------|--------|------|
| `0001_scene_visibility` | `game.Scene` | Column |
| `0002_chantry_rating_linked_object` | `locations.ChantryBackgroundRating` | Columns |
| `0003_discipline_property_names` | `characters.Discipline` | Data |
| `0004_scene_rolls_and_read_marker` | `game.Post`, `game.UserSceneReadStatus` | Columns and data |
| `0005_story_chronicle` | `game.Story` | Column |
| `0006_sheet_cover_facts` | `characters.Werewolf` | Column |
| `0007_assign_story_chronicles` | `game.Story` | Data |
| `0008_unique_scene_read_status` | `game_userscenereadstatus` | Data and unique index (raw SQL) |
| `0011_retire_custom_visibility` | All 53 concrete roots storing `PermissionMixin.visibility` | Data (raw SQL) |

## 0001_scene_visibility

[`0001_scene_visibility.py`](../migrations/0001_scene_visibility.py)

- **Change**: adds the `visibility` column of `game.Scene` with
  `add_missing_columns(schema_editor, "game.Scene", ("visibility",))`.
- **Guards**: skipped when the model, its table or the field is missing, or the column
  exists.
- **Data**: existing scenes get the field's default, `Scene.Visibility.CHRONICLE`.
- **Tests**: only the generic ones.

## 0002_chantry_rating_linked_object

[`0002_chantry_rating_linked_object.py`](../migrations/0002_chantry_rating_linked_object.py)

- **Change**: adds `linked_location` and `linked_character` (nullable foreign keys) to
  `locations.ChantryBackgroundRating`.
- **Guards**: as `add_missing_columns`; each column is added only if missing.
- **Data**: existing ratings get `NULL` in both.
- **Tests**: [`test_chantry_rating_linked_object.py`](../tests/test_chantry_rating_linked_object.py)
  (adds each missing column; leaves existing columns alone).

## 0003_discipline_property_names

[`0003_discipline_property_names.py`](../migrations/0003_discipline_property_names.py)

- **Change**: for each name in `DISCIPLINE_FIELDS` (the Vampire discipline trait fields,
  from `celerity` to `visceratika`), sets `property_name` to that field name on
  `characters.Discipline` rows whose `name` matches it case-insensitively and whose
  `property_name` is empty. This links reference rows to character trait fields.
- **Guards**: returns if `Discipline` or its `property_name` field is gone. Rows that
  already have a `property_name` are not touched, so a rerun changes nothing.
- **Data**: updates reference data only.
- **Tests**: only the generic ones.

## 0004_scene_rolls_and_read_marker

[`0004_scene_rolls_and_read_marker.py`](../migrations/0004_scene_rolls_and_read_marker.py)

- **Change**: adds `game.Post.roll` (nullable JSON, the outcome of a dice command for the
  scene's roll strip) and `game.UserSceneReadStatus.last_read_post` (nullable foreign key
  to `Post`, the unread divider's position).
- **Guards**: each column only if missing. The backfill runs only when
  `add_missing_columns` reports that it added `last_read_post`, that is only in the run
  that creates the column, when the models match the data being written.
- **Data**: existing posts keep `roll = NULL` and show their message text. For read
  statuses with no marker: a status marked read gets the scene's latest post (highest
  `pk`); an unread one gets the user's own latest post in the scene (through
  `character__owner`), or stays `NULL` if they never posted there.
- **Tests**: [`test_scene_rolls_and_read_marker.py`](../tests/test_scene_rolls_and_read_marker.py)
  (adds each missing column; leaves existing columns alone; backfills the new marker).

## 0005_story_chronicle

[`0005_story_chronicle.py`](../migrations/0005_story_chronicle.py)

- **Change**: adds the nullable `chronicle` foreign key to `game.Story`.
- **Guards**: as `add_missing_columns`.
- **Data**: existing stories are left without a chronicle; `0007` assigns them.
- **Tests**: [`test_story_chronicle.py`](../tests/test_story_chronicle.py) (adds the
  column and keeps stories; leaves an existing column alone).

## 0006_sheet_cover_facts

[`0006_sheet_cover_facts.py`](../migrations/0006_sheet_cover_facts.py)

- **Change**: adds `deed_name` to `characters.Werewolf` (defined in
  `characters/models/werewolf/garou.py`). `SHEET_FIELDS` is a list of
  `(model label, field names)` pairs, so further sheet columns can join it.
- **Guards**: as `add_missing_columns`.
- **Data**: existing Garou get the field's default, an empty string.
- **Tests**: [`test_sheet_cover_facts.py`](../tests/test_sheet_cover_facts.py).

## 0007_assign_story_chronicles

[`0007_assign_story_chronicles.py`](../migrations/0007_assign_story_chronicles.py)

- **Change**: gives each story without a chronicle the chronicle its characters play in.
  A story's only link to play is its `StoryXPRequest` rows. In one grouped query it takes,
  per story without a chronicle, the lowest and highest chronicle of the request
  characters that have one; when they are equal, it sets the story's `chronicle_id`.
- **Guards**: returns if `Story.chronicle`, `StoryXPRequest.story` or
  `StoryXPRequest.character` is gone. The update is filtered on `chronicle__isnull=True`,
  so assigned stories are never changed and a rerun does nothing.
- **Data**: stories whose characters span several chronicles, or have no placed
  characters, stay unassigned for staff to place by hand. Characters without a chronicle
  are ignored.
- **Tests**: [`test_assign_story_chronicles.py`](../tests/test_assign_story_chronicles.py)
  (shared chronicle; characters without a chronicle; several chronicles; no placed
  characters; assigned stories and reruns; one query for the spans and one update per
  story).

## 0008_unique_scene_read_status

[`0008_unique_scene_read_status.py`](../migrations/0008_unique_scene_read_status.py)

- **Change**: makes `(user, scene)` unique in `game_userscenereadstatus`. Raw SQL: the
  table (`TABLE`), the columns (`COLUMNS`: `id`, `user_id`, `scene_id`, `read`,
  `last_read_post_id`) and the index (`INDEX = "unique_user_scene_read_status"`) are
  module constants, quoted with `connection.ops.quote_name`, so later model changes cannot
  alter what it does.
- **Guards**: returns if the table is missing or lacks any of the columns (a later rename
  owns it). Creates the index only if `has_unique_user_scene()` finds no unique
  constraint or index on exactly `(scene_id, user_id)`; a fresh database has one from the
  model's `Meta`.
- **Data**, in order:
  1. deletes rows whose `user_id` or `scene_id` is `NULL` (the model now cascades on
     delete, so such rows can no longer arise);
  2. for each `(user_id, scene_id)` with more than one row, keeps the oldest (lowest
     `id`), sets its `read` to true only if every copy was read and its
     `last_read_post_id` to the highest marker among the copies, and deletes the others;
  3. creates the unique index.
- **Tests**: [`test_unique_scene_read_status.py`](../tests/test_unique_scene_read_status.py)
  rebuilds the table without the constraint (as older databases have it) and checks the
  merge, the deletion of orphaned rows, that an existing constraint is left alone, that a
  renamed marker column skips the migration, and the cascade.

## 0011_retire_custom_visibility

[`0011_retire_custom_visibility.py`](../migrations/0011_retire_custom_visibility.py)

- **Change**: retires the unsupported `CUS` (Custom) visibility choice by replacing
  only those values with `PRI`. The abstract `PermissionMixin` and `core.models.Model`
  create no table of their own; the migration freezes all 53 concrete owning tables,
  including character reference data, `CharacterModel`, `Group`, `CharacterTemplate`,
  `ItemModel` and `LocationModel`. Descendant tables inherit the root's column and
  are not updated separately.
- **Guards**: looks up each live model and field without importing app models, and
  skips a missing or renamed model, field, table or column, or a field that is no
  longer stored locally. SQL runs on the migration's connection with quoted table
  and column names. A rerun leaves data unchanged; reversal is a no-op.
- **Data**: `PUB`, `PRI`, `CHR` and other stored values are unchanged. Existing owner,
  storyteller and observer grants are unchanged. `PRI` preserves the restriction on
  detail-card admission to full viewers; list discovery permissions are unchanged.
- **Tests**: [`test_retire_custom_visibility.py`](../tests/test_retire_custom_visibility.py)
  checks all owning tables, unchanged values, idempotence, missing and renamed schema,
  field ownership, unrelated visibility columns, the supplied non-default connection
  and the no-op reverse.

## See also

- [Writing a migration](writing-a-migration.md)
- [Schema migrations](../../docs/architecture/schema-migrations.md)
- [Changing the schema](../../docs/guides/changing-the-schema.md)
- [game app](../../game/README.md)
- [`tg_schema/schema.py`](../schema.py)
