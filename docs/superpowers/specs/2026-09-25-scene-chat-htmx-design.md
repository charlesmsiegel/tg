# Server-rendered live scene chat with htmx over Channels

## Intent and scope

Step 11 rewrites the play-by-post scene chat so that a post's markup exists in
one template, rendered on the server for the first page load and for every live
update, and pushed to browsers as HTML over the existing Django Channels
WebSocket. The browser uses htmx 2 and its `ws` extension, vendored as static
files; there is no React, Vite, npm or build step. The user asked for the plan
to be implemented, which supersedes the brief's design-only restriction, as in
Steps 2, 3, 4, 9 and 10.

In scope: `game/consumers.py`, the scene page (`game/scene/detail.html` and new
partials), the three scene action endpoints from Step 5 where they must share
the posting path or announce changes, one new service module, one selector,
the vendored extension and its tests. Out of scope: other game views, chargen,
and Channels infrastructure (Redis configuration, ASGI deployment).

## Upstream designs this builds on

All upstream designs exist and are implemented on `main`:

| Step | What this design reuses |
|---|---|
| 0 Authorization | The three-state scene read rule (`game.security.can_view_scene`, `filter_scenes`): `PUBLIC` grants read only, never posting; a hidden scene is indistinguishable from a missing one. Scene mutation needs `PermissionManager.can_manage_scope(user, chronicle, gameline)` for STs, and a player's post must use their own character that belongs to the scene and its chronicle. No global ST exceptions; `Profile.is_st()` is for dashboards only. |
| 4 Rules out of views | `game.text.straighten_quotes` (one implementation; the `SceneDetailView`/`SceneChatConsumer` aliases stay because tests pin them). |
| 5 Action endpoints | `SceneCloseView` (G1), `SceneAddCharacterView` (G2) and `ScenePostView` (G3) in `game/actions.py`, each one URL, one permission and one service call inside `ObjectActionView`'s transaction. `ScenePostView` is the chat's no-socket fallback. |
| 8 Template consolidation | `PostManager.for_scene_optimized()` and the scene query budget test (`core/tests/test_query_budgets.py`). Step 8 recorded that the page styles "author is an ST anywhere" while the consumer styles "author manages this scene's scope", and left the choice to this step. |
| 9 Static JS | Scripts are static files; configuration travels as `data-*`; the inline-script inventory test allows exactly one executable inline script, the scene page's, and this step removes that exception. |
| 10 htmx pilot | Vendoring layout and SRI checks (`source_static/vendor/`, `VENDOR.md`, `core.tests.test_htmx`), the `interactive_scripts.html` include and its htmx config (`allowEval: false`, `includeIndicatorStyles: false`, `selfRequestsOnly: true`), `core.htmx` helpers (`is_fragment_request`, `mark_fragment`, `vary_on_htmx`), the `TG-Fragment` header, and the rule of no inline scripts, no `hx-on`, no eval. Step 10 flagged ordering and reconnection as the parts of a live stream that request/response htmx does not solve; §4 handles them. |

## Audit status of the brief's findings

Every item was re-checked on this branch (after Steps 0-10). The audit's line
numbers predate Steps 4, 5 and 8, which already fixed several findings.

| Finding | Status |
|---|---|
| Consumer `connect`, `receive` (JSON), `handle_chat_message`, `handle_add_character`, `chat_message_broadcast`, `character_added_broadcast`, `send_error` all `json.dumps`; `serialize_post` builds the post JSON | **Confirmed** (292 lines now). |
| Consumer has its own `straighten_quotes`, views another | **Refuted as current:** Step 4 moved the single implementation to `game/text.py`; both classes keep an alias. |
| `user_owns_character`/`character_in_scene` authorize inside the consumer | **Confirmed.** Checked against Step 0 below: the socket path is weaker than the HTTP path in three ways (see "New findings"). |
| Initial posts render from `object.post_set.all` and ignore `context["posts"]` | **Refuted as current:** Step 8 changed the loop to `{% for post in posts %}` over `for_scene_optimized()`. |
| 329-line inline `<script>` builds post DOM in `appendPost`, duplicating the template | **Confirmed:** lines 125-454 (330 lines); `appendPost` rebuilds the markup of lines 49-55 by hand. |
| Each post reads `post.character.owner.profile.is_st` (N+1) | **Refuted as current:** Step 8 replaced it with the `author_is_st` `Exists()` annotation. The semantic disagreement with the consumer remains (**confirmed**) and is decided in §1. |
| `SceneDetailView.post` handles `close_scene`, `character_to_add`, `message` | **Refuted as current:** Step 5 deleted it; the branches are `SceneCloseView`, `SceneAddCharacterView`, `ScenePostView`. |
| The storyteller check is inline and differs from the rest of the file | **Refuted as current:** `SceneCloseView.has_permission` uses `can_manage_scope`. |
| `character_to_add` doesn't verify the chronicle | **Refuted as current** for HTTP: `AddCharForm` filters `chronicle=scene.chronicle`. The socket's `add_character` checks it too (Step 0 test `test_character_from_other_chronicle_cannot_join`). |

**New findings (all confirmed by reading and by a failing test before the fix):**

1. **HTTP posts are never broadcast.** `ScenePostView` saves the post and
   redirects; other open tabs only see it on reload. The same holds for
   characters added and for closing the scene.
2. **Malformed dice commands are misreported.** `Scene.add_post` returns `None`
   both for `@storyteller` messages and when `message_processing` raises
   `ValueError`. The consumer tells the sender "Message sent to storyteller" for
   a bad `/extended` command; the HTTP path flashes "Post added successfully!".
   In both cases nothing was posted.
3. **The client clears the message 100 ms after sending, whatever the outcome.**
   A rejected post (error reply) loses the player's text.
4. **The socket's `add_character` is dead and weaker than `AddCharForm`.** The
   page never sends it (the add form is a normal POST), and it lets a player
   re-add a present character and never lets an ST add a player's character.
5. **Posts made between the page render and the socket opening are lost** until
   reload, and so are posts made while the socket is reconnecting.
6. **The socket path accepts unbounded `display_name`**; `Post.display_name` is
   `max_length=100`. `PostForm` enforces that on HTTP; the socket bypasses the
   form, so on PostgreSQL a long name raises inside `create_post` (reported to
   the user as a generic error), and on SQLite it is stored untruncated.
7. **Anonymous readers of a `PUBLIC` scene get no live updates**: the inline
   script opens the socket only when `CURRENT_USER_ID` is set, although the
   consumer admits them.

## Decisions

| Question | Decision | Why |
|---|---|---|
| Viewer-specific markup | **Render per recipient.** The group event carries ids, not HTML; each connection's handler (which already re-checks the recipient's read access on every event) loads the post and renders the partial with its own `viewer_id`. | The only per-viewer post markup today is "your character" (`highlight`), but the page also has per-viewer controls (the character select, the add-character options). Rendering per recipient keeps one template with the same inputs as the page render, never sends one user's markup to another (a future ST-only control cannot leak by being "hidden with CSS"), and needs no client code for styling. Cost: one indexed query and one small render per recipient per post; scenes have a handful of viewers. Per-user groups were rejected: a user with two tabs is two connections anyway, and the per-connection handler already exists. |
| ST styling of a post | **"The author can manage this scene's scope"** (`can_manage_scope(owner, scene.chronicle, scene.gameline)`), computed for all authors of a page of posts in one query by `game.selectors.scene_storyteller_ids`. | Step 0 removed global ST semantics from everything but dashboards, and `Scene.add_post` already uses the scoped rule to clear `waiting_for_st`. The consumer already used it; now the page agrees. Visible change: an ST of another chronicle posting as a player character is no longer styled as an ST. |
| Posting paths | **Both stay**: the socket for live use, `ScenePostView` as the no-JS and socket-down fallback. Both call `game.scene_chat.can_post()`, validate with `PostForm`, and persist and broadcast through `game.scene_chat.create_post()`. | One set of rules (character ownership, membership, chronicle, lengths, quote straightening, command handling) and one broadcast, whatever the transport. |
| Protocol version | The socket URL chooses it: `/ws/scene/<id>/?v=2` speaks HTML; the bare URL speaks the old JSON until PR 4, after which it is refused with close code `4400`. | Per-recipient rendering makes serving both formats trivial during the rollout (each connection renders its own). Tabs opened before the deploy keep their old script, which reconnects to the bare URL; after PR 4 it gets `4400`, gives up after its five retries and falls back to posting over HTTP, as it already does when the socket is down. |
| Denied connections | Accept, then close with code **`4403`** (missing and hidden scenes alike). | A handshake rejected before `accept` reaches the browser as `1006`, which the htmx `ws` extension retries forever (up to every 64 s). `4403` is outside its retry list (1006, 1011, 1012, 1013), carries no existence information, and lets the page say "live updates unavailable". |
| Catching up | On every `htmx:wsOpen` the client sends `{"action": "sync", "after": <highest post id on the page>}`; the server answers on that socket with the posts after it (at most one window; beyond that a "reload" notice). | Covers both the render-to-connect gap and reconnects, uses the same authorization as posting, and needs no new URL. |
| Duplicates and order | Post elements have `id="post-<pk>"`. The client drops an incoming post whose id is already on the page and inserts each post before the first post with a higher id. | The sync reply and the live broadcast can overlap; two players posting at once can reach a third viewer in either order. Ids are monotonic and match `datetime_created` order for posts created through `add_post`. |
| Long scenes | The page shows the latest `SCENE_POST_WINDOW = 100` posts. "Show earlier posts" is a link to `?before=<first id>` (full page without JS) with `hx-get` to the same URL, which returns the previous window as a fragment. | No new URL or route policy; the same view and authorization serve both. |
| `django-htmx` | Still not added. | Nothing here needs more than `core.htmx`. |
| Alpine | Not loaded on the scene page. | Nothing needs it; the include gains a flag to omit it. |

## 1. One post partial

`game/templates/game/scene/_post.html` renders one post. Inputs: `post` (with
`character` and `character.owner` joined, and an `author_is_st` attribute) and
`viewer_id` (the viewer's user id or `None`). It never reads `request`, so the
page and the consumer render it identically.

```html
<div class="post-item" id="post-{{ post.pk }}" data-post-id="{{ post.pk }}">
  <p class="post mb-0">
    <strong {% if post.author_is_st %}class="st"{% elif viewer_id and post.character.owner_id == viewer_id %}class="highlight"{% endif %}>
      {% if post.character %}<a href="{{ post.character.get_absolute_url }}">{{ post.display_name }}</a>{% else %}{{ post.display_name }}{% endif %}
    </strong>: {{ post.message|safe_post }}
  </p>
</div>
```

The inline styles of today's markup move to `.post-item` in `style.css`. The
message goes through the same `safe_post` filter (bleach allowlist and quote
spans) that `render_post_html` used for the JSON; `display_name` is
autoescaped.

**Selector.** `game.selectors.scene_posts(scene, *, before=None, after=None,
limit=SCENE_POST_WINDOW)` returns a list of posts in ascending id order with
`character__owner` joined and `author_is_st` set from one
`scene_storyteller_ids(scene, owner_ids)` query (staff, superusers, the head
ST, and `STRelationship` rows for the scene's chronicle and gameline, the
exact facts `can_manage_scope` reads without a request). `before` returns the
window just before an id, `after` the posts after one (used by sync, with
`limit + 1` to detect overflow). A test checks that `scene_storyteller_ids`
agrees with `can_manage_scope` for every role.

`PostManager.for_scene_optimized()` keeps its signature and `select_related`
but drops the "ST anywhere" `Exists()` annotation, which nothing else reads.

## 2. Page and client

Structure of `detail.html` (only the parts that change):

```
div#scene-live  hx-ext="ws"  ws-connect="/ws/scene/<pk>/?v=2"   (open scenes only)
                data-ws-state="connecting"
  div#connection-status > span#status-indicator            (text set by scene-chat.js)
  div#scene-chat-notice  role=status aria-live=polite       (server notices and errors)
  div.tg-card > div#posts-container
      a#earlier-posts (if older posts exist)
      {% for post in posts %}{% include "game/scene/_post.html" %}{% endfor %}
      div#no-posts-message (only when empty; CSS hides it once a post exists)
  div#scene-actions                                          (always present)
      form#post-form  method=post action=scene_post  ws-send
                      hx-vals='{"action": "post"}'  hx-params="not csrfmiddlewaretoken"
          csrf
          div#post-character-field   {% include "_post_character_field.html" %}
          div#post-message-fields    {% include "_post_message_fields.html" %}
          submit
      form#add-char-form method=post action=scene_add_character
          csrf, span#add-char-field (select), submit          (CSS hides it with no options)
      form close, commands link                               (unchanged)
{% include "core/includes/interactive_scripts.html" with ws=True alpine=False %}
```

Without JavaScript nothing changes: the forms post to the Step 5 endpoints,
which redirect back. The regions the server replaces live are split so that a
replacement never contains a `<form>` or CSRF token (the consumer has no
request to mint one) and never touches text the viewer is typing in another
field.

**Out-of-band swaps.** Every top-level element of a server message is swapped
out of band by the `ws` extension:

| Message | Top-level elements |
|---|---|
| New post | `<div hx-swap-oob="beforeend:#posts-container">` + the partial |
| Sync reply | the same wrapper with every missed post, or a notice |
| Sender, post accepted | `#post-message-fields` (fresh, empty, `autofocus` on the message) + an empty or informational notice |
| Sender, post refused | the notice only; the typed text stays |
| Character joined | a notice for everyone; `#post-character-field` for the character's owner; `#add-char-field` for every signed-in viewer (the option disappears) |
| Scene closed | `#scene-actions` replaced by "This scene is closed." and a notice, then close code `1000` (no reconnect) |

Notices use `hx-swap-oob="innerHTML"` on `#scene-chat-notice`, so the live
region itself stays in place and screen readers announce the change.

**"No posts yet".** `#posts-container:has(.post-item) #no-posts-message
{display: none}` hides it once a post arrives. No message has to know whether
it is the first post.

**`scene-chat.js`** (static, `defer`, about 90 lines, no inline code):

- connection state: sets `data-ws-state` and the status text on
  `htmx:wsConnecting/wsOpen/wsClose/wsError`, with a specific message for
  `4403` (access lost), `4400` (reload needed) and `1000` after a close;
- on `htmx:wsOpen`, sends the sync message with the highest `data-post-id`;
- on `htmx:wsConfigSend` from the post form, if the socket is not open,
  cancels the socket send and calls `form.submit()`, so the post goes through
  `ScenePostView` (htmx has already cancelled the native submit);
- disables the Post button between `htmx:wsAfterSend` and the reply (or a close);
- on `htmx:oobBeforeSwap` into `#posts-container`, removes posts already on the
  page from the incoming fragment and inserts out-of-order posts before the
  first post with a higher id; scrolls a live post into view;
- Enter submits the message and Shift+Enter inserts a newline, as today
  (`form.requestSubmit()`, so HTML validation still runs).

**Vendoring.** `htmx-ext-ws` 2.0.4 (`dist/ws.min.js`, 5,144 bytes, 0BSD, no
`sourceMappingURL`) goes to `source_static/vendor/htmx-ext-ws/2.0.4/` with its
licence and a `VENDOR.md` row: npm integrity
`sha512-LnOpFRL/2hInhdKl/9N0OJsb4GYQ5/teUdTHNZYY9ytYdxYEqjfLEe0MWgF3ODjfwGJRb4E95igAbU66te48ZA==`,
checked against the registry when vendoring. `interactive_scripts.html` takes
`ws` (add the extension after htmx) and `alpine` (default true) flags; the SRI
test renders it with both and checks every file.

## 3. Protocol

**Client to server (v2).** `ws-send` serialises the form's fields plus
`hx-vals` as a JSON object and adds a `HEADERS` object (htmx request headers),
which the server ignores. `hx-params` keeps the CSRF token off the socket; the
socket's origin is already checked by `AllowedHostsOriginValidator`.

```json
{"action": "post", "character": "12", "display_name": "", "message": "…", "HEADERS": {…}}
{"action": "sync", "after": 431}
```

Values are read as strings (`character`, `display_name`, `message`) or an
integer (`after`); anything else is ignored. Frames larger than
`DATA_UPLOAD_MAX_MEMORY_SIZE` (the HTTP limit) are refused. Unknown actions get
an error notice.

**Server to client (v2).** HTML only, as in §2.

**v1 (until PR 4).** Unchanged JSON in both directions (`chat_message`,
`add_character`; `new_post`, `character_added`, `system_message`, `error`), but
`chat_message` goes through the shared service, so its checks and messages are
the new ones. Group events are protocol-neutral (`scene.post` with `post_id`,
`scene.characters` with `character_id`, `scene.closed`); each connection
renders them in its own protocol.

**Rollout.** PR 2 deploys a server that speaks both; PR 3 switches the page to
v2 (old tabs keep v1 until reloaded); PR 4, one deploy later, removes v1 and
answers the bare URL with `4400`, which makes any remaining old tab fall back
to HTTP posting.

## 4. Reliability

- **Reconnect.** The extension reconnects after `1006/1011/1012/1013` (server
  restart, network loss) with full-jitter backoff capped at 64 s, and never
  after the server's deliberate `1000`, `4400` or `4403`. Messages sent while
  connecting are queued by the extension; the fallback above sends them over
  HTTP instead when the socket is known to be down.
- **Catch-up** by `sync` on every open, including the first (render-to-connect
  gap). More than one window missed → a notice with a reload link.
- **Ordering and duplicates** as in Decisions. Server-side, each connection's
  messages are sent in the order the channel layer delivers them.
- **Closed scene.** Closing broadcasts `scene.closed`; connections replace the
  actions and close with `1000`. A finished scene's page has no `ws-connect`.
  Posting to a finished scene is refused by both paths.
- **Broadcast failures** (for example Redis down) never fail the post: events
  are sent from `transaction.on_commit(..., robust=True)`, so a post is never
  announced before it is committed and a layer error is only logged.

## 5. Authorization

| Moment | Check |
|---|---|
| `connect` | The scene exists and `can_view_scene(user, scene)` (anonymous users only for `PUBLIC`). Else accept + close `4403`. |
| Every `receive` | Reload the scene; still visible (else `4403` close), not finished. |
| `post` | `scene_chat.can_post(user, scene)`: authenticated, and owns a character in the scene. Then `PostForm(user, scene)`: the character is the user's own, in this scene and this chronicle; a user with several must pick one; message not blank; display name ≤ 100. |
| `sync` | Covered by the visibility re-check. |
| Every group event | Re-check the recipient's visibility before rendering (as today); lost access → close `4403`. |
| HTTP fallback | Unchanged Step 5 gates (`can_view_scene` → 404; not finished; owns a character in the scene → 403), plus the same `can_post` and `PostForm` inside the service. `SceneAddCharacterView` (`AddCharForm`: this chronicle, own characters unless scope ST, not already present) and `SceneCloseView` (`can_manage_scope`) are unchanged and now broadcast. |

The socket's `add_character` is removed with v1 in PR 4 (finding 4): adding a
character stays an HTTP action with the stronger form.

## 6. One posting path

`game/scene_chat.py`:

```python
SCENE_POST_WINDOW = 100
def group_name(scene_id) -> str
def can_post(user, scene) -> bool
def create_post(scene, form) -> ServiceResult          # form is a valid PostForm
def broadcast(scene_id, event_type, **data) -> None    # on_commit, robust
```

`create_post` resolves the character (the user's only character in the scene,
or the chosen one), straightens quotes, calls `Scene.add_post`, and classifies
the outcome: a post (`ok`, broadcast `scene.post`), an `@storyteller` message
(`ok`, "Message sent to the storyteller."), or a refused command (raises
`ActionFailed("Command does not match the expected format.")`, finding 2). It
runs inside the caller's transaction (`ObjectActionView` for HTTP; an explicit
`atomic()` in the consumer).

`ScenePostView.perform` becomes `return scene_chat.create_post(self.object,
form)`; the consumer's post handler runs `can_post`, `PostForm` and
`create_post` in one `database_sync_to_async` call. `SceneAddCharacterView` and
`SceneCloseView` call `broadcast()` after their model call.

## 7. Performance

- The page renders one window of posts from `scene_posts()`: two queries
  (posts with authors, storyteller ids) whatever the window size. The query
  budget test keeps its ceiling and gains a "window does not grow" case.
- The per-post `profile.is_st` query is gone (Step 8), and the new ST test is
  one query per page or per live post.
- Per live post and recipient: one visibility query, one post query, one
  storyteller query, one render.
- Unchanged and noted: `Scene.add_post` updates read status with one
  `get_or_create` and `save` per participant. It is on the posting path, not
  the render path, and its semantics belong to the notifications code.

## 8. Tests

- **Partial** (`game/tests/templates/test_post_partial.py`): link and display
  name, sanitised message (a `<script>` is stripped, quotes wrapped), `st` for
  a scoped ST author, `highlight` only for the viewer's own posts, nothing for
  anonymous viewers, ownerless posts render without a link, and the page's
  post markup equals the partial's.
- **Selector**: windows (`before`, `after`, overflow), storyteller ids agree
  with `can_manage_scope` across staff, head ST, scoped ST, wrong-gameline ST,
  other-chronicle ST and players.
- **Service**: validation, quote straightening, `@storyteller`, refused command
  (no post, `ActionFailed`), `can_post`, broadcast only after commit.
- **HTTP actions**: a post, an added character and a close each reach a group
  listener; storyteller and bad-command messages are reported correctly.
- **Consumer** (`WebsocketCommunicator`, `TransactionTestCase`): connect
  allowed and denied (`4403`) across the Step 0 audiences; a v2 post returns
  the fresh fields to the sender and broadcasts HTML that equals the partial
  rendered for each recipient (`highlight` for the author only); refused posts
  (another user's character, a non-member, a finished scene, anonymous on a
  public scene, bad command, blank message, over-long display name) create
  nothing and return a notice; `sync` returns the missed posts and the
  overflow notice; a character joining updates the owner's fields; a close
  replaces the actions and closes with `1000`; v1 JSON keeps working until PR
  4, after which the bare URL gets `4400`.
- **Static**: the SRI test covers the extension; the inline-script inventory
  allows none; no template other than the partial renders post markup.
- **Browser** (Playwright, `ChannelsLiveServerTestCase` so the socket is real;
  skipped without Playwright or Chromium): two signed-in players in two
  contexts, A posts and B sees it without reload, A's own post is highlighted
  for A only; the "no posts" placeholder disappears; the textarea clears only
  on success; a refused command keeps the text and shows the notice; a post
  made while B's socket is down appears after B reconnects (sync); HTTP
  fallback when the socket is closed; earlier posts load in place; no console
  errors from application code.

## 9. PR slicing

1. **Partial, selector and service; no protocol change.** `_post.html`,
   `scene_posts`/`scene_storyteller_ids`, `game/scene_chat.py`; the page uses
   the partial; `ScenePostView` and the v1 consumer post through the service
   (fixes findings 2 and 6); HTTP actions broadcast `scene.*` events, which
   the v1 consumer translates to its JSON (finding 1).
2. **The consumer speaks HTML on `?v=2`.** Per-recipient rendering, notices,
   sync, closed-scene handling, `4403`; v1 unchanged.
3. **The client switches to htmx ws.** Vendored extension, include flags, page
   regions, `scene-chat.js`, earlier-posts window, CSS; the inline script is
   no longer used by the page.
4. **Delete v1.** The inline script (if not already gone), `serialize_post`,
   the JSON handlers, the socket `add_character`, the inventory-test
   exception; the bare URL gets `4400`.

## Theory

A post is a row plus one template. Whether it reaches a browser in the first
page load, in a live broadcast, in a catch-up after a reconnect or in an
"earlier posts" fragment, it is rendered by the same partial with the same
inputs for the viewer who will see it. The transport only moves HTML; the
server decides who may post, what a post looks like for each viewer, and what
a client missed. The browser's remaining job is connection state, de-duplication
and order, which no server rendering can do for it.
