# Character creation (chargen)

This page explains how a player builds a character step by step: the workflow registry
that orders the steps, how a request reaches the right step view, the allocation rules that
check Attributes and Abilities, the freebie stage, the htmx-driven interactive workflow and
its no-JavaScript fallback, and how the finished character is submitted for approval. It is
for developers changing chargen and for agents adding or editing a step. For the step-by-step
recipe of adding a step, see [Adding a chargen step](../guides/adding-a-chargen-step.md).

Terms such as Attributes, Abilities, freebies and ST are defined in the
[glossary](../reference/glossary.md).

## The moving parts

| Piece | Source | Responsibility |
|-------|--------|----------------|
| Workflow types | [`characters/chargen/workflow.py`](../../characters/chargen/workflow.py) | `Step` and `Workflow` dataclasses; imports nothing from the project |
| Workflow registry | [`characters/chargen/registry.py`](../../characters/chargen/registry.py) | Step-list rows, the `WorkflowViews` and `FreebiePosition` descriptors (re-exports `Step` and `Workflow`) |
| Workflow definitions | [`characters/chargen/definitions.py`](../../characters/chargen/definitions.py) | Shared `Step` constants and one `Workflow` per character `type` in `WORKFLOWS` |
| Skip predicates | [`characters/chargen/predicates.py`](../../characters/chargen/predicates.py) | Read-only checks that decide whether a step applies |
| Transitions | [`characters/chargen/transitions.py`](../../characters/chargen/transitions.py) | `advance()` (the only forward move) and `previous_position()` |
| Router | [`characters/views/core/human.py`](../../characters/views/core/human.py) `HumanCharacterCreationView`, [`core/views/generic.py`](../../core/views/generic.py) `DictView` | Dispatches `/characters/<pk>/` to the step view for `creation_status` |
| Step mixins | [`characters/views/core/chargen_mixins.py`](../../characters/views/core/chargen_mixins.py) | `ChargenStepMixin` (authorization, skip/wait handling, htmx partials, rendering), `ChargenProgressMixin` |
| Allocation steps | [`characters/views/core/allocations.py`](../../characters/views/core/allocations.py) | `AllocationStepMixin`, `PointAllocationView` |
| Allocation rules | [`characters/rules/allocation.py`](../../characters/rules/allocation.py), [`characters/rules/limits.py`](../../characters/rules/limits.py) | Pure `AllocationRule` / `PriorityRule` objects and the point pools per gameline |
| Allocation forms | [`characters/forms/core/allocation.py`](../../characters/forms/core/allocation.py) | `AllocationFormMixin` runs the rules in `clean()`; helpers for running totals and the PRI / SEC / TER picker |
| Freebie step | [`characters/views/core/spending.py`](../../characters/views/core/spending.py) `FreebieSpendingView` | Spends freebies through the freebie spending service |
| Back button | [`characters/views/core/chargen_back.py`](../../characters/views/core/chargen_back.py) `ChargenBackView` | Moves one applicable step back |
| Templates | [`characters/templates/characters/core/chargen.html`](../../characters/templates/characters/core/chargen.html) and [`characters/templates/characters/core/chargen/`](../../characters/templates/characters/core/chargen/) | Page shell, step body, step list, htmx fragments |

## Workflows and steps

A `Step` is a frozen dataclass with:

- `key`: a unique name within the workflow (`"attributes"`, `"freebies"`, ...).
- `label`: the text shown in the step list.
- `view_path`: dotted path of the view class, imported lazily through `Step.view`.
- `template`: the step body included inside the shared chargen page (default
  `characters/core/chargen/form.html`).
- `skip_if`: an optional predicate `(character) -> bool`; `Step.should_skip()` calls it.
- `group`: consecutive steps with the same group share one row in the step list. Every
  background-gated step uses `group="background"`.

A `Workflow` is an ordered tuple of steps plus an `interactive` flag. Its constructor raises
`ValueError` unless every key is unique and exactly one step has the key `"freebies"`.
`Workflow.freebie_step` is the 1-based position of that step, `Workflow.view_mapping` maps
positions to view classes, and `Workflow.progress(position)` returns one dict per step
(`key`, `label`, `status` of `completed` / `current` / `pending`, `conditional`, `group`).
`progress_rows()` folds consecutive grouped steps into single rows for the template.

`characters.chargen.get_workflow(character_type)` looks a workflow up in `WORKFLOWS`. It
imports the definitions lazily so it is safe to call while models load.

### Positions, not ids

`Character.creation_status` (an `IntegerField`, default `1`) stores the **1-based position**
of the current step in the character's workflow. The number identifies an ordered task, not
a view. Changing which view or template renders a step is safe; inserting, removing or
reordering steps shifts the meaning of every saved position, so unfinished characters then
need a data migration (the registry module docstring states this rule).

### Definitions

[`definitions.py`](../../characters/chargen/definitions.py) declares shared steps once
(`ATTRIBUTE`, `ABILITY`, `BACKGROUNDS`, `EXTRAS` labelled "Biography", `FREEBIES`,
`LANGUAGES`, `SPECIALTIES`, the background-gated `ALLIES`, `MENTOR`, `NODE`, ... and the
gameline power steps) and composes them. `bind(tasks, module, prefix, templates=, views=,
interactive=)` turns shared steps into a gameline workflow: each step's view becomes
`<module>.<prefix><view_path>View` unless `views` overrides it, and `templates` overrides
step templates by key. Common prefixes:

- `STATS = (ATTRIBUTE, ABILITY, BACKGROUNDS)`
- `MORTAL = STATS + (EXTRAS, FREEBIES, LANGUAGES)`
- `MAGE_BACKGROUNDS`: the Mage background-detail steps plus `SPECIALTIES`

Some character types have detail pages but no creation workflow (`autumn_person`,
`inanimae`, `nunnehi`, `earthbound`, `htr_human`, `hunter`, `mtr_human`, `mummy`,
`revenant`). `DETAIL_ONLY_FREEBIE_POSITIONS` gives them a freebie position so the
`freebie_step` class attribute (a `FreebiePosition` descriptor) still answers for them.

### Skip predicates

Predicates in [`predicates.py`](../../characters/chargen/predicates.py) never write, so a
GET can evaluate them:

| Predicate | Skips the step when |
|-----------|---------------------|
| `exhausted_freebies` | freebies are approved and none remain |
| `no_languages` | the character has no "Language" merit |
| `background(name)` | the character has no incomplete `BackgroundRating` for that background (`complete=False`) |
| `hedge_mage` / `psychic` | the Sorcerer is (or is not) a hedge mage |
| `no_rotes` | `rote_points == 0` |
| `completed_passions` / `completed_fetters` | the Wraith already has passions / fetters |

When the languages step is skipped, `transitions._skip_effect` adds English to the
character's languages, the same default the languages form applies.

## From URL to step view

Every character's canonical URL is `characters:character` (`/characters/<pk>/`,
`Character.get_absolute_url`). The request passes through two `DictView` routers:

```text
/characters/<pk>/
  GenericCharacterDetailView      key: character.type   (characters/views/core/__init__.py)
    -> e.g. HumanCharacterCreationView   key: creation_status, chargen_router = True
         -> workflow.view_mapping[creation_status]   (the step view)
         or default_redirect (the detail view) when the key is not a live step
```

`HumanCharacterCreationView` (and each gameline's `...CharacterCreationView`, which
subclasses it) sets `view_mapping = WorkflowViews()`, a descriptor that returns
`get_workflow(model_class.type).view_mapping`. `is_valid_key()` accepts the position only
while the character's status is `Un` (unfinished) or `Rev` (returned for revisions); any
other status shows the detail view.

`DictView.handle_request` with `chargen_router = True` checks, before dispatching to a step:

- The user needs `Permission.EDIT_FULL` on the character. Owners have it while the status
  is `Un` or `Rev`; scoped storytellers and admins always do (see
  [Authorization](authorization.md)).
- On a `GET` or `HEAD`, a user without `EDIT_FULL` but with `VIEW_FULL` gets the detail view
  (for an htmx fragment request the router answers with `HX-Redirect` instead). Any other
  request without `EDIT_FULL` gets 404. (A reader without `VIEW_FULL` never gets this far:
  `GenericCharacterDetailView` is a `protected_object` router and shows them
  `PublicObjectDetailView` on a read, 404 otherwise.)
- The target step view is then authorized with `core.access_policy.authorize_route`. Step
  views are listed under the `CHARGEN_STEP` policy in
  [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py), which again
  requires `EDIT_FULL` and status `Un`/`Rev` and answers 404 otherwise.

## `ChargenStepMixin`

Every step view includes `ChargenStepMixin` (directly or through `AllocationStepMixin`,
`CharacterFormStepView`, `FreebieSpendingView` or `PointAllocationView`). Its `dispatch()`:

1. Loads the `Character` by `pk` and runs `authorize_route` for the step view itself, so a
   step URL reached directly is checked the same way as through the router.
2. Resolves the workflow step at `creation_status` and computes two states:
   - **waiting**: the step is `freebies` and `freebies_approved` is false. A GET renders the
     page with a "Waiting on ST to assign your freebie total" notice
     (`chargen/freebies.html`); a POST raises `PermissionDenied`.
   - **skipping**: the step's `skip_if` is true. A GET renders `chargen/skip.html` ("There
     is nothing to allocate for this step"); a POST calls `advance()` and redirects to the
     wizard.
3. Otherwise calls the view's normal lifecycle. If that returns a 302 to
   `character.get_absolute_url()` while the character is still `Un` or `Rev`, the redirect
   is rewritten to `characters:character`, because several subclasses point
   `get_absolute_url` at a plain detail route that would drop the user out of the wizard.

`render_to_response()` adds the step context used by the templates: `step`,
`chargen_steps` (`Workflow.progress`), `chargen_step_rows` (`progress_rows`),
`chargen_next_step`, `chargen_formsets` (every `*_context` dict holding a `formset`) and,
on the abilities step, `ability_rows` / `ability_columns`. `get_template_names()` returns
`chargen/step_fragment.html` for an htmx fragment request on an interactive workflow; otherwise
the view's `template_name` when it ends in `/chargen.html` (a gameline shell such as
`characters/mage/mage/chargen.html`, each of which only extends the core page), else
`characters/core/chargen.html`.

`get_form()` swaps plain `NumberInput` widgets for `widgets.widgets.dots.DotRatingInput`
using the bounds from the step's allocation rules (`dot_bounds()`), so every workflow
rates with clickable dots while the number input stays the real control. On interactive
workflows the dots are driven by the Alpine `tgDots` component and `get_form()` also calls
the form's `enable_htmx_chains()` when it has one; elsewhere the widget's own media script
drives them.

`ChargenProgressMixin` builds `chargen_steps` from a `chargen_step_labels` list. Only the
Human `...ChargenView` classes use it, and `ChargenStepMixin.render_to_response()`
replaces its values with the registry's progress for any character that has a workflow.

## Advancing and going back

`transitions.advance(character, user=)` is the only way forward:

- It runs in a transaction and raises `PermissionDenied` unless the character is `Un` or
  `Rev` and the user has `EDIT_FULL`.
- It moves from the current position to the next one and keeps moving past consecutive
  steps whose `skip_if` is true (applying `_skip_effect` to each), stopping at the last
  step at the latest.
- It saves only `creation_status` (`update_fields`); the calling view saves its own form
  data. It raises `ValueError` when called on the final step, because the final step
  submits the character instead of advancing.

Step views call `advance(self.object, user=self.request.user)` from `form_valid()` once
their data is valid.

`ChargenBackView` (`characters:chargen_back`, `POST /characters/<pk>/chargen/back/`, route
policy `LOGIN`) is owner-only. Inside a transaction it re-reads the character with
`select_for_update()` so concurrent Back posts and a concurrent freebie award serialize,
then checks `Character.can_navigate_back()`:

- the character is `Un` or `Rev`,
- `creation_status > 1` and within the workflow, and
- `freebies_approved` is false.

Once the storyteller has approved freebies, back navigation is blocked entirely, because
changing an earlier step could invalidate the freebie allocation. When allowed,
`retreat(character)` stores `previous_position()`, the nearest earlier step that does
not skip. `Character.chargen_back_url` exposes the URL only while back navigation is
allowed; the templates also hide the button from anyone but the owner.

## Allocation rules

Point pools are data, not view code. [`characters/rules/allocation.py`](../../characters/rules/allocation.py)
defines two frozen rule types that never touch the database:

- `AllocationRule`: named `fields` that must sum to exactly `total` (or at most, with
  `comparison="at_most"`), with an optional per-trait `maximum` and an optional `allowed`
  set restricting which traits may be rated above zero (for example in-clan Disciplines).
- `PriorityRule`: three groups ranked primary / secondary / tertiary, each of which must
  total its rank's `points` plus `base` per field. It checks every field lies within
  `minimum`..`maximum` first.

Each rule returns `RuleViolation(message, field, flash)` objects per phase.
`first_violation(rules, values)` reports the earliest violation in phase order `totals`,
`bounds`, `choices`, then rule order. Rules also expose `status(values)` (running totals for
display) and `client_data()` (JSON-safe limits for the browser).

[`characters/rules/limits.py`](../../characters/rules/limits.py) holds the pools:
`attribute_rule(primary, secondary, tertiary)` (Attributes start at one dot, `base=1`,
range 1-5), `ability_rule(model, form_fields, primary, secondary, tertiary, ...)` (range
0-`CHARGEN_ABILITY_MAXIMUM`, which is 3; each group counts only the abilities the form
offers), and constants such as `VAMPIRE_DISCIPLINES`, `GHOUL_DISCIPLINES`,
`VAMPIRE_VIRTUES`, `CHANGELING_ARTS`, `WRAITH_ARCANOI`, `DEMON_LORES` and `FALLEN_VIRTUES`.

### PRI / SEC / TER ranking

On the Attributes and Abilities steps the player ranks each group with three radio buttons
named `priority_<group>` (`priority_physical`, `priority_talents`, ...) whose values are
`primary`, `secondary` or `tertiary`. These are not form fields and are never saved:

- If every group has a distinct posted rank, each group must total exactly the target for
  its chosen rank, and the error message names the ranking.
- If no rank is posted, the ranking is inferred from the dots: the sorted group totals must
  equal the sorted targets.
- A partial or repeated ranking is an error ("Choose primary, secondary and tertiary once
  each for ...").

### Forms and views

`AllocationFormMixin` (with `AllocationModelForm` and the cached factory
`allocation_modelform(model, fields)`) takes `allocation_rules=` and an optional
`extra_clean=` callable. Its `clean()` merges the cleaned ratings with the posted ranks,
reports only the first violation, and keeps any flash text in `flash_errors`.

`AllocationStepMixin` connects a view to this:

- The view declares `get_allocation_rules()` (and optionally `get_extra_clean()`); it
  never sums ratings itself.
- `get_form_class()` builds an `allocation_modelform` over `fields` when no `form_class`
  is set; `get_form_kwargs()` passes the rules.
- `get_context_data()` adds `allocation_rules` (client data) and, for a `PriorityRule`,
  `priority` from `priority_columns()`: one column per group with its running count
  (`"2 left"`, `"done"`, `"1 over"`), rank options and bound fields.
- `form_invalid()` repeats flash texts as `messages.error`.
- `live_validation = True` and `validation_totals()` feed the interactive validator.

Per-gameline point values live on the step view classes as `primary`, `secondary` and
`tertiary`. For example `HumanAttributeView` uses 7/5/3 and `HumanAbilityView` 11/7/4;
`MageAbilityView` uses 13/9/5; mortal-kin Attribute views such as `VtMHumanAttributeView`
use 6/4/3.

`PointAllocationView` is the other allocation lifecycle: a bounded pool filled one record
at a time. Adapters set `model`, `allocation_name`, `total_attribute`, `spent_method` and
`complete_method` and implement `add_record()`. The view rejects a record that would exceed
the pool and advances once `complete_method()` returns true.

## Freebies

Freebies are spent at the workflow's `freebies` step, which every workflow has exactly once.

1. The pool starts from `Human.freebies` (default 15; some types, such as `Companion`, set
   their own). Mage's Spheres step also pays for starting Arete above 1 from this pool
   (`Mage.purchase_starting_arete`).
2. When the character reaches the freebie step it waits for the storyteller. It appears in
   the storyteller's "Freebies to Approve" queue (`ProfileDashboard.freebies_to_approve`:
   characters at their `freebie_step` with `freebies_approved=False`). The storyteller
   awards 0-15 backstory freebies with `FreebieAwardForm`
   (`accounts:freebie_award`), which calls `Human.award_backstory_freebies()`: it locks the
   row, adds the amount and sets `freebies_approved = True`. See
   [XP, freebies and approvals](xp-and-approvals.md#freebies).
3. The player then spends. `FreebieSpendingView.form_valid()` translates the form's
   `category` / `example` / `value` into service arguments, spends through
   `FreebieSpendingServiceFactory.locked(character)` (a row lock and a fresh read), and
   calls `advance()` once `freebies` reaches 0 while the character is still on the freebie
   step. After that the step is skipped by `exhausted_freebies`.

Each gameline adapts `FreebieSpendingView` with its own form (for example
`HumanFreebiesForm`, `ChainedMageFreebiesForm`).

## Submission at the end

The last step of every workflow is `specialties`. `HumanSpecialtiesView.form_valid()`
(inherited by each gameline's `...SpecialtiesView`) records a `Specialty` for every trait
that needs one, then sets `character.status = "Sub"` and saves. The character now leaves
the wizard: the router shows the detail view, and it appears in the storyteller's
"Characters to Approve" queue. Approval, returns for revision and the rest of the status
lifecycle are covered in [XP, freebies and approvals](xp-and-approvals.md).

A character returned for revisions (`Rev`) re-enters the wizard at its stored
`creation_status`. Back navigation stays blocked there once `freebies_approved` is set.

## Walkthrough: a Human

The `human` workflow has seven steps; every view lives in
[`characters/views/core/human.py`](../../characters/views/core/human.py).

| Pos. | Key | View | Step template | Notes |
|-----:|-----|------|---------------|-------|
| — | (create) | `HumanBasicsView` at `characters:create:human` | `characters/core/human/humanbasics.html` | Name, Nature, Demeanor, Concept. `core.mixins.prepare_created_object()` sets the owner and, for anyone but an admin, status `Un`. |
| 1 | `attributes` | `HumanAttributeChargenView` | `characters/core/attribute_block/form.html` | `attribute_rule(7, 5, 3)` |
| 2 | `abilities` | `HumanAbilityChargenView` | `characters/core/chargen/abilities.html` | `ability_rule(..., 11, 7, 4)` |
| 3 | `backgrounds` | `HumanBackgroundsChargenView` | `characters/core/background_block/form.html` | |
| 4 | `biography` | `HumanBiographicalInformationChargenView` | `characters/core/chargen/form.html` | Age, history, goals, notes |
| 5 | `freebies` | `HumanFreebiesChargenView` | `characters/core/chargen/freebies.html` | Waits for the ST's award, then spends |
| 6 | `languages` | `HumanLanguagesChargenView` | `characters/core/human/human_language_block_form.html` | Skipped without a Language merit; always adds English |
| 7 | `specialties` | `HumanSpecialtiesChargenView` | `characters/core/chargen/specialties.html` | Saves specialties and submits (`Sub`) |

A request for step 1 runs: `GET /characters/42/` → `GenericCharacterDetailView` (type
`human`) → `HumanCharacterCreationView` (`creation_status == 1`, status `Un`, user has
`EDIT_FULL`) → `HumanAttributeChargenView`. The page is `characters/core/chargen.html`,
which includes `chargen/step_body.html`, which includes the step's template. On a valid
POST the view calls `advance()` (position 2), saves, and redirects to
`characters:character`, and the router now serves the Abilities step.

## How gamelines differ

Each gameline reuses the shared steps and adds its own, in its own views module:

| Types | Module | Steps between Backgrounds and Biography | Background-detail steps after Languages |
|-------|--------|----------------------------------------|-----------------------------------------|
| `human`, `drone` | `core.human`, `werewolf.drone` | — | — |
| `vtm_human`, `wta_human`, `kinfolk`, `ctd_human`, `wto_human`, `dtf_human` | per gameline | — | Allies |
| `vampire` | `vampire.vampire_chargen` | Disciplines, Virtues | Allies, Mentor, Contacts, Retainers |
| `ghoul` | `vampire.ghoul_chargen` | Disciplines | Allies |
| `werewolf` | `werewolf.garou` | Gifts, History | Allies, Mentor, Contacts |
| `fera` and the 12 Fera breeds | `werewolf.fera` | Gifts, History (and Breed Faction as step 1) | Allies |
| `fomor` | `werewolf.fomor` | Powers | Allies, Contacts |
| `mage` | `mage.mage` | Spheres, Focus | Rote, then Node, Library, Familiar, Wonder, Enhancement, Sanctum, Allies, Mentor, Contacts, Retainers, Chantry |
| `mta_human`, `companion` | `mage.mtahuman`, `mage.companion` | — | Node, Library, Wonder, Enhancement, Sanctum, Allies, Chantry |
| `sorcerer` | `mage.sorcerer` | Psychic, Path, Ritual (each skipped by hedge-mage / psychic type) | Node, Library, Familiar, Artifact, Enhancement, Sanctum, Allies, Chantry |
| `changeling` | `changeling.changeling` | Arts Realms | Allies |
| `wraith` | `wraith.wraith_chargen` | Arcanos, Shadow, Passions, Fetters | Allies, Mentor, Contacts |
| `demon` | `demon.demon_chargen` | Lores, Apocalyptic Form, Virtues | Allies, Mentor, Contacts, Retainers, Followers |
| `thrall` | `demon.thrall_chargen` | Virtues | Allies |

Every workflow ends with Specialties. Modules are under `characters/views/`. Other
differences:

- Point values: the step views' `primary` / `secondary` / `tertiary` (see
  [Forms and views](#forms-and-views)).
- Power steps use `AllocationRule`s from `limits.py`; for example
  `VampireDisciplinesView` restricts `VAMPIRE_DISCIPLINES` to the clan's Disciplines with
  `dataclasses.replace(..., allowed=clan)`, and `VampireVirtuesView` rates the Virtues the
  vampire's Path uses (`vampire_virtue_rule`).
- Background-detail steps (Allies, Node, Library, ...) appear only if the character bought
  that Background and has not completed its detail.
- Only the `vampire` workflow sets `interactive=True`.

## Interactive (htmx) workflows

An interactive workflow uses the same URL, views and forms; only rendering differs.
`ChargenStepMixin.dispatch` sets `self.chargen_interactive` from the workflow, and the page
loads htmx, the Alpine.js CSP build and the chargen scripts through
`core/includes/interactive_scripts.html` (see [Front end](frontend.md#javascript)).

### Requests the step URL answers

A request is a *fragment request* when it carries `HX-Request: true` and is not a history
restore or boosted request (`core.htmx.is_fragment_request`).

| Request | Response | Fragment kind (`TG-Fragment` header) |
|---------|----------|--------------------------------------|
| Fragment GET or POST | `chargen/step_fragment.html`: the step form, the step list (out of band) and messages (out of band) | `chargen-step` |
| Fragment `POST` with `_validate=1` | `chargen/feedback.html`: the form's checks run without saving (`render_validation`) | `chargen-feedback` |
| Fragment `GET` with `_options=<field>` | `chargen/options.html`: `<option>`s for one chained select (`render_options`) | `chargen-options` |

Validate and options partials never advance, skip or save. They answer 204 when the step is
unavailable (waiting or skipping) or when the user exceeds `CHARGEN_PARTIAL_LIMIT` partial
requests per character per minute (read with `getattr`, default 60; the project settings do
not define it). Partial responses carry `TG-Step` (the step key); options responses also
carry `TG-Chain` (the ancestor values they were computed for) and, when the form defines
`field_visibility()`, an `HX-Trigger-After-Swap` event `tg-visibility`. All interactive
responses vary on the htmx request headers (`core.htmx.vary_on_htmx`).

After a fragment POST, a redirect back into the wizard is followed inside the XHR and the
next step's fragment is swapped in. A redirect anywhere else (the final step submitting)
becomes an `HX-Redirect`, so htmx navigates the whole page.

The validator element in `chargen/step_body.html` posts `_validate=1` on load, on change
(250 ms delay), on input (600 ms delay) and after a chained select's options are swapped
(`tg-options-swapped`, 250 ms). `feedback.html` shows "Ready" when the form is
valid (including the view's `validate_submission()`) and `validation_is_final` is true; `FreebieSpendingView` sets
`validation_is_final = False` because the spending service's checks cannot be dry-run, so
its feedback says "No problems found so far". Running totals come from
`validation_totals()`.

### Client scripts

`ChargenStepMixin.interactive_scripts` lists
[`chargen.js`](../../characters/static/characters/js/chargen.js),
[`chargen-components.js`](../../characters/static/characters/js/chargen-components.js) and
[`chargen-priority.js`](../../characters/static/characters/js/chargen-priority.js):

- `chargen.js` swaps a response only if its `TG-Fragment` matches the requesting element's
  `data-tg-expect`; otherwise it loads the URL as a full page (expired session, error page,
  a step that left the wizard). It drops validation and option responses for a step no
  longer shown or for chain values that have changed, revalidates after an options swap,
  and moves focus to the error summary or the new step heading after a step swap.
- `chargen-components.js` registers the Alpine components `tgDots` (clickable dots),
  `tgPool` (instant totals from the rules' client data) and `tgConditional` (applies the
  server's field visibility). They give instant feedback only and never block input or
  submission.
- `chargen-priority.js` keeps the PRI / SEC / TER radios unique (choosing a rank another
  column holds swaps them) and updates each column's count. It runs on every workflow.

## Without JavaScript

Every workflow, interactive or not, works as plain HTML:

- `chargen.html` renders a normal `<form method="post" enctype="multipart/form-data">`
  (multipart so steps with an image field can upload). On an interactive workflow the
  form in `chargen/step.html` has both `action` and `hx-post`, so it posts normally when
  htmx is absent.
- `DotRatingInput` keeps the `<input type="number">` as the control; the dots are hidden
  without JavaScript.
- The PRI / SEC / TER choices are ordinary radio inputs posted with the form; with none
  chosen the server infers the ranking.
- Chained selects re-render with the right options on the bound form after a POST.
- The server's `clean()` is the verdict in every case. Non-interactive workflows also load
  [`attribute-validation.js`](../../characters/static/characters/js/attribute-validation.js)
  or [`ability-validation.js`](../../characters/static/characters/js/ability-validation.js)
  for running hints, and [`core/js/validation.js`](../../core/static/core/js/validation.js)
  provides the shared `TG.validation` helpers they use.

## Templates

| Template | Role |
|----------|------|
| `characters/core/chargen.html` | Page shell (extends `core/tl_base.html`): the cover carries the draft's name, portrait and step list; the pages hold one step |
| `chargen/step_body.html` | Error summary, "Step 01 of 07" and heading, the step template (or `skip.html`), the live validator, Save / Back / Cancel |
| `chargen/interactive.html`, `chargen/step.html` | The htmx root and the swappable `form#chargen-step` |
| `chargen/step_fragment.html` | Fragment response: the step form plus out-of-band step list and messages |
| `chargen/progress_region.html`, `steps.html`, `step_list.html` | The step list (`#chargen-progress`); desktop list and a mobile segment bar with a "Steps" sheet. Grouped rows are tagged "if taken", other skippable rows "if any" |
| `chargen/form.html`, `fields.html` | Default step body: the form's fields and any formsets |
| `chargen/abilities.html`, `alloc_row.html`, `priority_head.html`, `pool.html` | Ranked allocation columns, the PRI / SEC / TER picker and the `tgPool` summary |
| `chargen/freebies.html`, `freebies_chained.html` | Freebie step bodies (plain and interactive) |
| `chargen/specialties.html`, `skip.html` | Final step and the "nothing to allocate" body |
| `chargen/feedback.html`, `options.html` | Validate-only and chained-options partials |

The Save button renders first in the actions row so it stays the implicit submitter when the
player presses Enter; Back carries `formnovalidate` and `formaction`, so it would otherwise
submit and discard the step's edits.

## See also

- [Adding a chargen step](../guides/adding-a-chargen-step.md)
- [XP, freebies and approvals](xp-and-approvals.md)
- [Authorization](authorization.md)
- [Front end](frontend.md)
- [`characters` app](../../characters/README.md)
