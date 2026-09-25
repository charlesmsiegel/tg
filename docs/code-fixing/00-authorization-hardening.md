# Task: Design the authorization fix for the `tg` Django app ("Step 0: security")

You are designing, **not implementing**, a fix for a set of authorization and input-handling holes in this repository (`charlesmsiegel/tg`, Django 5.2 with django-polymorphic 4.1; a World of Darkness character/chronicle manager). The output is a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/tg-permissions/SKILL.md`, `.claude/skills/model-standards/SKILL.md`, `.claude/skills/tg-testing/SKILL.md`.
- Read the existing design docs in `docs/superpowers/specs/` and `docs/superpowers/plans/` and follow their format and naming. Write:
  - `docs/superpowers/specs/2026-09-25-authorization-hardening-design.md`
  - `docs/superpowers/plans/2026-09-25-authorization-hardening.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if you need to run tests or introspect URL patterns.
- The findings below came from a code-reading audit. Items marked **Confirmed** were re-checked against the source. Items marked **Reported** are credible but unverified: confirm or refute each one (ideally with a quick failing test or a Django shell check) before you design around it, and say in the doc which ones you confirmed.

## How authorization works today

- **`core/permissions.py` → `PermissionManager`**
  - `get_user_roles()` builds a role set for (user, object).
  - `ROLE_PERMISSIONS` (lines ~55–100) maps roles to permissions.
  - Status overrides adjust the result.
  - Roles: OWNER, ADMIN, CHRONICLE_HEAD_ST, GAME_ST, PLAYER, OBSERVER, AUTHENTICATED, ANONYMOUS.
  - **OWNER has VIEW_FULL, EDIT_LIMITED, SPEND_XP and SPEND_FREEBIES, but not EDIT_FULL and not APPROVE.**
  - There is no per-request caching; each check costs several queries.
- **View mixins in `core/mixins.py`**
  - `PermissionRequiredMixin` (a `dispatch` gate) and its subclasses `ViewPermissionMixin` (VIEW_FULL, 404 on deny), `EditPermissionMixin` (EDIT_FULL, 403), `SpendFreebiesPermissionMixin` and `SpendXPPermissionMixin` (unused).
  - `StorytellerRequiredMixin` (a global `profile.is_st()`, not scoped to a chronicle).
  - `STRequiredMixin` (chronicle-scoped, unused, and references a nonexistent `head_storytellers`).
  - `CharacterOwnerOrSTMixin` and `OwnerRequiredMixin`.
  - A second, unrelated `STRequiredMixin` in `core/views/character_template.py:30`.
- **`SpecialUserMixin` (`core/mixins.py:266`) is NOT a gate.**
  - It only computes a template flag (`is_approved_user`).
  - `check_if_special_user` returns True for the owner, for **any** ST, and for **anyone at all when `obj.owner is None`**.
  - About 45 view classes list it with no real permission mixin.
- **There is no global login or permission middleware** (`tg/settings/base.py:43-53`).
- **Polymorphic routing uses `DictView` (`core/views/generic.py:43-75`).**
  - It loads the object, reads an attribute (`type` or `creation_status`), and calls `view_mapping[key].as_view()(request, ...)` for both GET and POST.
  - Character, item and location detail URLs (`/characters/<pk>/`, `/items/<pk>/`, `/locations/<pk>/`) go through it.
  - For characters there are two hops. `GenericCharacterDetailView` (`characters/views/core/__init__.py:138`) dispatches on `type` to a per-gameline `*CharacterCreationView` (e.g. `MageCharacterCreationView`, `characters/views/mage/mage.py:1095`). That view dispatches on `creation_status` to a chargen **step view** while `status == "Un"` (`characters/views/core/human.py:653-668`), and otherwise to the detail view.
  - **Neither DictView hop checks permissions.**
- **Templates gate their UI with `is_approved_user`, `is_st` and `owner == user`.**
  - The meaning of `is_approved_user` depends on who set it: the staff middleware, `PermissionRequiredMixin`, `SpecialUserMixin`, or hard-coded True in a few views.
  - Templates only hide buttons; they do not enforce anything.
  - The `core/templatetags/permissions.py` library is loaded by zero templates.
- **Project rule (CLAUDE.md):** reference/game-data models (Clans, Disciplines, Spheres, etc.) are intentionally public with no login required. Player-related objects must require login and permissions.

## Findings

### Critical

1. **Chargen step views are reachable with no authorization. Confirmed.**
   - Any unfinished character's current step is served at `/characters/<pk>/` through the DictView hops above. Many step classes are only `SpecialUserMixin, UpdateView/CreateView`, e.g. `MageFocusView` (`characters/views/mage/mage.py:662`), `MageSpheresView` (`:745`) and `MageRoteView` (`:869`); also `FeraGiftsView`, the Demon ability views and others.
   - Result: anyone, including logged-out users, who knows or guesses a pk can GET and POST the current step of someone else's unfinished character.
   - Permission gating is inconsistent within a single wizard. In the Mage wizard, steps 1, 3, 7, 8 and 10–21 are gated by SPEND_FREEBIES, while steps 2, 4, 5, 6 and 9 are not gated.
2. **Item and location create/update views have no auth. Confirmed for items; Reported for locations.**
   - About 23 update and 22 create views in `items/views/` are plain `MessageMixin, UpdateView/CreateView`, e.g. `items/views/mage/wonder.py:30,40`, `items/views/core/weapon.py:18,32`, material, medium, melee, ranged and thrown; also charm, artifact, grimoire, talisman, periapt, sorcerer_artifact, fetish, talen, hunter gear/relic, treasure, dross, demon relic, bloodstone, and wraith relic/artifact.
   - In `locations/`: TremereChantry, Barrens and City (`locations/views/vampire/__init__.py:241,266,303,331`; `locations/views/core/city.py:18,51`) and `ChantryBasicsView`.
   - The 4 create and 4 update views for Book, HouseRule, Language and NewsItem in `core/views/` are also reported unprotected.
   - About 24 item detail views have no `ViewPermissionMixin`.
   - Most create views never set `owner`, so objects end up with `owner=None`, which `SpecialUserMixin` treats as "everyone is special".
3. **Unauthenticated endpoint that imports arbitrary code. Confirmed.**
   - `widgets/views.py:16-65` (`auto_chained_ajax_view`), auto-mounted at `/__chained_select__/` by `widgets/apps.py:25-45`, takes a GET `form=module.Name` parameter.
   - It calls `importlib.import_module` on it and then **calls `getattr(module, name)()` with no arguments**, with no auth and no allowlist. For example, `?form=os.abort&field=x` would kill the worker.
4. **Owners can approve their own XP and freebie spends. Confirmed by code reading; needs a test.**
   - `Permission.APPROVE` is defined and mapped, but no non-test code checks it.
   - `ApprovalMixin.post` (`core/mixins.py:677-760`) approves or rejects pending spending requests based only on a button value in POST. Its host detail views are gated only by `ViewPermissionMixin` (VIEW_FULL), which owners have.
   - `MageDetailView.post` (`characters/views/mage/mage.py:268-437`) re-implements approval inline with the same gap.
   - `game/views.py` `XPSpendingRequestApproveView` (~:932-965) marks requests approved while bypassing the spending service entirely (Reported).
   - The approve path does not lock the request row (`.get(...)` with no `select_for_update`, `core/mixins.py:~697`; reject does lock), so two concurrent approvals can both apply. Confirmed.

### High

5. **State changes happen before the permission check. Confirmed.**
   - Several step views override `dispatch` on the subclass, and that `dispatch` runs before the permission mixin's `dispatch` in the MRO. It does `obj.creation_status += 1; obj.save()` on a plain GET.
   - Examples: `HumanFreebiesView.dispatch` (`characters/views/core/human.py:518-524`), `HumanLanguagesView.dispatch` (`:537-545`), `GenericBackgroundView.dispatch` (`characters/views/core/generic_background.py:87-95`), and the (unrouted) `ChantryPointsView` / `ChantryIntegratedEffectsView` in `locations/views/mage/chantry.py:216-253`.
6. **Storyteller checks aren't scoped to a chronicle. Reported.**
   - About 10 separate "is ST" checks exist, and most use the global `profile.is_st()`. So an ST of any chronicle can edit any chronicle, scene or journal, and approve XP anywhere.
   - Examples: `StorytellerRequiredMixin` users in `game/views.py` (ChronicleUpdateView ~:1100, SceneUpdateView, StoryXPRequest views, WeeklyXPRequestApprove/BatchApprove) and `ChronicleDetailView.post` story/scene creation (~:246).
   - Contrast `accounts.WeeklyXPApprovalView` (`accounts/views.py:153`), which is properly chronicle-scoped.
7. **Missing object-relationship checks in `game/views.py` POST handlers. Reported.**
   - `SceneDetailView.post` (~:298-344) adds any character without checking that it belongs to the scene's chronicle.
   - `JournalDetailView.post` (~:408-440) doesn't check that the JournalEntry belongs to this journal. It also picks the entry key with `[k for k in POST if "entry" in k][0]`, which matches `submit_entry`.
   - `ChronicleDetailView.post` reads raw `request.POST[...]` without its form (KeyError → 500).
   - `FreebieSpendingRecordUpdateView` (~:1038) lets owners edit already-applied records.
   - ChronicleDetailView, SceneListView, JournalListView and the SettingElement views require only login, with no chronicle-membership check.
8. **Index POST handlers write arbitrary rows and crash. Confirmed.**
   - `ItemIndexView.post` (`items/views/core/__init__.py:181-205`), `LocationIndexView.post` (`locations/views/core/__init__.py:177-201`) and `CharacterIndexView.post` (`characters/views/core/__init__.py:~380-399`) call `ObjectType.objects.get_or_create(name=<raw POST>)`, so any visitor can create DB rows.
   - They only assign `redi` for some gamelines: items and locations handle wod/wta/mta, and characters handle wod/vtm/wta/mta/wto/ctd. Any other gameline raises `UnboundLocalError` (500).
   - `game/views.py` `ChronicleDetailView._get_create_redirect_url` (~:184-213) has the full map; consider reusing it.

### Medium (address in the design, fix as capacity allows)

9. **The list queryset filter disagrees with the per-object check. Reported.**
   - `PermissionManager.filter_queryset_for_user` omits STRelationship storytellers, who do get CHRONICLE_HEAD_ST in `get_user_roles`.
   - It also handles PLAYER and anonymous `visibility="PUB"` differently from the object check.
   - No item or location ListView applies visibility filtering at all.
10. **Owners get a 403 on some of their own chargen steps. Reported.** These steps use `EditPermissionMixin`, which requires EDIT_FULL, and owners don't have it: `characters/views/werewolf/wtahuman.py:349,407`, `changeling/ctdhuman.py:285,343`, `mage/mtahuman.py:636,719`, `changeling/changeling.py:517,573`, `werewolf/fomor.py:301,363`, `demon/demon_chargen.py:185`, `mage/sorcerer.py:791`. The same gap makes the limited-edit (owner) branches of `ItemUpdateView` / `LocationUpdateView` unreachable. Your design must not break owners' legitimate access while closing the holes.
11. **Retire/decease handling in `MageDetailView.post`** (`mage.py:429-434`) skips the owner/EDIT_FULL check that `CharacterDetailView.post` performs (`characters/views/core/character.py:55-77`). Reported.
12. **Untyped `<pk>` URL converters** (116 routes) turn bad input into 500s instead of 404s. Low severity, but cheap to fix if the design touches URL config anyway.

## What the design must deliver

1. **An inventory.** Write a script, and include it in the plan, that walks the URL resolver (`get_resolver().url_patterns`, recursing through includes). For every view it should emit the route, the view class, its MRO-derived gate (which permission, or none), whether it's login-required, and the HTTP methods it accepts.
   - For DictView routers, expand `view_mapping` so every reachable step view appears.
   - Put the resulting table, or a summary with counts plus the full list as an appendix, in the design doc. Classify each view as public-reference, login-only, or object-permission, and give its intended gate.
2. **One mechanism with deny-by-default.** Pick a single way for views to declare their required access, for example:
   - a required `permission_required` / `public = True` class attribute enforced by a base class or middleware;
   - or a check at the DictView boundary.

   Views that declare nothing must be denied, or must fail a test. Justify the choice against the alternatives, including where the gate lives for DictView-routed step views (router, step view, or both).
3. **A route-walking regression test** that fails when any routed view (including DictView-expanded targets) lacks a declared gate, plus targeted tests for each Critical and High finding: anonymous user, other player, ST of a different chronicle, owner, and the chronicle's head ST.
4. **Chargen policy.** Say exactly who may perform each chargen step (the owner via SPEND_FREEBIES? head ST? admin?), and how to keep owners working (finding 10). Mutations must happen only after authorization (finding 5).
5. **Items and locations policy.** Decide who may create and edit shared game-data items that have no owner (Wonder, Weapon, etc.) versus player-owned objects. Decide whether create views must set `owner`. Say what `owner=None` means after the fix, which requires removing or changing `SpecialUserMixin`'s "no owner → everyone" rule. Keep CLAUDE.md's public read access for reference data.
6. **Approval policy.** Enforce APPROVE (chronicle-scoped), lock rows on approve, and route every approval path through the spending services.
7. **Chronicle-scoped ST checks.** Pick one canonical helper (for example, extend `PermissionManager`) and list every call site to migrate. Also propose per-request role caching if it is cheap to add safely.
8. **Widgets endpoint.** Replace dynamic import with an explicit registry or allowlist of chained-select forms. Decide whether it needs login. Check how forms that require constructor kwargs (`user`, `character`) should be handled, or explicitly scope that out.
9. **Index POST handlers.** Stop using `get_or_create` on user input and use one complete gameline → URL map.
10. **A rollout plan** as small, independently shippable PRs ordered by severity. For each PR give the scope, the files touched, the tests added, and the behaviour changes users will notice (for example, "STs of other chronicles can no longer edit chronicle X").
11. **Risks and open questions** for the repository owner, where the answer is a product decision rather than a technical one.

## Constraints

- Design only. Do not modify application code. The only files you create are the two docs, plus the inventory script if you want to commit it under `scripts/`.
- Keep the fix narrow: close the holes and establish the deny-by-default mechanism. Don't refactor the chargen wizard, deduplicate views, or change templates beyond what enforcement requires. A later refactor will introduce a single per-gameline chargen step list and generic step views, so don't build infrastructure that refactor would replace. Do make the permission mechanism something that refactor can reuse.
- Don't rely on templates for enforcement; the server must enforce every check.
- Prefer existing building blocks (`PermissionManager`, `core/mixins.py`) over new libraries.
- Keep the existing test suite passing (`python manage.py test`), and call out any tests that encode the current insecure behaviour and would need to change.
