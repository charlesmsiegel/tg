# Reference data models

This page lists the game-reference catalogues that live in the `characters` app: the rows
a character sheet points at, such as clans, Disciplines, tribes, Gifts, Spheres, Arcanoi,
kiths and Lores. It is for developers adding a catalogue or a field to one, and for agents
looking up where a trait's reference row is stored. The shared core catalogues (archetypes,
derangements, specialties, merits and flaws, and the `Statistic` rows for Attributes,
Abilities and Backgrounds) are on [Character models](models.md#core-reference-models).

For the step-by-step recipe, see
[Adding reference data](../../docs/guides/adding-reference-data.md). Reference rows are
loaded by the `populate_db` scripts (see [Seed data](../../docs/getting-started/seed-data.md)).

## Kinds of reference model

| Kind | Base | What it carries |
|------|------|-----------------|
| Catalogue object | `core.models.Model` (polymorphic) | `name`, `description`, `sources`, and the `owner` / `chronicle` / `status` / `visibility` columns every `core` model has (see [`core/models.py`](../../core/models.py)) |
| Statistic | `characters.models.core.statistic.Statistic` (polymorphic) | `name` and `property_name`, the name of the rating field on the character model. `Discipline` and `Sphere` are statistics |
| Plain table | `django.db.models.Model` | Only its own fields: `RevenantFamily`, `GiftPermission`, `Creed`, `Edge`, `HunterOrganization`, `Dynasty`, `MummyTitle` |

## Access

Reference detail and list views use the `PUBLIC_READ` route policy: they need no login.
Their create and update views use `STAFF_WRITE`: staff or superusers only. A few models on
this page are player content and use the object policies instead (`OBJECT_CREATE`,
`OBJECT_DETAIL`, `OBJECT_LIST`, `OBJECT_WRITE`): Mage `Effect` and `Rote`, and Changeling
`Chimera`. The policies are defined in [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py)
and explained in [Authorization](../../docs/architecture/authorization.md).

Every catalogue has `create:`, `update:` and usually `list:` routes in its gameline
namespace; the route names are given below and listed in full in
[Views and URLs](views-and-urls.md).

## Vampire

Source: [`characters/models/vampire/`](../models/vampire/). Namespace `characters:vampire:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `VampireClan` | Catalogue | `nickname`, `disciplines` (`ManyToManyField(Discipline)`, reverse `clans`), `weakness`, `is_bloodline`, `parent_clan` (`ForeignKey("self")`, reverse `bloodlines`); `get_all_disciplines()` adds the parent clan's for bloodlines | `clan` |
| `Discipline` | Statistic | `description`. `save()` fills a missing `property_name` from the slugified name when it matches a field in `VAMPIRE_DISCIPLINES` | `discipline` |
| `Path` | Catalogue | `requires_conviction`, `requires_instinct` (which virtues a follower uses), `ethics`; `check_character_virtues()`, `update_character_virtues()`, `get_virtues_display()` | `path` |
| `VampireSect` | Catalogue | `philosophy` | `sect` |
| `VampireTitle` | Catalogue | `sect` (`ForeignKey(VampireSect)`, reverse `titles`), `value`, `is_negative`, `powers` | `title` |
| `RevenantFamily` | Plain | `name` (unique), `description`, `weakness`, `disciplines` (reverse `revenant_families`) | `revenant_family` |

## Werewolf

Source: [`characters/models/werewolf/`](../models/werewolf/). Namespace `characters:werewolf:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `Tribe` | Catalogue | `willpower` (starting Willpower, default `3`); `get_camps()`, `get_gifts_by_rank(rank)` and properties `gifts_1` ... `gifts_6` | `tribe` |
| `Camp` | Catalogue | `tribe` (`ForeignKey(Tribe)`), `camp_type` (`camp`, `lodge`, `house`, `philosophy`) | `camp` |
| `Gift` | Catalogue | `rank`, `allowed` (`ManyToManyField(GiftPermission)`) | `gift` |
| `GiftPermission` | Plain | `shifter`, `condition` (see [Gift permissions](models-werewolf.md#gift-permissions)) | none |
| `Rite` | Catalogue | `level`, `rite_type` | `rite` |
| `Totem` | Catalogue | `cost`, `totem_type` (`respect`, `war`, `wisdom`, `cunning`), `individual_traits`, `pack_traits`, `ban` | `totem` |
| `SpiritCharm` | Catalogue | `essence_cost`, `point_cost` | `spirit_charm` (list: `charm`) |
| `FomoriPower` | Catalogue | none beyond the base | `fomoripower` |
| `BattleScar` | Catalogue | `glory` | `battlescar` |
| `RenownIncident` | Catalogue | `glory`, `honor`, `wisdom`, `posthumous`, `only_once`, `breed`, `rite` (`ForeignKey(Rite)`) | `renownincident` |
| `SeptPosition` | Catalogue | none beyond the base (a `POSITION_TYPES` list is declared but not stored); no list route | `septposition` |

## Mage

Source: [`characters/models/mage/`](../models/mage/). Namespace `characters:mage:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `Sphere` | Statistic | none beyond `name` / `property_name`; `get_heading()` | `sphere` |
| `MageFaction` | Catalogue | `parent` (`ForeignKey("self")`: affiliation, faction, subfaction), `founded`, `ended`, `languages`, `affinities` (Spheres), `paradigms`, `practices`, `media` (`items.Medium`), `materials` (`items.Material`); `get_all_paradigms()` and `get_all_practices()` walk up the parents | `mage_faction` |
| `Paradigm` | Catalogue | `tenets`; `get_associated_practices()`, `get_limited_practices()`, `get_intersection_practices()` | `paradigm` |
| `Tenet` | Catalogue | `tenet_type` (`met`, `per`, `asc`, `oth`), `associated_practices`, `limited_practices` | `tenet` |
| `Practice` | Catalogue | `benefit`, `penalty`, `abilities`, `instruments`, `common_resonance_traits`; `get_rotes()` | `practice` (detail through the `GenericPracticeDetailView` router) |
| `SpecializedPractice` | `Practice` | `parent_practice` (reverse `specialization`), `faction`, `extra_benefit` | `specialized_practice` |
| `CorruptedPractice` | `Practice` | `parent_practice` (reverse `corruption`), `extra_benefit`, `price` | `corrupted_practice` |
| `Instrument` | Catalogue | none beyond the base | `instrument` |
| `Resonance` | Catalogue | one boolean per Sphere; `associated_spheres()` | `resonance` |
| `Effect` | Player object | one integer per Sphere, `rote_cost`, `max_sphere` (both computed in `save()`); `cost()`, `is_learnable(mage)`, `spheres()` | `effect` |
| `Rote` | Player object | `effect`, `practice`, `attribute`, `ability`; `random_name()`, `random()` | `rote` |
| `SorcererFellowship` | Catalogue | `favored_attributes`, `favored_paths` | `sorcerer_fellowship` |
| `LinearMagicPath` | Catalogue | `numina_type` (`hedge_magic`, `psychic`); `property_name` property | `path` |
| `LinearMagicRitual` | Catalogue | `path` (`ForeignKey(LinearMagicPath)`), `level` | `ritual` |
| `Advantage` | Catalogue | `ratings` (`core.Number`), `max_rating`, `min_rating`; same rating helpers as `MeritFlaw` | `advantage` (detail only) |

## Wraith

Source: [`characters/models/wraith/`](../models/wraith/). Namespace `characters:wraith:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `Arcanos` | Catalogue | `arcanos_type` (`standard`, `dark`), `level`, `pathos_cost`, `angst_cost`, `difficulty`, `parent_arcanos` (reverse `levels`) | `arcanos` |
| `Guild` | Catalogue | `guild_type` (`greater`, `lesser`, `banned`), `willpower` (default `5`) | `guild` |
| `WraithFaction` | Catalogue | `faction_type` (`legion`, `guild`, `heretic`, `spectre`, `other`), `parent` (reverse `subfactions`) | `faction` |
| `ShadowArchetype` | Catalogue | `point_cost`, `core_function`, `modus_operandi`, `dominance_behavior`, `effect_on_psyche`, `strengths`, `weaknesses` | `shadow_archetype` |
| `Thorn` | Catalogue | `thorn_type` (`individual`, `collective`), `point_cost`, `activation_cost`, `activation_trigger`, `mechanical_description`, `resistance_system`, `resistance_difficulty`, `duration`, `frequency_limitation`, `limitations` | `thorn` |

## Changeling

Source: [`characters/models/changeling/`](../models/changeling/). Namespace
`characters:changeling:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `Kith` | Catalogue | `affinity`, `birthrights` (JSON list), `frailty` | `kith` |
| `House` | Catalogue | `court` (`seelie`, `unseelie`), `boon`, `flaw`, `factions` (`ManyToManyField(HouseFaction)`) | `house` |
| `HouseFaction` | Catalogue | none beyond the base | `house_faction` |
| `Legacy` | Catalogue | `court` | `legacy` |
| `Cantrip` | Catalogue | `art`, `primary_realm`, `modifier_realms` (JSON), `level` (1 to 5), `glamour_cost`, `difficulty`, `duration`, `range`, `effect`, `type_of_effect` (`chimerical`, `wyrd`, `both`), `bunk_examples` (JSON) | `cantrip` |
| `Chimera` | Player object | `chimera_type`, `chimera_points`, `sentience_level`, `behavior`, `appearance`, `durability`, `special_abilities` (JSON), `can_interact_with_physical`, `loyalty`, `creator`, `origin`, `is_permanent`, `dream_source` | `chimera` |

## Demon

Source: [`characters/models/demon/`](../models/demon/). Namespace `characters:demon:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `DemonHouse` | Catalogue | `celestial_name`, `starting_torment` (default `3`), `domain` | `house` |
| `DemonFaction` | Catalogue | `philosophy`, `goal`, `leadership`, `tactics` | `faction` |
| `Lore` | Catalogue | `property_name` (the `LoreBlock` field without `lore_of_` / `the_`), `houses` (reverse `lores`) | `lore` |
| `Visage` | Catalogue | `house` (`ForeignKey(DemonHouse, CASCADE)`, reverse `visages`), `default_apocalyptic_form` | `visage` |
| `ApocalypticFormTrait` | Catalogue | `cost`, `house` (reverse `apocalyptic_traits`), `high_torment_only` | `apocalyptic_trait` |
| `Ritual` | Catalogue | `house`, `primary_lore`, `primary_lore_rating`, `secondary_lore_requirements` (JSON), `base_cost`, `restrictions`, `minimum_casting_time`, `system`, `torment_effect`, `variations`, `flavor_text`, `source_page`; `total_lore_dots()`, `get_secondary_lores()` | `ritual` |

`Pact` (a Demon-Thrall link; see [Demon models](models-demon.md#pact)) is not reference
data: it is per-character. Its detail and list views under `characters:demon:pact` are
`LOGIN` routes that show a pact only to users with `VIEW_FULL` on its demon or its thrall
(others get 404; the list leaves such pacts out, staff see all); create and update are
`STAFF_WRITE`.

## Hunter

Source: [`characters/models/hunter/`](../models/hunter/). Namespace `characters:hunter:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `Creed` | Plain | `name` (unique), `primary_virtue` (`conviction`, `vision`, `zeal`), `philosophy`, `nickname`, `description`, `favored_edges` (JSON) | `creed` |
| `Edge` | Plain | `name`, `virtue`, `level`, `cost`, `duration`, `system`, `book` (`ForeignKey("core.Book")`) | `edge` |
| `HunterOrganization` | Plain | `organization_type` (`cell`, `network`, `compact`, `conspiracy`), `philosophy`, `goals`, `resources`, `leader` (`ForeignKey(Hunter)`, reverse `led_organizations`), `members` (reverse `organizations`) | `organization` |

## Mummy

Source: [`characters/models/mummy/`](../models/mummy/). Namespace `characters:mummy:`.

| Model | Kind | Fields | Route name |
|-------|------|--------|------------|
| `Dynasty` | Plain | `name` (unique), `description`, `era`, `favored_hekau` | `dynasty` |
| `MummyTitle` | Plain | `name` (unique), `rank_level`, `description` | `title` |

## See also

- [Character models](models.md)
- [Adding reference data](../../docs/guides/adding-reference-data.md)
- [Seed data](../../docs/getting-started/seed-data.md)
- [Authorization](../../docs/architecture/authorization.md)
- [Views and URLs](views-and-urls.md)
