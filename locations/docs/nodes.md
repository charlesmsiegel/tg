# Nodes and reality zones

This page explains the Mage `Node` model, the point budget `NodeForm` enforces when a
node is created or edited, how weekly Quintessence and Tass output is derived, and the
reality zones that nodes, sanctums and demesnes carry. It is for developers changing
node rules and for agents creating nodes through the site or the chargen wizards.

## The `Node` model

Source: [`locations/models/mage/node.py`](../models/mage/node.py).

`Node` (`type = "node"`, `gameline = "mta"`) extends `MeritFlawBlock` and
`LocationModel`.

| Field | Type | Meaning |
|-------|------|---------|
| `rank` | int 0–10 | The node's rating (validators and a `CheckConstraint`) |
| `size` | `SizeChoices` | -2 Household Object, -1 Small Room, 0 Average Room (default), 1 Small Building, 2 Large Building |
| `ratio` | `RatioChoices` | -2 "0.0", -1 "0.25", 0 "0.5" (default), 1 "0.75", 2 "1.0": the share of output that is Quintessence |
| `points` | int 0–100 | Set to `3 × rank` by `set_rank()`; `NodeForm` does not set it |
| `quintessence_per_week`, `tass_per_week` | int 0–100 | Weekly output |
| `quintessence_form`, `tass_form` | text | What the Quintessence and Tass look like |
| `merits_and_flaws` | M2M `characters.MeritFlaw` through `NodeMeritFlawRating` (rating -10 to 10) | |
| `resonance` | M2M `characters.Resonance` through `NodeResonanceRating` (rating 0–10) | |
| `reality_zone` | FK `RealityZone` | See [reality zones](#reality-zones) |

Model helpers:

- `set_rank(rank)` sets `rank` and `points = 3 × rank`.
- `add_resonance(resonance)` raises a Resonance rating by one, up to 5 (returns
  `False` at 5); `resonance_rating()`, `total_resonance()`, `filter_resonance(minimum,
  maximum, sphere)` and `check_resonance(resonance, sphere)` read ratings.
- `has_resonance()` is true when total Resonance is at least `rank`.
- `filter_mf(minimum, maximum)` narrows `MeritFlawBlock.filter_mfs()` to merits and
  flaws whose ratings fall in the range.
- `update_output()` splits `points` into Quintessence (`int(points × ratio)`) and Tass
  (the rest), using the ratio's label as the fraction.
- `resonance_postprocessing()` adds two dots of "Corrupted" Resonance when the node has
  the Corrupted flaw, and one Resonance matching the Sphere of each "Sphere Attuned (…)"
  merit.
- `set_output_forms()`, `has_output_forms()`, `has_output()`, `set_ratio()`,
  `set_size()`.

`update_output()` and `resonance_postprocessing()` are model helpers; `NodeForm` does
not call them and computes the output itself.

A chantry's `nodes` field (related name `chantry_nodes`) lists the nodes it holds; see
[chantries](chantries.md).

## Creating and editing a node: `NodeForm`

Source: [`locations/forms/mage/node.py`](../forms/mage/node.py).

`NodeForm` is used by:

- the node create and edit pages (`locations:mage:create:node`,
  `locations:mage:update:node`);
- step 3 of the [chantry wizard](chantries.md#the-creation-wizard);
- the Node background step of the Mage, MtA human, Companion and Sorcerer character
  wizards (`characters.views.mage.*`). The constructor drops the `obj` and `npc_role`
  keyword arguments those views pass.

### Fields and formsets

Model fields: `name`, `rank`, `description`, `ratio`, `size`, `quintessence_form`,
`tass_form`, `contained_within` (optional), `gauntlet`, `shroud`,
`dimension_barrier`.

| Formset | Prefix | Rows |
|---------|--------|------|
| `NodeResonanceRatingFormSet` | `resonance` | `resonance` as free text with autocomplete (`get_or_create`d by name on clean), `rating` 0–5 |
| `NodeMeritFlawRatingFormSet` | `merit_flaw` | `mf` chained to `rating`; the merits and flaws offered are those allowed for the `node` `ObjectType` (created if missing), and the rating choices are that merit or flaw's `ratings` |
| `RealityZonePracticeRatingFormSet` | `reality_zone` | `practice`, `rating` -5 to 5; see [reality zones](#reality-zones) |

`is_valid()` requires the form and all three formsets to be valid.

### Validation (`clean()`)

With R the rank:

1. `rank` is required.
2. The Resonance ratings must total at least R.
3. The reality zone ratings must total 0, and the positive ratings must sum to R.
4. The points left must be positive:

   ```text
   points_remaining = 3R − (total Resonance − R) − total merit/flaw rating − ratio − size
   ```

   `ratio` and `size` are their stored values (-2 to 2), so a small node or a
   Tass-heavy ratio gives points back. A result of 0 or less fails with "Node invalid:
   spend fewer points on merits/flaws, resonance, size, or ratio".

The output is then:

```text
quintessence_per_week = int(points_remaining × ratio fraction)   # 0.0, 0.25, 0.5, 0.75 or 1.0
tass_per_week         = points_remaining − quintessence_per_week
```

### Saving

`save(commit=True)` saves the node with the computed output, saves the Resonance and
merit/flaw formsets against it, links its reality zone and saves the practice ratings.
It reuses an existing zone without renaming it; otherwise it creates a neutrally named
`Reality Zone`. `commit=False` does not save the zone or its ratings.

### Views

`_NodeCreateView` ([`views/mage/node.py`](../views/mage/node.py)) is a `FormView`
that calls `prepare_created_object()` (owner and status) before `form.save()`, then
redirects to the node. The detail view adds the node's Resonance and merit/flaw
ratings, ordered by name, to the context. The template shared by all these pages is
`locations/mage/node/form_include.html`; see [templates](templates.md).

## Reality zones

Source: [`locations/models/mage/reality_zone.py`](../models/mage/reality_zone.py),
[`locations/forms/mage/reality_zone.py`](../forms/mage/reality_zone.py).

A `RealityZone` describes which practices work well or badly in a place. It is a plain
model with `name`, `description` and `practices` (M2M `characters.Practice` through
`ZoneRating`, `rating` -10 to 10). `get_positive_practices()` and
`get_negative_practices()` return the ratings above and below zero, strongest first;
`get_applied_to()` lists the nodes, Horizon realms, sanctums, demesnes and sectors that use the
zone.

`Node`, `Sanctum`, `Demesne`, `HorizonRealm` and `Sector` each have a `reality_zone`
nullable `SET_NULL` foreign key, so several places can share one zone.

### Where zones come from

`NodeForm`, `SanctumForm` and `DemesneForm` use `RealityZoneFormMixin`:

- they bind `RealityZonePracticeRatingFormSet` (prefix `reality_zone`) to the place's
  existing zone, or to a new unsaved one;
- they require the ratings to total 0 and the positive ratings to sum to the place's
  rank;
- on save they create a neutrally named zone only if needed, preserve any existing
  name, link it, and save the ratings. Editing shared ratings affects all linked places.

The practice choices exclude `SpecializedPractice` and `CorruptedPractice`. The
formset allows deleting rows.

Reality zones also have their own pages (`locations:mage:reality_zone`, list, create
and update). Standalone zones are public reference data; linked zones require
`VIEW_FULL` on every linked place, even for places with public cards. Only staff may
create or edit zones directly. List, detail, inline displays and zone form choices
enforce the same read permission. The detail view lists practices by sign and the
places returned by `get_applied_to()`.
Player-origin zones retain private classification after all their links are removed;
only staff can read those orphans. Inline editing forms enforce the same shared-zone
permission before exposing or saving practice rows, while allowing parent edits
with rank and inaccessible shared ratings read-only.

Sanctum and Demesne edit pages differ: a Sanctum edits through `SanctumForm` (with the
zone formset), while the Demesne edit page is a generated form of `name`,
`description`, `contained_within`, `size` and `accessibility` without the zone.

## See also

- [Location models](models.md)
- [Chantries](chantries.md)
- [Location forms](forms.md)
- [Location templates](templates.md)
- [Glossary](../../docs/reference/glossary.md)
