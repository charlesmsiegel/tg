# Scenes

This page explains how scenes work inside the `game` app: who can see and change a
scene, how a post is created, the dice and point commands, the stored roll data behind
the roll strip, the post windows on the scene page, and the per-user read markers. It is
the app-level reference; the cross-app design (ASGI, channel layers, why events carry ids)
is in [scenes and real-time](../../docs/architecture/scenes-and-realtime.md), and the
WebSocket protocol is in [websockets](websockets.md).

## Lifecycle

1. **Create.** A storyteller opens a scene from the chronicle page
   (`game:chronicle_create_scene`, `actions.ChronicleSceneCreateView`) or from the
   standalone form (`game:scene_manage:create` or `create_for_chronicle`,
   `views.SceneCreateView`). Either way the caller must be able to manage the chosen
   gameline in that chronicle (`PermissionManager.can_manage_scope`).
   `Chronicle.add_scene` returns an existing scene with the same name and location
   instead of creating a duplicate.
2. **Cast.** Characters join through `game:scene_add_character`, or automatically when
   their owner posts as them.
3. **Play.** Players post as their characters (`game:scene_post` over HTTP, or the
   WebSocket). Posts may roll dice and spend points.
4. **Close.** A scoped storyteller posts to `game:scene_close`. `Scene.close()` marks
   the scene finished and enrolls its characters in the week ending on the Sunday on or
   after the latest post's date (see [XP](xp.md#weekly-xp)). The close is broadcast so
   open pages stop accepting posts.
5. **Award XP.** A storyteller awards scene XP from their profile
   (`accounts:scene_xp_award`); `Scene.award_xp` sets `xp_given`.

`views.SceneUpdateView` (`game:scene_manage:update`) edits name, location, date,
gameline, visibility, `finished` and `xp_given` directly. Setting `finished` there does
not run `Scene.close()`, so it neither enrolls characters in a week nor broadcasts.

## Who can do what

| Action | Rule | Where |
|--------|------|-------|
| Read a scene | `game.security.can_view_scene` (below) | `AuthorizationMiddleware` (404 when hidden), `SceneActionView.can_see`, the consumer |
| Post | Signed in, scene open, and the user owns a character in the scene (`scene_chat.can_post`) | `ScenePostView`, `SceneChatConsumer.submit` |
| Add a character | Can read the scene and the scene is open. The choices (`AddCharForm`) are the chronicle's characters not yet in the scene, limited to the user's own unless they can manage the scene's scope. | `SceneAddCharacterView` |
| Close | `PermissionManager.can_manage_scope(user, scene.chronicle, scene.gameline)` | `SceneCloseView` |
| Create | Chronicle page: head ST, staff, or any `STRelationship` in the chronicle may open the form; saving requires `can_manage_scope` for the chosen gameline | `ChronicleSceneCreateView`, `SceneCreateView` |
| Edit | `StorytellerRequiredMixin`, then `can_manage_scope` for the submitted gameline | `SceneUpdateView` |

### Visibility

`Scene.visibility` decides who may read a scene. `game.security.filter_scenes(queryset,
user)` applies it to any scene queryset and `can_view_scene(user, scene)` checks one:

| Visibility | Readers |
|------------|---------|
| `PUBLIC` | Everyone, including anonymous visitors |
| `CHRONICLE` (default) | Signed-in users who can read the chronicle: its head ST and game storytellers, anyone with an `STRelationship` in it, and owners of a character in it |
| `PARTICIPANTS` | Staff of the chronicle (`staffed_chronicles`) and owners of a character in the scene |

Staff and superusers read every scene. The scene list and detail pages are open to
anonymous GET requests at the route level so public scenes work without an account;
the middleware answers a plain `404` for a scene the caller may not read.

## Posting

There is one posting path. The HTTP action (`actions.ScenePostView`) and the WebSocket
consumer both call `scene_chat.can_post`, validate with `game.forms.PostForm` and save
with `scene_chat.create_post(scene, form)` inside a transaction.

`create_post`:

1. Picks the character: the user's only character in the scene, or the one chosen in
   the form (`PostForm` requires a choice when the user has more than one).
2. Straightens typographic quotes (`game.text.straighten_quotes`).
3. Calls `Scene.add_post(character, display_name, message)`.
4. On success, schedules a `scene.post` broadcast for after the commit and returns
   `ServiceResult.ok("Post added successfully!", obj=post)`.
5. Raises `core.actions.ActionFailed("Command does not match the expected format.")` for
   a malformed dice command; nothing is saved.

`Scene.add_post`:

- Adds the character to the scene if missing, and uses the character's name when the
  display name is empty.
- A message starting with `@storyteller` (any case) is not posted. It sets
  `waiting_for_st=True` and stores the rest of the message in `st_message`; the caller
  reports "Message sent to the storyteller." The scene then appears under "Scenes
  needing attention" on storytellers' profiles.
- A later post by a character whose owner can manage the scene's scope clears
  `waiting_for_st`.
- Runs `process_message` (below), creates the `Post` with its `roll` data, and calls
  `UserSceneReadStatus.objects.record_post`.

## Dice and point commands

`game.models.process_message(character, message)` handles both, inside one
transaction. The user-facing reference is the Commands page
(`game:commands`, template `game/scene/commands.html`).

### Point tags

Tags may appear anywhere in the message and stay in the stored text. They change the
character and save it once:

| Tag | Effect |
|-----|--------|
| `#WP` | Spend 1 temporary Willpower (not below 0); also adds one success to a `/roll` or `/stat` in the same message |
| `#WP<n>` | Spend `n` temporary Willpower; a negative `n` regains it; no extra success |
| `#Q<n>` | Subtract `n` from `quintessence`, if the character has it |
| `#P<n>` | Add `n` to `paradox`, if the character has it |
| `#<n>B`, `#<n>L`, `#<n>A` | Take `n` bashing, lethal or aggravated damage (`add_bashing`, `add_lethal`, `add_aggravated`) |

The spent tags are summarised (for example `#WP, #3L`) and written into the roll line.

### Dice commands

At most one command is used per message. The text before it becomes the post's prose.
Checked in this order:

| Command | Syntax | Result |
|---------|--------|--------|
| `/extended` | `/extended <dice> target <successes> [difficulty <d>] [True\|False]` | Rolls until the running total reaches the target, a roll botches, or 100 rolls |
| `/rolls` | `/rolls <n> rolls @ <dice> [difficulty <d>] [True\|False]` | `n` rolls; a roll with no successes raises the next roll's difficulty by 1; a botch stops the sequence |
| `/stat` | `/stat <Trait> + <Trait> [+ <number>] [difficulty <d> [True\|False]]` | Pool from the character's traits plus flat numbers. Each name is lowercased, spaces become underscores, and the result is read as an attribute of the character (`dexterity`, `firearms`, `arete`). An unknown name or a pool below 1 is an error. |
| `/roll` | `/roll <dice> [difficulty <d>] [True\|False]` | One roll |

Difficulty defaults to 6. The trailing `True` means a relevant specialty. A command that
does not match its pattern raises `ValueError`; the transaction rolls back any point
spends, so a refused message costs nothing.

Each roll is `roll_result(...)`: `{"dice": [...], "difficulty", "successes", "botch"}`,
built on `core.utils.dice`. A botch is a roll with no successes and at least one 1;
Willpower adds one success and so cancels a botch.

### Stored roll data and the roll strip

A command post stores two things:

- `Post.message`: the prose, the spent tags, a description and the formatted dice as
  HTML (for example `roll of 5 dice at difficulty 6: 3, 7, 9, 2, 10: <b>3</b>`).
- `Post.roll`: `roll_record(...)`, a dict with `version` (`ROLL_DATA_VERSION = 1`),
  `kind` (`roll`, `stat`, `rolls`, `extended`), `text`, `spent`, `pool`, `pool_label`,
  `difficulty`, `specialty`, `willpower`, `rolls`, `roll_count`, `successes`, `botch`,
  and per-kind extras (`target`, `max_rolls`, `complete`, `requested_rolls`).

`game.rolls.roll_strip(post.roll)` (exposed as `Post.roll_strip`) turns the dict into
the rows, label, pool, result and die faces that `game/scene/_post.html` draws. It
returns `None` for posts without roll data or with malformed data, and the template
then shows `message` instead. Keep both fields in step when changing a command.

## The scene page

`views.SceneDetailView` (`game:scene`, template `game/scene/detail.html`) renders:

- a window of the latest 100 posts (`selectors.SCENE_POST_WINDOW`) from
  `selectors.scene_post_window`, oldest first, with `author_is_st` set on each post;
- `?before=<post id>` for the 100 posts before that id. As a normal request this is a
  full page; as an htmx fragment request it returns `game/scene/_post_window.html`
  marked with the `TG-Fragment: scene-posts` header, which "Show earlier posts" swaps in
  place. Invalid cursors are ignored (`scene_chat.post_cursor`);
- `cast` (`selectors.scene_cast`), and for signed-in users on an open scene the
  characters they can post as (`post_characters`) and add (`add_characters`);
- `live`: true for an open scene on its latest window. The template then connects the
  htmx `ws` extension to `/ws/scene/<pk>/?v=2` (see [websockets](websockets.md)).

`author_is_st` comes from `selectors.with_author_roles`, which checks all post authors
in one query with `scene_storyteller_ids`: staff, superusers, the head ST, and users
with an `STRelationship` for the scene's chronicle and gameline. Storyteller posts get
the `tl-turn--st` style.

## Read markers

`UserSceneReadStatus` holds, per user and scene, `read` and `last_read_post`. The
dashboard's unread-scene count and the "New" divider on the scene page come from it.

### Writing

- `UserSceneReadStatusManager.record_post(scene, post, author)` runs for every new
  post. Every user who owns a character in the scene gets a row (created if missing).
  The author's row is marked read through `post`; every other participant's row is set
  unread.
- `mark_read(scene, user_id, post=LATEST_POST, shown_from=None)` moves one user's
  marker forward in a single `UPDATE`. It never moves back, sets `read` only if no newer
  post exists, and, with `shown_from`, skips the update when unread posts before
  `shown_from` have not been shown yet. `post=None` means an empty window was shown: the
  row becomes read only if the scene still has no posts.

### Who marks what read

| Trigger | Effect |
|---------|--------|
| Opening the scene's latest window (`SceneDetailView.read_latest`) | Marks read through the latest post, unless unread posts run back past the window; creates a row for a participant who has none |
| Loading earlier windows from the live page with `reading=1` (`read_back_to`) | Once the window reaches the first unread post, marks the scene read through its latest post |
| A live post delivered over the socket (`SceneChatConsumer.render_posts`) | `mark_read(..., posts[-1], shown_from=posts[0])` |
| "Mark read" on the profile (`accounts:mark_scene_read`) | Marks read through the latest post |

### The divider

`selectors.scene_read_marker(scene, user)` returns `(tracked, read, marker)` in one
query. `selectors.unread_divider(scene, posts, read=..., marker=..., has_earlier=...)`
returns `{"post_id", "count"}` for the first unread post in the window, or `None`.
`_post_window.html` draws the divider above that post.

## See also

- [Scenes and real-time](../../docs/architecture/scenes-and-realtime.md)
- [WebSockets](websockets.md)
- [game models](models.md#scenes)
- [Access and selectors](access-and-selectors.md)
- [game views and URLs](views-and-urls.md)
