# locations

The `locations` app models the places of a chronicle: cities and generic locations,
Vampire havens and domains, Werewolf caerns, Mage chantries, nodes and realms,
Changeling freeholds, Wraith haunts and necropoli, Demon bastions, Hunter safehouses
and Mummy tombs. This page is the entry point for developers and coding agents working
in the app; the detailed reference lives in [`docs/`](docs/).

## Main concepts

- **`LocationModel`** ([`models/core/location.py`](models/core/location.py)) is the
  polymorphic base of every place. It extends `core.models.Model` (owner, chronicle,
  status, visibility, sources, description, image), adds the three barrier ratings
  (`gauntlet`, `shroud`, `dimension_barrier`), a `creation_status` wizard counter, an
  owning character (`owned_by`) and **containment**: `contained_within` places a
  location inside one or more others.
- **Gameline subclasses** live under `models/<gameline>/`. Several recompute fields on
  save (for example a haven's total rating, a tomb's rank, a caern's gauntlet). See
  [models](docs/models.md).
- **Reference data** that is not a location: `RealityZone` (a set of practice
  ratings) is a plain model that nodes, sanctums, demesnes, realms and sectors point to.
- **The registry** ([`registry.py`](registry.py)) declares each routable model's URLs,
  access policy per action, fields or form class, and templates. Views and URL patterns
  are built from it; see [views and URLs](docs/views-and-urls.md).
- **Creation wizards**: a Mage chantry is built in a seven-step wizard that spends
  points on backgrounds and Integrated Effects ([chantries](docs/chantries.md)); a
  Changeling freehold has a four-step wizard ([freeholds](docs/freeholds.md)).
- **Point-built places**: nodes and reality zones ([nodes](docs/nodes.md)), and
  Horizon and Paradox realms with random generation ([realms](docs/realms.md)).

## Key modules

| Path | Responsibility |
|------|----------------|
| [`models/`](models/) | `LocationModel`, `City`, and the subclasses for each gameline |
| [`registry.py`](registry.py) | One `ModelSpec` per routable model |
| [`services/chantry_points.py`](services/chantry_points.py) | The single source of chantry point costs, caps and purchase/refund mutations |
| [`views/`](views/) | Registry-built views, the staff index, the polymorphic detail router, the chantry and freehold wizards |
| [`urls/`](urls/) | URL modules; each asks the registry for its routes and adds the wizard entry points |
| [`forms/`](forms/) | Type chooser, owner-limited edit form, chantry wizard forms, node/sanctum/demesne forms with reality-zone formsets, freehold wizard forms, paradox realm forms |
| [`templates/locations/`](templates/locations/) | Spread templates: shells in `core/` and `tl/`, one folder per type |
| [`static/locations/js/`](static/locations/js/) | Behaviour for the chantry effects step and the freehold forms |
| [`admin.py`](admin.py) | Django admin registrations |
| [`tests/`](tests/) | Model, form, service, view, URL and authorization tests |

## How it connects to other apps

- **core**: base model, registry machinery (`core.model_registry`), route policies,
  public projection views, the approval service (`core.services.approval`, which calls
  a chantry's `submission_errors()` and `on_returned_for_revision()` hooks), and the
  shared fallback templates in `core/templates/core/registry/`.
- **characters**: `LocationModel.owned_by`, `City.characters`, chantry personnel and
  cabals, and many Mage statistics (Effects, Resonance, practices, merits and flaws,
  backgrounds). Mage-family character wizards reuse `NodeForm`, `LibraryForm`,
  `SanctumForm` and `ChantrySelectOrCreateForm` and their templates for background
  steps.
- **items**: a Mage `Library` holds `items.Grimoire` books; `ItemModel.located_at`
  points at locations.
- **game**: `game.Scene.location` points at a location (`LocationModel.get_scenes()`);
  locations belong to a `game.Chronicle`.
- **populate_db**: loads the example Sectors in `populate_db/mage/sectors.py` (see
  [`populate_db/README.md`](../populate_db/README.md)).

## Admin

[`admin.py`](admin.py) registers `LocationModel`, `City`, `Sanctum`, `Node`,
`NodeMeritFlawRating`, `NodeResonanceRating`, `Library`, `Sector`, `HorizonRealm`,
`RealityZone`, `ZoneRating`, `Caern`, `Chantry`, `ChantryBackgroundRating`, `Haunt`,
`Necropolis`, `Haven`, `HavenMeritFlawRating`, `Domain`, `Elysium`, `Rack`,
`TremereChantry`, `Barrens`, `Freehold`, `Bastion` and `Reliquary`. The other types
(for example `Demesne`, `ParadoxRealm`, `DreamRealm`, `Holding`, `Trod`, `Byway`,
`Citadel`, `WraithFreehold`, `Nihil`, `HuntingGround`, `Safehouse`, `Tomb`,
`CultTemple`, `UndergroundSanctuary`) have no admin registration.

## Tests

Tests mirror the source tree under [`tests/`](tests/) (`models/`, `forms/`, `views/`
per gameline), plus:

- [`tests/services/test_chantry_points.py`](tests/services/test_chantry_points.py)
  for the chantry point rules;
- [`tests/views/mage/test_chantry_wizard.py`](tests/views/mage/test_chantry_wizard.py),
  `test_chantry_create.py` and `test_chantry_update.py` for the chantry flows;
- [`tests/views/test_authorization.py`](tests/views/test_authorization.py) and
  [`tests/views/test_form_pages.py`](tests/views/test_form_pages.py) across types;
- [`tests/urls/test_url_patterns.py`](tests/urls/test_url_patterns.py) for route names.

Run them with `python manage.py test locations`. See
[`docs/development/testing.md`](../docs/development/testing.md).

## Documentation

| Page | Contents |
|------|----------|
| [docs/models.md](docs/models.md) | Every location model, grouped by gameline |
| [docs/chantries.md](docs/chantries.md) | Mage chantry points, the creation wizard, direct ST forms and character integration |
| [docs/nodes.md](docs/nodes.md) | Nodes, their point budget and output, and reality zones |
| [docs/realms.md](docs/realms.md) | Horizon realm build points and Paradox realm generation |
| [docs/freeholds.md](docs/freeholds.md) | Changeling freehold features, powers and the creation wizard |
| [docs/views-and-urls.md](docs/views-and-urls.md) | Registry, policies, routers, the index and the full URL table |
| [docs/forms.md](docs/forms.md) | Every location form |
| [docs/templates.md](docs/templates.md) | Template layout, shells, partials and chargen includes |

## See also

- [Adding an item or location type](../docs/guides/adding-an-item-or-location-type.md)
- [Data model overview](../docs/architecture/data-model.md)
- [Authorization](../docs/architecture/authorization.md)
- [XP and approvals](../docs/architecture/xp-and-approvals.md)
- [items app](../items/README.md)
