# TODO List

This document consolidates all remaining TODOs across the codebase with context about what needs to be done.

---

## 🔴 High Priority - Code TODOs

### Python Code TODOs

1. **Create LimitedCharacterForm for owner editing**
   - **File**: `characters/views/core/character.py:142`
   - **Context**: Currently, character owners can edit all fields when they should only be able to edit descriptive fields (notes, description, etc.). Need to create a limited form that restricts editing to non-mechanical fields.
   - **Related**: Part of permissions system - owners should have limited edit access
   - **Impact**: Security/gameplay integrity

2. **Add tribal restrictions for Kinfolk backgrounds**
   - **File**: `characters/views/werewolf/kinfolk.py:255`
   - **Context**: `KinfolkBackgroundsView` doesn't enforce tribal restrictions on background choices. Some backgrounds may be restricted based on the Kinfolk's associated tribe.
   - **Impact**: Character creation rules enforcement

3. **Find source for "Slow Healing" merit**
   - **File**: `populate_db/merits_and_flaws_INC.py:14`
   - **Context**: The "Slow Healing" merit (3 pt flaw) for Mage/Sorcerer needs source book verification and page number.
   - **Impact**: Documentation completeness

---

## 🟡 Medium Priority - Testing & Quality

### Permissions System Testing

**File**: `APPLYING_PERMISSIONS_GUIDE.md`

- [ ] **Create limited forms for owner editing**
  - Implement forms that restrict owners to editing only descriptive fields
  - Apply to all character/item/location edit views
  - Test that mechanical fields are properly protected

- [ ] **Test all permission scenarios**
  - Test as Owner, Chronicle Member, Storyteller, Stranger
  - Verify visibility tiers work correctly
  - Ensure 404s are returned for unauthorized access

- [ ] **Update corresponding tests**
  - Add unit tests for permission checks
  - Add integration tests for view access
  - Test permission edge cases

### Validation System Testing

**File**: `VALIDATION_IMPLEMENTATION_SUMMARY.md`

- [ ] **Add integration tests for transactions**
  - Test `spend_xp()` atomicity with concurrent requests
  - Test `approve_xp_spend()` rollback on failure
  - Test `award_xp()` all-or-nothing behavior
  - Verify race condition prevention with `select_for_update()`

### XP/Freebie Migration Testing

**File**: `VIEW_TEMPLATE_MIGRATION_GUIDE.md`

Generic testing checklist for any XP/freebie view updates:
- [ ] Display of XP/freebie history works correctly
- [ ] Total spent calculations are accurate
- [ ] New requests are created properly
- [ ] Approval workflow functions (if applicable)
- [ ] Both JSONField and model data display during transition
- [ ] No regressions in existing functionality

---

## 🟢 Low Priority - Feature Completeness

### Model Implementation Gaps

**Source**: Extracted from app MODELS.md files (accounts, characters, game, items, locations)

#### Characters App - Demon Gameline (CRITICAL GAP)

**Status**: 11 models defined but NO admin registration, views, URLs, or templates implemented

Models needing full implementation:
- [ ] **Demon** - Base demon character class
  - File: `characters/models/demon/demon.py`
  - Needs: Admin, views, forms, templates, URLs

- [ ] **DtFHuman** - Demon in human form (playable character)
  - File: `characters/models/demon/dtfhuman.py`
  - Needs: Admin, character creation views, detail/update views, templates
  - Fields: House, Faction, Torment, Faith, Lores, Apocalyptic Form

- [ ] **Visage** - Demonic visage/appearance
  - File: `characters/models/demon/visage.py`
  - Needs: Admin, reference data views, populate script

- [ ] **Lore** - Demonic lore/knowledge
  - File: `characters/models/demon/lore.py`
  - Needs: Admin, reference data views, populate script

- [ ] **Pact** - Demonic pact
  - File: `characters/models/demon/pact.py`
  - Needs: Admin, creation/management views, templates

- [ ] **Thrall** - Demon servant/thrall
  - File: `characters/models/demon/thrall.py`
  - Needs: Admin, creation/management views, templates

- [ ] **Thorn** - Demon weakness
  - File: `characters/models/demon/thorn.py`
  - Needs: Admin, reference data views, populate script

- [ ] **DemonFaction** - Demon faction
  - File: `characters/models/demon/faction.py`
  - Needs: Admin, reference data views, populate script

- [ ] **DemonHouse** - Demonic house
  - File: `characters/models/demon/house.py`
  - Needs: Admin, reference data views, populate script

- [ ] **LoreBlock** - Container for character's lores
  - Verify if admin/views needed

- [ ] **LoreRating** - Individual lore rating
  - Verify if admin/views needed

- [ ] **ApocalypticFormTrait** - Apocalyptic form special ability
  - Verify if admin/views needed

#### Game App - Journal System

- [ ] **Journal** - Character journal (NOT in admin)
  - File: `game/models.py`
  - Needs: Admin registration, improved management views

- [ ] **JournalEntry** - Individual journal entry (NOT in admin)
  - File: `game/models.py`
  - Needs: Admin registration, improved creation/edit views, templates

#### Game App - Limited Implementations

- [ ] **Week** - Weekly time period
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Full CRUD views and templates for week management

- [ ] **Post** - Scene post/message
  - Status: Admin ✅, Views ⚠️ (embedded in scenes), Templates ⚠️
  - Needs: Standalone post management views if required

- [ ] **WeeklyXPRequest** - Weekly XP request
  - Status: Admin ✅, Views ⚠️ (basic), Templates ⚠️
  - Needs: Enhanced views for request creation, approval workflow, templates

- [ ] **StoryXPRequest** - Story milestone XP request
  - Status: Admin ✅, Views ⚠️ (basic), Templates ⚠️
  - Needs: Enhanced views for story completion tracking, approval workflow

- [ ] **UserSceneReadStatus** - Track scene read status
  - Status: Admin ✅, Views ⚠️ (background tracking)
  - Needs: Verify views are sufficient for functionality

- [ ] **STRelationship** - Storyteller to chronicle relationship
  - Status: Admin ✅, Views ⚠️ (admin management), Templates ⚠️
  - Needs: User-facing views for ST management

- [ ] **ObjectType** - Object type registry
  - Status: Admin ✅, Views ⚠️ (internal tracking)
  - Needs: Verify views are sufficient for functionality

- [ ] **SettingElement** - Common knowledge/lore
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Full implementation for chronicle lore management

- [ ] **Gameline** - Gameline definition
  - Status: Admin ✅, Views ⚠️ (configuration model)
  - Needs: Verify views are sufficient for configuration

#### Items App - Vampire Items (2 models)

- [ ] **Artifact** (Vampire) - Vampire artifact
  - File: `items/models/vampire/artifact.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

- [ ] **Bloodstone** - Mystical bloodstone
  - File: `items/models/vampire/bloodstone.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

#### Items App - Wraith Items (2 models)

- [ ] **WraithRelic** - Wraith relic from life
  - File: `items/models/wraith/relic.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

- [ ] **Artifact** (Wraith) - Wraith artifact
  - File: `items/models/wraith/artifact.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

#### Items App - Changeling Items (1 model)

- [ ] **Treasure** - Changeling treasure
  - File: `items/models/changeling/treasure.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

#### Items App - Demon Items (1 model)

- [ ] **Relic** (Demon) - Demon relic
  - File: `items/models/demon/relic.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

#### Locations App - Wraith Locations (CRITICAL GAP)

**Status**: 2 models defined but NO admin registration, views, URLs, or templates implemented

- [ ] **Haunt** - Haunted location in the living world
  - File: `locations/models/wraith/haunt.py`
  - Status: ❌ NO VIEWS/ADMIN
  - Needs: Full implementation (admin, views, forms, templates, URLs)
  - Fields: Fetter strength, manifestation difficulty

- [ ] **Necropolis** - Wraith city in the Shadowlands
  - File: `locations/models/wraith/necropolis.py`
  - Status: ❌ NO VIEWS/ADMIN
  - Needs: Full implementation (admin, views, forms, templates, URLs)
  - Fields: Hierarchy control, guild presence

#### Locations App - Vampire Locations (4 models)

- [ ] **Domain** - Territory controlled by a vampire
  - File: `locations/models/vampire/domain.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

- [ ] **Haven** - Vampire's private sanctuary
  - File: `locations/models/vampire/haven.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

- [ ] **Elysium** - Neutral ground for vampire society
  - File: `locations/models/vampire/elysium.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

- [ ] **Rack** - Quality hunting grounds
  - File: `locations/models/vampire/rack.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

#### Locations App - Demon Locations (2 models)

- [ ] **Bastion** - Fortified stronghold of the Earthbound
  - File: `locations/models/demon/bastion.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

- [ ] **Reliquary** - Location that serves as an Earthbound's vessel
  - File: `locations/models/demon/reliquary.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

#### Locations App - Changeling Locations

- [ ] **Changeling location models** - NOT STARTED
  - No location models exist for Changeling gameline
  - Consider: Freehold, Trod, Hollow, Dreamscape
  - Needs: Research source material, define models, implement full stack

### Django Messages Framework - Remaining Views

**File**: `MESSAGING_IMPLEMENTATION.md`

The following views still need `MessageMixin` added for user feedback:

#### Characters
- [ ] `characters/views/core/npc.py` - NPCCreateView, NPCUpdateView
- [ ] `characters/views/core/human.py` - Base views (consider inheritance implications)

#### Items

**Vampire Items:**
- [ ] `items/views/vampire/*.py` - Haven components, Domain views

**Werewolf Items:**
- [ ] `items/views/werewolf/rite.py`
- [ ] Other werewolf item views

**Changeling Items:**
- [ ] `items/views/changeling/*.py` - Treasure views, Token views

**Wraith Items:**
- [ ] `items/views/wraith/*.py` - Artifact views, Relic views

#### Locations

**Mage Locations:**
- [ ] `locations/views/mage/chantry.py` - ChantryCreateView, ChantryUpdateView
- [ ] `locations/views/mage/node.py` - Node CRUD views
- [ ] `locations/views/mage/sanctum.py` - Sanctum CRUD views
- [ ] `locations/views/mage/library.py` - Library CRUD views
- [ ] Other mage location views

**Vampire Locations:**
- [ ] `locations/views/vampire/haven.py` - HavenCreateView, HavenUpdateView
- [ ] `locations/views/vampire/domain.py` - Domain CRUD views
- [ ] Other vampire location views

**Werewolf Locations:**
- [ ] `locations/views/werewolf/caern.py` - Caern CRUD views
- [ ] Other werewolf location views

**Changeling Locations:**
- [ ] `locations/views/changeling/freehold.py` - Freehold CRUD views
- [ ] Other changeling location views

**Wraith Locations:**
- [ ] `locations/views/wraith/haunt.py` - Haunt CRUD views
- [ ] Other wraith location views

#### Core/Reference Data
- [ ] `core/views/*.py` - Book, SourceMaterial, HouseRule views

#### Game-Specific Reference Data
- [ ] Mage spheres, practices, tenets, factions
- [ ] Werewolf gifts, rites, breeds, tribes
- [ ] Vampire clans, disciplines, paths
- [ ] Changeling arts, realms, kiths
- [ ] Wraith arcanoi, guilds, circles
- [ ] Demon lores, factions, houses

### Character Template System Enhancements

**File**: `characters/docs/template_system.md`

Future enhancements for the CharacterTemplate system:

- [ ] **User-created templates (Storyteller-only)**
  - Allow STs to create custom templates for their chronicles
  - Restrict template creation to users with ST permissions
  - Add template management interface

- [ ] **Template variations by clan/tribe/tradition**
  - Create specialized templates for each faction
  - E.g., "Brujah Brawler", "Glass Walker Hacker", "Verbena Herbalist"
  - Populate with faction-appropriate backgrounds and powers

- [ ] **Template import/export (JSON)**
  - Export templates as JSON for sharing
  - Import community-created templates
  - Validation on import to prevent malicious data

- [ ] **Template voting/ratings**
  - Let users rate templates they've used
  - Display popular templates first
  - Add comments/feedback on templates

- [ ] **NPC quick-creation from templates**
  - One-click NPC creation from template
  - Auto-populate NPC fields from template data
  - Faster ST workflow for creating multiple NPCs

### Code Quality & Best Practices

**Source**: Consolidated from best practice violations analysis

#### Critical Security Issues
- [ ] **Fix security settings in production**
  - `tg/settings.py:27-29` - Move to environment-based configuration
  - Set `DEBUG = False` in production
  - Configure proper `ALLOWED_HOSTS` instead of `["*"]`
  - Create environment-specific settings files (base.py, development.py, production.py)

- [ ] **Add authentication to views**
  - Multiple views lack `LoginRequiredMixin` or authentication checks
  - `game/views.py` - ChronicleDetailView, SceneDetailView, ChronicleScenesDetailView
  - Add `LoginRequiredMixin` to all views that require authentication

- [ ] **Implement authorization checks**
  - `game/views.py:113-119` and throughout - No permission validation
  - Users can close any scene, post as any character, approve XP without ST status
  - Create permission mixins (e.g., `StorytellerRequiredMixin`)
  - Add permission checks before allowing actions

- [ ] **Replace `.get()` with `get_object_or_404()`**
  - `game/views.py:27, 76, 87, 121, 134, 250` - Using `.get()` causes 500 errors
  - Replace with `get_object_or_404()` for proper 404 responses

#### Performance Issues
- [ ] **Fix N+1 query problems**
  - `accounts/models.py:115-121` - st_relations() causes N queries
  - `game/models.py:196-205` - weekly_characters() queries per scene
  - `accounts/models.py:163-170` - rotes_to_approve() queries per rote
  - Use `select_related()`, `prefetch_related()`, and proper querysets

- [ ] **Add database indexes**
  - `game/models.py:322-328` - Post model lacks indexes on frequently queried fields
  - Add `db_index=True` to datetime_created and other frequently filtered fields
  - Create composite indexes for common query patterns

#### Code Architecture
- [ ] **Move business logic out of forms**
  - `accounts/forms.py:89-96` - SceneXP.save() contains business logic
  - Move XP award logic to model methods
  - Keep forms focused on data validation

- [ ] **Address fat models with complex inheritance**
  - `characters/models/core/` - Human class has 7+ parent classes
  - Consider composition over inheritance
  - Evaluate proxy models for polymorphic behavior

- [ ] **Move signal registration to apps.py**
  - `accounts/models.py:264-268` - Signal registered in models.py
  - Move to `accounts/apps.py` ready() method
  - Create separate `accounts/signals.py` module

#### Model & Data Validation
- [ ] **Add model validation**
  - Most models lack `clean()` methods
  - Add validation in `clean()` for data integrity
  - Call `full_clean()` in `save()` methods

- [ ] **Fix class name typo**
  - `accounts/forms.py:24` - `CustomUSerCreationForm` should be `CustomUserCreationForm`
  - Update all references

#### Testing & Code Quality
- [ ] **Improve test coverage**
  - Only `accounts/tests.py` has actual tests
  - Add comprehensive test suite using pytest-django
  - Test all views, forms, and model methods
  - Aim for 80%+ coverage

- [ ] **Standardize CBV patterns**
  - `game/views.py` - Views inherit from View but don't follow CBV patterns
  - Use proper Django generic views (DetailView, ListView, etc.)
  - Follow standard `get_context_data()` pattern

- [ ] **Centralize hardcoded choices**
  - `game/models.py:18-35`, `accounts/models.py:28-48` - Choices duplicated
  - Create `core/constants.py` for shared choices
  - Use constants throughout codebase

#### Development Tools
- [ ] **Add Django Debug Toolbar**
  - Configure in development settings
  - Helps identify N+1 queries and performance issues

- [ ] **Configure logging**
  - Add LOGGING configuration to settings
  - Set up file and console handlers
  - Configure per-app log levels

- [ ] **Add caching configuration**
  - Configure Redis or Memcached for caching
  - Use `@cache_page` decorator for appropriate views
  - Cache expensive querysets

#### Long-term Improvements
- [ ] **Consider custom User model**
  - Currently using Profile extension of Django User
  - Document trade-offs of current approach
  - For new projects, AbstractUser is preferred

- [ ] **Add migration best practices**
  - Create data migrations for schema changes
  - Periodically squash old migrations
  - Test migrations in CI/CD pipeline

- [ ] **Improve code style consistency**
  - `accounts/models.py:116` - `str` variable shadows built-in
  - Add docstrings to complex methods
  - Use black/ruff for formatting
  - Consider mypy for type checking

---

## 🔵 Deployment & Environment

### Permissions System Deployment

**File**: `PERMISSIONS_IMPLEMENTATION_COMPLETE.md`

- [ ] **Create and activate virtual environment**
  - Set up clean Python virtual environment
  - Isolate dependencies from system Python

- [ ] **Install dependencies**
  - Run `pip install -r requirements.txt`
  - Verify all packages install correctly

- [ ] **Test with different user roles**
  - Manual testing with Owner, Chronicle Member, ST, Stranger accounts
  - Verify visibility tiers and edit permissions
  - Check that 404s are returned appropriately

- [ ] **Deploy to staging**
  - Deploy permissions system to staging environment
  - Run full test suite in staging
  - Performance testing under load

- [ ] **User acceptance testing**
  - Get feedback from real users
  - Test edge cases in production-like environment
  - Verify no usability issues

- [ ] **Deploy to production**
  - Final deployment of permissions system
  - Monitor error logs closely
  - Be ready to rollback if issues arise

### Validation System Deployment

**File**: `VALIDATION_IMPLEMENTATION_SUMMARY.md`

- [ ] **Deploy to staging**
  - Deploy transaction protection and constraints
  - Test XP spending workflows
  - Verify constraint violations are caught

- [ ] **Monitor for validation errors**
  - Watch logs for CheckConstraint violations
  - Monitor for transaction rollbacks
  - Track performance impact

- [ ] **Deploy to production**
  - Final deployment of validation system
  - Monitor database constraint violations
  - Alert on any data integrity issues

- [ ] **Monitor database constraint violations**
  - Set up alerts for constraint violations
  - Log violations for analysis
  - Fix any existing invalid data

---

## 📊 Priority Summary

| Category | High Priority | Medium Priority | Low Priority |
|----------|--------------|-----------------|--------------|
| Code TODOs | 3 items | - | - |
| Testing | - | 9 items | 6 items |
| Model Implementation Gaps | - | - | 60+ models |
| Feature Completeness | - | - | 35+ views |
| Template Enhancements | - | - | 5 features |
| Code Quality & Best Practices | - | - | 20+ items |
| Deployment | - | 8 items | - |

**Model Implementation Gap Breakdown:**
- **CRITICAL**: Demon characters (12 models) - No views/admin
- **CRITICAL**: Wraith locations (2 models) - No views/admin
- **Partial**: Vampire items (2 models), Wraith items (2 models), Changeling items (1 model), Demon items (1 model)
- **Partial**: Vampire locations (4 models), Demon locations (2 models)
- **Partial**: Game app models (10 models with limited views)
- **Not Started**: Changeling locations (no models exist)

---

## 🎯 Recommended Next Steps

1. **Code Quality** (High Priority)
   - Implement `LimitedCharacterForm` for owner editing
   - Add tribal restrictions for Kinfolk backgrounds

2. **Testing** (Medium Priority)
   - Add integration tests for atomic transactions
   - Test all permission scenarios
   - Update test coverage

3. **Deployment** (Medium Priority)
   - Set up staging environment
   - Deploy permissions and validation systems
   - Monitor for issues

4. **Model Implementation Gaps** (Low Priority - but large scope)
   - **Priority 1**: Complete Demon character implementation (12 models)
   - **Priority 2**: Complete Wraith location implementation (2 models)
   - **Priority 3**: Complete partial implementations (Vampire/Wraith/Changeling/Demon items and locations)
   - **Priority 4**: Enhance Game app models with better views/templates

5. **Feature Completeness** (Low Priority)
   - Add MessageMixin to remaining views
   - Implement template system enhancements
