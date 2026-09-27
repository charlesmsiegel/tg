# Interactive character creation with htmx and Alpine.js (Vampire pilot)

## Intent and scope

Step 10 gives character creation the goals a React rewrite would have had
(step changes without reloads, live server validation and running totals,
instant dot feedback, conditional fields, dependent selects) without React,
Vite, npm or a build step. The game rules stay in Python: forms, services and
`characters/rules/` (Step 4) decide; browser code only hints. The user asked
for the plan to be implemented, which supersedes the brief's design-only
restriction, as in Steps 2, 3, 4 and 9. The pilot gameline is **Vampire**
(13 steps). Scene chat (Step 11) and non-chargen pages are out of scope;
Step 5's detail-page actions may later reuse the fragment helpers in
`core/htmx.py`, but this design does not cover them.

## Upstream designs this builds on

All five upstream designs exist and are implemented on `main`:

| Step | What this design reuses |
|---|---|
| 0 Authorization | `authorize_route` with the `CHARGEN_STEP` policy, applied by the middleware, by `DictView` and again by `ChargenStepMixin.dispatch`; the `/__chained_select__/` allowlist (registered forms and parents, `user` supplied from the request). |
| 2 Step registry | `characters/chargen/`: `Workflow`, `Step.template` fragments that have no outer `<form>`, `advance()`, `previous_position()`, and `workflow.progress()` for the progress bar. |
| 3 Shared steps | The shared step bases (`CharacterFormStepView`, `CharacterExtrasView`, `GenericBackgroundView`, `FreebieSpendingView`), so one mixin change covers all 13 Vampire steps. |
| 4 Rules out of views | `AllocationRule`/`PriorityRule` with `client_data()`, `AllocationStepMixin.get_allocation_rules()`, `BackgroundRatingFormSet(enforce_allocation=True)`, and costs in `characters/costs.py`. |
| 9 Static JS | Every script is a static file; widgets declare `forms.Media`; configuration travels as `data-*` or `json_script`; widget managers already re-initialise on `htmx:afterSwap` and have double-load guards. |

## Audit status of the brief's findings

Each **Reported** item was re-checked on this branch (after Steps 0-9):

| Finding | Status |
|---|---|
| Each step is a full page load at `/characters/<pk>/`, routed by type and then by `creation_status` | **Confirmed.** Every step posts back to the same URL; the router re-dispatches on the saved position. |
| `POINT_POOL_JS` is a 442-line Python string | **Confirmed, moved by Step 9** to `widgets/static/widgets/point_pool.js` (442 lines). **New finding:** no production view uses it. Only the unused `AttributeForm`, `AbilityForm` and `SphereForm` load it. |
| `attribute_block/form.html` has a 232-line inline validator | **Confirmed, moved** to `characters/js/attribute-validation.js` (231 lines). It changes the inputs' `max` and disables `<option>`s, which is a second copy of `PriorityRule`. |
| `ability_block/validation.html` (84 lines) | **Confirmed, moved** (84 lines). It disables Save until the client thinks the totals match. |
| `background_block/form.html` (83 lines) | **Confirmed, moved** (80 lines). It needs a map of every background's multiplier sent to the client. |
| `conditional_js` in 14 templates | **Confirmed** (14). **New finding:** Vampire's chargen freebies step renders the generic `form.as_p` (the Step 2 fragment), which has no `<field>_wrap` wrappers and no `conditional_js`, so its visibility rules do nothing and all five fields always show. |
| Chained selects embed the whole choice tree | **Confirmed.** The Vampire freebies form ships every Attribute, Ability, Background, Merit/Flaw, Discipline and Virtue option, plus merit/flaw ratings, as JSON. |
| Global `TG.validation` in `core/form.html` | **Confirmed, moved** to `core/js/validation.js` (43 lines). |
| Unused `AttributeForm` / `form_pool.html` | **Confirmed unused.** Evaluated below. |
| 12 unreferenced AJAX endpoints | **Refuted as current:** Step 1 already removed them. |
| `/__chained_select__/` is an allowlist | **Confirmed.** Only `MageCreationForm` (`faction`, `subfaction`) is registered. |
| Back navigation and progress | **Confirmed.** `ChargenBackView` handles Back (POST, owner only, row-locked). The registry's `workflow.progress()` feeds the progress bar through `ChargenStepMixin`; `ChargenProgressMixin` survives only for the Human wrappers. |
| Vampire has 13 steps and its templates have drift | **Confirmed.** The Disciplines and Virtues fragments hard-code "3" and "7" instead of reading the rule. Both repeat `{% csrf_token %}` inside the outer form. The virtue script hard-codes `TARGET = 7`. The cost table in the old `freebies_form.html` hard-codes costs, and the chargen step shows none. |

## Decisions

| Question | Decision | Why |
|---|---|---|
| Pilot gameline | Vampire | It has the most step kinds among the simpler gamelines: priority allocation, two rule-backed allocations, a formset, chained freebies, languages, linked-NPC backgrounds and a terminal step. Every step view is a Step 3 shared base, so the pilot exercises code that all gamelines share. |
| How a gameline opts in | `Workflow.interactive` (registry flag, set with `bind(..., interactive=True)`) | Step 2 owns per-workflow metadata. One flag switches all steps of a gameline at once, with no per-view attributes to forget. Other gamelines render exactly as before. |
| htmx version | 2.0.11, vendored | 4.x is still `next`. |
| Alpine build | **CSP build** `@alpinejs/csp` 3.17.4 | The standard build compiles attribute expressions with `new Function`, which needs `'unsafe-eval'` and would add a CSP blocker right after Step 9 removed most of the inline scripts. In the 3.17 CSP build, expressions are parsed without eval (property access, comparisons, method calls with arguments) but may not reach globals. That forces every component into `Alpine.data()` in a static file, which is also where we want them for review and tests. Cost: no `x-html` and no inline arrow functions, neither of which we need. |
| `django-htmx` | **Not added** | We need four things: detect `HX-Request`, detect history-restore requests, set `HX-Redirect`, and add `Vary`. That is about 40 lines in `core/htmx.py` and needs no middleware or new dependency. Revisit for Step 11 if it needs `HX-Trigger-After-*` or boosted-request handling. |
| Where fragments come from | The **same step URL** (`/characters/<pk>/`) through the existing router | Authorization, routing and step choice are reused unchanged, and a fragment can never render a step the router would not render. |
| Conditional fields | **Server-evaluated** visibility (Python evaluator over the existing `conditional_fields` declarations), applied client-side by a small Alpine component | Every visibility change in the pilot happens when a chained parent changes, and that already needs a server round trip for options. Running the rule interpreter in Python keeps the rules in Python and gives the no-JS render correct visibility. The JS interpreter (`conditional.js`) is not loaded on interactive pages. |
| Running totals | Alpine sums visible inputs instantly (hint). The server computes authoritative totals and messages (validate-only mode). | A plain sum of visible inputs is arithmetic, not a rule. Anything that needs lookups (background multipliers, freebie costs) or judgement (the distribution check) comes from the server. |

## 1. Request/response contract

All of this applies only when `workflow.interactive` is true.

**Detection.** `core.htmx.is_fragment_request(request)` is true when `HX-Request: true` is present and neither `HX-History-Restore-Request` nor `HX-Boosted` is. A history-restore request must get a full page.

**Full page (no header).** Same URL and the same step view. The gameline shell (`characters/vampire/vampire/chargen.html`, which only extends the core shell) renders `characters/core/chargen/interactive.html`:

```
div#chargen-root  [hx-headers CSRF]
  header card (character name)
  div#chargen-progress              <- progress bar
  form#chargen-step  method=post action=<path>  hx-post=<path>
       hx-target=this  hx-swap=outerHTML  hx-push-url=false
       hx-disabled-elt="find button[type=submit]"  data-step=<key>
    csrf, non-field errors, h2#chargen-step-heading[tabindex=-1]
    {% include step.template %}          <- Step 2 fragment, unchanged contract
    div#chargen-feedback [role=status aria-live=polite]
    div#chargen-validator [hidden, hx-post ... see §2]
    buttons: Save (submit) | Back (formaction + hx-post=back_url) | Cancel (link)
    {% page_media %}                      <- this step's widget scripts
```

Without JavaScript the `hx-*` attributes do nothing. The form posts normally, the step view redirects, and the router renders the next step: today's behaviour.

**Fragment (`HX-Request`).** The same view renders `characters/core/chargen/step_fragment.html`, which contains:
- the new `form#chargen-step`, swapped over the old one (`outerHTML`);
- `div#chargen-progress` with `hx-swap-oob="true"`;
- `div#tg-messages` with `hx-swap-oob="true"`, which drains queued Django messages so they do not surface later on a full page.

Headers on every chargen response are `Vary: HX-Request, HX-History-Restore-Request, HX-Boosted` (every header `is_fragment_request()` reads, so a cache never serves a fragment where a full page is due) and `TG-Fragment: chargen-step` on fragments. Fragment responses have status 200, including forms with validation errors: htmx swaps 2xx only, and a bound form with errors is a normal render.

**Advancing.** Step views keep their Post/Redirect/Get lifecycle. A successful POST returns `302 /characters/<pk>/`. The browser follows it inside the same XHR and keeps the `HX-Request` header (same-origin redirect), so the redirected GET returns the next step's fragment. The pilot's browser tests check this header behaviour. The redirect keeps routing and authorization for the next step in one place, the router.

**Leaving the wizard.** If a fragment request's response is a redirect anywhere other than the wizard URL (the terminal Specialties step submits the character and redirects to its detail page), `ChargenStepMixin` turns it into `200` with `HX-Redirect: <location>`, and htmx does a full navigation. If the router receives a fragment request for a character that is no longer in the wizard, it answers `HX-Redirect` to the same URL instead of rendering the detail page into the form.

**Swap guard.** `chargen.js` swaps a response into `#chargen-step` only if it carries the expected `TG-Fragment` value. Any other response navigates the page to `xhr.responseURL`. That covers an expired session (a public or login page), a 403/404/500, or an unexpected full page, so no page is ever nested inside the form. For validate-only and options requests, the guard drops the response instead.

**`hx-push-url`.** Every step lives at the same URL, so pushing history would only add identical entries. It is `false`. Browser Back leaves the wizard, as it effectively does today; the wizard's own Back button is the way to go back a step.

**Back.** The Back button keeps `formaction` and `formnovalidate` for no-JS use, and gains `hx-post="{{ back_url }}"` with the same target and swap. htmx cancels the native submit of a submit button that has its own `hx-post`. `ChargenBackView` is unchanged: it redirects to the wizard URL, the redirect is followed, and the previous step's fragment arrives with an OOB progress bar and any "cannot go back" warning in the OOB messages.

**Errors.** A 4xx/5xx step response is not swapped; the guard navigates to the URL so the server renders its own error page. `hx-disabled-elt` disables the submit buttons while a request is in flight, so a second click can no longer queue a duplicate POST.

**Focus.** After a step swap, `chargen.js` moves focus to the error summary if the new form has errors, and otherwise to `#chargen-step-heading`. Validate-only swaps never move focus. `#chargen-feedback`, the pool totals and `#tg-messages` are `aria-live="polite"` regions.

## 2. Live validation without duplicated rules

**Endpoint.** It is the same step URL, `POST` with `_validate=1`, and only for fragment requests. `ChargenStepMixin` handles it in `dispatch`, **after** authorization and **before** any skip or advance logic, so a validate POST can never advance a skippable step. A validate POST on an unavailable step (skip, or freebies awaiting approval) returns `204`.

**What runs.** The view's own `get_form()` with the posted data, then `form.is_valid()`. That runs exactly the Step 4 checks: `AllocationFormMixin.clean()` with `get_allocation_rules()`, `BackgroundRatingFormSet.clean()` with `background_violations()`, and the chained-consistency and category checks in the freebies form. `form_valid()` is never called, so no service runs and nothing is saved. `ModelForm._post_clean` only mutates the in-memory instance. The response renders `characters/core/chargen/feedback.html` with `TG-Fragment: chargen-feedback`:
- the first error message in the step's own wording, or "Ready to save";
- **totals**, from a new pure method `status(values)` on `AllocationRule` and `PriorityRule` (current total, target or targets, and whether the total is satisfied) and from `BackgroundRatingFormSet.allocation_status()` (the weighted cost of the rows against the budget, using the same multiplier arithmetic its `clean()` uses);
- for freebies, the character's remaining freebies. After `is_valid()` the step also runs its own side-effect-free submit checks (`validate_submission()`; for freebies, `get_spending_kwargs()`, so "Discipline with no trait" is reported exactly as the submit reports it). Because the spending service itself still runs only on submit, the freebies step never says "Ready to save": a clean form reads "No problems found so far". A per-selection cost preview needs a side-effect-free `quote()` on the spending services, whose handlers compute cost and write in one method today. That split belongs to Step 4's services and is a follow-up. Running it inside a rolled-back transaction was rejected: signals and caches would still see the writes.

**Triggering.** `div#chargen-validator` carries:

```
hx-post=<path> hx-vals='{"_validate": "1"}' hx-include="closest form"
hx-trigger="change from:closest form delay:250ms, input from:closest form delay:600ms"
hx-target="#chargen-feedback" hx-swap="innerHTML" hx-sync="this:replace"
```

`delay:` debounces typing, `replace` aborts an in-flight validation when a newer one starts, `load` paints the first totals, and `hx-disabled-elt="unset"` keeps Save enabled during validation. A validation still in flight when the step is saved is **not** aborted: htmx logs every abort as a console error, and aborting is unnecessary. htmx resolves a request's target when the request starts, so the response can only land in the detached old `#chargen-feedback`; htmx never starts a delayed request from an element that has left the page; and the swap guard also drops any feedback whose `TG-Step` header no longer matches the form on screen. A browser test holds a validation response until after the step swap to prove it.

**Rate limiting.** Debounce plus `replace` gives at most one validation request in flight per page. On top of that, a per-user, per-character cache counter shared by validate and options requests (setting `CHARGEN_PARTIAL_LIMIT`, default 60 per minute) answers `204` when exceeded, and htmx ignores a 204. This protects against a runaway client loop, not a determined attacker (who could just POST the real form), so it degrades silently.

## 3. Alpine components

`characters/static/characters/js/chargen-components.js` registers three components on `alpine:init`. It loads before the Alpine CSP build, and both are `defer`. Alpine's mutation observer initialises components in swapped-in fragments and in formset rows cloned later.

**`tgDots`** replaces click-to-set dot feedback. It is rendered by `widgets.widgets.dots.DotRatingInput` (template `widgets/dot_rating.html`):

```html
<span class="tg-dots-control" x-data="tgDots" data-min="1" data-max="5">
  <input type="number" name="strength" id="id_strength" value="3" min="1" max="5"
         x-ref="input" @input="sync" class="tg-dots-number">
  <span class="tg-dot-buttons" role="group" aria-label="Strength">
    <button type="button" class="tg-dot" data-value="1" @click="pick"
            :aria-pressed="..." aria-label="Strength 1">...</button> ... (min..max)
  </span>
</span>
```

- **API:** `data-min`/`data-max` come from the server. `pick(event)` sets the input to the clicked value; clicking the current top dot lowers it by one, clamped to `min`. It then dispatches bubbling `input` and `change` events, which drive `tgPool` and the validator. `sync()` reflects typed values back onto the dots.
- **No-JS:** the number input stays the real form control. The buttons are hidden until Alpine initialises (`[x-cloak]`), and the number input is hidden when Alpine is present.
- **Wiring:** `ChargenStepMixin.get_form()` on an interactive workflow swaps the `NumberInput` of every field named by the step's allocation rules for a `DotRatingInput`. `min`/`max` come from `rule.client_data()`, so bounds are server data, not literals.

**`tgPool`** replaces the counters in `attribute-validation.js`, `ability-validation.js` and `vampire-virtues.js` on interactive pages:

```html
<div x-data="tgPool" data-pool-rules="pool-rules-attributes" aria-live="polite">
  <span x-text="summary"></span>
</div>
{{ allocation_rules|json_script:"pool-rules-attributes" }}
```

- **API:** it reads `client_data()` of the step's rules from `json_script`. `AllocationRule.client_data()` now also lists its `fields`; `PriorityRule.client_data()` its `groups`. It listens to `input` and `change` on its form and exposes `summary` (for example "Physical 8 · Social 6 · Mental 5 (need 10/8/6)"). The rule-dependent parts (primary, secondary and tertiary targets; the maximum per trait) are data from the server; the component only adds up visible inputs.
- **Hints only:** it never disables Save, changes `max`, or blocks input. The server's validate response is the verdict. This removes the client checks that disagreed with the server: the ability script's Save-disable and the attribute script's dynamic `max`.

**`tgConditional`** replaces `conditional_js` and `conditional.js` for chained freebies forms:

```html
<div x-data="tgConditional" data-visibility='{"example": false, "value": false, ...}'
     @tg-visibility.window="apply">
  <div id="example_wrap" :hidden="!shown.example" hidden>{{ form.example }}</div> ...
```

- **API:** `shown` is initialised from server-rendered `data-visibility` and updated by `apply(event)` from the `tg-visibility` event. The server sends that event with each options response through `HX-Trigger`.
- **Python evaluator:** `ConditionalFieldsMixin.field_visibility(values)` implements the exact semantics of `conditional.js` (`visible_when`: all conditions must hold; `hidden_when`: any condition hides; `value_is`/`in`/`not_in`, `checked_is`, `metadata_is`, `metadata_truthy`, `_context`). It reads option metadata from the chained field's `choices_map`. The same evaluator sets the `hidden` attributes on full renders, so a no-JS bound form shows the right fields.

**What each replaces on Vampire pages:**

| Script | Lines | Interactive pages use instead | Other gamelines |
|---|---|---|---|
| `attribute-validation.js` | 231 | `tgDots` + `tgPool` + validator | unchanged until rollout |
| `ability-validation.js` | 84 | `tgDots` + `tgPool` + validator | unchanged until rollout |
| `background-validation.js` + multiplier map | 80 | server totals from the validator | unchanged until rollout |
| `vampire-virtues.js` | 52 | `tgDots` + `tgPool` + validator | **deleted** (Vampire only) |
| `core/js/validation.js` | 43 | not loaded (interactive shell omits it) | unchanged until rollout |
| `chained.js` + embedded tree | 215 | options fragments (§4) | unchanged until rollout |
| `conditional.js` + `conditional_js` | 190 | `tgConditional` + Python evaluator | unchanged until rollout |
| `point_pool.js` + widget, mixin, three forms, `form_pool.html` | 442 JS + about 700 Python | ideas reused in `tgPool` | **deleted** (unused everywhere) |

**Evaluation of the unused point-pool alternative.** Reused ideas: pool configuration supplied by Python rather than written in the template, declarative status elements, and one component for any "sum these fields against targets" step. Rejected: its Python side (`distribution_targets`, `with_targets()`) is a second copy of `PriorityRule` that has already drifted (it has no ability maximum of 3), and its JS enforces constraints by changing `max` and disabling options. Nothing in the app loads it, and Step 1 left its deletion to this step, so it is deleted.

## 4. Chained selects via `hx-get`

**Character-scoped forms** (all freebies forms take `instance=character`) do **not** go through the global endpoint. The global endpoint authenticates but has no object to authorize, and registering a form there would need a new rule for which character a request may name. Instead the child select's options come from the **step URL itself**:

```
GET /characters/<pk>/?_options=example&category=Discipline      (HX-Request)
```

- **Authorization:** the router and `ChargenStepMixin` apply `CHARGEN_STEP` as for any step request. The view builds its own form with its usual kwargs (`instance`, `user`, and so on), so no kwargs are rebuilt from client data.
- **Allowed fields:** `_options` must name a `ChainedChoiceField` of that form that has a parent; anything else gets `400`.
- **Response:** `characters/core/chargen/options.html` returns the `<option>` elements from `field.get_choices_for_parent(parent)` (the same method `ChainedSelectMixin.clean()` validates against) and an OOB reset of each grandchild select. Visibility from `field_visibility()` travels in `HX-Trigger-After-Swap: {"tg-visibility": {...}}`, which htmx fires only once the options were actually swapped in. Plain `HX-Trigger` would fire even for a dropped answer. The headers are `TG-Fragment: chargen-options` and `TG-Chain`, which holds the ancestor values the answer was computed for.
- **Stale answers:** each select only replaces its own earlier requests, so an old `example` answer can arrive after a newer `category` change. `chargen.js` drops any options answer whose `TG-Chain` no longer matches the selects on screen.
- **Widget:** `HtmxChainedSelect` renders `hx-get=<path>`, `hx-vals='{"_options": "<child>"}'`, `hx-include` limited to the chain's own selects (never the CSRF token), `hx-target="#id_<child>"` and `hx-swap="innerHTML"`. It emits no embedded tree and declares no `chained.js` media.
- **No-JS:** the category select posts with the form. An incomplete choice fails `clean()` ("Must Choose Trait"), and the bound re-render fills `example` through the existing `_populate_initial_choices`, with visibility computed from the bound data. It takes one extra round trip without JS; today it does not work at all without JS.

**User-scoped forms** (`MageCreationForm`, which needs `user`) keep the Step 0 allowlisted endpoint. It gains an `<option>` fragment response when `HX-Request` is present, rendering the same `options.html`, while JSON stays for existing callers. The registry factory already builds the form from `request.user`. That change ships with the Mage rollout, which is its first consumer; the pilot does not add dead code for it.

## 5. Cross-cutting concerns

- **CSRF.** Forms keep `{% csrf_token %}`. `#chargen-root` also carries `hx-headers='{"X-CSRFToken": "…"}'`, so a request that does not include the form still passes `CsrfViewMiddleware`. Options requests are GETs and never include the token in the query string.
- **Authorization.** There are no new URLs. Every fragment, validate and options request passes the middleware, `DictView` (`VIEW_FULL`, then `EDIT_FULL` for Un/Rev characters) and `ChargenStepMixin` (`CHARGEN_STEP`). Nothing is "hidden because not rendered". Tests cover anonymous users, other players and submitted characters on every mode.
- **Vendoring, pinning and SRI.** The files live at `source_static/vendor/htmx/2.0.11/htmx.min.js` and `source_static/vendor/alpinejs-csp/3.17.4/cdn.min.js`, and the version is part of the path. `source_static/vendor/VENDOR.md` records the npm tarball `sha512` (checked against the registry when vendoring), the `sha384` SRI hash and the license. `core/includes/interactive_scripts.html` emits the `integrity` attributes. A test recomputes each file's SRI hash and compares it with the include, so an edited vendor file fails CI. Neither file contains `sourceMappingURL`, so `ManifestStaticFilesStorage` does not rewrite them and SRI stays valid on hashed URLs.
- **htmx configuration** (`<meta name="htmx-config">`): `allowEval: false`, `includeIndicatorStyles: false` (no injected `<style>`, which is CSP-friendly), `selfRequestsOnly: true`, `historyCacheSize: 0`. `allowScriptTags` stays true so a step's widget `<script src>` tags in a fragment load. Their managers already guard against double loading and re-initialise on `htmx:afterSwap` (Step 9).
- **CSP readiness.** This design adds no inline scripts, `hx-on` handlers, eval or injected styles, so it introduces no CSP blocker. Adding the CSP header itself stays out of scope (Step 9 lists the remaining blockers).
- **Accessibility.** See focus and live regions in §1. Dot buttons are real `<button>`s with `aria-pressed` and labels, and the number input stays in the accessibility tree without JS.

## 6. Tests

- **Django client (no browser):** full page versus fragment for every pilot step shape; `Vary` and `TG-Fragment` headers; OOB progress and messages; history-restore requests get a full page; the terminal step returns `HX-Redirect`; the router answers `HX-Redirect` for characters outside the wizard; Back through htmx; validate-only returns totals and errors with **zero INSERT/UPDATE/DELETE** (`CaptureQueriesContext`) and the row unchanged; validate on a skippable step does not advance; throttling returns 204; the options endpoint returns filtered `<option>`s and `HX-Trigger` visibility, and rejects unknown or root fields; every mode is denied to anonymous users, other players and submitted characters; non-pilot gamelines render unchanged (no htmx attributes); `field_visibility` matches `conditional.js` case by case; `status()` on the rules; SRI hashes.
- **Playwright** (Chromium from `/opt/pw-browsers`, skipped when Playwright or Chromium is missing): `tgDots` clicking, clamping and syncing typed values; `tgPool` totals; `tgConditional` plus chained options; the validator's server verdict; a validation held in flight across a step swap; an expired session loading as a full page; parity between `conditional.js` and the Python evaluator on the same inputs; and a **full 13-step Vampire walkthrough** that counts document loads and XHRs and fails on any console error from application code.
- **No-JS walkthrough:** the same 13 steps through the Django test client, posting forms exactly as a browser without scripts would (no `HX-Request`), including the two-round-trip chained freebies path.

## 7. Pilot success criteria and rollout

**Measured in the pilot and recorded in the plan's execution record:** lines of application JS no longer loaded on Vampire chargen pages, lines deleted and lines added; document loads and total requests for a full walkthrough, before and after; correctness bugs fixed (the drift listed above, conditional fields dead on the chargen freebies step, and client checks disagreeing with the server).

**Go/no-go for other gamelines (all must hold):**
1. All existing chargen tests and the new contract tests pass, and a non-interactive gameline's output is unchanged.
2. The no-JS walkthrough passes for the pilot.
3. The Playwright walkthrough passes with exactly one full page load, and the only errors in the browser console are expected 4xx probes.
4. There are no client-side rule copies on interactive pages: `tgPool` and `tgDots` read only server data, and the validator agrees with the submit verdict in tests.
5. There is no regression in authorization tests, and validate-only proves it makes no writes.
6. One week in production with no fragment-guard navigations logged beyond expected session expiry. This is observed by the owner and cannot be checked from the repository.

**Rollout order**, each a small PR that sets `interactive=True` and converts that gameline's step fragments:

1. **Ghoul and VtM Human.** They share Vampire's freebies form family and ability template.
2. **Human core wrappers.**
3. **Werewolf** (Garou, Kinfolk, WtA Human; then Fomor and Drone). This adds Gifts and the Kinfolk tribe background limits, which are already server rules.
4. **Wraith** (Arcanoi rule, Passions and Fetters formsets).
5. **Changeling** (Arts and Realms rules).
6. **Demon** (Lores, Apocalyptic Form).
7. **Fera.** There are 12 types on one workflow, and the breed declarations need a check.
8. **Mage, Companion and Sorcerer** last. They have the most bespoke formsets and services (rotes, spheres with Arete purchase, and numina), and they are the first consumer of the Step 0 endpoint's `<option>` fragments.

When the last gameline is converted, delete `attribute-validation.js`, `ability-validation.js`, `background-validation.js`, `core/js/validation.js`, `chained.js`'s embedded-tree mode and `conditional.js` for chargen, then remove the `interactive` flag.

## 8. Where htmx and Alpine would be the wrong tool

- **Highly stateful client editors** with many interdependent local edits before a save, such as a drag-and-drop relationship map, a dice-pool builder with undo, or offline editing. Server round trips per edit would feel slow, and Alpine components would grow into an unmanaged SPA.
- **Real-time multi-user streams** such as scene chat. A WebSocket stream (Step 11, Channels) is a different transport; htmx's SSE and WebSocket extensions can render server HTML there, but ordering, presence and reconnection are not request/response problems.
- **Rules that must run offline or at keystroke frequency.** If a rule really must run in the browser, it needs a single shared definition (for example JSON rule data interpreted in both places). Alpine components must never carry rule logic.
- **Large client-side data grids** (sorting and filtering thousands of rows). Server-side pagination or filtering through htmx is fine; client-side virtual grids are not what htmx or Alpine are for.
- **Cross-origin or third-party embeds.** `selfRequestsOnly` is deliberate.

## Implementation record and findings

Implemented as specified, with these deviations and discoveries:

- **No abort on submit** (see §2). The abort was designed in, then removed after the browser run showed htmx logging each abort as a console error. The detached-target property and the step guard already cover the race, and a browser test pins that.
- **Chains follow `parent_field` links.** `ChainedSelectMixin.chain_for()` walks parents, so a plain `ChoiceField` root works. That is required because of the next finding.
- **Confirmed defect, fixed for Vampire:** `ChainedHumanFreebiesForm.category` is a plain `ChoiceField`, so the legacy mixin never builds a chain and never embeds a tree. `choices_map` is also assigned after chain setup, so bound re-renders never refill `example`. In real Chromium, the non-interactive Ghoul freebies step leaves "Trait" with only the empty option after choosing a category, and every conditional field stays visible. The same form family serves ten other chargen freebie views (Ghoul, VtM Human, MtA Human, Mage, Changeling, CtD Human, WtA Human, Fera, Fomor, WtO Human); they stay broken until their rollout PR, which fixes them the same way. This raises the priority of the rollout order in §7.
- **Confirmed defect, fixed:** once `example` options are filled on a bound form, their 3-tuple metadata crashed `Select` rendering (`too many values to unpack`). The widget now receives `(value, label)` pairs and the metadata stays in `choices_map` for the visibility rules.
- **Confirmed, worked around, not changed:** `VampireCharacterCreationView.default_redirect` is a bare `DetailView` with no access policy, so an owner who GETs `/characters/<pk>/` for a submitted Vampire gets 403. The fragment guard therefore sends `HX-Redirect` to `get_absolute_url()` rather than the router URL. Fixing the router fallback belongs to Step 0/7 ownership.
- **Preserved for the owner:** `out_of_clan_discipline` has no freebie cost (`get_freebie_cost` returns 10000), so the freebies form offers every Discipline but the service refuses non-clan ones for lack of freebies. The cost table shows only what the cost source defines.
- **Review fixes (Codex review of `aa0ad2a`):** the vary list now covers every header that selects the fragment; freebies feedback runs the submit's choice resolution and no longer claims "Ready to save" before the spending service has run; stale chained-options answers are dropped by `TG-Chain`, and their visibility is sent only after a swap. A browser test holds an answer across a category change, and it fails without the fix.
- **Review fixes (Codex review of `2a347f2`):** on a fresh page a chain's children start from the option the root select actually shows (its first choice), as `current_values()` already assumed, so the freebies Trait select offers the Attributes before any category change. An accepted options swap resets descendant selects without an `input` or `change` event, so `chargen.js` fires `tg-options-swapped` and the validator re-runs; a validation that raced a slow options answer no longer leaves its stale "Invalid selection" error on screen. Each fix has a test that fails without it.
- **Review follow-ups (Claude review of `2a347f2`):** rule and group labels now come from the server in `client_data()`, so the live hint and the feedback fragment cannot title-case a name differently; `_chain_value()` no longer treats a falsy initial value such as `0` as unselected.
- **Noted:** building the freebies form lazily creates `ObjectType` rows (`get_or_create`) on any render. Validate-only adds no writes of its own; the test warms the form first. `core/form.html` renders `object.name|safe` in the title and heading; the interactive shell autoescapes the name, and the shared template is left to its owner. Adding a second background row without JS has always needed the formset Add button.
- **Deleted:** `vampire-virtues.js` and the whole unused point-pool stack (widget, mixins, `point_pool.js`, `AttributeForm`, `AbilityForm`, `SphereForm`, `form_pool.html` and their tests: 2,383 lines, 442 of them JS).

## Theory

A chargen step is a server-rendered form at one URL. Interactivity is a
transport choice (a whole page or the step's fragment), not a second
implementation. The server decides the step, the verdict, the totals, the
visible fields and the options; the browser only makes those decisions
instant or incremental. A gameline opts in with one registry flag. The seams
to watch are redirects followed inside XHR, script loading in fragments, and
stale asynchronous responses, and each has an explicit guard and a test.
