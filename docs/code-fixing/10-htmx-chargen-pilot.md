# Task: Design interactive character creation with htmx and Alpine.js, piloted on one gameline, in `tg` (Step 10)

You are designing, **not implementing**, an interactive character-creation ("chargen") experience that reaches the goals a React/Vite rewrite would have had, **without** React, Vite, npm or a build step:
- step transitions without full page reloads;
- live server-side validation and running totals (freebies, point pools);
- instant feedback when clicking dots;
- conditional fields;
- dependent (chained) selects.

The tools are **htmx** and **Alpine.js**, vendored as static files alongside Bootstrap in `source_static/`, plus optionally the `django-htmx` pip package. The repository is `charlesmsiegel/tg`: Django 5.2 with django-polymorphic 4.1, a server-rendered World of Darkness manager. The owner explicitly chose this over React to keep game rules in Python only. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/tg-frontend/SKILL.md`, `.claude/skills/tg-domain/SKILL.md`, `.claude/skills/tg-permissions/SKILL.md` and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. This step builds directly on:
  - Step 0: authorization and the chained-select allowlist;
  - Step 2: the chargen step registry and per-step template partials;
  - Step 3: shared step views;
  - Step 4: rules in forms and services, and the cost/limit data source;
  - Step 9: JS in static files.

  Read those designs if they exist; where one is missing, state your assumptions about it explicitly. Write:
  - `docs/superpowers/specs/2026-09-25-htmx-chargen-design.md`
  - `docs/superpowers/plans/2026-09-25-htmx-chargen.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed. Chromium and Playwright are available (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`; don't run `playwright install`).
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## How chargen works today

- **Every step is a full page load at `/characters/<pk>/`.** Two `DictView` hops route it by `type`, then by `creation_status`, to a step view (`characters/views/core/__init__.py:138`, `characters/views/core/human.py:653-668`). **Confirmed.** Each type's single `chargen.html` shows the right form using `{% if object.creation_status == N %}` ladders; Step 2 replaces these with per-step partials.
- **Client-side interactivity today** (Reported):
  - `widgets/widgets/point_pool.py` `POINT_POOL_JS` (442 lines, stored as a Python string);
  - `characters/core/attribute_block/form.html` (a 232-line inline validator);
  - `characters/core/ability_block/validation.html` (84 lines);
  - `characters/core/background_block/form.html` (83 lines);
  - `{{ form.conditional_js }}` show/hide in 14 freebies templates (`widgets/mixins/conditional.py` `CONDITIONAL_FIELDS_JS`);
  - chained selects (`widgets/widgets/chained.py`) that embed the entire choice tree as JSON;
  - a global `TG.validation` in `core/form.html`.
- **These client validators duplicate server rules and drift.** Recent commits were needed to "align client-side chargen validation with server rules".
- **An unused, half-built alternative** exists: `characters/forms/core/attribute_form.py` (`AttributeForm` with `DistributionPoolMixin`) and `attribute_block/form_pool.html`, which says it "replaces ~230 lines of custom JavaScript". Evaluate reusing its ideas.
- **Existing JSON endpoints.** There are 12 AJAX endpoints, all unreferenced (Step 1 removes them), and a `/__chained_select__/` endpoint (`widgets/views.py`) that Step 0 converts to an allowlist.
- **Back navigation:** `characters/views/core/chargen_back.py`. **Progress bar:** `ChargenProgressMixin` (`characters/views/core/chargen_mixins.py`).
- **Pilot candidate: Vampire.** It has 13 steps (`characters/views/vampire/vampire_chargen.py:~349-364`) and its template has known drift. Alternatively, use whichever gameline Step 2 migrates first.

## What the design must deliver

1. **A request/response contract:**
   - A step view returns the step partial when `HX-Request` is present and the full page otherwise, so the page still works without JS.
   - Specify the swap target, `hx-push-url` behaviour, and the final-step redirect (`HX-Redirect`).
   - Specify how validation errors re-render, and how the progress bar and back navigation update (out-of-band swaps).
2. **Live validation without duplicated rules:** a "validate only" mode on the same step endpoint (e.g. `hx-post` with `hx-trigger="change delay:…"` and a validate flag). It runs the Step 4 form and service checks without saving and returns the fields plus totals partial. Consider rate limiting, debounce and request cancellation (`hx-sync`).
3. **Alpine components** for instant feedback on dot and pool widgets and for conditional fields:
   - limits and costs come from the server (Step 4's data source) through `data-*` attributes or `json_script`;
   - the server remains authoritative on submit;
   - specify each component's API and how it replaces the current point-pool, attribute, ability and background scripts and `conditional_js`.
4. **Chained selects via `hx-get`** to the Step 0 allowlisted endpoint, returning `<option>` fragments. Specify how forms that need `user` or `character` kwargs are handled.
5. **Cross-cutting concerns:**
   - CSRF with htmx (e.g. `hx-headers` on `<body>` from the CSRF token);
   - authorization on every fragment endpoint, reusing Step 0 gates, never "hidden because not rendered";
   - Alpine's CSP build versus standard build, given there's no CSP today;
   - vendoring, version pinning and SRI for htmx and Alpine;
   - whether to add `django-htmx`;
   - accessibility (focus management after swaps, `aria-live` for totals).
6. **Tests:** Django test-client tests for full vs fragment responses and validate-only mode (no DB writes); Playwright tests for Alpine behaviours and a full pilot wizard walkthrough; a no-JS walkthrough test.
7. **Pilot success criteria and rollout:**
   - measure lines of JS removed, requests per wizard, and any correctness bugs fixed;
   - define the go/no-go criteria for rolling out to other gamelines;
   - give a per-gameline rollout order.
8. **A short "where htmx/Alpine would be the wrong tool" section,** to mark the boundary of this approach for future features.

## Constraints and scope

- Design only. Don't modify application code.
- No React, Vite, npm or bundler. Rules stay in Python; client code may only hint.
- Out of scope: scene chat (Step 11); non-chargen pages. Detail-page actions from Step 5 may adopt the fragment hook later; mention it, but don't design it.
