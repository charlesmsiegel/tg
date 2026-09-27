# Template consolidation and hidden template queries design (Step 8)

The user asked for this step to be planned **and implemented**, which supersedes the
design-only instruction in `docs/code-fixing/08-template-consolidation.md` (Steps 2, 6,
7 and 9 were handled the same way). The implementation plan is
`docs/superpowers/plans/2026-09-25-template-consolidation.md`; the full analysis
output is in `2026-09-25-template-consolidation-report.md`.

## Sources and boundaries

Read: `CLAUDE.md`; the consolidated skill `.claude/skills/tg-standards/` (the
tg-frontend, tg-testing and tg-permissions skills named by the brief were merged into
its `templates.md`, `testing.md` and `permissions.md` references); the Step 2
(chargen registry), Step 6 (permission context), Step 7 (item/location registry) and
Step 9 (JS static assets) designs, all of which are implemented at this HEAD.

Out of scope, and left untouched:

- chargen shells and step fragments (`chargen.html`, `steps/`, `core/chargen/`) and
  `creation_status` logic — Step 2. The 21 byte-identical one-line `chargen.html`
  stubs are Step 2's deliberate per-type override slots.
- permission flags in templates (`object_perms`, `is_approved_user`) — Step 6.
- inline and static JavaScript, including the six `*-template-select.js` files that
  differ only in colour — Step 9; the scene chat script — Step 11.
- item/location URL and view generation — Step 7. Step 7's registry already has a
  shared-template fallback (`core/registry/<action>.html`); this step routes it
  through the same resolution helper instead of adding a second mechanism.

One boundary ruling: Step 2 left **70 legacy step fragments unreferenced** (the old
per-gameline `*_block_form.html`, `freebies_form.html`, `history_*`, `appearance_*`
files). They are most of the audit's byte-identical groups. Deleting unreferenced
files does not change any chargen behaviour, so this step deletes them rather than
"consolidating" dead code.

## Audit verification

Checked at this HEAD with `scripts/template_similarity.py`, `scripts/find_dead_code.py
--section templates`, a Django shell and `CaptureQueriesContext` over the fixture set
described under *Safety net*.

| Audit claim | Finding |
| --- | --- |
| ~890 templates; characters 543, locations 153, items 104, game 43, core 40, accounts 34 | **Confirmed (total), counts drifted**: 890 = characters 539, locations 146, items 98, game 39, core 38, accounts 30. |
| `detail.html` ×99, `form.html` ×97, `list.html` ×72 | **Confirmed for `characters/`**: 99 / 98 / 69. Project-wide 179 / 178 / 145. |
| 16 byte-identical groups, 70 files | **Confirmed, but stale**: 17 groups, 91 files. 21 of them are Step 2's `chargen.html` stubs (new since the audit), and **42 of the remaining 70 are unreferenced** leftovers of Step 2. Only 28 files in 10 groups are live duplicates. |
| `history_block_form` ×8, `freebies_form` ×7, `appearance_block_form` ×6, `specialties_block_form` ×5 | **Confirmed identical, refuted as live**: every copy is unreferenced. |
| `appearance_block_display` ×7, `history_block_display` ×7 | **Confirmed identical**; only the `vtmhuman` copy is live. |
| `basics_display_include` ×6 | **Confirmed**, all six live. |
| generic `detail.html` ×7 across reference models | **Confirmed**: each is the single line `{% extends "core/object.html" %}`. |
| `template_select.html` ×6 differ in 6 lines | **Confirmed**: 4 changed lines per file (`data-gameline`, two heading classes, the JS file name). |
| `vtmhuman/form.html` vs `wtohuman/form.html` 0.99 | **Confirmed**: 0.988. |
| `list.html`: 63 of 72 ≥ 0.80 similar to a sibling | **Confirmed (characters)**: 61 of 69. Project-wide 115 of 145; 32 item/location lists are ≥ 0.90 and differ only in title, heading class and empty text. |
| six cabal/circle/conclave detail pages near-identical | **Refuted/stale**: cabal, circle and conclave are one-line stubs extending `characters/core/group/detail.html`; coterie adds 3 lines. |
| 4–5 level `extends` chains | **Confirmed**: 20 templates sit 5 hops below `core/base.html` (all splat detail pages), 26 at 4. |
| `wtohuman/detail.html` 274 lines overrides nearly everything | **Confirmed, and it is a bug**: it overrides only `abilities`, with an inline block reading `<ability>_spec` variables no view supplies, so Wraith and WtO Human sheets never show specialties. Its sibling `wtohuman/ability_block_display.html` is dead. |
| splat detail pages 60–365 lines | **Confirmed** (21–365). |
| `mage/form.html` 553 lines, 33 `_spec` lines, 7 Technocracy repeats, `form` used as instance, `rotes`/`resonance` never supplied | **Confirmed, worse**: `form.affiliation.name` is the BoundField's HTML name (`"affiliation"`), so the Technocracy labels can never appear; `form.get_heading`, `form.paradigms.all`, `form.languages.all` and `form.get_mf_and_rating_list` all render empty. |
| `characters/index.html` 597 lines, 265-line `<style>`, 56 inline styles | **Confirmed**: 264-line style block, 56 `style=` attributes. |
| `{% regroup chars by group_set.first %}` queries per character | **Confirmed**, plus the same pattern in `charlist_include.html` and `game/chronicle/display_includes/character_table.html`. |
| `get_specialty` one query per call, prefetch can't help | **Confirmed**. |
| 275 uses | **Refuted (low)**: 480 filter applications on 240 lines in 14 templates. |
| ~60–80 extra queries per sheet | **Confirmed**: 73 queries for a VtM/WtA/CtD/MtR human sheet, 71 for vampire/ghoul/revenant, 137 for a Mage (fixture set, staff viewer). Changeling and Kinfolk views add ~40 more by building `<stat>_spec` context with one `specialties.filter()` per stat. |
| `scene/detail.html` loops `object.post_set.all` ignoring `posts` | **Confirmed**; `post.character.owner.profile.is_st` adds 3 queries per post (82 queries for 6 posts). |
| `resonance` and `is_game_st` tags run queries | **Refuted as hot spots**: `resonance` was deleted by Step 1; `is_game_st` is loaded by no template (Step 6 owns the tag library). |
| `tg-card` in 434 templates, ~313 Bootstrap-only, 40 Bootstrap `card` | **Confirmed approximately**: 429, 314, 37. |
| `stat_card` / `stat_row` / `property_row` have zero uses | **Confirmed and already resolved**: Step 1 deleted them. |
| 3,020 inline `style=` attributes | **Confirmed approximately**: 2,888. |
| `title.html` 6-branch chain without htr/mtr disagrees with `core/form.html` | **Confirmed**: Hunter and Mummy page headers lose their themed title colour and font. `get_heading` is literally `f"{get_gameline()}_heading"`. |
| nested `{% with %}` in `xp_story_st.html` | **Confirmed**: five nested `with` blocks to build field names. |

## Analysis tool

`scripts/template_similarity.py [--threshold 0.9] [--same-name-only] [--no-diff]
[--json] [--basename-stats]` scans `<app>/templates/**/*.html` (generated `docs/`
pages excluded) and prints byte-identical groups (SHA-256) and near-identical groups
(line-based `difflib` ratio ≥ threshold, joined transitively with union-find, with a
unified diff of every member against the first). Byte-identical copies collapse to one
representative before comparison. It runs in about a second over 890 templates. It is
paired with the existing `scripts/find_dead_code.py --section templates`, because a
duplicate that nothing references should be deleted, not shared.

## Consolidation mechanism

**Where shared templates live.** Character fragments shared across models or
gamelines go under `characters/templates/characters/shared/<topic>/` (for example
`shared/human/ability_block_display.html`). Cross-app page shells go under
`core/templates/core/shared/`. The item/location registry keeps its fallback
directory `core/templates/core/registry/`.

**Resolution order.** `core.template_resolution.SharedTemplateMixin` turns a view's
template list into *specific, then shared*:

```python
class CharacterTemplateSelectView(SharedTemplateMixin, ...):
    shared_template_name = "characters/shared/human/template_select.html"

class VtMHumanTemplateSelectView(CharacterTemplateSelectView):
    template_name = "characters/vampire/vtmhuman/template_select.html"  # override slot
```

`get_template_names()` returns `[template_name, shared_template_name]`; Django's
`select_template` renders the first that exists. The specific name stays declared as
the override slot: to customise one gameline, create that file, `{% extends %}` the
shared template and override its blocks. `shared_template_names(names, *shared)` is
the plain function behind the mixin; the Step 7 registry calls it to build
`[declared, core/registry/<action>.html]`, so there is exactly one fallback rule.

**Includes.** A shared fragment is included by its shared path. Per-gameline variation
is expressed with the ordinary Django mechanism — a block in the parent template that
a child overrides — not with a dynamic include lookup. Fragments read the gameline from
the object (`object.get_heading`, `object.get_gameline`); no fragment hard-codes a
heading class.

**One-line stubs.** A template whose entire content is `{% extends "X" %}` is removed
and its view names `X` (or X becomes its shared fallback). This applies to the seven
reference `detail.html` stubs, the three group detail stubs and the melee/thrown weapon
detail stubs. Step 2's `chargen.html` stubs are left for Step 2.

**Parameterised shells.** Where copies differ only in literals, the literals become
context: the 30 item/location card lists become `core/registry/list.html`, driven by
`list_title` (registry `ModelSpec.list_title`, defaulting to the model's
`verbose_name_plural`) and `list_heading` (`<gameline>_heading`). The six
`template_select.html` files become one template using `character.get_gameline` and
`character.get_heading`.

## `extends` hierarchy policy

Maximum depth: **5 hops below `core/base.html`**, enforced by a test. Each level owns
one slice and exposes named blocks for the next:

| Level | Template | Owns |
| --- | --- | --- |
| 0 | `core/base.html` | page chrome, assets |
| 1 | `core/object.html` | object page frame: title, description, image, buttons |
| 2 | `characters/core/character/detail.html` | sheet frame, full vs. limited view, scenes, buttons |
| 3 | `characters/core/human/detail.html` | the human sheet: every section block with a shared default include |
| 4 | `<gl>/<gl>human/detail.html` | gameline defaults: which `basics` and `abilities` fragments to include |
| 5 | `<gl>/<splat>/detail.html` | splat-only blocks (powers, advantages, health, …) |

Rules: a level overrides only blocks it owns; a gameline level selects fragments
(one-line `{% include %}` per block) rather than inlining markup; a block that
several gamelines render identically moves up to level 3 as the default.

Outlier fix: `wraith/wtohuman/detail.html` becomes an 8-line level-4 template like its
siblings, including the shared ability block. This is a visible fix — WtO Human and
Wraith sheets gain their specialties and the same ability-card layout as every other
gameline.

## Hidden query fixes

1. **Specialties.** `Human.specialties_by_stat()` returns `{stat: [names]}` built from
   `self.specialties.all()`. If the relation is not already prefetched it calls
   `prefetch_related_objects([self], "specialties")`, which stores the rows in the
   instance's prefetch cache, so **every later call on that instance is free** and the
   relation's own `add()`/`remove()`/`set()`/`clear()` invalidate it automatically.
   `get_specialty(stat)` keeps its signature and semantics (first specialty by the
   model's ordering, else `None`) and reads the map; the `get_specialty` template
   filter is unchanged. The Changeling and Kinfolk views use the map instead of one
   `filter()` per stat. The shared ability block iterates rows from
   `Human.ability_rows()` instead of 30 hand-written `{% if object|get_specialty %}`
   pairs. Detail views prefetch `specialties` in `get_queryset()`.
2. **Scene.** The template loops `posts`. `PostManager.for_scene_optimized()` adds
   `select_related("character__owner")` and an `author_is_st` `Exists()` annotation
   over `STRelationship`, preserving today's "author is an ST anywhere" styling (the
   WebSocket consumer's scope-based `is_st` disagrees; recorded for Step 11).
3. **Group regroup.** `attach_first_groups(characters)` loads the groups named by the
   existing `first_group_id` annotation in one `in_bulk()` query and sets
   `character.first_group`; the three templates regroup by `first_group`. The
   chronicle view annotates its querysets with the same subquery.
4. **Budgets.** `characters/tests/views/test_query_budgets.py` renders every seeded
   character detail page and the scene page with `assertNumQueries`-style ceilings
   (recorded per page after the fix, with a small margin), and asserts that a sheet's
   query count does not grow when specialties are added and that the scene page does
   not grow with the number of posts.

## Component and style policy

- `stat_card`, `stat_row`, `property_row`: already deleted by Step 1. Not revived; the
  shared fragments above are the component layer.
- New or touched templates use `tg-card`/`tg-card-header`/`tg-card-body`,
  `tg-table`, `tg-badge`; Bootstrap is used only for grid layout (`row`, `col-*`) and
  utilities. A Bootstrap `card` is converted when its template is otherwise touched.
- Page headers set `data-gameline="{{ object.get_gameline }}"`; `core/includes/title.html`
  loses its elif chain (this restores Hunter and Mummy header theming).
- Page-specific CSS lives in `source_static/pages/<page>.css`, linked from that page's
  `styling` block at the position of the old `<style>` so the cascade is unchanged. The
  character index `<style>` block and its 56 inline styles move to
  `source_static/pages/character-index.css`.
- A ratchet test (`core/tests/test_template_style_budget.py`) fails when the project's
  inline-style count or the number of `<style>` blocks grows; the budget is lowered as
  templates are cleaned.
- `{% with %}` chains that build field names are replaced by form helpers that yield
  bound fields (`StoryXP.rows()`).
- Gameline theming stays as the tg-standards skill describes: `{{ object.get_heading }}`
  on titles, `data-gameline` on `header-card`s.

## Safety net

- `core/tests/template_fixtures.py::seed()` creates one approved instance of every
  concrete character, item and location model (plus the reference rows they need), a
  chronicle and a scene with posts by an ST and a player. Required fields are filled
  generically; the few models it cannot build are reported, not hidden.
- `scripts/template_screenshots.py capture DIR` seeds a throwaway SQLite database,
  runs `runserver` against it and saves a full-page screenshot, the DOM and the visible
  text of **every** fixture detail and edit page, every routed list page, the character
  index and the scene page (477 pages) as the fixture storyteller, with all external
  requests blocked. `compare BEFORE AFTER` reports status changes, pixel differences
  (with diff images) and text differences. Every PR in this step is checked against the
  base-commit capture; each visible difference is either intended and listed in the
  plan, or fixed.
- `core/tests/test_template_render_smoke.py` renders every seeded object's detail and
  edit page and every argument-free list page through the test client and asserts a
  200 (the Step 1 `KNOWN_MISSING` pages excepted). The existing
  `core/tests/test_routed_templates.py` continues to check that every template
  reachable from a routed view exists and compiles.

## PR slicing

1. **Tools and safety net**: similarity script, fixture seeder, screenshot script,
   render smoke test. No template changes.
2. **Byte-identical (zero risk)**: delete the 70 unreferenced templates; remove the
   one-line stubs; move the live identical groups (basics include, xp form, ghoul
   advantage/powers, house/legacy title) into `shared/`. Screenshot diff must be empty.
3. **Near-identical**: `SharedTemplateMixin` and `template_select`; the registry card
   list; the shared ability block (fixes `wtohuman`); reference forms and group lists
   where they are parameterisable. Expected visual differences: WtO Human/Wraith
   abilities only.
4. **Query fixes** (independent of 2–3, highest value): specialties, scene posts,
   regroup, budget tests. Screenshot diff must be empty.
5. **Components and styles**: `title.html` gameline (expected Hunter/Mummy header
   change), character index stylesheet, style ratchet, `mage/form.html` repair,
   `StoryXP.rows()`.

This session implements all five slices on one branch with one commit per slice so
they can be reviewed in order.

## Risks

- Cached template loader: missing specific names are cached misses, so the
  specific-then-shared lookup costs nothing after the first render.
- `specialties_by_stat()` caches on the instance: a specialty renamed through another
  instance during the same request is not seen until the next request, the same
  staleness any prefetch has.
- Moving inline styles to classes can lose to more specific selectors; the screenshot
  comparison is the check, not code review.
