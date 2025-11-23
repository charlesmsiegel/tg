# Items App Models

Item models for the World of Darkness RPG system, organized by gameline. All item models inherit from the polymorphic `ItemModel` base class.

## Model Hierarchy

```
core.models.Model (abstract polymorphic base)
└── ItemModel (base item)
    ├── Weapon (base weapon)
    │   ├── MeleeWeapon
    │   ├── RangedWeapon
    │   └── ThrownWeapon
    ├── Material (crafting materials)
    ├── Medium (crafting medium)
    └── [Gameline-specific items]
```

---

## Core Models (8 models)

### Base Classes
- **`ItemModel`** - Base polymorphic item class
  - Name, description, gameline
  - Ownership, chronicle assignment
  - Visibility settings

### Weapon System
- **`Weapon`** - Base weapon class
  - Damage, difficulty, range
  - Type (Bashing/Lethal/Aggravated)
- **`MeleeWeapon`** - Hand-to-hand weapons
  - Swords, axes, clubs, knives
- **`RangedWeapon`** - Projectile weapons
  - Bows, crossbows, thrown weapons (not guns)
  - Rate of fire, range, accuracy
- **`ThrownWeapon`** - Throwing weapons
  - Daggers, shuriken, improvised objects

### Crafting Materials
- **`Material`** - Crafting materials
  - Wood, metal, stone, bone, etc.
  - Used in item creation
- **`Medium`** - Crafting medium/base
  - Canvas, parchment, clay, etc.
  - Used for artistic creations

---

## Mage: The Ascension (7 models)

### Magical Items
- **`Artifact`** - Permanent magical item
  - Resonance, Quintessence storage
  - Created through vulgar magic
- **`Wonder`** - Mage-created magical device
  - Arete rating, Quintessence capacity
  - Paradox accumulation
  - Resonance ratings
- **`Talisman`** - Enchanted item
  - Stores magical effects
  - Temporary or permanent
- **`Charm`** - Minor enchanted item
  - Simple magical effect
  - Often single-use or limited charges

### Knowledge Items
- **`Grimoire`** - Spell book/magical tome
  - Contains rotes, practices, knowledge
  - Arete level, tradition affiliation
- **`SorcererArtifact`** - Linear magic artifact
  - Created by sorcerers
  - Path-specific powers

### Ratings
- **`WonderResonanceRating`** - Wonder's resonance levels
  - Dynamic, Entropic, Static resonance

---

## Werewolf: The Apocalypse (2 models)

### Spirit-Bound Items
- **`Fetish`** - Spirit-bound object
  - Gnosis rating, spirit type
  - Permanent magical item
  - Requires attunement
  - Examples: Klaive, Grand Klaive, Spirit Whistle
- **`Talen`** - One-use spirit item
  - Single activation
  - Consumed on use
  - Examples: Healing Stone, Spirit Tracker

---

## Vampire: The Masquerade (2 models)

### Vampire Items
- **`Artifact`** - Vampire artifact
  - Note: Different from Mage/Wraith Artifact (same name, different models)
  - Vampire-specific magical item
- **`Bloodstone`** - Mystical bloodstone
  - Stores vitae
  - Vampire blood magic item

---

## Wraith: The Oblivion (2 models)

### Wraith Items
- **`WraithRelic`** - Wraith relic from life
  - Connection to living world
  - Corpus-reinforced object
- **`Artifact`** - Wraith artifact
  - Note: Different from Mage/Vampire Artifact (same name, different model)
  - Oblivion-forged items

---

## Changeling: The Dreaming (1 model)

### Fae Items
- **`Treasure`** - Changeling treasure
  - Glamour-infused objects
  - Chimeric or real
  - May grant powers or boons

---

## Demon: The Fallen (1 model)

### Demonic Items
- **`Relic`** - Demon relic
  - Faith-powered objects
  - Demonic artifacts

---

## File Locations

- **Models:** `items/models/`
  - `core/` - Shared item models (weapons, materials)
  - `mage/` - MtA items
  - `werewolf/` - WtA items
  - `vampire/` - VtM items
  - `wraith/` - WtO items
  - `changeling/` - CtD items
  - `demon/` - DtF items

- **Admin:** `items/admin.py` (13 models registered)
- **Views:** `items/views/` (organized by gameline)
- **Forms:** `items/forms/`
- **Templates:** `items/templates/items/`

---

## Implementation Status

| Gameline | Models | Admin | Views | Templates | Status |
|----------|--------|-------|-------|-----------|--------|
| Core | 8 | ✅ | ✅ | ✅ | Complete |
| Mage | 7 | ✅ | ✅ | ✅ | Complete |
| Werewolf | 2 | ✅ | ✅ | ✅ | Complete |
| Vampire | 2 | ⚠️ | ⚠️ | ⚠️ | Partial |
| Wraith | 2 | ✅ | ⚠️ | ⚠️ | Partial |
| Changeling | 1 | ✅ | ⚠️ | ⚠️ | Partial |
| Demon | 1 | ✅ | ⚠️ | ⚠️ | Partial |

---

## See Also

- `docs/models/implementation_status.md` - Full implementation details
- `docs/file_paths.md` - File path reference
- `CLAUDE.md` - Coding standards
