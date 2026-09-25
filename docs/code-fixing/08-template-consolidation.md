# Task: Design template consolidation and removal of hidden template queries in `tg` (Step 8)

You are designing, **not implementing**, the deduplication and simplification of the Django template layer, and the removal of database queries hidden in templates. The repository is `charlesmsiegel/tg`: Django 5.2, a World of Darkness manager with 8 gamelines and about 890 templates (excluding generated `*/docs/*.html`). You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` (Template Standards) and these skills: `.claude/skills/tg-frontend/SKILL.md` (TG components, gameline theming, `get_heading`) and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. Read the Step 2 (chargen step registry) and Step 6 (permission context) designs if they exist: chargen templates and permission flags in templates belong to those steps. Write:
  - `docs/superpowers/specs/2026-09-25-template-consolidation-design.md`
  - `docs/superpowers/plans/2026-09-25-template-consolidation.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed. Chromium and Playwright are available for screenshot comparisons (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`; don't run `playwright install`).
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one, ideally with a script, and say in the doc which ones you confirmed.

## Current state

**Volume and layout** (Reported).
- characters 543 templates, locations 153, items 104, game 43, core 40, accounts 34.
- The layout is `characters/templates/characters/<gameline>/<model>/`.
- Common names: `detail.html` ×99, `form.html` ×97, `list.html` ×72.

**Byte-identical copies** (Reported): 16 groups covering 70 files. The biggest:
- `history_block_form.html` ×8;
- `freebies_form.html` ×7 (a vampire/ghoul copy is 96% similar);
- `appearance_block_display.html` ×7;
- `history_block_display.html` ×7;
- `appearance_block_form.html` ×6;
- `basics_display_include.html` ×6;
- `specialties_block_form.html` ×5;
- a generic `detail.html` ×7 across unrelated reference models.

**Near-identical copies** (Reported):
- `template_select.html` ×6 (162 lines each) differ in 6 lines: the `data-gameline` value and the heading class.
- `vtmhuman/form.html` vs `wtohuman/form.html` are 0.99 similar.
- In `list.html`, 63 of 72 are at least 0.80 similar to a sibling.
- The six cabal/circle/conclave detail pages are near-identical.

**Inconsistent decomposition** (Reported).
- Detail pages use 4–5 level `extends` chains: `core/object.html` → `core/character/detail` → `core/human/detail` → `<gl>/<gl>human/detail` → `<gl>/<splat>/detail`.
- `wraith/wtohuman/detail.html` (274 lines) overrides nearly everything, while its siblings are 9–14 lines.
- Splat detail pages range from 60 to 365 lines.

**Heavy templates** (Reported):
- **`characters/mage/mage/form.html` (553 lines).**
  - 33 copy-pasted `{% if <ability>_spec %}` lines (`~81-261`).
  - 7 repeats of `{% if form.affiliation.name == "Technocratic Union" %}`.
  - It treats `form` as a model instance (`form.get_heading`, `form.paradigms.all`).
  - It iterates `rotes` and `resonance`, which the view never supplies, so those parts render nothing.
- **`characters/index.html` (597 lines).**
  - A 265-line inline `<style>` block and 56 inline `style=` attributes.
  - `{% regroup chars by group_set.first %}` runs a query per character, even though the view already annotates `first_group_id`.
- **`game/scene/detail.html` (456 lines):** see hidden queries below. Its 329-line inline script is Step 11's.

**Hidden queries.**
- The `get_specialty` filter (`core/templatetags/get_specialty.py`) calls `Human.get_specialty` (`characters/models/core/human.py:373-377`), which runs `self.specialties.filter(stat=stat).first()`. That is one query per call, and prefetching can't help. **Confirmed.**
  - It appears **275 times** in templates (**Confirmed**), usually twice per stat (`{% if object|get_specialty:'x' %}({{ object|get_specialty:'x' }})`).
  - Reported: about 60–80 extra queries per character sheet.
- `game/scene/detail.html:48` loops `object.post_set.all`, ignoring the optimized `context["posts"] = Post.objects.for_scene_optimized(scene)` built at `game/views.py:282`. **Confirmed.** Reported: it also reads `post.character.owner.profile.is_st` per post.
- Reported: the `resonance` and `is_game_st` tags run queries.

**Components, partly adopted** (Reported).
- `tg-card` is used in 434 of the templates; about 313 still use only Bootstrap row/col layout, and 40 use Bootstrap `card`.
- The intended components `core/includes/stat_card.html`, `stat_row.html` and `property_row.html` have zero real uses.
- There are 3,020 inline `style="..."` attributes.
- `core/includes/title.html:~5` maps `get_heading` to `data-gameline` through a 6-branch elif chain with no htr/mtr, while `core/form.html:~21` uses `object.get_gameline`; the two disagree.
- `{% with %}` workarounds (e.g. `accounts/includes/xp_story_st.html:~25-29` nests 5 of them to build field names).

## What the design must deliver

1. **An analysis script** that finds byte-identical and near-identical template groups (with a similarity threshold) and reports each group with its diff. Include its output.
2. **A consolidation mechanism.** For example, shared templates under `characters/templates/characters/shared/` that take the gameline from `object.get_heading` or context, plus a template resolution order (gameline-specific, then shared) via `get_template_names` or the template loader. Show how an override remains possible.
3. **An `extends` hierarchy policy:** the maximum depth, what each level owns, and a fix for the outliers (e.g. `wtohuman/detail.html`).
4. **Query fixes:**
   - replace `get_specialty` with a design that uses prefetched specialties, e.g. a per-object `{stat: specialty}` dict built once, or a prefetch-aware model method;
   - make `scene/detail.html` use `posts`;
   - fix the index regroup;
   - add `assertNumQueries` or query-count budget tests for each gameline's character detail page and the scene page.
5. **Component policy:** adopt or delete `stat_card`, `stat_row` and `property_row`; set rules for `tg-card` vs Bootstrap; move inline styles and the index `<style>` block into stylesheets under `source_static/`. Keep the gameline theming from the tg-frontend skill.
6. **Safety net:** a before/after screenshot comparison (Playwright) for a fixed fixture set covering each gameline's detail, form and list pages, and render smoke tests for every template reachable from a view.
7. **PR slicing:** start with the byte-identical groups (zero-risk), then the near-identical ones, then the query fixes (independent, high value), then components and styles.

## Constraints and scope

- Design only. Don't modify application code.
- Out of scope, owned by other steps:
  - chargen step templates and `creation_status` ladders (Step 2);
  - permission flags such as `is_approved_user` in templates (Step 6);
  - inline JavaScript (Step 9 relocates it, Step 11 rewrites chat);
  - item and location template selection as affected by the Step 7 registry. Coordinate: the registry's shared-template fallback should use your mechanism.
