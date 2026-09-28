# Scene Chat over htmx WebSockets Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans. Tasks are ordered;
> each is an independently reviewable PR. Steps use checkbox syntax.

**Goal:** Scene posts are rendered by one server template for the first page
load and every live update, pushed as HTML over the existing Channels socket
and swapped in by htmx's `ws` extension; the 330-line inline script is gone.

**Architecture:** `game/scene_chat.py` is the one posting path (permission,
`PostForm`, quote straightening, `add_post`, broadcast on commit) for the
socket and the HTTP fallback. Group events carry ids; each connection renders
`game/scene/_post.html` for its own viewer. The socket protocol is chosen by
URL (`?v=2` = HTML) so old tabs keep working through the rollout.

**Tech Stack:** Django 5.2, Channels 4.1 (InMemory layer in tests, Redis in
production), htmx 2.0.11 + htmx-ext-ws 2.0.4 (vendored), Playwright for Python
against the preinstalled Chromium.

**Spec:** ../specs/2026-09-25-scene-chat-htmx-design.md

## Global constraints

- No npm, bundler, React or Vite; no inline scripts, `hx-on` or eval.
- No new URLs or route policies; Step 0 gates stay as they are and every
  socket action re-checks them.
- Without JavaScript the page behaves as today (Step 5 endpoints).
- Never send one viewer's rendering to another connection.

## Review focus

- A socket post and an HTTP post go through the same `can_post`, `PostForm`
  and `create_post`; neither can post as another user's character, a
  non-member, into a finished scene, or anonymously.
- Broadcasts happen only after commit and never fail the request.
- A replaced region never contains a form or CSRF token and never clears text
  the viewer is typing elsewhere.
- Denials close with `4403` and reveal nothing about hidden scenes.

### Task 1 (PR 1): Partial, selector and one posting service

Files: `game/templates/game/scene/_post.html`, `game/selectors.py`,
`game/scene_chat.py`, `game/models.py` (`for_scene_optimized`),
`game/views.py`, `game/actions.py`, `game/consumers.py` (v1 posts through the
service; `scene.*` events), `game/templates/game/scene/detail.html`,
`source_static/style.css`, tests.
Interfaces: `scene_post_window(scene, *, before, limit)`,
`scene_posts_after(scene, after, *, limit)`, `scene_post(scene, id)`,
`scene_storyteller_ids(scene, user_ids)`, `SCENE_POST_WINDOW`,
`group_name(id)`, `can_post(user, scene)`, `create_post(scene, form)`,
`broadcast(scene_id, type, **data)`.

- [x] Failing tests first: HTTP post is not broadcast; bad command reported as success; socket accepts a 101-character display name.
- [x] `scene_storyteller_ids` (one query) with an agreement test against `can_manage_scope` for every role.
- [x] Post windows (`before`, `after`, overflow) with `author_is_st` set; `?before=` pages back without JavaScript.
- [x] `_post.html` with `viewer_id`; the page includes it; inline styles move to `.post-item`; links use the type-dispatching character route (they were blank).
- [x] `scene_chat.create_post` classifies post / storyteller / refused command; `ScenePostView.perform` and the v1 consumer use it; `PostForm` validates socket input.
- [x] `SceneAddCharacterView` and `SceneCloseView` broadcast; v1 consumer translates `scene.post`/`scene.characters`/`scene.closed` into its JSON.
- [x] Query budget: the scene page cost does not grow with the window.

### Task 2 (PR 2): The consumer speaks HTML on `?v=2`

Files: `game/consumers.py`, `game/templates/game/scene/ws/*.html`
(`_notice`, `_post_oob`, `_closed`), `game/templates/game/scene/_post_character_field.html`,
`_post_message_fields.html`, `_add_character_field.html`, tests.

- [x] Protocol flag from the query string; v1 behaviour untouched.
- [x] v2 connect denial: accept + close `4403`.
- [x] `post`: sender gets fresh `#post-message-fields` + notice; refused posts get a notice only.
- [x] Per-recipient `scene.post` render (visibility re-check, one post query, the partial with the recipient's `viewer_id`).
- [x] `sync` with overflow notice; frame-size limit; unknown action notice.
- [x] `scene.characters`: notice for all, `#post-character-field` for the owner, `#add-char-field` for signed-in viewers.
- [x] `scene.closed`: `#scene-actions` replaced, close `1000`.
- [x] `WebsocketCommunicator` tests for all of the above, including broadcast HTML equal to the partial per recipient.

### Task 3 (PR 3): The client switches to htmx ws

Files: `source_static/vendor/htmx-ext-ws/2.0.4/{ws.min.js,LICENSE}`,
`source_static/vendor/VENDOR.md`, `core/templates/core/includes/interactive_scripts.html`,
`core/tests/test_htmx.py`, `game/static/game/js/scene-chat.js`,
`game/templates/game/scene/detail.html`, `_post_window.html`, `game/views.py`
(`?before=` window and fragment), `source_static/style.css`,
`widgets/tests/test_static_assets.py`, `game/tests/browser/test_scene_chat.py`.

- [x] Vendor the extension from the npm tarball; verify the registry `sha512`; record SRI and licence.
- [x] Include flags `ws` and `alpine`; SRI test renders every combination.
- [x] Page regions and `ws-connect`/`ws-send`/`hx-vals`/`hx-params`; CSS for the placeholder and empty add form.
- [x] `scene-chat.js`: state, sync on open, HTTP fallback, CSRF token kept off the socket, busy button, de-duplication and order, Enter to send.
- [x] Delete the inline script (a page cannot run both clients); the inline-script inventory allows no template.
- [x] Earlier-posts window: full page and fragment from the same URL, `Vary` and `TG-Fragment`.
- [x] Playwright (Daphne child process, `route_web_socket` for drops and injected frames): two players see each other's posts live; highlight and ST style per viewer; placeholder; failure keeps text; catch-up before first open and after a reconnect; duplicates and late posts; HTTP fallback on `4403`; closing; earlier posts; no console errors.

### Task 4 (PR 4): Delete the JSON protocol

Files: `game/consumers.py`, `game/tests/consumers/test_consumers.py`,
`game/tests/consumers/test_scene_chat_socket.py`.

- [x] Remove the JSON payload builders (`serialize_post`, later `post_payload`), the v1 handlers, the socket `add_character` and the JSON helpers.
- [x] Any socket URL without `?v=2` closes with `4400`.
- [x] Replace the tautological v1 consumer tests; keep the Step 0 audience tests on the HTML protocol.

## Suggested PR order

1 → 2 → 3 → 4. PR 4 ships at least one deploy after PR 3 so tabs opened
before PR 3 have had a chance to reload; any that have not fall back to HTTP.


## Execution record

- **Ruling:** the user asked for the plan to be made and implemented, which
  supersedes the brief's design-only scope, as in Steps 2, 3, 4, 9 and 10.
  The four tasks are four commits on one branch, in PR order, after the spec
  and plan.
- **Ruling:** the frontend, permissions and testing skills named in the brief
  are consolidated in `.claude/skills/tg-standards/`; its references were used.
- **Ruling:** Playwright for Python and `tblib` are development-only and are
  not added to `requirements.txt`. The browser tests skip without Playwright
  or Chromium and never run `playwright install`.
- **Baseline:** 430 game, htmx, static-asset and query-budget tests passed
  before any change.
- **Deviations:** see the spec's implementation record (`hx-params` removed
  because it breaks `ws-send` in htmx 2.0.11; the inline script deleted in
  PR 3; the browser tests start Daphne with `subprocess`; the fragment
  template chosen in `render_to_response`).
- **Defects found and fixed:** HTTP posts, added characters and closes were
  never broadcast; malformed dice commands were reported as success (HTTP) or
  as "sent to storyteller" (socket); a refused socket post lost the typed text;
  the socket bypassed `PostForm` (unbounded display name); posts made between
  page render and socket open, or during a reconnect, were lost; anonymous
  readers of public scenes got no live updates; every post link on the page
  was `href=""`; page and socket disagreed on who is styled as an ST.
- **Noted, not changed:** per-participant read-status writes in
  `Scene.add_post`; the Close Scene button shown to non-STs (Step 6 owns
  template permission flags); no rate limit on posting by either path.

### Measurements

| Measure | Before | After |
|---|---|---|
| Inline script on the scene page | 330 lines (257 non-blank), 1 executable inline script left in the app | **0**; the inventory test allows none |
| Static chat JS | none | `scene-chat.js`: 180 lines, 142 of code; plus vendored `htmx-ext-ws` 2.0.4 (5 KB) and htmx 2.0.11 |
| Places that build post markup | 2 (template, `appendPost`) + a JSON serializer | **1** (`_post.html`) |
| Consumer | 292 lines, JSON in and out, own authorization helpers | 278 lines, HTML out, posts through `game.scene_chat` |
| Posting paths | 2 with different rules | 1 service (`can_post`, `PostForm`, `create_post`, `broadcast`) |
| Posts rendered on a page | all | latest 100; earlier windows in place |
| Queries for a window of posts | 1 (with an `Exists` per row) | 2 whatever the window size (posts, storyteller ids) |
| Per live post and recipient | 1 scene + visibility check, JSON built once by the sender | scene + visibility check, 1 post query, 1 storyteller query, one render |

### Verification

- New tests: 35 non-socket tests (`game/tests/test_scene_chat.py`), 18
  socket tests on the HTML protocol (`test_scene_chat_socket.py`), the 4
  Step 0 socket pins rewritten for it (`test_consumers.py`, which drops 24
  tautological tests), 8 Playwright tests against a real Daphne process
  (`game/tests/browser/`), and the vendoring/SRI and inline-script inventory
  updates.
- Regressions checked against the old code before fixing: the bad-command
  success message and the blank links (throwaway test on the parent commit);
  the ordering/duplicate test fails with the client handler disabled.
- `game core widgets accounts` plus both browser suites: 1,920 tests OK
  (`--parallel 4`, 4 pre-existing skips).
- Full suite (`--parallel 4`, browser tests enabled): 7,479 tests, 34
  skipped, 3 failures, none in code this step touches.
  `TestHumanCharacterCreationView.test_creation_status_selector` and
  `TestAttributeView.test_update_view_template` fail identically on `main`
  (Step 10's record). `ValidateOnlyTests.test_partial_requests_are_throttled_per_character`
  passes alone; its throttle key includes the clock minute, so three requests
  that straddle a minute boundary in a slow parallel run are never throttled.
  That flake belongs to Step 10's test, not this change.
