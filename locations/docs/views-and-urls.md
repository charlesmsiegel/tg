# Location views and URLs

This page explains how the `locations` app builds its views and URL patterns from the
registry, which access policy guards each action, which views carry custom behaviour,
the routes outside the registry (wizards, aliases, AJAX), and the full list of
location URLs. It is for developers adding or changing a location page and for agents
that link to or call one. The wizard flows themselves are described in
[chantries](chantries.md) and [freeholds](freeholds.md).

## The registry

Source: [`locations/registry.py`](../registry.py), built on
[`core/model_registry.py`](../../core/model_registry.py).

`locations.registry.registry` is a `ModelRegistry("locations", [...])` with one
`ModelSpec` per routable model. It uses the same machinery as the items registry:
`ModelSpec` and `ActionSpec` fields, import-time validation, `registry.view(model,
action)` to build a view class, and `registry.urls(group, action)` to build URL
patterns. That mechanism is described once in the
[items views page](../../items/docs/views-and-urls.md#the-registry); this page covers
what is specific to locations.

Two `ModelSpec` features matter here:

- **`dispatch_view`**: `Chantry` sets it to
  `locations.views.mage.chantry.ChantryCreationView`. The polymorphic router then sends
  `/locations/<pk>/` for a chantry to the chantry wizard router instead of the plain
  detail view (see [below](#polymorphic-detail-routing)).
- **`custom` bases**: many location actions wrap a hand-written view (listed under
  [custom views](#custom-views)).

## Access policies

The evaluator is `core.access_policy.authorize_route()`; see
[authorization](../../docs/architecture/authorization.md). Registry views check their
declared policy in `RegistryViewMixin.dispatch()`; other routes are checked by
`core.middleware.authorization.AuthorizationMiddleware` using
`core/route_policy_manifest.py`.

| Policy | Used by | Effect |
|--------|---------|--------|
| `OBJECT_DETAIL` | Detail of every location type | `VIEW_FULL` shows the page; otherwise GET/HEAD returns the public projection (name, public info, approved image) only for `PUB`, or `CHR` in a readable chronicle. `PRI`, unknown values and other methods return 404 |
| `OBJECT_LIST` | List of every location type | Staff and superusers see the per-type list (filtered by `VisibilityFilterMixin`); others get the shared public list |
| `OBJECT_CREATE` | Create of every location type; `ChantryBasicsView`, `FreeholdBasicsView` | Login required (401 for anonymous users) |
| `OBJECT_WRITE` | Update of most types | `EDIT_FULL` required; non-staff POSTs may not change `owner`, `chronicle`, `status` and the other approval fields |
| `OBJECT_ST_WRITE` | `Chantry` update | As `OBJECT_WRITE`, and the user must hold a scoped editor role (admin, head storyteller or storyteller of the chantry's chronicle) |
| `OBJECT_ACTION` | `ParadoxRealm` update | `EDIT_FULL` required, with the same approval-field guard |
| `PUBLIC_READ` / `STAFF_WRITE` | `RealityZone` | Standalone zones are public; linked zones require full access to every place; staff create and edit |
| `CHARGEN_STEP` | The chantry wizard steps and freehold wizard steps | `EDIT_FULL` required and the object's `status` must be `Un` or `Rev`; otherwise 404 |
| `ROUTER` | `GenericLocationDetailView`, `ChantryCreationView`, `FreeholdCreationView` | No check at the router; the target view is authorized |
| `PUBLIC_INDEX` | `LocationIndexView` | Anyone; the view decides what to show |
| `LOGIN` | `LoadExamplesView` | Login required; the view then requires `EDIT_FULL` on the chantry and answers 404 otherwise, as for a missing one |

As for items, non-staff users always receive the public list, so per-type list
templates render only for staff.

## Polymorphic detail routing

`/locations/<pk>/` (URL name `locations:location`) is `GenericLocationDetailView`
([`locations/views/core/__init__.py`](../views/core/__init__.py)), a
`core.views.registry.RegistryDetailView`. It loads the concrete location, finds its
entry in `registry.detail_views` (every registered `LocationModel` subclass;
`RealityZone` is excluded because it is not a location), authorizes that type's
registry detail view against the object, and renders the target:

- for most types, the type's detail view;
- for `Chantry`, `ChantryCreationView`, which shows the wizard step for
  `creation_status` 1–6 to users who may edit a draft and the detail page otherwise.

Most location types use `locations:location` as their `get_absolute_url()` target.

## Creating a location from a menu

`locations.forms.core.LocationCreationForm` (fields `gameline` and `loc_type`, chained)
lists the types from `registry.menu(user)`: staff, superusers and storytellers see all
types, other players only Mage types, and `STAFF_WRITE` types (`RealityZone`) only
staff. The form submits with GET to `core:object_type_redirect` with
`kind="location"`, which resolves the slug with `registry.resolve()` and redirects to
`registry.selection_url()`. For `Chantry` and `Freehold` this is the wizard entry
(`model_urls["create"]`), because their registry create routes are named
`chantry_direct` and `freehold_direct`, not the slug.

## The staff index

`/locations/index/` (URL name `locations:index`) is `LocationIndexView`.

- Staff and superusers get `locations/index.html`: one chronicle's containment tree.
  `?chronicle=<pk>` or `?chronicle=none` picks the chronicle (default: the first
  chronicle with places); `?line=<code>` keeps only places of that gameline and the
  ancestors that lead to them. The tree is built from one polymorphic query and one
  query on the `contained_within` through table; roots are places with no container,
  cycles are cut, and display depth is capped at `MAX_DEPTH` (8).
- Everyone else gets the shared public list of locations, with the creation form when
  logged in.

## Custom views

| Class | Module | Behaviour |
|-------|--------|-----------|
| `_LocationCreateView` | [`views/core/location.py`](../views/core/location.py) | Login required; placeholders and help text; `prepare_created_object()` |
| `_LocationUpdateView` | [`views/core/location.py`](../views/core/location.py) | `EditPermissionMixin`; scoped editors get the full form, other editors `LimitedLocationEditForm` (`description`, `public_info`, `image`) |
| `_ChantryDetailView` | [`views/mage/chantry.py`](../views/mage/chantry.py) | Adds `factions`: the faction chain as linked names joined by "/" |
| `_ChantryListView` | same | Adds `can_create_directly` |
| `_ChantryCreateView`, `_ChantryUpdateView` | same | Direct storyteller forms; see [chantries](chantries.md#three-ways-to-create-a-chantry) |
| `_NodeCreateView`, `_DemesneCreateView`, `_LibraryCreateView`, `_SanctumCreateView`, `_ParadoxRealmCreateView` | [`views/mage/`](../views/mage/) | `FormView`s: `prepare_created_object()`, `form.save()`, redirect to the new object |
| `_ParadoxRealmUpdateView` | [`views/mage/paradox_realm.py`](../views/mage/paradox_realm.py) | `FormView` bound to the realm |
| `_NodeDetailView`, `_ParadoxRealmDetailView`, `_HavenDetailView` | [`views/mage/`](../views/mage/), [`views/vampire/`](../views/vampire/) | Add rating rows (Resonance, merits and flaws, obstacles, atmospheres) to the context |
| `_RealityZoneDetailView` / `_RealityZoneListView` | [`views/mage/reality_zone.py`](../views/mage/reality_zone.py) | Standalone zones or zones whose linked places the viewer can all fully view; practices and applied places on detail |
| `_FreeholdDetailView`, `_FreeholdCreateView`, `_FreeholdUpdateView` | [`views/changeling/freehold.py`](../views/changeling/freehold.py) | Feature points and Holdings in the context; see [freeholds](freeholds.md) |

Reality-zone reads keep the reference-data route policy so standalone zones do not
require login. `ViewPermissionMixin` guards detail (hidden and missing zones both
return 404), and `VisibilityFilterMixin` filters the list through `PermissionManager`.
Linked-zone reads deliberately require `VIEW_FULL`, not just a public place card or
partial player/observer access. For shared zones, access to one place is insufficient.
The same permission gates inline zone displays and registry form choices, including
validation of submitted zone IDs. The nullable many-to-one links remain unchanged.
An edit form with an inline zone formset also returns 404 if its shared zone is
unreadable, preventing an owner of one place from reading or modifying another
place's shared practices. A player-origin zone keeps its classification after its
last place is deleted, detached or reassigned; its orphan is readable only by staff.

## Routes outside the registry

| Path | URL name | View | Purpose |
|------|----------|------|---------|
| `/locations/<pk>/` | `locations:location` | `GenericLocationDetailView` | Polymorphic router |
| `/locations/index/` | `locations:index` | `LocationIndexView` | Staff index |
| `/locations/mage/create/chantry/` | `locations:mage:create:chantry` | `ChantryBasicsView` | Chantry wizard entry |
| `/locations/changeling/create/freehold/` | `locations:changeling:create:freehold` | `FreeholdBasicsView` | Freehold wizard entry |
| `/locations/changeling/update/freehold/<pk>/` | `locations:changeling:update:freehold` | `FreeholdCreationView` | Freehold wizard router |
| `/locations/mage/ajax/load_chantry_examples/` | `locations:mage:ajax:load_chantry_examples` | `LoadExamplesView` | JSON options (`?category=New Background` or `Existing Background`, `&object=<chantry pk>`) of backgrounds the chantry can afford; only the chantry's editors, others get 404 |
| `/locations/mage/<type>/` | `locations:mage:<type>` | The type's list view | Aliases of every Mage list without `list/` in the path |
| `/locations/hunter/safehouse/`, `/locations/hunter/hunting-ground/` | `locations:hunter:safehouse-list`, `locations:hunter:hunting-ground-list` | The Hunter list views | List aliases |

The Mage list aliases share their URL names with the Mage detail routes (for example
`locations:mage:chantry` is both `/locations/mage/chantry/` and
`/locations/mage/chantry/<pk>/`); `reverse()` picks the pattern that matches the
arguments you pass.

## URL patterns

[`locations/urls/__init__.py`](../urls/__init__.py) is included at `/locations/` under
the `locations` namespace. Its structure matches the items app: one include per
gameline from `core.constants.GameLine.URL_PATTERNS`, then the `core` group's
`create/`, `update/` and `list/` includes, `index/`, the `core` detail routes and the
router. URL names follow the same pattern:

| Action | URL name | Path prefix |
|--------|----------|-------------|
| detail | `locations:<group>:<name>` | `/locations/<group>/` |
| list | `locations:<group>:list:<name>` | `/locations/<group>/list/` |
| create | `locations:<group>:create:<name>` | `/locations/<group>/create/` |
| update | `locations:<group>:update:<name>` | `/locations/<group>/update/` |

For the `core` group, drop `<group>:` and `<group>/`.

### Every registry route

Paths are relative to `/locations/`. Policies are `OBJECT_DETAIL`, `OBJECT_LIST`,
`OBJECT_CREATE` and `OBJECT_WRITE` unless the [policy table](#access-policies) says
otherwise. `LocationModel` has no per-type detail route; it is reached through
`locations:location`.

### `core`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `City` | `city` | `city` | `city/<pk>/` | `list/city/` | `create/city/` | `update/city/<pk>/` | `locations:location` |
| `LocationModel` | `location` | `location` | — | `list/location/` | `create/location/` | `update/location/<pk>/` | `locations:location` |

### `vampire`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Haven` | `haven` | `haven` | `vampire/haven/<pk>/` | `vampire/list/havens/` | `vampire/create/haven/` | `vampire/update/haven/<pk>/` | `locations:location` |
| `Domain` | `domain` | `domain` | `vampire/domain/<pk>/` | `vampire/list/domains/` | `vampire/create/domain/` | `vampire/update/domain/<pk>/` | `locations:vampire:domain` |
| `Elysium` | `elysium` | `elysium` | `vampire/elysium/<pk>/` | `vampire/list/elysiums/` | `vampire/create/elysium/` | `vampire/update/elysium/<pk>/` | `locations:location` |
| `Rack` | `rack` | `rack` | `vampire/rack/<pk>/` | `vampire/list/racks/` | `vampire/create/rack/` | `vampire/update/rack/<pk>/` | `locations:location` |
| `TremereChantry` | `tremere_chantry` | `chantry`, `tremere_chantry` | `vampire/chantry/<pk>/` | `vampire/list/tremere_chantry/` | `vampire/create/chantry/`<br>`vampire/create/tremere_chantry/` | `vampire/update/chantry/<pk>/` | `locations:location` |
| `Barrens` | `barrens` | `barrens` | `vampire/barrens/<pk>/` | `vampire/list/barrens/` | `vampire/create/barrens/` | `vampire/update/barrens/<pk>/` | `locations:location` |

### `werewolf`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Caern` | `caern` | `caern` | `werewolf/caern/<pk>/` | `werewolf/list/caern/` | `werewolf/create/caern/` | `werewolf/update/caern/<pk>/` | `locations:location` |

### `mage`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Chantry` | `chantry` | `chantry_direct`, `chantry` | `mage/chantry/<pk>/` | `mage/list/chantry/` | `mage/create/chantry/direct/` | `mage/update/chantry/<pk>/` | `locations:location` |
| `Demesne` | `demesne` | `demesne` | `mage/demesne/<pk>/` | `mage/list/demesne/` | `mage/create/demesne/` | `mage/update/demesne/<pk>/` | `locations:location` |
| `Library` | `library` | `library` | `mage/library/<pk>/` | `mage/list/library/` | `mage/create/library/` | `mage/update/library/<pk>/` | `locations:location` |
| `Node` | `node` | `node` | `mage/node/<pk>/` | `mage/list/node/` | `mage/create/node/` | `mage/update/node/<pk>/` | `locations:location` |
| `ParadoxRealm` | `paradox_realm` | `paradox_realm` | `mage/paradox_realm/<pk>/` | `mage/list/paradox_realm/` | `mage/create/paradox_realm/` | `mage/update/paradox_realm/<pk>/` | `locations:location` |
| `HorizonRealm` | `horizon_realm` | `horizon_realm` | `mage/horizon_realm/<pk>/` | `mage/list/horizon_realm/` | `mage/create/realm/` | `mage/update/realm/<pk>/` | `locations:location` |
| `Sanctum` | `sanctum` | `sanctum` | `mage/sanctum/<pk>/` | `mage/list/sanctum/` | `mage/create/sanctum/` | `mage/update/sanctum/<pk>/` | `locations:location` |
| `Sector` | `sector` | `sector` | `mage/sector/<pk>/` | `mage/list/sector/` | `mage/create/sector/` | `mage/update/sector/<pk>/` | `locations:location` |
| `RealityZone` | `reality_zone` | `reality_zone` | `mage/reality_zone/<pk>/` | `mage/list/reality_zone/` | `mage/create/reality_zone/` | `mage/update/reality_zone/<pk>/` | `locations:mage:reality_zone` |

### `wraith`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Byway` | `byway` | `byway` | `wraith/byway/<pk>/` | `wraith/list/byway/` | `wraith/create/byway/` | `wraith/update/byway/<pk>/` | `locations:wraith:byway` |
| `Citadel` | `citadel` | `citadel` | `wraith/citadel/<pk>/` | `wraith/list/citadel/` | `wraith/create/citadel/` | `wraith/update/citadel/<pk>/` | `locations:wraith:citadel` |
| `WraithFreehold` | `wraith_freehold` | `freehold` | `wraith/freehold/<pk>/` | `wraith/list/freehold/` | `wraith/create/freehold/` | `wraith/update/freehold/<pk>/` | `locations:wraith:freehold` |
| `Haunt` | `haunt` | `haunt` | `wraith/haunt/<pk>/` | `wraith/list/haunt/` | `wraith/create/haunt/` | `wraith/update/haunt/<pk>/` | `locations:wraith:haunt` |
| `Necropolis` | `necropolis` | `necropolis` | `wraith/necropolis/<pk>/` | `wraith/list/necropolis/` | `wraith/create/necropolis/` | `wraith/update/necropolis/<pk>/` | `locations:wraith:necropolis` |
| `Nihil` | `nihil` | `nihil` | `wraith/nihil/<pk>/` | `wraith/list/nihil/` | `wraith/create/nihil/` | `wraith/update/nihil/<pk>/` | `locations:wraith:nihil` |

### `changeling`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `DreamRealm` | `dream_realm` | `dream_realm` | `changeling/dream_realm/<pk>/` | `changeling/list/dream_realm/` | `changeling/create/dream_realm/` | `changeling/update/dream_realm/<pk>/` | `locations:changeling:dream_realm` |
| `Freehold` | `freehold` | `freehold_direct`, `freehold` | `changeling/freehold/<pk>/` | `changeling/list/freehold/` | `changeling/create/freehold/direct/` | `changeling/update/freehold/<pk>/direct/` | `locations:changeling:freehold` |
| `Holding` | `holding` | `holding` | `changeling/holding/<pk>/` | `changeling/list/holding/` | `changeling/create/holding/` | `changeling/update/holding/<pk>/` | `locations:changeling:holding` |
| `Trod` | `trod` | `trod` | `changeling/trod/<pk>/` | `changeling/list/trod/` | `changeling/create/trod/` | `changeling/update/trod/<pk>/` | `locations:changeling:trod` |

### `demon`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Bastion` | `bastion` | `bastion` | `demon/bastion/<pk>/` | `demon/list/bastion/` | `demon/create/bastion/` | `demon/update/bastion/<pk>/` | `locations:demon:bastion` |
| `Reliquary` | `reliquary` | `reliquary` | `demon/reliquary/<pk>/` | `demon/list/reliquary/` | `demon/create/reliquary/` | `demon/update/reliquary/<pk>/` | `locations:demon:reliquary` |

### `hunter`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `HuntingGround` | `hunting_ground` | `hunting_ground` | `hunter/hunting-ground/<pk>/` | `hunter/list/hunting-grounds/` | `hunter/create/hunting-ground/` | `hunter/update/hunting-ground/<pk>/` | `locations:location` |
| `Safehouse` | `safehouse` | `safehouse` | `hunter/safehouse/<pk>/` | `hunter/list/safehouses/` | `hunter/create/safehouse/` | `hunter/update/safehouse/<pk>/` | `locations:location` |

### `mummy`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Tomb` | `tomb` | `tomb` | `mummy/tomb/<pk>/` | `mummy/list/tomb/` | `mummy/create/tomb/` | `mummy/update/tomb/<pk>/` | `locations:mummy:tomb` |
| `CultTemple` | `cult_temple` | `cult_temple` | `mummy/cult_temple/<pk>/` | `mummy/list/cult_temple/` | `mummy/create/cult_temple/` | `mummy/update/cult_temple/<pk>/` | `locations:mummy:cult_temple` |
| `UndergroundSanctuary` | `underground_sanctuary` | `sanctuary` | `mummy/sanctuary/<pk>/` | `mummy/list/sanctuary/` | `mummy/create/sanctuary/` | `mummy/update/sanctuary/<pk>/` | `locations:mummy:sanctuary` |

`TremereChantry` has two create routes (`vampire/create/chantry/` and
`vampire/create/tremere_chantry/`). The `Chantry` registry create route is the direct
storyteller form; the wizard entry `mage/create/chantry/` is added by
[`urls/mage/create.py`](../urls/mage/create.py). The `Freehold` registry create and
update routes are the direct forms; the wizard routes are added by
[`urls/changeling/create.py`](../urls/changeling/create.py) and
[`urls/changeling/update.py`](../urls/changeling/update.py).

## See also

- [Location models](models.md)
- [Chantries](chantries.md) and [freeholds](freeholds.md)
- [Location forms](forms.md)
- [Location templates](templates.md)
- [Authorization](../../docs/architecture/authorization.md)
- [URL reference](../../docs/reference/urls.md)
