# Task: Design a unified permission context for templates and querysets in `tg` (Step 6)

You are designing, **not implementing**, a single, consistent way for permission information to reach templates and list querysets. The repository is `charlesmsiegel/tg`: Django 5.2 with django-polymorphic 4.1, a World of Darkness manager. Step 0 makes the **server-side gates** correct. This step makes everything around them coherent:
- what templates are told the user can do;
- that list filtering and per-object checks agree;
- that permission checks are cheap.

You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/tg-permissions/SKILL.md`, `.claude/skills/tg-frontend/SKILL.md` and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. **The Step 0 authorization design (`*-authorization-hardening-design.md`) is a prerequisite.** Build on its mechanism and its canonical chronicle-scoped storyteller helper. If it doesn't exist yet, state your assumptions. Write:
  - `docs/superpowers/specs/2026-09-25-permission-context-design.md`
  - `docs/superpowers/plans/2026-09-25-permission-context.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## Current state

- **`PermissionManager`** is in `core/permissions.py`. `get_user_roles` is at `~:103-172`, `ROLE_PERMISSIONS` at `~:55-100` (**Confirmed**), status overrides at `~:208-261`, and `filter_queryset_for_user` at `~:390-470`.
- **`is_approved_user` means different things depending on who set it** (Reported, with some items confirmed):
  - `core/middleware/approved_user.py:~7-8` sets it for staff.
  - `PermissionRequiredMixin` (`core/mixins.py:~82`) sets it True for any passed check, including view-only.
  - `SpecialUserMixin.get_is_approved_user` (`core/mixins.py:~280`) means owner, any storyteller, or staff. **Confirmed.**
  - `characters/views/core/character.py:~45` sets it to `user_can_edit`.
  - `locations/views/mage/chantry.py:~204,236` hard-code True.
  - `game/views.py:~403` overwrites the value the mixin just set.
  - About 28 view locations re-set it so owners can see the chargen UI.
- **Template usage** (Reported): `is_approved_user` 43 times in 20 files, `is_st` 34, `profile.is_st` 14, `owner == user` 6.
- **Unused permission helpers:**
  - `core/templatetags/permissions.py` (205 lines, with about 605 lines of tests) is loaded by **zero** templates. **Confirmed.**
  - `core.context_processors.permissions` (`core/context_processors.py:~15`) isn't registered in settings (Reported).
- **Cost** (Reported):
  - There is no per-request caching. `get_user_roles` costs up to about 5 queries per call, and `get_visibility_tier` calls `user_has_permission` up to 4 times.
  - `VisibilityFilterMixin.get_context_data` (`core/mixins.py:~149-160`) triggers about 7 role computations, roughly 30 or more queries per detail page.
  - `profile.is_st()` (`accounts/models.py:~89-91`) is uncached and called 17 times in `game/views.py`.
- **List filtering and object checks disagree** (Reported):
  - `filter_queryset_for_user` leaves out STRelationship storytellers, who get CHRONICLE_HEAD_ST in `get_user_roles`, so they can edit objects they can't see in lists.
  - The `owned_by.owner` path exists only in the object check.
  - PLAYER is "any character in the chronicle, any status" in roles, but "approved character and `status="App"`" in the filter.
  - Anonymous users see `visibility="PUB"` objects in lists, but anonymous has no permissions, so the detail page 404s.
  - No item or location ListView applies visibility filtering at all; `VisibilityFilterMixin` is used by 9 character ListViews only.
- **About 10 separate "is ST" checks** exist across mixins, views and templates. Step 0 picks the canonical one; this step migrates the template and queryset side to it.

## What the design must deliver

1. **A template-facing contract.** For example, a `perms` object in context per primary object, with fields like `can_view_full`, `can_edit`, `can_edit_limited`, `can_spend_xp`, `can_spend_freebies`, `can_approve` and `is_chronicle_st`. Define:
   - how it is computed (once per request per object);
   - how views provide it (mixin or context processor);
   - how lists of objects get per-row permissions without N+1 queries.
2. **Retiring `is_approved_user`:** a migration table mapping each template usage to the new field it should use, and a plan for removing the flag.
3. **The fate of the `permissions` template-tag library and the context processor:** adopt, rewrite or delete, with a justification.
4. **Per-request memoization** of roles and permissions, keyed on (user, object). Include invalidation after in-request mutations, and query-count targets with `assertNumQueries` tests for the key pages.
5. **A single rule definition** that both `get_user_roles` and `filter_queryset_for_user` derive from, or failing that, a property-style test that asserts `obj in filter_queryset_for_user(user) ⇔ user_has_permission(user, obj, VIEW_*)` over fixture matrices. Decide the intended rule for each disagreement listed above; flag product decisions.
6. **List visibility for items and locations.** Apply the same filtering, or document why it isn't needed.
7. **PR slicing:** caching first (a pure performance change), then the context contract, then template migration by app, then list-filter alignment.

## Constraints and scope

- Design only. Don't modify application code.
- Templates must never be the enforcement point; they only reflect server-side decisions.
- Out of scope: the view-level gates themselves (Step 0) and template visual deduplication (Step 8).
