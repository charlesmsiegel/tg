# Complete Model Inventory

All 186+ models in the World of Darkness RPG Management System, organized by app and gameline.

## Summary Statistics

- **Total Models:** 186+
- **Admin Registered:** 87 (82%)
- **Missing Admin:** 11 (18%)
- **Complete CRUD Views:** 45 models
- **Partial Views:** 35 models
- **No Views:** 11 models

---

## CORE & SHARED MODELS (34)

### Core App (5 models)
- `Book` - Game books and source material
- `BookReference` - Page references in books
- `NewsItem` - Site news items
- `Language` - Language definitions
- `HouseRule` - Campaign house rules

### Game App (15 models)
- `Chronicle` - Campaign/chronicle definitions
- `Scene` - Individual game sessions
- `Story` - Multi-scene story arcs
- `Week` - Weekly tracking for XP
- `Journal` - Character journals
- `JournalEntry` - Individual journal entries
- `Post` - Scene posts/messages
- `UserSceneReadStatus` - Track scene read status
- `WeeklyXPRequest` - XP requests by week
- `StoryXPRequest` - XP requests by story
- `STRelationship` - Storyteller to chronicle relationship
- `ObjectType` - Types of game objects (character/item/location)
- `SettingElement` - Common knowledge elements
- `Gameline` - Game line definitions

### Accounts App (1 model)
- `Profile` - User profile with theme/ST status

### Base Model (1)
- `core.models.Model` - Abstract base for all polymorphic models

---

## CHARACTER MODELS BY GAMELINE

### Core/Shared Character Models (22 models)
**Base Classes:**
- `Character` - Base polymorphic character
- `CharacterModel` - Polymorphic proxy/grouping
- `Human` - Base playable character

**Trait Systems:**
- `MeritFlaw` - Merit/Flaw definitions
- `MeritFlawBlock` - Merit/Flaw container on character
- `MeritFlawRating` - Individual merit/flaw ratings
- `Derangement` - Mental derangements

**Stat Systems:**
- `Ability` - Skills/abilities
- `AbilityBlock` - Container for abilities
- `Attribute` - Physical/social/mental attributes
- `AttributeBlock` - Container for attributes
- `Specialty` - Skill specialties
- `Statistic` - Generic statistic

**Background System:**
- `Background` - Background definitions
- `BackgroundBlock` - Container for backgrounds
- `BackgroundRating` - Individual background ratings
- `PooledBackgroundRating` - Shared background pool

**Other:**
- `Archetype` - Character archetypes
- `Group` - Character groups/coteries/packs
- `HealthBlock` - Damage track
- `HumanUrlBlock` - URL block for humans

---

### Vampire: The Masquerade (1 model)
- `VtMHuman` - Vampire character (extends Human)

---

### Werewolf: The Apocalypse (19 models)
**Playable Characters:**
- `Werewolf` - Base werewolf (Garou)
- `WtAHuman` - Garou character (extends Human)
- `Bastet` - Bastet race
- `Corax` - Corax race
- `Gurahl` - Gurahl race
- `Mokole` - Mokole race
- `Nuwisha` - Nuwisha race
- `Ratkin` - Ratkin race
- `Fera` - Other fera

**Organization:**
- `Tribe` - Tribal affiliation
- `Camp` - Camp/philosophy within tribe
- `Pack` - Organized group of werewolves
- `Totem` - Pack totem spirits

**Powers & Traits:**
- `Gift` - Werewolf gift/power
- `GiftPermission` - Permissions to use gifts
- `Rite` - Rituals
- `RenownIncident` - Renown-generating events
- `BattleScar` - Battle scar traits

**Other Entities:**
- `Kinfolk` - Half-human relatives
- `SpiritCharacter` - Spirit characters
- `SpiritCharm` - Spirit charms/powers
- `Fomor` - Fomorian characters
- `FomoriPower` - Fomorian powers

---

### Mage: The Ascension (33 models)
**Playable Characters:**
- `Mage` - Mage character (extends Human)
- `MtAHuman` - Mage character (extends Human)
- `Sorcerer` - Sorcerer character
- `Companion` - Familiar/companion

**Powers & Knowledge:**
- `Paradigm` - Magical paradigm/belief system
- `Practice` - Magical practice type
- `SpecializedPractice` - Specialized practice variant
- `CorruptedPractice` - Corrupted practice
- `Sphere` - Sphere of magic
- `Effect` - Magical effect
- `Rote` - Formalized spell
- `Resonance` - Personal resonance trait
- `Focus` - Magical focus

**Traditions & Conventions:**
- `Tenet` - Paradigm tenet
- `Instrument` - Magical instrument
- `Cabal` - Cabal group
- `MageFaction` - Faction (Tradition/Convention)
- `SorcererFellowship` - Sorcerer fellowship

**Ratings & Relationships:**
- `ResRating` - Resonance rating per mage
- `PracticeRating` - Practice skill rating
- `AdvantageRating` - Companion advantage rating
- `Advantage` - Companion advantage
- `PathRating` - Linear magic path rating
- `LinearMagicPath` - Linear magic path
- `LinearMagicRitual` - Linear magic ritual

---

### Wraith: The Oblivion (10 models)
**Playable Characters:**
- `Wraith` - Wraith character (extends Human)
- `WtOHuman` - Wraith character (extends Human)

**Powers & Traits:**
- `Guild` - Wraith guild affiliation
- `Arcanos` - Wraith arcane power
- `Fetter` - Emotional connection to living world
- `Passion` - Personal passion/motivation
- `ShadowArchetype` - Shadow archetype
- `Thorn` - Internal conflict

**Other:**
- `WraithFaction` - Faction/group
- `ThoronRating` - Thorn rating (typo in actual code)

---

### Changeling: The Dreaming (11 models)
**Playable Characters:**
- `Changeling` - Changeling character (extends Human)
- `CtDHuman` - Changeling character (extends Human)

**Traits & Organization:**
- `House` - Changeling house affiliation
- `HouseFaction` - House faction
- `Kith` - Changeling kith (race)
- `Motley` - Motley group
- `Legacy` - Changeling legacy/lineage

**Powers & Traits:**
- `Cantrip` - Changeling magic
- `Chimera` - Chimeric creature

---

### Demon: The Fallen (11 models) **[INCOMPLETE]**
**Playable Characters:**
- `Demon` - Demon character **[NO VIEWS/ADMIN]**
- `DtFHuman` - Demon human form **[NO VIEWS/ADMIN]**

**Powers & Traits:**
- `Visage` - Demonic visage **[NO VIEWS/ADMIN]**
- `Lore` - Demonic lore/knowledge **[NO VIEWS/ADMIN]**
- `LoreBlock` - Container for lores
- `LoreRating` - Individual lore rating
- `Pact` - Demonic pact **[NO VIEWS/ADMIN]**
- `Thrall` - Demon servant/thrall **[NO VIEWS/ADMIN]**
- `Thorn` - Demon weakness/contradiction **[NO VIEWS/ADMIN]**
- `ApocalypticFormTrait` - Apocalyptic form trait

**Organization:**
- `DemonFaction` - Demon faction **[NO VIEWS/ADMIN]**
- `DemonHouse` - Demon house **[NO VIEWS/ADMIN]**

---

## ITEM MODELS BY GAMELINE

### Core/Shared Items (8 models)
**Base Classes:**
- `ItemModel` - Base polymorphic item

**Weapon System:**
- `Weapon` - Base weapon
- `MeleeWeapon` - Melee weapon
- `RangedWeapon` - Ranged weapon (bow, crossbow, etc.)
- `ThrownWeapon` - Thrown weapon

**Crafting Materials:**
- `Material` - Material/crafting material
- `Medium` - Medium/crafting medium

---

### Mage Items (7 models)
- `Artifact` - Artifact/magical item
- `Wonder` - Wonder (creation)
- `Talisman` - Talisman (enchanted item)
- `Charm` - Charm/enchanted item
- `Grimoire` - Grimoire/spell book
- `SorcererArtifact` - Sorcerer artifact
- `WonderResonanceRating` - Wonder resonance rating

---

### Werewolf Items (2 models)
- `Fetish` - Fetish item
- `Talen` - Talen/one-time use item

---

### Wraith Items (2 models)
- `WraithRelic` - Wraith relic
- `Artifact` - Wraith artifact (note: same name as Mage artifact)

---

### Changeling Items (1 model)
- `Treasure` - Changeling treasure

---

### Demon Items (1 model) **[INCOMPLETE]**
- `Relic` - Demon relic **[NO VIEWS/ADMIN]**

---

## LOCATION MODELS BY GAMELINE

### Core/Shared Locations (2 models)
- `LocationModel` - Base polymorphic location
- `City` - City location

---

### Mage Locations (7 models)
- `Node` - Nodes of power
- `Chantry` - Mage tower/chantry
- `Library` - Magical library
- `Sanctum` - Sanctum safehold
- `Sector` - Umbral sector
- `RealityZone` - Reality zone/mage pocket realm
- `HorizonRealm` - Horizon realm
- `NodeMeritFlawRating` - Node merit/flaw rating
- `NodeResonanceRating` - Node resonance rating
- `ChantryBackgroundRating` - Chantry background rating
- `ZoneRating` - Reality zone rating

---

### Werewolf Locations (1 model)
- `Caern` - Sacred Caern (werewolf holy site)

---

### Wraith Locations (2 models) **[INCOMPLETE]**
- `Haunt` - Haunted location **[NO VIEWS/ADMIN]**
- `Necropolis` - Necropolis/Wraith city **[NO VIEWS/ADMIN]**

---

## MODELS BY ADMIN REGISTRATION STATUS

### Fully Registered (87 models)

**Characters (64):**
All core models, VtM, WtA, MtA, WtO, CtD models registered
Demon models NOT registered

**Items (13):**
All core items, Mage, Werewolf items registered
Wraith, Changeling, Demon items mostly registered

**Locations (9):**
Core locations, Mage, Werewolf locations registered
Wraith Haunt/Necropolis NOT registered

**Game (12):**
Chronicle, Scene, Story, Week, Post, STRelationship registered
Journal, JournalEntry NOT registered

**Core (5):**
Book, BookReference, NewsItem, Language, HouseRule registered

**Accounts (1):**
Profile registered

### Not Registered (11 models)
- Demon character models (9): Demon, DtFHuman, DemonFaction, DemonHouse, Visage, Lore, Pact, Thrall, Thorn
- Wraith locations (2): Haunt, Necropolis
- Game models (2): Journal, JournalEntry

---

## MODELS BY VIEW IMPLEMENTATION STATUS

### Full CRUD (Create, Update, Detail, List) - 45 models
Core traits, all major character types per gameline, most mage/werewolf models

### Partial CRUD (Detail, Create, Update) - 35 models
Human variants, groups, organizations, sorcerer/companion models

### Detail Only - 10 models
CharacterModel, Sphere, some trait models

### No Views - 11 models
Demon game line (9), Wraith Haunt/Necropolis (2)

---

## MODELS BY TEMPLATE COVERAGE

### Complete Templates - 107 models
All major character types, items, locations have form.html and detail.html

### Missing Templates - 11 models
Demon models (9), Wraith Haunt/Necropolis (2)

---

## URL PATTERNS

### Characters
Base path: `/characters/`
Gamelines: `vampire/`, `werewolf/`, `mage/`, `wraith/`, `changeling/`
Missing: `demon/` gameline entirely

### Items
Base path: `/items/`
Gamelines: `core/`, `mage/`, `werewolf/`
Partial: Missing demon, wraith, changeling item URLs

### Locations
Base path: `/locations/`
Gamelines: `core/`, `mage/`, `werewolf/`
Partial: Missing wraith, changeling, demon location URLs

---

