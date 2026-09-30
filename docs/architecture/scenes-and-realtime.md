# Scenes and real-time updates

This page explains how play-by-post scenes work: the `Scene` and `Post` models, who can
see a scene, the single posting path, dice commands and the roll strip, unread tracking,
the post window, and the WebSocket layer that pushes new posts to open pages (with its
plain-HTTP fallback). It is for developers changing the scene page, the chat, or anything
that writes posts or read markers. Scene XP is covered in
[XP, freebies and approvals](xp-and-approvals.md#scene-xp).

## Models

All of these live in [`game/models.py`](../../game/models.py).

**`Scene`**: one session of play. Key fields: `name`, `chronicle`, `location`,
`characters` (many-to-many to `characters.CharacterModel`, reverse name `scenes`),
`visibility`, `finished`, `xp_given`, `waiting_for_st` and `st_message`, `date_of_scene`,
`gameline`. `Scene.objects` is built from `SceneQuerySet`, which adds `active()`,
`finished()`, `awaiting_xp()`, `waiting_for_st()`, `for_chronicle()`,
`for_user_chronicles(user)` and similar filters.

**`Post`**: one message. Fields: `scene`, `character` (null for a post without a
character), `display_name`, `message`, `datetime_created`, and `roll` (a JSON copy of a
dice command's outcome, null for other posts). Posts are ordered by `datetime_created`, but
the code that pages and compares posts orders by primary key, because ids follow creation
order for every post the app writes and are what live clients compare.
`Post.objects.for_scene_optimized(scene)` joins the character and its owner.

**`UserSceneReadStatus`**: one row per user and scene, enforced by the unique constraint
`unique_user_scene_read_status` on `(user, scene)`. Fields: `read` (boolean) and
`last_read_post` (the newest post the user has seen, null for rows that predate markers).
The manager `UserSceneReadStatusManager` owns all writes; see
[Unread tracking](#unread-tracking).

### Scene lifecycle

- A storyteller creates a scene (`SceneCreateView` under `game:scene_manage:`, or
  `ChronicleSceneCreateView` from a chronicle page).
- Characters join through `SceneAddCharacterView` (`POST game:scene_add_character`); a
  character is also added automatically the first time it posts.
- `SceneCloseView` (`POST game:scene_close`) requires
  `PermissionManager.can_manage_scope(user, scene.chronicle, scene.gameline)`, locks the
  scene and calls `Scene.close()`. That sets `finished`, adds the scene's characters to the
  `Week` ending on the Sunday after the last post, and saves. A closed scene is read-only:
  every other scene action refuses it.

## Visibility

`Scene.visibility` is one of `Scene.Visibility`:

| Value | Who can read |
|-------|--------------|
| `PUBLIC` | Everyone, including anonymous visitors |
| `CHRONICLE` (default) | Signed-in users who can read the chronicle (`readable_chronicles`: head ST, game storytellers, ST relationships, and anyone owning a character in it) |
| `PARTICIPANTS` | Storytellers of the chronicle (`staffed_chronicles`) and owners of a character in the scene |

Staff and superusers read every scene. The rules live in
[`game/security.py`](../../game/security.py): `filter_scenes(queryset, user)` filters any
scene queryset and `can_view_scene(user, scene)` checks one scene with the same query.
`core.middleware.authorization.AuthorizationMiddleware` answers a plain 404 for any
`pk`-routed scene URL the user cannot read, so a hidden scene is indistinguishable from a
missing one. Scene lists, the dashboard and the WebSocket consumer all go through
`filter_scenes` / `can_view_scene`.

## Posting

[`game/scene_chat.py`](../../game/scene_chat.py) is the one posting path. The WebSocket
consumer and the HTTP fallback both use it:

1. **Authorize** with `can_post(user, scene)`: the user is signed in, the scene is not
   finished, and the user owns at least one character in the scene.
2. **Validate** with `game.forms.PostForm(data, user=, scene=)`. Its character choices are
   the user's characters in the scene and chronicle (`character_queryset`); a character
   must be chosen only when there is more than one; the message cannot be blank.
3. **Persist** with `create_post(scene, form)` inside the caller's transaction. It picks
   the character, straightens typographic quotes (`game.text.straighten_quotes`) and calls
   `Scene.add_post(character, display_name, message)`.

`Scene.add_post()`:

- adds the character to the scene if needed and defaults `display_name` to its name;
- treats a message starting with `@storyteller` as a note to the storytellers: it sets
  `waiting_for_st` and `st_message`, creates **no** post and returns `None` (the scene then
  appears under "Scenes Needing Attention" on storytellers' dashboards);
- clears `waiting_for_st` when a character owned by a storyteller of the scene's chronicle
  and gameline posts;
- runs `process_message()` (point spends and dice, below); a malformed dice command
  returns `None` without posting;
- creates the `Post` and calls `UserSceneReadStatus.objects.record_post()`.

`create_post()` turns the `None` results apart: a storyteller note succeeds with "Message
sent to the storyteller."; anything else raises `ActionFailed("Command does not match the
expected format.")`. On success it calls `broadcast(scene.pk, POST_CREATED,
post_id=post.pk)`.

## Dice commands and the roll strip

`process_message(character, message)` in `game/models.py` runs inside a transaction and
returns `(text_to_store, roll_data)`. If the dice command is malformed it raises
`ValueError`, and the point spends it had already saved are rolled back, so a refused
message costs nothing.

**Point spends** anywhere in the message change the character before the roll:

| Token | Effect |
|-------|--------|
| `#WP` | Spend 1 temporary Willpower; a `/roll` or `/stat` in the same message gets one automatic success |
| `#WP<n>` | Spend `n` temporary Willpower (no automatic success) |
| `#Q<n>` | Spend `n` Quintessence (characters that have it) |
| `#P<n>` | Gain `n` Paradox (characters that have it) |
| `#<n>B`, `#<n>L`, `#<n>A` | Take `n` bashing, lethal or aggravated damage |

**Dice commands** (checked in this order; the text before the command is kept as prose):

| Command | Meaning |
|---------|---------|
| `/extended <dice> target <successes> [difficulty <d>] [true]` | Roll until the successes reach the target, a roll botches, or 100 rolls (`EXTENDED_MAX_ROLLS`) |
| `/rolls <n> rolls @ <dice> [difficulty <d>] [true]` | `n` rolls; a roll with no successes raises the next roll's difficulty by one, a botch ends the series |
| `/stat <Trait> + <Trait> [+ <n>] [difficulty <d> [true]]` | Dice pool from the character's ratings (for example `Dexterity + Firearms`); an unknown trait or an empty pool is an error |
| `/roll <dice> [difficulty <d>] [true]` | A single roll |

Difficulty defaults to 6. A trailing `true` marks a relevant specialty, which makes each 10
count one extra success. Dice come from `core.utils.dice()`: each die at or above the
difficulty is a success, each 1 cancels one, and a roll with no successes and at least one
1 is a botch. The Commands page (`game:commands`, template
`game/scene/commands.html`) documents these for players.

The stored `message` keeps the roll written out as text, as it always has. The
structured outcome goes into `Post.roll` via `roll_record()` (versioned by
`ROLL_DATA_VERSION`): `kind` (`roll`, `stat`, `rolls`, `extended`), prose `text`,
`spent`, `pool`, `difficulty`, `specialty`, `willpower`, the per-roll `rolls` (dice,
difficulty, successes, botch) and totals.

`Post.roll_strip` (a cached property) passes that data to
[`game/rolls.py`](../../game/rolls.py) `roll_strip()`, which returns the rows, label, pool,
per-die tiles (hit, one) and result that `game/scene/_post.html` draws as the roll strip.
It returns `None` for a post without roll data or with data it cannot read, and the
template then shows the message text instead.

## Unread tracking

Unread state is per user and scene, in `UserSceneReadStatus`. Every write goes through two
manager methods.

### `record_post(scene, post, author)`

Called for each new post. Every user who owns a character in the scene gets a row (rows
are bulk-created with `ignore_conflicts=True`, so a concurrent post cannot duplicate one).
The author (the post character's owner, if they have a character in the scene) is marked
read through the new post; every other participant's row is set `read=False`.

### `mark_read(scene, user_id, post=LATEST_POST, shown_from=None)`

Records that the user has read the scene through `post`. It updates existing rows only, in
a single `UPDATE`, and returns the number of rows changed.

- `post=LATEST_POST` (the default, a sentinel object) means the scene's newest post,
  looked up at update time.
- `post=None` means an empty window was shown: the row becomes read only if the scene
  still has no posts, so a first post that arrived meanwhile stays unread.
- The marker never moves backwards: the new `last_read_post` is the greater of the stored
  marker and `post`. A row already read through `post` or later is not written.
- `read` becomes true only if no post is newer than the new marker, checked in the same
  statement. A post that landed after the page was rendered, and was never shown, keeps
  the scene unread.
- `shown_from` (the first of the posts just shown, used for live delivery) moves the row
  only if no unread post precedes `shown_from`. A backlog the reader has not loaded yet
  therefore keeps its marker.

### Where markers move

| Caller | Call |
|--------|------|
| Scene page, latest window (`SceneDetailView.read_latest`) | If unread posts reach back past the window, nothing is written and the divider stays. Otherwise a tracked reader is marked read through the latest shown post (only when that changes the row); a participant without a row gets one, created read. Readers who have never had a character in the scene are not tracked. |
| "Show earlier posts" fragment with `reading=1` (`SceneDetailView.read_back_to`) | Once the loaded window reaches the reader's first unread post, `mark_read(scene, user)` marks the scene read through its latest post. |
| WebSocket delivery (`SceneChatConsumer.render_posts`) | `mark_read(scene, viewer, posts[-1], shown_from=posts[0])` for every post sent to a signed-in viewer. |
| Dashboard "mark read" (`accounts:mark_scene_read`, `MarkSceneReadView`) | Creates the row if missing, then `mark_read(scene, user)`. |
| New post (`Scene.add_post`) | `record_post()`, which calls `mark_read` for the author. |

### Selectors

[`game/selectors.py`](../../game/selectors.py) holds the read side (selectors never write):

- `scene_read_marker(scene, user)` returns `(tracked, read, marker)` in one query.
- `unread_divider(scene, posts, read=, marker=, has_earlier=)` returns
  `{"post_id", "count"}` for the "New" divider above the first post after the marker, or
  `None`. Without a marker, every post counts as new unless the row says the scene is read.
  When the whole window is new and earlier posts exist, the count comes from the database.
- `ProfileDashboard.unread_scenes()` lists scenes whose row for the user is unread, filtered
  through `filter_scenes`.

## The post window

A scene page never loads every post. `scene_post_window(scene, before=None, limit=100)`
(`SCENE_POST_WINDOW`) returns the latest 100 posts, or the 100 before post id `before`,
oldest first, plus a `has_earlier` flag. `with_author_roles()` sets `post.author_is_st` on
each post in one query (`scene_storyteller_ids`: staff, superusers, the chronicle's head
ST, and users with an `STRelationship` for the chronicle and the scene's gameline), which
the template uses to mark storyteller posts.

`SceneDetailView` (`game:scene`, `/game/scene/<pk>/`, template `game/scene/detail.html`):

- `?before=<post id>` pages back. The cursor is parsed by `scene_chat.post_cursor()`,
  which accepts only ASCII digits within the 64-bit id range and ignores anything else.
- The window renders through `game/scene/_post_window.html`: a "↑ Show earlier posts"
  link when `has_earlier`, then the posts, with the unread divider on the latest window.
- The link is a normal `href` to `?before=<id>`, so without JavaScript it opens the older
  window as a full page (with a "Back to the latest posts" link and no live updates). With
  htmx it carries `hx-get` (plus `&reading=1` when the chain started on the live page) and
  swaps itself for the returned fragment. The view answers such requests with only
  `_post_window.html` and the `TG-Fragment: scene-posts` header; `scene-chat.js` loads
  the URL as a full page if any other response arrives (an expired session, an error).
- A page is **live** only when the scene is open and no `before` cursor is set.

## Real-time updates

### Wiring

| Piece | Source |
|-------|--------|
| ASGI entry point | [`tg/asgi.py`](../../tg/asgi.py): HTTP goes to Django; WebSocket goes through `AllowedHostsOriginValidator` and `AuthMiddlewareStack` (session user in `scope["user"]`) to `game.routing.websocket_urlpatterns` |
| Route | [`game/routing.py`](../../game/routing.py): `ws/scene/<scene_id>/` -> `SceneChatConsumer` |
| Consumer | [`game/consumers.py`](../../game/consumers.py) `SceneChatConsumer` (an `AsyncWebsocketConsumer`) |
| Broadcasts | `game.scene_chat.broadcast()` |
| Client | htmx with the `ws` extension, loaded by `core/includes/interactive_scripts.html` with `ws=True` on a live page, and [`game/static/game/js/scene-chat.js`](../../game/static/game/js/scene-chat.js) |

On a live page the `#scene-live` element carries `hx-ext="ws"` and
`ws-connect="/ws/scene/<pk>/?v=2"`, and the post form carries `ws-send` with
`hx-vals='{"action": "post"}'`.

### Connecting

`connect()` accepts and immediately closes a connection it refuses, because a refused
handshake reaches the browser as code 1006, which the ws extension retries forever:

| Close code | When |
|------------|------|
| `4400` (`CLOSE_OUTDATED`) | The query string is not `v=2` (a page from an older protocol) |
| `4403` (`CLOSE_DENIED`) | The scene is missing or the viewer cannot read it (`can_view_scene`); also sent later if the viewer loses access |
| `1000` (`CLOSE_NORMAL`) | After the scene closes |

Otherwise the connection joins the channel group `scene_<id>` (`scene_chat.group_name`).
Public scenes admit anonymous viewers.

### Messages from the client

The client sends JSON text frames; binary frames, invalid JSON and frames larger than
`DATA_UPLOAD_MAX_MEMORY_SIZE` are answered with an error notice.

- `{"action": "post", "character": ..., "display_name": ..., "message": ...}` runs the same
  checks as the HTTP view (`can_post`, `PostForm`, `create_post` in a transaction). The
  reply is a fresh message-field region and a notice; the post itself arrives through its
  broadcast, like everyone else's.
- `{"action": "sync", "after": <post id>}` (a JSON number) returns the posts after that id.
  `scene-chat.js` sends it on every (re)connect with the highest post id on the page, so
  posts made while the socket was down are filled in. If more than 100 posts were missed
  the reply is a notice with a reload link instead.

### Group events carry ids, not markup

`broadcast(scene_id, event_type, **data)` sends an event to the scene's group with
`transaction.on_commit(...)`, so nobody renders a row that may still roll back. A
channel-layer failure is caught and logged on `game.scene_chat` without failing the change. The events are:

| Event type | Data | Sent by | Consumer handler |
|------------|------|---------|------------------|
| `scene.post` (`POST_CREATED`) | `post_id` | `create_post` | `scene_post` |
| `scene.characters` (`CHARACTER_JOINED`) | `character_id` | `SceneAddCharacterView` | `scene_characters` |
| `scene.closed` (`SCENE_CLOSED`) | none | `SceneCloseView` | `scene_closed` |

Each connection re-reads the scene and re-checks `can_view_scene` for its own viewer on
every event, then renders the HTML for that viewer: `game/scene/ws/_posts.html` (the new
posts, appended out of band to `#posts-container`, rendered with the viewer's id so "you"
markers are right), `_cast.html` and the viewer's own form fields for a join, and
`ws/_closed.html` plus a notice for a close. Because the event holds only ids, one viewer's
rendering never reaches another connection, and a viewer who has lost access is
disconnected with 4403 instead of receiving the post.

`_post.html` never reads `request`, so the page and the consumer render identical markup.

### Client behaviour

`scene-chat.js` does only what the server cannot:

- shows the connection state (`#connection-status`) and the message for the close codes
  above;
- drops a post already on the page (a sync reply and a broadcast can carry the same post)
  and inserts posts in id order;
- folds consecutive posts by the same speaker into one turn, scrolls to the newest post or
  to the unread divider, and sends on Enter (Shift+Enter for a new line).

### HTTP fallback

The post form is a normal form: `action` is `game:scene_post`
(`/game/scene/<pk>/posts/`), handled by `game.actions.ScenePostView`, an
`ObjectActionView` using the same `can_post`, `PostForm` and `create_post`. It flashes the
result and redirects to the scene. The page falls back to it when:

- JavaScript is off (no socket at all; the page reloads after each post);
- the socket is down: `scene-chat.js` cancels the ws send and submits the form over HTTP;
- the scene page is not live (an older window, a finished scene).

## Local and production

The channel layer is configured by `CHANNEL_LAYERS`:

- [`tg/settings/base.py`](../../tg/settings/base.py) uses
  `channels.layers.InMemoryChannelLayer`. It works inside a single process only, which is
  enough for `python manage.py runserver`: `daphne` is listed first in `INSTALLED_APPS`, so
  `runserver` serves the ASGI application, WebSockets included.
- [`tg/settings/production.py`](../../tg/settings/production.py) uses
  `channels_redis.core.RedisChannelLayer` with `REDIS_URL` (default
  `redis://127.0.0.1:6379/0`), so broadcasts reach connections in every worker process.

With more than one process and the in-memory layer, a post only reaches viewers connected
to the same process; the others still see it on their next sync or reload. See
[Deployment](../operations/deployment.md) for running the ASGI server and
[Configuration](../getting-started/configuration.md) for `REDIS_URL`.

## See also

- [XP, freebies and approvals](xp-and-approvals.md)
- [Authorization](authorization.md)
- [Front end](frontend.md)
- [`game` app](../../game/README.md)
- [Deployment](../operations/deployment.md)
