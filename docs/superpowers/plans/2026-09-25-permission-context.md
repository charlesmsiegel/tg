# Permission context implementation plan

Spec: [permission-context-design](../specs/2026-09-25-permission-context-design.md).

Execute inline in this existing worktree, as requested. Keep the following order so the work can be reviewed as small PRs; do not publish or merge as part of this task.

## 1. Request memoization (performance only)

Files: `core/permissions.py`, new `core/tests/permissions/test_permission_context.py`.
- [x] Add failing tests for repeated roles/capabilities (zero warm queries), independent requests/users, live owner/status changes and relationship revocation after invalidation.
- [x] Add request facts/role caches and `invalidate_request_cache(request) -> None`; extend convenience checks with optional `request=None` without breaking positional callers.
- [x] Run `python manage.py test core.tests.permissions core.tests.security.test_scoped_roles --noinput`.

## 2. Template contract and batched rows

Files: new `core/permission_context.py`, `core/mixins.py`, `core/middleware/authorization.py`, `core/templatetags/permissions.py`.
- [x] Add immutable `ObjectPermissions` and `get_object_permissions(request, obj)`; implement `prepare_permission_objects(request, objects)` for bounded polymorphic pages.
- [x] Add `PermissionContextMixin`, middleware fallback for legacy TemplateResponses and `object_permissions` tag. Preserve built-in `perms`; public projection has no full-object context.
- [x] Test all capability fields against PermissionManager, draft versus approved owners, same-chronicle wrong-gameline ST, 1/20-row query counts and middleware fallback.
- [x] Run new context tests and `core.tests.mixins core.tests.templatetags.test_permissions`.

## 3. Character templates and legacy flag retirement

Files: character chargen/detail templates and views, Chantry locgen/views, `core/context_processors.py`, `tg/settings/base.py`.
- [x] Migrate every row in the spec's mapping table and remove old view assignments/helpers and obsolete middleware/processor.
- [x] Replace group edit and Mage XP global-ST controls with scoped capabilities; preserve read-only sheets.
- [x] Verify rendered owner controls and read-only ST absence, and scan templates for `is_approved_user`.

## 4. Game and core templates

Files: `game/views.py`, game journal/approval/list/chronicle templates, core character-template views/templates.
- [x] Use linked-character snapshots for private record detail/row approval and journal responses; batch paginated row subjects.
- [x] Separate owner-column display, global staff actions and actual approval capabilities. Keep private-record/scene gates unchanged.
- [x] Test cross-gameline STs see rows but no approval controls; owners cannot see another chronicle's controls; template owner buttons follow status/scoped rules.

## 5. List alignment

Files: `core/permissions.py`, `core/views/public_object.py`, item/location list views, parity tests.
- [x] Add failing matrix tests for polymorphic observers, colliding PKs and no-role models, plus current role/status/visibility combinations.
- [x] Correct SQL predicates, preserving creator ownership and any-status PLAYER. Apply VisibilityFilterMixin to concrete item/location lists; preserve safe public discovery separately.
- [x] Run `core.tests.permissions`, item/location authorization tests and public detail/list security tests.

## 6. Final review and verification

- [x] Run `python manage.py check`, affected app suites, formatting and `git diff --check`.
- [x] Review cache invalidation, snapshot/status keys, polymorphic observer identity, related-character scope and public projection boundaries.
- [x] Record results below; leave design, plan and implementation reviewable in the worktree.

## Review focus

Unsaved objects must not share keys. Base/concrete observer rows must agree without cross-tree grants. Read-only ST rows must never imply approval. Cached owner/status values must not survive an in-request mutation. Public list rows must never receive full private model fields.

## Execution record

- Initial inspection: clean worktree; Django 5.2.17 available; Step 0 prerequisites present. Consolidated tg-standards guidance replaces missing old skill paths.
- Design choice: keep public discovery separate from private VIEW_FULL/VIEW_PARTIAL parity, preserving Step 0's deliberate public-card policy.

- Regression evidence: the initial cache test measured 27 extra queries; no-role filtering returned all rows; base-query observer discovery omitted a concrete Human. Added tests first and fixed each cause.
- Request cache/context verification: 240 focused permission, mixin, template-tag and security tests pass. Five membership queries prepare one or twenty concrete rows; six queries prepare one or twenty linked base-character rows (one polymorphic hydration query). Warm checks cost zero queries. Unsaved identity, live owner/status/NPC state, separate users/requests and explicit revocation invalidation are covered.
- Ruling: use a correlated observer-ID subquery rather than a Q-wrapped Exists expression. Installed django-polymorphic 4.1 rejects the latter while translating Q trees. The correlated query preserves content-type/PK identity; cross-tree collisions and base/subclass discovery are tested.
- Fresh review (permission_review) found three issues, all fixed: missing permissions-library load (template compilation regression); spending self-approval controls (service-specific capability and NPC/self-owner tests); unbounded unused list snapshot preparation (zero-query unpaginated-context test). The reviewer did not independently execute database tests; parent verification supplies that evidence.
- Ruling: preserve public projections and their PUB/CHR discovery audience while adding private-read audiences to public discovery. The cost if wrong would be additional public-card discoverability for users who already have private VIEW_PARTIAL/FULL; no additional private fields are exposed.
- Django system checks and `git diff --check` pass. Ruff comparison against HEAD found zero new diagnostics; 48 existing diagnostics remain in touched files. Changed Python files are Black formatted.
- Broad verification command: a `LocalMigrationTestRunner` subclass runs `core.tests game.tests items.tests.views locations.tests.views characters.tests.views`, with MD5 test-only password hashing and an in-memory SQLite database. It excludes exactly three LiveServer/Firefox tests (`NewUserTest.test_create_account`, `NewUserTest.test_homepage_has_login`, `TestHomepage.test_homepage_structure`); the initial unrestricted attempt stalled in browser-dependent coverage and was interrupted. No production test/settings behavior was changed for this runner.
- User follow-up: commit the completed work and create a PR against main after final verification.

- Final verification: **2,479 tests run, OK (4 existing skips)** in 391.391 seconds; three Firefox/LiveServer tests excluded as listed above. The earlier broad run's two errors were obsolete assertions for retired context names; updated tests now pass in the complete rerun. Additional focused verification: 195 game-view/dead-code tests passed after the final helper change. All 35 changed templates compile, Django system checks pass, and the staged diff passes whitespace checks.

## Claude review follow-up (PR #1470)

Reviewed [Claude's comment](https://github.com/charlesmsiegel/tg/pull/1470#issuecomment-5844456701) against the full HTTP path; there were no inline review threads and the Claude review check succeeded.

1. **Public-list regression: not reproduced; suggested blanket grant declined.** `AuthorizationMiddleware` invokes `authorize_route`; `OBJECT_LIST` routes return `render_public_object_list` before the private ListView mixin for nonstaff readers. Unowned `PUB` rows remain discoverable; unowned `PRI` rows remain unlisted. Direct detail routes return the allowlisted public card, not the full sheet. New HTTP tests exercise anonymous and regular readers for Weapon, Wonder, Talisman, City, TremereChantry and Barrens, checking both discovery and private-field exclusion. Treating nullable ownership as a public/full grant would contradict Step 0's explicit shared-object policy.
2. **Group leader authority: suggested shortcut declined; missing coverage added.** `GroupCreateView` inherits `MessageMixin.form_valid`, which calls `prepare_created_object` and sets the creator as owner even though owner is absent from editable form fields. HTTP tests prove creation, draft creator editing, approved creator read-only access and denial of a different leader's owner. The pre-existing `OBJECT_WRITE` gate grants no leader-owner bypass. Also, the legacy template's `update` block is not rendered by current `core/object.html`; an isolated rendering test pins its capability condition if that block is restored later.
3. **Line-ending noise: accepted.** Restored the original CRLF bytes in the two named templates, leaving only the intended condition changes relative to the PR base. Stage those files with command-local `core.autocrlf=false`; use `core.whitespace=cr-at-eol` for their whitespace check. No repository-wide setting change.
4. **Snapshot cache roles: preserve correctness and explain it.** Request-cached roles must be consulted before a snapshot cache hit because owner/chronicle can change in memory. The snapshot key intentionally includes the resulting roles. A new regression moves a warmed object into an unrelated chronicle and verifies ST view/edit/approve grants disappear without any database queries. Added an inline explanation rather than a redundant invalidation-key implementation.

Draft reviewer response (not posted): The new regressions verify that public lists and creator-owned groups continue to work through the centralized route and creation hooks. The suggested unowned-object and leader-owner grants would bypass existing Step 0 policy, so those grants were not added. The line-ending noise is removed, and snapshot scope freshness is now explicitly documented and tested.

Follow-up validation: **272 tests passed** across permissions, security, mixins, template tags, group views and public item/location/character authorization. The seven added tests include six-model public-list matrices for two audiences. Ruff and Black pass for the changed Python files. Relative to the original PR base, the two restored templates now show 1 and 8 changed condition lines instead of 52 and 77 rewritten lines.


## Rebase integration with the CRUD registry (2026-09-26)

- Rebased onto `origin/main` at `ec840ba6`. Its generated item/location views replace the handwritten classes listed in the original migration plan. Kept all registry exports and custom view hooks; the visibility integration now lives in `ModelRegistry._build_view`, applying `VisibilityFilterMixin` only to actions with `OBJECT_LIST` policy. Public reference lists retain their existing policy.
- `RegistryViewMixin` inherits `PermissionContextMixin`, providing snapshots to authorized detail/update contexts even for direct view calls without middleware. The registry's authorization dispatch still runs before private view rendering.
- New regression tests first reproduced unfiltered private querysets and missing direct-view permission context, then passed after integration. The 87-test registry suite passes, including ordinary Weapon and custom Chantry lists, anonymous Material reference lists, and creator-owned Weapon detail capabilities.
- Rechecked Claude's published review and all inline threads. Run `36229819494` completed successfully without a new published comment or inline thread; its execution summary records tool permission denials, so that status is not independent evidence that the code is defect-free. The earlier four review points remain covered by the preceding disposition and regression tests.
- Black passes for both registry files. Ruff reports no new diagnostics; its existing `UP038` in the registry contract tests is also present on `origin/main`.
- Broad rebase verification ran 2,599 entries (four existing skips), excluding the same three browser tests. It exposed three stale assertions already present unchanged on main: two expected extracted Wonder JavaScript inside the HTML template, and one retained six obsolete missing-template entries (three now exist; three are no longer referenced by routed templates). Updated those tests to check the loaded static asset and current routed-template inventory. The command also included a nonexistent `items.tests.urls` label, producing one loader error; that label was removed from subsequent verification.
- Final targeted verification: **250 tests passed** across routed templates, Wonder views, the complete registry suite, permission/security tests and group views. The broad run had no other failures. Black, Django checks and whitespace checks pass; Ruff has no new diagnostics.
