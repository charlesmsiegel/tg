# Changeling freeholds

This page explains the Changeling `Freehold` model (its archetype, features and
powers, and how feature points and Holdings are counted), the four-step creation
wizard, and the direct create and edit forms. It is for developers working on
freeholds and for agents creating them. The Wraith `WraithFreehold` is an unrelated
model; see [models](models.md#wraith-the-oblivion-wto).

## The model

Source: [`locations/models/changeling/freehold.py`](../models/changeling/freehold.py).

`Freehold` (`type = "freehold"`, `gameline = "ctd"`) extends `LocationModel`.

| Field | Meaning |
|-------|---------|
| `archetype` | `academy`, `hearth` (default), `homestead`, `manor`, `market`, `repository`, `stronghold`, `thorpe`, `workshop` |
| `aspect`, `quirks` | The underlying dream; oddities the holders cannot change |
| `balefire` | 0–5, default 1 |
| `size` | 0–5, default 1 |
| `sanctuary` | 0–5, default 0 |
| `resources` | 0–5, default 0 |
| `passages` | 0–20, default 1: trods and raths connected to the freehold |
| `powers` | JSON list of `PowerChoices` values |
| `academy_ability` | The Ability an Academy teaches |
| `hearth_ability` | `leadership` or `socialize`, for a Hearth |
| `dual_nature_archetype`, `dual_nature_ability` | The second archetype (and its ability) for the Dual Nature power |
| `resource_description`, `passage_description`, `balefire_description` | Free text |

The numeric ranges are enforced by validators and matching `CheckConstraint`s.

### Feature points and Holdings

Powers and their costs:

| Power (`PowerChoices`) | Cost |
|------------------------|------|
| `warning_call` | 1 |
| `glamour_to_dross` | 2 |
| `resonant_dreams` | 2 |
| `call_forth_flame` | 3 |
| `dual_nature` | 3 |

- `get_total_feature_points()` = `balefire + size + sanctuary + resources`, plus
  `passages − 1` when there is more than one passage (the first is free), plus the
  cost of each power.
- `get_holdings_required()` = feature points ÷ 3, rounded up: the Holdings background
  dots the freehold needs.
- `has_power(name)` checks the `powers` list.
- `get_archetype_display_with_benefit()` returns the archetype with its benefit, for
  example "Academy (-2 difficulty on Kenning)" using `academy_ability`, or "Hearth
  (-2 difficulty on Leadership)" using `hearth_ability`.
- `get_size_description()` describes sizes 0–5 in words.

## Two ways to create a freehold

| Route | View | Form |
|-------|------|------|
| `/locations/changeling/create/freehold/` (`locations:changeling:create:freehold`) | `FreeholdBasicsView`, then the wizard | The four wizard forms |
| `/locations/changeling/create/freehold/direct/` (`locations:changeling:create:freehold_direct`) | `FreeholdCreateView` | `FreeholdForm` (all fields) |

The freehold's `get_creation_url()` and the create menu point at the wizard. Its
`get_update_url()` is `locations:changeling:update:freehold`, the wizard router, and
the all-fields edit page is `/locations/changeling/update/freehold/<pk>/direct/`
(`locations:changeling:update:freehold_direct`).

## The creation wizard

Source: [`locations/views/changeling/creation.py`](../views/changeling/creation.py),
[`locations/forms/changeling/creation.py`](../forms/changeling/creation.py).

| Step | View | Form fields | After a valid POST |
|------|------|-------------|--------------------|
| 1 Basics | `FreeholdBasicsView` (`LoginRequiredMixin`, `CreateView`) | `name`, `archetype`, `aspect`, `description` | Saves with `creation_status = 1`; when the user has characters (`profile.my_characters()`), `owned_by` is set to the first. Redirects to `get_update_url()`. |
| 2 Features | `FreeholdFeaturesView` | `balefire`, `size`, `sanctuary`, `resources`, `passages`, `balefire_description` | `creation_status = 2` |
| 3 Powers | `FreeholdPowersView` | `powers` (checkboxes), `dual_nature_archetype`, `dual_nature_ability` | `creation_status = 3` |
| 4 Details | `FreeholdDetailsView` | `academy_ability`, `hearth_ability`, `resource_description`, `passage_description`, `quirks`, `contained_within`, `owned_by` | `creation_status = 5`, then redirect to the detail page |

Steps 2 to 4 are reached through `FreeholdCreationView` at
`/locations/changeling/update/freehold/<pk>/`, a `core.views.generic.DictView` keyed on
`creation_status` (1 → Features, 2 → Powers, 3 → Details). A step is shown only while
the freehold's `status` is `Un` or `Rev` and the user has `EDIT_FULL`; a reader with
only `VIEW_FULL` is sent to the detail page, and anyone else gets a 404. Any other
`creation_status` renders `FreeholdDetailView`. The step views also require the
`SPEND_FREEBIES` permission (`core.mixins.SpendFreebiesPermissionMixin`).

`FreeholdBasicsView` does not set `owner` or `status`; the new freehold keeps the
model defaults (`owner` empty, `status = "Un"`).

Validation in the wizard forms:

- **Features** (`FreeholdFeaturesForm.clean()`) computes `feature_points` for display;
  it does not cap the total.
- **Powers** (`FreeholdPowersForm.clean()`): Dual Nature needs a second archetype, and
  a second archetype of Academy needs an ability.
- **Details** (`FreeholdDetailsForm`): an Academy needs `academy_ability` and a Hearth
  needs `hearth_ability`. The field for the other archetype is hidden.

The step templates are under `locations/changeling/freehold/chargen/` and share
`chargen/base.html`; see [templates](templates.md).

## The direct form: `FreeholdForm`

Source: [`locations/forms/changeling/freehold.py`](../forms/changeling/freehold.py).

One form with every freehold field plus `contained_within`, `owned_by` and the three
barriers. `clean()` applies the archetype and Dual Nature rules above and sets
`feature_points` and `holdings_required` on the form (`(feature_points + 2) // 3`).
`save()` defaults `powers` to `[]` and clears `academy_ability`, `hearth_ability` and
the Dual Nature fields when the archetype or powers do not use them. On edit, those
fields render hidden when they do not apply.

Views ([`views/changeling/freehold.py`](../views/changeling/freehold.py)):

- `_FreeholdCreateView` (`FormView`) calls `prepare_created_object()` (owner and
  status) and saves the form.
- `_FreeholdUpdateView` (`UpdateView`, `EditPermissionMixin`) and
  `_FreeholdDetailView` add `feature_points` and `holdings_required` to the context.

The direct form loads [`static/locations/js/freehold-form.js`](../static/locations/js/freehold-form.js);
the Features and Powers steps load `freehold-features.js` and `freehold-powers.js`.

## See also

- [Location models](models.md)
- [Location forms](forms.md)
- [Views and URLs](views-and-urls.md)
- [Character creation](../../docs/architecture/character-creation.md)
- [Glossary](../../docs/reference/glossary.md)
