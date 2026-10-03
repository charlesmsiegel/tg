# Location models

This page describes every model in the `locations` app, grouped by gameline: what each
represents, its fields, the values it computes and the rules it enforces. It is for
developers changing location models and for agents reading or writing location data.
The Mage chantry, node, realm and Changeling freehold models have their own pages with
the full rules: [chantries](chantries.md), [nodes](nodes.md), [realms](realms.md) and
[freeholds](freeholds.md).

## The base: `LocationModel`

Source: [`locations/models/core/location.py`](../models/core/location.py).

`LocationModel` extends `core.models.Model` (a django-polymorphic model, see the
[data model overview](../../docs/architecture/data-model.md)) and `RegistryURLMixin`.
It inherits `name`, `owner`, `chronicle`, `status`, `visibility`, `sources`,
`description`, `public_info`, `image`, `image_status`, `st_notes` and the other
`core.Model` fields. `core.models.Model.save()` calls `full_clean()` unless you pass
`skip_validation=True`, so validators, constraints and `clean()` run on every save.

`LocationModel` adds:

| Field | Type | Meaning |
|-------|------|---------|
| `contained_within` | M2M to `LocationModel`, related name `contains` | The places this one sits inside; a place may have several containers |
| `parent` | FK to `LocationModel`, related name `children` | A single parent link. `core.services.chronicle_data` uses it to pick root locations and some admin lists show it; the staff index and the detail page's "Located in" use `contained_within` |
| `owned_by` | FK `characters.CharacterModel` | The character who holds the place (reverse accessor `locationmodel_set`) |
| `gauntlet` | int, default 7 | 0–10 |
| `shroud` | int, default 7 | 0–10 |
| `dimension_barrier` | int, default 6 | 0–10 |
| `creation_status` | int, default 1 | Step counter for the creation wizards (chantry, freehold); must not be negative |

`clean()` enforces the 0–10 ranges and the non-negative `creation_status`.

Methods:

- `get_scenes()` returns the `game.Scene` rows whose `location` is this place.
- `containment_chains(max_depth=10)` returns one chain per direct container, innermost
  first. Each chain follows the first container of every step and stops at a top-level
  place, at `max_depth`, or when the graph loops back.
- `owned_by_list()` returns `[owned_by]` or `[]`.

The manager is `LocationModelManager`: `core.models.ModelManager` with a
`LocationQuerySet` that adds `top_level()` (places with no container).

`type = "location"`; `gameline` is inherited as `"wod"`. As with items, the `type`
string is for display and grouping; the registry slug is the unique key. For URL
methods (`get_absolute_url()` and friends) see
[views and URLs](views-and-urls.md#polymorphic-detail-routing).

## Class hierarchy

```text
core.models.Model
└── LocationModel                                   (wod)
    ├── City                                        (wod)
    ├── Haven, Domain, Elysium, Rack,
    │   TremereChantry, Barrens                     (vtm)
    ├── Caern                                       (wta)
    ├── Chantry, Node, Library, Sanctum,
    │   Demesne, Sector                             (mta)
    ├── HorizonRealm                                (mta)
    │   └── ParadoxRealm                            (mta)
    ├── Freehold, Holding, Trod, DreamRealm         (ctd)
    ├── Haunt, Necropolis, Citadel, Byway,
    │   Nihil, WraithFreehold                       (wto)
    ├── Bastion, Reliquary                          (dtf)
    ├── HuntingGround, Safehouse                    (htr)
    └── Tomb, CultTemple, UndergroundSanctuary      (mtr)

django.db.models.Model
├── RealityZone, ZoneRating                         (Mage reference data)
├── ParadoxObstacle, ParadoxAtmosphere              (children of ParadoxRealm)
└── rating through models (NodeResonanceRating, HavenMeritFlawRating, ...)
```

## Generic: `City`

Source: [`locations/models/core/city.py`](../models/core/city.py).

`City` (`type = "city"`) adds `population` (int), `characters` (M2M
`characters.Character`), and free-text `mood`, `theme`, `media` and `politicians`.
`add_character(character)` adds to `characters` and saves.

## Vampire: the Masquerade (`vtm`)

Source: [`locations/models/vampire/`](../models/vampire/).

| Model | `type` | Main fields | Computed |
|-------|--------|-------------|----------|
| `Haven` | `haven` | `size` (1–5, `HavenSizeChoices`: Cramped … Luxurious), `security`, `location`, flags `has_guardian`, `has_luxury`, `is_hidden`, `has_library`, `has_workshop`; `merits_and_flaws` through `HavenMeritFlawRating` | `save()` sets `total_rating = size + security + location + 1 per flag` |
| `Domain` | `domain` | `size`, `population`, `control`, `is_elysium`, `has_rack`, `is_disputed`, `domain_type` | `save()` sets `total_rating = size + population + control (+1 has_rack, -1 is_disputed)`, minimum 0 |
| `Elysium` | `elysium` | `prestige`, `keeper_name`, `elysium_type`, `is_protected`, `allows_weapons`, `has_blood_dolls`, `has_art_collection`, `has_library`, `is_court` | |
| `Rack` | `rack` | `quality`, `population_density`, `risk_level` (default 3), `rack_type`, `blood_quality`, `is_protected`, `is_exclusive`, `is_contested`, `masquerade_risk` | `get_total_value()`: `quality + population_density - (risk_level - 3)`, +1 protected, +1 exclusive, -1 contested, minimum 0 (not stored) |
| `TremereChantry` | `tremere_chantry` | `size`, `security_level`, `library_rating`, `ritual_rooms`, `blood_vault_capacity`, `regent_name`, `resident_count`, `apprentice_count`, `has_wards`, `has_sanctum`, `has_blood_forge`, `has_scrying_chamber`, `has_gargoyle_guardians`, `pyramid_level`, `reports_to` | `save()` sets `total_rating = size + security_level + library_rating`, +2 sanctum, +1 for each other feature flag |
| `Barrens` | `barrens` | `size`, `danger_level`, `population_density`, control flags (`is_contested`, `is_anarch_territory`, `is_sabbat_territory`, `is_unclaimed`, `controlling_faction`), resource flags, `masquerade_threat`, activity flags, `barrens_type`, `notable_locations` | `get_control_status()` returns the first that applies: Unclaimed, Anarch, Sabbat, Contested, `controlling_faction`, Unknown |

`HavenMeritFlawRating` links a haven to a `characters.MeritFlaw` with a rating of
-10 to 10, unique per `(haven, mf)`.

`TremereChantry` is unrelated to the Mage `Chantry`.

## Werewolf: the Apocalypse (`wta`)

Source: [`locations/models/werewolf/caern.py`](../models/werewolf/caern.py).

`Caern` (`type = "caern"`): `rank` (int) and `caern_type` (`enigmas`, `gnosis`,
`healing`, `leadership`, `rage`, `stamina`, `strength`, `urban`, `visions`, `will`,
`wisdom`, `wyld`). `save()` sets `gauntlet` from `rank`: 4 below rank 3, 3 for ranks
3–4, 2 from rank 5. The guard skips this only when `gauntlet` is passed as a keyword to
`save()`, so in practice the gauntlet always follows the rank.

## Mage: the Ascension (`mta`)

Source: [`locations/models/mage/`](../models/mage/).

| Model | `type` | Summary | Details |
|-------|--------|---------|---------|
| `Chantry` | `chantry` | A Mage stronghold bought with points spent on backgrounds and Integrated Effects | [chantries](chantries.md) |
| `Node` | `node` | A place of power producing Quintessence and Tass | [nodes](nodes.md) |
| `HorizonRealm` | `horizon_realm` | A pocket realm built from build points | [realms](realms.md) |
| `ParadoxRealm` | `paradox_realm` | A `HorizonRealm` subclass generated from Paradox tables | [realms](realms.md) |
| `Library` | `library` | A collection of grimoires | Below |
| `Sanctum` | `sanctum` | A mage's personal workspace with a reality zone | Below |
| `Demesne` | `demesne` | A mental realm with a reality zone | Below |
| `Sector` | `sector` | A Digital Web sector | Below |

### `Library`

Fields: `rank` (default 1), `faction` (FK `characters.MageFaction`), `books` (M2M
`items.Grimoire`).

- `add_book(grimoire)` adds and saves; `num_books()` counts books.
- `set_rank(rank)` saves.
- `increase_rank(book=None)` raises `rank` by one and adds `book`, or a random book
  when `book` is `None` or already held.
- `random_book()` creates a `Grimoire` owned by the library's owner and chronicle
  (and held by `owned_by`, when set), rolls a rank between 1 and the library's rank,
  picks the library's faction or, half the time, one of its child factions, calls
  `Grimoire.random()` and adds the book.

`Chantry.chantry_library` points at a `Library` (reverse accessor `chantry`).

### `Sanctum` and `Demesne`

| Model | Fields |
|-------|--------|
| `Sanctum` | `rank`, `reality_zone` (FK `RealityZone`) |
| `Demesne` | `rank`, `reality_zone`, `size` (text), `accessibility` (`easy`, `moderate`, `difficult`, `private`) |

Their forms create and maintain the reality zone; see
[nodes](nodes.md#reality-zones).

### `Sector`

A Digital Web sector. Fields cover classification (`sector_class`: `virgin`, `grid`,
`c_sector`, `corrupted`, `junklands`, `haunts`, `trash`, `streamland`, `warzone`),
access (`access_level` `free` or `restricted`, `requires_password`, `password_hint`,
`approved_users`), reality (`power_rating` default 5, `security_level`, `constraints`,
`reality_zone`, `difficulty_modifier`, `paradox_risk_modifier`, `is_reformattable`,
`corruption_level`), time (`time_dilation` decimal default 1.0,
`temporal_instability`), data (`aro_count`, `aro_density`, `data_flow_rate`,
`estimated_users`), `connected_sectors` (non-symmetrical M2M to other sectors, reverse accessor `conduits_from`), `hazards` and
`notable_features`.

Rules helpers (none of them save):

| Method | Returns |
|--------|---------|
| `get_effective_difficulty(paradigm_match=True)` | 6, plus `difficulty_modifier` when a reality zone is set, plus 1 when the paradigm does not match and `constraints` is set; clamped to 3–10 |
| `generates_paradox_for_power(level)` | How far `level` exceeds `power_rating`, or 0 |
| `is_accessible_to(user_credentials=None)` | `True` for free sectors; for restricted ones, whether any line of `approved_users` appears in the credentials |
| `get_whiteout_risk(pool)` | `critical` (11+), `high` (6+), `moderate` (3+), `low` |
| `calculate_base_paradox(is_vulgar=False, has_witnesses=False)` | 1 for a vulgar effect with witnesses or in a restricted sector, plus `paradox_risk_modifier`, plus 1 in a corrupted sector |
| `get_navigation_difficulty()` | 6, +2 restricted, + up to 2 for security, +1 corrupted or junklands; at most 10 |
| `get_de_rez_type(violation_severity="minor")` | `hard` or `soft` |
| `time_in_sector(minutes)` | `minutes * time_dilation` |

### `RealityZone` and `ZoneRating`

`RealityZone` is a plain Django model (not a location) with `name`, `description` and
`practices` (M2M `characters.Practice` through `ZoneRating`, whose `rating` is -10 to
10). It carries `type = "reality_zone"` and `gameline = "mta"` as class attributes and
`RegistryURLMixin` for its URLs. Helpers: `get_positive_practices()`,
`get_negative_practices()` and `get_applied_to()` (the nodes, Horizon realms, sanctums,
demesnes and sectors that use it, including inherited realm types).

Zones can be shared: each place keeps a nullable `SET_NULL` foreign key, not a
one-to-one link. Place forms create a neutrally named `Reality Zone` when no zone is
linked and otherwise reuse it without changing its name. Editing its practice
ratings affects every linked place. Staff can give the zone an independent name.

A staff-created standalone zone is public reference data. Reading a linked zone requires
`VIEW_FULL` on every linked place, even when a place has a public card; partial
player or observer access does not disclose zone names or practices. This also
protects names copied by older versions without rewriting staff-owned zone names.
The non-editable `is_player_zone` flag is sticky: forms set it on new player zones,
and `LocationModel.save()` sets it atomically with any new link. Migration
`tg_schema.0012_protect_player_reality_zones` adds it to older databases and marks
every currently linked zone. Deleting, detaching or reassigning the last place never
makes such a zone public; only staff can read its orphaned zone. A stale zone save
cannot clear the flag. Unlinked zones whose old links were removed before this
migration have no recoverable provenance and are not guessed to be player zones.
See [nodes](nodes.md#reality-zones).

#### Reviewing zones orphaned before migration 0012

Old zones whose last place was removed before this release have no stored origin.
Migration 0012 cannot distinguish copied private names from independent staff
references. Before deploying the public zone pages, staff should review these
candidates in the trusted application environment after applying the migration.
Confirm the intended database first. Candidate names and descriptions may be
private; keep the output out of public channels.

In `python manage.py shell`, this read-only query lists up to 200 unclassified,
unlinked candidates. A matching name alone is not evidence of private origin.
Check available records or backups and make an explicit decision for each zone.

```python
from django.db.models import Exists, OuterRef
from locations.models.mage.reality_zone import RealityZone

last_reviewed_pk = 0
candidates = RealityZone.objects.filter(is_player_zone=False, pk__gt=last_reviewed_pk)
for relation in RealityZone.get_location_relations():
    linked = relation.related_model.objects.filter(
        reality_zone_id=OuterRef("pk")
    ).non_polymorphic()
    candidates = candidates.filter(~Exists(linked))
for row in candidates.order_by("pk").values("pk", "name", "description")[:200]:
    print(row)
```

For the next page, set `last_reviewed_pk` to the last reviewed PK and repeat the
query. After staff confirms specific zones are player-origin, fill the explicit ID
list below and run this separate classification step. An empty list changes
nothing. This marks only the chosen records private; it does not delete or rename
data, and it never automatically declassifies a zone. Leave confirmed independent
references unselected. If provenance is uncertain, staff must decide rather than
applying a blanket update or a name-based heuristic.

```python
confirmed_private_zone_ids = []  # Fill only with individually reviewed PKs.
RealityZone.objects.filter(
    pk__in=confirmed_private_zone_ids, is_player_zone=False
).update(is_player_zone=True)
```

Verify each selected zone now has `is_player_zone=True`, is absent from anonymous
lists and returns 404 to anonymous detail requests; staff can still read it.

## Changeling: the Dreaming (`ctd`)

Source: [`locations/models/changeling/`](../models/changeling/).

| Model | `type` | Main fields | Notes |
|-------|--------|-------------|-------|
| `Freehold` | `freehold` | Archetype, aspect, quirks, the five features, `powers` (JSON list), archetype abilities | See [freeholds](freeholds.md) |
| `Holding` | `holding` | `rank` (`barony`, `county`, `duchy`, `kingdom`, `province`), `court` (`seelie`, `unseelie`, `shadow`, `independent`, `disputed`), ruler, liege, vassals, `freehold_count` 0–50, `military_strength` / `wealth` / `stability` 0–5, politics, `threats` (JSON list), `history` | `str()` adds rank and ruler |
| `Trod` | `trod` | `trod_type` (`silver_path`, `rath`, `moonpath`, `seasonal`, `hidden`), origin and destination names and descriptions, `strength` 0–5, `difficulty` 0–10, `glamour_cost` 0–10, `hazards` (JSON list), `is_two_way`, `is_stable`, travel notes | `str()` adds "origin → destination" |
| `DreamRealm` | `dream_realm` | `depth` (`near`, `far`, `deep`), `realm_type`, `stability` / `accessibility` 0–5, `exit_difficulty` / `glamour_level` 0–10, `time_flow`, `dominant_themes` / `hazards` / `special_properties` (JSON lists), descriptive text fields | `get_depth_description()` |

The numeric ranges are enforced by validators and matching `CheckConstraint`s.

## Wraith: the Oblivion (`wto`)

Source: [`locations/models/wraith/`](../models/wraith/).

| Model | `type` | Main fields | Notes |
|-------|--------|-------------|-------|
| `Haunt` | `haunt` | `rank`, `shroud_rating` (default 5), `haunt_type`, `haunt_size`, `faith_resonance`, `attracts_ghosts` | `set_rank(rank)` also sets `shroud_rating` (rank 1 → 5 … rank 5 → 1; other ranks → 5) |
| `Necropolis` | `necropolis` | `region` (`stygia`, `ivory`, `jade`, `obsidian`, `other`), `population`, `deathlord` | |
| `Citadel` | `citadel` | `purpose`, `defense_rating`, `garrison_size`, `commander`, `controlling_faction`, `has_soulforges`, `has_prison`, `has_gateway` | |
| `Byway` | `byway` | `danger_level`, `stability`, `origin`, `destination`, `travel_time`, `maelstrom_proximity`, `spectral_activity`, `has_waystation`, `patrolled`, `haunted` | |
| `Nihil` | `nihil` | `void_type`, `stability`, `hazard_level` (default 10), `oblivion_proximity`, `entropy_rating`, `estimated_size`, drain and effect flags, `spectral_activity`, `contains_relics`, `origin_story` | |
| `WraithFreehold` | `wraith_freehold` | `population`, `government_type`, `leader`, `hierarchy_relation`, `allied_factions`, `defense_rating`, `resource_level`, feature flags, `hidden`, `founding_principle` | Unrelated to the Changeling `Freehold` |

`Byway`, `Citadel`, `Haunt`, `Nihil` and `WraithFreehold` order by name and define a
`str()` that adds a type or detail in parentheses.

## Demon: the Fallen (`dtf`)

Source: [`locations/models/demon/`](../models/demon/).

| Model | `type` | Fields | Methods |
|-------|--------|--------|---------|
| `Bastion` | `bastion` | `ritual_strength`, `warding_level`, `consecration_date` | |
| `Reliquary` | `reliquary` | `reliquary_type` (`location`, `perfect`, `improvised`), `location_size`, `max_health_levels` / `current_health_levels` (default 20), `soak_rating`, `has_pervasiveness`, `has_manifestation`, `manifestation_range` | `is_damaged()`, `damage_percentage()` |

## Hunter: the Reckoning (`htr`)

Source: [`locations/models/hunter/`](../models/hunter/).

| Model | `type` | Main fields | Computed on save |
|-------|--------|-------------|------------------|
| `HuntingGround` | `hunting_ground` | `size`, `population`, `supernatural_activity`, `primary_threat`, `threat_description`, `is_contested`, `control_level`, `rival_cells` (M2M `characters.Hunter`, related name `rival_territories`), `contact_network`, `surveillance_coverage`, `last_incident`, `incident_log`, `key_locations` | `total_rating` = the six ratings summed, -2 when contested, minimum 0 |
| `Safehouse` | `safehouse` | `size`, `capacity`, `security_level`, `armory_level`, `surveillance_level`, `medical_facilities`, `is_compromised`, `is_mobile`, `has_panic_room`, `has_escape_routes`, `has_dead_drop`, `has_communications`, `cover_story`, `legal_owner` | `total_rating` = five ratings summed, +1 per panic room, escape routes, dead drop, -2 when compromised, minimum 0 |

## Mummy: the Resurrection (`mtr`)

Source: [`locations/models/mummy/`](../models/mummy/).

| Model | `type` | Main fields | Computed on save |
|-------|--------|-------------|------------------|
| `Tomb` | `tomb` | `size` (0–5 choices), `security` 0–5, `sanctity` 0–5, `era`, feature flags, `ba_per_week` 0–100, `duat_barrier` 0–10 (default 7), `merits_and_flaws` through `TombMeritFlawRating`, guardian and discovery notes | `rank = size + security + sanctity`; at rank 7 or more, `duat_barrier = max(3, 7 - (rank - 7))` |
| `CultTemple` | `cult_temple` | `cult_size` 0–10, `public_cover`, `cult_leader_name`, `cult_wealth` 0–5, `has_library`, `has_ritual_chamber` | |
| `UndergroundSanctuary` | `underground_sanctuary` | `sanctuary_type` (`catacombs`, `basement`, `caves`, `subway`, `bunker`), `concealment_rating` 0–5 | |

`TombMeritFlawRating` is unique per `(tomb, mf)` with a rating of -10 to 10.

## Computed fields at a glance

These fields are overwritten on every save, so forms that expose them cannot set them.

| Model | Field | Rule |
|-------|-------|------|
| `Haven`, `Domain`, `TremereChantry`, `HuntingGround`, `Safehouse` | `total_rating` | See the tables above |
| `Caern` | `gauntlet` | From `rank` |
| `Tomb` | `rank`, sometimes `duat_barrier` | From size, security and sanctity |

## See also

- [Chantries](chantries.md), [nodes](nodes.md), [realms](realms.md), [freeholds](freeholds.md)
- [Views and URLs](views-and-urls.md)
- [Location forms](forms.md)
- [Data model overview](../../docs/architecture/data-model.md)
- [Glossary](../../docs/reference/glossary.md)
