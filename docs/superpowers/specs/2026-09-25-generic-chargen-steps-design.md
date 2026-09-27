# Shared character creation steps

## Intent and compatibility

Implement the Step 3 brief, superseding its historical design-only restriction.
After rebasing on main (`c14f2bad`), Step 0 authorization and Step 2's 231-slot
registry are available. Preserve every registered view path, saved position,
route-policy identity, form field, allocation rule, and gameline template.
The registry owns navigation and applicability; views own form orchestration;
existing models and spending services own the rules they already implement.

## Approach

Retain named view subclasses as configuration adapters. Consolidate actual
algorithms in shared bases, with hooks only for observed variations. Rejected:
generating view classes dynamically (obscures route identities), and putting game
rules into Step metadata (duplicates the existing model/service responsibilities).
No migrations, dependencies, new routes, workflow reordering, or htmx.

* Languages: one HumanLanguagesView, with model/template configuration. Read
  validated language_1..N values, add English, and use advance(character, user=...).
  Preserve Wraith feedback/context. Fix Companion's zero-based/nonexistent field
  lookup and missing default English in Companion/Sorcerer.
* Specialties: one submission handler and object/form lifecycle. Default
  get_specialties_needed() delegates to needed_specialties(); Companion and
  Sorcerer preserve their current alternate rules as overrides. Use cleaned data.
* Abilities: one bounded-rating and three-pool algorithm using model ability
  groups. Preserve per-view allocation totals, forms, context, and Wraith messages.
* Extras: one field/widget/placeholder lifecycle and advancement handler;
  configuration retains model-specific fields and wording. Explicit preparation
  hooks retain Companion gifts/freebie budgets and Wraith
  completion behavior. Do not move those game rules into a new service here.
* Template selection: one approved/public gameline/type-filtered form and one
  apply/skip handler, preserving the six public view/form import names and routes.
* Freebies: reuse HumanFreebiesView and FreebieSpendingServiceFactory for Companion
  and Sorcerer. Preserve advancement exactly once, supported category
  values, familiar derived stats and existing validation. Never route invalid
  forms into form_valid. The shared view advances on an exhausted successful spend;
  services persist spending but do not own navigation. Adapt validated choice IDs
  into the objects expected by the existing service handlers.
* Wraith point allocations: one bounded allocation view configured with total,
  spent/completion methods, form, messages and add-record hook for Passions/Fetters.
* CRUD: one permission-aware form selection mixin using the scoped editor role.
  Preserve explicit allowlists; generated ModelForms use reviewed fields and model
  ability/attribute groups, never unrestricted model introspection or __all__.
* Detail: reuse CharacterDetailView through HumanDetailView where appropriate,
  retaining XP approval handlers and custom context. All character details get
  scene filtering and authorized retire/decease behavior; reference-data views do
  not acquire character actions.

## Registry and authorization

Shared step bases include ChargenStepMixin and SpendFreebiesPermissionMixin.
Existing subclasses stay bound by Step.view_path. advance remains the only
navigation operation; terminal specialties set Sub without advancing beyond the
workflow. GET remains read-only, skip effects stay in the transition service,
and freebie approval gates remain in ChargenStepMixin. No per-copy role checks.

## Shared class API

| Shared implementation | Adapter configuration / extension |
|---|---|
| `HumanLanguagesView` | `model`, `template_name`, `success_message`; fields come from `HumanLanguageForm` |
| `HumanSpecialtiesView` | Same configuration; `get_specialties_needed()` retains exceptional rule selection |
| `HumanAbilityView` | `model`, `fields`, three allocation totals, optional success/rating/pool messages |
| `CharacterExtrasView` | `fields`, date/optional fields, widget attributes/help text; `validate_extras(form)` and `prepare_character(form)` |
| `CharacterTemplateSelectView` | `model`, `form_class`, `template_name`, `creation_route`; selection form configures `gameline` and `character_type` |
| `FreebieSpendingView` | `model`, `form_class`, `template_name`, `example_models`, `category_aliases`; `get_spending_kwargs(form)` extends validated service arguments |
| `PointAllocationView` | Model/form/template, pool name, total/spent/completion method names, completion message; `add_record(obj, data)` |
| `ScopedEditFormMixin` | `limited_form_class`; full Django ModelForm generated from reviewed `fields` or an existing `form_class` |
| `CharacterDetailView` | Existing model/template/context overrides; status buttons and handlers consult the model's existing transition map |

## Audit and verification

Capture an AST inventory before/after implementation, grouping own-method bodies
and separately reporting configuration, exact duplicates, and real variations.
An AST similarity group is a review lead, not proof of equivalent behavior.
Record confirmed/refuted brief findings and measured reductions in the report.

Use the existing registry golden fixture and all-step GET coverage. Add table-driven
POST characterization by registered step family, asserting persisted fields,
relations, progression/submission and redirects. Add failing regression tests for
listed bugs. Include invalid inputs, unauthorized POST immutability, returned and
locked statuses, mixed gameline ST roles, incomplete linked backgrounds at final
freebie spend, specialty path rules, and detail action authorization.

## Review slices and estimated reduction

Languages (~350 lines), specialties (~250), abilities (~170), extras (~350),
template selection (~280), freebies (~180), Wraith allocations (~60), CRUD/detail
(~300 plus shared field lists). These are ordered independently reviewable slices
within the single implementation PR requested by the user; actual results belong
in the inventory report. Keep virtues, arts/realms, apocalyptic forms, linear magic,
focus/spheres/rotes, Fera breed/faction and linked-background creation bespoke.

## Theory and extension

A chargen step is a form lifecycle whose configuration varies by character type;
navigation is a separate registry concern. A new gameline reuses a named adapter
with its model, template and exceptional hook, without copying persistence code.
Explicit field allowlists cost some declarations but avoid exposing sensitive
model fields as models evolve. General duplicate-submit/row-lock redesign remains
outside this refactor, as in Step 2.

## Implementation findings

Characterization exposed additional defects at the boundaries being consolidated:
Sorcerer path specialties have no Statistic row and crashed their form; the form
now uses the supplied stat key and a readable fallback label. Template selection
checked some anonymous requests before authentication and allowed a locked
position-zero character to apply a template; the shared entry-point guard closes
both cases. Companion extras assigned their freebie budget after advancement,
which could skip spending when the previous balance was zero; preparation now
precedes applicability checks. Initial template selection remains a direct 0-to-1
assignment because position zero is outside the registry.

The original Companion view charged double for willpower and updated familiar
Essence and Ferocity Rage, whereas its existing service did not. Narrow service
overrides preserve these existing view effects. No cost table is redesigned.
The actual chained freebie forms often return choice IDs while services expect
objects; the shared view normalizes that boundary and rejects invalid forms.

Character CRUD uses explicit composed allowlists to generate Django ModelForms,
rather than unrestricted introspection. This deliberately preserves field order
and excludes any newly added model field until reviewed. Human/Spirit views which
never had limited-form selectors retain their previous field policy. Remove the
nonexistent Vampire current_willpower field and repeated Mage time entry. Missing
direct EditPermissionMixin guards on Vampire/Ghoul/Revenant are restored. Mage
retire/decease delegates to the common handler, avoiding a validation exception
when attempting to retire a deceased Mage.

The shared detail handler also hides and ignores transitions disallowed by
Character.STATUS_TRANSITIONS (for example Un-to-Dec), rather than exposing a
button whose POST raises model validation errors. Mage keeps its existing 403
action guards before delegating mutation to the common handler. No status rule
is changed. Non-Mage biography intentionally uses neutral wording, since mortal
gameline affiliation and Companion/Sorcerer status do not imply a Mage Awakening.
