# Items and locations registry implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement these tasks in order.

**Goal:** Replace repeated item/location CRUD declarations with a registry while preserving routes, workflows and Step 0 authorization.

**Architecture:** One declaration per model generates generic views, URLs, menus and model URL methods. Explicit custom view overrides preserve workflow behavior; polymorphic dispatch uses concrete classes.

**Tech Stack:** Python, Django 5.2, django-polymorphic 4.1, existing permission evaluator.

**Spec:** `docs/superpowers/specs/2026-09-25-items-locations-registry-design.md`

## Global constraints

- Preserve all existing URL names and valid paths; use integer converters.
- Keep reference data publicly readable; writes follow explicit Step 0 policies.
- No character-view migration or template visual redesign.
- Work in the existing isolated worktree. The user requested implementation in this session.

## Review focus

- Identical type strings across gamelines must select different model classes.
- An override or newly declared action cannot bypass authorization.
- Same URL name may denote both a list and a parameterized detail route.
- Chantry's canonical URL must continue creation-state dispatch.
- Menus must work without seeded ObjectType rows and reject unknown/ambiguous names.

## Task 1: Compatibility baseline and registry contract

Files: `scripts/inventory_model_routes.py`, `core/tests/fixtures/model_routes.json`,
`core/tests/test_model_registry.py`, `core/model_registry.py`.

- [x] Capture existing names, paths, and callbacks in a read-only inventory script/fixture.
- [x] Write failing tests for registry coverage, policy completeness, duplicate model/slug rejection and route parity.
- [x] Implement `ModelRegistry`, `ModelSpec`, and `ActionSpec`: explicit metadata, lazy views, fail-closed validation, `urls(group, action)`, `view(model, action)`, `menu()` and `resolve(type_name, gameline)`.
- [x] Run `python manage.py test core.tests.test_model_registry --noinput` and verify the contract tests pass after declarations are installed.

## Task 2: Core pilot and gameline migration

Files: `items/registry.py`, `locations/registry.py`, `items/views/`,
`locations/views/`, `items/urls/`, `locations/urls/`, shared fallback templates.

- [x] Extract audited form fields, templates, messages and widget attributes into one entry per model; retain custom method classes explicitly.
- [x] Migrate core Item/Weapon/Material/Medium and Location/City as pilot.
- [x] Migrate Mage, then Werewolf, Vampire, Wraith, Changeling, Demon, Hunter and Mummy; each slice independently uses the same factory and retains compatibility exports.
- [x] Generate CRUD routes per action with explicit historical path overrides. Preserve wizard/AJAX routes. Remove exception swallowing in app URL mounts.
- [x] Add generated view policy enforcement and owner assignment; preserve custom form hooks. Test GET/POST denial and successful writes, including staff-only references.
- [x] Run item/location/security tests and parity checks after migration.

## Task 3: Dispatch, model URLs and navigation

Files: shared registry view/URL helpers, item/location base models and URL overrides,
index views/forms, `core/create_redirects.py`, `core/views/public_object.py`.

- [x] Write regressions for both Artifact and Relic collisions, canonical Chantry dispatch, and no duplicate detail fetch.
- [x] Replace string dispatch with concrete model lookup; pass the loaded instance through authorization and detail rendering.
- [x] Replace duplicate model URL methods with registry-backed inheritance, preserving existing canonical paths.
- [x] Replace ObjectType menu/redirect dependencies for items/locations; retain character handling. Test zero-seed menus, unknown selections and gameline ambiguity.
- [x] Run focused tests and existing custom workflow suites.

## Task 4: Cleanup and verification

- [x] Delete superseded boilerplate classes and hand-written CRUD routes; retain only compatibility exports and custom handlers.
- [x] Generate per-model list/detail/create/update smoke tests for authorized and unauthorized users; pin reference/public-card distinctions and model coverage.
- [x] Run `python manage.py check`, relevant suites and `python manage.py test --noinput`; record failures and limitations honestly.
- [x] Review final diff against the spec, update audit findings/custom class list and record completion evidence.

## Review/PR slicing

For incremental review, split Task 1 plus the core pilot first, then one gameline per
PR in the order above, then navigation/model URLs and boilerplate removal. Every PR
must retain all baseline routes and explicit policies. This session implements the
whole plan in the supplied worktree. The subsequent user instruction requests a commit and PR after verification.


## Completion evidence (2026-09-26)

- `python manage.py check`: no issues.
- Full Django suite with four workers: 7,167 tests run, 33 skipped, no failures,
  exit code 0 (656.922 seconds).
- After the final RealityZone related-location privacy guard, the registry,
  authorization-security and RealityZone suites ran 107 tests, all passing.
- Test-only settings used in-memory SQLite, MD5 password hashing and quiet logging;
  production settings were unchanged. The normal repository test runner was retained.
- `ruff check --select F,E9,I` passed for changed Python files; Black and diff
  whitespace checks passed.
- URL inventory preserves all 268 baseline names/paths and callback identities.
  Two base-model list endpoints are added. All 63 entries have CRUD/denial smoke coverage.
- Independent review found and verified fixes for custom Node `super()` recursion,
  unfinished-Chantry public cards, missing ParadoxRealm IDs, RealityZone registration,
  and duplicate route validation. A final regression verified that public RealityZone
  pages do not disclose private related locations or ranks.

Implementation rulings: preserve compatibility modules instead of deleting their
Python import paths; keep ObjectType rows/IDs intact; store dispatch identity as the
model class; preserve specialized workflows via explicit private custom classes.
The original design-only scope was superseded by the user's implementation request;
the subsequent instruction authorizes committing and opening a PR.
