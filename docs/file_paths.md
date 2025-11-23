# File Path Reference Guide

Quick reference for navigating the World of Darkness Django codebase.

---

## Model Definition Files

### Core Models

**`core/models.py`**
- Book, BookReference, NewsItem, Language, HouseRule (5 models)
- Model (base abstract class for all polymorphic models)

**`accounts/models.py`**
- Profile (1 model)

**`game/models.py`**
- Chronicle, Scene, Story, Week, Journal, JournalEntry, Post
- WeeklyXPRequest, StoryXPRequest, UserSceneReadStatus
- STRelationship, ObjectType, SettingElement, Gameline (15 models)

### Character Models

**`characters/models/core/`** (22 files)
- Character, Human, Archetype, Derangement, Specialty, Group
- MeritFlaw, Ability, Attribute, Background, HealthBlock, etc.

**`characters/models/vampire/`**
- VtMHuman

**`characters/models/werewolf/`** (18 files)
- Werewolf, WtAHuman, Tribe, Camp, Pack, Gift, Rite, etc.

**`characters/models/mage/`** (13 files)
- Mage, MtAHuman, Paradigm, Practice, Effect, Rote, Cabal, etc.

**`characters/models/wraith/`** (9 files)
- Wraith, WtOHuman, Guild, Arcanos, Fetter, Passion, etc.

**`characters/models/changeling/`** (8 files)
- Changeling, CtDHuman, House, Kith, Motley, Legacy, etc.

**`characters/models/demon/`** (10 files) ⚠️ **INCOMPLETE**
- Demon, DtFHuman, DemonFaction, DemonHouse, Visage, Lore, etc.

### Item Models

**`items/models/core/`** (8 files)
- ItemModel, Weapon, MeleeWeapon, RangedWeapon, ThrownWeapon
- Material, Medium

**`items/models/mage/`** (6 files)
- Artifact, Wonder, Talisman, Charm, Grimoire, SorcererArtifact

**`items/models/werewolf/`** (2 files)
- Fetish, Talen

**`items/models/wraith/`** (2 files)
- WraithRelic, Artifact

**`items/models/changeling/`** (1 file)
- Treasure

**`items/models/demon/`** (1 file) ⚠️ **INCOMPLETE**
- Relic

### Location Models

**`locations/models/core/`** (2 files)
- LocationModel, City

**`locations/models/mage/`** (7 files)
- Node, Chantry, Library, Sanctum, Sector, RealityZone, Realm

**`locations/models/werewolf/`** (1 file)
- Caern

**`locations/models/wraith/`** (2 files) ⚠️ **INCOMPLETE**
- Haunt, Necropolis

---

## Admin Registration

| App | File | Models Registered |
|-----|------|-------------------|
| Characters | `characters/admin.py` | 64 models (414 lines) |
| Items | `items/admin.py` | 13 models (66 lines) |
| Locations | `locations/admin.py` | 9 models (58 lines) |
| Game | `game/admin.py` | 12 models (67 lines) |
| Core | `core/admin.py` | 5 models (25 lines) |
| Accounts | `accounts/admin.py` | 1 model (8 lines) |

---

## Views

### Character Views
- `characters/views/core/` - 7 files
- `characters/views/vampire/` - 1 file
- `characters/views/werewolf/` - 11 files
- `characters/views/mage/` - 11 files
- `characters/views/wraith/` - 1 file (minimal)
- `characters/views/changeling/` - 6 files
- ⚠️ Demon views: **Missing entirely**

### Item Views
- `items/views/core/` - 8 files (fully implemented)
- `items/views/mage/` - 6 files (fully implemented)
- `items/views/werewolf/` - 2 files (fully implemented)
- ⚠️ Demon, Wraith, Changeling item views: **Missing**

### Location Views
- `locations/views/core/` - 2 files
- `locations/views/mage/` - 7 files
- `locations/views/werewolf/` - 1 file
- ⚠️ Wraith: Haunt, Necropolis views **missing**

### Other Views
- `game/views.py` - Limited CRUD
- `core/views/` - 5 files (NewsItem, Language, Book)
- `accounts/views.py` - Profile

---

## URL Patterns

### Character URLs
- `characters/urls/__init__.py` - Main router
- `characters/urls/core/` - create, update, index, detail
- `characters/urls/vampire/`
- `characters/urls/werewolf/`
- `characters/urls/mage/`
- `characters/urls/wraith/`
- `characters/urls/changeling/`
- ⚠️ Demon URLs: **Missing entirely**

### Item URLs
- `items/urls/__init__.py` - Main router
- `items/urls/core/` - Fully implemented
- `items/urls/mage/` - Fully implemented
- `items/urls/werewolf/` - Fully implemented
- ⚠️ Other gamelines: Partial or missing

### Location URLs
- `locations/urls/__init__.py` - Main router
- `locations/urls/core/`
- `locations/urls/mage/`
- `locations/urls/werewolf/`
- ⚠️ Wraith, other gamelines: Partial or missing

### Other URLs
- `game/urls.py`
- `core/urls.py`

---

## Templates

### Character Templates
- `characters/templates/characters/core/` - Fully implemented
- `characters/templates/characters/vampire/` - Minimal
- `characters/templates/characters/werewolf/` - Fully implemented
- `characters/templates/characters/mage/` - Fully implemented
- `characters/templates/characters/wraith/` - Minimal
- `characters/templates/characters/changeling/` - Fully implemented
- ⚠️ Demon: **Missing entirely**

### Item Templates
- `items/templates/items/core/` - Fully implemented
- `items/templates/items/mage/` - Fully implemented
- `items/templates/items/werewolf/` - Fully implemented
- ⚠️ Other gamelines: Missing or minimal

### Location Templates
- `locations/templates/locations/core/` - Fully implemented
- `locations/templates/locations/mage/` - Fully implemented
- `locations/templates/locations/werewolf/` - Fully implemented
- ⚠️ Wraith: Haunt/Necropolis missing

---

## Forms

- `characters/forms/` - 33 form files
- `items/forms/` - 6 form files
- `locations/forms/` - 9 form files

---

## Key Development Insights

### 1. Polymorphic Model Pattern
- All Character/Item/Location models inherit from `core.models.Model`
- Uses django-polymorphic for inheritance
- Child models override `get_gameline()` to identify their type

### 2. Naming Conventions
- **Main character types**: `Character` → `Human` → `[VtMHuman, Mage, WtAHuman, etc.]`
- **Human variants**: `VtMHuman`, `MtAHuman`, `WtAHuman`, `WtOHuman`, `CtDHuman`, `DtFHuman`
- **Trait models**: Usually inherit from `models.Model`, not `Character`
- **Faction models**: `[GamelineName]Faction` (MageFaction, WraithFaction, DemonFaction)

### 3. Structure Patterns
- **Gameline subdirectories**: core, vampire, werewolf, mage, wraith, changeling, demon
- Each has: `models/`, `views/`, `urls/`, `templates/`
- Core models are in the "core" subdirectory
- Shared traits (MeritFlaw, Background) are in core

### 4. Missing Implementation Pattern (Demon)
- ✅ Models ARE defined in model files
- ❌ Models are NOT registered in admin.py
- ❌ Views DO NOT exist (no view classes)
- ❌ URLs DO NOT exist (no path definitions)
- ❌ Templates DO NOT exist (no .html files)
- ⚠️ Forms may or may not exist

### 5. Partial Implementation (Wraith Locations)
- ✅ Models exist (Haunt, Necropolis)
- ❌ Admin registration missing
- ❌ No views/URLs/templates
- Suggests incomplete feature

---

## See Also

- `docs/models/` - Model documentation and implementation status
- `CLAUDE.md` - Project coding standards and patterns
- `TODO.md` - Known gaps and planned improvements
