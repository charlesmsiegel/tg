# characters

The `characters` app owns every character in the project, for all eight World of Darkness
gamelines, plus the groups they belong to and the game-reference catalogues their sheets
point at (clans, Disciplines, tribes, Gifts, Spheres, Arcanoi, kiths, Lores, creeds,
dynasties and more). It also owns character creation ("chargen"), freebie and XP
spending, and the character sheet. This page is the entry point for developers and agents
working in the app; the pages under [`docs/`](docs/) are the detailed reference.

## Main concepts

- **Polymorphic character tree.** Every character is a `django-polymorphic` row under
  `core.models.Model`: `CharacterModel` → `Character` → `Human` → a gameline mortal
  (`VtMHuman`, `WtAHuman`, `MtAHuman`, `WtOHuman`, `CtDHuman`, `DtFHuman`, `HtRHuman`,
  `MtRHuman`) → the supernatural types (`Vampire`, `Werewolf`, `Mage`, `Wraith`,
  `Changeling`, `Demon`, `Hunter`, `Mummy` and their relatives). `SpiritCharacter` extends
  `Character` directly. Each class sets a `type` string (`"vampire"`, `"wta_human"`) and a
  `gameline` code (`"vtm"`, `"wta"`) that drive URLs, chargen and services.
- **Traits as columns.** Attributes, Abilities and gameline powers (Disciplines, Spheres,
  Arcanoi, Arts, Lores, Edges, Hekau) are integer fields on the model. Backgrounds are
  `BackgroundRating` rows; merits and flaws are `MeritFlawRating` rows.
- **Status machine.** `Un` (unapproved) → `Sub` (submitted) → `App` (approved), with `Rev`
  (returned for revisions), `Ret` (retired) and `Dec` (deceased); allowed moves are in
  `Character.STATUS_TRANSITIONS`.
- **Chargen workflows.** Each type with a wizard has an ordered `Workflow` of steps;
  `creation_status` stores the current 1-based position. The canonical URL
  `characters:character` shows the wizard while a character is `Un` or `Rev` and the sheet
  afterwards.
- **Spending services.** Freebies (at creation) and XP (in play) are spent through one
  service class per character type, selected by `character.type`. XP spends wait for
  storyteller approval; freebie spends apply at once and can be reversed.
- **Reference data.** Catalogue models are public to read and staff-only to edit.

Terms such as ST, freebies, Disciplines and Spheres are defined in the
[glossary](../docs/reference/glossary.md).

## Key modules

| Path | Responsibility |
|------|----------------|
| [`models/core/`](models/core/) | `Character`, `Human`, the attribute / ability / health blocks, backgrounds, merits and flaws, `Group`, core catalogues |
| `models/<gameline>/` | Gameline character types, groups and catalogues (`vampire`, `werewolf`, `mage`, `wraith`, `changeling`, `demon`, `hunter`, `mummy`) |
| [`managers/`](managers/) | `BackgroundManager`, `MeritFlawManager` (plain helper classes behind `Human`) |
| [`chargen/`](chargen/) | Workflow registry, workflow definitions, skip predicates, transitions |
| [`rules/`](rules/) | Pure allocation rules and chargen point pools |
| [`costs.py`](costs.py) | Freebie and XP cost tables |
| [`services/`](services/) | XP and freebie spending services and single-purpose services (status, specialties, rotes, gameline chargen writes) |
| [`forms/`](forms/) | Update allowlists (`forms/core/crud_fields.py`), limited owner forms, chargen, freebie, XP and NPC forms |
| [`views/`](views/) | Routers, sheet and chargen views per gameline, sheet actions, the "Known by" mixin |
| [`urls/`](urls/) | URLconf under `/characters/`, one package per gameline |
| [`templates/characters/`](templates/characters/) | Sheet shell, form shells, chargen templates, reference shells, `tl/` partials |
| [`templatetags/`](templatetags/) | `character_edit`, `startswith` |
| [`static/characters/js/`](static/characters/js/) | Chargen and sheet scripts |
| [`admin.py`](admin.py) | Admin registrations |
| [`utils.py`](utils.py) | `get_character_object_type()` |
| [`tests/`](tests/) | Tests, helpers and golden files |

The app has no migration files: tables come from the current models, and the `tg_schema`
app brings older databases up to date (see
[Schema migrations](../docs/architecture/schema-migrations.md)).

## How it connects to other apps

| App | Relationship |
|-----|--------------|
| `core` | Base `Model` (owner, chronicle, status, visibility), `PermissionManager`, view mixins, `DictView` routers, route policies, `linked_stat`, `CharacterTemplate`, the `tl` template tags |
| `game` | `Chronicle` and `Scene` (characters appear in scenes), `ObjectType` (merit/flaw eligibility and creation pickers), `XPSpendingRequest`, `FreebieSpendingRecord`, spending approval, weekly XP |
| `accounts` | Profile queues of characters to approve and freebies to award; the freebie award calls `Human.award_backstory_freebies()` |
| `items` | Fetishes, Wonders, artifacts, materials and media referenced by characters and Mage chargen steps |
| `locations` | Nodes, libraries, sanctums and chantries created by Mage background steps; the Hunter `safehouse`; chantries register their own cleanup for retired characters |
| `widgets` | Chained selects, conditional fields and dot-rating inputs used by chargen forms |
| `populate_db` | Seed scripts for the reference catalogues |

## Documentation

| Page | Contents |
|------|----------|
| [Character models](docs/models.md) | Core tree, blocks, backgrounds, merits and flaws, groups, core catalogues; index of gameline pages |
| [Vampire](docs/models-vampire.md), [Werewolf](docs/models-werewolf.md), [Mage](docs/models-mage.md), [Wraith](docs/models-wraith.md), [Changeling](docs/models-changeling.md), [Demon](docs/models-demon.md), [Hunter](docs/models-hunter.md), [Mummy](docs/models-mummy.md) | Character types per gameline |
| [Reference data](docs/reference-data.md) | Every catalogue model, by gameline |
| [Forms](docs/forms.md) | Allowlists, limited forms, chargen, freebie, XP and NPC forms |
| [Views and URLs](docs/views-and-urls.md) | URLconf, routers, view families, sheet actions, Known by, routes per gameline |
| [Chargen](docs/chargen.md) | Workflow of every type, point values, gameline steps |
| [Services](docs/services.md) | Spending services, factories, single-purpose services |
| [Costs and rules](docs/costs-and-rules.md) | Cost tables, allocation rules, point pools |
| [Templates](docs/templates.md) | Sheet and form shells, chargen and reference templates, tags, scripts |
| [Admin](docs/admin.md) | Admin registrations |
| [Testing](docs/testing.md) | Test layout, helpers, golden files |

Project-wide context: [Data model](../docs/architecture/data-model.md),
[Character creation](../docs/architecture/character-creation.md),
[XP, freebies and approvals](../docs/architecture/xp-and-approvals.md),
[Authorization](../docs/architecture/authorization.md),
[Adding a character type](../docs/guides/adding-a-character-type.md).

## See also

- [Documentation index](../docs/README.md)
- [`core` app](../core/README.md)
- [`game` app](../game/README.md)
- [Adding reference data](../docs/guides/adding-reference-data.md)
