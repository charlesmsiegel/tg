# Task: Design moving JavaScript out of Python strings and inline templates in `tg` (Step 9)

You are designing, **not implementing**, the relocation of the application's JavaScript into real static files. Today that JS lives as Python string constants inside form widgets and as inline `<script>` blocks in templates. The repository is `charlesmsiegel/tg`: Django 5.2, a server-rendered World of Darkness manager. This step is a **relocation without behaviour change**. There is no build step and no npm, and it must stay that way. Step 10 later decides which pieces get rewritten with htmx/Alpine. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/tg-frontend/SKILL.md` and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. Read the Step 0 design if it exists: it replaces the `/__chained_select__/` endpoint's dynamic import with an allowlist, and the chained-select JS must keep working against it. Write:
  - `docs/superpowers/specs/2026-09-25-js-static-assets-design.md`
  - `docs/superpowers/plans/2026-09-25-js-static-assets.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed. Chromium and Playwright are available (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`; don't run `playwright install`). `requirements.txt` also pins `selenium`.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## Current state

- **Static assets.** `STATICFILES_DIRS = [BASE_DIR / "source_static"]` (`tg/settings/base.py:136`, **Confirmed**). All 11.4k lines of JS there are Bootstrap (`source_static/boot/js/`). There are no application `.js` files. **Confirmed.**
- **JS stored as Python string constants and emitted inline by widget `render()`.** The names are **Confirmed**; line counts are Reported:

  | Constant | File | Lines |
  |---|---|---|
  | `POINT_POOL_JS` | `widgets/widgets/point_pool.py:19` | 442 |
  | `FILTERABLE_LIST_JS` | `widgets/widgets/filterable.py:58` | 358 |
  | `FORMSET_MANAGER_JS` | `widgets/widgets/formset_manager.py:19` | 332 |
  | `CHAINED_SELECT_JS` | `widgets/widgets/chained.py:14` | 216 |
  | `CONDITIONAL_FIELDS_JS` | `widgets/mixins/conditional.py:57` | 191 |
  | `OPTION_METADATA_JS` | `widgets/widgets/metadata_select.py:40` | 109 |
  | `CREATE_OR_SELECT_JS` | `widgets/widgets/create_or_select.py:15` | 95 |

- **"Emit once" flags are not thread-safe.** `ChainedSelect._js_rendered` and `CreateOrSelectWidget._js_rendered` are **class-level** flags reset by a `request_finished` signal (`widgets/widgets/chained.py:242-332`, `widgets/widgets/create_or_select.py:132-183`). **Confirmed.** Under concurrent requests this state is shared, so scripts can go missing or be emitted twice. `core/views/generic.py:121` has a similar `render_formset_manager_script_once()`.
- **Inline template JS** (Reported): about 1,640 lines across 25 templates. The largest are:
  - `game/scene/detail.html` (329; owned by Step 11, excluded here)
  - `characters/core/attribute_block/form.html` (232; point-allocation validator with values interpolated from `{{ primary }}` and similar)
  - `items/mage/wonder/form_include.html` (108)
  - `characters/mage/mage/mage_xp_form.html` (88)
  - `characters/core/ability_block/validation.html` (84)
  - `characters/core/background_block/form.html` (83)
  - `characters/vampire/vampire/chargen.html` (53)
  - six copies of `template_select.html` (36 each)
  - a global `TG.validation` helper in `core/form.html:~116+`
- **Freebie forms** get show/hide logic from `{{ form.conditional_js }}` in 14 templates (Reported).
- **Chained selects** embed the whole choice tree as JSON at render time (`widgets/mixins/chained.py:~103-168`, Reported). They are used by about 15 form modules.
- **There is no Content-Security-Policy today.** Moving scripts out of templates is also what would make a strict CSP possible later.

## What the design must deliver

1. **File layout and loading.**
   - Where each script lives, e.g. `widgets/static/widgets/*.js` for widget behaviour and `<app>/static/<app>/js/*.js` for page scripts.
   - Plain scripts or native ES modules, with no bundler.
   - How widgets declare their JS through Django `forms.Media`, which naturally deduplicates, so the `_js_rendered` flags and `render_*_once` helpers can be deleted.
   - How templates render `{{ form.media }}`.
2. **Passing configuration to scripts:** replace string interpolation into JS with `data-*` attributes and `{{ value|json_script:"id" }}`. Specify the conventions, including initialization for elements added dynamically (formset rows).
3. **An inventory table:** every inline `<script>` and every Python-string JS constant, its destination file, its config inputs, and whether Step 10 is expected to replace it. For code Step 10 will replace (point pools, attribute/ability/background validators, conditional fields, chained selects), **move it verbatim, don't refactor it**.
4. **Caching and versioning:** static file names, `ManifestStaticFilesStorage` or equivalent if not already used (check the settings), and cache-busting.
5. **Tests:**
   - browser tests (Playwright or the existing Selenium) for each moved behaviour, written **before** the move and run against both versions: point pool totals, chained select population, conditional fields, formset add/remove, filterable list, create-or-select, and the attribute validator;
   - a test that no template contains inline `<script>` outside an allowlist.
6. **A CSP readiness note:** what remains after this step that would block `script-src 'self'` (inline event handlers such as `onclick=` and `javascript:` URLs), without adding a CSP.
7. **PR slicing:** widgets first, one widget per PR; then template scripts by app.

## Constraints and scope

- Design only. Don't modify application code.
- No npm, bundler or Vite. Vendored static files only.
- Behaviour must stay identical.
- Out of scope: the scene chat script (Step 11); htmx/Alpine rewrites (Step 10); server-side validation rules (Step 4).
