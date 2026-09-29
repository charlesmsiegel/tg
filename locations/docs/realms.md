# Horizon and Paradox realms

This page covers the two Mage realm models: `HorizonRealm`, a pocket realm bought with
build points, and its subclass `ParadoxRealm`, a realm a mage is pulled into by
Paradox, which can be generated at random from dice tables. It is for developers
working on realm rules and for agents creating realms.

## `HorizonRealm`

Source: [`locations/models/mage/realm.py`](../models/mage/realm.py).

`HorizonRealm` (`type = "horizon_realm"`, `gameline = "mta"`) extends
`MeritFlawBlock` and `LocationModel`.

| Field | Range | Meaning |
|-------|-------|---------|
| `rank` | 1–10 | Realm rating |
| `build_points` | 0–200, default 11 | Points available to buy features |
| `base_maintenance`, `quintessence_maintenance` | 0–100 | Upkeep |
| `primary_earthly_connection` | text | |
| `size` | `SizeChoices` 1–6, default 1 | A single room … An entire world |
| `environment` | `EnvironmentChoices` 1–6, default 1 | Same as the primary Earthly connection … Anything is possible |
| `access_points` | 0–20, default 1 | |
| `plants`, `animals`, `people`, `ephemera` | 0–5 | Inhabitants |
| `guardians` | 0–10 | Security |
| `arcane` | 0–5 | Security |
| `resonance` | M2M `characters.Resonance` through `HorizonRealmResonanceRating` (0–10) | |
| `merits_and_flaws` | M2M `characters.MeritFlaw` through `HorizonRealmMeritFlawRating` (-10 to 10) | |
| `reality_zone` | FK `RealityZone` | See [reality zones](nodes.md#reality-zones) |

The ranges are enforced by validators and `CheckConstraint`s.

### Build point rules

`set_rank(rank)` sets the rank and, from the class tables, the build points and base
maintenance (and copies base maintenance into `quintessence_maintenance`):

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|------|---|---|---|---|---|---|---|---|---|----|
| `RANK_BUILD_POINTS` | 11 | 22 | 33 | 44 | 55 | 70 | 85 | 100 | 115 | 150 |
| `RANK_BASE_MAINTENANCE` | 1 | 2 | 3 | 4 | 5 | 10 | 15 | 20 | 25 | 50 |

Costs:

| Method | Formula |
|--------|---------|
| `structure_cost()` | `size × 5 + environment × 3 + max(0, access_points − 1) × 2` |
| `inhabitants_cost()` | `plants × 2 + animals × 2 + people × 5 + ephemera × 4` |
| `security_cost()` | `guardians × 3 + arcane × 2` |
| `total_cost()` | The sum of the three |
| `remaining_points()` | `build_points − total_cost()` |

None of these are enforced on save; they are helpers for display and validation.
Resonance helpers mirror the node's: `add_resonance()` (up to 5 per Resonance),
`resonance_rating()`, `total_resonance()`, and `has_resonance()` (total at least
`rank`). `filter_mf(minimum, maximum)` narrows the available merits and flaws.

### Pages

The Horizon realm pages use the generated registry form, which exposes only `name`,
`description` and `contained_within`. Create is at `/locations/mage/create/realm/`
(`locations:mage:create:horizon_realm`); the build fields keep their defaults unless
set another way (admin, shell or data script).

## `ParadoxRealm`

Source: [`locations/models/mage/paradox_realm.py`](../models/mage/paradox_realm.py).

`ParadoxRealm` (`type = "paradox_realm"`) is a multi-table subclass of `HorizonRealm`,
so it has every Horizon realm field as well as its own:

| Field | Meaning |
|-------|---------|
| `primary_sphere`, `secondary_sphere` | `SphereChoices` (the nine Spheres); the secondary is optional |
| `paradigm`, `secondary_paradigm` | `ParadigmChoices` (14 paradigms, default `antimagick`); the secondary is optional |
| `atmosphere_details` | JSON list |
| `num_primary_obstacles`, `num_random_obstacles` | Obstacle counts |
| `final_obstacle_type` | `FinalObstacleTypeChoices`: give a secret, win a game, solve a riddle, button, maze, abnormal maze, silver bullet, guess the name, random sphere, combined |
| `final_obstacle_details` | JSON object |

Related rows:

| Model | Fields | Access |
|-------|--------|--------|
| `ParadoxObstacle` | `realm` (CASCADE, related name `realm_obstacles`), `sphere`, `obstacle_number` (1–10), `order`, `name`, `description`; ordered by `order` | `realm.get_obstacles()` |
| `ParadoxAtmosphere` | `realm` (CASCADE, related name `realm_atmospheres`), `paradigm`, `atmosphere_number` (1–10), `description` | `realm.get_atmosphere_elements()` |

### Random generation

`ParadoxRealm.random(name="Random Paradox Realm", save=False)` follows the guide's
tables. The dice helpers are static methods: `roll_d10()`, `roll_d5()` (a d10 halved,
rounded up), `roll_2d10()` and `roll_d100()`.

1. **Sphere (Table B1, `random_sphere()`)**: a d10 picks one of the nine Spheres in
   `SphereChoices` order; a 10 means two Spheres, so the method rerolls until it has a
   primary and a different secondary.
2. **Paradigm (Table B2, `random_paradigm()`)**: 2d10. Totals 2–13 map to fixed
   paradigms; 14–16 pick a random paradigm other than Unstable (standing in for "the
   character's paradigm"); 17–19 give Antimagick; 20 means two different paradigms,
   rolled again.
3. **Obstacle count (Table B3, `random_obstacle_count()`)**: a d10 returns
   `(primary, random)` counts; on a 10 both are d5 rolls, capped so they total at most
   six.
4. **Final obstacle (Table B4, `random_final_obstacle()`)**: a d10; a 10 gives
   `combined`.

The method builds the realm unsaved. With `save=True` it also saves the realm, then
creates two or three `ParadoxAtmosphere` rows for the primary paradigm, one
`ParadoxObstacle` per primary obstacle in the primary Sphere, and one per random
obstacle in a freshly rolled Sphere, numbered in order.

Obstacle names come from `ParadoxObstacle.get_obstacle_name(sphere, roll)` and
atmosphere text from `ParadoxAtmosphere.get_atmosphere_description(paradigm, roll)`.
Both tables are abbreviated; a missing entry falls back to a generic label such as
"forces Obstacle 4".

The paradigm map has an entry for a total of 1 (Unstable), which 2d10 never rolls, so
`random()` never produces an Unstable realm.

### `ParadoxRealmForm`

Source: [`locations/forms/mage/paradox_realm.py`](../forms/mage/paradox_realm.py).

Fields: `name`, `description`, the Sphere and paradigm fields, the obstacle counts,
`final_obstacle_type`, `final_obstacle_details`, `contained_within` (optional), the
three barriers, and `generate_random` (a checkbox that is not a model field). It
carries two inline formsets: `ParadoxObstacleFormSet` (prefix `obstacles`) and
`ParadoxAtmosphereFormSet` (prefix `atmospheres`), both allowing deletion.

- Without `generate_random`, `is_valid()` also validates both formsets, and
  `save(commit=True)` saves the realm and both formsets.
- With `generate_random`, the formsets are not validated and `save()` returns
  `ParadoxRealm.random(name=<the name entered>, save=commit)`: a new realm with
  generated obstacles and atmospheres. The form's bound instance is not the object
  returned.

### Views

| View | Behaviour |
|------|-----------|
| `_ParadoxRealmDetailView` | Adds `obstacles` (by order) and `atmospheres` to the context |
| `_ParadoxRealmCreateView` | `FormView`: `prepare_created_object()`, `form.save()`, redirect to the realm |
| `_ParadoxRealmUpdateView` | `FormView` with `EditPermissionMixin`; binds the form to the realm; policy `OBJECT_ACTION` (requires `EDIT_FULL`) |

All are in [`views/mage/paradox_realm.py`](../views/mage/paradox_realm.py).

## See also

- [Location models](models.md)
- [Nodes and reality zones](nodes.md)
- [Location forms](forms.md)
- [Views and URLs](views-and-urls.md)
- [Glossary](../../docs/reference/glossary.md)
