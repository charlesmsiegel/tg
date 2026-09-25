# Authorization Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a deny-by-default authorization boundary for all project routes, close the confirmed Step 0 holes, provide public/full views for every `core.Model` object, and conceal restricted game records completely.

**Architecture:** One policy declaration and `PermissionManager` evaluator govern all project views. Middleware evaluates direct URL callbacks before dispatch; `DictView` selects a safe public projection or authorized full target before invoking its view. The route-walking inventory and regression test cover included URLs, nested router mappings, public targets and fallback classes. Rollout is staged by module to keep PRs reviewable; the final PR removes temporary legacy fallthrough.

**Implementation note:** The implemented declaration is the explicit class/callback map in `core/route_policy_manifest.py`; `core/access_policy.py` evaluates it and calls `PermissionManager` for object roles. The route regression test compares that map with every reachable URL and router target. The code landed as one worktree change set; the task sections below remain the review and cherry-pick boundaries.

**Tech Stack:** Django 5.2, django-polymorphic 4.1, Django `TestCase`/`TransactionTestCase`, existing XP/freebie services, `scripts/inventory_authorization_routes.py`.

**Spec:** `docs/superpowers/specs/2026-09-25-authorization-hardening-design.md` (read the policy matrix, findings, and owner decisions before changing code).

## Worktree implementation status

The tasks below remain the suggested small PR boundaries. This worktree now contains the integrated implementation: an explicit route policy manifest and middleware, router authorization, public object projections, scoped roles and draft/revision workflow, guarded spending decisions, private record and scene visibility rules, a registered widget endpoint, validated index redirects, and focused regression tests. The tracked `tg_schema` migration adds scene visibility on existing databases; `tg/test_runner.py` handles local apps that still have empty migrations packages in fresh test databases. The route inventory remains a pre-fix baseline, so its old MRO-gate column does not describe the current middleware boundary.

Verification completed so far: 3,178 tests across accounts, core, game, widgets, items, and locations passed with 3 skips. The full suite is running separately; record its final result here before review. This integration has not been split into the PR boundaries below.

## Global Constraints

- Staff may edit any object; `head_st` may manage all gamelines in its chronicle; ordinary STs require an exact chronicle plus gameline `STRelationship`.
- Owners may edit objects they created in `Un` or `Rev`; `Sub` locks editing until a scoped ST or staff returns it for revisions. Owner access does not confer `APPROVE`.
- Self-approval is denied for player characters. A head ST or matching chronicle+gameline ST may approve their own NPC expenditure; staff status alone does not satisfy that exception.
- `owner=None` is shared/unowned, never an implicit edit grant.
- Reference/game-data GET/HEAD stays public. Every `core.Model` object has an anonymous-safe GET/HEAD projection; its full view and every mutation require per-object permission. Journals/spending records and restricted scenes must return indistinguishable 404s to unauthorized callers.
- The server checks before all GET or POST mutations; templates remain presentation only.
- Keep the later chargen step-list/generic-view refactor out of this campaign.
- No new permission library. `PermissionManager` and `core/mixins.py` remain the building blocks.
- Every PR runs its focused tests and `python manage.py check`; the final gate runs `python manage.py test`.

## File Responsibilities

| File | Responsibility |
|---|---|
| `core/permissions.py` | Policy value type, scoped role resolution, status-aware permission, list visibility, and the sole evaluator. |
| `core/middleware/authorization.py` (new) | `process_view` adapter that passes the URL callback and request to the evaluator before dispatch. |
| `core/views/generic.py` | `DictView` calls the same evaluator for a mapped target and class fallback. |
| `core/views/public_object.py` (new) | Renders a safe public projection from an allowlisted value object, never a full model/template context. |
| `core/mixins.py` | Legacy mixin compatibility, scoped checks, and template flag behavior. No second policy engine. |
| `scripts/inventory_authorization_routes.py` | Read-only URL and router inventory; use it to review classification changes. |
| `core/tests/security/` | Route-declaration and policy matrix tests. |
| App views/tests | Explicit declarations, action checks, validated input, and regression cases adjacent to each app. |
| `game/models.py` and `game` migration | Persist the scene read mode with a `CHRONICLE` default; Task 6A handles production schema rollout separately. |

## Review Focus

Each case must become a failing focused test in its owning PR before implementation:

1. An `STRelationship` with the correct chronicle but wrong gameline must not edit or approve a Mage character. PR 3.
2. A submitted object (`Sub`) rejects owner editing, but an authorized ST can return it to `Rev` and the owner can edit/resubmit. PR 2/5.
3. A `DictView` mapped fallback or newly added step with no declaration must fail the route test and deny at runtime. PR 2 and final PR.
4. Two approvals of the same pending request must apply the trait/balance once; SQLite sequential test plus database-specific concurrency test. PR 4.
5. Anonymous GET/HEAD sees the minimal card of a `PRI` object in `Un` and a `PUBLIC` scene, but gets the same 404 as a missing ID for a private journal, spending record or hidden scene; lists and counts reveal none. PR 2/5/6/6B.

## Rollout and Tasks

Each numbered task is a separately shippable PR. Task 0 repairs the pre-existing test database setup so later PRs can use `python manage.py test`. Start with the test shown, observe RED, make the smallest production change, verify focused and affected suites, and include the inventory delta in security PRs. Temporary module fallthrough is allowed only until Task 8; any route declared in an earlier task is enforced immediately. Keep declarations explicit rather than inferring them from `SpecialUserMixin` or class names.

### Task 0: Restore a working fresh test database

**Files:** Create `tg/test_runner.py`; modify `tg/settings/base.py`; add a focused test-runner smoke test under `core/tests/` only if the command-level regression cannot be checked in CI directly.

**Interface:** `TEST_RUNNER` points to a `DiscoverRunner` subclass that, before `setup_databases()`, sets `MIGRATION_MODULES[app_label] = None` only for local installed apps whose importable migrations package contains no migration files. If a real migration file is added later, that app uses migrations normally. Production `migrate` behavior is unchanged.

- [ ] Record RED by running `python manage.py test core.tests.views.test_generic --verbosity 1` on a fresh test database; the first fixture fails with `no such table: accounts_profile`.
- [ ] Add the test-runner setup hook and make it detect empty migrations packages rather than hard-coding a permanent skip. Keep framework and third-party app migrations intact.
- [ ] Run the same command to GREEN, then `python manage.py check` and a small cross-app suite. The one-off diagnostic with `MIGRATION_MODULES=None` for six local apps already passed all 27 `DictView` tests.
- [ ] PR behavior: no web behavior changes; `python manage.py test` can create the local app tables on a fresh test database.

### Task 1: Remove the widget import primitive

**Files:** Modify `widgets/views.py`, `widgets/apps.py` if registration changes, `widgets/widgets/chained.py`, `widgets/fields/chained.py`; create `widgets/tests/test_ajax_authorization.py`.

**Interface:** The `/__chained_select__/` GET callback accepts a registered identifier plus field and parent value, requires login, and resolves only an explicit zero-argument form factory. No arbitrary module import or constructor name comes from the request.

- [ ] Write RED tests: anonymous GET returns 401/login response; `form=os.abort` and `form=os.path` return 400 without calling anything; unknown field/parent returns 400; a registered public-choice form returns normalized choices; POST returns 405. Search templates and field/widget code for every generated `form=` value and record its constructor signature.
- [ ] Implement a literal registry of audited form identifiers and allowed chained fields. For forms needing `user` or `character`, either provide an authorized server-side factory bound to a validated subject or remove that use from this generic endpoint and return 400; do not pass client-selected kwargs. Check errors do not echo import paths or tracebacks.
- [ ] Run `python manage.py test widgets.tests` and `python manage.py check`.
- [ ] PR behavior: anonymous users and unregistered forms stop receiving choices; supported chained selects continue working.

### Task 2: Establish the policy boundary and protect routed chargen

**Files:** Modify `core/permissions.py`, `core/constants.py`, `core/models.py`, `core/views/generic.py`, `tg/settings/base.py`, character router/step and group detail views under `characters/views/`, status-transition code in `characters/models/core/character.py`; create `core/middleware/authorization.py`, `core/views/public_object.py`, its public template, `core/tests/security/__init__.py`, `core/tests/security/test_route_policies.py`, `characters/tests/views/test_chargen_authorization.py`, `characters/tests/views/test_public_object_views.py`; extend `scripts/inventory_authorization_routes.py` to include any class-valued public target.

**Interface:** A class/callback declares a typed `access_policy`. `authorize_access(request, policy, *, subject=None, action=None)` is the sole policy evaluator. A `PUBLIC_OBJECT` GET/HEAD policy yields an allowlisted public projection; `VIEW_FULL` yields the existing full per-gameline detail view. This PR also introduces `Role.CHRONICLE_ST_VIEW` for any ST assigned to the chronicle, `Role.CHRONICLE_ST` for exact chronicle/gameline edit scope, and `PermissionManager.get_scoped_roles(user, chronicle, gameline)` for character policies; Task 3 migrates existing noncharacter callers and adds caching. Middleware applies declarations to direct callbacks before dispatch. `DictView.handle_request()` chooses the current step for a user with chargen authority, read-only full detail for a user with `VIEW_FULL` but no chargen authority, or the public target for everyone else, then invokes the evaluator on the selected class before `as_view()`. An undeclared callback in an enforced module returns 403/404; a new router target without a declaration fails the route test. During rollout, only `characters` and the widget endpoint are enforced modules; later tasks widen the set.

- [ ] Write RED route tests using `get_resolver().url_patterns`, recurse through `URLResolver` and `DictView.view_mapping`, include class fallbacks, and assert a deliberately unannotated fake target fails. The test must check policy attributes exist on the concrete target and are not an inherited default. Compare discovered rows with the script's normalized route/branch/class set. Do not silently skip mapping errors.
- [ ] Write RED request tests for one Mage ungated step and one `EditPermissionMixin` step: anonymous and another player GET the public card from the canonical detail URL, but GET/POST to direct step/full routes deny with unchanged `creation_status`; owner, matching ST, head ST and staff can GET/POST the step while `Un` or `Rev`; a wrong-chronicle ST sees only the public card; a same-chronicle wrong-gameline ST sees read-only full detail at the canonical URL but cannot open or submit a direct chargen step. Repeat a minimal smoke case for Werewolf and Demon. Assert completed/submitted character step POST denies.
- [ ] Write RED public/full tests for a character and a group at each relevant status and both `PRI`/`PUB` visibility values. Anonymous/other player responses contain only `name` and `public_info` plus an approved public image; no stats, notes, owner-only forms, XP/freebie records, private relations or full model in context. Owner/any same-chronicle ST/head/game ST/staff receive the existing full view. POST never inherits the public GET grant.
- [ ] Add the immutable policy declarations, scoped role resolver, public projection view, and middleware, then annotate character/group routes and every reachable child/fallback. The resolver must distinguish head ST, exact chronicle+gameline `STRelationship`, read-only game ST, staff, and owner; test it with a `Gameline` fixture. Build the public context from a field allowlist instead of passing a model instance. Middleware must check `request.method`, load the polymorphic subject, and authorize before a subclass's `dispatch`. Router public/full target evaluation must happen before child `as_view`; existing `DictView` unit tests should cover it. Never use `is_approved_user` as the gate.
- [ ] Add `CharacterStatus.REVISION_REQUESTED = "Rev"` and the explicit `Sub -> Rev -> Sub` workflow using the existing status field. Only scoped ST/staff may return a submitted object for revisions; the owner can edit in `Rev` and resubmit. Extend the router's `Un` condition to include `Rev`. Test forbidden owner self-return and no duplicate spending on revisited steps. Do not add a new schema field for a reason in Step 0.
- [ ] Move `HumanFreebiesView`, `HumanLanguagesView`, `GenericBackgroundView` automatic advancement from GET/dispatch to authorized POST transitions. Check the unrouted Chantry point/effect dispatches for the same problem and cover before any route activates them. Preserve wizard screens and existing step numbering.
- [ ] Run `python manage.py test core.tests.views.test_generic characters.tests core.tests.security`, `python manage.py check`, and the inventory script. PR behavior: every character/group has a public card; full/chargen data remains private; owners stop seeing false 403s on formerly full-edit steps; submitted characters stay locked until an ST returns them to `Rev`; GET no longer advances progress.

### Task 3: Make roles chronicle and gameline scoped

**Files:** Modify `core/permissions.py`, `core/mixins.py`, `accounts/views.py`; create `core/tests/security/test_scoped_roles.py`; update `accounts/tests/views/test_profile_actions.py` and affected `characters/tests`.

**Interface:** All existing object-permission, view-mixin, and account-approval callers use the Task 2 `PermissionManager.get_scoped_roles(user, chronicle, gameline)` implementation. `PermissionManager.user_has_permission()` uses the same scoped roles for an object's `get_gameline()`; a missing or ambiguous `Gameline` mapping fails closed for gameline actions while preserving authorized same-chronicle read. `APPROVE` is granted by admin, head ST, or matching `STRelationship`, never by owner alone.

- [ ] Write RED matrix tests for staff, head ST, matching `STRelationship`, same-chronicle wrong gameline, other-chronicle ST, game ST, owner, and anonymous across `VIEW_FULL`, `EDIT_FULL`, `SPEND_FREEBIES`, `APPROVE`. Include a user who is both owner and ST to pin status precedence.
- [ ] Replace global authorization uses in `StorytellerRequiredMixin`, `STRequiredMixin`, `CharacterOwnerOrSTMixin`, `SpecialUserMixin` and `accounts.views.verify_st_for_chronicle` with the scoped resolver when a subject exists. Task 7 replaces the separate character-template global ST rule with the same scoped object policy. Remove the `owner is None` special-user grant. Context flags derive from evaluated permissions.
- [ ] Cache only the stable scoped role set on the request, keyed by `(user.pk, chronicle.pk, gameline code)`; evaluate owner and status on every permission call. Never use a process-global cache. If an ST relationship changes during one request, explicitly clear that key. Test with `assertNumQueries` around repeated checks and one status mutation.
- [ ] Run `python manage.py test core.tests accounts.tests characters.tests` and `python manage.py check`. PR behavior: an ST from another chronicle loses full access; a same-chronicle ST in another gameline keeps full read but loses edit/approve; a head ST retains chronicle-wide access.

### Task 4: Centralize and serialize approval

**Files:** Modify `core/mixins.py`, `characters/views/mage/mage.py`, `game/views.py`, `accounts/views.py`, `characters/services/xp_spending/base.py`, `characters/services/freebie_spending/base.py` where guard placement is needed; add `game/tests/views/test_approval_security.py`, `characters/tests/services/test_approval_security.py`.

**Interface:** One approval entry function accepts `(request_record, approver, decision)` after resolving the character; it checks `APPROVE`, rejects owner self-approval for player characters, permits it for NPCs only when the approver has head/matching ST scope, locks the pending row within `transaction.atomic`, and calls the matching existing service exactly once. Weekly XP uses its own guarded/locked model approval method.

- [ ] Write RED tests: owner and unrelated player cannot approve/reject from character detail; wrong-chronicle/gameline ST cannot; head ST/matching ST can approve another player's record; player-character self-approval denied even for staff; scoped ST can self-approve an NPC; staff without an ST scope cannot self-approve an NPC; repeated approval does not apply twice; `game.XPSpendingRequestApproveView` changes trait/balance through the service rather than status alone.
- [ ] Replace the duplicate Mage and `ApprovalMixin` approval branches with the shared entry; make all `game` and account approval routes call it or the weekly-specific guarded operation. Use `select_for_update().get(pk=..., approved="Pending", character=...)` inside the transaction for *both* approve and reject. Do not rely on a stale object loaded before the lock.
- [ ] Add a `TransactionTestCase` for sequential replay and a PostgreSQL/MySQL CI test for a true concurrent lock if such a database is available; document SQLite's limitation. Assert a service failure leaves the request pending and balances unchanged.
- [ ] Run `python manage.py test game.tests characters.tests accounts.tests` and `python manage.py check`. PR behavior: approval is limited to the right chronicle/gameline, NPC self-approval works for scoped STs, and double application is refused.

### Task 5: Protect item/location creates, edits, details, and lists

**Files:** Modify ungated classes in `items/views/` and `locations/views/` (especially `core/weapon.py`, `mage/wonder.py`, `core/city.py`, `vampire/__init__.py`, `mage/chantry.py`), shared `item.py`/`location.py` views, forms that expose owner/chronicle/status, `core/permissions.py`; add `items/tests/views/test_authorization.py`, `locations/tests/views/test_authorization.py`.

**Interface:** Every item/location route declares public GET/HEAD, full read, create, or edit policy. Every item/location, including ownerless and `PRI` rows, has the safe public projection at its detail URL; only owner, any same-chronicle ST, head ST, game ST and staff see full details. Player creation sets `owner=request.user`, `status="Un"`; shared creation needs staff or matching chronicle/gameline ST and leaves `owner=None` by deliberate server action. All edits resolve the saved object and apply owner-unapproved or scoped-ST/admin rules. Lists show only safe fields at the viewer's tier.

- [ ] Write RED tests for anonymous and another player GET of public item/location cards, denied full detail and POST; own `Un`/`Rev` item/location full edit; own `Sub`/`App` full-edit denial; matching ST and head ST full read/edit; same-chronicle wrong-gameline ST full read and edit denial; global ownerless write staff-only; chronicle ownerless write matching ST/head/staff only. Test forged `owner`, `status`, and `chronicle` fields and mismatched character ownership/chronicle relationships.
- [ ] Add declarations to every item/location class found by the inventory; use one create helper to validate the intended chronicle/gameline and assign fields server-side. Add the same scoped-ST/staff `Sub -> Rev` return and owner `Rev -> Sub` resubmission transitions for these objects. Remove `SpecialUserMixin` as an enforcement assumption. Fix the full-edit gate that currently blocks the limited owner form; allow only named limited fields after approval if that product rule is approved, otherwise deny.
- [ ] Make item/location list querysets use the shared discoverability filter and render only fields allowed at each row's public/partial/full tier. Test `PRI` direct public card with no list discovery and `PUB` listed public card; compare full-row sets with per-object `VIEW_FULL`. Check Material/Medium and other reference routes remain anonymous GET/HEAD accessible but writes staff-only.
- [ ] Run `python manage.py test items.tests locations.tests core.tests` and `python manage.py check`. PR behavior: every item/location has a public card while full details stay restricted; player creations gain a recorded owner; shared records no longer grant everyone edit access.

### Task 6: Repair chronicle/game authorization and relationships

**Files:** Modify `game/views.py`, related game forms and `core/permissions.py`; add `game/tests/views/test_chronicle_security.py`, `game/tests/views/test_scene_journal_security.py`, `game/tests/views/test_private_records.py`.

**Interface:** A game action resolves a Chronicle or character-derived Chronicle and applies the shared scoped policy. Journals and all spending-record families are visible only to their linked character's owner, authorized ST/game ST, or staff. Scene reads initially use the default chronicle audience; Task 6A persists the other two modes and Task 6B enables them. Unauthorized existing IDs and nonexistent IDs return indistinguishable 404s, and lists/counts omit hidden rows. Scene and Journal writes validate membership and parent-child links.

- [ ] Write RED tests for Chronicle/Scene/Journal/SettingElement lists/details and Story/Week/Scene/SettingElement/XP create/update: anonymous, unrelated player, player in the chronicle, wrong-chronicle ST, correct-chronicle wrong-gameline ST, owner, matching ST, game ST, head ST, staff. A matching ST must not edit another gameline's object. For Journal, JournalEntry, WeeklyXPRequest, StoryXPRequest, XPSpendingRequest and FreebieSpendingRecord, assert unauthorized existing and nonexistent IDs return the same 404 body/status on GET and POST, with no list, count, notification or linked-view disclosure.
- [ ] Write RED POST tests: add an owned character from a different chronicle to a scene; post as a nonmember; submit a journal response for an entry in another journal; send `submit_entry` without an entry ID; omit Chronicle POST `name`, `location`, or date; edit an approved FreebieSpendingRecord. Assert 4xx and no changes, not `IndexError`, `KeyError`, or 500.
- [ ] Replace global `profile.is_st()` checks and Storyteller/OwnerOrST view gates with declared scoped policies. Bind form/queryset subjects to their parent Chronicle; parse journal entry keys exactly and query through the current journal. Filter private-record querysets before lookup, display or counting and return 404 before form validation on forbidden IDs. Validate Chronicle story/scene forms and selected location. Restrict direct spending-record updates to pending records and show applied data read-only. Staff/scoped-ST corrections must use an audited service that reverses and reapplies balances; never reopen raw edits to an applied record.
- [ ] Run `python manage.py test game.tests accounts.tests`, `python manage.py check`, and the route inventory. PR behavior: journals and expenditures reveal no existence to outsiders; chronicle scene access and ST editing are scoped; cross-chronicle scene/journal writes are refused.

### Task 6A: Persist a safe scene visibility default

**Files:** Modify `game/models.py`; add a reviewed `game` schema/data migration and `game/tests/models/test_scene_visibility.py`.

**Interface:** `Scene.visibility` has three exact values: `CHRONICLE` (default), `PARTICIPANTS`, `PUBLIC`. All existing rows and new scenes use `CHRONICLE` until Task 6B enables mode changes. This PR changes no read behavior.

- [ ] Write RED model tests for the exact choices, default and persisted value; add a migration test asserting an existing scene becomes `CHRONICLE`.
- [ ] Design the schema rollout before code: `game/migrations/` is currently empty, so inspect the deployed schema and migration history, establish a safe initial migration/state baseline, then add the visibility column. Verify fresh database creation, upgrade of a copy of the existing database, and rollback. Do not rely on Task 0's test-runner override as the production migration path.
- [ ] Run `python manage.py test game.tests.models`, `python manage.py check`, and migration checks on fresh and copied databases. PR behavior: no visible change; scene mode has a safe persisted default.

### Task 6B: Enforce scene visibility and publishing

**Files:** Modify `game/forms.py`, `game/views.py`, `game/templates/game/scene/` and any scene settings form, `characters/views/core/character.py`, related location scene views, ChronicleDetail scene context and scene list/count selectors; add `game/tests/views/test_scene_visibility.py`.

**Interface:** A shared `can_view_scene(user, scene)` helper resolves staff/head/assigned/game ST, chronicle player, participant, or anonymous according to the spec; mutation checks remain separate and gameline-scoped. `SceneDetailView` permits anonymous GET only for `PUBLIC` and returns 404 for hidden existing or nonexistent IDs.

- [ ] Write RED tests for each mode with anonymous, player from another chronicle, chronicle player who never joined, current/former participant, game ST, wrong-chronicle ST, matching-gameline ST, wrong-gameline same-chronicle ST, head ST and staff. Assert hidden scene direct GET/POST, list, ChronicleDetail count, character/location panels and notifications reveal neither name nor existence. `PUBLIC` allows anonymous GET of scene posts but no POST or private linked records.
- [ ] Implement exact mode choices and one list/detail filtering predicate. Only staff/head/matching scene-gameline ST can change mode. Keep `scene.characters` members after completion so past participants retain access; a removal revokes it. Audit every place a Scene queryset is counted or rendered, including ChronicleDetail, character/location panels and notifications.
- [ ] Run `python manage.py test game.tests characters.tests locations.tests accounts.tests`, `python manage.py check`, and the inventory script. PR behavior: scenes default to chronicle-only read, can be restricted to participants, or deliberately published for anonymous read.

### Task 7: Fix index redirects, reference writes, and template access

**Files:** Modify `characters/views/core/__init__.py`, `items/views/core/__init__.py`, `locations/views/core/__init__.py`, `game/views.py`, `core/views/{book,houserules,language,newsitem,character_template}.py`, `core/forms/character_template.py`, shared redirect utility in `core/` if needed; add `core/tests/security/test_index_redirects.py`, `core/tests/security/test_template_access.py`, update reference tests.

**Interface:** `resolve_create_redirect(object_type, selected_type)` reads an existing `ObjectType` row with matching category, maps supported gameline codes to known namespace prefixes, and returns a route name or controlled 404. It never writes `ObjectType`. Public reference detail/list routes are GET/HEAD only; reference create/update requires staff. Every `CharacterTemplate` has the same public card/full view split as other `core.Model` objects; its export and NPC creation paths never expose full JSON to an unauthorized reader.

- [ ] Write RED tests for unknown `ObjectType`, type/category mismatch, invalid action, every configured gameline, absent route, missing POST key, and anonymous POST; assert the ObjectType row count is unchanged and no input causes a 500. Cover ChronicleDetail's redirect helper too.
- [ ] Replace all four `get_or_create` redirect branches with the shared read-only resolver. Use `settings.GAMELINES` for the code set and an explicit route prefix map; validate `reverse()` for each candidate and convert `NoReverseMatch` to 404. Keep index GET behavior according to its visibility policy.
- [ ] Annotate Book/HouseRule/Language/NewsItem and all remaining reference models: anonymous GET/HEAD on read routes, staff-only create/update/delete. Update any insecure existing tests that expect authenticated nonstaff reference writes.
- [ ] Replace the global ST template gate with explicit per-action policies. Test anonymous and unrelated-player public template detail with no JSON fields, owner full read and `Un`/`Rev` edit, `Sub` edit denial, same-chronicle ST/head ST full read and gameline-scoped management, other-chronicle ST public-card-only read, and staff management. Templates without a chronicle have no ST edit scope. Constrain template export, import and NPC creation to their own policies; validate the destination character's chronicle/gameline before applying a template. `is_public` controls listing, not the minimal detail card or full-data reuse; reuse requires an authorized action.
- [ ] Run `python manage.py test core.tests characters.tests items.tests locations.tests game.tests` and `python manage.py check`. PR behavior: unknown selection receives a 4xx, reference editing is restricted to staff, and template cards become public while full data stays scoped.

### Task 8: Turn on project-wide deny by default and verify parity

**Files:** Modify `core/middleware/authorization.py`, `core/permissions.py`, `core/tests/security/test_route_policies.py`, remaining project view declarations in `characters/views/`, `items/views/`, `locations/views/`, `game/views.py`, `accounts/views.py`, `core/views/`, `widgets/views.py`; optionally modify URL converters in each app's `urls.py`.

**Interface:** Every project callback and every reachable DictView target has an explicit typed policy; `None` denies at runtime. The route test includes all project modules, checks accepted methods, and retains only named framework exclusions. No temporary module fallthrough remains.

- [ ] Run `scripts/inventory_authorization_routes.py` and classify every remaining `none` or `function/unknown` project row, including class fallbacks and direct step routes. Add declarations to concrete views; keep public references explicit. Record policy-family totals in the PR.
- [ ] Write RED tests that add a synthetic unannotated direct URL, an unannotated mapped child, and an unannotated `public_view_class`; all must fail the route test and deny at runtime. Test a declared public reference, a `PRI` direct public card, a protected full projection, a login-only collection, and action-specific POST through middleware and router.
- [ ] Iterate every concrete `core.Model` subclass and assert its instances have a canonical public GET/HEAD detail route. Cover character, group, item, location and character-template families with distinct full-only sentinel fields; fail if any subclass falls through to a raw detail template or has no route.
- [ ] Remove rollout exemptions. Run a mixed fixture comparing list discoverability and rendered public/partial/full fields with the evaluator for anonymous, owner, observer, player, game ST, matching ST, head ST and staff. Repair discrepancies before merge.
- [ ] If editing URLconfs, replace untyped `<pk>` with `<int:pk>` only for integer-PK models; add a malformed-ID 404 test. Do not change noninteger converters blindly.
- [ ] Run `python manage.py check`, `python manage.py test`, and the inventory script. Review each changed behavior against the spec and baseline appendix. PR behavior: newly added project endpoints are denied until explicitly classified.

## Existing Tests and Data Checks

The repository already has `core/tests/views/test_generic.py`, `core/tests/views/test_reference.py`, `game/tests/views/test_views.py`, app-specific character/item/location suites, and `widgets/tests/test_chained_select.py`. Revise tests that assert the old global-ST, owner-403, anonymous *full* player-data, or unrestricted reference-write behavior. Preserve tests that assert a safe public card, and do not weaken tests that enforce object ownership. Add a read-only management/shell report in Task 5 or Task 4 to count legacy `owner=None` player objects and approvals marked approved without service effects; do not auto-rewrite ambiguous rows.

The current design branch used `C:/Users/charl/github/tg/.venv/Scripts/python.exe` (Django 5.2.17) for the inventory. `pip install -r requirements.txt` in the active interpreter failed because network sockets were blocked. Unmodified `python manage.py test core.tests.views.test_generic` fails before tests reach view code because fresh test databases lack `accounts_profile`; the temporary empty-migrations override passed all 27 tests. Task 0 repairs that baseline. Engineers may use the project virtualenv or install from requirements in an environment with package access.

## Handoff

Read the spec's open decisions before Task 5. Keep each PR independently deployable, with its own failing regression and focused verification. Task 8 is the required final gate; earlier temporary rollout exceptions are implementation staging, not accepted final behavior.
