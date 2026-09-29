# Live scene WebSocket

This page is the reference for the live scene chat: the WebSocket endpoint, the
message protocol between the browser and `game.consumers.SceneChatConsumer`, the group
events that scene actions broadcast, and the client script that drives the page. Read
it before changing the consumer, `game/scene_chat.py`, the scene templates the socket
swaps, or `scene-chat.js`. The architecture (ASGI server, channel layers, deployment
constraints) is in [scenes and real-time](../../docs/architecture/scenes-and-realtime.md).

## Stack

| Layer | Where | What it does |
|-------|-------|--------------|
| ASGI application | [`tg/asgi.py`](../../tg/asgi.py) (`ASGI_APPLICATION = "tg.asgi.application"`) | `ProtocolTypeRouter`: HTTP to Django, WebSocket to `AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(game.routing.websocket_urlpatterns)))` |
| Routing | [`game/routing.py`](../routing.py) | `ws/scene/(?P<scene_id>\d+)/$` → `SceneChatConsumer.as_asgi()` |
| Consumer | [`game/consumers.py`](../consumers.py) | `SceneChatConsumer(AsyncWebsocketConsumer)` |
| Posting and events | [`game/scene_chat.py`](../scene_chat.py) | `can_post`, `create_post`, `broadcast`, `group_name`, `post_cursor` |
| Channel layer | `CHANNEL_LAYERS` in `tg/settings/base.py` and `production.py` | `InMemoryChannelLayer` by default; `channels_redis.core.RedisChannelLayer` on `REDIS_URL` in production |
| Client | `htmx` with the `ws` extension, and [`game/static/game/js/scene-chat.js`](../static/game/js/scene-chat.js) | Connects, sends posts, swaps the server's HTML |

`AuthMiddlewareStack` puts the session user in `scope["user"]`; the origin validator
refuses connections from hosts outside `ALLOWED_HOSTS`. The in-memory layer only
delivers events within one process, so a multi-process deployment needs Redis.

## Connecting

The scene page (`game/scene/detail.html`) sets `live` when the scene is open and the
latest window is shown. It then loads the `ws` extension and connects:

```html
<div id="scene-live" data-scene-live hx-ext="ws"
     ws-connect="/ws/scene/{{ object.pk }}/?v=2" data-ws-state="connecting">
```

`SceneChatConsumer.connect()`:

1. Reads `scene_id` from the URL and joins nothing yet.
2. If the query string is not `v=2` (`PROTOCOL`), accepts and closes with `4400`.
   This ends retries from a tab loaded before the current protocol.
3. If the scene does not exist or `can_view_scene(user, scene)` is false, accepts and
   closes with `4403`. Missing and hidden scenes are refused alike. Anonymous users
   can connect to `PUBLIC` scenes.
4. Otherwise adds the channel to the group `scene_<id>` (`scene_chat.group_name`) and
   accepts.

The consumer accepts before closing on purpose: a refused handshake reaches the browser
as `1006`, which the `ws` extension retries; a close code of the server's own is not
retried.

| Close code | Constant | Meaning | Client text |
|------------|----------|---------|-------------|
| `1000` | `CLOSE_NORMAL` | The scene was closed | "Live updates have ended." |
| `4400` | `CLOSE_OUTDATED` | Wrong protocol version | "This page is out of date. Reload it to keep chatting." |
| `4403` | `CLOSE_DENIED` | The viewer cannot read the scene (on connect or later) | "Live updates are unavailable. Reload the page." |

## Client messages

The client sends JSON text frames. The consumer rejects binary frames, frames larger
than `DATA_UPLOAD_MAX_MEMORY_SIZE` (5 MB in `tg/settings/base.py`), invalid JSON and
non-object JSON with an error notice.

### `post`

Sent by the composer form (`<form id="post-form" ws-send hx-vals='{"action":
"post"}'>`), so the frame carries the form fields:

```json
{"action": "post", "character": "12", "display_name": "", "message": "Hello /roll 5"}
```

Only string values of `character`, `display_name` and `message` are read.
`SceneChatConsumer.submit` then follows the same path as the HTTP action
`game:scene_post`:

1. Refuses a finished scene ("This scene is closed.") and a user who fails
   `scene_chat.can_post` ("You can only post as your own characters in this scene.").
2. Validates `game.forms.PostForm(data=fields, user=user, scene=scene)`.
3. Calls `scene_chat.create_post(scene, form)` in a transaction.

The reply to the sender is:

- on success, a fresh `_post_message_fields.html` (clearing the text box) plus an
  empty or informational notice. The post itself reaches the sender, like everyone
  else, through the `scene.post` broadcast. A `@storyteller` message has no post, so
  the notice says "Message sent to the storyteller.";
- on failure, an error notice only, so the typed text stays in the box.

`scene-chat.js` removes `csrfmiddlewaretoken` from the frame; the token exists for the
HTTP fallback.

### `sync`

Sent by `scene-chat.js` on every (re)connect with the highest post id on the page:

```json
{"action": "sync", "after": 431}
```

`after` must be a JSON number (a string is an error). The consumer replies with the
posts after that id (`selectors.scene_posts_after`, up to 100). If more than 100 were
missed, it sends an informational notice with a "Reload the scene" link instead.

Any other `action` gets "Unknown action.". An unexpected exception is logged and
answered with "Could not process message.".

## Group events

Actions announce committed changes with `scene_chat.broadcast(scene_id, event_type,
**data)`. It registers a `transaction.on_commit(..., robust=True)` callback that calls
`group_send` on the channel layer, so no event describes a row that may still roll back,
and a channel-layer failure is logged without failing the action.

Events carry ids, never markup. Each consumer re-checks its own viewer with
`visible_scene()` (`can_view_scene`) and renders the event for that viewer, so a
rendering meant for one user never reaches another connection, and a viewer who has
lost access is closed with `4403`.

| Event type | Sent by | Data | Consumer method | Sends |
|------------|---------|------|-----------------|-------|
| `scene.post` | `scene_chat.create_post` (HTTP and socket posts) | `post_id` | `scene_post` | `ws/_posts.html` with the post, appended to `#posts-container` |
| `scene.characters` | `actions.SceneAddCharacterView` | `character_id` | `scene_characters` | A "<name> joined the scene." notice and the refreshed `_cast.html`; for signed-in viewers of an open scene, the refreshed add-character select and, for the character's owner, the post-as select |
| `scene.closed` | `actions.SceneCloseView` | none | `scene_closed` | `ws/_closed.html` (replaces the composer, clears the cover actions, sets the badge to "Closed") and a notice, then closes with `1000` |

Channels maps a type such as `scene.post` to the method `scene_post`.

### Read markers on delivery

`render_posts` (used by `scene.post` and `sync`) calls
`UserSceneReadStatus.objects.mark_read(scene, viewer_id, posts[-1],
shown_from=posts[0])` for a signed-in viewer. The marker moves to the newest delivered
post unless unread posts before the delivered ones have not been loaded on the page.
See [scenes](scenes.md#read-markers).

## Server-rendered fragments

Every reply is HTML whose top-level elements carry `hx-swap-oob`, which the `ws`
extension swaps into the page by id. Keep these ids stable (the comment at the top of
`detail.html` lists them):

| Template | Target |
|----------|--------|
| `game/scene/ws/_posts.html` | `beforeend:#posts-container` |
| `game/scene/ws/_notice.html` | `#scene-chat-notice` (inner HTML; empty clears it) |
| `game/scene/ws/_closed.html` | `#scene-actions`, `#scene-cover-actions`, `#scene-live-badge` |
| `game/scene/_post_message_fields.html` | `#post-message-fields` |
| `game/scene/_cast.html` | `#scene-cast` |
| `game/scene/_post_character_field.html`, `_add_character_field.html` | The post-as and add-character selects |

The same partials render the full page, so a live update and a reload show the same
markup.

## The client script

`scene-chat.js` is loaded on the scene page through `component_scripts` and never builds
markup. It:

- shows the connection state in `#connection-status` from the `htmx:wsConnecting`,
  `wsOpen` and `wsClose` events, using the close-code texts above;
- sends `sync` on every `htmx:wsOpen`;
- posts the form over plain HTTP (`form.submit()` to `game:scene_post`) while the socket
  is down, instead of queueing the message;
- disables the Post button until the reply containing the notice region arrives;
- drops a post that is already on the page and inserts out-of-order posts by id
  (`htmx:oobBeforeSwap`), since a `sync` reply and a broadcast can carry the same post;
- groups consecutive posts by the same speaker into one turn (`is-cont`) after each
  swap, restarting at the unread divider;
- scrolls to the newest post or the unread divider on load;
- loads "Show earlier posts" in place only if the response has
  `TG-Fragment: scene-posts`, and otherwise navigates to the link;
- submits on Enter (Shift+Enter inserts a newline).

## Testing

| Path | Covers |
|------|--------|
| `game/tests/consumers/test_scene_chat_socket.py` | Connect and close codes, posting, `sync`, group events |
| `game/tests/consumers/test_consumers.py` | Socket authorization and quote straightening |
| `game/tests/consumers/test_scene_socket_rolls_and_reads.py` | Roll strips and read markers over the socket |
| `game/tests/test_scene_chat.py` | `scene_chat`, post windows, broadcasts from the HTTP actions, the live page |
| `game/tests/browser/test_scene_chat.py` | A real browser against Daphne in a child process; skipped without the `playwright` package or a Chromium binary |

## See also

- [Scenes and real-time](../../docs/architecture/scenes-and-realtime.md)
- [Scenes](scenes.md)
- [game templates](templates.md)
- [Access and selectors](access-and-selectors.md)
- [Deployment](../../docs/operations/deployment.md)
