# Game Rules Out of Views Implementation Plan

> **For agentic workers:** Use test-driven development and verification-before-completion. Steps use checkbox syntax for tracking.

**Goal:** Views only orchestrate. Validation moves to forms, state changes to services, derived values to model methods, read-side aggregation to selectors, and limits to `characters/rules/`.

**Architecture:** Pure rule objects (`AllocationRule`, `PriorityRule`) are enforced by `AllocationFormMixin.clean()`. Step views pass their existing adapter configuration in as rules. Services return `ServiceResult` and own their transactions. Fera dispatch comes from subclass declarations.

**Tech Stack:** Django 5.2, django-polymorphic, unittest.

**Spec:** `docs/superpowers/specs/2026-09-25-game-rules-out-of-views-design.md`

## Global constraints

No migrations, new dependencies, route changes or workflow reordering. Error
and flash message text stays byte-identical unless the spec names a defect.
`advance()` stays in views. GET is read-only. Existing service classes keep
their public API. A behaviour change is allowed only for the spec's "Fixed"
defects (D1, D8–D12), each with a regression test that failed first.

## Review focus

* The first error message on an invalid allocation matches the old view (tests assert text).
* No `form_invalid` → `form_valid` remains; the AST guard enforces this.
* Rote learning cannot overspend under concurrent submits (lock + re-read).
* An invalid Focus or Apocalyptic Form submit writes nothing.
* Each Fera subtype renders the same fields, help text and gift groups as before.

## Task 1: Rules package and core allocation steps

Files: `characters/rules/{__init__,allocation,limits}.py`,
`characters/forms/core/allocation.py`, `characters/views/core/{human,backgrounds,allocations}.py`,
`characters/forms/core/backgroundform.py`, `characters/tests/rules/test_allocation.py`.

- [x] Unit-test `AllocationRule`/`PriorityRule` violations and `client_data()`.
- [x] Characterize the attribute, ability and background POSTs (existing suites plus text asserts).
- [x] Move R9–R11 into forms/formset; views keep context keys and flash hooks.

## Task 2: Mage rules

Files: `characters/forms/mage/{rote,mage,practiceform}.py`, `characters/services/{result,rotes,mage_chargen}.py`,
`characters/models/mage/mage.py`, `characters/views/mage/mage.py`, tests.

- [x] `RoteCreationForm.clean()` replaces both ladders (R1); `learn_rote` service (R2).
- [x] `MageFocusForm` + `PracticeRatingFormSet.clean()` + `set_starting_practices` (R4–R6, D8).
- [x] `MageSpheresForm.resonance` + `Mage.purchase_starting_arete` + remove bypass (R7, R8).
- [x] Detail-page specialties through `SpecialtiesForm` (R27, D12).

## Task 3: Gameline allocation steps and derived stats

Files: Changeling, Vampire, Ghoul, Demon, Thrall and Wraith chargen views;
`Human.apply_courage_willpower`, `Vampire.apply_virtues`.

- [x] Characterize each step's error text, flash messages and derived fields.
- [x] Convert R13–R19 to rules and hooks; add the D1 regression test.

## Task 4: Sorcerer and Demon forms

- [x] `SorcererBasicsForm` restricts chained choices; remove the bypass (R26, D11).
- [x] Numina formsets validate a total of 5; `set_starting_numina` (R20, D10).
- [x] `ApocalypticFormSelectionForm` + `apply_apocalyptic_form`; no mutation on invalid input (R21, D9).

## Task 5: Kinfolk and Companion

- [x] `KINFOLK_TRIBE_BACKGROUND_LIMITS`; `Kinfolk.background_violations` used by the formset and `add_background` (R12).
- [x] `Companion.prepare_starting_freebies` (R25; D2 preserved and pinned).

## Task 6: Fera polymorphism

- [x] Per-subclass declarations; `FeraBreedFactionView`/`FeraGiftsView` without `isinstance` (R22–R24).
- [x] Parametrized test over all 12 subtypes: fields, help text, gift context keys.

## Task 7: Game app and spending locks

- [x] `game/selectors.py` (R29, R30), `game/text.py` (R31), single-save weekly XP request (R28).
- [x] `Factory.locked()` context managers; the shared freebie view and the Mage detail XP spend use them.

## Task 8: Guard, integration, review, delivery

- [x] AST bypass guard test.
- [x] Full test suite, `manage.py check`, Black/Ruff on changed files, whitespace check.
- [x] Adversarial self-review of the diff; implementation record in the spec.
- [x] Commit, push `claude/zealous-fermi-m6cmmo`, open a PR.

## Execution record

Built on `a0e23a0` (Steps 0, 2, 3, 6, 7 and 9 already merged). The audit
confirmed or refuted every "Reported" brief item; see the spec's audit table.
Slices landed as ordered commits in one PR. Each slice was verified with its
characterization and regression tests plus the affected app suites before it
was committed. The final full suite, Django checks and lint results are in the
PR description. Deviations from the design are listed in the spec's
implementation record.
