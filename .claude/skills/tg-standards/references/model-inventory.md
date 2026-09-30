# Model inventory

Where each model family lives and which base it extends, so a new model lands next to its
relatives with the right base. Generated from the installed models; re-check with the
snippet at the end before relying on a count. Per-model detail is in the app docs
([characters/docs/models.md](../../../../characters/docs/models.md),
[core/docs/models.md](../../../../core/docs/models.md),
[game/docs/models.md](../../../../game/docs/models.md)).

Legend: **Human** = `characters.models.core.human.Human` subclass; **CharacterModel** =
other character; **Group** = `characters.models.core.group.Group`; **Model** =
`core.models.Model` (owned, approvable, often reference data); **plain** = ordinary
`models.Model` (often with `ValidatedSaveMixin`) or `Statistic`.

## characters (`characters/models/<gameline>/`)

| Gameline | Human | Group | Model | plain |
|----------|-------|-------|-------|-------|
| core | Human (plus `Character`, `CharacterModel` roots) | Group | Archetype, Derangement, MeritFlaw, Specialty | Ability, Attribute, Background, BackgroundRating, MeritFlawRating, PooledBackgroundRating, Statistic |
| vampire | VtMHuman, Vampire, Ghoul, Revenant | Coterie | VampireClan, VampireSect, VampireTitle, Path | Discipline, RevenantFamily |
| werewolf | WtAHuman, Werewolf, Kinfolk, Fomor, Drone, Fera and the Fera breeds (Ajaba, Ananasi, Bastet, Corax, Grondr, Gurahl, Kitsune, Mokole, Nagah, Nuwisha, Ratkin, Rokea); CharacterModel: SpiritCharacter | Pack | Tribe, Camp, Gift, Rite, Totem, SpiritCharm, FomoriPower, BattleScar, RenownIncident, SeptPosition | GiftPermission |
| mage | MtAHuman, Mage, Sorcerer, Companion | Cabal | MageFaction, Paradigm, Practice, SpecializedPractice, CorruptedPractice, Instrument, Tenet, Resonance, Rote, Effect, Advantage, LinearMagicPath, LinearMagicRitual, SorcererFellowship | Sphere, PracticeRating, ResRating, AdvantageRating, PathRating |
| wraith | WtOHuman, Wraith | Circle | WraithFaction, Guild, Arcanos, Thorn, ShadowArchetype | Fetter, Passion, ThornRating |
| changeling | CtDHuman, Changeling, AutumnPerson, Inanimae, Nunnehi | Motley | Kith, House, HouseFaction, Legacy, Cantrip, Chimera | |
| demon | DtFHuman, Demon, Thrall, Earthbound | Conclave | DemonHouse, DemonFaction, Lore, Ritual, Visage, ApocalypticForm, ApocalypticFormTrait | LoreRating, Pact |
| hunter | HtRHuman, Hunter | | | Creed, Edge, HunterOrganization |
| mummy | MtRHuman, Mummy | | | Dynasty, MummyTitle |

Character types route through `characters.views.core.GenericCharacterDetailView`
(`view_mapping` by `type`) and, when they have a chargen wizard, a workflow in
`characters/chargen/definitions.py`.

## items (`items/models/<gameline>/`, all `ItemModel` unless noted)

| Gameline | Models |
|----------|--------|
| core | ItemModel, Weapon, MeleeWeapon, RangedWeapon, ThrownWeapon; plain: Material, Medium |
| vampire | VampireArtifact, Bloodstone |
| werewolf | Fetish, Talen |
| mage | Wonder, Artifact, Charm, Talisman, Periapt, Grimoire, SorcererArtifact; plain: WonderResonanceRating |
| wraith | WraithArtifact, WraithRelic |
| changeling | Treasure, Dross |
| demon | Relic |
| hunter | HunterGear, HunterRelic |
| mummy | MummyRelic, Vessel, Ushabti; plain: RelicResonanceRating |

Every concrete `ItemModel` has a `ModelSpec` in `items/registry.py` ([registry.md](registry.md)).

## locations (`locations/models/<gameline>/`, all `LocationModel` unless noted)

| Gameline | Models |
|----------|--------|
| core | LocationModel, City |
| vampire | Haven, Domain, Elysium, Rack, Barrens, TremereChantry; plain: HavenMeritFlawRating |
| werewolf | Caern |
| mage | Node, Sanctum, Chantry, Library, Demesne, HorizonRealm, ParadoxRealm, Sector; plain: RealityZone, ZoneRating, ChantryBackgroundRating, NodeMeritFlawRating, NodeResonanceRating, HorizonRealmMeritFlawRating, HorizonRealmResonanceRating, ParadoxAtmosphere, ParadoxObstacle |
| wraith | Citadel, Haunt, Necropolis, Nihil, Byway, WraithFreehold |
| changeling | Freehold, Holding, Trod, DreamRealm |
| demon | Bastion, Reliquary |
| hunter | Safehouse, HuntingGround |
| mummy | Tomb, CultTemple, UndergroundSanctuary; plain: TombMeritFlawRating |

Every concrete `LocationModel` has a `ModelSpec` in `locations/registry.py`.

## core, game, accounts

| App | Base | Models |
|-----|------|--------|
| core | `Model` | CharacterTemplate |
| core | plain | Book, BookReference, Language, NewsItem, HouseRule, Noun, Number, Observer, TemplateApplication |
| game | plain | Chronicle, Gameline, STRelationship, ObjectType, SettingElement, Story, Week, Scene, Post, UserSceneReadStatus, Journal, JournalEntry, WeeklyXPRequest, StoryXPRequest, XPSpendingRequest, FreebieSpendingRecord |
| accounts | plain | Profile |

`widgets` and `tg_schema` have no models.

## Unique `type` values

No two `core.models.Model` subclasses in one app share a `type` string;
`core/tests/test_model_types.py` fails on a duplicate. Where a line needs a name another
line already uses, prefix it with the line (`demon_house`, `wraith_relic`,
`wraith_artifact`). `type` is a class attribute, not a column, so renaming one needs no
schema change; it does change `get_type()`, the label list pages show.

## Re-generating

```bash
DJANGO_SETTINGS_MODULE=tg.settings python -c "
import django; django.setup()
from django.apps import apps
from core.models import Model
for m in sorted(apps.get_models(), key=lambda m: (m._meta.app_label, m.__module__)):
    if m._meta.app_label in {'characters', 'items', 'locations', 'core', 'game', 'accounts'}:
        print(m._meta.label, m.__module__, getattr(m, 'type', ''), issubclass(m, Model))
"
```

## See also

- [docs/architecture/data-model.md](../../../../docs/architecture/data-model.md)
- [models.md](models.md), [registry.md](registry.md), [domain.md](domain.md)
