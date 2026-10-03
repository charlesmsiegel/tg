# Location forms

This page lists every form the `locations` app uses: the fields of the forms the
registry generates, the type chooser, the owner-limited edit form, and the hand-written
forms for Changeling places, chantries, nodes, sanctums, demesnes, libraries, sectors,
realms and reality zones. It is for developers changing what a location page accepts
and for agents submitting location forms. The multi-step flows are explained in
[chantries](chantries.md), [nodes](nodes.md), [realms](realms.md) and
[freeholds](freeholds.md).

## Generated forms

Types without a form class get a `ModelForm` built by the registry from the fields in
[`locations/registry.py`](../registry.py) (the action's `options["fields"]`, else the
spec's `fields`); `form_updates` adds placeholders and help text. See the
[items registry description](../../items/docs/views-and-urls.md#how-views-are-built).

| Model | Create fields | Update fields (when different) |
|-------|---------------|--------------------------------|
| `LocationModel` | `name`, `contained_within`, `gauntlet`, `shroud`, `dimension_barrier`, `description` | Same, or `LimitedLocationEditForm` for editors without a scoped editor role |
| `City` | `name`, `description`, `contained_within`, `gauntlet`, `shroud`, `dimension_barrier`, `population`, `mood`, `theme`, `media`, `politicians`, `characters` | |
| `Haven` | `name`, `description`, `contained_within`, `size`, `security`, `location`, `has_guardian`, `has_luxury`, `is_hidden`, `has_library`, `has_workshop` | |
| `Domain` | `name`, `description`, `contained_within`, `size`, `population`, `control`, `is_elysium`, `has_rack`, `is_disputed`, `domain_type` | |
| `Elysium` | `name`, `description`, `contained_within`, `prestige`, `keeper_name`, `elysium_type`, `is_protected`, `allows_weapons`, `has_blood_dolls`, `has_art_collection`, `has_library`, `is_court` | |
| `Rack` | `name`, `description`, `contained_within`, `quality`, `population_density`, `risk_level`, `rack_type`, `blood_quality`, `is_protected`, `is_exclusive`, `is_contested`, `masquerade_risk` | |
| `TremereChantry` | `name`, `description`, `contained_within`, `size`, `security_level`, `library_rating`, `ritual_rooms`, `blood_vault_capacity`, `regent_name`, `resident_count`, `apprentice_count`, `has_wards`, `has_sanctum`, `has_blood_forge`, `has_scrying_chamber`, `has_gargoyle_guardians`, `pyramid_level`, `reports_to` | |
| `Barrens` | `name`, `description`, `contained_within`, `size`, `danger_level`, `population_density`, the control, resource and activity flags, `controlling_faction`, `feeding_quality`, `masquerade_threat`, `barrens_type`, `notable_locations` | |
| `Caern` | `name`, `contained_within`, `description`, `rank`, `caern_type` | |
| `Chantry` | `chronicle` plus `DIRECT_FORM_FIELDS` (see [chantries](chantries.md#three-ways-to-create-a-chantry)) | `DIRECT_FORM_FIELDS` |
| `Demesne` | `DemesneForm` (below) | `name`, `description`, `contained_within`, `size`, `accessibility` |
| `Library` | `LibraryForm` (below) | `name`, `description`, `contained_within`, `rank`, `faction`, `books` |
| `HorizonRealm` | `name`, `description`, `contained_within` | |
| `RealityZone` | `name`, `description`, `practices` | |
| `Byway` | `name`, `description`, `contained_within`, `danger_level`, `stability`, `origin`, `destination`, `travel_time`, `maelstrom_proximity`, `spectral_activity`, `has_waystation`, `patrolled`, `haunted` | |
| `Citadel` | `name`, `description`, `contained_within`, `purpose`, `defense_rating`, `garrison_size`, `commander`, `controlling_faction`, `has_soulforges`, `has_prison`, `has_gateway` | |
| `WraithFreehold` | `name`, `description`, `contained_within`, `population`, `government_type`, `leader`, `hierarchy_relation`, `allied_factions`, `defense_rating`, `resource_level`, `has_soulforges`, `has_library`, `has_safe_passage`, `hidden`, `founding_principle` | |
| `Haunt` | `name`, `description`, `contained_within`, `rank`, `shroud_rating`, `haunt_type`, `haunt_size`, `faith_resonance`, `attracts_ghosts` | |
| `Necropolis` | `name`, `description`, `contained_within`, `region`, `population`, `deathlord` | |
| `Nihil` | `name`, `description`, `contained_within`, `void_type`, `stability`, `hazard_level`, `oblivion_proximity`, `entropy_rating`, `estimated_size`, the drain and effect flags, `spectral_activity`, `contains_relics`, `origin_story` | |
| `Bastion` | `name`, `contained_within`, `description`, `ritual_strength`, `warding_level`, `consecration_date` | |
| `Reliquary` | `name`, `contained_within`, `description`, `reliquary_type`, `location_size`, `max_health_levels`, `current_health_levels`, `soak_rating`, `has_pervasiveness`, `has_manifestation`, `manifestation_range` | |
| `HuntingGround` | `name`, `contained_within`, `description`, `size`, `population`, `supernatural_activity`, `primary_threat`, `threat_description`, `is_contested`, `control_level`, `contact_network`, `surveillance_coverage`, `last_incident`, `incident_log`, `key_locations` | |
| `Safehouse` | `name`, `contained_within`, `description`, `size`, `capacity`, `security_level`, `armory_level`, `surveillance_level`, `medical_facilities`, the feature flags, `cover_story`, `legal_owner` | |
| `Tomb` | `name`, `description`, `contained_within`, `size`, `security`, `sanctity`, `era`, the feature flags, `ba_per_week`, `guardian_description`, `original_occupant`, `discovered_date`, `archaeological_status` | Adds `duat_barrier` |
| `CultTemple` | `name`, `description`, `contained_within`, `cult_size`, `public_cover`, `cult_leader_name`, `cult_wealth`, `has_library`, `has_ritual_chamber` | |
| `UndergroundSanctuary` | `name`, `description`, `contained_within`, `sanctuary_type`, `concealment_rating` | |

Fields recomputed on save (such as `total_rating` or a caern's gauntlet) are listed in
[models](models.md#computed-fields-at-a-glance). The authoritative field lists are in
the registry; when you change one, render the new field in the type's `form.html`.

## `LocationCreationForm`

Source: [`locations/forms/core/location_creation.py`](../forms/core/location_creation.py).

The type chooser on the staff index and the public locations list: chained
`gameline` and `loc_type` selects filled from `registry.menu(user)`, plus unused
`name` and `rank` fields. The widgets get the ids `id_loc_gameline` and `id_loc_type`.
Pass `user=request.user`; the form submits with GET to `core:object_type_redirect`
and is never saved. See
[views and URLs](views-and-urls.md#creating-a-location-from-a-menu).

## `LimitedLocationEditForm`

Source: [`locations/forms/core/limited_edit.py`](../forms/core/limited_edit.py).

A `ModelForm` on `LocationModel` with `description`, `public_info` and `image`, given
by `_LocationUpdateView` to editors without a scoped editor role (typically the
owner).

## Changeling forms

| Form | Source | Fields | Rules |
|------|--------|--------|-------|
| `FreeholdForm` | [`forms/changeling/freehold.py`](../forms/changeling/freehold.py) | Every freehold field, `powers` as checkboxes, `contained_within`, `owned_by`, barriers | See [freeholds](freeholds.md#the-direct-form-freeholdform) |
| `FreeholdBasicsForm`, `FreeholdFeaturesForm`, `FreeholdPowersForm`, `FreeholdDetailsForm` | [`forms/changeling/creation.py`](../forms/changeling/creation.py) | One wizard step each | See [freeholds](freeholds.md#the-creation-wizard) |
| `DreamRealmForm` | [`forms/changeling/dream_realm.py`](../forms/changeling/dream_realm.py) | `name`, `description`, `depth`, `realm_type`, `stability`, `accessibility`, `appearance`, `laws_of_reality`, `inhabitants`, `ruler`, `emotional_tone`, `entry_requirements`, `exit_difficulty`, `mundane_connection`, `glamour_level`, `provides_glamour`, `treasures`, `time_flow`, `is_mutable` | Placeholders and help text only |
| `HoldingForm` | [`forms/changeling/holding.py`](../forms/changeling/holding.py) | `name`, `description`, `rank`, `court`, ruler and liege fields, `territory_description`, `mundane_location`, `vassals`, `freehold_count`, `major_freeholds`, `population`, `military_strength`, `wealth`, `stability`, `political_situation`, `notable_laws`, `rival_holdings`, `history` | Placeholders and help text only |
| `TrodForm` | [`forms/changeling/trod.py`](../forms/changeling/trod.py) | `name`, `description`, `trod_type`, origin and destination fields, `strength`, `difficulty`, `access_requirements`, `guardians`, `travel_duration`, `is_two_way`, `is_stable`, `glamour_cost`, `accessibility_notes`, `journey_description`, `known_to` | Placeholders and help text only |

The JSON list fields of these models (`dominant_themes`, `hazards`,
`special_properties`, `threats`) and `contained_within` are not part of the Dream
Realm, Holding and Trod forms.

## Mage forms

### Chantry forms

Source: [`locations/forms/mage/chantry.py`](../forms/mage/chantry.py). Full behaviour
in [chantries](chantries.md).

| Form | Kind | Use |
|------|------|-----|
| `ChantryCreateForm` | `ModelForm` with `ChantryFundingMixin` | Wizard entry: `name`, `chronicle`, `contained_within`, `description`, `faction`, `leadership_type`, `season`, `chantry_type`, the barriers, and `total_points` (0 or more). `save()` funds the chantry with `chantry_points.set_total_points()` and saves many-to-many data. |
| `ChantryPointForm` | `Form` (chained selects, conditional fields) | Wizard step 1. Constructor takes `chantry`, the instance the view resolved. `category` (`-----`, `Integrated Effects`, `New Background`, `Existing Background`; only the affordable ones are offered) and `example` chained to it; `note` and `display_alt_name` for new backgrounds. `clean()` re-checks with the points service; `save()` calls `buy_ie_dot()` or `buy_background_dot()` and lets their `ValidationError` propagate for the view to show. |
| `ChantryEffectsForm` | `characters.forms.mage.effect.EffectCreateOrSelectForm` | Wizard step 2. Constructor takes `chantry`; `select` is limited to affordable effects within the rank. `save()` adds the effect to `integrated_effects`. |
| `ChantrySelectOrCreateForm` | `ModelForm` with `CreateOrSelectMixin` | Character wizards' Chantry step; see below |
| `ChantryRemoveForm` | `Form` | Validates and applies one refund (`rating`, `ie` or `effect`) through the points service; not used by any view |
| `ChantryFundingMixin` | Mixin | When the submitted `total_points` differs from the stored one, `clean_total_points()` asks `chantry_points.funding_error()`: never negative, never below what a saved chantry has spent. On a saved chantry `save(commit=True)` writes the other fields with `update_fields` (never `total_points`), then a differing total through `chantry_points.set_total_points()` (locked and re-checked), in one transaction; it may raise `ValidationError`, which the update view turns into a form error. A total matching the stored one is left untouched. The submitted total is absolute, so a join between page load and save is replaced by it. `funded(form_class)` adds it in front of the registry-built direct create and update forms. |

#### `ChantrySelectOrCreateForm`

Constructor: `ChantrySelectOrCreateForm(data, character=<Human>, points=<int>)`.
`create_new` toggles between joining `existing_chantry` and creating a chantry from
`name` and the chantry detail fields. All fields are optional; creating requires a
name, joining requires a selection.

- The chantries offered are `joinable_chantries(character)`: unfinished (`Un`) or
  returned (`Rev`) chantries that the character's player owns or that already list
  the character in `members`, in the character's chronicle (or chronicle-less for a
  character with no chronicle). Joining only adds points, and points can only be
  spent while the chantry is in its wizard, so an approved, submitted, retired or
  deceased chantry is never offered; nor is another player's draft the character
  does not belong to, since the points would raise its rank behind that player's
  back. Membership is the invitation: a scoped Mage storyteller or staff member
  adds the character to `members` through the direct update form (the only way to
  edit that list; owners are refused there), and the character may then pool
  points into that draft. That is the one remaining way to raise another player's
  chantry rank, and it is a storyteller's decision. A POST naming a chantry
  outside the queryset is a field error and changes nothing.
- `save()` always commits, inside a transaction. Creating sets the owner (the
  character's player), chronicle, `status = "Un"`, `creation_status = 1`, funds the
  chantry with `chantry_points.set_total_points(chantry, points)`, saves many-to-many
  data and applies type grants. Joining calls `chantry_points.add_points(chantry,
  points)`, a single `UPDATE ... SET total_points = total_points + points` that also
  requires the chantry still to be in `Un`/`Rev`, and leaves the owner, chronicle and
  status alone. It returns the chantry. `save()` raises `ValidationError` when the
  chantry was deleted or approved after validation;
  `CharacterChantryBackgroundView` rolls back the claim and shows it as a form error.

### `NodeForm`, `SanctumForm`, `DemesneForm`

These forms share `RealityZoneFormMixin`, which binds a
`RealityZonePracticeRatingFormSet`, checks that ratings total zero and positive
ratings sum to the place's rank, and saves the zone and ratings. A new zone is named
`Reality Zone`; an existing zone keeps its independent name and shared identity.
`commit=False` saves neither zones nor ratings. `NodeForm` also carries Resonance and
merit/flaw formsets and the node point budget.
Registry views pass the request to the mixin before any private row is bound. When
the requester cannot fully view every linked place, the form has no zone instance
or zone formset and its rank is read-only. Descriptive parent edits remain usable;
forged rank or nested-zone changes fail validation and save nothing. Staff retain
the full shared-zone form. New form-created zones start with sticky player
provenance and never become public by losing their last place.
See [nodes](nodes.md#creating-and-editing-a-node-nodeform) and
[reality zones](nodes.md#reality-zones).

| Form | Model fields |
|------|--------------|
| `NodeForm` | `name`, `rank`, `description`, `ratio`, `size`, `quintessence_form`, `tass_form`, `contained_within`, barriers |
| `SanctumForm` | `name`, `contained_within`, `description`, `rank` |
| `DemesneForm` | `name`, `contained_within`, `description`, `rank`, `size`, `accessibility` |

### `LibraryForm`

Source: [`locations/forms/mage/library.py`](../forms/mage/library.py).

Fields `name`, `description`, `contained_within` (optional), `rank`, `faction`.
`save()` always saves the library, then calls `Library.random_book()` once per rank
to stock it with generated grimoires. Used by the library create page, step 4 of the
chantry wizard and the Library background step of the Mage-family character wizards.

### `SectorForm`

Source: [`locations/forms/mage/sector.py`](../forms/mage/sector.py).

Every `Sector` field plus `contained_within`, with `connected_sectors` as checkboxes.
`clean()` adds field errors (which block saving) when:

- `requires_password` is set without a `password_hint`;
- a restricted sector has neither a password nor `approved_users`;
- `corruption_level` is 8 or more and `is_reformattable` is set;
- a `warzone` has `power_rating` below 7;
- `temporal_instability` is set with `time_dilation` of 1.00.

### Paradox realm forms

`ParadoxRealmForm` with `ParadoxObstacleFormSet` and `ParadoxAtmosphereFormSet`; see
[realms](realms.md#paradoxrealmform).

### Reality zone formset

Source: [`locations/forms/mage/reality_zone.py`](../forms/mage/reality_zone.py).

`RealityZonePracticeRatingForm` has `practice` (practices other than specialized and
corrupted ones) and `rating` (-5 to 5). `RealityZonePracticeRatingFormSet` is an inline
formset on `RealityZone` (one extra row, deletion allowed) whose `save_new()` binds new
rows to the formset's zone.

## See also

- [Location models](models.md)
- [Views and URLs](views-and-urls.md)
- [Location templates](templates.md)
- [Chantries](chantries.md), [nodes](nodes.md), [realms](realms.md), [freeholds](freeholds.md)
- [widgets app](../../widgets/README.md)
