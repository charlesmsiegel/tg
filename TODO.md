# TODO List

This document tracks remaining work across the codebase with context about what needs to be done.

---

## 🔴 High Priority

### Security

1. **Address dependency vulnerabilities**
   - **Status**: 9 vulnerabilities detected (1 critical, 3 high, 4 moderate, 1 low)
   - **Action**: Review and update vulnerable dependencies
   - **Check**: https://github.com/charlesmsiegel/tg/security/dependabot

2. **Fix security settings for production**
   - **File**: `tg/settings.py:27-29`
   - **Issue**: DEBUG=True, ALLOWED_HOSTS=["*"] in settings
   - **Action**: Move to environment-based configuration
   - Set `DEBUG = False` in production
   - Configure proper `ALLOWED_HOSTS` from environment
   - Create environment-specific settings files (base.py, development.py, production.py)

3. **Add authentication to views**
   - **Files**: Multiple views in `game/views.py`
   - **Issue**: ChronicleDetailView, SceneDetailView, ChronicleScenesDetailView lack `LoginRequiredMixin`
   - **Action**: Add `LoginRequiredMixin` to all views that require authentication

4. **Implement authorization checks**
   - **Files**: `game/views.py` throughout
   - **Issue**: Users can close any scene, post as any character, approve XP without ST status
   - **Action**: Create permission mixins (e.g., `StorytellerRequiredMixin`)
   - Add permission checks before allowing actions

5. **Replace `.get()` with `get_object_or_404()`**
   - **Files**: `game/views.py:27, 76, 87, 121, 134, 250`
   - **Issue**: Using `.get()` causes 500 errors instead of proper 404 responses
   - **Action**: Replace all `.get()` calls in views with `get_object_or_404()`

### Code Quality

1. **Find source for "Slow Healing" merit**
   - **File**: `populate_db/merits_and_flaws_INC.py:14`
   - **Issue**: The "Slow Healing" merit (3 pt flaw) for Mage/Sorcerer needs source book verification and page number
   - **Impact**: Documentation completeness

---

## 🟡 Medium Priority

### Performance

1. **Fix N+1 query problems**
   - **Files**:
     - `accounts/models.py:115-121` - st_relations() causes N queries
     - `game/models.py:196-205` - weekly_characters() queries per scene
     - `accounts/models.py:163-170` - rotes_to_approve() queries per rote
   - **Action**: Use `select_related()`, `prefetch_related()`, and proper querysets

2. **Add database indexes**
   - **File**: `game/models.py:322-328`
   - **Issue**: Post model lacks indexes on frequently queried fields
   - **Action**: Add `db_index=True` to datetime_created and other frequently filtered fields
   - Create composite indexes for common query patterns

### Code Architecture

1. **Move business logic out of forms**
   - **File**: `accounts/forms.py:89-96`
   - **Issue**: SceneXP.save() contains business logic
   - **Action**: Move XP award logic to model methods
   - Keep forms focused on data validation

2. **Address fat models with complex inheritance**
   - **Files**: `characters/models/core/`
   - **Issue**: Human class has 7+ parent classes
   - **Action**: Consider composition over inheritance
   - Evaluate proxy models for polymorphic behavior

3. **Move signal registration to apps.py**
   - **File**: `accounts/models.py:264-268`
   - **Issue**: Signal registered in models.py
   - **Action**: Move to `accounts/apps.py` ready() method
   - Create separate `accounts/signals.py` module

### Model & Data Validation

1. **Add model validation**
   - **Files**: Most models across all apps
   - **Issue**: Most models lack `clean()` methods
   - **Action**: Add validation in `clean()` for data integrity
   - Call `full_clean()` in `save()` methods

2. **Fix class name typo**
   - **File**: `accounts/forms.py:24`
   - **Issue**: `CustomUSerCreationForm` should be `CustomUserCreationForm`
   - **Action**: Update class name and all references

### Testing

1. **Improve test coverage**
   - **Current**: Only `accounts/tests.py` has substantial tests
   - **Goal**: 80%+ coverage across all apps
   - **Action**: Add comprehensive test suite using Django's unittest framework
   - Test all views, forms, and model methods

2. **Standardize CBV patterns**
   - **File**: `game/views.py`
   - **Issue**: Views inherit from View but don't follow CBV patterns
   - **Action**: Use proper Django generic views (DetailView, ListView, etc.)
   - Follow standard `get_context_data()` pattern

### Development Tools

1. **Add Django Debug Toolbar**
   - Configure in development settings
   - Helps identify N+1 queries and performance issues

2. **Configure logging**
   - Add LOGGING configuration to settings
   - Set up file and console handlers
   - Configure per-app log levels

3. **Add caching configuration**
   - Configure Redis or Memcached for caching
   - Use `@cache_page` decorator for appropriate views
   - Cache expensive querysets

4. **Centralize hardcoded choices**
   - **Files**: `game/models.py:18-35`, `accounts/models.py:28-48`
   - **Issue**: Choices duplicated across files
   - **Action**: Create `core/constants.py` for shared choices
   - Use constants throughout codebase

---

## 🟢 Low Priority - Feature Completeness

### Demon Gameline Implementation (CRITICAL GAP)

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

### Wraith Locations (CRITICAL GAP)

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

- [ ] **Thorn** - Demon weakness
  - File: `characters/models/demon/thorn.py`
  - Needs: Admin, reference data views, populate script

### Game App Models - Limited Implementations

- [ ] **Journal** - Character journal
  - File: `game/models.py`
  - Status: NOT in admin
  - Needs: Admin registration, improved management views

- [ ] **JournalEntry** - Individual journal entry
  - File: `game/models.py`
  - Status: NOT in admin
  - Needs: Admin registration, improved creation/edit views, templates

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

### Items - Partial Implementations

**Vampire Items (2 models)**:
- [ ] **Artifact** (Vampire) - Vampire artifact
  - File: `items/models/vampire/artifact.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

- [ ] **Bloodstone** - Mystical bloodstone
  - File: `items/models/vampire/bloodstone.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

**Wraith Items (2 models)**:
- [ ] **WraithRelic** - Wraith relic from life
  - File: `items/models/wraith/relic.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

- [ ] **Artifact** (Wraith) - Wraith artifact
  - File: `items/models/wraith/artifact.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

**Changeling Items (1 model)**:
- [ ] **Treasure** - Changeling treasure
  - File: `items/models/changeling/treasure.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

**Demon Items (1 model)**:
- [ ] **Relic** (Demon) - Demon relic
  - File: `items/models/demon/relic.py`
  - Status: Admin ✅, Views ⚠️, Templates ⚠️
  - Needs: Complete views and templates

### Locations - Partial Implementations

**Vampire Locations (4 models)**:
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

**Demon Locations (2 models)**:
- [ ] **Bastion** - Fortified stronghold of the Earthbound
  - File: `locations/models/demon/bastion.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

- [ ] **Reliquary** - Location that serves as an Earthbound's vessel
  - File: `locations/models/demon/reliquary.py`
  - Status: Admin ⚠️, Views ⚠️, Templates ⚠️
  - Needs: Complete CRUD implementation

**Changeling Locations**:
- [ ] **Changeling location models** - NOT STARTED
  - No location models exist for Changeling gameline
  - Consider: Freehold, Trod, Hollow, Dreamscape
  - Needs: Research source material, define models, implement full stack

---

## 🔵 Deployment & Environment

### Permissions System Deployment

**Status**: ✅ **READY FOR STAGING** - Development complete
**Documentation**: `docs/deployment/` - All deployment guides
**Branch**: `claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4`

#### Staging Phase (PENDING)

- [ ] **Deploy to staging**
  - Deploy permissions system to staging environment
  - Run `python test_permissions_deployment.py` (expect 37/37 passing)
  - Performance testing under load
  - Follow `docs/deployment/permissions_staging_checklist.md`

- [ ] **User acceptance testing**
  - Get feedback from real users in staging
  - Test edge cases in production-like environment
  - Verify no usability issues
  - Document any issues found

#### Production Phase (PENDING)

- [ ] **Deploy to production**
  - Final deployment of permissions system
  - Monitor error logs closely for first 24 hours
  - Be ready to rollback if issues arise
  - Follow production procedures in deployment guide

### Validation System Deployment

**Status**: ✅ **READY FOR STAGING** - Development complete
**Documentation**: `docs/deployment/` - All deployment guides
**Tools**:
- `core/management/commands/validate_data_integrity.py`
- `core/management/commands/monitor_validation.py`

#### Staging Phase (PENDING)

- [ ] **Deploy to staging**
  - Run `python manage.py validate_data_integrity --fix` to prepare data
  - Apply migrations to add database constraints
  - Test XP spending workflows (player and ST)
  - Test scene XP award workflow
  - Verify constraint violations are caught and handled gracefully
  - Monitor for 1 week (see staging deployment guide)

- [ ] **Monitor for validation errors in staging**
  - Run `python manage.py monitor_validation` daily
  - Watch logs for CheckConstraint violations
  - Monitor for transaction rollbacks
  - Track performance impact (< 10% degradation target)
  - Collect user feedback from STs and players

#### Production Phase (PENDING)

- [ ] **Deploy to production**
  - Complete staging sign-off (1 week soak period)
  - Schedule maintenance window
  - Backup production database
  - Follow production deployment checklist
  - Apply migrations to add constraints
  - Monitor actively for 24 hours

- [ ] **Monitor database constraint violations in production**
  - Set up hourly cron job: `python manage.py monitor_validation --json`
  - Configure alerts for health score < 90
  - Log violations for analysis
  - Track metrics: XP success rate, response times, constraint violations
  - Weekly review of validation health reports

---

## 🎯 Recommended Next Steps

1. **Security Issues** (High Priority) 🔥
   - Address dependency vulnerabilities
   - Fix production security settings
   - Add authentication to unprotected views
   - Implement proper authorization checks

2. **Permissions System - Staging Deployment** (High Priority) 🔥
   - Development complete - All tests passing (37/37)
   - Deploy to staging environment
   - Run automated tests in staging
   - Conduct user acceptance testing

3. **Validation System - Staging Deployment** (High Priority) 🔥
   - Development complete - All tests passing
   - Deploy to staging environment
   - Monitor for validation errors
   - Track performance impact

4. **Code Quality** (Medium Priority)
   - Fix N+1 query problems
   - Replace `.get()` with `get_object_or_404()`
   - Add model validation
   - Improve test coverage

5. **Model Implementation Gaps** (Low Priority - but large scope)
   - **Priority 1**: Complete Demon character implementation (12 models)
   - **Priority 2**: Complete Wraith location implementation (2 models)
   - **Priority 3**: Complete partial implementations (Vampire/Wraith/Changeling/Demon items and locations)
   - **Priority 4**: Enhance Game app models with better views/templates

---

## 📚 Long-term Improvements

- [x] **Consider custom User model**
  - Currently using Profile extension of Django User
  - Documented trade-offs of current approach in `docs/design/user_model_architecture.md`
  - **Decision**: Keep current User + Profile approach (migration risk too high)
  - For new projects, AbstractUser is preferred (documented in design doc)

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

**Last Updated**: 2025-11-23
**Version**: 3.0
