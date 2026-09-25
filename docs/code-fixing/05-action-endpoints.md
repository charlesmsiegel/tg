# Task: Design dedicated action endpoints to replace multi-button POST handlers in `tg` (Step 5)

You are designing, **not implementing**, the replacement of large `post()` methods that branch on which button was pressed with small, dedicated action endpoints. Each endpoint gets its own URL, form, permission, transaction and response. The repository is `charlesmsiegel/tg`: Django 5.2 with django-polymorphic 4.1, a World of Darkness character and chronicle manager. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/tg-permissions/SKILL.md`, `.claude/skills/model-standards/SKILL.md` and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. Read the designs for Step 0 (authorization) and Step 4 (game rules out of views) if they exist. Actions should call Step 4's services and be gated by Step 0's mechanism. Write:
  - `docs/superpowers/specs/2026-09-25-action-endpoints-design.md`
  - `docs/superpowers/plans/2026-09-25-action-endpoints.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## Current multi-action handlers

### `MageDetailView.post` (`characters/views/mage/mage.py:268-437`, 170 lines, the longest method in the package)

**Confirmed:**
- It binds `MageXPForm` and `RoteCreationForm` together, then branches on `"spend_xp" in form.data.keys()`.
- The spend-XP branch has category sub-branches (Image, Rote, others), and the Rote one contains a nested validation ladder.
- It handles approval with `if "Approve" in form.data.values()`, then locates the request by searching for the key whose value is `"Approve"`.

**Reported:** it also handles Reject, specialties, retire and decease. It re-implements approval inline rather than using `XPApprovalMixin`, and its retire/decease path skips the owner/EDIT_FULL check that `CharacterDetailView.post` performs (`characters/views/core/character.py:~55-77`).

### `ApprovalMixin.post` (`core/mixins.py:~677-760`)

Used through `XPApprovalMixin` by most character detail views. **Confirmed:**
- It finds the request by parsing a button value out of `request.POST.values()`.
- It approves without `select_for_update`, while reject does lock the row.
- If the parent class has no `post`, it falls through to a redirect.

**Reported:** Drone, Fomor and Spirit detail views have no `post` at all, yet their shared template shows retire/decease buttons.

### `game/views.py`

- **`ChronicleDetailView.post` (`~:215-265`):**
  - Branches on `create_character` / `create_location` / `create_item` (**Confirmed** at :220, :227, :234), then `create_story` and `create_scene`.
  - Reported: it reads raw `request.POST["name"]`, `["location"]` and `["date_of_scene"]` even though a `SceneCreationForm` is built for the page, and `Story.objects.create` isn't linked to the chronicle.
- **`SceneDetailView.post` (`~:298-344`):** branches on `close_scene`, `character_to_add` and `message` (**Confirmed** at :302, :316, :324).
- **`JournalDetailView.post` (`~:408-440`):** branches on `submit_entry` and `submit_response`. It finds the entry with `[x for x in request.POST.keys() if "entry" in x][0]` (**Confirmed** at :428), which also matches `submit_entry`.

### Index "create or list" POSTs

`CharacterIndexView.post`, `ItemIndexView.post` and `LocationIndexView.post` (`characters/views/core/__init__.py:~380-399`, `items/views/core/__init__.py:~181-205`, `locations/views/core/__init__.py:~177-201`) redirect based on a posted type name, using an incomplete if/elif gameline map. **Confirmed.** Step 0 fixes the security side (the `get_or_create` on raw input and the unbound variable). Your design should decide whether these become plain GET links or a single typed endpoint.

## What the design must deliver

1. **A full inventory of actions:** every POST branch in the app, including ones this audit missed. For each: the current handler, the proposed URL (e.g. `POST /characters/<pk>/xp-requests/<id>/approve/`), the form, the permission (from the Step 0 mechanism), the service it calls (Step 4), and the response.
2. **A small base class or mixin for object actions.** It loads and authorizes the object, binds the form, runs the service in a transaction with appropriate locking, adds a message, and redirects. It must also be able to return a fragment later for htmx (Step 10); design the hook, not the htmx.
3. **Template changes:** how each button and form points at its new endpoint, and what happens to forms that currently submit several intents at once.
4. **Retire/decease and approval for every character type:** either every detail page offers only actions that work, or the buttons are removed.
5. **Tests:** per-action permission tests (owner, other player, ST of this chronicle, ST of another chronicle, anonymous); a test that GET on an action URL is rejected; idempotency and double-submit tests for approve.
6. **PR slicing:** one handler per PR, starting with approval, which is security-adjacent.

## Constraints and scope

- Design only. Don't modify application code.
- Don't change game rules; call services.
- Out of scope: new UI flows (htmx) and chargen step views, which are routed by the Step 2 registry.
