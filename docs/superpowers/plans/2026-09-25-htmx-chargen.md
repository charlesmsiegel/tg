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

- [ ] Download the npm tarballs, check the registry `sha512` integrity, copy the minified dist files and their license text.
- [ ] Record the version, source, npm integrity, SRI `sha384` and license in `VENDOR.md`.
- [ ] Add the include with `integrity`/`crossorigin` attributes and the htmx meta config.
- [ ] Move base messages into an include with an always-present `#tg-messages` live region.
- [ ] Tests: helpers; SRI of each file equals the include; the include references only vendored static paths.

### Task 2 (PR 2): Fragment contract for interactive workflows

Files: `characters/chargen/{registry,definitions}.py`,
`characters/views/core/chargen_mixins.py`, `characters/views/core/human.py`
(router guard), `characters/templates/characters/core/chargen.html`,
`characters/templates/characters/core/chargen/{interactive,step,step_fragment}.html`,
`characters/static/characters/js/chargen.js`, Vampire step fragments,
`characters/tests/views/test_chargen_htmx.py`.
Interfaces: `Workflow.interactive`; `bind(..., interactive=False)`;
context `chargen_interactive`; response headers `Vary: HX-Request` and `TG-Fragment`.

- [ ] Registry flag, set for `VAMPIRE` only; a test asserts which workflows are interactive.
- [ ] `ChargenStepMixin.render_to_response` picks the fragment template for fragment requests and adds the headers.
- [ ] `dispatch`: redirects out of the wizard become `HX-Redirect`; redirects within the wizard are left for the XHR to follow.
- [ ] Router: a fragment request for a character outside the wizard gets `HX-Redirect`.
- [ ] Templates: interactive shell, form swap target, OOB progress and messages, Back with `hx-post`.
- [ ] `chargen.js`: fragment-header swap guard, focus management, abort validation on submit, stale-step guard.
- [ ] Vampire fragments: take totals from the rules (drift), drop duplicate CSRF tokens, drop `vampire-virtues.js` (deleted).
- [ ] Tests: full vs fragment per step shape; history restore; terminal `HX-Redirect`; Back; non-interactive gamelines unchanged; authorization for every mode.

### Task 3 (PR 3): Validate-only mode and totals

Files: `characters/rules/allocation.py`, `characters/forms/core/backgroundform.py`,
`characters/views/core/chargen_mixins.py`,
`characters/templates/characters/core/chargen/feedback.html`, tests.
Interfaces: `AllocationRule.status(values)`, `PriorityRule.status(values)`,
`BackgroundRatingFormSet.allocation_status()`, `ChargenStepMixin.validation_totals(form)`;
setting `CHARGEN_VALIDATE_LIMIT`.

- [ ] Pure `status()` methods on the rules plus unit tests; `client_data()` lists `fields`/`groups`.
- [ ] Formset status using the same multiplier arithmetic as `clean()`.
- [ ] Handle `_validate` in `dispatch` after authorization and before skip/advance; answer 204 on unavailable steps; per-user throttle.
- [ ] Feedback fragment with the first error, totals and remaining freebies.
- [ ] Tests: no INSERT/UPDATE/DELETE; state unchanged; no advance on a skippable step; throttle; messages match the submit verdict.

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

- [ ] Dot widget swapped in by the mixin for rule fields, with min/max from `client_data()`.
- [ ] Pool status include replaces the attribute, ability and virtue counters on interactive pages (the old includes stay for other gamelines).
- [ ] Python visibility evaluator with a case table mirroring `conditional.js`.
- [ ] Options mode on the step URL; `HtmxChainedSelect`; freebies fragment with wrappers and a cost table from `characters.costs`.
- [ ] Tests: options filtering, rejection of bad fields, visibility header; the evaluator; no chained or conditional scripts on interactive pages.

### Task 5 (PR 5): Browser tests, no-JS walkthrough, measurements, cleanup

Files: `characters/tests/browser/test_chargen_interactive.py`,
`characters/tests/views/test_chargen_nojs_walkthrough.py`; deletion of the
point-pool stack and its tests; updates to Step 9 asset tests.

- [ ] Playwright: dots, pool, conditional and options, validator abort and stale guard, full 13-step walkthrough with request counting.
- [ ] No-JS walkthrough through the test client.
- [ ] Delete `point_pool.{py,js}`, the point-pool mixins, `AttributeForm`, `AbilityForm`, `SphereForm`, `form_pool.html` and their tests; update `widgets/__init__.py`.
- [ ] Record the metrics and go/no-go evidence below.

## Suggested PR order

1 → 2 → 3 → 4 → 5, as above. PR 2 is usable alone (fragment step swaps);
PR 3 and PR 4 are independent of each other after PR 2. Rollout PRs per
gameline follow the spec's order, each setting `interactive=True` and
converting that gameline's step fragments.

## Execution record

(Filled in during implementation.)
