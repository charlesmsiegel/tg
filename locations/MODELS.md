# Locations App Models

Location models for the World of Darkness RPG system, organized by gameline. All location models inherit from the polymorphic `LocationModel` base class.

## Model Hierarchy

```
core.models.Model (abstract polymorphic base)
└── LocationModel (base location)
    ├── City (general location)
    ├── Node (Mage)
    ├── Chantry (Mage)
    ├── Caern (Werewolf)
    └── [Other gameline-specific locations]
```

---

## Core Models (2 models)

### Base Classes
- **`LocationModel`** - Base polymorphic location class
  - Name, description, gameline
  - Owner, chronicle assignment
  - Visibility settings
  - Geographical information

- **`City`** - General city/settlement location
  - Population, government type
  - Can contain other locations
  - Used across all gamelines

---

## Mage: The Ascension (7 models + 4 rating models)

### Magical Locations
- **`Node`** - Source of Quintessence/magical energy
  - Quintessence rating and maximum
  - Resonance types (Dynamic, Entropic, Static)
  - Aura level, size
  - Merit/Flaw ratings
  - Node type (Natural, Constructed, etc.)

- **`Chantry`** - Mage tower/sanctum
  - Tradition/Convention affiliation
  - Library, laboratory, portal access
  - Background ratings (Library, Node, Allies, etc.)
  - Wards and protections

- **`Library`** - Magical library
  - Occult rating, research capacity
  - Contains grimoires and knowledge
  - Arete level of materials

- **`Sanctum`** - Personal magical sanctum
  - Mage's private workshop
  - Warding level
  - Connected to Node or Chantry

- **`Sector`** - Digital Web sector (Mage)
  - Virtual location in the Digital Web
  - Parent/child sector hierarchy
  - Access difficulty

- **`RealityZone`** - Reality zone/pocket realm
  - Custom reality rules
  - Paradox effects
  - Zone ratings for different sphere effects

- **`HorizonRealm`** - Horizon realm
  - Umbral realm controlled by mages
  - Unique physical laws

### Rating Models
- **`NodeMeritFlawRating`** - Node merits/flaws
- **`NodeResonanceRating`** - Node resonance levels
- **`ChantryBackgroundRating`** - Chantry backgrounds
- **`ZoneRating`** - Reality zone sphere modifications

---

## Werewolf: The Apocalypse (1 model)

### Sacred Sites
- **`Caern`** - Sacred werewolf gathering site
  - Level (1-5, power of the caern)
  - Totem spirit
  - Tribe affiliation
  - Gauntlet rating (barrier to spirit world)
  - Bawn (surrounding territory)
  - Type (Wisdom, War, Healing, etc.)

---

## Wraith: The Oblivion (2 models) ⚠️ **INCOMPLETE**

> **Status:** Models defined but no admin registration, views, URLs, or templates implemented.

### Wraith Locations
- **`Haunt`** - Haunted location in the living world **[NO VIEWS/ADMIN]**
  - Wraith's connection to living world
  - Fetter strength
  - Manifestation difficulty

- **`Necropolis`** - Wraith city in the Shadowlands **[NO VIEWS/ADMIN]**
  - Stygia and other Underworld cities
  - Hierarchy control
  - Guild presence

---

## File Locations

- **Models:** `locations/models/`
  - `core/` - Shared location models
  - `mage/` - MtA locations
  - `werewolf/` - WtA locations
  - `wraith/` - WtO locations (incomplete)

- **Admin:** `locations/admin.py` (9 models registered)
- **Views:** `locations/views/` (organized by gameline)
- **Forms:** `locations/forms/`
- **Templates:** `locations/templates/locations/`

---

## Implementation Status

| Gameline | Models | Admin | Views | Templates | Status |
|----------|--------|-------|-------|-----------|--------|
| Core | 2 | ✅ | ✅ | ✅ | Complete |
| Mage | 11 | ✅ | ✅ | ✅ | Complete |
| Werewolf | 1 | ✅ | ✅ | ✅ | Complete |
| Wraith | 2 | ❌ | ❌ | ❌ | **Incomplete** |
| Changeling | 0 | N/A | N/A | N/A | Not started |
| Demon | 0 | N/A | N/A | N/A | Not started |

---

## Special Features

### Mage Locations
- **Complex Background System**: Chantries can have Library, Node, Allies, Mentor, and other backgrounds
- **Reality Zone Ratings**: Customizable sphere effects per zone
- **Node Resonance**: Detailed resonance tracking for mystical energy
- **Digital Web**: Sector hierarchy for virtual locations

### Werewolf Locations
- **Caern Levels**: Power ratings from 1-5
- **Totem Spirits**: Each caern has a patron spirit
- **Gauntlet Ratings**: Barrier strength to spirit world

---

## See Also

- `docs/models/implementation_status.md` - Full implementation details
- `docs/file_paths.md` - File path reference
- `locations/docs/mage/digital_web_sectors.md` - Digital Web documentation
- `CLAUDE.md` - Coding standards
