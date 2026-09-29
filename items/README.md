# items

The `items` app holds every object a character can own or carry: weapons, Mage Wonders
and grimoires, Werewolf fetishes, Vampire bloodstones, Changeling treasures, Mummy
relics and the like. This page is the entry point for developers and coding agents
working in the app; the detailed reference lives in [`docs/`](docs/).

## Main concepts

- **`ItemModel`** ([`models/core/item.py`](models/core/item.py)) is the polymorphic
  base of every item. It extends `core.models.Model`, so each item has an owner,
  chronicle, status, visibility, sources, description, public info and image, and
  its `save()` runs `full_clean()`. Items add two relations: `owned_by`
  (characters) and `located_at` (locations).
- **Gameline subclasses** live under `models/<gameline>/` (for example
  `models/mage/wonder.py`). Each sets a `type` string and a `gameline` code.
  See [models](docs/models.md).
- **Reference data** that is not an item: `Material` and `Medium` (grimoire covers
  and writing media) are plain Django models in `models/core/`.
- **The registry** ([`registry.py`](registry.py)) declares, once per routable model,
  its URLs, access policy for each action, form fields or form class, and templates.
  Views and URL patterns are built from it. See
  [views and URLs](docs/views-and-urls.md).
- **Polymorphic detail routing**: `/items/<pk>/` resolves the concrete item type and
  hands the request to that type's detail view.

## Key modules

| Path | Responsibility |
|------|----------------|
| [`models/`](models/) | `ItemModel` and its subclasses, grouped by gameline (`core`, `changeling`, `demon`, `hunter`, `mage`, `mummy`, `vampire`, `werewolf`, `wraith`) |
| [`registry.py`](registry.py) | One `ModelSpec` per routable model: slug, gameline, URL routes, policies, fields, templates |
| [`views/`](views/) | View classes built by the registry, plus the custom behaviour they wrap (`_ItemUpdateView`, `_WonderCreateView`, grimoire context) and the staff index |
| [`urls/`](urls/) | URL modules; each one asks the registry for its routes |
| [`forms/`](forms/) | Item-type chooser, owner-limited edit forms, `WonderForm`, the Vampire artifact forms and the Sorcerer artifact chooser |
| [`templates/items/`](templates/items/) | Spread templates: shared shells in `core/item/` and `tl/`, one folder per item type |
| [`static/items/js/wonder-form.js`](static/items/js/wonder-form.js) | Toggles the create/select halves of each power subform in the Wonder form |
| [`admin.py`](admin.py) | Django admin registrations |
| [`tests/`](tests/) | Model, form, view and authorization tests |

## How it connects to other apps

- **core**: base model and managers (`core.models.Model`, `ModelManager`), the
  registry machinery (`core.model_registry`), route policies
  (`core.route_policy_manifest`, `core.access_policy`), the public projection views
  (`core.views.public_object`), and the shared fallback templates under
  `core/templates/core/registry/`.
- **characters**: `ItemModel.owned_by` points at `characters.CharacterModel`. Mage
  chargen reuses `WonderForm` and `items/mage/wonder/form_include.html`, and the
  Sorcerer wizard uses `ArtifactCreateOrSelectForm`. Grimoires reference Mage
  statistics (spheres, practices, instruments, rotes, factions); several items link
  to `characters.Effect`, `characters.Resonance`, `characters.DemonHouse` and
  `characters.Mummy`.
- **locations**: `ItemModel.located_at` points at `locations.LocationModel`, and a
  Mage `Library` holds `Grimoire` books.
- **game**: items belong to a `game.Chronicle`; the chronicle page offers its own
  item-creation form (`game.forms.ChronicleItemCreationForm`).
- **populate_db**: loads `Material`, `Medium`, weapons and example items (see
  [`populate_db/README.md`](../populate_db/README.md)).

## Admin

[`admin.py`](admin.py) registers `ItemModel`, the four weapon models, `Medium`,
`Material`, `Wonder`, `WonderResonanceRating`, `Charm`, `Talisman`, `Artifact`,
`Grimoire`, `Fetish`, `SorcererArtifact`, `VampireArtifact`, `Bloodstone`, the Demon
`Relic`, `WraithRelic`, `WraithArtifact` and `Treasure`. `Periapt`, `Talen`, `Dross`,
`HunterGear`, `HunterRelic`, `MummyRelic`, `Vessel`, `Ushabti` and
`RelicResonanceRating` have no admin registration; edit them through the site or the
shell.

## Tests

Tests mirror the source tree under [`tests/`](tests/): `tests/models/<gameline>/`,
`tests/forms/<gameline>/` and `tests/views/<gameline>/`. Two cross-cutting modules
are worth knowing:

- [`tests/views/test_authorization.py`](tests/views/test_authorization.py) checks
  that anonymous users and other players cannot edit an item and that creating one
  records the owner.
- [`tests/views/test_spread_forms.py`](tests/views/test_spread_forms.py) walks every
  registry entry and checks that its create and edit pages render every form field
  with Spread markup and no legacy classes.

Run the app's tests with `python manage.py test items`. See
[`docs/development/testing.md`](../docs/development/testing.md) for the test runner
and conventions.

## Documentation

| Page | Contents |
|------|----------|
| [docs/models.md](docs/models.md) | Every item model, grouped by gameline, with fields, computed values and invariants |
| [docs/views-and-urls.md](docs/views-and-urls.md) | The registry, access policies, custom views and the full URL table |
| [docs/forms.md](docs/forms.md) | The item-type chooser, limited edit forms, `WonderForm` and the Vampire artifact forms |
| [docs/templates.md](docs/templates.md) | Template layout, shared shells and blocks, fallbacks and chargen includes |

## See also

- [Adding an item or location type](../docs/guides/adding-an-item-or-location-type.md)
- [Data model overview](../docs/architecture/data-model.md)
- [Authorization](../docs/architecture/authorization.md)
- [locations app](../locations/README.md)
- [core app](../core/README.md)
