# Read audiences and selectors

This page documents the two read-side modules of the `game` app:
[`game/security.py`](../security.py), which decides who may read chronicles, scenes and
private records, and [`game/selectors.py`](../selectors.py), which builds the data the
chronicle, week and scene pages show. Read it before writing a query that lists game
objects to a user, or before changing who can see them.

Neither module writes. Write permissions (approve, edit, spend) come from
`core.permissions.PermissionManager` and `game.spending_approval`; see
[authorization](../../docs/architecture/authorization.md) and [XP](xp.md).

## Read audiences (`security.py`)

These functions answer "may this user read it?" for lists and single objects. The
middleware, the views, the action views, the profile dashboard and the WebSocket
consumer all use them, so a rule changed here changes everywhere at once.

### Chronicles

| Function | Returns |
|----------|---------|
| `readable_chronicles(user)` | Chronicles the user may open: every chronicle for staff and superusers; otherwise those where the user is `head_st`, a game storyteller, has an `STRelationship`, or owns a character. Anonymous: none. |
| `staffed_chronicles(user)` | Chronicles where the user has a full storyteller read role: head ST, game storyteller or any `STRelationship`. Every chronicle for staff and superusers; none for anonymous users. |

`staffed_chronicles` is a read audience, not a write permission: a game storyteller is
included but cannot approve or edit. The `core` queryset helpers
`for_user_chronicles` and `pending_approval_for_user` build on it (and add objects with
no chronicle for staff).

### Scenes

`filter_scenes(queryset, user)` filters any `Scene` queryset by `Scene.visibility`;
`can_view_scene(user, scene)` runs the same filter for one scene.

| Visibility | Readers |
|------------|---------|
| `PUBLIC` | Everyone, including anonymous users |
| `CHRONICLE` | Signed-in users for whom the scene's chronicle is in `readable_chronicles` |
| `PARTICIPANTS` | Signed-in users whose `staffed_chronicles` include the scene's chronicle, or who own a character in the scene |

Staff and superusers see every scene. A `CHRONICLE` or `PARTICIPANTS` scene with no
chronicle is visible only to staff (and, for `PARTICIPANTS`, to owners of its
characters).

### Private records

Journals, journal entries and the XP and freebie records are private to the character's
owner and the character's storytellers.

| Function | Rule |
|----------|------|
| `can_read_private_record(user, record)` | `PermissionManager.user_has_permission(user, character, Permission.VIEW_FULL)`, where `character` is `record.character` or, for a journal entry, `record.journal.character`. `False` when there is no character. |
| `filter_private_records(queryset, user)` | For a queryset of models with a `character` foreign key: every row for staff and superusers; rows whose character the user owns or whose character's chronicle is in `staffed_chronicles(user)`; none for anonymous users. |

The two are close but not identical: `filter_private_records` admits any storyteller of
the chronicle (including game storytellers), while `can_read_private_record` follows
the permission matrix for the specific character.

### Where they are enforced

| Place | Uses |
|-------|------|
| `core.middleware.authorization.AuthorizationMiddleware._check_game_detail` | `readable_chronicles`, `can_view_scene`, `can_read_private_record` for `game.views` detail, update and approve URLs; answers `404` |
| `game.views` list views | `readable_chronicles`, `filter_scenes`, `filter_private_records` |
| `game.actions` | `can_view_scene`, `can_read_private_record`, `readable_chronicles` in `can_see` |
| `game.consumers.SceneChatConsumer` | `can_view_scene` on connect and on every event |
| `accounts.dashboard.ProfileDashboard` | `staffed_chronicles`, `filter_scenes`, `filter_private_records` |
| `accounts.views.MarkSceneReadView` | `can_view_scene` |

## Selectors (`selectors.py`)

### Chronicle page

`chronicle_overview(chronicle, user)` returns the dict that `ChronicleDetailView` merges
into its context:

| Key | Content |
|-----|---------|
| `character_list`, `retired_characters`, `deceased_characters`, `npc_characters` | Player characters by status and active NPCs of the chronicle, in group order, with owner and profile joined |
| `active_by_gameline`, `retired_by_gameline`, `deceased_by_gameline`, `npc_by_gameline` | The same grouped by gameline (`core.services.ChronicleDataService`) |
| `top_locations`, `locations_by_gameline` | Top-level locations of the chronicle |
| `items`, `items_by_gameline` | Items of the chronicle |
| `all_scenes_by_gameline`, `active_scenes_by_gameline`, `completed_scenes_by_gameline`, `active_scenes` | Scenes filtered by `filter_scenes`, newest first |
| `setting_elements_by_gameline` | The chronicle's common knowledge |

A user who does not staff the chronicle sees only their own characters and items and no
location tree. The tables show owners, statuses and relationships, and a location row
renders its children, so a filtered parent could still expose another player's child.
Public object cards elsewhere remain available to chronicle members.

### Weeks

- `count_dates_in_week(sorted_dates, end_date)`: how many dates fall between
  `end_date - 7 days` and `end_date`, both inclusive (the same span as
  `Week.start_date`), using `bisect`.
- `annotate_week_scene_counts(weeks, user)`: sets `week.cached_scene_count` on each
  week to the number of finished scenes the user may see whose latest post falls in
  that week. It runs one query for all weeks; `WeekListView` uses it.

### Scene posts

| Function | Returns |
|----------|---------|
| `scene_post_window(scene, *, before=None, limit=SCENE_POST_WINDOW)` | `(posts, has_earlier)`: the latest `limit` posts (100 by default), or the `limit` before post id `before`, oldest first |
| `scene_posts_after(scene, after, *, limit=...)` | `(posts, has_more)`: posts with id greater than `after`, oldest first; the socket's `sync` reply |
| `scene_post(scene, post_id)` | One post of the scene, or `None` |
| `scene_cast(scene)` | The scene's characters with owners joined, by name |
| `with_author_roles(scene, posts)` | Sets `author_is_st` on each post |
| `scene_storyteller_ids(scene, user_ids)` | The subset of `user_ids` who may manage the scene: staff, superusers, the chronicle's head ST, and users with an `STRelationship` for the scene's chronicle whose `Gameline.name` matches `settings.GAMELINES[scene.gameline]["name"]`. One query. |

Post windows order by `pk`, not `datetime_created`: ids follow creation order for posts
the app creates, and live clients compare ids. Every window passes through
`with_author_roles`, so templates can style storyteller posts without a query per post.

### Read markers

| Function | Returns |
|----------|---------|
| `scene_read_marker(scene, user)` | `(tracked, read, marker)` in one query: whether the user has a `UserSceneReadStatus` row, whether it is read, and the newest post id they have read |
| `unread_divider(scene, posts, *, read, marker, has_earlier)` | `{"post_id", "count"}` for the first unread post in `posts`, or `None`. With no marker and `read=True` (rows from before markers existed) nothing is unread. When every post in the window is unread and earlier posts exist, `count` is taken from the database. |

How the markers are written is described in [scenes](scenes.md#read-markers).

## Helpers in `views.py`

A few small read helpers live next to the views that use them:

- `can_create_scene(user, chronicle, request=None)`: head ST, staff or any
  `STRelationship` in the chronicle. Controls NEW SCENE and
  `ChronicleSceneCreateView`.
- `current_week(today=None)`: the `Week` whose span contains today (the first with
  `end_date` between today and today + 7 days).
- `readable_chronicle_ids(user, chronicles)`: the ids among `chronicles` the user can
  open, in one query; the story pages use it to name a chronicle only to its readers.

## See also

- [Authorization](../../docs/architecture/authorization.md)
- [Scenes](scenes.md)
- [game views and URLs](views-and-urls.md)
- [accounts dashboard](../../accounts/docs/dashboard.md)
- [`core/permissions.py`](../../core/permissions.py)
