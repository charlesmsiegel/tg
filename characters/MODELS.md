# Characters App Models

Character models for the World of Darkness RPG system, organized by gameline. All character models inherit from the polymorphic `Character` base class.

## Model Hierarchy

```
core.models.Model (abstract polymorphic base)
└── Character (base character)
    └── Human (base playable character)
        ├── VtMHuman (Vampire)
        ├── WtAHuman/Werewolf (Werewolf)
        ├── MtAHuman/Mage (Mage)
        ├── WtOHuman/Wraith (Wraith)
        ├── CtDHuman/Changeling (Changeling)
        └── DtFHuman/Demon (Demon) ⚠️ INCOMPLETE
```

---

## Core/Shared Models (22 models)

### Base Classes
- **`Character`** - Base polymorphic character class
  - Status: Un (Unfinished), Sub (Submitted), App (Approved), Ret (Retired), Dec (Deceased)
  - XP tracking, visibility settings, chronicle assignment
- **`CharacterModel`** - Polymorphic proxy/grouping model
- **`Human`** - Base class for all playable characters
  - Attributes (Physical/Social/Mental)
  - Abilities (Talents/Skills/Knowledges)
  - Backgrounds, Merits/Flaws, Health

### Trait Systems
- **`MeritFlaw`** - Merit/Flaw definitions
- **`MeritFlawBlock`** - Container for character's merits/flaws
- **`MeritFlawRating`** - Individual merit/flaw with point cost
- **`Derangement`** - Mental derangements

### Stat Systems
- **`Ability`** - Skills and abilities (Alertness, Brawl, Academics, etc.)
- **`AbilityBlock`** - Container for character's abilities
- **`Attribute`** - Physical/Social/Mental attributes (Strength, Charisma, Perception, etc.)
- **`AttributeBlock`** - Container for character's attributes (9 attributes)
- **`Specialty`** - Skill specializations
- **`Statistic`** - Generic statistic tracker

### Background System
- **`Background`** - Background definitions (Resources, Allies, Contacts, etc.)
- **`BackgroundBlock`** - Container for character backgrounds
- **`BackgroundRating`** - Individual background rating
- **`PooledBackgroundRating`** - Shared background pool (for groups)

### Other
- **`Archetype`** - Nature/Demeanor archetypes
- **`Group`** - Character groups (coteries, packs, cabals, motleys)
- **`HealthBlock`** - Damage track and health levels
- **`HumanUrlBlock`** - URL routing helper

---

## Vampire: The Masquerade (1 model)

- **`VtMHuman`** - Vampire character
  - Extends `Human` with vampire-specific traits
  - Clan, Generation, Path, Disciplines
  - Blood Pool, Willpower, Humanity/Path ratings

---

## Werewolf: The Apocalypse (19 models)

### Playable Characters
- **`Werewolf`** - Base werewolf (Garou) character
- **`WtAHuman`** - Garou character (extends Human)
  - Breed, Auspice, Tribe, Renown
  - Rage, Gnosis, Willpower
  - Gifts and Rites
- **`Bastet`** - Bastet werecats
- **`Corax`** - Corax wereravens
- **`Gurahl`** - Gurahl werebears
- **`Mokole`** - Mokole weredragons
- **`Nuwisha`** - Nuwisha werecoyotes
- **`Ratkin`** - Ratkin wererats
- **`Fera`** - Other shapeshifters

### Organization
- **`Tribe`** - Tribal affiliations (Get of Fenris, Glass Walkers, etc.)
- **`Camp`** - Faction within tribe
- **`Pack`** - Organized group of werewolves
- **`Totem`** - Pack totem spirit

### Powers & Traits
- **`Gift`** - Werewolf supernatural powers
- **`GiftPermission`** - Gift access permissions by breed/auspice/tribe
- **`Rite`** - Werewolf rituals
- **`RenownIncident`** - Renown-gaining actions
- **`BattleScar`** - Physical scars from battle

### Other Entities
- **`Kinfolk`** - Half-human relatives
- **`SpiritCharacter`** - Spirit entities
- **`SpiritCharm`** - Spirit powers
- **`Fomor`** - Bane-possessed creatures
- **`FomoriPower`** - Fomori abilities

---

## Mage: The Ascension (33 models)

### Playable Characters
- **`Mage`** - Mage character
- **`MtAHuman`** - Mage character (extends Human)
  - Tradition/Convention, Essence, Focus
  - Spheres, Arete, Quintessence, Paradox
  - Resonance, Paradigm, Practices
- **`Sorcerer`** - Linear magic practitioner
  - Paths, Rituals, Numina
- **`Companion`** - Familiar/companion creature

### Powers & Knowledge
- **`Paradigm`** - Magical belief system
- **`Practice`** - Magical practice style
- **`SpecializedPractice`** - Specialized practice variant
- **`CorruptedPractice`** - Corrupted/tainted practice
- **`Sphere`** - Sphere of magic (Correspondence, Forces, Life, etc.)
- **`Effect`** - Magical effect/spell
- **`Rote`** - Formalized rote spell
- **`Resonance`** - Personal magical resonance
- **`Focus`** - Magical focus tools/paradigm elements

### Traditions & Conventions
- **`Tenet`** - Paradigm tenet/belief
- **`Instrument`** - Magical instrument/tool
- **`Cabal`** - Mage group/cabal
- **`MageFaction`** - Tradition/Convention/Craft faction
- **`SorcererFellowship`** - Sorcerer organization

### Ratings & Relationships
- **`ResRating`** - Resonance rating per mage
- **`PracticeRating`** - Practice skill level
- **`AdvantageRating`** - Companion advantage rating
- **`Advantage`** - Companion advantages
- **`PathRating`** - Linear magic path rating
- **`LinearMagicPath`** - Sorcerer path
- **`LinearMagicRitual`** - Sorcerer ritual

---

## Wraith: The Oblivion (10 models)

### Playable Characters
- **`Wraith`** - Wraith character
- **`WtOHuman`** - Wraith character (extends Human)
  - Guild, Arcanos, Passions, Fetters
  - Corpus, Pathos, Angst (Shadow power)
  - Shadow traits

### Powers & Traits
- **`Guild`** - Wraith guild affiliation
- **`Arcanos`** - Wraith arcane powers
- **`Fetter`** - Emotional connection to living world
- **`Passion`** - Personal passion/drive
- **`ShadowArchetype`** - Shadow personality archetype
- **`Thorn`** - Internal conflict/Shadow flaw

### Other
- **`WraithFaction`** - Faction/group
- **`ThoronRating`** - Thorn rating (note: typo in code)

---

## Changeling: The Dreaming (11 models)

### Playable Characters
- **`Changeling`** - Changeling character
- **`CtDHuman`** - Changeling character (extends Human)
  - Kith, Court, House, Seeming
  - Glamour, Banality, Willpower
  - Arts and Realms

### Traits & Organization
- **`House`** - Sidhe house affiliation
- **`HouseFaction`** - House faction
- **`Kith`** - Changeling race/type (Boggan, Eshu, Pooka, etc.)
- **`Motley`** - Changeling group
- **`Legacy`** - Changeling legacy/inheritance

### Powers & Traits
- **`Cantrip`** - Changeling magic spell
- **`Chimera`** - Chimeric creature

---

## Demon: The Fallen (11 models) ⚠️ **INCOMPLETE**

> **Status:** Models defined but no admin registration, views, URLs, or templates implemented.

### Playable Characters
- **`Demon`** - Demon character **[NO VIEWS/ADMIN]**
- **`DtFHuman`** - Demon in human form **[NO VIEWS/ADMIN]**
  - House, Faction, Torment
  - Faith, Lores
  - Apocalyptic Form

### Powers & Traits
- **`Visage`** - Demonic visage/appearance **[NO VIEWS/ADMIN]**
- **`Lore`** - Demonic lore/knowledge **[NO VIEWS/ADMIN]**
- **`LoreBlock`** - Container for lores
- **`LoreRating`** - Individual lore rating
- **`Pact`** - Demonic pact **[NO VIEWS/ADMIN]**
- **`Thrall`** - Demon servant/thrall **[NO VIEWS/ADMIN]**
- **`Thorn`** - Demon weakness **[NO VIEWS/ADMIN]**
- **`ApocalypticFormTrait`** - Apocalyptic form special ability

### Organization
- **`DemonFaction`** - Demon faction **[NO VIEWS/ADMIN]**
- **`DemonHouse`** - Demonic house **[NO VIEWS/ADMIN]**

---

## File Locations

- **Models:** `characters/models/`
  - `core/` - Shared character models
  - `vampire/` - VtM models
  - `werewolf/` - WtA models
  - `mage/` - MtA models
  - `wraith/` - WtO models
  - `changeling/` - CtD models
  - `demon/` - DtF models (incomplete)

- **Admin:** `characters/admin.py` (64 models registered)
- **Views:** `characters/views/` (organized by gameline)
- **Forms:** `characters/forms/`
- **Templates:** `characters/templates/characters/`

---

## See Also

- `docs/models/implementation_status.md` - Implementation status
- `docs/file_paths.md` - File path reference
- `CLAUDE.md` - Coding standards
