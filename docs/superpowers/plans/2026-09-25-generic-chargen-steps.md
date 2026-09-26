# Generic Chargen Steps Implementation Plan

> **For agentic workers:** Use test-driven development and verification-before-completion. Steps use checkbox syntax for tracking.

**Goal:** Consolidate duplicate character creation and CRUD view behavior while preserving registered workflows and authorization.

**Architecture:** Named adapters preserve existing imports and route policies. Shared Django bases implement form lifecycles; Step 2 continues to own routing and advancement.

**Tech Stack:** Django 5.2, django-polymorphic, unittest, Python AST.

**Spec:** `docs/superpowers/specs/2026-09-25-generic-chargen-steps-design.md`

## Global constraints

Preserve 231 registered positions and route-policy identities. No schema changes,
new dependencies, unrestricted form fields, or rule extraction (Step 4). GET is
read-only. Every successful transition uses the existing advance function; service
spends must not advance twice. The shared view advances after a successful final
spend; services own spending persistence. Keep existing character-specific rules as hooks.

## Review focus

* Languages with multiple required fields: every submitted value persists, plus English.
* Final freebie with an incomplete linked background: stop at that required step.
* Owners and unrelated gameline STs: form selection never grants ST-only fields.
* Returned/approved characters and direct as_view calls: authorization holds.
* Custom specialty/pool rules: normalization does not silently erase a variation.

## Task 1: Inventory and characterization

Files: `scripts/inventory_chargen_views.py`, `docs/superpowers/specs/generic-chargen-inventory.json`, `characters/tests/views/core/test_shared_chargen.py`.
Interface: dependency-free CLI outputs class paths, configuration, method fingerprints,
duplicate groups and source-line counts. Capture the rebased baseline before edits.

- [x] Build AST inventory and record baseline findings.
- [x] Add family-wide GET/POST characterization; run against the unchanged implementation.
- [x] Add focused failing tests for Companion/Sorcerer languages and detail actions.

## Task 2: Languages, specialties and abilities

Files: `characters/views/core/human.py` and configured gameline view subclasses;
test file from Task 1. Interfaces: HumanLanguagesView; HumanSpecialtiesView with
`get_specialties_needed(self)`; HumanAbilityView with model-defined groups and
primary/secondary/tertiary totals. Existing aliases remain importable.

- [x] Consolidate language saving and specialty submission; preserve exceptional hooks.
- [x] Replace unrolled ability handlers with the shared pool implementation.
- [x] Run shared-step tests and existing core/gameline view tests; verify bug regressions pass.

## Task 3: Extras and template selection

Files: shared extras/template modules under `characters/views/core/`, shared template
selection form under `characters/forms/core/`, configured adapters and focused tests.
Interfaces: extras preparation hook followed by advance; template selection configured
by model, gameline, character_type and creation route.

- [x] Characterize all distinct extras effects and template apply/skip/filter behavior.
- [x] Consolidate lifecycles and preserve deliberate gameline wording and rules.
- [x] Test all registered biography POSTs and six template selection flows.

## Task 4: Freebies and Wraith allocations

Files: `characters/views/core/human.py`, `characters/views/mage/{companion,sorcerer}.py`,
`characters/views/wraith/wraith_chargen.py`, focused tests and a shared allocation base.
Interfaces: FreebieSpendingServiceFactory.get_service(character).spend(...); configurable
allocation form, total/spent/completion methods and add-record hook.

- [x] Characterize actual form categories, invalid spending, derived familiar stats and final-point navigation.
- [x] Route Companion/Sorcerer through one service-based view lifecycle.
- [x] Consolidate passion/fetter allocation and preserve limits, dark passions and messages.
- [x] Run spending-service, transition and Wraith view tests.

## Task 5: CRUD and detail bases

Files: shared form selection mixin in `core/mixins.py`, explicit form field definitions,
character CRUD/detail adapters, `characters/tests/views/core/test_shared_character_crud.py`.
Interface: `limited_form_class` plus scoped-editor selection, composed reviewed field
groups; CharacterDetailView retains scene and status action behavior.

- [x] Test owner/ST field selection and unauthorized forged fields before consolidation.
- [x] Replace duplicated selectors, compose repeated field groups, remove duplicate Mage time field.
- [x] Unify character detail bases preserving custom approval/context handlers.
- [x] Verify retire/decease, scene visibility and public projection behavior.

## Task 6: Integration, review, commit and PR

- [x] Run registry, workflow, transition, character view/form/service and authorization tests.
- [x] Regenerate inventory; document measured savings, findings and exceptions.
- [x] Review the full diff independently and fix demonstrated regressions.
- [x] Run Django checks and diff whitespace checks; inspect final git status.
Delivery: commit the verified changes, push this branch and open a PR against main.

## Execution record

Rebased on `origin/main` at c14f2bad with no conflicts. Legacy project skill paths
have been consolidated into the parent checkout's tg-standards skill; current
authorization implementation takes precedence over stale examples there.


Implementation record: all five implementation tasks complete. The independent
review found a newly reachable Companion Advantage refund exploit and an Arete
choice/service mismatch; both received failing actual-view tests and fixes, then
independent successful reproducer runs. Generic biography wording for non-Mage
characters is intentional: those characters have not undergone a Mage Awakening.

Final verification: 1,953 relevant tests passed (four existing skips), Django
system checks passed, all 55 changed/new Python files compiled and passed Black
and selected Ruff checks, and the diff passed whitespace checks. See the audit
report for measured savings and the preserved rule boundaries.
