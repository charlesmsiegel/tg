# Permission context design

## Intent and scope

Implement Step 6 after the authorization-hardening work in this checkout. The current user instruction explicitly requests both planning and implementation, superseding the source summary's design-only restriction. Preserve Step 0's server gates and public projections. Templates describe authority; they never confer it. Work stays in the existing isolated worktree.

## Evidence and decisions

The requested old tg-permissions, tg-frontend and tg-testing skills were consolidated into `.claude/skills/tg-standards/`; its permissions, templates and testing references were read alongside CLAUDE.md. Step 0's design and plan exist and its implementation is present. Some older guidance about global STs/approved-owner editing is superseded by Step 0.

| Audit claim | Current finding |
| --- | --- |
| Inconsistent is_approved_user | Confirmed remaining ambiguity: staff context processor, full-read mixins, character and journal overrides, hard-coded Chantry step flags. Many former overrides were already removed. |
| SpecialUser grants any ST / unowned objects | Refuted at current HEAD: it calls VIEW_FULL. |
| Passed view permission implies approval / character uses edit | Refuted: both now use VIEW_FULL. |
| Unused template permission library and context processor | Confirmed: no production template loads the library; processor is unregistered. Its callable helpers cannot be called with arguments by Django templates. |
| No request cache | Partly refuted: scoped ST roles are cached, but object membership queries and convenience helpers repeat work. |
| STRelationship / player-status / anonymous mismatch | Fixed by Step 0: any assigned ST reads; any owned character grants PLAYER; anonymous has no private-list role. |
| owned_by.owner grants authority | Refuted: current object checks no longer grant it. Keep creator ownership (`owner`), not possession, as authority. |
| Item/location lists unfiltered | Refuted at runtime: OBJECT_LIST policy and index handlers render public-safe, filtered rows for nonstaff. Raw ListViews remain unfiltered when invoked directly. |
| ~30 permission queries / 17 global ST calls | Historical estimates, not current measurements. Pin actual permission overhead with query tests, not these estimates. |
| Polymorphic observer parity | Confirmed remaining defect: filtering by base content type misses observers attached to concrete subclasses. |
| No-role models | Empty Q can return all rows for an authenticated stranger. Start from an impossible predicate. |

## Architecture and alternatives

Choose a request-local permission snapshot layered on PermissionManager. An application-global cache would require cross-process invalidation and risks stale grants; reject it. Replacing every authorization route with a new policy engine duplicates Step 0; reject that too. Reuse its role matrix, status restrictions and scoped storyteller semantics.

PermissionManager remains the authority. `ObjectPermissions` is immutable and exposes `can_view_full`, `can_view_partial`, `can_edit`, `can_edit_limited`, `can_spend_xp`, `can_spend_freebies`, `can_approve`, `can_approve_spending`, `can_delete`, `can_manage_observers`, `is_owner`, `is_chronicle_st`, `is_scoped_st`, `can_manage_character`, `can_chargen`, and `visibility_tier`. `is_chronicle_st` means a same-chronicle read role (head, assigned or game ST); staff is represented by the capabilities and `can_manage_character`. `is_scoped_st` is a head/matching-gameline ST. New permissions extend the existing matrix and snapshot, not parallel template logic.

Use `object_perms`, not `perms` (reserved for Django auth). `PermissionContextMixin` supplies the primary object's snapshot; the existing authorization middleware supplies the same snapshot at TemplateResponse time for legacy views without that mixin. Character-linked private record templates explicitly use their character as the permission subject. No full model or permission snapshot is added to public projection responses. Keep Django's auth processor; remove the ambiguous special-user processor and obsolete middleware registration. Retire the unused callable permission processor; rewrite the permission tag library to delegate to the request-aware manager and add `{% object_permissions row as row_perms %}` for secondary objects.

## Cache lifecycle and rows

Request caches are keyed by user identity (including staff/superuser flags), model label and object identity (Python identity for unsaved objects). Cache database memberships once per user/request: headed chronicles, game-ST chronicles, chronicle/gameline assignments, player chronicles and observer model/PK pairs. Cache roles and immutable capability snapshots; include live owner, scope, gameline, status and NPC state in effective cache keys, so changing draft status or owner in memory does not retain a grant. Do not cache anything globally or on model instances across requests. Calls without `request=` keep working and do not retain results.

`invalidate_request_cache(request)` clears all role/membership/snapshot caches after relationship, observer or membership changes in a request that continues checking permissions. Clearing all is deliberately simpler and safer than partial dependency invalidation. Existing mutation handlers redirect; new requests naturally refresh. Tests cover in-memory status/owner changes, persisted relationship revocation followed by explicit invalidation, different users and separate requests.

`prepare_permission_objects(request, objects)` resolves base polymorphic rows in batches before row snapshots. `VisibilityFilterMixin` prepares rows only when a paginator bounds the page; unpaginated lists do not eagerly compute unused row capabilities. a template tag then reads each snapshot without queries. Related-record pages batch their character subjects. Targets: five membership queries for a cold prepared subject/page (content-type lookup and polymorphic hydration are separate ORM costs), zero queries for repeated capabilities on a warm object, zero extra permission queries as a homogeneous page grows from one to twenty rows (excluding fetching/polymorphic hydration, measured separately). Avoid evaluating a full unpaginated collection just to attach permissions.

## Queryset parity and discovery

Keep SQL predicates explicit and enforce parity with a fixture matrix rather than inventing a policy-to-SQL compiler. The contract is `obj in filter_queryset_for_user(user, qs)` iff VIEW_FULL or VIEW_PARTIAL for that concrete object. Test character, item, location and inherited models, all statuses and visibility codes, null chronicle, shared objects, each ST role, owner, player, observer, unrelated and anonymous users. Possession alone does not grant access. Generic observer IDs must retain their content type to avoid cross-model PK collisions; base polymorphic queries use concrete polymorphic content types.

Public discovery is a separate deliberate Step 0 product rule: anonymous may discover PUB safe cards without VIEW_PARTIAL; direct public cards exist even for unlisted objects. Private/full queryset parity does not apply to this public projection. Reuse the private filter as one discovery audience alongside PUB/is_public and CHR discovery, keeping public fields allowlisted. Do not give anonymous private permissions to make a list equation appear true. Add visibility filtering to item/location ListViews as defense in depth for direct invocation, while route middleware continues serving public cards. Public reference models remain public.

## Template migration

Map every current legacy-flag occurrence below. Chargen uses `can_chargen` (EDIT_FULL and Un/Rev); read-only full sheets use `can_view_full`. Chantry generation uses `can_chargen`; journal read uses the linked character's `can_view_full`. Remove view assignments once templates have moved. Game list labels describing another user's data use `show_owner_column`, not approval authority; actionable spending approval uses `object_perms.can_approve_spending`; other object approval uses `object_perms.can_approve`. Week and global SettingElement creation/editing use explicitly staff-scoped names because their routes require staff. Scene-author ST styling is presentation, not permission, and is outside this migration.

| Template (line at audit) | Old flag -> capability |
| --- | --- |
| `characters/templates/characters/changeling/changeling/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/changeling/changeling/chargen.html:94` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/changeling/ctdhuman/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/changeling/ctdhuman/chargen.html:92` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/core/character/detail.html:16` | `is_approved_user` -> `object_perms.can_view_full` |
| `characters/templates/characters/mage/companion/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/mage/companion/chargen.html:131` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/mage/mage/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/mage/mage/chargen.html:150` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/mage/mtahuman/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/mage/mtahuman/chargen.html:124` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/mage/sorcerer/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/mage/sorcerer/chargen.html:144` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/vampire/ghoul/chargen.html:7` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/vampire/ghoul/chargen.html:219` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/vampire/vampire/chargen.html:7` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/vampire/vampire/chargen.html:277` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/vampire/vtmhuman/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/vampire/vtmhuman/chargen.html:92` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/fera/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/fera/chargen.html:124` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/fomor/chargen.html:7` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/fomor/chargen.html:153` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/garou/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/garou/chargen.html:44` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/kinfolk/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/kinfolk/chargen.html:92` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/wtahuman/chargen.html:6` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/werewolf/wtahuman/chargen.html:92` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/wraith/wraith/chargen.html:7` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/wraith/wraith/chargen.html:249` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/wraith/wtohuman/chargen.html:9` | `is_approved_user` -> `object_perms.can_chargen` |
| `characters/templates/characters/wraith/wtohuman/chargen.html:92` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:20` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:27` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:35` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:42` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:49` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:56` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:64` | `is_approved_user` -> `object_perms.can_chargen` |
| `locations/templates/locations/mage/chantry/locgen.html:73` | `is_approved_user` -> `object_perms.can_chargen` |
| `game/templates/game/journal/detail.html:8` | `is_approved_user` -> `object_perms.can_view_full` |

Other migrations: group edit and character-template edit/delete buttons use object capabilities; Mage XP approval controls use the spending-specific capability; journal response controls use linked-character approval scope. Chronicle scene creation uses a named chronicle-scoped context decision. Permission tags remain for secondary objects, with request caching; no global-ST tag is used as object authority.

## Verification and limits

Regression tests pin query counts and invalidation; a fixture matrix pins SQL/object parity; template-render tests pin owner/read-only ST/matching ST controls and prevent legacy flag reintroduction. Exercise public item/location discovery and private field exclusion. Run focused permission, mixin, tag, security, character and game suites, then Django checks and formatting. Record actual commands/results in the plan. No schema migrations or Step 0 gate changes are planned.

## Operational use and theory note

A permission fact is either request-stable database membership or a live object input. Memberships are memoized; changing an object's owner/status/NPC field changes its next snapshot immediately, including when the caller holds a base polymorphic row. A new capability belongs in PermissionManager (or an existing action-specific service such as spending approval), then in the immutable snapshot; no independent template rule should be introduced.

After mutating an observer, owned-character chronicle membership, game-ST membership, head ST or STRelationship during a request that continues checking authority, call `PermissionManager.invalidate_request_cache(request)`. If an update was made through a different ORM instance or `QuerySet.update()`, also refresh the subject instance before evaluating its live fields. The invalidator clears every dependent membership, role, subject and snapshot cache. Current relationship-write flows redirect; no cross-request invalidation mechanism is needed.

For a new list needing row controls: paginate it, select related character subjects on record querysets, call `prepare_permission_objects(request, list(page_objects))`, load `permissions`, and use `{% object_permissions row as row_perms %}`. Plain public cards must continue using their allowlisted dictionaries. The generic snapshot is not a replacement for route-specific action checks (for example official-template writes and self-approval rules).

Product decisions retained: possession (`owned_by`) is not creator authority; any-status owned characters establish PLAYER membership; all chronicle STs can read but only matching STs edit; anonymous PUB discovery is a public projection rather than a private permission. Public discovery now includes the same private-read audience, including concrete-subclass observers and PLAYER, plus the pre-existing public/CHR audience. This intentionally makes discoverability agree with the object's existing private-read roles while keeping public rows safe.
