# Digital Web Sectors - Implementation Guide

## Overview

This implementation adds comprehensive mechanics for Digital Web Sectors based on "The Operative's Dossier" sourcebook for Mage: The Ascension 20th Anniversary Edition.

## Changes Made

### 1. Enhanced Sector Model (`locations/models/mage/sector.py`)

#### New Fields Added:

**Sector Classification:**
- `sector_class`: Expanded to include C-Sectors and Warzones
- `access_level`: Free vs Restricted sectors

**Power and Security:**
- `power_rating`: Default 5 (Warzones: 7, affects Paradox for Forces/Prime)
- `security_level`: 0-10 difficulty to hack/breach
- `requires_password`: Boolean for password protection
- `password_hint`: Hint for sector password
- `approved_users`: Text list of approved user credentials

**Constraint Protocols:**
- `constraints`: Detailed rules for the sector
- `genre_theme`: e.g., "Film Noir", "Cyberpunk", "Medieval Fantasy"
- `difficulty_modifier`: Arete roll modifier for paradigm compatibility
- `paradox_risk_modifier`: Additional Paradox generation

**Size and Structure:**
- `size_rating`: 1 (Room) to 6 (Region)
- `administrator`: Who controls the sector
- `connected_sectors`: Many-to-many for conduits/links

**Temporal Effects:**
- `time_dilation`: Time flow ratio (1.0 = normal)
- `temporal_instability`: For "Hung Sectors"

**Corruption:**
- `is_reformattable`: Can sector be reformatted?
- `corruption_level`: 0-10 scale
- `has_lag`: Warning sign of Whiteout

**ARO (Augmented Reality Objects):**
- `aro_count`: Number of AROs present
- `aro_density`: None/Sparse/Moderate/Dense/Overwhelming

**Streamland Specific:**
- `data_flow_rate`: Trickle/Steady/High/Torrent

**Population:**
- `estimated_users`: Approximate user count

**Additional:**
- `hazards`: Environmental dangers, hostile entities
- `notable_features`: Landmarks, unique properties

#### New Methods:

1. **`get_effective_difficulty(paradigm_match=True)`**
   - Calculates Arete/Enlightenment roll difficulty
   - Accounts for Reality Zone and paradigm compatibility
   - Returns 3-10 (capped)

2. **`generates_paradox_for_power(effect_power_level)`**
   - Checks if effect exceeds sector's power rating
   - Returns additional Paradox points generated

3. **`is_accessible_to(user_credentials=None)`**
   - Validates user access to restricted sectors
   - Checks credentials against approved user list

4. **`get_whiteout_risk(paradox_pool_size)`**
   - Returns risk level: low/moderate/high/critical
   - Based on sourcebook (lag at 11+ Paradox)

5. **`calculate_base_paradox(is_vulgar, has_witnesses)`**
   - Calculates base Paradox for an effect
   - Includes sector-specific modifiers
   - Corrupted sectors always add +1

6. **`get_navigation_difficulty()`**
   - Returns difficulty to navigate TO this sector
   - Accounts for security, restrictions, corruption

7. **`get_de_rez_type(violation_severity)`**
   - Determines Soft vs Hard De-Rez
   - Based on violation severity and sector type

8. **`time_in_sector(real_world_minutes)`**
   - Calculates time passage with dilation factor

## Populated Sectors

### Grid Sectors
1. **The Grid - Public Space**: Billion-user public internet
2. **Gladiator Arena Alpha**: Warzone with Rating 7

### C-Sectors (Constrained)
3. **Spy's Demise**: Film noir speakeasy with genre enforcement
4. **Iteration X Research Vault 7**: Maximum security SRVRZ
5. **Onion Router Gateway**: Dark Web access point
6. **Arcology X Digital Infrastructure**: Smart city IoT network
7. **Ultima Thule Research Network**: Isolated Antarctic station

### Corrupted Web
8. **Whiteout Crater Z-17**: Destroyed sector, unreformattable
9. **Frozen Moment Sector**: Hung Sector with time anomalies

### Junklands
10. **Echo Station Beta**: Abandoned hub with ghost processes

### Haunts
11. **Memorial Park - Social Media Graveyard**: Deceased users' pages

### Trash
12. **/dev/null - The Trash Sector**: Where deleted data goes

### Streamland
13. **Streamland**: Massive data flow sector

### Virgin Web
14. **The Unformatted Expanse**: Raw, unformatted space

## Installation Instructions

### Step 1: Create Migrations

```bash
python manage.py makemigrations locations
```

This will create a migration file for the new Sector fields.

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

### Step 3: Populate Sectors

```bash
python manage.py shell
```

Then in the Python shell:

```python
exec(open('populate_db/mage/sectors.py').read())
```

Or run the setup script:

```bash
bash setup_db.sh
```

## Usage Examples

### Checking Access

```python
sector = Sector.objects.get(name="Spy's Demise")
can_access = sector.is_accessible_to(user_credentials=["Black Suit", "Approved Agent"])
```

### Calculating Paradox

```python
sector = Sector.objects.get(name="Iteration X Research Vault 7")

# Base paradox for vulgar effect with witnesses
paradox = sector.calculate_base_paradox(is_vulgar=True, has_witnesses=True)

# Additional paradox for high-power effect
effect_level = 7  # Forces 7 blast
if effect_level > sector.power_rating:
    paradox += sector.generates_paradox_for_power(effect_level)
```

### Navigation

```python
sector = Sector.objects.get(name="Whiteout Crater Z-17")
difficulty = sector.get_navigation_difficulty()
# Returns 7 (base 6 + 1 for corrupted)
```

### Time Dilation

```python
hung_sector = Sector.objects.get(name="Frozen Moment Sector")
real_time = 60  # 60 minutes
sector_time = hung_sector.time_in_sector(real_time)
# Returns 0.0 (time frozen)
```

### Whiteout Risk

```python
sector = Sector.objects.get(name="Gladiator Arena Alpha")
risk = sector.get_whiteout_risk(paradox_pool_size=12)
# Returns "critical" (12 >= 11)
```

## Game Mechanics Implementation

### Paradox in Sectors

From the sourcebook (p. 65):

1. **Power Rating Exceeded**:
   - Forces/Prime effects scoring 6+ successes in a Rating 5 sector
   - 1 Paradox per success over the rating

2. **Sector Modifiers**:
   - Corrupted sectors: +1 Paradox for ALL effects
   - Sector-specific modifiers apply

3. **Dual Tracks for AR**:
   - AR users have separate Paradox in Digital Web and Meatspace
   - Both can backlash simultaneously

### Constraint Protocol Violations

Violating a sector's constraints (e.g., using a smartphone in Spy's Demise):
- Vulgar with witnesses (+2 difficulty)
- May trigger De-Rez

### Access Control

**Restricted Sectors**:
- Require credentials or password
- Unauthorized access = vulgar with witnesses
- Unauthorized magic = vulgar with witnesses
- May trigger immediate Hard De-Rez

### De-Rez Types

**Soft De-Rez** (p. 62):
- Returns to save point
- 1-3 unsoakable bashing damage
- Next scene: +2 difficulty (mental fatigue)

**Hard De-Rez** (p. 63):
- Kicks out of Digital Web entirely
- 2 soakable lethal damage (Difficulty 7)
- Holistically Immersed: cannot soak
- Next scene: -2 to Mental Attribute rolls until healed

**Icon Death** (p. 63):
- Icon destroyed, must rebuild
- AR users: gear freezes, requires repair

### Navigation

**Between Sectors** (p. 60):
- Perception + Computer (variable difficulty)
- Or Intelligence + Area Knowledge (Digital Web)
- Or Wits + Cryptography (recognize patterns)
- ARO coordinates reduce difficulty by 1-2

**Linking** (p. 60):
- One-way portals between sectors
- Touch to travel
- CTRL-Z within 3 turns returns to origin

**Pop Apps** (p. 60):
- Correspondence/Data 3
- Within sector: coincidental
- Between sectors: vulgar with witnesses (+2 difficulty)
- Restricted sectors: Difficulty 8-9, can cause Icon Death

## Template for Adding New Sectors

```python
new_sector = Sector.objects.get_or_create(
    name="Your Sector Name",
    defaults={
        "description": "Detailed description of the sector...",
        "sector_class": "grid",  # or c_sector, corrupted, etc.
        "access_level": "free",  # or "restricted"
        "power_rating": 5,
        "security_level": 0,
        "size_rating": 3,

        # For restricted sectors:
        "requires_password": False,
        "password_hint": "",
        "approved_users": "",

        # For C-Sectors:
        "genre_theme": "",
        "constraints": "",

        # Reality effects:
        "difficulty_modifier": 0,
        "paradox_risk_modifier": 0,

        # Population:
        "estimated_users": 0,
        "aro_density": "moderate",

        # Time effects:
        "time_dilation": 1.00,
        "temporal_instability": False,

        # Corruption:
        "corruption_level": 0,
        "is_reformattable": True,

        # Administration:
        "administrator": "",

        # Details:
        "notable_features": "",
        "hazards": "",
    }
)[0]
new_sector.add_source("The Operative's Dossier", page_number)
```

## Source References

All mechanics are based on:
- **The Operative's Dossier**, Chapter Three: Digital Web 3.0 (pp. 57-71)
- Specific sector examples from Chapter One: Constructs and Symposiums

## Notes for Storytellers

### Paradox Tracking
- AR users maintain TWO Paradox tracks simultaneously
- One in Digital Web, one in Meatspace
- Both can backlash at the same time (very dangerous)

### Reality Zones
- Sectors with Reality Zones make compatible magic coincidental
- Incompatible paradigms face increased difficulty
- C-Sectors enforce their genre strictly

### Warzones
- Rating 7 sectors designed for combat
- Can handle massive destructive output
- Still generate Paradox if effects exceed Rating 7

### Corrupted Web
- 117 reformat attempts, 89 deaths, 0 successes
- All Programs generate Paradox
- Avoid unless absolutely necessary

### Dark Web
- Requires special access (onion routing)
- Contains both heroes and monsters
- Virtual Adepts and Nephandi frequent these spaces

## Future Enhancements

Potential additions:
1. ARO model (Augmented Reality Objects)
2. Conduit model (links between sectors)
3. Virtual Assistant NPCs
4. Whiteout Paradox backlash types
5. Integrated Effects for sectors
6. Sector-specific hazard encounters

## Support

For questions or issues, refer to:
- CLAUDE.md for project conventions
- Mage 20th Anniversary Edition core rules
- The Operative's Dossier sourcebook
