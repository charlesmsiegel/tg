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

## Task 1: Tools and safety net

Files: `scripts/template_similarity.py`, `scripts/template_screenshots.py`,
`scripts/screenshot_settings.py`, `core/tests/template_fixtures.py`,
`core/tests/test_template_render_smoke.py`,
`docs/superpowers/specs/2026-09-25-template-consolidation-report.md`.

- [ ] Similarity script: identical + near groups with diffs, JSON, basename stats.
- [ ] Generic fixture seeder; report models it cannot build.
- [ ] Screenshot capture/compare; capture the base commit into a scratch directory.
- [ ] Render smoke test over the fixture set (detail, edit, list pages).
- [ ] Record baseline query counts for character detail pages and the scene page.

## Task 2: Byte-identical groups

- [ ] Delete the 70 templates `find_dead_code.py --section templates` reports as
      unreferenced (all Step 2 leftovers); re-run the dead-code scan and the routed
      template test.
- [ ] Remove one-line stubs: reference `detail.html` ×7 (views → `core/object.html`),
      group detail ×3 (views → `characters/core/group/detail.html`), melee/thrown weapon
      detail (registry → `items/core/weapon/detail.html`).
- [ ] Move live identical groups into `characters/shared/`: `basics_display_include`
      ×6, companion/sorcerer XP form, ghoul/revenant advantage display, ghoul/vampire
      powers display, house/legacy title. Update includes.
- [ ] Screenshot compare: no differences.

## Task 3: Near-identical groups

- [ ] `core/template_resolution.py`: `shared_template_names()` and
      `SharedTemplateMixin`, with tests for order, de-duplication and override.
- [ ] Registry: `get_template_names()` uses `shared_template_names()`;
      `ModelSpec.list_title`; list context `list_title`/`list_heading`;
      `core/registry/list.html` becomes the card list; delete the 30 identical card
      lists and their declarations.
- [ ] `template_select.html` ×6 → `characters/shared/human/template_select.html`
      via `SharedTemplateMixin` on `CharacterTemplateSelectView`.
- [ ] Shared ability block driven by `Human.ability_rows()`; the six gameline
      `ability_block_display.html` files are deleted; `wtohuman/detail.html` includes the
      shared block (expected visual change: WtO Human and Wraith ability cards).
- [ ] Reference `form.html` ×4 and other parameterisable groups found by the script.
- [ ] Screenshot compare: only the listed differences.

## Task 4: Hidden query fixes

- [ ] Failing tests first: specialty lookups do not query per stat; scene page query
      count independent of post count; index/charlist/chronicle character tables
      independent of character count.
- [ ] `Human.specialties_by_stat()`; `get_specialty()` reads it; Changeling/Kinfolk
      views use it; `HumanDetailView` prefetches `specialties`.
- [ ] `for_scene_optimized()` joins owner and annotates `author_is_st`; the template
      loops `posts`.
- [ ] `attach_first_groups()`; the three regroup sites use `first_group`.
- [ ] `characters/tests/views/test_query_budgets.py`: per-page ceilings for every
      gameline's detail pages and the scene page.
- [ ] Screenshot compare: no differences.

## Task 5: Components and styles

- [ ] `core/includes/title.html` uses `object.get_gameline` (expected change: Hunter
      and Mummy header titles become themed).
- [ ] Character index: `<style>` block and inline styles →
      `source_static/pages/character-index.css`.
- [ ] Inline style / `<style>` ratchet test; extends-depth test (≤ 5).
- [ ] `mage/form.html`: read model data from `object`, loop ability fields, one
      Technocracy flag, show rotes/resonance from the object.
- [ ] `StoryXP.rows()` replaces the nested `{% with %}` block.
- [ ] Screenshot compare: only the listed differences.

## Task 6: Verification and hand-off

- [ ] `python manage.py check`; ruff/black on changed Python; full test suite.
- [ ] Re-run the similarity script and record the after numbers in the report.
- [ ] Record completion evidence below; commit per slice; push; open the PR.

## Completion evidence

_To be filled in when the work is verified._
