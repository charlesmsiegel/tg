# Item forms

This page covers the forms the `items` app uses: the fields of the forms the registry
generates for each type, the item-type chooser, the owner-limited edit forms, the
Wonder form shared with Mage character creation, the Vampire artifact forms and the
Sorcerer artifact chooser. It is for developers changing what an item page accepts and
for agents submitting item forms.

## Generated forms

Most item types have no form class. The registry builds a `ModelForm` from the
`fields` declared in [`items/registry.py`](../registry.py): the action's
`options["fields"]` when present, otherwise the spec's `fields`. `form_updates` then
adds placeholder attributes or help text to named fields. See
[views and URLs](views-and-urls.md#how-views-are-built) for the mechanism.

| Model | Create fields | Update fields (when different) |
|-------|---------------|--------------------------------|
| `ItemModel` | `name`, `description` | Same, or `LimitedItemEditForm` for editors without a scoped editor role |
| `Weapon`, `MeleeWeapon`, `ThrownWeapon` | `name`, `description`, `difficulty`, `damage`, `damage_type`, `conceal` | |
| `RangedWeapon` | Weapon fields plus `range`, `rate`, `clip` | |
| `Material` | `name`, `is_hard` | |
| `Medium` | `name`, `length_modifier_type`, `length_modifier` | |
| `Artifact` | `name`, `rank`, `background_cost`, `quintessence_max`, `description`, `power` | |
| `Charm` | Artifact fields plus `arete` | |
| `Talisman` | `name`, `rank`, `background_cost`, `quintessence_max`, `description`, `powers`, `arete` | |
| `Periapt` | Charm fields plus `max_charges`, `current_charges`, `is_consumable` | |
| `Grimoire` | `name`, `rank`, `background_cost`, `description`, `abilities`, `spheres`, `date_written`, `faction`, `practices`, `instruments`, `is_primer`, `language`, `length`, `cover_material`, `inner_material`, `medium`, `rotes` | Same without `background_cost` |
| `SorcererArtifact` | `name`, `rank`, `description` | |
| `Fetish`, `Talen` | `name`, `rank`, `background_cost`, `quintessence_max`, `description`, `gnosis`, `spirit` | |
| `Bloodstone` | `name`, `description`, `blood_stored`, `max_blood`, `is_active`, `created_by_generation`, `stone_type` | |
| `WraithRelic` | `name`, `description`, `level`, `rarity`, `pathos_cost` | |
| `WraithArtifact` | `name`, `description`, `level`, `artifact_type`, `material`, `corpus`, `pathos_cost` | |
| `Treasure` | `name`, `description`, `rating`, `treasure_type`, `creator`, `creation_method`, `permanence`, `special_abilities`, `glamour_storage`, `glamour_affinity` | |
| `Dross` | `name`, `description`, `quality`, `glamour_value`, `physical_form`, `color`, `source`, `is_stable`, `decay_rate`, `resonance`, `special_effects`, `restricted_to`, `is_consumable`, `recharge_method`, `container_description`, `estimated_value` | |
| `Relic` (Demon) | `name`, `description`, `relic_type`, `complexity`, `lore_used`, `power`, `material`, `house`, `is_permanent`, `difficulty`, `dice_pool` | |
| `HunterGear` | `name`, `description`, `gear_type`, `damage`, `range`, `rate`, `capacity`, `concealability`, `availability`, `legality`, `requires_training` | |
| `HunterRelic` | `name`, `description`, `power_level`, `background_cost`, `is_blessed`, `is_cursed`, `requires_faith`, `is_unique`, `powers`, `activation_cost`, `origin`, `limitations` | |
| `MummyRelic` | `name`, `description`, `rank`, `relic_type`, `era`, `original_owner`, `powers`, `ba_cost`, `associated_hekau`, `requires_sekhem`, `requires_ritual`, `is_cursed`, `is_unique`, `is_sentient`, `material`, `hieroglyphic_inscription`, `history`, `current_location_notes` | |
| `Vessel` | `name`, `description`, `rank`, `vessel_type`, `transfer_rate`, `efficiency`, `is_portable`, `requires_ritual`, `is_attuned`, `attuned_to`, `material`, `inscriptions` | Adds `current_ba` |
| `Ushabti` | `name`, `description`, `rank`, `purpose`, `physical_rating`, `mental_rating`, `special_abilities`, `material`, `size_description`, `appearance`, `command_word`, `obeys_only_creator`, `creator` | Adds `is_currently_animated`, `animation_duration_hours` |

Some of these fields are recalculated on save (for example `background_cost` on
`Fetish`, `Talen` and `MummyRelic`); see
[models](models.md#computed-fields-at-a-glance).

`Wonder` and `VampireArtifact` use form classes, described below.

Each type's form template (for example `items/mummy/vessel/form.html`) renders these
fields by name. When you add a field to the registry, add it to the template too;
[`tests/views/test_spread_forms.py`](../tests/views/test_spread_forms.py) fails when
a form field is not rendered.

## `ItemCreationForm`

Source: [`items/forms/core/item_creation.py`](../forms/core/item_creation.py).

A plain `Form` with chained selects (`widgets.ChainedSelectMixin`) used on the items
index and the public items list to pick a type to create.

| Field | Notes |
|-------|-------|
| `gameline` | `ChainedChoiceField`; choices are the `GameLine.CHOICES` that have at least one creatable type |
| `item_type` | `ChainedChoiceField` whose options depend on `gameline`; values are registry slugs, labels are `ModelSpec.menu_label` |
| `name` | Optional; not rendered by `items/index.html` |
| `rank` | Integer, initial 1, maximum 5; not rendered by `items/index.html` |

Pass the user: `ItemCreationForm(user=request.user)`. Without an authenticated user
the choices stay empty. The choices come from `registry.menu(user)`, so ordinary
players see only Mage types (see
[views and URLs](views-and-urls.md#creating-an-item-from-a-menu)). The form is
submitted with GET to `core:object_type_redirect`; it is never validated or saved.

## `LimitedItemEditForm`

Source: [`items/forms/core/limited_edit.py`](../forms/core/limited_edit.py).

A `ModelForm` on `ItemModel` with only `description`, `public_info` and `image`.
`_ItemUpdateView` gives it to editors who pass `EDIT_FULL` but lack a scoped editor
role, typically the item's owner, so they can describe the item without changing its
name or mechanics. The `image` help text notes that a new image needs storyteller
approval.

## Vampire artifact forms

Source: [`items/forms/vampire/artifact.py`](../forms/vampire/artifact.py).

| Form | Fields | Used by |
|------|--------|---------|
| `VampireArtifactForm` | `name`, `description`, `power_level` (input `min=1`, `max=5`), `background_cost` (`min=0`, `max=10`), `is_cursed`, `is_unique`, `requires_blood`, `powers`, `history` | Create for everyone; update for scoped editors |
| `LimitedVampireArtifactEditForm` | `description`, `history` | Update for other editors |

The `min`/`max` values are HTML input attributes only; the model does not constrain
these fields.

## `WonderForm`

Source: [`items/forms/mage/wonder.py`](../forms/mage/wonder.py).

`WonderForm` is a plain `Form` that creates or edits a Charm, Artifact or Talisman
together with its Resonance ratings and powers. It backs the Wonder create and edit
pages and the Wonder step of Mage, MtA human and Companion character creation
(`characters.views.mage.mage`, `mtahuman` and `companion`).

### Fields and formsets

| Field | Notes |
|-------|-------|
| `wonder_type` | `charm`, `artifact` or `talisman`; picks the class in `wonder_classes` |
| `name`, `description` | Required |
| `rank` | Required integer (its label reads "Arete") |
| `arete` | Optional integer |
| `resonance_formset` | `WonderResonanceRatingFormSet`, prefix `resonance`: an inline formset of `WonderResonanceRatingForm` rows (`resonance` as free text with autocomplete suggestions, `rating` 0–5). `clean_resonance()` `get_or_create`s the Resonance by name. |
| `effect_formset` | `characters.forms.mage.effect.EffectCreateOrSelectFormSet`, prefix `effects`: each row selects an existing `Effect` or defines a new one from Sphere ratings |

Constructor keyword arguments: `instance` (an existing Wonder to edit) and `rank`
(stored on the form, default 0). `is_valid()` requires the form and both formsets to
be valid.

### Validation rules (`clean()`)

With `rank` as R:

1. `rank` is required.
2. Charms and Talismans need `arete`, and `arete` must be at least R.
3. The Resonance ratings must total at least R.
4. A Talisman may have up to R powers; a Charm or Artifact may have one.
5. No single power may cost more than R (Charm) or 2R (Artifact, Talisman). A power's
   cost is the selected Effect's `cost()` or the sum of the Sphere ratings of a new one.
6. Extra Resonance (total minus R), plus Arete above R (Charms and Artifacts only),
   plus the cost of every power must not exceed 3R.

### Saving

`save(commit=True)` uses `instance` when given, otherwise a new object of the chosen
class, and copies `name`, `description`, `rank` and (when set) `arete`. With
`commit=True` it saves the Wonder, saves the Resonance formset against it, saves the
effect formset, then sets `power` to the first effect (Charm, Artifact) or adds every
effect to `powers` (Talisman), and saves again. It returns the Wonder.

Because the concrete class is known only after validation, `_WonderCreateView` calls
`form.save(commit=False)` to get an instance before `prepare_created_object()` runs;
see [views and URLs](views-and-urls.md#custom-views).

The template is `items/mage/wonder/form_include.html` with
[`static/items/js/wonder-form.js`](../static/items/js/wonder-form.js); see
[templates](templates.md#wonder-form).

## `ArtifactCreateOrSelectForm`

Source: [`items/forms/mage/sorcerer_artifact.py`](../forms/mage/sorcerer_artifact.py).

A `ModelForm` on `SorcererArtifact` with `widgets.CreateOrSelectMixin`: tick
`select_or_create` to create a new artifact from `name`, `rank` and `description`, or
leave it unticked and choose one in `select` (any `SorcererArtifact`). Every field is
optional; the mixin requires a selection when not creating. `save()` returns the
selected artifact or the new one. The Sorcerer character wizard
(`characters.views.mage.sorcerer`) uses it with the template
`items/mage/artifact/form_include.html`.

## See also

- [Item models](models.md)
- [Views and URLs](views-and-urls.md)
- [Item templates](templates.md)
- [Character creation](../../docs/architecture/character-creation.md)
- [widgets app](../../widgets/README.md)
