# Adding a chargen step

This guide covers adding a step to a character-creation (chargen) workflow, or changing an
existing one: the step definition, the step view, its template, its route policy, what
interactive (htmx) workflows add, what happens to characters already part-way through, and the
tests. It is for developers and agents working in [`characters/chargen/`](../../characters/chargen/)
and the gameline `*_chargen` view modules. The machinery (routers, `ChargenStepMixin`, skip
predicates, freebies) is explained in [Character creation](../architecture/character-creation.md).

The running example adds a "Pact" step to the Thrall workflow, after Virtues. It is
illustrative: the real Thrall workflow has no such step. Names containing `Pact` in step or
view names are invented; everything they plug into is real.

## How a step is defined

| Piece | Where | What it holds |
|-------|-------|---------------|
| `Step` | [`characters/chargen/registry.py`](../../characters/chargen/registry.py) | `key` (unique in the workflow), `label` (shown in the step list), `view_path` (dotted path of the view), `template` (the step body, default `characters/core/chargen/form.html`), `skip_if` (predicate or `None`), `group` (steps sharing a group collapse into one row of the step list) |
| `Workflow` | same | `steps` (a tuple) and `interactive` (htmx mode). Rejects duplicate keys and requires exactly one `freebies` step. |
| Shared steps and workflows | [`characters/chargen/definitions.py`](../../characters/chargen/definitions.py) | Module-level `Step` constants (`ATTRIBUTE`, `ABILITY`, `BACKGROUNDS`, `EXTRAS`, `FREEBIES`, `LANGUAGES`, `SPECIALTIES`, `DISCIPLINES`, `VIRTUES`, ...), the tuples `STATS` and `MORTAL`, one `bind(...)` per workflow, and `WORKFLOWS` (character `type` to workflow) |
| Skip predicates | [`characters/chargen/predicates.py`](../../characters/chargen/predicates.py) | Read-only checks such as `exhausted_freebies`, `no_languages`, `background("allies")` |
| Transitions | [`characters/chargen/transitions.py`](../../characters/chargen/transitions.py) | `advance(character, user=...)` and `previous_position(character)` |

`bind(tasks, module, prefix, templates=..., views=..., interactive=...)` copies each shared
`Step` and sets its `view_path` to `f"{module}.{prefix}{step.view_path}View"` (so the
`VIRTUES` step bound with prefix `"Thrall"` points at `ThrallVirtuesView`), unless `views`
names the class for that key; `templates` overrides the step-body template per key.

A character's position is the 1-based index of its current step, stored in
`Character.creation_status`. The step list therefore identifies a step by where it sits, not
by its key: inserting, removing or reordering steps changes what every stored position means.

## Prerequisites

- The character type already has a workflow and a `...CharacterCreationView` router (see
  [Adding a character type](adding-a-character-type.md)).
- You know whether the step always applies or can be skipped, and whether it saves a model
  form, a plain form or a set of records.

## Steps

### 1. Define the step

If an existing `Step` constant fits (for example `VIRTUES` or a background detail step such as
`ALLIES`), reuse it. Otherwise add one to `definitions.py`, next to the others:

```python
PACT = Step(
    "pact",
    "Pact",
    "Pact",  # bind() turns this into "<prefix>PactView"
    "characters/demon/thrall/steps/pact.html",
    skip_if=no_master,
)
```

A skippable step needs a predicate in `predicates.py`. Predicates run on `GET` too, so they
must only read:

```python
def no_master(character):
    return character.master_id is None
```

For a step that details a Background (Allies, Mentor, Node, ...), use `background("<name>")`
as `skip_if` and set `group="background"`: `test_every_background_gated_step_is_in_the_background_group`
in [`characters/tests/test_chargen_registry.py`](../../characters/tests/test_chargen_registry.py)
requires both or neither.

A skipped step can have a side effect when `advance()` passes over it. The only one today is
in `transitions._skip_effect`: skipping `languages` adds English. Add a branch there only if
skipping must write something.

### 2. Place it in the workflow

Insert it into the workflow's tuple:

```python
THRALL = bind(
    STATS
    + (
        VIRTUES,
        PACT,
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.demon.thrall_chargen",
    "Thrall",
)
```

The last step of every workflow is `SPECIALTIES`; its view sets the status to `Sub` (see
[Character creation](../architecture/character-creation.md#submission-at-the-end)).

### 3. Write the step view

Put the view in the workflow's module (`characters/views/demon/thrall_chargen.py`). Pick the
base that matches the step:

| Base | Use for | Example |
|------|---------|---------|
| `UpdateView` with `ChargenStepMixin` and `SpendFreebiesPermissionMixin` (or `SpecialUserMixin`) | Editing fields of the character | `HumanBiographicalInformation` in [`characters/views/core/human.py`](../../characters/views/core/human.py) |
| `AllocationStepMixin` + the above | Dots that must add up to a total or follow PRI/SEC/TER priorities, described by `characters.rules` | `ThrallVirtuesView` (`allocation_rules = (FALLEN_VIRTUES,)`), `HumanAttributeView` |
| `CharacterFormStepView` ([`characters/views/core/form_steps.py`](../../characters/views/core/form_steps.py)) | A plain `forms.Form` whose `form_valid` writes records | `HumanLanguagesView`, `HumanSpecialtiesView` |
| `PointAllocationView` ([`characters/views/core/allocations.py`](../../characters/views/core/allocations.py)) | Adding one record at a time to a bounded pool | `WraithPassionsView`, `WraithFettersView` |
| `GenericBackgroundView` ([`characters/views/core/generic_background.py`](../../characters/views/core/generic_background.py)) | Detailing each rating of one Background | `ThrallAlliesView` |
| `CharacterExtrasView` ([`characters/views/core/extras.py`](../../characters/views/core/extras.py)) | The biography step | `ThrallExtrasView` |

The contract every step view keeps:

- **Include `ChargenStepMixin`** (directly or through one of the bases above). Its `dispatch()`
  loads the character, authorizes the route, handles a skipped step and the freebies wait, and
  renders the step inside the chargen page.
- **Call `advance(character, user=request.user)` when the step is complete**, in
  `form_valid()`, then let the view redirect. `advance()` checks `EDIT_FULL` and status
  `Un`/`Rev`, moves `creation_status` past any following steps whose `skip_if` is true and
  saves only that field. Save your form data with the view's normal lifecycle.
- **Never call `form_valid()` from `form_invalid()`**
  ([`characters/tests/test_view_rules_guard.py`](../../characters/tests/test_view_rules_guard.py)).
- **Redirect to `get_absolute_url()` or the wizard.** When the response is a redirect to the
  character's `get_absolute_url()` and the character is still `Un` or `Rev`,
  `ChargenStepMixin.dispatch()` rewrites it to the wizard URL, `characters:character`.

```python
# characters/views/demon/thrall_chargen.py already imports UpdateView, advance,
# ChargenStepMixin and SpecialUserMixin; add SpendFreebiesPermissionMixin from core.mixins.
class ThrallPactView(ChargenStepMixin, SpendFreebiesPermissionMixin, SpecialUserMixin, UpdateView):
    model = Thrall
    fields = ["master", "daily_faith_offered"]
    template_name = "characters/demon/thrall/chargen.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        advance(self.object, user=self.request.user)
        return response
```

`template_name` is the page: a name ending in `/chargen.html` is rendered as given (the
Thrall one only extends `characters/core/chargen.html`), anything else falls back to
`characters/core/chargen.html`. The step's own markup is the `Step.template`, which
[`characters/core/chargen/step_body.html`](../../characters/templates/characters/core/chargen/step_body.html)
includes between the step heading and the Save, Back and Cancel buttons.

Every `ChargenStepMixin` subclass in a workflow module must be used by some workflow step
(`test_no_orphan_step_views`).

### 4. Write the step template

Create the `Step.template` file, for example
`characters/templates/characters/demon/thrall/steps/pact.html`. It renders only the step's
fields; the surrounding form, errors summary and buttons come from `step_body.html`. The
default, [`characters/core/chargen/form.html`](../../characters/templates/characters/core/chargen/form.html),
renders `form` through `characters/core/chargen/fields.html` plus any formsets the view exposes
(context keys ending in `_context` that hold a `formset`). Use it unless the step needs its own
layout.

```django
{% for field in form.visible_fields %}
    {% include "core/tl/field.html" with field=field %}
{% endfor %}
```

Follow the Spread rules (no inline `style=""`, no Bootstrap classes); see
[Front end](../architecture/frontend.md).

### 5. Declare the route policy

Add the view's dotted path to `CHARGEN_STEP` in
[`core/route_policy_manifest.py`](../../core/route_policy_manifest.py):

```text
characters.views.demon.thrall_chargen.ThrallPactView
```

`CHARGEN_STEP` answers 404 unless the user has `EDIT_FULL` on the character and its status
is `Un` or `Rev`. Step views have no URL of their own; the route-policy test reaches them
through the router's `view_mapping`.

### 6. Update the golden fixture

[`characters/tests/fixtures/chargen_order.json`](../../characters/tests/fixtures/chargen_order.json)
lists, per character type, the dotted step-view paths in order. Insert the new path at its
position. `test_all_persisted_positions_are_preserved` compares it with the registry and loads
every step template, so the fixture change is the reviewed record that stored positions
moved.

### 7. Move characters already in the wizard

Inserting a step before other steps, removing one or reordering them shifts what existing
`creation_status` values mean: a Thrall saved at position 5 (Biography) would reopen at the
new Pact step. Ship a `tg_schema` migration that moves unfinished characters of that type,
as the registry's module docstring requires. See [Reordering steps](#reordering-steps).
Appending a step after the last one a character could have reached, or changing only a
step's template or view class, needs no migration.

## Reordering steps

Write the remap as a `tg_schema` migration (procedure and rules in
[Changing the schema](changing-the-schema.md)). Look the model up with `live_model`, touch
only characters still in creation, and map old positions to new ones in one `update()` per
distinct shift (a mapping with several shifts can use `Case`/`When` in a single update):

```python
"""Thrall chargen gained a Pact step at position 5: move unfinished thralls past it."""

from django.db import migrations
from django.db.models import F

from tg_schema.schema import live_field, live_model


def move_thrall_positions(apps, schema_editor):
    Thrall = live_model("characters.Thrall")
    if live_field(Thrall, "creation_status") is None:
        return
    Thrall.objects.using(schema_editor.connection.alias).filter(
        status__in=("Un", "Rev"), creation_status__gte=5
    ).update(creation_status=F("creation_status") + 1)


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0008_unique_scene_read_status")]
    operations = [migrations.RunPython(move_thrall_positions, migrations.RunPython.noop)]
```

A positional shift cannot be made repeatable by filtering, because a moved row looks like any
other row at its new position. It relies on Django recording the migration as applied, so keep
it in a migration of its own and test that one run moves each position exactly once.

## Interactive (htmx) workflows

A workflow bound with `interactive=True` serves htmx fragments from the same step URL; today
only `VAMPIRE` is interactive. The same views and forms serve both modes, and a browser
without JavaScript posts the plain form (see
[`characters/tests/views/test_chargen_nojs_walkthrough.py`](../../characters/tests/views/test_chargen_nojs_walkthrough.py)).
`ChargenStepMixin` adds, only for fragment requests (`core.htmx.is_fragment_request`: an
`HX-Request` that is neither a history restore nor boosted):

| Request | Response |
|---------|----------|
| `GET`/`POST` with `HX-Request` | The step rendered with `fragment_template` (`characters/core/chargen/step_fragment.html`), marked `TG-Fragment: chargen-step` and varied on the htmx headers. A redirect to the wizard URL is followed inside the request; a redirect elsewhere (the terminal step) becomes `HX-Redirect`. |
| `POST` with `_validate=1` | `render_validation()`: runs the step's form checks and `validate_submission()` without saving or advancing, and renders `feedback_template` with errors and `validation_totals()` (`TG-Fragment: chargen-feedback`, `TG-Step: <key>`) |
| `GET` with `_options=<field>` | `render_options()`: the `<option>` list for a `widgets` `ChainedChoiceField` whose form defines `chain_for()` (`TG-Fragment: chargen-options`), with `TG-Chain` and, if the form has `field_visibility()`, a `tg-visibility` event in `HX-Trigger-After-Swap`. Unknown fields get 400. |

Validate and options requests answer 204 when the step is unavailable (no step, freebies
awaiting approval, or a step being skipped) and when a user exceeds the per-minute limit for a
character (`settings.CHARGEN_PARTIAL_LIMIT`, 60 when unset). They never advance, skip or save.

To make a new step work well in an interactive workflow:

- Set `live_validation = True` on the view when its template should show the live verdict
  (`AllocationStepMixin` and `FreebieSpendingView` already do).
- Override `validation_totals(form)` to report running totals, and `validate_submission(form)`
  for checks the submit makes after `is_valid()`; keep both free of side effects.
- Set `validation_is_final = False` when the submit runs checks that cannot be dry-run (a
  spending service), so the feedback does not promise success.
- Mark any other partial you add with `core.htmx.mark_fragment(response, kind)` and
  `vary_on_htmx(response)`.

## Tests

| What | Where |
|------|-------|
| The step renders for the owner at its position through `characters:character` | `test_every_step_renders_for_its_owner_without_changing_progress` in [`characters/tests/test_chargen_workflow.py`](../../characters/tests/test_chargen_workflow.py) runs every workflow step automatically |
| A valid post saves and advances; an invalid one re-renders without advancing | a view test in `characters/tests/views/<gameline>/test_<type>_chargen.py` |
| The skip predicate and any skip effect | [`characters/tests/test_chargen_transitions.py`](../../characters/tests/test_chargen_transitions.py) |
| Another user, a submitted character and an anonymous user get 404 or no fragment | `characters/tests/views/test_chargen_htmx.py` (interactive), `test_unauthorized_reads_and_posts_do_not_advance` in `test_chargen_workflow.py` |
| Validate and options partials write nothing (interactive only) | `test_valid_allocation_is_ready_but_never_saved_or_advanced` in [`characters/tests/views/test_chargen_htmx.py`](../../characters/tests/views/test_chargen_htmx.py) |
| The position migration | `tg_schema/tests/test_<name>.py` |
| Order and templates | `chargen_order.json` (step 6), checked by `test_chargen_registry.py` |

## Checklist

- [ ] `Step` defined or reused; unique key; `skip_if` is read-only; background steps grouped.
- [ ] Workflow tuple updated; still exactly one `freebies` step; `SPECIALTIES` last.
- [ ] Step view includes `ChargenStepMixin`, calls `advance()` on completion, never calls
  `form_valid()` from `form_invalid()`.
- [ ] Step template renders only the step's fields; Spread rules followed.
- [ ] View listed under `CHARGEN_STEP`.
- [ ] `chargen_order.json` updated.
- [ ] `tg_schema` migration and test when stored positions moved.
- [ ] Interactive workflows: `live_validation`, side-effect-free validation hooks.
- [ ] Tests for the step, its skip rule and its denials.

## See also

- [Character creation](../architecture/character-creation.md)
- [Adding a character type](adding-a-character-type.md)
- [Changing the schema](changing-the-schema.md)
- [`characters/chargen/definitions.py`](../../characters/chargen/definitions.py)
- [`characters/views/core/chargen_mixins.py`](../../characters/views/core/chargen_mixins.py)
