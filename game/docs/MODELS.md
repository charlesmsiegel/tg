# Game App Models

Game management models for chronicle, scene, and XP tracking across all World of Darkness gamelines.

---

## Chronicle Management (5 models)

### Core Models
- **`Chronicle`** - Campaign/chronicle definition
  - Name, description, setting
  - Storytellers (many-to-many with User)
  - Allowed objects (characters, items, locations)
  - Gameline(s) supported
  - Active/inactive status

- **`Scene`** - Individual game session
  - Chronicle, location
  - Description, date
  - Characters present
  - Posts/messages
  - XP awarded status
  - Finished/active status

- **`Story`** - Multi-scene story arc
  - Chronicle association
  - Name, description
  - Related scenes
  - XP milestone tracking

- **`Week`** - Weekly time period
  - Used for weekly XP tracking
  - Chronicle association
  - Start/end dates

- **`Post`** - Scene post/message
  - Scene association
  - Character posting
  - Content (text, rolls, actions)
  - Timestamp
  - Read status tracking

---

## Journal System (2 models)

> **Note:** Journal and JournalEntry are NOT registered in admin

- **`Journal`** - Character journal
  - Belongs to specific character
  - Chronicle association
  - Privacy settings

- **`JournalEntry`** - Individual journal entry
  - Journal association
  - Entry text, date
  - Scene reference (optional)
  - In-character or out-of-character

---

## XP & Progression (3 models)

### XP Request System
- **`WeeklyXPRequest`** - Weekly XP request
  - Character, week association
  - Learning activity (with scene reference)
  - Roleplaying activity (with scene reference)
  - Custom XP reasons
  - Approval status
  - Storyteller notes

- **`StoryXPRequest`** - Story milestone XP request
  - Character, story association
  - Completion status
  - XP amount
  - Approval status

- **`UserSceneReadStatus`** - Track scene read status
  - User, scene association
  - Last read timestamp
  - Helps with "new content" indicators

---

## Relationship Management (2 models)

- **`STRelationship`** - Storyteller to chronicle relationship
  - User (storyteller)
  - Chronicle
  - Gameline they ST for
  - Role (Head ST, Game ST, Assistant ST)

- **`ObjectType`** - Object type registry
  - Tracks which objects (character/item/location) belong to chronicles
  - Type classification
  - Gameline association

---

## Setting & Knowledge (2 models)

- **`SettingElement`** - Common knowledge/lore
  - Chronicle-specific or general
  - Gameline association
  - Name, description
  - Category (history, location, NPC, organization, etc.)
  - Visibility (public, ST-only, etc.)

- **`Gameline`** - Gameline definition
  - Name (Vampire, Werewolf, Mage, etc.)
  - Short code (VtM, WtA, MtA)
  - Description
  - Active status

---

## File Locations

- **Models:** `game/models.py`
- **Admin:** `game/admin.py` (12 models registered)
- **Views:** `game/views.py`
- **Forms:** `game/forms.py`
- **Templates:** `game/templates/game/`
- **URLs:** `game/urls.py`

---

## Implementation Status

| Model | Admin | Views | Templates | Notes |
|-------|-------|-------|-----------|-------|
| Chronicle | ✅ | ✅ | ✅ | Full CRUD |
| Scene | ✅ | ✅ | ✅ | Full CRUD with posting |
| Story | ✅ | ✅ | ✅ | Full CRUD |
| Week | ✅ | ⚠️ | ⚠️ | Limited views |
| Post | ✅ | ⚠️ | ⚠️ | Embedded in scenes |
| Journal | ❌ | ✅ | ✅ | Not in admin |
| JournalEntry | ❌ | ⚠️ | ⚠️ | Not in admin |
| WeeklyXPRequest | ✅ | ⚠️ | ⚠️ | Basic functionality |
| StoryXPRequest | ✅ | ⚠️ | ⚠️ | Basic functionality |
| UserSceneReadStatus | ✅ | ⚠️ | N/A | Background tracking |
| STRelationship | ✅ | ⚠️ | ⚠️ | Admin management |
| ObjectType | ✅ | ⚠️ | N/A | Internal tracking |
| SettingElement | ✅ | ⚠️ | ⚠️ | Limited implementation |
| Gameline | ✅ | ⚠️ | N/A | Configuration model |

---

## Key Workflows

### Chronicle Creation
1. ST creates chronicle
2. Sets gameline(s), storytellers
3. Players create characters for chronicle
4. ST approves characters

### Scene Management
1. ST creates scene in chronicle
2. Adds characters as participants
3. Players post in scene
4. ST closes scene when complete
5. XP awarded to participants

### XP System
1. **Weekly XP**: Players submit `WeeklyXPRequest` for week
   - Learning: Scene where character learned something
   - Roleplay: Scene with good roleplay
   - Other: Custom reasons
2. **Story XP**: Automatically awarded on story completion via `StoryXPRequest`
3. ST approves/denies requests
4. XP added to character's `xp` field
5. Character spends XP through spending system (tracked in separate models)

### Journal Workflow
1. Player creates `Journal` for character
2. Adds `JournalEntry` instances
3. Can reference specific scenes
4. Privacy controls who can view

---

## Design Patterns

### Chronicle as Container
- Chronicles contain characters, items, locations
- `allowed_objects` ManyToMany tracks what's available
- Characters/items/locations have `chronicle` ForeignKey

### Scene Participation
- Scenes have many characters (participants)
- Posts link character to scene
- Tracks who was present and active

### XP Approval Workflow
- Requests created by players
- STs review and approve/deny
- Approved XP added to character
- Spending XP requires separate approval (character advancement system)

### Read Status Tracking
- `UserSceneReadStatus` tracks last read time
- Helps show "new posts" indicators
- Per-user, per-scene tracking

---

## See Also

- `docs/models/implementation_status.md` - Full implementation details
- `docs/file_paths.md` - File path reference
- `docs/guides/jsonfield_migration.md` - XP system migration notes
- `CLAUDE.md` - Coding standards
