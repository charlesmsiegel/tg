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
