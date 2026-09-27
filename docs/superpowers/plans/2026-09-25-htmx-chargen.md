# Interactive Chargen (htmx + Alpine) Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans. Tasks are ordered;
> each is an independently reviewable PR. Steps use checkbox syntax.

**Goal:** Vampire character creation runs as one page with fragment step
swaps, live server validation and totals, dot and pool hints, server-driven
conditional fields and chained options, with no build step and no rule
copies in the browser.

**Architecture:** One registry flag (`Workflow.interactive`) turns on a fragment
contract in `ChargenStepMixin`. The same step URL serves the full page, the
step fragment, validate-only feedback and option fragments. Alpine CSP-build
components read only server data.

**Tech Stack:** Django 5.2, htmx 2.0.11, Alpine CSP 3.17.4 (vendored static
files), Playwright for Python against the preinstalled Chromium.

**Spec:** ../specs/2026-09-25-htmx-chargen-design.md

## Global constraints

- No npm, bundler, React or Vite. Rules stay in forms, services and `characters/rules/`.
- Gamelines other than Vampire must render byte-for-byte as before (the flag is off).
- No new URLs; every mode goes through the router and `CHARGEN_STEP`.
- No inline scripts, `hx-on` handlers or eval, so CSP readiness is preserved.
- Keep Step 2 fragment paths and saved positions.

## Review focus

- A validate-only POST writes nothing and never advances, even on a skippable step.
- A redirect out of the wizard during a fragment request becomes `HX-Redirect`, never a nested page.
- Stale validate or options responses never paint a different step.
- Option requests reject non-chained, root or unknown fields, and never leak the CSRF token into URLs.
- Vendored bytes match the recorded SRI.

### Task 1 (PR 1): Vendor libraries and htmx helpers

Files: `source_static/vendor/**`, `source_static/vendor/VENDOR.md`, `core/htmx.py`,
`core/templates/core/includes/{interactive_scripts,messages}.html`,
`core/templates/core/base.html`, `core/tests/test_htmx.py`.
Interfaces: `is_htmx(request)`, `is_fragment_request(request)`,
`hx_redirect(url)`, `mark_fragment(response, kind)`, `vary_on_htmx(response)`.

- [x] Download the npm tarballs, check the registry `sha512` integrity, copy the minified dist files and their license text.
- [x] Record the version, source, npm integrity, SRI `sha384` and license in `VENDOR.md`.
- [x] Add the include with `integrity`/`crossorigin` attributes and the htmx meta config.
- [x] Move base messages into an include with an always-present `#tg-messages` live region.
- [x] Tests: helpers; SRI of each file equals the include; the include references only vendored static paths.

### Task 2 (PR 2): Fragment contract for interactive workflows

Files: `characters/chargen/{registry,definitions}.py`,
`characters/views/core/chargen_mixins.py`, `characters/views/core/human.py`
(router guard), `characters/templates/characters/core/chargen.html`,
`characters/templates/characters/core/chargen/{interactive,step,step_fragment}.html`,
`characters/static/characters/js/chargen.js`, Vampire step fragments,
`characters/tests/views/test_chargen_htmx.py`.
Interfaces: `Workflow.interactive`; `bind(..., interactive=False)`;
context `chargen_interactive`; response headers `Vary: HX-Request` and `TG-Fragment`.

- [x] Registry flag, set for `VAMPIRE` only; a test asserts which workflows are interactive.
- [x] `ChargenStepMixin.render_to_response` picks the fragment template for fragment requests and adds the headers.
- [x] `dispatch`: redirects out of the wizard become `HX-Redirect`; redirects within the wizard are left for the XHR to follow.
- [x] Router: a fragment request for a character outside the wizard gets `HX-Redirect`.
- [x] Templates: interactive shell, form swap target, OOB progress and messages, Back with `hx-post`.
- [x] `chargen.js`: fragment-header swap guard, focus management, stale-step guard.
- [x] Vampire fragments: take totals from the rules (drift), drop duplicate CSRF tokens, drop `vampire-virtues.js` (deleted).
- [x] Tests: full vs fragment per step shape; history restore; terminal `HX-Redirect`; Back; non-interactive gamelines unchanged; authorization for every mode.

### Task 3 (PR 3): Validate-only mode and totals

Files: `characters/rules/allocation.py`, `characters/forms/core/backgroundform.py`,
`characters/views/core/chargen_mixins.py`,
`characters/templates/characters/core/chargen/feedback.html`, tests.
Interfaces: `AllocationRule.status(values)`, `PriorityRule.status(values)`,
`BackgroundRatingFormSet.allocation_status()`, `ChargenStepMixin.validation_totals(form)`;
setting `CHARGEN_PARTIAL_LIMIT`.

- [x] Pure `status()` methods on the rules plus unit tests; `client_data()` lists `fields`/`groups`.
- [x] Formset status using the same multiplier arithmetic as `clean()`.
- [x] Handle `_validate` in `dispatch` after authorization and before skip/advance; answer 204 on unavailable steps; per-user throttle.
- [x] Feedback fragment with the first error, totals and remaining freebies.
- [x] Tests: no INSERT/UPDATE/DELETE; state unchanged; no advance on a skippable step; throttle; messages match the submit verdict.

### Task 4 (PR 4): Alpine components, chained options, conditional fields

Files: `characters/static/characters/js/chargen-components.js`,
`widgets/widgets/dots.py`, `widgets/templates/widgets/dot_rating.html`,
`widgets/widgets/chained.py` (`HtmxChainedSelect`),
`widgets/mixins/{chained,conditional}.py`,
`characters/templates/characters/core/chargen/{options,freebies_chained,pool}.html`,
block templates (conditional includes), `source_static/style.css`, tests.
Interfaces: `DotRatingInput(min, max)`; Alpine `tgDots`, `tgPool`, `tgConditional`;
`ConditionalFieldsMixin.field_visibility(values)`; `ChainedSelectMixin.enable_htmx(url)`;
`GET ?_options=<child>`.

- [x] Dot widget swapped in by the mixin for rule fields, with min/max from `client_data()`.
- [x] Pool status include replaces the attribute, ability and virtue counters on interactive pages (the old includes stay for other gamelines).
- [x] Python visibility evaluator with a case table mirroring `conditional.js`.
- [x] Options mode on the step URL; `HtmxChainedSelect`; freebies fragment with wrappers and a cost table from `characters.costs`.
- [x] Tests: options filtering, rejection of bad fields, visibility header; the evaluator; no chained or conditional scripts on interactive pages.

### Task 5 (PR 5): Browser tests, no-JS walkthrough, measurements, cleanup

Files: `characters/tests/browser/test_chargen_interactive.py`,
`characters/tests/views/test_chargen_nojs_walkthrough.py`; deletion of the
point-pool stack and its tests; updates to Step 9 asset tests.

- [x] Playwright: dots, pool, conditional and options, in-flight validation across a swap, expired session, JS/Python visibility parity, full 13-step walkthrough with request counting.
- [x] No-JS walkthrough through the test client.
- [x] Delete `point_pool.{py,js}`, the point-pool mixins, `AttributeForm`, `AbilityForm`, `SphereForm`, `form_pool.html` and their tests; update `widgets/__init__.py`.
- [x] Record the metrics and go/no-go evidence below.

## Suggested PR order

1 → 2 → 3 → 4 → 5, as above. PR 2 is usable alone (fragment step swaps);
PR 3 and PR 4 are independent of each other after PR 2. Rollout PRs per
gameline follow the spec's order, each setting `interactive=True` and
converting that gameline's step fragments.

## Execution record

- **Ruling:** the user asked for the plan to be implemented, which supersedes the brief's design-only scope, as in Steps 2, 3, 4 and 9. All five tasks are implemented in this branch as four commits (the spec plus Task 1; Tasks 2-4; the point-pool deletion from Task 5; tests and records).
- **Ruling:** the referenced frontend, domain, permissions and testing skills are consolidated in `.claude/skills/tg-standards/`; its references were used.
- **Ruling:** Playwright for Python is a development-only dependency and is not added to `requirements.txt`. The browser tests skip without it and use the preinstalled Chromium (`/opt/pw-browsers`, or `TG_BROWSER_BINARY`); `playwright install` is never run.
- **Baseline:** 428 chargen, Vampire and widget tests passed before any change.
- **Deviation:** there is no abort-on-submit for in-flight validation; see the spec's implementation record. A browser test holds a validation across the swap instead.
- **Defects found and fixed on the Vampire path:** the freebies Trait select never received options (confirmed in Chromium); a bound re-render crashed on option metadata; conditional fields were dead on the chargen freebies step; the Disciplines and Virtues text hard-coded their totals; client validators disagreed with the server (the abilities script disabled Save, the attributes script rewrote `max`); duplicate CSRF inputs; double submission (Save is now disabled while a request is in flight).
- **Defects confirmed but left for their owners:** the same freebies Trait defect on ten non-pilot chargen views, which their rollout PRs fix; a 403 on the generic router fallback for submitted Vampires; the missing out-of-clan Discipline freebie cost; `object.name|safe` in `core/form.html`.

### Measurements (pilot success criteria)

| Measure | Before | After |
|---|---|---|
| Full page loads for the 13-step walkthrough (17 saves, 9 of them freebies) | 18 (1 plus one Post/Redirect/Get page per save) | **1** for the wizard, plus 1 for the submitted character's page |
| XHRs in that walkthrough | 0 | 61-65 (varies with debounce timing): 17 saves, their followed redirects, debounced validations and option fetches |
| HTML per step response | full page, 22-48 KB | fragment, 10.6-36.5 KB (about 11.5 KB of page chrome saved on every step) |
| Application JS loaded across Vampire chargen pages | 895 lines (attribute 231, ability 84, background 80, core validation 43, virtues 52, chained 215, conditional 190) | **174 lines** (`chargen.js` 57, `chargen-components.js` 117), plus vendored htmx 2.0.11 (52 KB) and Alpine CSP 3.17.4 (72 KB) |
| Application JS deleted | | 494 lines (`point_pool.js` 442, `vampire-virtues.js` 52); 2,383 lines in total with the unused point-pool Python and tests |
| Client-side rule copies on Vampire pages | 4 (distribution, ability cap, background budget, virtue total) | 0: only server data is read |

### Go/no-go evidence

1. Existing chargen tests plus 34 contract tests pass, and non-interactive gamelines are unchanged (`NonInteractiveWorkflowTests`). Full suite after rebasing onto `main` (Step 8), with browser tests enabled: 7,392 tests, 33 skipped, 3 failures. Two of them (`TestHumanCharacterCreationView.test_creation_status_selector` and `TestAttributeView.test_update_view_template`) fail identically on `main` (7,387 tests). The third was a query-budget test under load: `main` failed a different one in the same concurrent run, and `core.tests.test_query_budgets` passes in isolation on this branch.
2. The no-JS 13-step walkthrough passes (`test_chargen_nojs_walkthrough`).
3. The Playwright walkthrough passes with one wizard page load and no console errors from application code (7 browser tests).
4. There are no client rule copies (table above). Validate and submit verdicts agree (`test_verdict_matches_submit_for_virtues`).
5. Authorization tests cover every mode for other players, anonymous users and submitted characters, and validate-only is shown to make zero INSERT/UPDATE/DELETE statements.
6. Production observation (one week without unexpected guard navigations) is the owner's call and cannot be checked from here.
