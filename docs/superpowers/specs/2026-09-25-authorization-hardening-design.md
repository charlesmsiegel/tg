# Authorization Hardening Design

## Goal

Close the Step 0 authorization and input-handling holes without rebuilding the character creation wizard. Every project-owned route, including a target reached through `DictView`, must declare a server-enforced access policy. Every `core.Model` object has a minimal public read view and a full view for its owner, correctly scoped STs, and staff. Staff can edit any object. A head ST can manage every gameline in their chronicle; another ST can edit only objects in the chronicle and gameline of their `STRelationship`. A player can edit an object they created while its status is `Un` or `Rev` (returned for revision). Reference/game-data reads such as Clans, Disciplines and Spheres remain public.

This document records the agreed design and the pre-fix route inventory. The accompanying implementation is in this worktree. The inventory appendix describes the original mixin gates; the runtime boundary now uses the explicit manifest in `core/route_policy_manifest.py`, enforced by `AuthorizationMiddleware` and `DictView`. The public detail exception applies to `core.Model`; journals, spending records and restricted scenes do not reveal their existence to unauthorized callers.

## Evidence and Scope

Read `CLAUDE.md`, both existing specs and plans in `docs/superpowers/`, `core/permissions.py`, `core/mixins.py`, the routers, the named handlers, model relationships, services, and settings. The three requested repository skills (`.claude/skills/tg-permissions/SKILL.md`, `model-standards/SKILL.md`, `tg-testing/SKILL.md`) are absent from this worktree and the parent checkout. The root `CLAUDE.md` remains the repository guidance. The supplied audit is the discovery list; source inspection below distinguishes independently confirmed findings.

`scripts/inventory_authorization_routes.py` recurses from `get_resolver().url_patterns`, expands class-valued `DictView.view_mapping` branches and class fallbacks, and emits route, branch, class, current MRO gate, whether that gate rejects anonymous requests, accepted methods, and proposed policy family. It is read-only and does not need the database. In the initial Django 5.2.17 inventory, the development URLconf produced **2,569 rows**: **1,831 direct URL patterns** and **738 expanded router targets**. Of those rows, 1,088 were framework-owned (admin, debug toolbar, auth, media), leaving **1,481 project-owned rows**. Baseline MRO counts over all rows: 875 no gate, 895 function/unknown, eight `AjaxLoginRequiredMixin`, 113 `LoginRequiredMixin`, 157 `VIEW_FULL`, 97 `EDIT_FULL`, 400 `SPEND_FREEBIES`, 16 global `StorytellerRequiredMixin`, six `CharacterOwnerOrSTMixin`, and two `OwnerRequiredMixin`. Of the project-owned rows, **681 showed no MRO gate**. The baseline policy-family column was a review aid rather than an automatically approved declaration.

After implementation, the same script reports **2,575 rows**, including **1,487 project-owned rows** and **975 distinct project targets**. All 975 targets have explicit entries in `core/route_policy_manifest.py`, and the resolver regression test reports zero undeclared targets. The largest policy groups are 234 chargen steps, 125 public reference views, 120 staff-only reference writes, 103 object details, 102 object writes, and 82 object creates. The MRO gate column remains useful historical evidence but does not show the new middleware gate; the `Declared policy` and `Effective login policy` columns do.

The proposed inventory buckets are **1,303 object-permission**, **143 login-only**, and **35 public-reference** project rows; the other **1,088** are framework-owned exclusions. These are review buckets, not runtime policy defaults. The script reports 284 expanded project routes containing untyped `<pk>`; this exceeds the audit's source-route estimate because includes create multiple resolved patterns. Function-view methods are marked `ANY*`: decorators and wrappers need manual inspection. `Login enforced by MRO` means anonymous is rejected by that MRO gate, not that a `LoginRequiredMixin` is literally present. A `VIEW_FULL` gate does reject anonymous under today's role matrix.

### Finding disposition

| Finding | Disposition and evidence |
|---|---|
| 1 chargen | Confirmed: `GenericCharacterDetailView` forwards to `*CharacterCreationView`, then to step classes such as `MageFocusView`; neither router checks permission and several steps inherit only `SpecialUserMixin`. |
| 2 items, locations, core writes | Confirmed: `WonderCreate/Update`, `WeaponCreate/Update`, `CityCreate/Update`, `TremereChantryCreate/Update`, `BarrensCreate/Update`, and Book/HouseRule/Language/NewsItem writes have no gate. Item/location detail mappings include ungated views. The common `Model.owner` is nullable and only a few create views set it. |
| 3 widget import | Confirmed: `widgets.views.auto_chained_ajax_view` imports a client-supplied module and calls its selected attribute with no arguments. `widgets.apps` mounts it at `/__chained_select__/`. `os.abort` is a valid illustrative payload; do not execute it in tests. |
| 4 approval | Confirmed by code reading: `ApprovalMixin.post` and `MageDetailView.post` do not check `APPROVE`; their approve lookup has no row lock. `game.views.XPSpendingRequestApproveView` saves approval fields without applying the spending service. A behavioral regression test is required before the fix. |
| 5 pre-gate writes | Confirmed: `HumanFreebiesView`, `HumanLanguagesView`, `GenericBackgroundView` and unrouted Chantry step dispatch methods save progress before an inherited permission dispatch. |
| 6 global ST | Confirmed: `StorytellerRequiredMixin`, `CharacterOwnerOrSTMixin`, `SpecialUserMixin`, several `game.views` branches and template flags call global `profile.is_st()`. `STRelationship` has both `chronicle` and `gameline`, which most checks ignore. `accounts.views.verify_st_for_chronicle` is chronicle-scoped but still ignores gameline. |
| 7 relationship and POST | Confirmed: Scene add-character checks owner but not matching chronicle; Journal response looks up an entry by a broad POST-key substring and does not bind it to this journal; Chronicle POST reads required keys raw; `FreebieSpendingRecordUpdateView` has no pending-only filter. Chronicle/Scene/Journal/SettingElement lists and details are primarily login-only. |
| 8 index POST | Confirmed: the three index handlers call `ObjectType.objects.get_or_create` with raw POST data and have incomplete gameline redirect branches. `ChronicleDetailView._get_create_redirect_url` has a fuller map but also does `get_or_create`, so it is not safe to reuse unchanged. |
| 9 queryset mismatch | Confirmed: `_build_chronicle_st_filters` includes head and game ST but omits `chronicle__storytellers`; its approved-player and anonymous `PUB` logic differs from `get_user_roles`. Item/location lists are not uniformly filtered. |
| 10 owner 403 | Confirmed by role matrix and MRO: OWNER has `SPEND_FREEBIES` and `EDIT_LIMITED`, not `EDIT_FULL`; the named steps with `EditPermissionMixin` deny an owner without an additional role. `ItemUpdateView` and `LocationUpdateView` place limited-form selection behind that full-edit gate. |
| 11 Mage retire/decease | Confirmed: `MageDetailView.post` writes `Ret`/`Dec` without the check present in `CharacterDetailView.post`. |
| 12 untyped pk | Confirmed in the URL inventory. Address opportunistically after security PRs; it is not an authorization substitute. |

No failing tests were added to this design-only branch. The plan requires each exploit to be captured as a failing behavioral test before its PR changes production code.

### Test baseline limitation

Unmodified `python manage.py test core.tests.views.test_generic` currently fails all 27 tests during fixture setup with `no such table: accounts_profile`. The six local apps (`accounts`, `core`, `characters`, `items`, `locations`, `game`) each have an importable, empty `migrations/` package. `MigrationLoader(None)` classifies `accounts` and `core` as migrated with zero migration files, so Django's fresh test database does not synchronize their tables. A one-off test run that sets `MIGRATION_MODULES[app] = None` for these six apps before `call_command("test", ...)` passes all 27 tests. The rollout therefore starts with a narrow test-runner correction that only treats an app as unmigrated when its migrations package has no migration files. This is pre-existing infrastructure breakage, not a security regression.

## Approaches Considered

### 1. Add permission mixins to every view

This reuses `core/mixins.py` but is not deny by default, can be bypassed by a subclass `dispatch`, and does not guard `DictView.as_view()` handoffs. Rejected as the primary mechanism.

### 2. Gate only at the three polymorphic routers

This cheaply blocks the most severe character, item and location detail routes. It does not cover direct step URLs, create/update routes, game handlers, function views, or future routes. Use router validation as one part of the selected design, not as the sole mechanism.

### 3. Declare policies on views and enforce them at routing boundaries (chosen)

Add a small policy declaration and evaluator using `PermissionManager` for role checks, enforced by a project `process_view` middleware before any view's `dispatch` or handler. A `DictView` handoff invokes the *same evaluator* on its selected target before calling `as_view()`, because Django middleware is not re-entered for that internal call. The router itself declares a policy and is checked before it reads or dispatches an object. The route-walking test requires a declaration on every project-owned class target and function callback, including nested mappings and fallbacks. This provides one rule model and covers the pre-dispatch mutation hole. It remains reusable when the future wizard step list replaces today's mappings.

**Implementation choice:** The declarations live in `core/route_policy_manifest.py`, keyed by the concrete view class or callback's import path. `scripts/build_route_policy_manifest.py` regenerates the reviewed map from the URL inventory; the route test requires an exact match between reachable targets and declarations. `core/access_policy.py` is the single route evaluator and delegates role decisions to `PermissionManager`. Middleware and `DictView` call that same evaluator. This avoids editing hundreds of reference views merely to add a class attribute, while an undeclared new target still fails closed at runtime and in tests.

## Policy Contract

Use a deliberately small set of immutable declarations, for example `access_policy = PUBLIC_REFERENCE | LOGIN | object_policy(Permission.X, subject=...) | create_policy(...)`. The names are illustrative; implementation must keep one canonical type and evaluator. A policy specifies allowed HTTP methods, how to load its subject from URL or related object, and whether a request is a read or mutation. `None` or an unknown policy **denies in production** and fails the route test. Never infer safety from `SpecialUserMixin`, a template flag, a form, or a successful GET.

The middleware covers project callbacks under `core`, `characters`, `items`, `locations`, `game`, `accounts`, and `widgets`. Framework callbacks from Django admin/auth, debug toolbar, and static/media serving are named exclusions with their framework's own authorization; do not exempt a project callback merely by URL prefix. Existing Django auth views under `/accounts/` are framework callbacks. For function views, attach the policy to the final callable in the URLconf and test that decorators preserve it. Middleware checks method before evaluating a subject; unsupported methods return 405. Anonymous denial uses 401 JSON for AJAX or login redirect for interactive actions, while denied full/private object reads return 404 and mutations return 403. A declared public-object GET/HEAD returns the minimal public projection instead of a denial. Missing or malformed `pk` returns 404/400, never 500.

An object policy resolves the *actual polymorphic object* and its `owner`, `chronicle`, status, and `get_gameline()`. Related records (XP requests, journals, scenes) resolve their character/chronicle before checking. A create policy gets the intended chronicle and gameline from validated URL/form choices, then sets owner and chronicle server-side as appropriate. Client-provided `owner`, `chronicle`, approval fields, and `status` are never accepted as authority. Policies for mixed GET/POST detail views declare an action per POST branch, and each branch calls the evaluator again at its mutation point if it needs a stronger permission than page viewing. A valid public or full page view is never evidence of permission to approve or retire.

### Public and full views of game objects

Use two **server-selected read projections** for every `core.Model` object, including characters, groups, items, locations, and character templates. The canonical detail URL remains stable where one exists; any remaining concrete `core.Model` subclass needs a canonical public detail route. GET/HEAD returns a minimal public projection to anyone, including anonymous users, at every status (`Un`, `Rev`, `Sub`, `App`, `Ret`, `Dec`). The public template receives only a safe projection of explicitly public fields: `name`, `public_info`, and a reviewed image only when its image approval state permits public display. It must not receive the full model instance, stats, XP/freebie records, notes, unpublished relations, or full-template context. Existing character `not_owner.html` shows more fields and is therefore a source to review, not an automatic safe-field list. Owner, chronicle head ST, any ST assigned to that chronicle, assigned read-only game ST, and staff GETs render the existing full per-gameline detail view, with the complete object context. A user with only `VIEW_PARTIAL` receives the public projection until a separately reviewed partial-field contract exists. The full-view decision uses `VIEW_FULL`, not `is_approved_user`: an owner retains the full sheet while `Sub`, `App`, `Ret`, or `Dec` even when editing is locked. Thus the public and full views can share a URL without relying on template flags to conceal private context.

`visibility` and `display` may control list discovery and optional extra partial fields, but do not remove the minimal public detail projection. A private (`PRI`) object can have an unlisted yet directly reachable public card; its full view remains private. This public card is the user-requested exception to `CLAUDE.md`'s general login rule for player-related objects; all writes, chargen steps, full reads, journals and approval data still require authorization. The `DictView` first hop must choose the public projection **before** forwarding an unauthorized GET into a chargen step. Its mapped target and any class-valued public target are checked by the same evaluator and enumerated by the route test/inventory. Direct per-gameline detail URLs make the same public/full selection. Public object detail is GET/HEAD only; POST never inherits the public read grant. Route/model coverage checks iterate concrete `core.Model` subclasses: each needs a canonical public detail route, including `CharacterTemplate` with a minimal projection and no export data. A template's `is_public` controls list discovery, not existence of its safe public card or access to its full JSON data. Its owner receives full read; template creation, update, delete, export, import and NPC creation need an explicit action policy, with staff, head ST and matching chronicle/gameline ST authority and owner editing only in `Un`/`Rev`. A template without a chronicle has no ST edit scope.

### Private journals, spending records, and scenes

Journal, JournalEntry, XPSpendingRequest, FreebieSpendingRecord, WeeklyXPRequest and StoryXPRequest records have **no** public projection. Their owner is the linked character's owner; read access belongs to that owner, the chronicle head ST, any ST assigned to the chronicle, a read-only game ST assigned to the chronicle, and staff. Mutations still require their stronger action-specific policy. A caller without read access, including anonymous users and a player in the same chronicle who does not own the character, receives the same 404 for an existing or missing ID. All lists, dashboard counts, linked-object summaries and search results omit unauthorized records before rendering; a forbidden POST with a known ID also returns 404 before form validation or side effects. No redirect, message, count, differing error body, or related-object link may confirm existence.

Scene visibility is a separate three-state rule, stored on `Scene` with a safe `CHRONICLE` default for existing rows:

| Scene read mode | Who can GET/HEAD and discover it | Who may change the mode |
|---|---|---|
| `CHRONICLE` (default) | Owners of any character in the chronicle; its head ST, assigned STs, game STs; staff | Staff or the head/matching gameline ST |
| `PARTICIPANTS` | Players who own a character in `scene.characters` (past or current participants); chronicle head/assigned/game STs; staff | Staff or the head/matching gameline ST |
| `PUBLIC` | Everyone, including anonymous users | Staff or the head/matching gameline ST |

For scene **editing**, ordinary STs still need the exact scene chronicle plus `Scene.gameline` relationship; head ST and staff can edit. A player's scene POST must additionally use their own character that belongs to the scene and chronicle. `PUBLIC` grants read only, never posting, character enrollment, closing, XP awards, or mode changes. A participant-only scene keeps its `scene.characters` membership after completion so past players retain read access; if a participant is removed, access ends unless a separately recorded attendance relation is introduced later. The response for a forbidden scene ID is the same 404 as a missing one, regardless of method. Filter `SceneListView`, ChronicleDetail's scene context, related location/character scene panels, search, notifications and counts by this rule; a hidden scene's name or count must not leak through another page. Fully public scenes may show their scene content and posts to anonymous users, but never a linked private journal or spending record.

`Scene` has no visibility field today. The scene-mode PR must add a real persisted field, a safe default/data migration for existing rows, and a reviewed database rollout. The local apps' empty migrations packages make migration bootstrapping a technical prerequisite; the test-runner workaround in Task 0 does not replace production migration planning. Keep this schema change in its own PR so it can be reviewed and deployed before the mode-selecting UI.

### Roles and status rules

`PermissionManager` remains canonical. Add one scoped role resolver for `(user, chronicle, gameline)` and use it throughout: staff/superuser get ADMIN; chronicle `head_st` gets `CHRONICLE_HEAD_ST` across every gameline in that chronicle; an `STRelationship` grants a `CHRONICLE_ST_VIEW` role for full read of objects and private records in its chronicle, plus a separate `CHRONICLE_ST` edit/approve role only when the gameline also matches; `game_storytellers` remain read-only. Only the latter role receives edit/approve permissions. Normalize a model's code (`get_gameline()`, such as `mta`) to the `Gameline` row representing the corresponding configured name; test missing/duplicate/mismatched rows and fail closed for gameline actions while retaining authorized same-chronicle read. `chronicle=None` has no ST scope; staff may act, and an owner may act within owner rules. This explicit gameline rule supersedes today's `Role.CHRONICLE_HEAD_ST` grant to every `chronicle.storytellers` member.

Staff may edit all mutable objects. A player may fully edit an object with `owner == user` and `status in {"Un", "Rev"}`, including its current chargen step, without gaining `EDIT_FULL` on other people's objects or on approved objects. `Sub` locks owner editing while awaiting review. On `App`/`Ret`/`Dec`, owner editing is denied; any legacy limited form that permits post-approval changes must be reviewed as a separate product rule and remains closed in Step 0. The policy evaluator must give a scoped ST/admin role precedence over owner status restrictions, so an ST who owns an object does not lose legitimate ST authority because `Role.OWNER` is also present. `EDIT_LIMITED` remains a separate field-level form policy, not a way to submit full edit forms. `APPROVE` never follows from OWNER or `VIEW_FULL`.

Add `CharacterStatus.REVISION_REQUESTED = "Rev"` to the common `Model.status` choices and an explicit transition `Sub -> Rev` initiated only by a scoped ST or staff. `Rev -> Sub` is the owner's resubmission, which locks edits again. Do not let an owner self-return a submitted object to `Un` or `Rev`. `Rev` is still unapproved, but existing XP/freebie records and point balances must not be replayed by revisiting a chargen step. Extend status validators and status displays to make the transition usable. Use the existing status field; a persisted reason or new audit model is outside Step 0 unless the owner explicitly requests it.

### Chargen and character detail

For *every* current chargen step: the owner may GET/POST only while the character is `Un` or `Rev`, via the chargen action (`SPEND_FREEBIES` or a named equivalent bound to those statuses); staff and the scoped ST may GET/POST in those statuses; unrelated players, anonymous users, observers and STs assigned only to other chronicles are denied **from the step and full sheet**, while their GET/HEAD of the canonical detail URL receives the public projection. An ST assigned to this chronicle but another gameline sees the full sheet and is denied step mutations. No step may accept `Sub`, `App`, `Ret`, or `Dec`. The second router currently routes steps only for `Un`; extend that condition to `Rev`. This includes Mage steps 2/4/5/6/9 and the presently `EDIT_FULL`-gated Werewolf, Changeling, Mage, Demon and Sorcerer steps. Do not grant OWNER global `EDIT_FULL` just to make those steps work. For `Un`/`Rev`, `GenericCharacterDetailView` sends a user with chargen authority to the current step, a user with `VIEW_FULL` but no chargen authority to the read-only full detail, and everyone else to the public projection. The second router checks before the step hop; direct step GET/POST also require chargen authority through middleware. Authorized complete-character detail uses `VIEW_FULL`. List summaries render only public fields for anonymous or partial viewers; full detail templates remain `VIEW_FULL`.

Move automatic wizard skipping/progress increments out of `dispatch` and GET. After authorization, a valid POST may advance within a transaction; a GET is read-only. If a step is inapplicable, GET may redirect to another authorized step without saving, with the transition persisted only by an authorized explicit POST or a safe server-side transition after a prior POST. Add a test that anonymous/other-player GET and POST leave `creation_status`, child rows, and audit fields unchanged. Apply the same rule to the unrouted Chantry views before routing them.

Character detail POST branches: XP spending requires `SPEND_XP`; approvals and denials require `APPROVE`; retire/decease require owner or scoped ST/admin permission as the existing character transition rule intends. `MageDetailView` must use the same checks as `CharacterDetailView` and may keep its specialized form handling. Character detail view permission alone never authorizes POST.

### Items, locations, and reference data

For `ItemModel`/`LocationModel` and subclasses, `owner=None` means **shared, unowned data**, never an implicit edit grant. A player creation path sets `owner=request.user` server-side, starts at `status="Un"`, and validates any selected chronicle. Staff may create shared objects globally or in a chronicle; a scoped ST may create a shared object only in their chronicle and gameline. If the create URL has no chronicle, an ST must choose one through a validated form before save; there is no global ST fallback. If an item/location belongs to a character, validate the `owned_by`/location relationship and chronicle against that character. Owner edits of `Un`/`Rev` objects use the full form; `Sub` locks owner edits; approved objects deny owner editing; a future limited-edit form requires an explicit product decision. Staff or an ST with the matching chronicle/gameline may edit the full form regardless of status. Server-side assignment prevents forged `owner=None`, `chronicle`, `status`, and gameline changes.

Reference model GET/HEAD views (Clan, Discipline, Sphere, Book, HouseRule, Language, Material, Medium and similar lookup records) explicitly declare `PUBLIC_REFERENCE`; reference writes require staff, unless a specific chronicle-scoped SettingElement is tied to a chronicle and its scoped ST. This preserves `CLAUDE.md`'s public reads. Item/location lists use a public-safe row projection for anyone allowed to discover a row, and a full row only for a full-view role. Ownerless and player-owned item/location detail both have the minimal public projection; full detail follows the owner/chronicle/gameline rule. `PUB`, `PRI`, `CHR`, `CUS`, and `display` govern discovery or optional additional visibility, never full edit and never whether the direct minimal card exists. Remove `SpecialUserMixin.check_if_special_user`'s `owner is None -> True` behavior and set `is_approved_user` from the server policy result for template compatibility. Template flags remain presentation hints.

`PermissionManager.filter_queryset_for_user` must be equivalent to per-object view checks **at the list's rendered tier**: include any same-chronicle `STRelationship` for full read and exact chronicle/gameline relationships for mutation, and honor head ST and game ST view roles, and align `PUB`/player/observer discovery with the public/partial/full field projection. Test set equality on a mixed fixture; add filter use to item/location lists and game lists. A direct minimal public detail URL may be reachable even when a `PRI` object is undiscoverable in a list. Never rely on filtering alone for full detail authorization.

### Approvals, game relationships, and input

All approve/reject entry points (`ApprovalMixin`, Mage inline POST, `game.XPSpendingRequestApproveView`, freebie and XP account endpoints, and weekly/story XP handlers) resolve the request's character and call one guarded approval service. The service checks `APPROVE` against that character's chronicle/gameline. If `character.owner_id == approver.pk`, it denies self-approval for player characters. It permits self-approval only when `character.npc is True` **and** the approver is the chronicle head ST or a matching chronicle+gameline `STRelationship` ST; staff status alone does not satisfy this exception. Inside `transaction.atomic`, select the *pending request* with `select_for_update`, verify the pending state again, apply/deny with the existing XP/freebie service, and commit its status/trait/balance effects once. For weekly XP, use its existing model/form approval operation behind the same scoped check and locking contract; do not route it through the character-spending service if its data model differs. Repeated or concurrent requests are idempotent. SQLite cannot prove row-lock semantics; use a transaction-capable database test for concurrency, plus deterministic sequential tests everywhere.

Migrate `StorytellerRequiredMixin`, `STRequiredMixin`, `CharacterOwnerOrSTMixin`, `SpecialUserMixin`, `accounts.views.verify_st_for_chronicle`, and `game.views` ST branches to the scoped resolver. Specific call sites: ChronicleDetail POST story/scene creation; SceneDetail close/post/add-character; JournalDetail ST response; Story, Week, SettingElement, StoryXPRequest, Chronicle, Scene create/update; WeeklyXPRequest single/batch approve; XPSpendingRequest approve/update; FreebieSpendingRecord detail/update; the game list/detail context flags. `core.views.character_template.STRequiredMixin` is currently global and must be replaced by the template's scoped action policy; there is no global ST exception. Direct `profile.is_st()` calls in companion and Demon/Vampire chargen context flags must derive from the scoped object. Keep the profile method for dashboard purposes, not authorization.

Scene add-character must require `character.chronicle_id == scene.chronicle_id`; posting must also use a scene member from that chronicle. Journal responses must parse one exact `entry-<positive integer>-st_message` key, fetch the entry through `self.object.all_entries()`, and require scoped ST authorization for that journal's character. Invalid or ambiguous keys return a form error/400 after the journal itself is authorized. Chronicle story/scene creation uses validated forms and checks the selected location's chronicle. `FreebieSpendingRecordUpdateView` and XP spending update views restrict direct editing to pending records and cannot mutate an already applied spend. Staff and scoped STs may correct an applied expenditure only through a separate audited reversal/reapplication service, preserving balances and approval history; direct field editing is never a valid correction. Chronicle/SettingElement views retain their own chronicle policies; Scene views use the three-state rule; Journal and spending views use the linked-character private rule. `LOGIN` alone is insufficient for any of these restricted records.

The widget endpoint becomes GET-only, login-required, and backed by a static mapping of audited form identifiers to *zero-argument* form factories and allowed chained fields. No client-supplied import path is ever imported. Unknown form/field/parent values return 400 without echoing internal exceptions. Forms requiring `user` or `character` kwargs are excluded in this PR until an explicit factory can derive the subject from a validated URL and authorize it; the existing uses must be searched and either migrated to a supported factory or disabled with a clear 400. Never instantiate arbitrary classes from a query parameter.

All four creation redirects (`CharacterIndexView`, `ItemIndexView`, `LocationIndexView`, ChronicleDetail) use one `ObjectType` lookup filtered by expected type and one complete `settings.GAMELINES` code-to-namespace map. Unknown type/action/gameline returns 400 or 404 without creating data. Redirects to create routes require login; index/list navigation may remain public only where the target is public. Avoid passing raw type names into arbitrary route names. Use validated keys from seeded `ObjectType`, and test all configured gamelines including `dtf`, `htr`, `mtr`, and `orp` where a route may be absent (controlled 404).

## Regression Contract

Route-walking test recurses `URLResolver` and every `DictView` mapping/fallback, checks every project callback has an **explicit** policy (not inherited merely from a generic `View`), checks only approved framework exclusions, and verifies the declared method set covers accepted methods. It fails on any new unclassified route or new step. Include the full appendix output in code review when mappings change.

Behavioral matrix for each sensitive operation: anonymous, unrelated player, player in same chronicle, scene participant, ST of different chronicle, ST of correct chronicle but wrong gameline, owner, matching ST, game ST, head ST, and staff. Test GET, valid POST, malformed POST, and unchanged database state after denial. Cover representative Mage/Werewolf/Demon steps; all step classes are covered by the route policy test. Iterate every concrete `core.Model` subclass to verify that a canonical public detail route exists. Pin the two read projections for every `core.Model` family, including character templates: anonymous and unrelated users receive only the public card, while owner, any ST assigned to that chronicle, head ST and staff receive the full view; STs assigned only to another chronicle receive the public card. Assert full-only fields are absent from both response content and public template context for `PRI` and `PUB` objects in every status. For journals and every spending-record family, assert unauthorized existing and missing IDs have identical 404 responses, and list/count/linked views reveal neither. Test all three scene modes for the same audience matrix, including a former participant and a nonparticipant player, plus public read with denied public POST. Also cover public reference anonymous GET; shared ownerless edit denial; player `Un`/`Rev` edit and `Sub`/`App` denial; ST gameline boundaries; NPC-only ST self-approval; simultaneous approval; and mismatched Scene/Journal object IDs. Existing tests that expect global ST access, owner 403 in chargen, unfiltered lists, full player data for anonymous users, or approval through a detail view's `VIEW_FULL` must be updated to the new rule rather than retained as compatibility tests.

## Risks and Product Decisions

- **Confirmed head ST scope:** `head_st` covers every gameline in its chronicle; ordinary STs can read across their chronicle but require exact chronicle + gameline to edit or approve.
- **Confirmed self-approval exception:** an ST may approve their own NPC expenditure only with matching ST scope; no one may self-approve a player character expenditure.
- **Unowned legacy rows:** existing `owner=None` item/location records need a one-time inventory to distinguish intended shared content from player creations that lost ownership. Do not assign an owner by guess; fail closed for edits until classified.
- **Limited edits after approval:** identify the exact approved-item/location fields owners may change. Until specified, permit no owner update to `App` objects; do not expose the full form.
- **Revision explanation:** the `Rev` state works without a new schema field. Decide later whether an ST must provide a persisted reason and where it should be shown.
- **Public fields and discovery:** this design exposes only a minimal card (`name`, `public_info`, reviewed image) at every status, including `Un`, and lets `visibility`/`display` control list discovery. Review whether `description`, owner name or chronicle name should be added to the card; do not copy full templates until each field is approved for public use.
- **Legacy template workflows:** template management currently uses a global ST check and `is_public` for discovery. Review whether an unscoped template should be assigned to a chronicle; until then only its owner in `Un`/`Rev` or staff may edit it, and only staff may approve or publish it. A scoped ST's NPC-creation action must use a template in the same chronicle/gameline.
- **Scene attendance:** `Scene.characters` is the available participation record. Removing a character removes participant-only access even if they played earlier. A distinct attendance history needs a separate product decision and schema change.
- **Public scene content:** `PUBLIC` exposes scene posts and linked public object cards to anonymous readers. Review any existing scene template include that queries private journals, XP or storyteller-only notes before enabling the mode.
- **Scene migration:** production databases need a safe schema rollout for `Scene.visibility` despite the local apps' empty migrations packages. Task 6A gates mode deployment on a tested migration/rollback plan; the test-only runner fix does not solve production schema history.
- **Legacy approval state:** records marked approved without service application need a reconciliation report, not automatic replay.

## Non-Goals

- Rebuilding the chargen wizard or introducing a per-gameline step registry.
- Deduplicating view classes or changing unrelated templates.
- Adding a third-party object-permission library.
- Treating UI flags as authorization.

## Acceptance Criteria

- A new project route or router target without a declaration fails the route test and is denied at runtime.
- Anonymous and unrelated users can read only the minimal public card for an unfinished character; they cannot access its full sheet or mutate chargen. Authorized owners can complete every step.
- Player edits work only on their own unapproved objects; staff and correctly scoped STs can edit; wrong-chronicle or wrong-gameline STs cannot.
- Approval requires scoped `APPROVE`, allows ST self-approval only for NPCs, locks a pending row, and uses the appropriate service exactly once.
- Every `core.Model` object has a public GET/HEAD projection and a full projection limited to owner, its chronicle ST/game ST/head ST and staff; public reference GET remains public.
- Journals and spending records reveal neither content nor existence outside their owner/ST/staff audience; scenes obey `CHRONICLE`, `PARTICIPANTS`, or `PUBLIC` read mode with 404 for hidden records.
- Widget imports and raw `ObjectType` creation from index POST are gone; malformed inputs return controlled 4xx.
- `python manage.py test` passes after intended insecure-behavior tests are revised. The route inventory and focused security suite are part of each affected PR's verification.

## Appendix: Pre-fix route inventory

Generated from `scripts/inventory_authorization_routes.py` under the initial development URLconf. Each row is a reachable direct route or a router branch. `ANY*` means the function callback's accepted methods need manual review; framework-owned rows are explicit exclusions from the project middleware. Policy-family labels were review buckets; current runtime declarations are in `core/route_policy_manifest.py`.



Rows: 2569; direct routes: 1831
- AjaxLoginRequiredMixin: 8
- CharacterOwnerOrSTMixin: 6
- LoginRequiredMixin: 113
- OwnerRequiredMixin: 2
- Permission.EDIT_FULL: 97
- Permission.SPEND_FREEBIES: 400
- Permission.VIEW_FULL: 157
- function/unknown: 895
- global StorytellerRequiredMixin: 16
- none: 875

| Route | Router branch | View class | Current MRO gate | Login enforced by MRO | Methods | Intended policy family |
|---|---|---|---|---|---|---|
| __chained_select__/ |  | widgets.views.auto_chained_ajax_view | function/unknown | unknown | ANY* | login-only: allowlisted GET |
| __debug__/render_panel/ |  | debug_toolbar.views.render_panel | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| __debug__/history_sidebar/ |  | debug_toolbar.panels.history.views.history_sidebar | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| __debug__/history_refresh/ |  | debug_toolbar.panels.history.views.history_refresh | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| __debug__/sql_select/ |  | debug_toolbar.panels.sql.views.sql_select | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| __debug__/sql_explain/ |  | debug_toolbar.panels.sql.views.sql_explain | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| __debug__/sql_profile/ |  | debug_toolbar.panels.sql.views.sql_profile | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| __debug__/template_source/ |  | debug_toolbar.panels.templates.views.template_source | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/ |  | django.contrib.admin.sites.index | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/login/ |  | django.contrib.admin.sites.login | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/logout/ |  | django.contrib.admin.sites.logout | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/password_change/ |  | django.contrib.admin.sites.password_change | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/password_change/done/ |  | django.contrib.admin.sites.password_change_done | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/autocomplete/ |  | django.contrib.admin.sites.autocomplete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/jsi18n/ |  | django.contrib.admin.sites.i18n_javascript | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/r/<path:content_type_id>/<path:object_id>/ |  | django.contrib.contenttypes.views.shortcut | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/group/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/group/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/group/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/group/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/group/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/group/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/auth/user/<id>/password/ |  | django.contrib.auth.admin.user_change_password | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/user/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/user/add/ |  | django.contrib.auth.admin.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/user/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/user/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/user/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/auth/user/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/accounts/profile/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/accounts/profile/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/accounts/profile/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/accounts/profile/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/accounts/profile/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/accounts/profile/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/charactermodel/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/charactermodel/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/charactermodel/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/charactermodel/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/charactermodel/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/charactermodel/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/character/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/character/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/character/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/character/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/character/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/character/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/human/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/human/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/human/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/human/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/human/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/human/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/archetype/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/archetype/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/archetype/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/archetype/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/archetype/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/archetype/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/meritflaw/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflaw/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflaw/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflaw/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflaw/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflaw/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/meritflawrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflawrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflawrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflawrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflawrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/meritflawrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/derangement/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/derangement/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/derangement/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/derangement/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/derangement/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/derangement/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/group/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/group/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/group/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/group/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/group/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/group/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/specialty/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specialty/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specialty/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specialty/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specialty/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specialty/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/resonance/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resonance/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resonance/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resonance/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resonance/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resonance/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/effect/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/effect/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/effect/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/effect/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/effect/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/effect/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/paradigm/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/paradigm/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/paradigm/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/paradigm/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/paradigm/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/paradigm/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/practice/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practice/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practice/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practice/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practice/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practice/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/specializedpractice/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specializedpractice/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specializedpractice/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specializedpractice/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specializedpractice/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/specializedpractice/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/corruptedpractice/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/corruptedpractice/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/corruptedpractice/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/corruptedpractice/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/corruptedpractice/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/corruptedpractice/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/instrument/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/instrument/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/instrument/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/instrument/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/instrument/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/instrument/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/tenet/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tenet/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tenet/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tenet/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tenet/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tenet/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/magefaction/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/magefaction/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/magefaction/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/magefaction/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/magefaction/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/magefaction/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/rote/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rote/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rote/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rote/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rote/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rote/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/totem/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/totem/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/totem/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/totem/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/totem/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/totem/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/spiritcharm/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharm/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharm/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharm/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharm/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharm/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/spiritcharacter/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharacter/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharacter/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharacter/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharacter/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/spiritcharacter/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/mtahuman/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mtahuman/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mtahuman/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mtahuman/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mtahuman/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mtahuman/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/mage/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mage/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mage/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mage/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mage/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/mage/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/resrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/resrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/cabal/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/cabal/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/cabal/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/cabal/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/cabal/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/cabal/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/housefaction/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/housefaction/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/housefaction/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/housefaction/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/housefaction/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/housefaction/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/vtmhuman/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vtmhuman/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vtmhuman/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vtmhuman/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vtmhuman/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vtmhuman/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/vampire/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampire/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampire/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampire/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampire/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampire/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/ghoul/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ghoul/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ghoul/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ghoul/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ghoul/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ghoul/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/revenant/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenant/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenant/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenant/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenant/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenant/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/revenantfamily/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenantfamily/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenantfamily/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenantfamily/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenantfamily/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/revenantfamily/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/vampireclan/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampireclan/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampireclan/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampireclan/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampireclan/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampireclan/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/vampiresect/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiresect/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiresect/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiresect/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiresect/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiresect/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/vampiretitle/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiretitle/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiretitle/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiretitle/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiretitle/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/vampiretitle/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/path/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/path/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/path/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/path/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/path/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/path/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/discipline/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/discipline/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/discipline/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/discipline/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/discipline/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/discipline/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/wtohuman/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtohuman/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtohuman/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtohuman/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtohuman/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtohuman/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/practicerating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practicerating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practicerating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practicerating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practicerating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/practicerating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/statistic/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/statistic/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/statistic/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/statistic/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/statistic/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/statistic/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/ability/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ability/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ability/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ability/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ability/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ability/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/attribute/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/attribute/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/attribute/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/attribute/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/attribute/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/attribute/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/background/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/background/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/background/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/background/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/background/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/background/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/backgroundrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/backgroundrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/backgroundrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/backgroundrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/backgroundrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/backgroundrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/pooledbackgroundrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pooledbackgroundrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pooledbackgroundrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pooledbackgroundrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pooledbackgroundrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pooledbackgroundrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/wtahuman/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtahuman/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtahuman/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtahuman/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtahuman/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wtahuman/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/rite/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rite/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rite/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rite/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rite/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rite/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/tribe/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tribe/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tribe/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tribe/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tribe/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/tribe/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/gift/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/gift/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/gift/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/gift/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/gift/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/gift/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/renownincident/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/renownincident/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/renownincident/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/renownincident/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/renownincident/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/renownincident/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/battlescar/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/battlescar/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/battlescar/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/battlescar/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/battlescar/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/battlescar/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/camp/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/camp/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/camp/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/camp/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/camp/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/camp/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/werewolf/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/werewolf/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/werewolf/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/werewolf/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/werewolf/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/werewolf/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/kinfolk/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kinfolk/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kinfolk/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kinfolk/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kinfolk/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kinfolk/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/pack/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pack/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pack/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pack/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pack/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pack/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/fomor/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomor/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomor/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomor/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomor/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomor/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/fomoripower/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomoripower/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomoripower/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomoripower/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomoripower/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fomoripower/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/ananasi/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ananasi/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ananasi/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ananasi/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ananasi/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ananasi/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/rokea/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rokea/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rokea/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rokea/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rokea/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/rokea/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/kitsune/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kitsune/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kitsune/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kitsune/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kitsune/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kitsune/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/nagah/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/nagah/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/nagah/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/nagah/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/nagah/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/nagah/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/ajaba/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ajaba/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ajaba/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ajaba/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ajaba/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ajaba/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/grondr/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/grondr/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/grondr/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/grondr/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/grondr/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/grondr/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/drone/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/drone/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/drone/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/drone/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/drone/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/drone/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/septposition/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/septposition/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/septposition/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/septposition/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/septposition/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/septposition/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/changeling/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/changeling/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/changeling/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/changeling/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/changeling/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/changeling/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/legacy/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/legacy/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/legacy/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/legacy/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/legacy/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/legacy/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/ctdhuman/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ctdhuman/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ctdhuman/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ctdhuman/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ctdhuman/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ctdhuman/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/house/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/house/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/house/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/house/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/house/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/house/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/kith/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kith/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kith/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kith/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kith/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/kith/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/motley/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/motley/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/motley/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/motley/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/motley/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/motley/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/companion/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/companion/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/companion/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/companion/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/companion/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/companion/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/sorcerer/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcerer/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcerer/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcerer/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcerer/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcerer/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/linearmagicpath/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicpath/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicpath/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicpath/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicpath/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicpath/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/linearmagicritual/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicritual/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicritual/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicritual/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicritual/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/linearmagicritual/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/pathrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pathrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pathrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pathrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pathrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pathrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/sphere/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sphere/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sphere/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sphere/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sphere/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sphere/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/sorcererfellowship/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcererfellowship/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcererfellowship/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcererfellowship/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcererfellowship/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/sorcererfellowship/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/advantage/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantage/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantage/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantage/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantage/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantage/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/advantagerating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantagerating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantagerating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantagerating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantagerating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/advantagerating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/giftpermission/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/giftpermission/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/giftpermission/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/giftpermission/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/giftpermission/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/giftpermission/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/demon/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demon/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demon/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demon/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demon/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demon/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/dtfhuman/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/dtfhuman/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/dtfhuman/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/dtfhuman/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/dtfhuman/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/dtfhuman/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/demonfaction/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonfaction/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonfaction/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonfaction/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonfaction/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonfaction/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/demonhouse/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonhouse/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonhouse/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonhouse/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonhouse/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/demonhouse/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/visage/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/visage/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/visage/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/visage/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/visage/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/visage/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/lore/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lore/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lore/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lore/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lore/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lore/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/lorerating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lorerating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lorerating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lorerating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lorerating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/lorerating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/pact/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pact/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pact/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pact/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pact/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/pact/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/thrall/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thrall/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thrall/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thrall/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thrall/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thrall/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/earthbound/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/earthbound/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/earthbound/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/earthbound/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/earthbound/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/earthbound/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/apocalypticformtrait/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/apocalypticformtrait/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/apocalypticformtrait/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/apocalypticformtrait/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/apocalypticformtrait/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/apocalypticformtrait/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/ritual/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ritual/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ritual/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ritual/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ritual/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/ritual/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/wraith/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraith/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraith/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraith/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraith/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraith/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/guild/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/guild/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/guild/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/guild/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/guild/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/guild/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/wraithfaction/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraithfaction/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraithfaction/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraithfaction/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraithfaction/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/wraithfaction/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/arcanos/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/arcanos/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/arcanos/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/arcanos/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/arcanos/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/arcanos/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/shadowarchetype/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/shadowarchetype/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/shadowarchetype/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/shadowarchetype/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/shadowarchetype/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/shadowarchetype/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/thorn/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thorn/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thorn/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thorn/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thorn/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thorn/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/thornrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thornrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thornrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thornrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thornrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/thornrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/fetter/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fetter/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fetter/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fetter/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fetter/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/fetter/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/characters/passion/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/passion/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/passion/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/passion/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/passion/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/characters/passion/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/chronicle/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/chronicle/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/chronicle/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/chronicle/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/chronicle/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/chronicle/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/scene/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/scene/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/scene/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/scene/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/scene/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/scene/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/post/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/post/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/post/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/post/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/post/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/post/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/settingelement/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/settingelement/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/settingelement/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/settingelement/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/settingelement/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/settingelement/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/objecttype/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/objecttype/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/objecttype/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/objecttype/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/objecttype/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/objecttype/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/gameline/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/gameline/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/gameline/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/gameline/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/gameline/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/gameline/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/strelationship/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/strelationship/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/strelationship/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/strelationship/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/strelationship/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/strelationship/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/story/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/story/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/story/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/story/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/story/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/story/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/week/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/week/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/week/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/week/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/week/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/week/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/weeklyxprequest/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/weeklyxprequest/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/weeklyxprequest/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/weeklyxprequest/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/weeklyxprequest/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/weeklyxprequest/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/storyxprequest/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/storyxprequest/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/storyxprequest/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/storyxprequest/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/storyxprequest/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/storyxprequest/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/userscenereadstatus/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/userscenereadstatus/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/userscenereadstatus/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/userscenereadstatus/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/userscenereadstatus/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/userscenereadstatus/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/journal/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journal/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journal/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journal/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journal/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journal/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/journalentry/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journalentry/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journalentry/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journalentry/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journalentry/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/journalentry/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/xpspendingrequest/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/xpspendingrequest/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/xpspendingrequest/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/xpspendingrequest/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/xpspendingrequest/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/xpspendingrequest/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/game/freebiespendingrecord/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/freebiespendingrecord/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/freebiespendingrecord/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/freebiespendingrecord/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/freebiespendingrecord/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/game/freebiespendingrecord/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/itemmodel/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/itemmodel/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/itemmodel/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/itemmodel/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/itemmodel/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/itemmodel/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/weapon/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/weapon/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/weapon/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/weapon/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/weapon/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/weapon/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/meleeweapon/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/meleeweapon/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/meleeweapon/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/meleeweapon/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/meleeweapon/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/meleeweapon/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/thrownweapon/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/thrownweapon/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/thrownweapon/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/thrownweapon/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/thrownweapon/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/thrownweapon/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/rangedweapon/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/rangedweapon/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/rangedweapon/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/rangedweapon/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/rangedweapon/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/rangedweapon/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/medium/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/medium/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/medium/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/medium/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/medium/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/medium/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/material/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/material/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/material/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/material/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/material/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/material/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/wonder/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonder/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonder/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonder/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonder/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonder/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/wonderresonancerating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonderresonancerating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonderresonancerating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonderresonancerating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonderresonancerating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wonderresonancerating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/charm/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/charm/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/charm/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/charm/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/charm/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/charm/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/talisman/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/talisman/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/talisman/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/talisman/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/talisman/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/talisman/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/artifact/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/artifact/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/artifact/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/artifact/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/artifact/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/artifact/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/grimoire/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/grimoire/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/grimoire/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/grimoire/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/grimoire/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/grimoire/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/fetish/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/fetish/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/fetish/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/fetish/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/fetish/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/fetish/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/sorcererartifact/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/sorcererartifact/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/sorcererartifact/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/sorcererartifact/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/sorcererartifact/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/sorcererartifact/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/vampireartifact/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/vampireartifact/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/vampireartifact/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/vampireartifact/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/vampireartifact/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/vampireartifact/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/bloodstone/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/bloodstone/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/bloodstone/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/bloodstone/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/bloodstone/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/bloodstone/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/relic/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/relic/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/relic/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/relic/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/relic/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/relic/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/wraithrelic/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithrelic/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithrelic/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithrelic/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithrelic/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithrelic/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/wraithartifact/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithartifact/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithartifact/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithartifact/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithartifact/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/wraithartifact/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/items/treasure/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/treasure/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/treasure/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/treasure/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/treasure/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/items/treasure/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/locationmodel/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/locationmodel/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/locationmodel/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/locationmodel/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/locationmodel/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/locationmodel/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/sanctum/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sanctum/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sanctum/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sanctum/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sanctum/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sanctum/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/city/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/city/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/city/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/city/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/city/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/city/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/node/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/node/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/node/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/node/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/node/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/node/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/nodemeritflawrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/nodemeritflawrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/nodemeritflawrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/nodemeritflawrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/nodemeritflawrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/nodemeritflawrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/noderesonancerating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/noderesonancerating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/noderesonancerating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/noderesonancerating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/noderesonancerating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/noderesonancerating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/library/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/library/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/library/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/library/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/library/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/library/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/sector/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sector/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sector/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sector/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sector/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/sector/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/horizonrealm/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/horizonrealm/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/horizonrealm/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/horizonrealm/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/horizonrealm/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/horizonrealm/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/realityzone/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/realityzone/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/realityzone/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/realityzone/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/realityzone/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/realityzone/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/zonerating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/zonerating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/zonerating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/zonerating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/zonerating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/zonerating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/caern/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/caern/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/caern/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/caern/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/caern/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/caern/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/chantry/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantry/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantry/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantry/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantry/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantry/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/chantrybackgroundrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantrybackgroundrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantrybackgroundrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantrybackgroundrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantrybackgroundrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/chantrybackgroundrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/haunt/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haunt/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haunt/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haunt/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haunt/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haunt/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/necropolis/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/necropolis/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/necropolis/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/necropolis/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/necropolis/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/necropolis/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/haven/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haven/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haven/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haven/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haven/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/haven/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/domain/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/domain/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/domain/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/domain/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/domain/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/domain/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/elysium/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/elysium/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/elysium/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/elysium/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/elysium/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/elysium/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/rack/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/rack/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/rack/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/rack/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/rack/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/rack/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/tremerechantry/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/tremerechantry/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/tremerechantry/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/tremerechantry/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/tremerechantry/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/tremerechantry/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/barrens/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/barrens/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/barrens/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/barrens/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/barrens/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/barrens/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/havenmeritflawrating/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/havenmeritflawrating/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/havenmeritflawrating/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/havenmeritflawrating/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/havenmeritflawrating/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/havenmeritflawrating/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/freehold/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/freehold/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/freehold/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/freehold/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/freehold/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/freehold/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/bastion/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/bastion/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/bastion/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/bastion/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/bastion/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/bastion/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/locations/reliquary/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/reliquary/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/reliquary/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/reliquary/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/reliquary/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/locations/reliquary/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/core/newsitem/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/newsitem/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/newsitem/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/newsitem/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/newsitem/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/newsitem/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/core/book/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/book/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/book/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/book/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/book/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/book/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/core/bookreference/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/bookreference/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/bookreference/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/bookreference/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/bookreference/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/bookreference/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/core/language/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/language/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/language/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/language/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/language/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/language/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/core/houserule/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/houserule/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/houserule/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/houserule/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/houserule/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/houserule/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/core/charactertemplate/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/charactertemplate/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/charactertemplate/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/charactertemplate/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/charactertemplate/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/charactertemplate/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/core/templateapplication/ |  | django.contrib.admin.options.changelist_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/templateapplication/add/ |  | django.contrib.admin.options.add_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/templateapplication/<path:object_id>/history/ |  | django.contrib.admin.options.history_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/templateapplication/<path:object_id>/delete/ |  | django.contrib.admin.options.delete_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/templateapplication/<path:object_id>/change/ |  | django.contrib.admin.options.change_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/core/templateapplication/<path:object_id>/ |  | django.views.generic.base.RedirectView | none | no | GET,POST,PUT,PATCH,DELETE,HEAD,OPTIONS | framework-owned: explicit exclusion |
| admin/^(?P<app_label>auth\|accounts\|characters\|game\|items\|locations\|core)/$ |  | django.contrib.admin.sites.app_index | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
| admin/(?P<url>.*)$ |  | django.contrib.admin.sites.catch_all_view | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
|  |  | core.views.home.HomeListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| book/create/ |  | core.views.book.BookCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| book/<pk>/ |  | core.views.book.BookDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| book/update/<pk>/ |  | core.views.book.BookUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| book/ |  | core.views.book.BookListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| language/create/ |  | core.views.language.LanguageCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| language/<pk>/ |  | core.views.language.LanguageDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| language/update/<pk>/ |  | core.views.language.LanguageUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| language/ |  | core.views.language.LanguageListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| newsitem/create/ |  | core.views.newsitem.NewsItemCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| newsitem/<pk>/ |  | core.views.newsitem.NewsItemDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| newsitem/update/<pk>/ |  | core.views.newsitem.NewsItemUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| newsitem/ |  | core.views.newsitem.NewsItemListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| houserules/index/ |  | core.views.houserules.HouseRulesIndexView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| houserules/create/ |  | core.views.houserules.HouseRuleCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| houserules/<pk>/ |  | core.views.houserules.HouseRuleDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| houserules/update/<pk>/ |  | core.views.houserules.HouseRuleUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| templates/ |  | core.views.character_template.CharacterTemplateListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered public/full collection |
| templates/create/ |  | core.views.character_template.CharacterTemplateCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: template action scoped to owner/ST/staff |
| templates/<int:pk>/ |  | core.views.character_template.CharacterTemplateDetailView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| templates/<int:pk>/edit/ |  | core.views.character_template.CharacterTemplateUpdateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: template action scoped to owner/ST/staff |
| templates/<int:pk>/delete/ |  | core.views.character_template.CharacterTemplateDeleteView | LoginRequiredMixin | yes | GET,POST,DELETE,OPTIONS,HEAD | object-permission: template action scoped to owner/ST/staff |
| templates/<int:pk>/export/ |  | core.views.character_template.CharacterTemplateExportView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: template action scoped to owner/ST/staff |
| templates/import/ |  | core.views.character_template.CharacterTemplateImportView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: template action scoped to owner/ST/staff |
| templates/<int:pk>/create-npc/ |  | core.views.character_template.CharacterTemplateQuickNPCView | LoginRequiredMixin | yes | POST,OPTIONS | object-permission: template action scoped to owner/ST/staff |
| characters/vampire/create/vtmhuman/ |  | characters.views.vampire.vtmhuman.VtMHumanBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/vampire/ |  | characters.views.vampire.vampire_chargen.VampireBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/ghoul/ |  | characters.views.vampire.ghoul_chargen.GhoulBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/revenant/ |  | characters.views.vampire.revenant.RevenantCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/clan/ |  | characters.views.vampire.clan.VampireClanCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/sect/ |  | characters.views.vampire.sect.VampireSectCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/path/ |  | characters.views.vampire.path.PathCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/title/ |  | characters.views.vampire.title.VampireTitleCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/discipline/ |  | characters.views.vampire.discipline.DisciplineCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/vampire/create/coterie/ |  | characters.views.vampire.coterie.CoterieCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/vampire/create/revenant_family/ |  | characters.views.vampire.revenant_family.RevenantFamilyCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/vampire/update/vtmhuman/<pk>/ |  | characters.views.vampire.vtmhuman.VtMHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/vtm_human/full/<pk>/ |  | characters.views.vampire.vtmhuman.VtMHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/vampire/<pk>/ |  | characters.views.vampire.vampire.VampireUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/ghoul/<pk>/ |  | characters.views.vampire.ghoul.GhoulUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/revenant/<pk>/ |  | characters.views.vampire.revenant.RevenantUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/clan/<pk>/ |  | characters.views.vampire.clan.VampireClanUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/sect/<pk>/ |  | characters.views.vampire.sect.VampireSectUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/path/<pk>/ |  | characters.views.vampire.path.PathUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/title/<pk>/ |  | characters.views.vampire.title.VampireTitleUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/discipline/<pk>/ |  | characters.views.vampire.discipline.DisciplineUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/vampire/update/coterie/<pk>/ |  | characters.views.vampire.coterie.CoterieUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/update/revenant_family/<pk>/ |  | characters.views.vampire.revenant_family.RevenantFamilyUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/vampire/list/clan/ |  | characters.views.vampire.clan.VampireClanListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/vampire/list/coterie/ |  | characters.views.vampire.coterie.CoterieListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/vampire/list/discipline/ |  | characters.views.vampire.discipline.DisciplineListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/vampire/list/path/ |  | characters.views.vampire.path.PathListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/vampire/list/sect/ |  | characters.views.vampire.sect.VampireSectListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/vampire/list/title/ |  | characters.views.vampire.title.VampireTitleListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/vampire/vampire/<pk>/ |  | characters.views.vampire.vampire.VampireDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/ghoul/<pk>/ |  | characters.views.vampire.ghoul.GhoulDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/revenant/<pk>/ |  | characters.views.vampire.revenant.RevenantDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/clan/<pk>/ |  | characters.views.vampire.clan.VampireClanDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/sect/<pk>/ |  | characters.views.vampire.sect.VampireSectDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/path/<pk>/ |  | characters.views.vampire.path.PathDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/title/<pk>/ |  | characters.views.vampire.title.VampireTitleDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/discipline/<pk>/ |  | characters.views.vampire.discipline.DisciplineDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/vampire/vampire/<int:pk>/chargen/ |  | characters.views.vampire.vampire_chargen.VampireCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/vampire/vampire/<int:pk>/chargen/ | 1 | characters.views.vampire.vampire_chargen.VampireAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 2 | characters.views.vampire.vampire_chargen.VampireAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 3 | characters.views.vampire.vampire_chargen.VampireBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 4 | characters.views.vampire.vampire_chargen.VampireDisciplinesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 5 | characters.views.vampire.vampire_chargen.VampireVirtuesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 6 | characters.views.vampire.vampire_chargen.VampireExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 7 | characters.views.vampire.vampire_chargen.VampireFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 8 | characters.views.vampire.vampire_chargen.VampireLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 9 | characters.views.vampire.vampire_chargen.VampireAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 10 | characters.views.vampire.vampire_chargen.VampireMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 11 | characters.views.vampire.vampire_chargen.VampireContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 12 | characters.views.vampire.vampire_chargen.VampireRetainersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | 13 | characters.views.vampire.vampire_chargen.VampireSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vampire/<int:pk>/chargen/ | <default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/vampire/ghoul/<int:pk>/chargen/ |  | characters.views.vampire.ghoul_chargen.GhoulCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/vampire/ghoul/<int:pk>/chargen/ | 1 | characters.views.vampire.ghoul_chargen.GhoulAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 2 | characters.views.vampire.ghoul_chargen.GhoulAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 3 | characters.views.vampire.ghoul_chargen.GhoulBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 4 | characters.views.vampire.ghoul_chargen.GhoulDisciplinesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 5 | characters.views.vampire.ghoul_chargen.GhoulExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 6 | characters.views.vampire.ghoul_chargen.GhoulFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 7 | characters.views.vampire.ghoul_chargen.GhoulLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 8 | characters.views.vampire.ghoul_chargen.GhoulAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | 9 | characters.views.vampire.ghoul_chargen.GhoulSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/ghoul/<int:pk>/chargen/ | <default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/vampire/vtmhuman/<int:pk>/template/ |  | characters.views.vampire.vtmhuman.VtMHumanTemplateSelectView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/vampire/vtmhuman/<int:pk>/creation/ |  | characters.views.vampire.vtmhuman.VtMHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 1 | characters.views.vampire.vtmhuman.VtMHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 2 | characters.views.vampire.vtmhuman.VtMHumanAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 3 | characters.views.vampire.vtmhuman.VtMHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 4 | characters.views.vampire.vtmhuman.VtMHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 5 | characters.views.vampire.vtmhuman.VtMHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 6 | characters.views.vampire.vtmhuman.VtMHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 7 | characters.views.vampire.vtmhuman.VtMHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | 8 | characters.views.vampire.vtmhuman.VtMHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/vampire/vtmhuman/<int:pk>/creation/ | <default> | characters.views.vampire.vtmhuman.VtMHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/coterie/<pk>/ |  | characters.views.vampire.coterie.CoterieDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/vampire/revenant_family/<pk>/ |  | characters.views.vampire.revenant_family.RevenantFamilyDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/werewolf/create/charms/ |  | characters.views.werewolf.charm.SpiritCharmCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/spirits/ |  | characters.views.werewolf.spirit.SpiritCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/totems/ |  | characters.views.werewolf.totem.TotemCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/wtahuman/ |  | characters.views.werewolf.wtahuman.WtAHumanBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/rites/ |  | characters.views.werewolf.rite.RiteCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/tribes/ |  | characters.views.werewolf.tribe.TribeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/renownincidents/ |  | characters.views.werewolf.renownincident.RenownIncidentCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/battlescar/ |  | characters.views.werewolf.battlescar.BattleScarCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/gifts/ |  | characters.views.werewolf.gift.GiftCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/pack/ |  | characters.views.werewolf.pack.PackCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/fomor/ |  | characters.views.werewolf.fomor.FomorBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/werewolf/ |  | characters.views.werewolf.garou.WerewolfBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/kinfolk/ |  | characters.views.werewolf.kinfolk.KinfolkBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/fera/ |  | characters.views.werewolf.fera.FeraBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/camps/ |  | characters.views.werewolf.camp.CampCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/fomoripower/ |  | characters.views.werewolf.fomoripower.FomoriPowerCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/drone/ |  | characters.views.werewolf.drone.DroneBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/create/septposition/ |  | characters.views.werewolf.septposition.SeptPositionCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/werewolf/update/charms/<pk>/ |  | characters.views.werewolf.charm.SpiritCharmUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/spirits/<pk>/ |  | characters.views.werewolf.spirit.SpiritUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/totems/<pk>/ |  | characters.views.werewolf.totem.TotemUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/wtahuman/<pk>/ |  | characters.views.werewolf.wtahuman.WtAHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/rites/<pk>/ |  | characters.views.werewolf.rite.RiteUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/tribes/<pk>/ |  | characters.views.werewolf.tribe.TribeUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/gifts/<pk>/ |  | characters.views.werewolf.gift.GiftUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/renownincidents/<pk>/ |  | characters.views.werewolf.renownincident.RenownIncidentUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/battlescar/<pk>/ |  | characters.views.werewolf.battlescar.BattleScarUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/pack/<pk>/ |  | characters.views.werewolf.pack.PackUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/fomor/<pk>/ |  | characters.views.werewolf.fomor.FomorCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/werewolf/update/fomor/<pk>/ | 1 | characters.views.werewolf.fomor.FomorAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 2 | characters.views.werewolf.fomor.FomorAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 3 | characters.views.werewolf.fomor.FomorBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 4 | characters.views.werewolf.fomor.FomorPowersView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 5 | characters.views.werewolf.fomor.FomorExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 6 | characters.views.werewolf.fomor.FomorFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 7 | characters.views.werewolf.fomor.FomorLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 8 | characters.views.werewolf.fomor.FomorAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 9 | characters.views.werewolf.fomor.FomorContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | 10 | characters.views.werewolf.fomor.FomorSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fomor/<pk>/ | <default> | characters.views.werewolf.fomor.FomorDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/update/fomor/full/<pk>/ |  | characters.views.werewolf.fomor.FomorUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/werewolf/full/<pk>/ |  | characters.views.werewolf.garou.WerewolfUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/werewolf/<pk>/ |  | characters.views.werewolf.garou.WerewolfCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/werewolf/update/werewolf/<pk>/ | 1 | characters.views.werewolf.garou.WerewolfAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 2 | characters.views.werewolf.garou.WerewolfAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 3 | characters.views.werewolf.garou.WerewolfBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 4 | characters.views.werewolf.garou.WerewolfGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 5 | characters.views.werewolf.garou.WerewolfHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 6 | characters.views.werewolf.garou.WerewolfExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 7 | characters.views.werewolf.garou.WerewolfFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 8 | characters.views.werewolf.garou.WerewolfLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 9 | characters.views.werewolf.garou.WerewolfAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 10 | characters.views.werewolf.garou.WerewolfMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 11 | characters.views.werewolf.garou.WerewolfContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | 12 | characters.views.werewolf.garou.WerewolfSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/werewolf/<pk>/ | <default> | characters.views.werewolf.garou.WerewolfDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/update/kinfolk/<pk>/ |  | characters.views.werewolf.kinfolk.KinfolkUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/kinfolk/full/<pk>/ |  | characters.views.werewolf.kinfolk.KinfolkUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/fera/<pk>/ |  | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/werewolf/update/fera/<pk>/ | 1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | 11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/update/fera/<pk>/ | <default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/update/fera/full/<pk>/ |  | characters.views.werewolf.fera.FeraUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/camps/<pk>/ |  | characters.views.werewolf.camp.CampUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/fomoripower/<pk>/ |  | characters.views.werewolf.fomoripower.FomoriPowerUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/update/wta_human/full/<pk>/ |  | characters.views.werewolf.wtahuman.WtAHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/list/charms/ |  | characters.views.werewolf.charm.SpiritCharmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/totems/ |  | characters.views.werewolf.totem.TotemListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/rites/ |  | characters.views.werewolf.rite.RiteListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/tribes/ |  | characters.views.werewolf.tribe.TribeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/gifts/ |  | characters.views.werewolf.gift.GiftListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/battlescar/ |  | characters.views.werewolf.battlescar.BattleScarListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/renownincidents/ |  | characters.views.werewolf.renownincident.RenownIncidentListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/camps/ |  | characters.views.werewolf.camp.CampListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/fomoripower/ |  | characters.views.werewolf.fomoripower.FomoriPowerListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/list/pack/ |  | characters.views.werewolf.pack.PackListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/werewolf/charms/<pk>/ |  | characters.views.werewolf.charm.SpiritCharmDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/spirits/<pk>/ |  | characters.views.werewolf.spirit.SpiritDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/totems/<pk>/ |  | characters.views.werewolf.totem.TotemDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/rites/<pk>/ |  | characters.views.werewolf.rite.RiteDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/tribes/<pk>/ |  | characters.views.werewolf.tribe.TribeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/gifts/<pk>/ |  | characters.views.werewolf.gift.GiftDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/battlescar/<pk>/ |  | characters.views.werewolf.battlescar.BattleScarDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/renownincidents/<pk>/ |  | characters.views.werewolf.renownincident.RenownIncidentDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/camps/<pk>/ |  | characters.views.werewolf.camp.CampDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/fomoripower/<pk>/ |  | characters.views.werewolf.fomoripower.FomoriPowerDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/fera/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/ratkin/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/mokole/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/bastet/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/corax/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/nuwisha/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/gurahl/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/ananasi/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/rokea/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/kitsune/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/nagah/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/ajaba/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/grondr/<pk>/ |  | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/drone/<pk>/ |  | characters.views.werewolf.drone.DroneDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/septposition/<pk>/ |  | characters.views.werewolf.septposition.SeptPositionDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/template/ |  | characters.views.werewolf.wtahuman.WtAHumanTemplateSelectView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/werewolf/wtahuman/<int:pk>/creation/ |  | characters.views.werewolf.wtahuman.WtAHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 1 | characters.views.werewolf.wtahuman.WtAHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 2 | characters.views.werewolf.wtahuman.WtAHumanAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 3 | characters.views.werewolf.wtahuman.WtAHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 4 | characters.views.werewolf.wtahuman.WtAHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 5 | characters.views.werewolf.wtahuman.WtAHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 6 | characters.views.werewolf.wtahuman.WtAHumanLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 7 | characters.views.werewolf.wtahuman.WtAHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | 8 | characters.views.werewolf.wtahuman.WtAHumanSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/werewolf/wtahuman/<int:pk>/creation/ | <default> | characters.views.werewolf.wtahuman.WtAHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/ajax/load_mf_ratings/ |  | characters.views.mage.mage.LoadMFRatingsView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/load_xp_examples/ |  | characters.views.mage.mage.LoadXPExamplesView | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/load_companion_examples/ |  | characters.views.mage.companion.LoadExamplesView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/load_sorcerer_examples/ |  | characters.views.mage.sorcerer.LoadExamplesView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/load_advantage_values/ |  | characters.views.mage.companion.LoadCompanionValuesView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/get_abilities/ |  | characters.views.mage.mage.GetAbilitiesView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/get_practice_abilities/ |  | characters.views.mage.sorcerer.GetPracticeAbilitiesView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/load_attributes/ |  | characters.views.mage.sorcerer.LoadAttributesView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/ajax/load_affinities/ |  | characters.views.mage.sorcerer.LoadAffinitiesView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/create/effect/ |  | characters.views.mage.effect.EffectCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/resonance/ |  | characters.views.mage.resonance.ResonanceCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/instruments/ |  | characters.views.mage.focus.InstrumentCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/paradigms/ |  | characters.views.mage.focus.ParadigmCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/practices/ |  | characters.views.mage.focus.PracticeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/specialized_practices/ |  | characters.views.mage.focus.SpecializedPracticeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/corrupted_practices/ |  | characters.views.mage.focus.CorruptedPracticeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/tenet/ |  | characters.views.mage.focus.TenetCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/sorcerer_fellowship/ |  | characters.views.mage.fellowship.SorcererFellowshipCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/mage_faction/ |  | characters.views.mage.faction.MageFactionCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/rotes/ |  | characters.views.mage.rote.RoteCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/paths/ |  | characters.views.mage.hedge_magic.PathCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/rituals/ |  | characters.views.mage.hedge_magic.RitualCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/mtahuman/ |  | characters.views.mage.mtahuman.MtAHumanBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/companion/ |  | characters.views.mage.companion.CompanionBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/sorcerer/ |  | characters.views.mage.sorcerer.SorcererBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/mage/ |  | characters.views.mage.mage.MageBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/mage/full/ |  | characters.views.mage.mage.MageCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/companion/full/ |  | characters.views.mage.companion.CompanionCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/cabal/ |  | characters.views.mage.cabal.CabalCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mage/create/sphere/ |  | characters.views.mage.sphere.SphereCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/mage/update/effect/<pk>/ |  | characters.views.mage.effect.EffectUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/resonances/<pk>/ |  | characters.views.mage.resonance.ResonanceUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/paradigms/<pk>/ |  | characters.views.mage.focus.ParadigmUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/instruments/<pk>/ |  | characters.views.mage.focus.InstrumentUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/practices/<pk>/ |  | characters.views.mage.focus.PracticeUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/specialized_practices/<pk>/ |  | characters.views.mage.focus.SpecializedPracticeUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/corrupted_practices/<pk>/ |  | characters.views.mage.focus.CorruptedPracticeUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/tenet/<pk>/ |  | characters.views.mage.focus.TenetUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/mage_factions/<pk>/ |  | characters.views.mage.faction.MageFactionUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/sorcerer_fellowship/<pk>/ |  | characters.views.mage.fellowship.SorcererFellowshipUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/rotes/<pk>/ |  | characters.views.mage.rote.RoteUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/paths/<pk>/ |  | characters.views.mage.hedge_magic.PathUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/rituals/<pk>/ |  | characters.views.mage.hedge_magic.RitualUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/mtahuman/<pk>/ |  | characters.views.mage.mtahuman.MtAHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/mage/full/<pk>/ |  | characters.views.mage.mage.MageUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/sorcerer/full/<pk>/ |  | characters.views.mage.sorcerer.SorcererUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/mage/<pk>/ |  | characters.views.mage.mage.MageCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/mage/update/mage/<pk>/ | 1 | characters.views.mage.mage.MageAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 2 | characters.views.mage.mage.MageAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 3 | characters.views.mage.mage.MageBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 4 | characters.views.mage.mage.MageSpheresView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 5 | characters.views.mage.mage.MageFocusView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 6 | characters.views.mage.mage.MageExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 7 | characters.views.mage.mage.MageFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 8 | characters.views.mage.mage.MageLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 9 | characters.views.mage.mage.MageRoteView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 10 | characters.views.mage.mage.MageNodeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 11 | characters.views.mage.mage.MageLibraryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 12 | characters.views.mage.mage.MageFamiliarView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 13 | characters.views.mage.mage.MageWonderView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 14 | characters.views.mage.mage.MageEnhancementView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 15 | characters.views.mage.mage.MageSanctumView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 16 | characters.views.mage.mage.MageAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 17 | characters.views.mage.mage.MageMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 18 | characters.views.mage.mage.MageContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 19 | characters.views.mage.mage.MageRetainersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 20 | characters.views.mage.mage.MageChantryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | 21 | characters.views.mage.mage.MageSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/update/mage/<pk>/ | <default> | characters.views.mage.mage.MageDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/update/companion/full/<pk>/ |  | characters.views.mage.companion.CompanionUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/mta_human/full/<pk>/ |  | characters.views.mage.mtahuman.MtAHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/cabal/<pk>/ |  | characters.views.mage.cabal.CabalUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/update/sphere/<pk>/ |  | characters.views.mage.sphere.SphereUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/mage/list/effect/ |  | characters.views.mage.effect.EffectListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/resonances/ |  | characters.views.mage.resonance.ResonanceListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/instruments/ |  | characters.views.mage.focus.InstrumentListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/paradigms/ |  | characters.views.mage.focus.ParadigmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/practices/ |  | characters.views.mage.focus.PracticeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/specialized_practices/ |  | characters.views.mage.focus.SpecializedPracticeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/corrupted_practices/ |  | characters.views.mage.focus.CorruptedPracticeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/tenet/ |  | characters.views.mage.focus.TenetListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/mage_factions/ |  | characters.views.mage.faction.MageFactionListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/sorcerer_fellowships/ |  | characters.views.mage.fellowship.SorcererFellowshipListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/rotes/ |  | characters.views.mage.rote.RoteListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/paths/ |  | characters.views.mage.hedge_magic.PathListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/rituals/ |  | characters.views.mage.hedge_magic.RitualListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/cabal/ |  | characters.views.mage.cabal.CabalListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mage/list/spheres/ |  | characters.views.mage.sphere.SphereListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/mage/mtahuman/<int:pk>/template/ |  | characters.views.mage.mtahuman.MtAHumanTemplateSelectView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mage/mtahuman/<int:pk>/creation/ |  | characters.views.mage.mtahuman.MtAHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/mage/mtahuman/<int:pk>/creation/ | 1 | characters.views.mage.mtahuman.MtAHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 2 | characters.views.mage.mtahuman.MtAHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 3 | characters.views.mage.mtahuman.MtAHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 4 | characters.views.mage.mtahuman.MtAHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 5 | characters.views.mage.mtahuman.MtAHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 6 | characters.views.mage.mtahuman.MtAHumanLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 7 | characters.views.mage.mtahuman.MtAHumanNodeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 8 | characters.views.mage.mtahuman.MtAHumanLibraryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 9 | characters.views.mage.mtahuman.MtAHumanWonderView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 10 | characters.views.mage.mtahuman.MtAHumanEnhancementView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 11 | characters.views.mage.mtahuman.MtAHumanSanctumView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 12 | characters.views.mage.mtahuman.MtAHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 13 | characters.views.mage.mtahuman.MtAHumanChantryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | 14 | characters.views.mage.mtahuman.MtAHumanSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/mage/mtahuman/<int:pk>/creation/ | <default> | characters.views.mage.mtahuman.MtAHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/effect/<pk>/ |  | characters.views.mage.effect.EffectDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/resonances/<pk>/ |  | characters.views.mage.resonance.ResonanceDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/instruments/<pk>/ |  | characters.views.mage.focus.InstrumentDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/paradigms/<pk>/ |  | characters.views.mage.focus.ParadigmDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/practices/<pk>/ |  | characters.views.mage.focus.GenericPracticeDetailView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/mage/practices/<pk>/ | practice | characters.views.mage.focus.PracticeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/practices/<pk>/ | specialized_practice | characters.views.mage.focus.SpecializedPracticeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/practices/<pk>/ | corrupted_practice | characters.views.mage.focus.CorruptedPracticeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/specialized_practices/<pk>/ |  | characters.views.mage.focus.SpecializedPracticeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/corrupted_practices/<pk>/ |  | characters.views.mage.focus.CorruptedPracticeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/tenet/<pk>/ |  | characters.views.mage.focus.TenetDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/mage_factions/<pk>/ |  | characters.views.mage.faction.MageFactionDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/sorcerer_fellowships/<pk>/ |  | characters.views.mage.fellowship.SorcererFellowshipDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/rotes/<pk>/ |  | characters.views.mage.rote.RoteDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/paths/<pk>/ |  | characters.views.mage.hedge_magic.PathDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/rituals/<pk>/ |  | characters.views.mage.hedge_magic.RitualDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/advantages/<pk>/ |  | characters.views.mage.advantage.AdvantageDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mage/sphere/<pk>/ |  | characters.views.mage.sphere.SphereDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/wraith/create/arcanos/ |  | characters.views.wraith.arcanos.ArcanosCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/create/circle/ |  | characters.views.wraith.circle.CircleCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/create/faction/ |  | characters.views.wraith.faction.WraithFactionCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/create/guild/ |  | characters.views.wraith.guild.GuildCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/create/shadow_archetype/ |  | characters.views.wraith.shadow_archetype.ShadowArchetypeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/create/thorn/ |  | characters.views.wraith.thorn.ThornCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/create/wtohuman/ |  | characters.views.wraith.wtohuman.WtOHumanBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/create/wraith/ |  | characters.views.wraith.wraith_chargen.WraithBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/wraith/update/arcanos/<pk>/ |  | characters.views.wraith.arcanos.ArcanosUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/circle/<pk>/ |  | characters.views.wraith.circle.CircleUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/faction/<pk>/ |  | characters.views.wraith.faction.WraithFactionUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/guild/<pk>/ |  | characters.views.wraith.guild.GuildUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/shadow_archetype/<pk>/ |  | characters.views.wraith.shadow_archetype.ShadowArchetypeUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/thorn/<pk>/ |  | characters.views.wraith.thorn.ThornUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/wtohuman/<pk>/ |  | characters.views.wraith.wtohuman.WtOHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/wto_human/full/<pk>/ |  | characters.views.wraith.wtohuman.WtOHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/update/wraith/<pk>/ |  | characters.views.wraith.wraith_chargen.WraithCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/wraith/update/wraith/<pk>/ | 1 | characters.views.wraith.wraith_chargen.WraithAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 2 | characters.views.wraith.wraith_chargen.WraithAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 3 | characters.views.wraith.wraith_chargen.WraithBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 4 | characters.views.wraith.wraith_chargen.WraithArcanosView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 5 | characters.views.wraith.wraith_chargen.WraithShadowView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 6 | characters.views.wraith.wraith_chargen.WraithPassionsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 7 | characters.views.wraith.wraith_chargen.WraithFettersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 8 | characters.views.wraith.wraith_chargen.WraithExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 9 | characters.views.wraith.wraith_chargen.WraithFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 10 | characters.views.wraith.wraith_chargen.WraithLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 11 | characters.views.wraith.wraith_chargen.WraithAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 12 | characters.views.wraith.wraith_chargen.WraithMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 13 | characters.views.wraith.wraith_chargen.WraithContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | 14 | characters.views.wraith.wraith_chargen.WraithSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/update/wraith/<pk>/ | <default> | characters.views.wraith.wraith.WraithDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/update/wraith/full/<pk>/ |  | characters.views.wraith.wraith.WraithUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/list/arcanoi/ |  | characters.views.wraith.arcanos.ArcanosListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/wraith/list/circles/ |  | characters.views.wraith.circle.CircleListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/wraith/list/factions/ |  | characters.views.wraith.faction.WraithFactionListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/wraith/list/guilds/ |  | characters.views.wraith.guild.GuildListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/wraith/list/shadow_archetypes/ |  | characters.views.wraith.shadow_archetype.ShadowArchetypeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/wraith/list/thorns/ |  | characters.views.wraith.thorn.ThornListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/wraith/arcanos/<pk>/ |  | characters.views.wraith.arcanos.ArcanosDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/circle/<pk>/ |  | characters.views.wraith.circle.CircleDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/faction/<pk>/ |  | characters.views.wraith.faction.WraithFactionDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/guild/<pk>/ |  | characters.views.wraith.guild.GuildDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/shadow_archetype/<pk>/ |  | characters.views.wraith.shadow_archetype.ShadowArchetypeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/wraith/<pk>/ |  | characters.views.wraith.wraith.WraithDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/thorn/<pk>/ |  | characters.views.wraith.thorn.ThornDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ |  | characters.views.wraith.wraith_chargen.WraithCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/wraith/wraith/<int:pk>/chargen/ | 1 | characters.views.wraith.wraith_chargen.WraithAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 2 | characters.views.wraith.wraith_chargen.WraithAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 3 | characters.views.wraith.wraith_chargen.WraithBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 4 | characters.views.wraith.wraith_chargen.WraithArcanosView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 5 | characters.views.wraith.wraith_chargen.WraithShadowView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 6 | characters.views.wraith.wraith_chargen.WraithPassionsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 7 | characters.views.wraith.wraith_chargen.WraithFettersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 8 | characters.views.wraith.wraith_chargen.WraithExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 9 | characters.views.wraith.wraith_chargen.WraithFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 10 | characters.views.wraith.wraith_chargen.WraithLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 11 | characters.views.wraith.wraith_chargen.WraithAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 12 | characters.views.wraith.wraith_chargen.WraithMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 13 | characters.views.wraith.wraith_chargen.WraithContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | 14 | characters.views.wraith.wraith_chargen.WraithSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wraith/<int:pk>/chargen/ | <default> | characters.views.wraith.wraith.WraithDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ |  | characters.views.wraith.wtohuman.WtOHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 1 | characters.views.wraith.wtohuman.WtOHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 2 | characters.views.wraith.wtohuman.WtOHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 3 | characters.views.wraith.wtohuman.WtOHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 4 | characters.views.wraith.wtohuman.WtOHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 5 | characters.views.wraith.wtohuman.WtOHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 6 | characters.views.wraith.wtohuman.WtOHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 7 | characters.views.wraith.wtohuman.WtOHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | 8 | characters.views.wraith.wtohuman.WtOHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/chargen/ | <default> | characters.views.wraith.wtohuman.WtOHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/template/ |  | characters.views.wraith.wtohuman.WtOHumanTemplateSelectView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/wraith/wtohuman/<int:pk>/creation/ |  | characters.views.wraith.wtohuman.WtOHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/wraith/wtohuman/<int:pk>/creation/ | 1 | characters.views.wraith.wtohuman.WtOHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | 2 | characters.views.wraith.wtohuman.WtOHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | 3 | characters.views.wraith.wtohuman.WtOHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | 4 | characters.views.wraith.wtohuman.WtOHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | 5 | characters.views.wraith.wtohuman.WtOHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | 6 | characters.views.wraith.wtohuman.WtOHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | 7 | characters.views.wraith.wtohuman.WtOHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | 8 | characters.views.wraith.wtohuman.WtOHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/wraith/wtohuman/<int:pk>/creation/ | <default> | characters.views.wraith.wtohuman.WtOHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/create/changeling/ |  | characters.views.changeling.changeling.ChangelingBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/motley/ |  | characters.views.changeling.motley.MotleyCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/kith/ |  | characters.views.changeling.kith.KithCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/house/ |  | characters.views.changeling.house.HouseCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/house_faction/ |  | characters.views.changeling.house_faction.HouseFactionCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/legacy/ |  | characters.views.changeling.legacy.LegacyCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/ctdhuman/ |  | characters.views.changeling.ctdhuman.CtDHumanBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/inanimae/ |  | characters.views.changeling.inanimae.InanimaeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/nunnehi/ |  | characters.views.changeling.nunnehi.NunnehiCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/autumn_person/ |  | characters.views.changeling.autumn_person.AutumnPersonCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/cantrip/ |  | characters.views.changeling.cantrip.CantripCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/create/chimera/ |  | characters.views.changeling.chimera.ChimeraCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/changeling/update/changeling/<pk>/ |  | characters.views.changeling.changeling.ChangelingUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/changeling/full/<pk>/ |  | characters.views.changeling.changeling.ChangelingUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/motley/<pk>/ |  | characters.views.changeling.motley.MotleyUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/kith/<pk>/ |  | characters.views.changeling.kith.KithUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/house/<pk>/ |  | characters.views.changeling.house.HouseUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/house_faction/<pk>/ |  | characters.views.changeling.house_faction.HouseFactionUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/legacy/<pk>/ |  | characters.views.changeling.legacy.LegacyUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/ctdhuman/<pk>/ |  | characters.views.changeling.ctdhuman.CtDHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/ctdhuman/full/<pk>/ |  | characters.views.changeling.ctdhuman.CtDHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/inanimae/<pk>/ |  | characters.views.changeling.inanimae.InanimaeUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/nunnehi/<pk>/ |  | characters.views.changeling.nunnehi.NunnehiUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/autumn_person/<pk>/ |  | characters.views.changeling.autumn_person.AutumnPersonUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/cantrip/<pk>/ |  | characters.views.changeling.cantrip.CantripUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/update/chimera/<pk>/ |  | characters.views.changeling.chimera.ChimeraUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/list/cantrip/ |  | characters.views.changeling.cantrip.CantripListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/changeling/list/chimera/ |  | characters.views.changeling.chimera.ChimeraListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/changeling/list/kith/ |  | characters.views.changeling.kith.KithListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/changeling/list/house/ |  | characters.views.changeling.house.HouseListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/changeling/list/house_faction/ |  | characters.views.changeling.house_faction.HouseFactionListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/changeling/list/legacy/ |  | characters.views.changeling.legacy.LegacyListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/changeling/list/motley/ |  | characters.views.changeling.motley.MotleyListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/changeling/autumn_person/<pk>/ |  | characters.views.changeling.autumn_person.AutumnPersonDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/inanimae/<pk>/ |  | characters.views.changeling.inanimae.InanimaeDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/nunnehi/<pk>/ |  | characters.views.changeling.nunnehi.NunnehiDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/kith/<pk>/ |  | characters.views.changeling.kith.KithDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/house/<pk>/ |  | characters.views.changeling.house.HouseDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/house_faction/<pk>/ |  | characters.views.changeling.house_faction.HouseFactionDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/legacy/<pk>/ |  | characters.views.changeling.legacy.LegacyDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/template/ |  | characters.views.changeling.ctdhuman.CtDHumanTemplateSelectView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/changeling/ctdhuman/<int:pk>/creation/ |  | characters.views.changeling.ctdhuman.CtDHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 1 | characters.views.changeling.ctdhuman.CtDHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 2 | characters.views.changeling.ctdhuman.CtDHumanAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 3 | characters.views.changeling.ctdhuman.CtDHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 4 | characters.views.changeling.ctdhuman.CtDHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 5 | characters.views.changeling.ctdhuman.CtDHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 6 | characters.views.changeling.ctdhuman.CtDHumanLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 7 | characters.views.changeling.ctdhuman.CtDHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | 8 | characters.views.changeling.ctdhuman.CtDHumanSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/changeling/ctdhuman/<int:pk>/creation/ | <default> | characters.views.changeling.ctdhuman.CtDHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/changeling/<pk>/ |  | characters.views.changeling.changeling.ChangelingDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/motley/<pk>/ |  | characters.views.changeling.motley.MotleyDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/cantrip/<pk>/ |  | characters.views.changeling.cantrip.CantripDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/changeling/chimera/<pk>/ |  | characters.views.changeling.chimera.ChimeraDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/create/apocalyptic_trait/ |  | characters.views.demon.apocalyptic_trait.ApocalypticFormTraitCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/demon/ |  | characters.views.demon.demon_chargen.DemonBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/dtfhuman/ |  | characters.views.demon.dtfhuman_chargen.DtFHumanBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/thrall/ |  | characters.views.demon.thrall_chargen.ThrallBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/earthbound/ |  | characters.views.demon.earthbound.EarthboundCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/conclave/ |  | characters.views.demon.conclave.ConclaveCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/faction/ |  | characters.views.demon.faction.DemonFactionCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/house/ |  | characters.views.demon.house.DemonHouseCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/visage/ |  | characters.views.demon.visage.VisageCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/lore/ |  | characters.views.demon.lore.LoreCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/demon/create/pact/ |  | characters.views.demon.pact.PactCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/demon/update/apocalyptic_trait/<int:pk>/ |  | characters.views.demon.apocalyptic_trait.ApocalypticFormTraitUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/demon/<int:pk>/ |  | characters.views.demon.demon.DemonUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/dtfhuman/<int:pk>/ |  | characters.views.demon.dtfhuman.DtFHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/thrall/<int:pk>/ |  | characters.views.demon.thrall.ThrallUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/earthbound/<int:pk>/ |  | characters.views.demon.earthbound.EarthboundUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/conclave/<int:pk>/ |  | characters.views.demon.conclave.ConclaveUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/faction/<int:pk>/ |  | characters.views.demon.faction.DemonFactionUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/house/<int:pk>/ |  | characters.views.demon.house.DemonHouseUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/visage/<int:pk>/ |  | characters.views.demon.visage.VisageUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/lore/<int:pk>/ |  | characters.views.demon.lore.LoreUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/update/pact/<int:pk>/ |  | characters.views.demon.pact.PactUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/demon/update/ritual/<int:pk>/ |  | characters.views.demon.ritual.RitualUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/list/apocalyptic_trait/ |  | characters.views.demon.apocalyptic_trait.ApocalypticFormTraitListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/conclave/ |  | characters.views.demon.conclave.ConclaveListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/demon/ |  | characters.views.demon.demon.DemonListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/dtfhuman/ |  | characters.views.demon.dtfhuman.DtFHumanListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/thrall/ |  | characters.views.demon.thrall.ThrallListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/earthbound/ |  | characters.views.demon.earthbound.EarthboundListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/faction/ |  | characters.views.demon.faction.DemonFactionListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/house/ |  | characters.views.demon.house.DemonHouseListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/visage/ |  | characters.views.demon.visage.VisageListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/lore/ |  | characters.views.demon.lore.LoreListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/list/pact/ |  | characters.views.demon.pact.PactListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/demon/list/ritual/ |  | characters.views.demon.ritual.RitualListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/demon/apocalyptic_trait/<int:pk>/ |  | characters.views.demon.apocalyptic_trait.ApocalypticFormTraitDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/conclave/<int:pk>/ |  | characters.views.demon.conclave.ConclaveDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/demon/<int:pk>/ |  | characters.views.demon.demon.DemonDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/ |  | characters.views.demon.dtfhuman.DtFHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/thrall/<int:pk>/ |  | characters.views.demon.thrall.ThrallDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/earthbound/<int:pk>/ |  | characters.views.demon.earthbound.EarthboundDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/faction/<int:pk>/ |  | characters.views.demon.faction.DemonFactionDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/house/<int:pk>/ |  | characters.views.demon.house.DemonHouseDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/visage/<int:pk>/ |  | characters.views.demon.visage.VisageDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/lore/<int:pk>/ |  | characters.views.demon.lore.LoreDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/pact/<int:pk>/ |  | characters.views.demon.pact.PactDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/demon/ritual/<int:pk>/ |  | characters.views.demon.ritual.RitualDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ |  | characters.views.demon.demon_chargen.DemonCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/demon/demon/<int:pk>/chargen/ | 1 | characters.views.demon.demon_chargen.DemonAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 2 | characters.views.demon.demon_chargen.DemonAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 3 | characters.views.demon.demon_chargen.DemonBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 4 | characters.views.demon.demon_chargen.DemonLoresView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 5 | characters.views.demon.demon_chargen.DemonApocalypticFormView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 6 | characters.views.demon.demon_chargen.DemonVirtuesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 7 | characters.views.demon.demon_chargen.DemonExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 8 | characters.views.demon.demon_chargen.DemonFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 9 | characters.views.demon.demon_chargen.DemonLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 10 | characters.views.demon.demon_chargen.DemonAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 11 | characters.views.demon.demon_chargen.DemonMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 12 | characters.views.demon.demon_chargen.DemonContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 13 | characters.views.demon.demon_chargen.DemonRetainersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 14 | characters.views.demon.demon_chargen.DemonFollowersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | 15 | characters.views.demon.demon_chargen.DemonSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/demon/<int:pk>/chargen/ | <default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/demon/dtfhuman/<int:pk>/chargen/ |  | characters.views.demon.dtfhuman_chargen.DtFHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 1 | characters.views.demon.dtfhuman_chargen.DtFHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 2 | characters.views.demon.dtfhuman_chargen.DtFHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 3 | characters.views.demon.dtfhuman_chargen.DtFHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 4 | characters.views.demon.dtfhuman_chargen.DtFHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 5 | characters.views.demon.dtfhuman_chargen.DtFHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 6 | characters.views.demon.dtfhuman_chargen.DtFHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 7 | characters.views.demon.dtfhuman_chargen.DtFHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | 8 | characters.views.demon.dtfhuman_chargen.DtFHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/chargen/ | <default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/demon/thrall/<int:pk>/chargen/ |  | characters.views.demon.thrall_chargen.ThrallCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/demon/thrall/<int:pk>/chargen/ | 1 | characters.views.demon.thrall_chargen.ThrallAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 2 | characters.views.demon.thrall_chargen.ThrallAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 3 | characters.views.demon.thrall_chargen.ThrallBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 4 | characters.views.demon.thrall_chargen.ThrallVirtuesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 5 | characters.views.demon.thrall_chargen.ThrallExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 6 | characters.views.demon.thrall_chargen.ThrallFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 7 | characters.views.demon.thrall_chargen.ThrallLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 8 | characters.views.demon.thrall_chargen.ThrallAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | 9 | characters.views.demon.thrall_chargen.ThrallSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/thrall/<int:pk>/chargen/ | <default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/demon/dtfhuman/<int:pk>/template/ |  | characters.views.demon.dtfhuman_chargen.DtFHumanTemplateSelectView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/demon/dtfhuman/<int:pk>/creation/ |  | characters.views.demon.dtfhuman_chargen.DtFHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/demon/dtfhuman/<int:pk>/creation/ | 1 | characters.views.demon.dtfhuman_chargen.DtFHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | 2 | characters.views.demon.dtfhuman_chargen.DtFHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | 3 | characters.views.demon.dtfhuman_chargen.DtFHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | 4 | characters.views.demon.dtfhuman_chargen.DtFHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | 5 | characters.views.demon.dtfhuman_chargen.DtFHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | 6 | characters.views.demon.dtfhuman_chargen.DtFHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | 7 | characters.views.demon.dtfhuman_chargen.DtFHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | 8 | characters.views.demon.dtfhuman_chargen.DtFHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/demon/dtfhuman/<int:pk>/creation/ | <default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/mummy/create/mtrhuman/ |  | characters.views.mummy.mtr_human.MtRHumanCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mummy/create/mummy/ |  | characters.views.mummy.mummy.MummyCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/mummy/create/dynasty/ |  | characters.views.mummy.dynasty.DynastyCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/mummy/create/title/ |  | characters.views.mummy.mummy_title.MummyTitleCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/mummy/update/mtrhuman/<pk>/ |  | characters.views.mummy.mtr_human.MtRHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mummy/update/mummy/<pk>/ |  | characters.views.mummy.mummy.MummyUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/mummy/update/dynasty/<pk>/ |  | characters.views.mummy.dynasty.DynastyUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/mummy/update/title/<pk>/ |  | characters.views.mummy.mummy_title.MummyTitleUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/mummy/list/mtrhuman/ |  | characters.views.mummy.mtr_human.MtRHumanListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mummy/list/mummy/ |  | characters.views.mummy.mummy.MummyListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/mummy/list/dynasty/ |  | characters.views.mummy.dynasty.DynastyListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/mummy/list/title/ |  | characters.views.mummy.mummy_title.MummyTitleListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/mummy/mtrhuman/<pk>/ |  | characters.views.mummy.mtr_human.MtRHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mummy/mummy/<pk>/ |  | characters.views.mummy.mummy.MummyDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/mummy/dynasty/<pk>/ |  | characters.views.mummy.dynasty.DynastyDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/mummy/title/<pk>/ |  | characters.views.mummy.mummy_title.MummyTitleDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/hunter/create/hunter/ |  | characters.views.hunter.hunter.HunterCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/hunter/create/htrhuman/ |  | characters.views.hunter.htrhuman.HtRHumanCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/hunter/create/creed/ |  | characters.views.hunter.creed.CreedCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/hunter/create/edge/ |  | characters.views.hunter.edge.EdgeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/hunter/create/organization/ |  | characters.views.hunter.organization.HunterOrganizationCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/hunter/update/hunter/<int:pk>/ |  | characters.views.hunter.hunter.HunterUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/hunter/update/htrhuman/<int:pk>/ |  | characters.views.hunter.htrhuman.HtRHumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/hunter/update/creed/<int:pk>/ |  | characters.views.hunter.creed.CreedUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/hunter/update/edge/<int:pk>/ |  | characters.views.hunter.edge.EdgeUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/hunter/update/organization/<int:pk>/ |  | characters.views.hunter.organization.HunterOrganizationUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| characters/hunter/list/hunter/ |  | characters.views.hunter.hunter.HunterListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/hunter/list/htrhuman/ |  | characters.views.hunter.htrhuman.HtRHumanListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/hunter/list/creed/ |  | characters.views.hunter.creed.CreedListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/hunter/list/edge/ |  | characters.views.hunter.edge.EdgeListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/hunter/list/organization/ |  | characters.views.hunter.organization.HunterOrganizationListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/hunter/hunter/<int:pk>/ |  | characters.views.hunter.hunter.HunterDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/hunter/htrhuman/<int:pk>/ |  | characters.views.hunter.htrhuman.HtRHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/hunter/creed/<int:pk>/ |  | characters.views.hunter.creed.CreedDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/hunter/edge/<int:pk>/ |  | characters.views.hunter.edge.EdgeDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/hunter/organization/<int:pk>/ |  | characters.views.hunter.organization.HunterOrganizationDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| characters/ajax/load_examples/ |  | characters.views.core.human.LoadExamplesView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/ajax/load_values/ |  | characters.views.core.human.LoadValuesView | AjaxLoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/create/character/ |  | characters.views.core.character.CharacterCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/create/group/ |  | characters.views.core.group.GroupCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/create/human/ |  | characters.views.core.human.HumanBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/create/human/full/ |  | characters.views.core.human.HumanCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/create/npc/ |  | characters.views.core.npc.NPCProfileCreateView | LoginRequiredMixin | yes | GET,POST,OPTIONS,HEAD | object-permission: create policy |
| characters/create/npc/<int:pk>/ |  | characters.views.core.npc.NPCProfileCreateView | LoginRequiredMixin | yes | GET,POST,OPTIONS,HEAD | object-permission: create policy |
| characters/create/archetypes/ |  | characters.views.core.archetype.ArchetypeCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/create/meritflaws/ |  | characters.views.core.meritflaw.MeritFlawCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/create/specialties/ |  | characters.views.core.specialty.SpecialtyCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/create/derangement/ |  | characters.views.core.derangement.DerangementCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| characters/update/character/<pk>/ |  | characters.views.core.character.CharacterUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/update/group/<pk>/ |  | characters.views.core.group.GroupUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/update/human/full/<pk>/ |  | characters.views.core.human.HumanUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/update/human/<pk>/ |  | characters.views.core.human.HumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/update/human/<pk>/ | 1 | characters.views.core.human.HumanAttributeChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/update/human/<pk>/ | 2 | characters.views.core.human.HumanAbilityChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/update/human/<pk>/ | 3 | characters.views.core.human.HumanBackgroundsChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/update/human/<pk>/ | 4 | characters.views.core.human.HumanBiographicalInformationChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/update/human/<pk>/ | 5 | characters.views.core.human.HumanFreebiesChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/update/human/<pk>/ | 6 | characters.views.core.human.HumanLanguagesChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/update/human/<pk>/ | 7 | characters.views.core.human.HumanSpecialtiesChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/update/human/<pk>/ | <default> | characters.views.core.human.HumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/update/archetypes/<pk>/ |  | characters.views.core.archetype.ArchetypeUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/update/meritflaws/<pk>/ |  | characters.views.core.meritflaw.MeritFlawUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/update/specialties/<pk>/ |  | characters.views.core.specialty.SpecialtyUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/update/derangement/<pk>/ |  | characters.views.core.derangement.DerangementUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| characters/list/archetypes/ |  | characters.views.core.archetype.ArchetypeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/list/meritflaws/ |  | characters.views.core.meritflaw.MeritFlawListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/list/specialties/ |  | characters.views.core.specialty.SpecialtyListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/list/derangement/ |  | characters.views.core.derangement.DerangementListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| characters/index/ |  | characters.views.core.CharacterIndexView | none | no | GET,POST,OPTIONS,HEAD | login-only: filtered collection |
| characters/retired/ |  | characters.views.core.RetiredCharacterIndex | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/deceased/ |  | characters.views.core.DeceasedCharacterIndex | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/npc/ |  | characters.views.core.NPCCharacterIndex | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| characters/groups/<pk>/ |  | characters.views.core.GenericGroupDetailView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/groups/<pk>/ | group | characters.views.core.group.GroupDetailView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/groups/<pk>/ | pack | characters.views.werewolf.pack.PackDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/groups/<pk>/ | cabal | characters.views.mage.cabal.CabalDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/groups/<pk>/ | motley | characters.views.changeling.motley.MotleyDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/groups/<pk>/ | coterie | characters.views.vampire.coterie.CoterieDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/groups/<pk>/ | circle | characters.views.wraith.circle.CircleDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/groups/<pk>/ | conclave | characters.views.demon.conclave.ConclaveDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/archetypes/<pk>/ |  | characters.views.core.archetype.ArchetypeDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/meritflaws/<pk>/ |  | characters.views.core.meritflaw.MeritFlawDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/specialties/<pk>/ |  | characters.views.core.specialty.SpecialtyDetailView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/derangement/<pk>/ |  | characters.views.core.derangement.DerangementDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<int:pk>/chargen/back/ |  | characters.views.core.chargen_back.ChargenBackView | LoginRequiredMixin | yes | POST | object-permission: object/action policy |
| characters/<pk>/ |  | characters.views.core.GenericCharacterDetailView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | human | characters.views.core.human.HumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | human/1 | characters.views.core.human.HumanAttributeChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | human/2 | characters.views.core.human.HumanAbilityChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | human/3 | characters.views.core.human.HumanBackgroundsChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | human/4 | characters.views.core.human.HumanBiographicalInformationChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | human/5 | characters.views.core.human.HumanFreebiesChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | human/6 | characters.views.core.human.HumanLanguagesChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | human/7 | characters.views.core.human.HumanSpecialtiesChargenView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | human/<default> | characters.views.core.human.HumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | vtm_human | characters.views.vampire.vtmhuman.VtMHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | vtm_human/1 | characters.views.vampire.vtmhuman.VtMHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/2 | characters.views.vampire.vtmhuman.VtMHumanAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/3 | characters.views.vampire.vtmhuman.VtMHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/4 | characters.views.vampire.vtmhuman.VtMHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/5 | characters.views.vampire.vtmhuman.VtMHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/6 | characters.views.vampire.vtmhuman.VtMHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/7 | characters.views.vampire.vtmhuman.VtMHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/8 | characters.views.vampire.vtmhuman.VtMHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vtm_human/<default> | characters.views.vampire.vtmhuman.VtMHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | vampire | characters.views.vampire.vampire_chargen.VampireCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | vampire/1 | characters.views.vampire.vampire_chargen.VampireAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/2 | characters.views.vampire.vampire_chargen.VampireAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/3 | characters.views.vampire.vampire_chargen.VampireBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/4 | characters.views.vampire.vampire_chargen.VampireDisciplinesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/5 | characters.views.vampire.vampire_chargen.VampireVirtuesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/6 | characters.views.vampire.vampire_chargen.VampireExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/7 | characters.views.vampire.vampire_chargen.VampireFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/8 | characters.views.vampire.vampire_chargen.VampireLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/9 | characters.views.vampire.vampire_chargen.VampireAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/10 | characters.views.vampire.vampire_chargen.VampireMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/11 | characters.views.vampire.vampire_chargen.VampireContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/12 | characters.views.vampire.vampire_chargen.VampireRetainersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/13 | characters.views.vampire.vampire_chargen.VampireSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | vampire/<default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/<pk>/ | ghoul | characters.views.vampire.ghoul_chargen.GhoulCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | ghoul/1 | characters.views.vampire.ghoul_chargen.GhoulAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/2 | characters.views.vampire.ghoul_chargen.GhoulAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/3 | characters.views.vampire.ghoul_chargen.GhoulBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/4 | characters.views.vampire.ghoul_chargen.GhoulDisciplinesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/5 | characters.views.vampire.ghoul_chargen.GhoulExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/6 | characters.views.vampire.ghoul_chargen.GhoulFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/7 | characters.views.vampire.ghoul_chargen.GhoulLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/8 | characters.views.vampire.ghoul_chargen.GhoulAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/9 | characters.views.vampire.ghoul_chargen.GhoulSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ghoul/<default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/<pk>/ | revenant | characters.views.vampire.revenant.RevenantDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | wta_human | characters.views.werewolf.wtahuman.WtAHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | wta_human/1 | characters.views.werewolf.wtahuman.WtAHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/2 | characters.views.werewolf.wtahuman.WtAHumanAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/3 | characters.views.werewolf.wtahuman.WtAHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/4 | characters.views.werewolf.wtahuman.WtAHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/5 | characters.views.werewolf.wtahuman.WtAHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/6 | characters.views.werewolf.wtahuman.WtAHumanLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/7 | characters.views.werewolf.wtahuman.WtAHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/8 | characters.views.werewolf.wtahuman.WtAHumanSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wta_human/<default> | characters.views.werewolf.wtahuman.WtAHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | werewolf | characters.views.werewolf.garou.WerewolfCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | werewolf/1 | characters.views.werewolf.garou.WerewolfAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/2 | characters.views.werewolf.garou.WerewolfAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/3 | characters.views.werewolf.garou.WerewolfBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/4 | characters.views.werewolf.garou.WerewolfGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/5 | characters.views.werewolf.garou.WerewolfHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/6 | characters.views.werewolf.garou.WerewolfExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/7 | characters.views.werewolf.garou.WerewolfFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/8 | characters.views.werewolf.garou.WerewolfLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/9 | characters.views.werewolf.garou.WerewolfAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/10 | characters.views.werewolf.garou.WerewolfMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/11 | characters.views.werewolf.garou.WerewolfContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/12 | characters.views.werewolf.garou.WerewolfSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | werewolf/<default> | characters.views.werewolf.garou.WerewolfDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | spirit_character | characters.views.werewolf.spirit.SpiritDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | kinfolk | characters.views.werewolf.kinfolk.KinfolkCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | kinfolk/1 | characters.views.werewolf.kinfolk.KinfolkAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/2 | characters.views.werewolf.kinfolk.KinfolkAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/3 | characters.views.werewolf.kinfolk.KinfolkBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/4 | characters.views.werewolf.kinfolk.KinfolkExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/5 | characters.views.werewolf.kinfolk.KinfolkFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/6 | characters.views.werewolf.kinfolk.KinfolkLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/7 | characters.views.werewolf.kinfolk.KinfolkAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/8 | characters.views.werewolf.kinfolk.KinfolkSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kinfolk/<default> | characters.views.werewolf.kinfolk.KinfolkDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | fomor | characters.views.werewolf.fomor.FomorCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | fomor/1 | characters.views.werewolf.fomor.FomorAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/2 | characters.views.werewolf.fomor.FomorAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/3 | characters.views.werewolf.fomor.FomorBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/4 | characters.views.werewolf.fomor.FomorPowersView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/5 | characters.views.werewolf.fomor.FomorExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/6 | characters.views.werewolf.fomor.FomorFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/7 | characters.views.werewolf.fomor.FomorLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/8 | characters.views.werewolf.fomor.FomorAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/9 | characters.views.werewolf.fomor.FomorContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/10 | characters.views.werewolf.fomor.FomorSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fomor/<default> | characters.views.werewolf.fomor.FomorDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | drone | characters.views.werewolf.drone.DroneCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | drone/1 | characters.views.werewolf.drone.DroneAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | drone/2 | characters.views.werewolf.drone.DroneAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | drone/3 | characters.views.werewolf.drone.DroneBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | drone/4 | characters.views.werewolf.drone.DroneExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | drone/5 | characters.views.werewolf.drone.DroneFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | drone/6 | characters.views.werewolf.drone.DroneLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | drone/7 | characters.views.werewolf.drone.DroneSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | drone/<default> | characters.views.werewolf.drone.DroneDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | fera | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | fera/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | fera/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | ajaba | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | ajaba/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ajaba/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | ananasi | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | ananasi/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ananasi/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | bastet | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | bastet/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | bastet/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | corax | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | corax/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | corax/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | grondr | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | grondr/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | grondr/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | gurahl | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | gurahl/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | gurahl/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | kitsune | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | kitsune/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | kitsune/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | mokole | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | mokole/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mokole/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | nagah | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | nagah/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nagah/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | nuwisha | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | nuwisha/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | nuwisha/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | ratkin | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | ratkin/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ratkin/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | rokea | characters.views.werewolf.fera.FeraCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | rokea/1 | characters.views.werewolf.fera.FeraBreedFactionView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/2 | characters.views.werewolf.fera.FeraAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/3 | characters.views.werewolf.fera.FeraAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/4 | characters.views.werewolf.fera.FeraBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/5 | characters.views.werewolf.fera.FeraGiftsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/6 | characters.views.werewolf.fera.FeraHistoryView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/7 | characters.views.werewolf.fera.FeraExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/8 | characters.views.werewolf.fera.FeraFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/9 | characters.views.werewolf.fera.FeraLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/10 | characters.views.werewolf.fera.FeraAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/11 | characters.views.werewolf.fera.FeraSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | rokea/<default> | characters.views.werewolf.fera.FeraDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | mta_human | characters.views.mage.mtahuman.MtAHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | mta_human/1 | characters.views.mage.mtahuman.MtAHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/2 | characters.views.mage.mtahuman.MtAHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/3 | characters.views.mage.mtahuman.MtAHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/4 | characters.views.mage.mtahuman.MtAHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/5 | characters.views.mage.mtahuman.MtAHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/6 | characters.views.mage.mtahuman.MtAHumanLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/7 | characters.views.mage.mtahuman.MtAHumanNodeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/8 | characters.views.mage.mtahuman.MtAHumanLibraryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/9 | characters.views.mage.mtahuman.MtAHumanWonderView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/10 | characters.views.mage.mtahuman.MtAHumanEnhancementView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/11 | characters.views.mage.mtahuman.MtAHumanSanctumView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/12 | characters.views.mage.mtahuman.MtAHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/13 | characters.views.mage.mtahuman.MtAHumanChantryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/14 | characters.views.mage.mtahuman.MtAHumanSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mta_human/<default> | characters.views.mage.mtahuman.MtAHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | mage | characters.views.mage.mage.MageCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | mage/1 | characters.views.mage.mage.MageAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/2 | characters.views.mage.mage.MageAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/3 | characters.views.mage.mage.MageBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/4 | characters.views.mage.mage.MageSpheresView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/5 | characters.views.mage.mage.MageFocusView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/6 | characters.views.mage.mage.MageExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/7 | characters.views.mage.mage.MageFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/8 | characters.views.mage.mage.MageLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/9 | characters.views.mage.mage.MageRoteView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/10 | characters.views.mage.mage.MageNodeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/11 | characters.views.mage.mage.MageLibraryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/12 | characters.views.mage.mage.MageFamiliarView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/13 | characters.views.mage.mage.MageWonderView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/14 | characters.views.mage.mage.MageEnhancementView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/15 | characters.views.mage.mage.MageSanctumView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/16 | characters.views.mage.mage.MageAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/17 | characters.views.mage.mage.MageMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/18 | characters.views.mage.mage.MageContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/19 | characters.views.mage.mage.MageRetainersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/20 | characters.views.mage.mage.MageChantryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/21 | characters.views.mage.mage.MageSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | mage/<default> | characters.views.mage.mage.MageDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | companion | characters.views.mage.companion.CopanionCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | companion/1 | characters.views.mage.companion.CompanionAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/2 | characters.views.mage.companion.CompanionAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/3 | characters.views.mage.companion.CompanionBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/4 | characters.views.mage.companion.CompanionExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/5 | characters.views.mage.companion.CompanionFreebiesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/6 | characters.views.mage.companion.CompanionLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/7 | characters.views.mage.companion.CompanionNodeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/8 | characters.views.mage.companion.CompanionLibraryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/9 | characters.views.mage.companion.CompanionWonderView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/10 | characters.views.mage.companion.CompanionEnhancementView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/11 | characters.views.mage.companion.CompanionSanctumView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/12 | characters.views.mage.companion.CompanionAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/13 | characters.views.mage.companion.CompanionChantryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/14 | characters.views.mage.companion.CompanionSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | companion/<default> | characters.views.mage.companion.CompanionDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | sorcerer | characters.views.mage.sorcerer.SorcererCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | sorcerer/1 | characters.views.mage.sorcerer.SorcererAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/2 | characters.views.mage.sorcerer.SorcererAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/3 | characters.views.mage.sorcerer.SorcererBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/4 | characters.views.mage.sorcerer.SorcererPsychicView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/5 | characters.views.mage.sorcerer.SorcererPathView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/6 | characters.views.mage.sorcerer.SorcererRitualView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/7 | characters.views.mage.sorcerer.SorcererExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/8 | characters.views.mage.sorcerer.SorcererFreebiesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/9 | characters.views.mage.sorcerer.SorcererLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/10 | characters.views.mage.sorcerer.SorcererNodeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/11 | characters.views.mage.sorcerer.SorcererLibraryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/12 | characters.views.mage.sorcerer.SorcererFamiliarView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/13 | characters.views.mage.sorcerer.SorcererArtifactView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/14 | characters.views.mage.sorcerer.SorcererEnhancementView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/15 | characters.views.mage.sorcerer.SorcererSanctumView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/16 | characters.views.mage.sorcerer.SorcererAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/17 | characters.views.mage.sorcerer.SorcererChantryView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/18 | characters.views.mage.sorcerer.SorcererSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | sorcerer/<default> | characters.views.mage.sorcerer.SorcererDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | ctd_human | characters.views.changeling.ctdhuman.CtDHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | ctd_human/1 | characters.views.changeling.ctdhuman.CtDHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/2 | characters.views.changeling.ctdhuman.CtDHumanAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/3 | characters.views.changeling.ctdhuman.CtDHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/4 | characters.views.changeling.ctdhuman.CtDHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/5 | characters.views.changeling.ctdhuman.CtDHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/6 | characters.views.changeling.ctdhuman.CtDHumanLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/7 | characters.views.changeling.ctdhuman.CtDHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/8 | characters.views.changeling.ctdhuman.CtDHumanSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | ctd_human/<default> | characters.views.changeling.ctdhuman.CtDHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | changeling | characters.views.changeling.changeling.ChangelingCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | changeling/1 | characters.views.changeling.changeling.ChangelingAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/2 | characters.views.changeling.changeling.ChangelingAbilityView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/3 | characters.views.changeling.changeling.ChangelingBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/4 | characters.views.changeling.changeling.ChangelingArtsRealmsView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/5 | characters.views.changeling.changeling.ChangelingExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/6 | characters.views.changeling.changeling.ChangelingFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/7 | characters.views.changeling.changeling.ChangelingLanguagesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/8 | characters.views.changeling.changeling.ChangelingAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/9 | characters.views.changeling.changeling.ChangelingSpecialtiesView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | changeling/<default> | characters.views.changeling.changeling.ChangelingDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | autumn_person | characters.views.changeling.autumn_person.AutumnPersonDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | inanimae | characters.views.changeling.inanimae.InanimaeDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | nunnehi | characters.views.changeling.nunnehi.NunnehiDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | wto_human | characters.views.wraith.wtohuman.WtOHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | wto_human/1 | characters.views.wraith.wtohuman.WtOHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/2 | characters.views.wraith.wtohuman.WtOHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/3 | characters.views.wraith.wtohuman.WtOHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/4 | characters.views.wraith.wtohuman.WtOHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/5 | characters.views.wraith.wtohuman.WtOHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/6 | characters.views.wraith.wtohuman.WtOHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/7 | characters.views.wraith.wtohuman.WtOHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/8 | characters.views.wraith.wtohuman.WtOHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wto_human/<default> | characters.views.wraith.wtohuman.WtOHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | wraith | characters.views.wraith.wraith_chargen.WraithCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | wraith/1 | characters.views.wraith.wraith_chargen.WraithAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/2 | characters.views.wraith.wraith_chargen.WraithAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/3 | characters.views.wraith.wraith_chargen.WraithBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/4 | characters.views.wraith.wraith_chargen.WraithArcanosView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/5 | characters.views.wraith.wraith_chargen.WraithShadowView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/6 | characters.views.wraith.wraith_chargen.WraithPassionsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/7 | characters.views.wraith.wraith_chargen.WraithFettersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/8 | characters.views.wraith.wraith_chargen.WraithExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/9 | characters.views.wraith.wraith_chargen.WraithFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/10 | characters.views.wraith.wraith_chargen.WraithLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/11 | characters.views.wraith.wraith_chargen.WraithAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/12 | characters.views.wraith.wraith_chargen.WraithMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/13 | characters.views.wraith.wraith_chargen.WraithContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/14 | characters.views.wraith.wraith_chargen.WraithSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | wraith/<default> | characters.views.wraith.wraith.WraithDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | dtf_human | characters.views.demon.dtfhuman_chargen.DtFHumanCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | dtf_human/1 | characters.views.demon.dtfhuman_chargen.DtFHumanAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/2 | characters.views.demon.dtfhuman_chargen.DtFHumanAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/3 | characters.views.demon.dtfhuman_chargen.DtFHumanBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/4 | characters.views.demon.dtfhuman_chargen.DtFHumanExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/5 | characters.views.demon.dtfhuman_chargen.DtFHumanFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/6 | characters.views.demon.dtfhuman_chargen.DtFHumanLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/7 | characters.views.demon.dtfhuman_chargen.DtFHumanAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/8 | characters.views.demon.dtfhuman_chargen.DtFHumanSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | dtf_human/<default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/<pk>/ | demon | characters.views.demon.demon_chargen.DemonCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | demon/1 | characters.views.demon.demon_chargen.DemonAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/2 | characters.views.demon.demon_chargen.DemonAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/3 | characters.views.demon.demon_chargen.DemonBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/4 | characters.views.demon.demon_chargen.DemonLoresView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/5 | characters.views.demon.demon_chargen.DemonApocalypticFormView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/6 | characters.views.demon.demon_chargen.DemonVirtuesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/7 | characters.views.demon.demon_chargen.DemonExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/8 | characters.views.demon.demon_chargen.DemonFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/9 | characters.views.demon.demon_chargen.DemonLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/10 | characters.views.demon.demon_chargen.DemonAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/11 | characters.views.demon.demon_chargen.DemonMentorView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/12 | characters.views.demon.demon_chargen.DemonContactsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/13 | characters.views.demon.demon_chargen.DemonRetainersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/14 | characters.views.demon.demon_chargen.DemonFollowersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/15 | characters.views.demon.demon_chargen.DemonSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | demon/<default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/<pk>/ | thrall | characters.views.demon.thrall_chargen.ThrallCharacterCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| characters/<pk>/ | thrall/1 | characters.views.demon.thrall_chargen.ThrallAttributeView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/2 | characters.views.demon.thrall_chargen.ThrallAbilityView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/3 | characters.views.demon.thrall_chargen.ThrallBackgroundsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/4 | characters.views.demon.thrall_chargen.ThrallVirtuesView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/5 | characters.views.demon.thrall_chargen.ThrallExtrasView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/6 | characters.views.demon.thrall_chargen.ThrallFreebiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/7 | characters.views.demon.thrall_chargen.ThrallLanguagesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/8 | characters.views.demon.thrall_chargen.ThrallAlliesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/9 | characters.views.demon.thrall_chargen.ThrallSpecialtiesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chargen SPEND_FREEBIES or VIEW_FULL |
| characters/<pk>/ | thrall/<default> | django.views.generic.detail.DetailView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| characters/<pk>/ | earthbound | characters.views.demon.earthbound.EarthboundDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | htr_human | characters.views.hunter.htrhuman.HtRHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | hunter | characters.views.hunter.hunter.HunterDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | mtr_human | characters.views.mummy.mtr_human.MtRHumanDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| characters/<pk>/ | mummy | characters.views.mummy.mummy.MummyDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/vampire/create/haven/ |  | locations.views.vampire.HavenCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/vampire/create/domain/ |  | locations.views.vampire.DomainCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/vampire/create/elysium/ |  | locations.views.vampire.ElysiumCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/vampire/create/rack/ |  | locations.views.vampire.RackCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/vampire/create/chantry/ |  | locations.views.vampire.TremereChantryCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/vampire/create/barrens/ |  | locations.views.vampire.BarrensCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/vampire/update/haven/<pk>/ |  | locations.views.vampire.HavenUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/vampire/update/domain/<pk>/ |  | locations.views.vampire.DomainUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/vampire/update/elysium/<pk>/ |  | locations.views.vampire.ElysiumUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/vampire/update/rack/<pk>/ |  | locations.views.vampire.RackUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/vampire/update/chantry/<pk>/ |  | locations.views.vampire.TremereChantryUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/vampire/update/barrens/<pk>/ |  | locations.views.vampire.BarrensUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/vampire/list/havens/ |  | locations.views.vampire.HavenListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/vampire/list/domains/ |  | locations.views.vampire.DomainListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/vampire/list/elysiums/ |  | locations.views.vampire.ElysiumListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/vampire/list/racks/ |  | locations.views.vampire.RackListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/vampire/haven/<pk>/ |  | locations.views.vampire.HavenDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/vampire/domain/<pk>/ |  | locations.views.vampire.DomainDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/vampire/elysium/<pk>/ |  | locations.views.vampire.ElysiumDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/vampire/rack/<pk>/ |  | locations.views.vampire.RackDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/vampire/chantry/<pk>/ |  | locations.views.vampire.TremereChantryDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/vampire/barrens/<pk>/ |  | locations.views.vampire.BarrensDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/werewolf/create/caern/ |  | locations.views.werewolf.caern.CaernCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/werewolf/update/caern/<pk>/ |  | locations.views.werewolf.caern.CaernUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/werewolf/list/caern/ |  | locations.views.werewolf.caern.CaernListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/werewolf/caern/<pk>/ |  | locations.views.werewolf.caern.CaernDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/create/node/ |  | locations.views.mage.node.NodeCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/sector/ |  | locations.views.mage.sector.SectorCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/realm/ |  | locations.views.mage.realm.RealmCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/paradox_realm/ |  | locations.views.mage.paradox_realm.ParadoxRealmCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/sanctum/ |  | locations.views.mage.sanctum.SanctumCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/demesne/ |  | locations.views.mage.demesne.DemesneCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/library/ |  | locations.views.mage.library.LibraryCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/chantry/ |  | locations.views.mage.chantry.ChantryCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mage/create/reality_zone/ |  | locations.views.mage.reality_zone.RealityZoneCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| locations/mage/update/node/<pk>/ |  | locations.views.mage.node.NodeUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/sector/<pk>/ |  | locations.views.mage.sector.SectorUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/library/<pk>/ |  | locations.views.mage.library.LibraryUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/realm/<pk>/ |  | locations.views.mage.realm.RealmUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/paradox_realm/<pk>/ |  | locations.views.mage.paradox_realm.ParadoxRealmUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/sanctum/<pk>/ |  | locations.views.mage.sanctum.SanctumUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/demesne/<pk>/ |  | locations.views.mage.demesne.DemesneUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/chantry/<pk>/ |  | locations.views.mage.chantry.ChantryUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/update/reality_zone/<pk>/ |  | locations.views.mage.reality_zone.RealityZoneUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| locations/mage/list/node/ |  | locations.views.mage.node.NodeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/sector/ |  | locations.views.mage.sector.SectorListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/chantry/ |  | locations.views.mage.chantry.ChantryListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/library/ |  | locations.views.mage.library.LibraryListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/horizon_realm/ |  | locations.views.mage.realm.RealmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/paradox_realm/ |  | locations.views.mage.paradox_realm.ParadoxRealmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/sanctum/ |  | locations.views.mage.sanctum.SanctumListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/demesne/ |  | locations.views.mage.demesne.DemesneListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/list/reality_zone/ |  | locations.views.mage.reality_zone.RealityZoneListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| locations/mage/ajax/load_chantry_examples/ |  | locations.views.mage.chantry.LoadExamplesView | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mage/node/ |  | locations.views.mage.node.NodeListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/sector/ |  | locations.views.mage.sector.SectorListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/chantry/ |  | locations.views.mage.chantry.ChantryListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/library/ |  | locations.views.mage.library.LibraryListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/horizon_realm/ |  | locations.views.mage.realm.RealmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/paradox_realm/ |  | locations.views.mage.paradox_realm.ParadoxRealmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/sanctum/ |  | locations.views.mage.sanctum.SanctumListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/demesne/ |  | locations.views.mage.demesne.DemesneListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mage/reality_zone/ |  | locations.views.mage.reality_zone.RealityZoneListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| locations/mage/node/<pk>/ |  | locations.views.mage.node.NodeDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/sector/<pk>/ |  | locations.views.mage.sector.SectorDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/chantry/<pk>/ |  | locations.views.mage.chantry.ChantryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/library/<pk>/ |  | locations.views.mage.library.LibraryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/horizon_realm/<pk>/ |  | locations.views.mage.realm.RealmDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/paradox_realm/<pk>/ |  | locations.views.mage.paradox_realm.ParadoxRealmDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/sanctum/<pk>/ |  | locations.views.mage.sanctum.SanctumDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/demesne/<pk>/ |  | locations.views.mage.demesne.DemesneDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mage/reality_zone/<pk>/ |  | locations.views.mage.reality_zone.RealityZoneDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| locations/wraith/create/byway/ |  | locations.views.wraith.byway.BywayCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/wraith/create/citadel/ |  | locations.views.wraith.citadel.CitadelCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/wraith/create/freehold/ |  | locations.views.wraith.freehold.WraithFreeholdCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/wraith/create/haunt/ |  | locations.views.wraith.haunt.HauntCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/wraith/create/necropolis/ |  | locations.views.wraith.necropolis.NecropolisCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/wraith/create/nihil/ |  | locations.views.wraith.nihil.NihilCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/wraith/update/byway/<pk>/ |  | locations.views.wraith.byway.BywayUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/wraith/update/citadel/<pk>/ |  | locations.views.wraith.citadel.CitadelUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/wraith/update/freehold/<pk>/ |  | locations.views.wraith.freehold.WraithFreeholdUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/wraith/update/haunt/<pk>/ |  | locations.views.wraith.haunt.HauntUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/wraith/update/necropolis/<pk>/ |  | locations.views.wraith.necropolis.NecropolisUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/wraith/update/nihil/<pk>/ |  | locations.views.wraith.nihil.NihilUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/wraith/list/byway/ |  | locations.views.wraith.byway.BywayListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/wraith/list/citadel/ |  | locations.views.wraith.citadel.CitadelListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/wraith/list/freehold/ |  | locations.views.wraith.freehold.WraithFreeholdListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/wraith/list/haunt/ |  | locations.views.wraith.haunt.HauntListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/wraith/list/necropolis/ |  | locations.views.wraith.necropolis.NecropolisListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/wraith/list/nihil/ |  | locations.views.wraith.nihil.NihilListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/wraith/byway/<pk>/ |  | locations.views.wraith.byway.BywayDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/wraith/citadel/<pk>/ |  | locations.views.wraith.citadel.CitadelDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/wraith/freehold/<pk>/ |  | locations.views.wraith.freehold.WraithFreeholdDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/wraith/haunt/<pk>/ |  | locations.views.wraith.haunt.HauntDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/wraith/necropolis/<pk>/ |  | locations.views.wraith.necropolis.NecropolisDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/wraith/nihil/<pk>/ |  | locations.views.wraith.nihil.NihilDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/changeling/create/freehold/ |  | locations.views.changeling.creation.FreeholdBasicsView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/changeling/create/freehold/direct/ |  | locations.views.changeling.freehold.FreeholdCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/changeling/create/holding/ |  | locations.views.changeling.holding.HoldingCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/changeling/create/trod/ |  | locations.views.changeling.trod.TrodCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/changeling/create/dream_realm/ |  | locations.views.changeling.dream_realm.DreamRealmCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/changeling/update/freehold/<int:pk>/ |  | locations.views.changeling.creation.FreeholdCreationView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| locations/changeling/update/freehold/<int:pk>/ | 1 | locations.views.changeling.creation.FreeholdFeaturesView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/changeling/update/freehold/<int:pk>/ | 2 | locations.views.changeling.creation.FreeholdPowersView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/changeling/update/freehold/<int:pk>/ | 3 | locations.views.changeling.creation.FreeholdDetailsView | Permission.SPEND_FREEBIES | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/changeling/update/freehold/<int:pk>/ | <default> | locations.views.changeling.freehold.FreeholdDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/changeling/update/freehold/<int:pk>/direct/ |  | locations.views.changeling.freehold.FreeholdUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/changeling/update/holding/<int:pk>/ |  | locations.views.changeling.holding.HoldingUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/changeling/update/trod/<int:pk>/ |  | locations.views.changeling.trod.TrodUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/changeling/update/dream_realm/<int:pk>/ |  | locations.views.changeling.dream_realm.DreamRealmUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/changeling/list/freehold/ |  | locations.views.changeling.freehold.FreeholdListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/changeling/list/holding/ |  | locations.views.changeling.holding.HoldingListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/changeling/list/trod/ |  | locations.views.changeling.trod.TrodListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/changeling/list/dream_realm/ |  | locations.views.changeling.dream_realm.DreamRealmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/changeling/freehold/<int:pk>/ |  | locations.views.changeling.freehold.FreeholdDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/changeling/dream_realm/<int:pk>/ |  | locations.views.changeling.dream_realm.DreamRealmDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/changeling/holding/<int:pk>/ |  | locations.views.changeling.holding.HoldingDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/changeling/trod/<int:pk>/ |  | locations.views.changeling.trod.TrodDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/demon/create/bastion/ |  | locations.views.demon.bastion.BastionCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/demon/create/reliquary/ |  | locations.views.demon.reliquary.ReliquaryCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/demon/update/bastion/<pk>/ |  | locations.views.demon.bastion.BastionUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/demon/update/reliquary/<pk>/ |  | locations.views.demon.reliquary.ReliquaryUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/demon/list/bastion/ |  | locations.views.demon.bastion.BastionListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/demon/list/reliquary/ |  | locations.views.demon.reliquary.ReliquaryListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/demon/bastion/<pk>/ |  | locations.views.demon.bastion.BastionDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/demon/reliquary/<pk>/ |  | locations.views.demon.reliquary.ReliquaryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mummy/create/tomb/ |  | locations.views.mummy.TombCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mummy/create/cult_temple/ |  | locations.views.mummy.CultTempleCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mummy/create/sanctuary/ |  | locations.views.mummy.UndergroundSanctuaryCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/mummy/update/tomb/<int:pk>/ |  | locations.views.mummy.TombUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mummy/update/cult_temple/<int:pk>/ |  | locations.views.mummy.CultTempleUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mummy/update/sanctuary/<int:pk>/ |  | locations.views.mummy.UndergroundSanctuaryUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/mummy/list/tomb/ |  | locations.views.mummy.TombListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mummy/list/cult_temple/ |  | locations.views.mummy.CultTempleListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mummy/list/sanctuary/ |  | locations.views.mummy.UndergroundSanctuaryListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/mummy/tomb/<int:pk>/ |  | locations.views.mummy.TombDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mummy/cult_temple/<int:pk>/ |  | locations.views.mummy.CultTempleDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/mummy/sanctuary/<int:pk>/ |  | locations.views.mummy.UndergroundSanctuaryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/hunter/create/safehouse/ |  | locations.views.hunter.safehouse.SafehouseCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/hunter/create/hunting-ground/ |  | locations.views.hunter.huntingground.HuntingGroundCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/hunter/update/safehouse/<pk>/ |  | locations.views.hunter.safehouse.SafehouseUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/hunter/update/hunting-ground/<pk>/ |  | locations.views.hunter.huntingground.HuntingGroundUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/hunter/list/safehouses/ |  | locations.views.hunter.safehouse.SafehouseListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/hunter/list/hunting-grounds/ |  | locations.views.hunter.huntingground.HuntingGroundListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/hunter/safehouse/ |  | locations.views.hunter.safehouse.SafehouseListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/hunter/safehouse/<pk>/ |  | locations.views.hunter.safehouse.SafehouseDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/hunter/hunting-ground/ |  | locations.views.hunter.huntingground.HuntingGroundListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/hunter/hunting-ground/<pk>/ |  | locations.views.hunter.huntingground.HuntingGroundDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/create/location/ |  | locations.views.core.location.LocationCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/create/city/ |  | locations.views.core.city.CityCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| locations/update/location/<pk>/ |  | locations.views.core.location.LocationUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/update/city/<pk>/ |  | locations.views.core.city.CityUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| locations/list/city/ |  | locations.views.core.city.CityListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| locations/index/ |  | locations.views.core.LocationIndexView | none | no | GET,POST,OPTIONS,HEAD | login-only: filtered collection |
| locations/city/<pk>/ |  | locations.views.core.city.CityDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ |  | locations.views.core.GenericLocationDetailView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| locations/<pk>/ | location | locations.views.core.location.LocationDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | city | locations.views.core.city.CityDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | node | locations.views.mage.node.NodeDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | sector | locations.views.mage.sector.SectorDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | library | locations.views.mage.library.LibraryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | horizon_realm | locations.views.mage.realm.RealmDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | paradox_realm | locations.views.mage.paradox_realm.ParadoxRealmDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | sanctum | locations.views.mage.sanctum.SanctumDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | chantry | locations.views.mage.chantry.ChantryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | reality_zone | locations.views.mage.reality_zone.RealityZoneDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| locations/<pk>/ | demesne | locations.views.mage.demesne.DemesneDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | caern | locations.views.werewolf.caern.CaernDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | haven | locations.views.vampire.HavenDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | domain | locations.views.vampire.DomainDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | elysium | locations.views.vampire.ElysiumDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | rack | locations.views.vampire.RackDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | tremere_chantry | locations.views.vampire.TremereChantryDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | barrens | locations.views.vampire.BarrensDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | haunt | locations.views.wraith.haunt.HauntDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | necropolis | locations.views.wraith.necropolis.NecropolisDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | citadel | locations.views.wraith.citadel.CitadelDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | nihil | locations.views.wraith.nihil.NihilDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | byway | locations.views.wraith.byway.BywayDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | wraith_freehold | locations.views.wraith.freehold.WraithFreeholdDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | freehold | locations.views.changeling.freehold.FreeholdDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | dream_realm | locations.views.changeling.dream_realm.DreamRealmDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | trod | locations.views.changeling.trod.TrodDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | holding | locations.views.changeling.holding.HoldingDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | bastion | locations.views.demon.bastion.BastionDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | reliquary | locations.views.demon.reliquary.ReliquaryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | hunting_ground | locations.views.hunter.huntingground.HuntingGroundDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | safehouse | locations.views.hunter.safehouse.SafehouseDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | tomb | locations.views.mummy.TombDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | cult_temple | locations.views.mummy.CultTempleDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| locations/<pk>/ | underground_sanctuary | locations.views.mummy.UndergroundSanctuaryDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/vampire/create/artifact/ |  | items.views.vampire.VampireArtifactCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/vampire/create/bloodstone/ |  | items.views.vampire.BloodstoneCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/vampire/update/artifact/<pk>/ |  | items.views.vampire.VampireArtifactUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/vampire/update/bloodstone/<pk>/ |  | items.views.vampire.BloodstoneUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/vampire/list/artifacts/ |  | items.views.vampire.VampireArtifactListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/vampire/list/bloodstones/ |  | items.views.vampire.BloodstoneListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/vampire/artifact/<pk>/ |  | items.views.vampire.VampireArtifactDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/vampire/bloodstone/<pk>/ |  | items.views.vampire.BloodstoneDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/werewolf/create/fetish/ |  | items.views.werewolf.fetish.FetishCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/werewolf/create/talen/ |  | items.views.werewolf.talen.TalenCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/werewolf/update/fetish/<pk>/ |  | items.views.werewolf.fetish.FetishUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/werewolf/update/talen/<pk>/ |  | items.views.werewolf.talen.TalenUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/werewolf/list/fetish/ |  | items.views.werewolf.fetish.FetishListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/werewolf/list/talen/ |  | items.views.werewolf.talen.TalenListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/werewolf/fetish/<pk>/ |  | items.views.werewolf.fetish.FetishDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/werewolf/talen/<pk>/ |  | items.views.werewolf.talen.TalenDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mage/create/wonder/ |  | items.views.mage.wonder.WonderCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mage/create/charm/ |  | items.views.mage.charm.CharmCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mage/create/artifact/ |  | items.views.mage.artifact.ArtifactCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mage/create/talisman/ |  | items.views.mage.talisman.TalismanCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mage/create/periapt/ |  | items.views.mage.periapt.PeriaptCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mage/create/grimoire/ |  | items.views.mage.grimoire.GrimoireCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mage/create/sorcerer_artifact/ |  | items.views.mage.sorcerer_artifact.SorcererArtifactCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mage/update/wonder/<pk>/ |  | items.views.mage.wonder.WonderUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mage/update/charm/<pk>/ |  | items.views.mage.charm.CharmUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mage/update/artifact/<pk>/ |  | items.views.mage.artifact.ArtifactUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mage/update/talisman/<pk>/ |  | items.views.mage.talisman.TalismanUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mage/update/periapt/<pk>/ |  | items.views.mage.periapt.PeriaptUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mage/update/grimoire/<pk>/ |  | items.views.mage.grimoire.GrimoireUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mage/update/sorcerer_artifact/<pk>/ |  | items.views.mage.sorcerer_artifact.SorcererArtifactUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mage/list/wonder/ |  | items.views.mage.wonder.WonderListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mage/list/charm/ |  | items.views.mage.charm.CharmListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mage/list/artifact/ |  | items.views.mage.artifact.ArtifactListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mage/list/talisman/ |  | items.views.mage.talisman.TalismanListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mage/list/periapt/ |  | items.views.mage.periapt.PeriaptListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mage/list/grimoire/ |  | items.views.mage.grimoire.GrimoireListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mage/list/sorcerer_artifact/ |  | items.views.mage.sorcerer_artifact.SorcererArtifactListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mage/wonder/<pk>/ |  | items.views.mage.wonder.WonderDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mage/charm/<pk>/ |  | items.views.mage.charm.CharmDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mage/artifact/<pk>/ |  | items.views.mage.artifact.ArtifactDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mage/talisman/<pk>/ |  | items.views.mage.talisman.TalismanDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mage/periapt/<pk>/ |  | items.views.mage.periapt.PeriaptDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mage/grimoire/<pk>/ |  | items.views.mage.grimoire.GrimoireDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mage/sorcerer_artifact/<pk>/ |  | items.views.mage.sorcerer_artifact.SorcererArtifactDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/wraith/create/relic/ |  | items.views.wraith.WraithRelicCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/wraith/create/artifact/ |  | items.views.wraith.WraithArtifactCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/wraith/update/relic/<pk>/ |  | items.views.wraith.WraithRelicUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/wraith/update/artifact/<pk>/ |  | items.views.wraith.WraithArtifactUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/wraith/list/relics/ |  | items.views.wraith.WraithRelicListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/wraith/list/artifacts/ |  | items.views.wraith.WraithArtifactListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/wraith/relic/<pk>/ |  | items.views.wraith.WraithRelicDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/wraith/artifact/<pk>/ |  | items.views.wraith.WraithArtifactDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/changeling/create/treasure/ |  | items.views.changeling.TreasureCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/changeling/create/dross/ |  | items.views.changeling.DrossCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/changeling/update/treasure/<pk>/ |  | items.views.changeling.TreasureUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/changeling/update/dross/<pk>/ |  | items.views.changeling.DrossUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/changeling/list/treasures/ |  | items.views.changeling.TreasureListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/changeling/list/dross/ |  | items.views.changeling.DrossListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/changeling/treasure/<pk>/ |  | items.views.changeling.TreasureDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/changeling/dross/<pk>/ |  | items.views.changeling.DrossDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/demon/create/relic/ |  | items.views.demon.relic.RelicCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/demon/update/relic/<pk>/ |  | items.views.demon.relic.RelicUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/demon/list/relics/ |  | items.views.demon.relic.RelicListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/demon/relic/<pk>/ |  | items.views.demon.relic.RelicDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mummy/create/relic/ |  | items.views.mummy.MummyRelicCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mummy/create/vessel/ |  | items.views.mummy.VesselCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mummy/create/ushabti/ |  | items.views.mummy.UshabtiCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/mummy/update/relic/<int:pk>/ |  | items.views.mummy.MummyRelicUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mummy/update/vessel/<int:pk>/ |  | items.views.mummy.VesselUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mummy/update/ushabti/<int:pk>/ |  | items.views.mummy.UshabtiUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/mummy/list/relic/ |  | items.views.mummy.MummyRelicListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mummy/list/vessel/ |  | items.views.mummy.VesselListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mummy/list/ushabti/ |  | items.views.mummy.UshabtiListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/mummy/relic/<int:pk>/ |  | items.views.mummy.MummyRelicDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mummy/vessel/<int:pk>/ |  | items.views.mummy.VesselDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/mummy/ushabti/<int:pk>/ |  | items.views.mummy.UshabtiDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/hunter/create/gear/ |  | items.views.hunter.gear.HunterGearCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/hunter/create/relic/ |  | items.views.hunter.relic.HunterRelicCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/hunter/update/gear/<pk>/ |  | items.views.hunter.gear.HunterGearUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/hunter/update/relic/<pk>/ |  | items.views.hunter.relic.HunterRelicUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/hunter/list/gear/ |  | items.views.hunter.gear.HunterGearListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/hunter/list/relics/ |  | items.views.hunter.relic.HunterRelicListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/hunter/gear/<pk>/ |  | items.views.hunter.gear.HunterGearDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/hunter/relic/<pk>/ |  | items.views.hunter.relic.HunterRelicDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/create/item/ |  | items.views.core.item.ItemCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/create/weapon/ |  | items.views.core.weapon.WeaponCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/create/meleeweapon/ |  | items.views.core.meleeweapon.MeleeWeaponCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/create/rangedweapon/ |  | items.views.core.rangedweapon.RangedWeaponCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/create/thrownweapon/ |  | items.views.core.thrownweapon.ThrownWeaponCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: create policy |
| items/create/material/ |  | items.views.core.material.MaterialCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| items/create/medium/ |  | items.views.core.medium.MediumCreateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| items/update/item/<pk>/ |  | items.views.core.item.ItemUpdateView | Permission.EDIT_FULL | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/update/weapon/<pk>/ |  | items.views.core.weapon.WeaponUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/update/meleeweapon/<pk>/ |  | items.views.core.meleeweapon.MeleeWeaponUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/update/rangedweapon/<pk>/ |  | items.views.core.rangedweapon.RangedWeaponUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/update/thrownweapon/<pk>/ |  | items.views.core.thrownweapon.ThrownWeaponUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: object/action policy |
| items/update/material/<pk>/ |  | items.views.core.material.MaterialUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| items/update/medium/<pk>/ |  | items.views.core.medium.MediumUpdateView | none | no | GET,POST,PUT,OPTIONS,HEAD | object-permission: reference write ADMIN |
| items/list/material/ |  | items.views.core.material.MaterialListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| items/list/medium/ |  | items.views.core.medium.MediumListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| items/list/weapon/ |  | items.views.core.weapon.WeaponListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/list/melee_weapon/ |  | items.views.core.meleeweapon.MeleeWeaponListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/list/ranged_weapon/ |  | items.views.core.rangedweapon.RangedWeaponListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/list/thrown_weapon/ |  | items.views.core.thrownweapon.ThrownWeaponListView | none | no | GET,OPTIONS,HEAD | login-only: filtered collection |
| items/index/ |  | items.views.core.ItemIndexView | none | no | GET,POST,OPTIONS,HEAD | login-only: filtered collection |
| items/material/<pk>/ |  | items.views.core.material.MaterialDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| items/medium/<pk>/ |  | items.views.core.medium.MediumDetailView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| items/weapon/<pk>/ |  | items.views.core.weapon.WeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/melee_weapon/<pk>/ |  | items.views.core.meleeweapon.MeleeWeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/ranged_weapon/<pk>/ |  | items.views.core.rangedweapon.RangedWeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/thrown_weapon/<pk>/ |  | items.views.core.thrownweapon.ThrownWeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ |  | items.views.core.GenericItemDetailView | none | no | GET,POST,OPTIONS,HEAD | object-permission: public GET / full target |
| items/<pk>/ | item | items.views.core.item.ItemDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | weapon | items.views.core.weapon.WeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | melee_weapon | items.views.core.meleeweapon.MeleeWeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | thrown_weapon | items.views.core.thrownweapon.ThrownWeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | ranged_weapon | items.views.core.rangedweapon.RangedWeaponDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | wonder | items.views.mage.wonder.WonderDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | charm | items.views.mage.charm.CharmDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | artifact | items.views.mage.artifact.ArtifactDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | talisman | items.views.mage.talisman.TalismanDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | grimoire | items.views.mage.grimoire.GrimoireDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | sorcerer_artifact | items.views.mage.sorcerer_artifact.SorcererArtifactDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | periapt | items.views.mage.periapt.PeriaptDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | fetish | items.views.werewolf.fetish.FetishDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | talen | items.views.werewolf.talen.TalenDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | vampire_artifact | items.views.vampire.VampireArtifactDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | bloodstone | items.views.vampire.BloodstoneDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | relic | items.views.wraith.WraithRelicDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | wraith_artifact | items.views.wraith.WraithArtifactDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | treasure | items.views.changeling.TreasureDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | dross | items.views.changeling.DrossDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | demon_relic | items.views.demon.relic.RelicDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | hunter_relic | items.views.hunter.relic.HunterRelicDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | hunter_gear | items.views.hunter.gear.HunterGearDetailView | none | no | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | mummy_relic | items.views.mummy.MummyRelicDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | vessel | items.views.mummy.VesselDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| items/<pk>/ | ushabti | items.views.mummy.UshabtiDetailView | Permission.VIEW_FULL | yes | GET,OPTIONS,HEAD | object-permission: public GET / full VIEW_FULL |
| game/chronicles/ |  | game.views.ChronicleListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/chronicle/<int:pk>/ |  | game.views.ChronicleDetailView | LoginRequiredMixin | yes | GET,POST,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/chronicle/<int:pk>/retired/ |  | characters.views.core.RetiredCharacterIndex | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| game/chronicle/<int:pk>/deceased/ |  | characters.views.core.DeceasedCharacterIndex | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| game/chronicle/<int:pk>/npc/ |  | characters.views.core.NPCCharacterIndex | none | no | GET,OPTIONS,HEAD | object-permission: object/action policy |
| game/scenes/ |  | game.views.SceneListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/scene/<int:pk>/ |  | game.views.SceneDetailView | LoginRequiredMixin | yes | GET,POST,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/commands/ |  | game.views.CommandsView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/journals/ |  | game.views.JournalListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/journal/<int:pk>/ |  | game.views.JournalDetailView | Permission.VIEW_FULL | yes | GET,POST,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/story/list/ |  | game.views.StoryListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/story/create/ |  | game.views.StoryCreateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/story/<int:pk>/ |  | game.views.StoryDetailView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/story/<int:pk>/update/ |  | game.views.StoryUpdateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/week/list/ |  | game.views.WeekListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/week/create/ |  | game.views.WeekCreateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/week/<int:pk>/ |  | game.views.WeekDetailView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/week/<int:pk>/update/ |  | game.views.WeekUpdateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/weekly-xp-request/list/ |  | game.views.WeeklyXPRequestListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/weekly-xp-request/create/<int:week_pk>/<int:character_pk>/ |  | game.views.WeeklyXPRequestCreateView | OwnerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/weekly-xp-request/batch-approve/ |  | game.views.WeeklyXPRequestBatchApproveView | global StorytellerRequiredMixin | yes | POST,OPTIONS | object-permission: chronicle scoped |
| game/weekly-xp-request/<int:pk>/ |  | game.views.WeeklyXPRequestDetailView | CharacterOwnerOrSTMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/weekly-xp-request/<int:pk>/approve/ |  | game.views.WeeklyXPRequestApproveView | global StorytellerRequiredMixin | yes | POST,OPTIONS | object-permission: chronicle scoped |
| game/story-xp-request/list/ |  | game.views.StoryXPRequestListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/story-xp-request/create/<int:character_pk>/ |  | game.views.StoryXPRequestCreateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/story-xp-request/<int:pk>/ |  | game.views.StoryXPRequestDetailView | CharacterOwnerOrSTMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/story-xp-request/<int:pk>/update/ |  | game.views.StoryXPRequestUpdateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/setting-element/list/ |  | game.views.SettingElementListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/setting-element/create/ |  | game.views.SettingElementCreateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/setting-element/<int:pk>/ |  | game.views.SettingElementDetailView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/setting-element/<int:pk>/update/ |  | game.views.SettingElementUpdateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/xp-spending-request/list/ |  | game.views.XPSpendingRequestListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/xp-spending-request/create/<int:character_pk>/ |  | game.views.XPSpendingRequestCreateView | OwnerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/xp-spending-request/<int:pk>/ |  | game.views.XPSpendingRequestDetailView | CharacterOwnerOrSTMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/xp-spending-request/<int:pk>/update/ |  | game.views.XPSpendingRequestUpdateView | CharacterOwnerOrSTMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/xp-spending-request/<int:pk>/approve/ |  | game.views.XPSpendingRequestApproveView | global StorytellerRequiredMixin | yes | POST,OPTIONS | object-permission: chronicle scoped |
| game/freebie-spending-record/list/ |  | game.views.FreebieSpendingRecordListView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | object-permission: filtered chronicle collection |
| game/freebie-spending-record/create/<int:character_pk>/ |  | game.views.FreebieSpendingRecordCreateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/freebie-spending-record/<int:pk>/ |  | game.views.FreebieSpendingRecordDetailView | CharacterOwnerOrSTMixin | yes | GET,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/freebie-spending-record/<int:pk>/update/ |  | game.views.FreebieSpendingRecordUpdateView | CharacterOwnerOrSTMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/chronicle-manage/create/ |  | game.views.ChronicleCreateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/chronicle-manage/<int:pk>/update/ |  | game.views.ChronicleUpdateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/scene-manage/create/ |  | game.views.SceneCreateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/scene-manage/create/<int:chronicle_pk>/ |  | game.views.SceneCreateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| game/scene-manage/<int:pk>/update/ |  | game.views.SceneUpdateView | global StorytellerRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | object-permission: chronicle scoped |
| accounts/password_reset/ |  | accounts.views.CustomPasswordResetView | none | no | GET,POST,PUT,OPTIONS,HEAD | login-only: own profile or scoped object |
| accounts/signup/ |  | accounts.views.SignUp | none | no | GET,POST,PUT,OPTIONS,HEAD | login-only: own profile or scoped object |
| accounts/profile/update/<pk>/ |  | accounts.views.ProfileUpdateView | LoginRequiredMixin | yes | GET,POST,PUT,OPTIONS,HEAD | login-only: own profile or scoped object |
| accounts/profile/<pk>/ |  | accounts.views.ProfileView | LoginRequiredMixin | yes | GET,OPTIONS,HEAD | login-only: own profile or scoped object |
| accounts/scene/<int:scene_pk>/award-xp/ |  | accounts.views.SceneXPAwardView | LoginRequiredMixin | yes | POST | login-only: own profile or scoped object |
| accounts/scene/<int:scene_pk>/mark-read/ |  | accounts.views.MarkSceneReadView | LoginRequiredMixin | yes | POST | login-only: own profile or scoped object |
| accounts/approve/<str:object_type>/<int:pk>/ |  | accounts.views.ObjectApprovalView | LoginRequiredMixin | yes | POST | login-only: own profile or scoped object |
| accounts/approve-image/<str:object_type>/<int:pk>/ |  | accounts.views.ImageApprovalView | LoginRequiredMixin | yes | POST | login-only: own profile or scoped object |
| accounts/character/<int:character_pk>/award-freebies/ |  | accounts.views.FreebieAwardView | LoginRequiredMixin | yes | POST | login-only: own profile or scoped object |
| accounts/weekly-xp/<int:week_pk>/<int:character_pk>/request/ |  | accounts.views.WeeklyXPRequestView | LoginRequiredMixin | yes | POST | login-only: own profile or scoped object |
| accounts/weekly-xp/<int:week_pk>/<int:character_pk>/approve/ |  | accounts.views.WeeklyXPApprovalView | LoginRequiredMixin | yes | POST | login-only: own profile or scoped object |
| accounts/login/ |  | accounts.views.CustomLoginView | none | no | GET,POST,PUT,OPTIONS,HEAD | login-only: own profile or scoped object |
| accounts/ |  | core.views.home.HomeListView | none | no | GET,OPTIONS,HEAD | public-reference: GET/HEAD only |
| accounts/login/ |  | django.contrib.auth.views.LoginView | none | no | GET,POST,PUT,OPTIONS,HEAD | framework-owned: explicit exclusion |
| accounts/logout/ |  | django.contrib.auth.views.LogoutView | none | no | POST,OPTIONS | framework-owned: explicit exclusion |
| accounts/password_change/ |  | django.contrib.auth.views.PasswordChangeView | none | no | GET,POST,PUT,OPTIONS,HEAD | framework-owned: explicit exclusion |
| accounts/password_change/done/ |  | django.contrib.auth.views.PasswordChangeDoneView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| accounts/password_reset/ |  | django.contrib.auth.views.PasswordResetView | none | no | GET,POST,PUT,OPTIONS,HEAD | framework-owned: explicit exclusion |
| accounts/password_reset/done/ |  | django.contrib.auth.views.PasswordResetDoneView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| accounts/reset/<uidb64>/<token>/ |  | django.contrib.auth.views.PasswordResetConfirmView | none | no | GET,POST,PUT,OPTIONS,HEAD | framework-owned: explicit exclusion |
| accounts/reset/done/ |  | django.contrib.auth.views.PasswordResetCompleteView | none | no | GET,OPTIONS,HEAD | framework-owned: explicit exclusion |
| ^media/(?P<path>.*)$ |  | django.views.static.serve | function/unknown | unknown | ANY* | framework-owned: explicit exclusion |
