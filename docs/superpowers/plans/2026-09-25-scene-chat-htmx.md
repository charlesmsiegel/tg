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
Interfaces: `scene_posts(scene, *, before, after, limit)`,
`scene_storyteller_ids(scene, user_ids)`, `SCENE_POST_WINDOW`,
`group_name(id)`, `can_post(user, scene)`, `create_post(scene, form)`,
`broadcast(scene_id, type, **data)`.

- [x] Failing tests first: HTTP post is not broadcast; bad command reported as success; socket accepts a 101-character display name.
- [x] `scene_storyteller_ids` (one query) with an agreement test against `can_manage_scope` for every role.
- [x] `scene_posts` windows (`before`, `after`, overflow) with `author_is_st` set.
- [x] `_post.html` with `viewer_id`; the page includes it; inline styles move to `.post-item`.
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
`game/tests/browser/test_scene_chat.py`.

- [x] Vendor the extension from the npm tarball; verify the registry `sha512`; record SRI and licence.
- [x] Include flags `ws` and `alpine`; SRI test renders every combination.
- [x] Page regions and `ws-connect`/`ws-send`/`hx-vals`/`hx-params`; CSS for the placeholder and empty add form.
- [x] `scene-chat.js`: state, sync on open, HTTP fallback, busy button, de-duplication and order, Enter to send.
- [x] Earlier-posts window: full page and fragment from the same URL, `Vary` and `TG-Fragment`.
- [x] Playwright: two players see each other's posts live; highlight per viewer; placeholder; failure keeps text; sync after reconnect; HTTP fallback; earlier posts; no console errors.

### Task 4 (PR 4): Delete the JSON protocol

Files: `game/consumers.py`, `game/templates/game/scene/detail.html`,
`widgets/tests/test_static_assets.py`, `game/tests/consumers/test_consumers.py`.

- [x] Remove `serialize_post`, the v1 handlers, the socket `add_character`, the JSON helpers and the inline script.
- [x] The bare socket URL closes with `4400`.
- [x] The inline-script inventory allows no template.
- [x] Replace v1 consumer tests with v2 equivalents; keep the Step 0 audience tests.

## Suggested PR order

1 → 2 → 3 → 4. PR 4 ships at least one deploy after PR 3 so tabs opened
before PR 3 have had a chance to reload; any that have not fall back to HTTP.

## Execution record

(Filled in after implementation.)
