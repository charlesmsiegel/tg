# Task: Design server-rendered live scene chat with htmx over Django Channels in `tg` (Step 11)

You are designing, **not implementing**, a rewrite of the play-by-post scene chat so that post markup is rendered on the server from one template and pushed to browsers as HTML. This replaces a WebSocket consumer that sends JSON and a large inline script that rebuilds the post markup by hand. The repository is `charlesmsiegel/tg`: Django 5.2 with Django Channels 4.1 and channels-redis, a World of Darkness chronicle manager. No React, Vite or npm: use htmx and its WebSocket extension, vendored as static files. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/tg-frontend/SKILL.md`, `.claude/skills/tg-permissions/SKILL.md` and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. Read these designs if they exist:
  - Step 0: authorization, including chronicle-scoped storyteller checks and the scene POST findings;
  - Step 5: action endpoints; `SceneDetailView.post` branches may already be split;
  - Step 9: static JS;
  - Step 10: htmx vendoring and conventions. Reuse them rather than choosing new ones.

  Write:
  - `docs/superpowers/specs/2026-09-25-scene-chat-htmx-design.md`
  - `docs/superpowers/plans/2026-09-25-scene-chat-htmx.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed. Chromium and Playwright are available (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`; don't run `playwright install`).
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## Current state

- **The consumer: `game/consumers.py`** (313 lines, **Confirmed**).
  - `connect` (:29), `receive` (:65, JSON), `handle_chat_message` (:84), `handle_add_character` (:149), `chat_message_broadcast` (:186), `character_added_broadcast` (:197) and `send_error` (:208) all `json.dumps` their payloads.
  - `serialize_post` (:299) builds the JSON for a post.
  - It has its own `straighten_quotes` (:220), and `game/views.py:~347-386` has another one (Reported). Step 4 may consolidate them.
  - Helpers `user_owns_character` and `character_in_scene` perform authorization inside the consumer. Review them against Step 0's policy.
- **The page: `game/templates/game/scene/detail.html`** (456 lines).
  - Initial posts render from `{% for post in object.post_set.all %}` at line 48. This ignores the optimized `context["posts"] = Post.objects.for_scene_optimized(scene)` that `game/views.py:282` builds. **Confirmed.**
  - Reported:
    - A 329-line inline `<script>` (`~126-455`) manages the WebSocket and builds post DOM in JS (`appendPost` `~302`), duplicating the template markup at `~48-54`.
    - Each post reads `post.character.owner.profile.is_st`, which is N+1.
- **Two ways to post.** Besides the WebSocket, `SceneDetailView.post` (`game/views.py:~298-344`) handles `close_scene`, `character_to_add` and `message` over HTTP (**Confirmed** branches at :302, :316, :324). Reported: its storyteller check is inline and differs from the rest of the file, and `character_to_add` doesn't verify that the character belongs to the scene's chronicle.

## What the design must deliver

1. **One post partial** (e.g. `game/scene/_post.html`) used for the initial render and for every live update. The consumer renders it with `render_to_string` (async-safe, e.g. through `database_sync_to_async`) and broadcasts HTML.
   - Decide how viewer-specific markup is handled (ST-only controls, "your character" styling): render a viewer-neutral fragment and apply per-viewer differences with CSS or a small script, or render per recipient through per-user groups. Justify the choice.
2. **The client:**
   - htmx's `ws` extension (`hx-ext="ws"`, `ws-connect`, `ws-send` on the post form);
   - out-of-band swaps (`hx-swap-oob="beforeend:#posts-container"`) for new posts and for characters added to the scene;
   - error display;
   - removing the "no posts yet" placeholder.

   The 329-line inline script should shrink to nothing or near nothing.
3. **Protocol:** the message shapes in both directions (form-encoded fields from `ws-send` vs the current JSON), versioning during rollout, and whether the old JSON protocol must keep working briefly (open tabs during deploy).
4. **Reliability:** reconnect behaviour; catching up missed posts after reconnect (e.g. `hx-get` of posts after the last seen id); ordering; duplicate suppression; a closed scene.
5. **Authorization:** check authentication and scene membership on connect, re-check on every receive (owner of the posting character, character in the scene, ST of *this* chronicle), all consistent with Step 0. Also check the HTTP fallback paths.
6. **One posting path:** decide whether HTTP posting remains as a no-JS fallback, and make both paths share one service function (validation, quote straightening, persistence, broadcast).
7. **Performance:** use the optimized posts queryset; eliminate the per-post `profile.is_st` query; paginate or window long scenes.
8. **Tests:** Channels `WebsocketCommunicator` tests (connect auth, posting, broadcast HTML contains the partial, unauthorized receive rejected); template tests for the partial; and a Playwright two-browser test in which a post from A appears for B.
9. **PR slicing:**
   1. Partial and service function, with no protocol change.
   2. The consumer broadcasts HTML.
   3. The client switches to htmx ws.
   4. Delete the inline script and the JSON serializers.

## Constraints and scope

- Design only. Don't modify application code.
- No React, Vite or npm.
- Out of scope: other game views, chargen, and Channels infrastructure (Redis configuration, deployment).
