# game models

This page is the reference for every model in [`game/models.py`](../models.py): fields,
relations, managers, methods and the rules they enforce. Read it before changing a
model or writing code that creates or queries these rows. Schema changes follow
[changing the schema](../../docs/guides/changing-the-schema.md); the app itself has no
migration files.

Models that inherit `core.base.ValidatedSaveMixin` run `full_clean()` on every
`save()` (pass `skip_validation=True` to skip it): `ObjectType`, `SettingElement`,
`Gameline`, `Chronicle`, `STRelationship`, `Story`, `Week` and `WeeklyXPRequest`. The
others (`Scene`, `Post`, `UserSceneReadStatus`, `Journal`, `JournalEntry`,
`StoryXPRequest`, `XPSpendingRequest`, `FreebieSpendingRecord`) are plain Django models.

## Relationship overview

```text
Chronicle ──< STRelationship >── User
    │               └── Gameline
    ├── head_st ──> User
    ├── game_storytellers >──< User
    ├── common_knowledge_elements >──< SettingElement
    ├── allowed_objects >──< ObjectType
    ├──< Story ──< StoryXPRequest >── CharacterModel
    └──< Scene ──< Post >── CharacterModel
           ├── characters >──< CharacterModel
           ├── location ──> LocationModel
           └──< UserSceneReadStatus >── User

Week ── characters >──< CharacterModel
  └──< WeeklyXPRequest >── CharacterModel (four optional Scene links)

CharacterModel ──1 Journal ──< JournalEntry
CharacterModel ──< XPSpendingRequest, FreebieSpendingRecord
```

## Reference and configuration models

### ObjectType

A creatable object type for a gameline, used to limit what players may create in a
chronicle (`Chronicle.allowed_objects`).

| Field | Notes |
|-------|-------|
| `name` | Type key, e.g. a model's type name; must be non-empty |
| `type` | `char`, `loc` or `obj` (`core.constants.ObjectTypeChoices`) |
| `gameline` | A `core.constants.GameLine` code; validated with `core.validators.validate_gameline` |

Ordered by `type`, `gameline`, `name`. `__str__` is `"<gameline>/<type>/<name>"` using
the display labels.

### SettingElement

A piece of common knowledge (`name`, `description`, `gameline`, default `wod`).
Chronicles attach them through `Chronicle.common_knowledge_elements`. `name` must be
non-empty. URL: `game:setting_element:detail`.

### Gameline

A named game line (`name`), referenced by `STRelationship.gameline`. The rows are
seeded by [`populate_db/aa_gamelines.py`](../../populate_db/aa_gamelines.py). The
`name` must equal the `name` of an entry in `settings.GAMELINES` (for example
`"Mage: the Ascension"`): scoped storyteller checks in `core.permissions` and
`game.selectors.scene_storyteller_ids` compare `Gameline.name` with
`settings.GAMELINES[code]["name"]`.

## Chronicles and storytellers

### Chronicle

| Field | Notes |
|-------|-------|
| `name` | Required (validated non-blank) |
| `head_st` | `ForeignKey(User, SET_NULL)`, related name `chronicles_as_head_st`: the storyteller with full control |
| `game_storytellers` | `ManyToManyField(User)`, related name `chronicles_as_game_st`: view-only storytellers |
| `storytellers` | `ManyToManyField(User, through="STRelationship")` |
| `theme`, `mood` | Free text, optional |
| `common_knowledge_elements` | `ManyToManyField(SettingElement)` |
| `year` | `IntegerField`, default 2022; must be between 1000 and 9999 when set |
| `headings` | `HeadingChoices` value or blank |
| `allowed_objects` | `ManyToManyField(ObjectType)`: the types players without an ST role may create here |

Methods:

- `get_absolute_url()` → `game:chronicle`; `get_retired_character_url()`,
  `get_deceased_character_url()`, `get_npc_url()` → the character index pages under the
  chronicle.
- `get_scenes()`, `get_active_scenes()`, `total_scenes()`.
- `add_scene(name, location, date_of_scene=None, gameline=None)`: returns the existing
  scene with that name and location in this chronicle, or creates one. `location` may be
  a `LocationModel` or a location name.
- `add_setting_element(name, description)`: get-or-create and attach.
- `players`: cached property, the distinct users owning a character in the chronicle.
- `storyteller_list()`: comma-separated usernames from `storytellers`.
- `is_head_st(user)`, `is_game_st(user)`.

### STRelationship

Makes a user a storyteller for one gameline of one chronicle.

| Field | Notes |
|-------|-------|
| `user` | `ForeignKey(User, SET_NULL)`, related name `st_relationships` |
| `chronicle` | `ForeignKey(Chronicle, SET_NULL)`, related name `st_relationships` |
| `gameline` | `ForeignKey(Gameline, SET_NULL)`, related name `st_relationships` |

- All three are required by `clean()` even though the columns are nullable.
- Unique on `(user, chronicle, gameline)` (constraint `unique_st_per_chronicle_gameline`).
- Ordered by `gameline__id`.
- Manager: `STRelationship.objects.for_user_optimized(user)` joins `chronicle` and
  `gameline`.

A matching `STRelationship` grants the `CHRONICLE_ST` role for objects of that
gameline; any relationship in the chronicle grants read access to its staff data. See
[authorization](../../docs/architecture/authorization.md) for the full role model.

## Stories

### Story

| Field | Notes |
|-------|-------|
| `name` | Required |
| `xp_given` | `True` once story XP was awarded |
| `chronicle` | `ForeignKey(Chronicle, SET_NULL, null=True)`, related name `stories`. Stories without a chronicle are listed to chronicle managers as "unassigned". |

`award_xp(character_awards)` is atomic: it converts each character's category dict
(`success`, `danger`, `growth`, `drama` booleans and `duration` integer) with
`core.xp_utils.calculate_story_xp` and applies them with
`core.xp_utils.award_xp_atomically`, which raises `ValidationError` if `xp_given` is
already true. See [XP](xp.md).

### StoryXPRequest

A per-character story XP record: `story` and `character` (both `SET_NULL`), booleans
`success`, `danger`, `growth`, `drama`, and integer `duration`. It has no approval field
and no method that awards XP; the admin shows a computed total.

## Scenes

### Scene

| Field | Notes |
|-------|-------|
| `name` | Title |
| `visibility` | `Scene.Visibility`: `CHRONICLE` (default), `PARTICIPANTS`, `PUBLIC`; indexed |
| `chronicle` | `ForeignKey(Chronicle, SET_NULL, null=True)` |
| `date_played` | `auto_now_add` date |
| `date_of_scene` | In-game date, default today, nullable |
| `characters` | `ManyToManyField("characters.CharacterModel")`, related name `scenes` |
| `location` | `ForeignKey("locations.LocationModel", SET_NULL, null=True)` |
| `user_read_status` | `ManyToManyField(User, through="UserSceneReadStatus")` |
| `finished` | Closed scenes are read-only; indexed |
| `xp_given` | Scene XP awarded |
| `waiting_for_st` | A player addressed the storyteller with `@storyteller` |
| `st_message` | The text of that message (up to 300 characters) |
| `gameline` | `GameLine` code, default `wod`; decides which gameline's STs manage the scene |

Ordering: `-date_of_scene`, `-date_played`.

`Scene.objects` is built from `SceneQuerySet`, so every method is chainable:

| Method | Filter |
|--------|--------|
| `active()` / `finished()` | `finished=False` / `True` |
| `awaiting_xp()` | `finished=True, xp_given=False` |
| `waiting_for_st()` | `waiting_for_st=True` |
| `with_location()` | `select_related("location")` |
| `for_chronicle(c)`, `active_for_chronicle(c)` | By chronicle |
| `for_user_chronicles(user)` | Chronicles in `staffed_chronicles(user)`; staff and superusers also get scenes without a chronicle |

Methods:

- `add_character(character)`: adds a character (or looks one up by name).
- `add_post(character, display, message)`: the model-level posting rule. See
  [scenes](scenes.md#posting). Returns the new `Post`, or `None` for a storyteller
  message or a malformed dice command.
- `close()`: sets `finished`, enrolls every character in the `Week` ending on the
  Sunday on or after the latest post's date (today if there are no posts), and saves.
- `award_xp(character_awards)`: `{character: bool}`; 1 XP per `True`, atomic, raises
  `ValidationError` when `xp_given` is already set.
- `most_recent_post()`, `total_posts()`, `total_characters()`, `get_absolute_url()`
  (`game:scene`).

`__str__` returns `name`; for an empty name (or `''`) it returns the location (or
"Scene") and `date_of_scene`, falling back to `date_played`.

### Post

| Field | Notes |
|-------|-------|
| `character` | `ForeignKey(CharacterModel, SET_NULL)` |
| `display_name` | Name shown on the post (defaults to the character's name in `add_post`) |
| `scene` | `ForeignKey(Scene, SET_NULL)` |
| `message` | Stored text, with any dice roll written out as HTML |
| `datetime_created` | Default `now`, indexed |
| `roll` | `JSONField`, nullable: the dice command's outcome as data (`roll_record`) |

Ordered by `datetime_created`, with indexes on `-datetime_created`,
`(scene, -datetime_created)` and `(character, -datetime_created)`. The scene code
orders by `pk`, which follows creation order for posts the app creates.

- `Post.objects.for_scene_optimized(scene)` joins `character` and `character__owner`.
- `roll_strip` (cached property) returns `game.rolls.roll_strip(self.roll)`: the roll
  strip dict, or `None` to show the message text.

### UserSceneReadStatus

One row per `(user, scene)`: whether the user has read the scene and how far.

| Field | Notes |
|-------|-------|
| `user` | `ForeignKey(User, CASCADE, null=True)`, related name `scene_read_statuses` |
| `scene` | `ForeignKey(Scene, CASCADE, null=True)`, related name `user_read_statuses` |
| `read` | Default `True` |
| `last_read_post` | `ForeignKey("game.Post", SET_NULL, null=True)`: the newest post the user has seen |

Unique on `(user, scene)` (`unique_user_scene_read_status`), indexed on the pair.
The manager `UserSceneReadStatusManager` provides `record_post(scene, post, author)` and
`mark_read(scene, user_id, post=LATEST_POST, shown_from=None)`; both are described in
[scenes](scenes.md#read-markers).

## Weeks and weekly XP

### Week

| Field | Notes |
|-------|-------|
| `end_date` | Required date |
| `characters` | `ManyToManyField("characters.CharacterModel")`: characters enrolled by closed scenes |

- Ordered by `-end_date`.
- `start_date` (property) is `end_date - 7 days`. The week's range is `start_date`
  through `end_date`, both inclusive, so a Sunday belongs to two consecutive weeks.
- `finished_scenes()`: finished scenes whose latest post's date falls in that range.
- `weekly_characters()`: non-NPC `Human` characters in those scenes, ordered by name.
- `get_absolute_url()` → `game:week:detail`.

### WeeklyXPRequest

A player's weekly XP claim for one character and week.

| Field | Notes |
|-------|-------|
| `week`, `character` | `SET_NULL` foreign keys |
| `finishing` | Default `True` |
| `learning`, `rp`, `focus`, `standingout` | Criteria claimed |
| `learning_scene`, `rp_scene`, `focus_scene`, `standingout_scene` | The scene that earned each criterion (optional `Scene` links) |
| `approved` | Default `False` |

- `clean()` requires the matching scene for each claimed criterion.
- `total_xp()` is the number of true criteria, `finishing` included (0 to 5).
- `approve(xp_data=None)` is atomic: it locks the row, raises `ValueError` if the row
  was not saved or is already approved, applies any updated fields from `xp_data`, marks
  it approved and adds `total_xp()` to the character's `xp` under a row lock on the
  character. Returns the XP added.
- Indexed on `(character, week)` and `approved`. Unique on `(week, character)`
  (constraint `unique_weekly_xp_request`; `tg_schema` 0010 removed older duplicates).

## Spending records

Both models use `core.constants.XPApprovalStatus` for `approved`: `"Pending"` (default),
`"Approved"`, `"Denied"`. Both cascade-delete with their character.

### XPSpendingRequest

| Field | Notes |
|-------|-------|
| `character` | `ForeignKey(CharacterModel, CASCADE)`, related name `xp_spendings` |
| `trait_name`, `trait_type` | Display name and category of the trait |
| `trait_value` | The new rating |
| `cost` | XP cost, deducted when the request is filed |
| `approved`, `approved_at`, `approved_by` | Decision; `approved_by` related name `approved_xp_spendings` |
| `created_at` | `auto_now_add` |

Ordered by `-created_at`; indexed on `(character, approved)` and
`(character, -created_at)`. Rows are created by the character XP services in
[`characters/services/xp_spending/`](../../characters/services/xp_spending/)
(`XPSpendingService.spend`, which deducts the cost first) and decided through
`game.spending_approval.decide_spending_request`, which calls the same service's
`apply` or `deny`. See [XP](xp.md#xp-spending).

### FreebieSpendingRecord

Same shape for freebie points spent during character creation: `character` (related
name `freebie_spendings`), `trait_name`, `trait_type`, `trait_value`, `cost`,
`approved`, `approved_at`, `approved_by` (related name `approved_freebie_spendings`),
`created_at`.

## Journals

### Journal

One per character: `character` is a `OneToOneField(CharacterModel, CASCADE)`. The
`game.signals.create_journal_for_character` receiver creates it on the first save of
any `CharacterModel` subclass, and ignores the `IntegrityError` of a concurrent create.

- `owner` and `chronicle` properties return the character's, so permission checks can
  treat a journal like the character.
- `add_post(date, message)`: runs the message through `message_processing` (point
  spends and dice commands, as in scenes), converts `date` to an aware datetime and
  creates a `JournalEntry`. Returns `None` if the dice command is malformed.
- `all_entries()`, `get_absolute_url()` (`game:journal`).

### JournalEntry

`journal` (`SET_NULL`, related name `entries`), `message`, `st_message` (the
storyteller's answer; empty until answered), `date` (in-game date as a datetime),
`datetime_created`. Ordered by `-date`, `datetime_created`.

## Module-level functions

`game/models.py` also holds the dice-command engine used by scenes and journals:

| Function | Purpose |
|----------|---------|
| `process_message(character, message)` | Applies point tags and rolls a dice command inside one transaction; returns `(stored_text, roll_record or None)` or raises `ValueError` |
| `message_processing(character, message)` | `process_message(...)[0]` |
| `roll_record(kind, text, spent, *, pool, difficulty, specialty, results, **extra)` | Builds the `Post.roll` dict (`version` `ROLL_DATA_VERSION = 1`) |
| `roll_result(n, difficulty=6, specialty=False, willpower=False)` | One roll: `{"dice", "difficulty", "successes", "botch"}` using `core.utils.dice` |
| `rolls_results`, `extended_roll_results` | Repeated and extended rolls |
| `format_roll`, `format_rolls`, `format_extended_roll`, `roll_once`, `rolls`, `extended_roll` | The HTML text written into the message |
| `get_next_sunday(date)` | The Sunday on or after `date` |

The commands themselves are described in [scenes](scenes.md#dice-and-point-commands).

## See also

- [Scenes](scenes.md)
- [XP](xp.md)
- [Access and selectors](access-and-selectors.md)
- [Data model overview](../../docs/architecture/data-model.md)
- [Authorization](../../docs/architecture/authorization.md)
