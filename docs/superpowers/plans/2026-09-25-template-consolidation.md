# Template consolidation implementation plan (Step 8)

> **For agentic workers:** Use superpowers:executing-plans to implement these tasks in order.

**Goal:** Remove duplicated templates, give shared templates one resolution rule, and
remove the database queries hidden in templates, without changing what pages show
except for the listed bug fixes.

**Architecture:** Shared fragments under `characters/shared/` and `core/shared/`;
`SharedTemplateMixin` / `shared_template_names()` for specific-then-shared lookup (also
used by the Step 7 registry fallback); prefetch-aware specialty map; view-built group
map; screenshot comparison over a generic fixture set.

**Tech stack:** Django 5.2 templates, django-polymorphic 4.1, Playwright (optional dev
tool) and Pillow for screenshots.

**Spec:** `docs/superpowers/specs/2026-09-25-template-consolidation-design.md`

## Global constraints

- No chargen shell/step changes (Step 2), no permission-flag changes (Step 6), no
  JavaScript changes (Steps 9/11), no item/location routing changes (Step 7).
- Every slice is compared with the base-commit screenshot capture. Allowed visual
  differences are listed per task; anything else is a bug in the slice.
- Keep `get_specialty(stat)` and the `get_specialty` filter working for other callers.

## Task 1: Tools and safety net (commit 1)

Files: `scripts/template_similarity.py`, `scripts/template_screenshots.py`,
`scripts/screenshot_settings.py`, `core/tests/template_fixtures.py`,
`core/tests/test_template_render_smoke.py`,
`docs/superpowers/specs/2026-09-25-template-consolidation-report.md`.

- [x] Similarity script: identical + near groups with diffs, JSON, basename stats.
- [x] Generic fixture seeder (one approved instance per concrete character, item and
      location model, reference rows, chronicle, scene with ST and player posts);
      reports the three models it cannot build.
- [x] Screenshot capture/compare; base commit captured (477 pages, only the two
      `KNOWN_MISSING` Ritual pages non-200).
- [x] Render smoke test over the fixture set (detail, edit, list pages).
- [x] Baseline query counts for character detail pages and the scene page.

## Task 2: Byte-identical groups (commit 2)

- [x] Delete the 70 templates `find_dead_code.py --section templates` reported as
      unreferenced (Step 2 leftovers; detail pages already show their fields).
- [x] Remove one-line stubs: reference `detail.html` ×7 (views → `core/object.html`),
      group detail ×3 (→ `characters/core/group/detail.html`), melee/thrown weapon
      detail (registry → `items/core/weapon/detail.html`).
- [x] Move live identical groups into `characters/shared/`: `basics_display_include`
      ×6, companion/sorcerer XP form, ghoul/revenant advantage display, ghoul/vampire
      powers display, house/legacy court title.
- [x] Screenshot compare: no differences.

## Task 3: Near-identical groups (commit 3)

- [x] `core/template_resolution.py` (`shared_template_names()`),
      `core.mixins.SharedTemplateMixin` and `ListHeadingMixin`, with tests for order,
      de-duplication, fallback and override.
- [x] Registry: `get_template_names()` uses `shared_template_names()`;
      `ModelSpec.list_title`/`plural_label`; list context `list_title`/`list_heading`;
      `core/registry/list.html` is the card list; 29 identical lists and their
      declarations deleted; base Item/Location lists keep `core/registry/object_list.html`.
- [x] `template_select.html` ×6 → `characters/shared/human/template_select.html`.
- [x] Shared ability block driven by `AbilityBlock.ability_sections()`; moved to the
      human sheet level; six gameline blocks and the inline WtO block deleted; Hunter
      keeps an empty block (`HtRHuman` lists non-field abilities).
- [x] Group lists ×5 → `characters/shared/group/list.html`; reference forms ×4 →
      `characters/shared/reference/form.html` (`verbose_name` filter).
- [x] Screenshot compare: WtO Human/Wraith and base Human sheets only.

## Task 4: Hidden query fixes (commit 4)

- [x] Failing tests first (`test_specialty_lookup.py`, `test_query_budgets.py`, both
      confirmed failing on the pre-fix commit: 3 of 5 and 7 of 8).
- [x] `Human.specialties_by_stat()`; `get_specialty()` reads it; unused Changeling
      and Kinfolk `<stat>_spec` context deleted.
- [x] `for_scene_optimized()` joins the owner and annotates `author_is_st`; the
      template loops `posts`.
- [x] `attach_first_groups()`; index, retired/deceased/NPC lists and chronicle tables
      regroup by `first_group`.
- [x] `core/tests/test_query_budgets.py`: per-page ceilings for all 44 seeded
      character models, the scene page and the index, plus scaling checks.
- [x] Screenshot compare: no differences.

## Task 5: Components and styles (commit 5)

- [x] `core/includes/title.html` uses `object.get_gameline`.
- [x] Character index: `<style>` block and 56 inline styles →
      `source_static/pages/character-index.css` (one selector raised to out-rank
      Bootstrap's striped rows, as the inline style did).
- [x] `core/tests/test_template_policy.py`: inline-style budget, `<style>` allowlist,
      extends depth ≤ 5.
- [x] `mage/form.html` (553 → 376 lines) via `MageFormContextMixin`; the five human edit
      forms read specialties and secondary abilities from `object`; the
      `get_specialty` filter tolerates a missing object.
- [x] `StoryXP.rows()` replaces the nested `{% with %}` block.
- [x] Screenshot compare: no differences on fixture pages.

## Task 6: Verification and hand-off

- [x] `python manage.py check`; ruff (F, I, E9) and black on changed Python files.
- [x] Full test suite (see evidence).
- [x] Similarity script re-run; after numbers in the report and the design's Results.
- [x] Commit per slice; push; open the PR.

## Completion evidence

Recorded 2026-09-27 in the cloud container (Python 3.11, Django 5.2.17, SQLite).

- `python manage.py check`: no issues.
- Full suite, four workers, on the slice-5 commit: 7,316 tests, 34 skipped, 3 failures.
  Two are pre-existing and fail identically on the base commit `a0e23a0` (7,279 tests,
  same 2 failures): `test_human.TestHumanCharacterCreationView.test_creation_status_selector`
  and `test_human.TestAttributeView.test_update_view_template` (they expect a
  `characters/core/human/attributes.html` template that Step 2's chargen shell no
  longer uses). The third, `TestChangelingDetailViewContext.test_detail_view_context_has_specialties`,
  asserted the unused `strength_spec` context removed in slice 4; it was replaced by a
  test that the sheet shows the specialty, folded into that commit, and passes.
- New Step 8 tests: render smoke (477 fixture pages), query budgets (8), template
  policy (3), template resolution (7), specialty lookup (5), shared character
  templates (5), Mage form template (4), `StoryXP.rows()` (1), `get_specialty` filter
  without an object (1).
- `ruff check --select F,I,E9` on every changed Python file: no new findings (three
  pre-existing F841s in `mage.py`, `kinfolk.py`). New Python files are black-clean.
  Existing files were not reformatted wholesale: the installed black (26.x) differs
  from the pre-commit pin (24.3) and would restyle unrelated code.
- Screenshots: 477 pages captured at the base commit and after every slice. Final
  comparison lists only the WtO Human, Wraith and base Human sheets (and the base
  Human edit URL, which lands on the same sheet), the two `KNOWN_MISSING` debug pages
  and render noise on one scene page; see the design's *Results*.
- Similarity: 890 → 755 templates; byte-identical 17 groups/91 files → 2/26;
  near-identical (≥ 0.90) 31/126 → 22/66.

Rulings made while implementing: dead duplicates are deleted rather than shared;
one-line stubs are replaced by pointing views at their parent; the base Item/Location
lists keep their `str()` rows; Hunter sheets keep no ability block until `HtRHuman`'s
ability lists are fixed; edit-form field drift is recorded, not rebuilt, in this step.
