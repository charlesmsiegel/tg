# Item models

This page describes every model in the `items` app, grouped by gameline: what each one
represents, its fields, the values it computes and the rules it enforces. It is for
developers changing item models and for agents that need to read or write item data.
For the registry entry, URLs and forms of each type, see
[views and URLs](views-and-urls.md) and [forms](forms.md).

## The base: `ItemModel`

Source: [`items/models/core/item.py`](../models/core/item.py).

`ItemModel` extends `core.models.Model` (a django-polymorphic model, see the
[data model overview](../../docs/architecture/data-model.md)) and `RegistryURLMixin`.
Every item therefore inherits:

| Inherited from `core.models.Model` | Notes |
|------|-------|
| `name`, `description`, `public_info`, `st_notes` | `name` is required; `Model.clean()` rejects a blank name |
| `owner` (User), `chronicle` (`game.Chronicle`) | Both nullable, `SET_NULL` |
| `status` | `CharacterStatus` codes (`Un`, `Sub`, `App`, `Rev`, `Ret`, `Dec`), default `Un` |
| `visibility` | `PUB`, `PRI`, `CHR`, `CUS`; default `PRI` |
| `image`, `image_status` | Images need approval before the public views show them |
| `sources` | M2M to `core.BookReference`; add with `add_source(book_title, page_number)` |
| `display`, `freebies_approved`, `observers` | Shared with every `core.Model` |

`core.models.Model.save()` calls `full_clean()` unless you pass
`skip_validation=True`, so field validators, `CheckConstraint`s and each model's
`clean()` run on every save, including saves from data scripts.

`ItemModel` adds:

| Field | Type | Meaning |
|-------|------|---------|
| `owned_by` | M2M `characters.CharacterModel` | Characters who hold the item (reverse accessor `itemmodel_set`) |
| `located_at` | M2M `locations.LocationModel` | Places where the item is kept (reverse accessor `itemmodel_set`) |

`owned_by_list()` returns `list(self.owned_by.all())`. The class attribute
`type = "item"`; `gameline` is inherited as `"wod"`.

The manager is `ItemModelManager`, built from `core.models.ModelManager` with an
`ItemQuerySet` that adds nothing of its own, so all `ModelQuerySet` helpers
(`visible()`, `for_chronicle()`, `owned_by()` and so on) are available.

### URL methods

`RegistryURLMixin` ([`core/registry_urls.py`](../../core/registry_urls.py)) gives every
registered model `get_absolute_url()`, `get_update_url()` and the classmethod
`get_creation_url()`. Each looks up the model's entry in
[`items/registry.py`](../registry.py) and reverses the URL name in its `model_urls`.
For most item types `get_absolute_url()` returns the polymorphic router
`items:item` (`/items/<pk>/`); see [views and URLs](views-and-urls.md#polymorphic-detail-routing).

### `type` and `gameline`

Each subclass sets two class attributes:

- `gameline`: the gameline code (`vtm`, `wta`, `mta`, `wto`, `ctd`, `dtf`, `mtr`,
  `htr`, or the inherited `wod`). `get_gameline()` reads it; templates use it for
  theming.
- `type`: a short string used for display (`get_type()`) and for grouping on the staff
  index. It is **not unique**: `WraithArtifact.type` and the Mage `Artifact.type` are
  both `"artifact"`, and `WraithRelic.type` and the Demon `Relic.type` are both
  `"relic"`. Use the registry slug (for example `wraith_artifact`) when you need a
  unique key.

## Class hierarchy

```text
core.models.Model
└── ItemModel                         (wod)
    ├── Weapon                        (wod)
    │   ├── MeleeWeapon
    │   ├── RangedWeapon
    │   └── ThrownWeapon
    ├── Wonder                        (mta)
    │   ├── Artifact
    │   ├── Charm
    │   ├── Periapt
    │   ├── Talisman
    │   ├── Grimoire
    │   ├── Fetish                    (wta)
    │   └── Talen                     (wta)
    ├── SorcererArtifact              (mta)
    ├── VampireArtifact, Bloodstone   (vtm)
    ├── Treasure, Dross               (ctd)
    ├── Relic                         (dtf)
    ├── HunterGear, HunterRelic       (htr)
    ├── MummyRelic, Vessel, Ushabti   (mtr)
    └── WraithArtifact, WraithRelic   (wto)

django.db.models.Model
├── Material                          (reference data)
├── Medium                            (reference data)
├── WonderResonanceRating             (through model)
└── RelicResonanceRating              (through model)
```

Fetish and Talen are Wonders (they inherit `rank`, `background_cost`,
`quintessence_max` and Resonance) but override `gameline` to `wta`.

## Generic (World of Darkness) items

Source: [`items/models/core/`](../models/core/).

### Weapons

| Model | `type` | Fields |
|-------|--------|--------|
| `Weapon` | `weapon` | `difficulty` (int, 0), `damage` (int, 0), `damage_type` (`B` Bashing, `L` Lethal, `A` Aggravated; default `L`), `conceal` (`P` Pocket, `J` Jacket, `T` Trenchcoat, `N` Not Applicable; default `P`) |
| `MeleeWeapon` | `melee_weapon` | Adds nothing |
| `ThrownWeapon` | `thrown_weapon` | Adds nothing |
| `RangedWeapon` | `ranged_weapon` | Adds `range`, `rate`, `clip` (ints, default 0) |

### Reference data: `Material` and `Medium`

These are plain Django models, not `ItemModel` subclasses. They have no owner, status
or visibility, and their registry actions use the `PUBLIC_READ` and `STAFF_WRITE`
policies.

| Model | Fields | Used by |
|-------|--------|---------|
| `Material` | `name` (text), `is_hard` (bool, default `True`) | `Grimoire.cover_material` / `inner_material`; `MageFaction.materials` |
| `Medium` | `name` (text), `length_modifier_type` (one character, default `"/"`), `length_modifier` (int, default 1) | `Grimoire.medium`; `MageFaction.media`; `Grimoire.random_length()` applies the modifier (`/`, `+`, `*` or `-`) to a random page count |

Both get their URL methods from `RegistryURLMixin` and so resolve to
`items:material` and `items:medium`.

## Mage: the Ascension (`mta`)

Source: [`items/models/mage/`](../models/mage/).

### `Wonder` and `WonderResonanceRating`

`Wonder` (`type = "wonder"`) is the base of every Mage magical item.

| Field | Type | Rule |
|-------|------|------|
| `rank` | int | 0–10 (validators and `CheckConstraint`) |
| `background_cost` | int | 0–10 |
| `quintessence_max` | int | 0–100 |
| `resonance` | M2M `characters.Resonance` through `WonderResonanceRating` | |

`WonderResonanceRating` has `wonder` and `resonance` foreign keys (both `SET_NULL`)
and a `rating` constrained to 0–10.

Methods:

- `add_resonance(resonance)` accepts a `Resonance` or a name (a name is
  `get_or_create`d), creates the rating row if needed and raises it by one. It returns
  `False` without changing anything when the rating is already 5.
- `resonance_rating(resonance)`, `total_resonance()`, `filter_resonance(minimum,
  maximum)`.
- `has_resonance()` is true when the total Resonance is at least `rank`.
- `set_rank()` / `has_rank()` (non-zero).

### Wonder subclasses

| Model | `type` | Adds | Behaviour |
|-------|--------|------|-----------|
| `Artifact` | `artifact` | `power` (FK `characters.Effect`) | `set_power()` saves; `has_power()` |
| `Charm` | `charm` | `arete` (int), `power` (FK Effect) | `set_power()` does not save |
| `Talisman` | `talisman` | `arete` (int), `powers` (M2M Effect) | `add_power()`; `has_powers()` is true when the number of powers equals `rank` |
| `Periapt` | `periapt` | `arete` (0–10), `power` (FK Effect), `max_charges` (1–100, default 1), `current_charges` (0–100, default 1), `is_consumable` (default `True`) | See below |
| `Grimoire` | `grimoire` | See [Grimoire](#grimoire) | |

`Periapt.clean()` raises non-field errors when `arete < rank` (code
`arete_below_rank`) or `current_charges > max_charges` (code `charges_exceed_max`).
Because `save()` runs `full_clean()`, these rules hold for every save.
`use_charge()` decrements and saves (returns `False` at zero), `recharge(amount=1)`
raises the charges up to `max_charges` and saves, and `is_depleted()` /
`charges_remaining()` read the count.

### Grimoire

A `Grimoire` is a Wonder that is a book of magical teaching.

| Field | Type |
|-------|------|
| `abilities` | M2M `characters.Ability` |
| `spheres` | M2M `characters.Sphere` |
| `practices`, `instruments` | M2M `characters.Practice`, `characters.Instrument` |
| `rotes` | M2M `characters.Rote` |
| `faction` | FK `characters.MageFaction` |
| `language` | FK `core.Language` |
| `cover_material`, `inner_material` | FK `Material` (related names `is_cover`, `is_inner`) |
| `medium` | FK `Medium` |
| `date_written` | int, default `-5000` (the "unset" sentinel for `has_date_written()`) |
| `is_primer` | bool |
| `length` | int (pages) |

**Contents rule.** `has_rotes()` is true when
`rotes + practices + spheres + abilities (+ 1 if is_primer) == rank + 3`. The detail
view renders the same rule as a contents strip; see
[views and URLs](views-and-urls.md#custom-views).

`set_rank()` clamps the rank to 1–5, although the field allows 0–10.

**Random generation.** `Grimoire.random(**overrides)` fills every property and saves.
Each keyword argument (`rank`, `is_primer`, `faction`, `practices`, `instruments`,
`date_written`, `medium`, `cover_material`, `inner_material`, `length`, `language`,
`abilities`, `spheres`, `rotes`) fixes that property; the rest are rolled by the
matching `random_*` method, in this order: rank, primer flag, faction, medium,
materials, length, focus (practices and instruments), date, abilities, language,
spheres, rotes, name. It sets `status` to `Sub`, `background_cost = 2 * rank` and
`quintessence_max = 5 * rank`. `random_rotes()` creates new `Rote` rows from matching
`Effect`s and calls `Rote.random(book=self)` on each. `locations.Library.random_book()`
uses this to stock libraries.

### `SorcererArtifact`

`SorcererArtifact` (`type = "sorcerer_artifact"`, verbose name "Artifact
(Sorcerer)") is a direct `ItemModel` subclass with a single `rank` field. It is the
item behind the Sorcerer's Artifact background; see
[forms](forms.md#artifactcreateorselectform).

## Werewolf: the Apocalypse (`wta`)

Source: [`items/models/werewolf/`](../models/werewolf/).

| Model | `type` | Adds | Behaviour |
|-------|--------|------|-----------|
| `Fetish` | `fetish` | `gnosis` (int), `spirit` (text, 100 chars) | `save()` sets `background_cost = rank` |
| `Talen` | `talen` | `gnosis` (int), `spirit` (text, 200 chars) | `save()` sets `background_cost = rank` |

Both inherit the Wonder fields and Resonance methods.
`characters` Garou, Fera and Kinfolk models import `Fetish` for their fetish
backgrounds.

## Vampire: the Masquerade (`vtm`)

Source: [`items/models/vampire/`](../models/vampire/).

| Model | `type` | Fields |
|-------|--------|--------|
| `VampireArtifact` | `vampire_artifact` | `power_level` (int, default 1, help text says 1–5 but nothing enforces it), `background_cost`, `is_cursed`, `is_unique`, `requires_blood`, `powers` (text), `history` (text) |
| `Bloodstone` | `bloodstone` | `blood_stored` (0), `max_blood` (10), `is_active` (`True`), `created_by_generation` (13), `stone_type` |

`Bloodstone.add_blood(amount)` and `remove_blood(amount)` change `blood_stored` in
memory and return `True`, or return `False` when the stone is inactive, the result
would exceed `max_blood`, or not enough blood is stored. Neither saves.

## Wraith: the Oblivion (`wto`)

Source: [`items/models/wraith/`](../models/wraith/).

| Model | `type` | Fields | Behaviour |
|-------|--------|--------|-----------|
| `WraithArtifact` | `artifact` | `level` (1), `background_cost`, `artifact_type` (`soulforged`, `skin`, `spectre`, `other`), `material` (`soulsteel`, `stygian_steel`, `necropolis_steel`, `ash_iron`, `labyrinthine_adamas`), `corpus`, `pathos_cost` | `save()` sets `background_cost = level` |
| `WraithRelic` | `relic` | `level` (1), `background_cost`, `rarity` (`common` … `legendary`), `pathos_cost` | `save()` sets `background_cost = level` |

Both have `set_level(level)` (also sets `background_cost`) and `has_level()`.

## Changeling: the Dreaming (`ctd`)

Source: [`items/models/changeling/`](../models/changeling/).

### `Treasure`

| Field | Rule |
|-------|------|
| `rating` | 1–5 (choices, validators and a `CheckConstraint`) |
| `treasure_type` | `weapon`, `armor`, `talisman`, `wonder`, `other`, or blank |
| `creator`, `creation_method`, `permanence` | Text, text, bool (default `True`) |
| `effects` | JSON list; `special_abilities` (text) |
| `glamour_storage` | 0–50 |
| `glamour_affinity` | Text |

`str()` shows the name followed by one star per rating dot.

### `Dross`

Crystallised Glamour. `glamour_value` is 1–10 (validators and a `CheckConstraint`).
Other fields: `quality` (`ephemeral`, `common`, `fine`, `exquisite`, `legendary`),
`physical_form`, `color`, `source`, `is_stable`, `decay_rate`, `resonance` (a text
field, not the Mage `Resonance` model), `special_effects`, `restricted_to`,
`is_consumable`, `recharge_method`, `container_description`, `estimated_value`.
`get_quality_multiplier()` maps the quality to 0.5, 1, 2, 4 or 10. `str()` falls back
to "<Quality> Dross (N Glamour)" when the name is empty.

## Demon: the Fallen (`dtf`)

Source: [`items/models/demon/relic.py`](../models/demon/relic.py).

`Relic` (`type = "relic"`, ordered by name):

| Field | Meaning |
|-------|---------|
| `relic_type` | `enhanced` (default), `enchanted`, `house_specific`, `demonic`, `ancient` |
| `complexity` | int, default 1 |
| `lore_used`, `power`, `material` | Text |
| `house` | FK `characters.DemonHouse` (related name `relics`) |
| `is_permanent` | bool |
| `difficulty` | int, default 6 |
| `dice_pool` | int |

`set_complexity(n)` accepts 1–10 and saves; `set_difficulty(n)` accepts 2 or more and
saves. Both return `False` and change nothing for other values.

## Hunter: the Reckoning (`htr`)

Source: [`items/models/hunter/`](../models/hunter/).

| Model | `type` | Fields |
|-------|--------|--------|
| `HunterGear` | `hunter_gear` | `gear_type` (`weapon`, `armor`, `surveillance`, `medical`, `occult`, `transportation`, `communication`, `utility`), `damage`, `range`, `rate`, `capacity`, `concealability` (all text), `availability` (int), `legality` (`legal`, `restricted`, `illegal`), `requires_training` |
| `HunterRelic` | `hunter_relic` | `power_level`, `background_cost`, `is_blessed`, `is_cursed`, `requires_faith`, `is_unique`, `powers`, `activation_cost`, `origin`, `limitations` |

Neither has behaviour beyond the base class.

## Mummy: the Resurrection (`mtr`)

Source: [`items/models/mummy/`](../models/mummy/).

### `MummyRelic` and `RelicResonanceRating`

`MummyRelic` (`type = "mummy_relic"`): `rank` 1–10, `background_cost` 1–10,
`relic_type`, `era`, `original_owner`, `powers`, `ba_cost` 0–20, `associated_hekau`,
`requires_sekhem` 0–10, `requires_ritual`, `is_cursed`, `is_unique`, `is_sentient`,
`material` (text), `hieroglyphic_inscription`, `history`, `current_location_notes`,
and `resonance` (M2M `characters.Resonance` through `RelicResonanceRating`).

- `save()` sets `background_cost = rank`.
- `can_activate(mummy)` is false when `requires_sekhem > mummy.sekhem` or
  `ba_cost > mummy.ba`.

`RelicResonanceRating` has `relic` and `resonance` foreign keys (both `CASCADE`), a
`rating` defaulting to 1 (0–10), and `unique_together = (relic, resonance)`.

### `Vessel`

A store of Ba. Fields: `rank` 1–10, `background_cost`, `max_ba` 1–100, `current_ba`
0–100, `vessel_type`, `transfer_rate` 1–10, `efficiency` 50–100 (percent),
`is_portable`, `requires_ritual`, `is_attuned`, `attuned_to` (FK `characters.Mummy`,
related name `attuned_vessels`), `material`, `inscriptions`.

- `save()` sets `max_ba = rank * 10`, `background_cost = rank`, and clamps
  `current_ba` to `max_ba`. Any `max_ba` you set yourself is overwritten.
- `store_ba(amount)` stores `min(amount, transfer_rate, free space)` scaled by
  `efficiency`, saves, and returns the amount stored.
- `withdraw_ba(amount)` removes `min(amount, transfer_rate, current_ba)`, saves, and
  returns it.
- `is_full()`, `is_empty()`, `can_use(mummy)` (false when attuned to someone else).

### `Ushabti`

An animated servant statue. Fields: `rank` 1–5, `is_currently_animated`,
`ba_to_animate`, `ba_per_day`, `animation_duration_hours` (at least 1), `purpose`,
`physical_rating` 1–5, `mental_rating` 1–5, `special_abilities`, `material` (choice:
clay, wood, stone, gold, bone, wax), `size_description`, `appearance`,
`command_word`, `obeys_only_creator`, `creator` (FK `characters.Mummy`, related name
`created_ushabti`).

- `save()` sets `ba_to_animate` and `ba_per_day` to `rank`.
- `animate(mummy)` returns `(False, message)` when the ushabti only obeys its creator
  and `mummy` is someone else, or when `mummy.ba < ba_to_animate`. Otherwise it calls
  `mummy.spend_ba(ba_to_animate)`, marks the ushabti animated, saves, and returns
  `(True, message)`.
- `deactivate()` clears the flag and saves.

## Computed fields at a glance

Several models overwrite fields in `save()`. Forms that expose these fields cannot set
them.

| Model | Field overwritten on save | Value |
|-------|---------------------------|-------|
| `Fetish`, `Talen` | `background_cost` | `rank` |
| `WraithArtifact`, `WraithRelic` | `background_cost` | `level` |
| `MummyRelic` | `background_cost` | `rank` |
| `Vessel` | `max_ba`, `background_cost`, `current_ba` | `rank * 10`, `rank`, clamped to `max_ba` |
| `Ushabti` | `ba_to_animate`, `ba_per_day` | `rank` |

## See also

- [Views and URLs](views-and-urls.md)
- [Forms](forms.md)
- [Data model overview](../../docs/architecture/data-model.md)
- [Adding an item or location type](../../docs/guides/adding-an-item-or-location-type.md)
- [Glossary](../../docs/reference/glossary.md)
