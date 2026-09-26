# Chargen Step Registry Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Drive all existing character creation workflows from one registry without changing persisted step positions.

**Architecture:** Immutable metadata with lazy view imports supplies routing, fragments, progress and freebie positions. A shared view mixin and transition service preserve authorization and make skip decisions from that metadata.

**Tech Stack:** Python, Django 5.2, django-polymorphic, existing Django templates and unittest runner. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-09-25-chargen-step-registry-design.md`

## Global constraints

- Preserve all 21 routers and 231 ordered view slots, including Fera aliases.
- Keep integer creation_status; no schema/data migration for this rollout.
- Keep Step 0 authorization and POST-only mutation.
- Keep game rules in existing views; no generic-class consolidation or htmx.
- Use the existing isolated worktree. Leave changes reviewable locally.

## Review focus

- Zero freebies before ST approval must not skip the approval wait.
- Background steps with multiple incomplete ratings must not advance too soon.
- Fera subtypes use exact polymorphic content types in freebie filtering.
- Psychic Sorcerers skip hedge paths/rituals, but hedge mages keep both.
- Back must not land on a skipped step that immediately forwards again.

## Task 1: Freeze order and introduce metadata

Files: `characters/chargen/{__init__,registry,definitions,predicates}.py`,
`characters/tests/fixtures/chargen_order.json`, `characters/tests/test_chargen_registry.py`.
Interfaces: `Step`, `Workflow`, `get_workflow(character_type) -> Workflow | None`,
`Workflow.step(position)`, `Workflow.view_mapping`, `Workflow.freebie_step`.

- [x] Capture the existing runtime router order as an independent JSON golden fixture.
- [x] Write tests for exact order, unique keys, one freebie step, template existence and explicit aliases; run and observe missing-registry failure.
- [x] Implement immutable records and composed definitions with lazy imports.
- [x] Run `python manage.py test characters.tests.test_chargen_registry`.

## Task 2: Vampire pilot and shared rendering

Files: `characters/views/core/chargen_mixins.py`, `characters/views/core/human.py`,
`characters/views/vampire/{vampire_chargen,ghoul_chargen,vtmhuman}.py`,
`characters/templates/characters/core/chargen*.html`, Vampire shells/fragments.
Interfaces: `ChargenStepMixin`, registry-derived router mapping, `step` and
`chargen_steps` template context.

- [x] Write owner rendering tests for Vampire positions 1-13; assert Mentor at 10, Contacts at 11, Retainers at 12 and Specialties at 13.
- [x] Observe old blank/wrong-form behavior, then replace mappings and numeric template ladders; retain existing widget and validation markup in partials.
- [x] Add common authorization-before-dispatch, progress and fragment selection.
- [x] Run registry and Vampire chargen tests; prove GET does not mutate.

## Task 3: Central transitions and freebie consumers

Files: `characters/chargen/transitions.py`, `characters/models/core/character.py`,
model freebie constants, `characters/views/core/{human,backgrounds,generic_background,chargen_back}.py`.
Interfaces: `advance(character, *, user) -> int`, `previous_position(character) -> int`,
registry-backed class/instance freebie descriptor.

- [x] Add transition tests for skip chains, denied users, invalid positions, approval waits, multi-record backgrounds, language effect and Back.
- [x] Replace hardcoded QuerySet map and model constants with registry lookup; test actual database membership at correct and incorrect positions.
- [x] Replace view increments and common self-skip handlers with the transition operation, keeping terminal submission explicit.
- [x] Run new transition tests and existing Back/authorization tests.

## Task 4: Remaining gameline batches

Files: chargen views and templates under `core`, `werewolf`, `mage`, `wraith`,
`changeling`, `demon`; per-gameline registry definitions and fragments.

- [x] Integrate Core and Werewolf; preserve Fera's leading breed/faction step.
- [x] Integrate Mage; replace Mage/Companion/Sorcerer ordered skip loops with predicates. Test Psychic versus hedge-mage paths and Chantry selection.
- [x] Integrate Wraith and Changeling with real formset rendering.
- [x] Integrate Demon, Thrall and DtFHuman with complete shells/fragments.
- [x] For each batch run owner GETs for every slot and its existing chargen tests, then check golden order parity.

## Task 5: Safety audit and final verification

- [x] Assert all router targets remain declared by the authorization manifest and no registered views are orphaned.
- [x] Inventory orphan views; remove the two unreferenced Fetish placeholders without inserting positions.
- [x] Check no duplicated numeric template ladders, model constants or raw view increments remain.
- [x] Run targeted chargen, QuerySet, permission and route tests, Django system checks and formatting checks on changed Python files.
- [x] Obtain a fresh whole-change review, fix material findings with regression tests, and record actual verification results below.

## Execution record

- Initial inventory: 21 routers, 231 step slots. Django 5.2.17 is installed.
- Authorization/Chantry changes already present; preserve POST-only skips and current positions.

- Ruling: preserve integer positions and use an independent golden fixture; no data migration is needed because no position changes. Future reorders must migrate Un/Rev rows.
- Ruling: preserve detail-only freebie eligibility in explicit registry metadata without adding creation routers for those types. Removing it would change unrelated approval behavior.
- Ruling: remove the unreferenced Fera/Werewolf Fetish placeholders rather than creating steps from incomplete views. This preserves persisted order.
- Ruling: allow a focused current-step shell to replace cumulative completed-stat ladders; existing detail routes still show the full sheet.
- Ruling: preserve existing form transactions and duplicate-submission behavior. This task does not promise new production database concurrency guarantees.
- Expanded owner coverage fixed pre-existing Fera/Demon form construction, Ally/Enhancement omitted fields, and Companion Library affiliation assumptions.
- Independent whole-change review completed; all three material findings reproduced RED and fixed GREEN (Sorcerer double advance and ritual fields; Wraith completion skips).
- No deferred minor findings. User requested a commit and PR after verification.

### Verification command

The combined run uses the repository's normal settings, database setup and password hasher:

```powershell
python manage.py test characters.tests.test_chargen_registry characters.tests.test_chargen_transitions characters.tests.test_chargen_workflow characters.tests.views.test_chargen_back characters.tests.views.test_chargen_mixins characters.tests.views.core.test_chargen_validation characters.tests.views.vampire.test_vampire_chargen characters.tests.views.vampire.test_ghoul_chargen characters.tests.views.wraith.test_wraith_chargen characters.tests.views.demon.test_demon_chargen characters.tests.views.demon.test_dtfhuman_chargen characters.tests.views.demon.test_thrall_chargen characters.tests.views.mage.test_background_views characters.tests.views.mage.test_chantry_background characters.tests.views.mage.test_mage_chantry_template core.tests.security.test_route_policies core.tests.security.test_object_workflow accounts.tests.context_processors.test_context_processors characters.tests.models.changeling.test_ctdhuman.TestCtDHuman.test_ctdhuman_freebie_step characters.tests.models.demon.test_dtf_human.DtFHumanModelTests.test_freebie_step_is_five characters.tests.models.demon.test_earthbound.EarthboundModelTests.test_freebie_step characters.tests.models.demon.test_thrall.ThrallModelTests.test_freebie_step characters.tests.models.hunter.test_hunter.TestHunter.test_hunter_freebie_step characters.tests.models.hunter.test_hunter.TestHtRHuman.test_htrhuman_freebie_step characters.tests.models.mummy.test_mummy.TestMtRHumanDefaults.test_freebie_step characters.tests.models.mummy.test_mummy.TestMtRHumanDefaults.test_mummy_freebie_step characters.tests.models.vampire.test_ghoul.TestGhoulFreebies.test_freebie_step characters.tests.models.vampire.test_revenant.TestRevenantFreebies.test_freebie_step characters.tests.models.vampire.test_vampire.TestVampireFreebieStep.test_vampire_freebie_step characters.tests.models.wraith.test_wraith.TestWraithCreation.test_wraith_freebie_step --verbosity 0
```

Additional checks: `python manage.py check`, `git diff --check`, Ruff on new registry/tests and shared mixin, Black on changed Python files. No full-project suite or browser automation is claimed.

Final combined verification: **250 tests passed** (234.492 seconds). Django system check reports no issues. Ruff, Black and `git diff --check` pass.

### PR review and rebase verification (2026-09-26)

- Rebased onto `eb5ed842` (`main`, application JavaScript extraction). The Vampire shell conflict was resolved by retaining the shared shell and loading the new static virtues validator from its registered fragment. A regression test checks that binding.
- Checked all three [Claude review comments](https://github.com/charlesmsiegel/tg/pull/1469#issuecomment-5844419562). The inherited `core/form.html` heading already displays the character name; the deliberate current-form layout remains. Added name assertions to the existing 231-slot owner-rendering test.
- Expanded independent expected freebie metadata to all nine detail-only types, checking both class and instance descriptors and detecting entries missing from the test.
- Reproduced the unequal-ability-group case: padding printed literal `None`. Conditional field rendering now keeps the empty cells without that text; the regression test checks the complete padded row.
- Browser inspection also exposed multiline single-line-comment delimiters printing developer notes around buttons and counters. Converted the five affected comments to Django block comments, with rendered-output coverage.
- Combined original verification labels plus `characters.tests.test_static_page_assets` and `widgets.tests.test_static_assets_browser`: **267 tests passed** (135.245 seconds). After the comment cleanup, `python manage.py test characters.tests.test_static_page_assets characters.tests.test_chargen_workflow characters.tests.views.core.test_chargen_validation core.tests.views.test_generic --verbosity 0`: **56 tests passed** (25.746 seconds). System check, Ruff, Black and whitespace checks pass.
- Local Chromium checked all 13 rendered Vampire step pages for name, current progress and heading visibility, and confirmed virtues JavaScript initialization. Rechecked Abilities, Backgrounds and Virtues after the comment cleanup and inspected the corrected Virtues screenshot. These were rendered-page browser checks, not an end-to-end browser submission flow. The in-app browser could not launch because its sandbox helper was unavailable; the local harness used disposable test data and browser profiles.
