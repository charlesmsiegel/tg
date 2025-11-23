# TODO List

This document tracks remaining work across the codebase with context about what needs to be done.

---

## 🔴 High Priority

### Security

1. **Address dependency vulnerabilities**
   - **Status**: 9 vulnerabilities detected (1 critical, 3 high, 4 moderate, 1 low)
   - **Action**: Review and update vulnerable dependencies
   - **Check**: https://github.com/charlesmsiegel/tg/security/dependabot

2. **Complete production security configuration**
   - **File**: `tg/settings.py:27-33`
   - **Status**: ✅ Partially fixed - DEBUG and ALLOWED_HOSTS now use environment variables
   - **Remaining Actions**:
     - Configure proper SECRET_KEY from environment (currently commented out)
     - Create environment-specific settings files (base.py, development.py, production.py)
     - Add additional security headers and CSRF settings for production

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

### Code Quality & Redundancy Cleanup

6. **✅ COMPLETED: Consolidate QuerySet and Manager Methods**
   - **Files**: `core/models.py:71-73` (consolidated)
   - **Impact**: HIGH - Eliminated 70+ lines of duplicate code
   - **Solution Implemented**: Used `PolymorphicManager.from_queryset()` pattern
   - **Result**: All six methods now defined once in `ModelQuerySet`:
     - `pending_approval_for_user()`
     - `visible()`
     - `for_chronicle()`
     - `owned_by()`
     - `with_pending_images()`
     - `for_user_chronicles()`
   - **Manager Creation**: `ModelManager = PolymorphicManager.from_queryset(ModelQuerySet)`
   - **Completed**: 2025-11-23

7. **Eliminate Duplicate Limited Edit Forms**
   - **Files**: `characters/forms/core/limited_edit.py:125-207`
   - **Impact**: HIGH - 82 lines of boilerplate code
   - **Issue**: 12 form classes that differ ONLY by their `Meta.model` attribute:
     - LimitedMageEditForm, LimitedMtAHumanEditForm, LimitedVampireEditForm
     - LimitedVtMHumanEditForm, LimitedGarouEditForm, LimitedWtAHumanEditForm
     - LimitedChangelingEditForm, LimitedCtDHumanEditForm, LimitedWraithEditForm
     - LimitedWtOHumanEditForm, LimitedDemonEditForm, LimitedDtFHumanEditForm
   - **Action**: Create factory function or generic form
   - **Solution**:
     ```python
     def create_limited_edit_form(model_class):
         """Factory function to create a limited edit form for a specific model."""
         class GeneratedLimitedEditForm(LimitedHumanEditForm):
             class Meta(LimitedHumanEditForm.Meta):
                 model = model_class
         GeneratedLimitedEditForm.__name__ = f'Limited{model_class.__name__}EditForm'
         return GeneratedLimitedEditForm
     ```

8. **Update Deprecated Mixin Import Paths**
   - **Files Affected**: 18 character view files
   - **Impact**: MEDIUM - Confusing import patterns, extra files to maintain
   - **Issue**: Despite consolidation to `core.mixins`, many files still import from deprecated shims
   - **Files Using Old Imports**:
     - characters/views/wraith/wtohuman.py
     - characters/views/werewolf/wtahuman.py, garou.py, fomor.py, fera.py
     - characters/views/vampire/vtmhuman.py, ghoul_chargen.py, vampire_chargen.py
     - characters/views/mage/sorcerer.py, mtahuman.py, mage.py, companion.py
     - characters/views/changeling/changeling.py, ctdhuman.py
     - characters/views/demon/demon_chargen.py, dtfhuman_chargen.py, thrall_chargen.py
     - characters/views/wraith/wraith_chargen.py
   - **Action**: Update imports from `from core.views.approved_user_mixin import SpecialUserMixin` to `from core.mixins import SpecialUserMixin`
   - **After**: Delete backward compatibility shims:
     - `core/views/message_mixin.py`
     - `core/views/approved_user_mixin.py`

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

3. **Dual XP Tracking Systems (Needs Data Migration)**
   - **Files**: `characters/models/core/character.py:116-530`
   - **Impact**: HIGH - Two parallel systems creating maintenance burden
   - **Issue**: Character maintains TWO complete XP tracking implementations:
     - **Old JSONField System** (deprecated): `spent_xp = models.JSONField(default=list)`
     - **New Model-Based System**: `XPSpendingRequest` model
     - **Compatibility Layer**: `has_pending_xp_or_model_requests()`, `total_spent_xp_combined()`
   - **Action**:
     1. Create data migration to convert JSONField data to XPSpendingRequest records
     2. Update all views using old system
     3. Update templates displaying `spent_xp` JSONField
     4. Remove old methods (lines 294-374)
     5. Remove `spent_xp` field
     6. Remove compatibility methods (lines 491-530)

4. **Move business logic out of forms**
   - **File**: `accounts/forms.py:89-96`
   - **Issue**: SceneXP.save() contains business logic
   - **Action**: Move XP award logic to model methods
   - Keep forms focused on data validation

5. **Address fat models with complex inheritance**
   - **Files**: `characters/models/core/`
   - **Issue**: Human class has 7+ parent classes
   - **Action**: Consider composition over inheritance
   - Evaluate proxy models for polymorphic behavior

6. **Move signal registration to apps.py**
   - **File**: `accounts/models.py:264-268`
   - **Issue**: Signal registered in models.py
   - **Action**: Move to `accounts/apps.py` ready() method
   - Create separate `accounts/signals.py` module

7. **Simplify remove_from_organizations() Method**
   - **Files**: `characters/models/core/character.py:206-258`
   - **Impact**: MEDIUM - Tight coupling, hard to extend
   - **Issue**: Method has 9 different `hasattr()` checks for different organizational structures
   - **Action**: Refactor using Django signals or registry pattern
   - Let each related model handle its own cleanup
   - Reduces coupling and improves extensibility

8. **Simplify Custom QuerySet Initialization**
   - **Files**: `core/models.py:25-34`
   - **Impact**: MEDIUM - Fragile internal query manipulation
   - **Issue**: `ModelQuerySet.__init__()` manually manipulates internal `query.select_related` dictionary
   - **Action**: Consider removing and relying on polymorphic library optimization, or use cleaner override pattern

9. **Simplify filter_queryset_for_user Implementation**
   - **Files**: `core/permissions.py:310-381`
   - **Impact**: MEDIUM - Hard to maintain, performance concerns
   - **Issue**: Uses broad exception handling and complex subqueries
   - **Action**: Replace broad `except Exception` with proper field checking
   - Consider breaking into smaller, testable methods
   - Profile performance of current vs simpler approaches

### Model & Data Validation

10. **Add model validation**
    - **Files**: Most models across all apps
    - **Issue**: Most models lack `clean()` methods
    - **Action**: Add validation in `clean()` for data integrity
    - Call `full_clean()` in `save()` methods

11. **Fix class name typo**
    - **File**: `accounts/forms.py:24`
    - **Issue**: `CustomUSerCreationForm` should be `CustomUserCreationForm`
    - **Action**: Update class name and all references

12. **Fix Status Validation Redundancy**
    - **Files**: `characters/models/core/character.py:122-188`
    - **Impact**: LOW - Confusing but functional
    - **Issue**: Status validation happens in three places with contradictory behavior
    - **Action**: Decide on validation strategy (strict, lenient, or clear opt-out)
    - Remove try/except that swallows ValidationError

### Testing

13. **Improve test coverage**
    - **Current**: Only `accounts/tests.py` has substantial tests
    - **Goal**: 80%+ coverage across all apps
    - **Action**: Add comprehensive test suite using Django's unittest framework
    - Test all views, forms, and model methods

14. **Standardize CBV patterns**
    - **File**: `game/views.py`
    - **Issue**: Views inherit from View but don't follow CBV patterns
    - **Action**: Use proper Django generic views (DetailView, ListView, etc.)
    - Follow standard `get_context_data()` pattern

### Development Tools

15. **Add Django Debug Toolbar**
    - Configure in development settings
    - Helps identify N+1 queries and performance issues

16. **Configure logging**
    - Add LOGGING configuration to settings
    - Set up file and console handlers
    - Configure per-app log levels

17. **Add caching configuration**
    - Configure Redis or Memcached for caching
    - Use `@cache_page` decorator for appropriate views
    - Cache expensive querysets

18. **Centralize hardcoded choices**
    - **Files**: `game/models.py:18-35`, `accounts/models.py:28-48`
    - **Issue**: Choices duplicated across files
    - **Action**: Create `core/constants.py` for shared choices
    - Use constants throughout codebase

### Code Quality Improvements

19. **Simplify Gameline Detection**
    - **Files**: `core/models.py:352-372`
    - **Impact**: LOW - Fragile string parsing
    - **Issue**: Models detect gameline by parsing class module path strings
    - **Action**: Use gameline class attribute and settings lookup
    - Use existing `get_gameline_name()` utility from `core/utils.py:75-87`

20. **Simplify Observer Permission Check**
    - **Files**: `core/permissions.py:156-164`
    - **Impact**: LOW - Works but could be cleaner
    - **Issue**: Checking observer status requires ContentType lookup
    - **Action**: Use GenericRelation directly instead of ContentType lookup

21. **Refactor SpecialUserMixin ST Check**
    - **Files**: `core/mixins.py:250`
    - **Impact**: LOW - Minor redundancy
    - **Issue**: Queries `STRelationship` directly instead of using `user.profile.is_st()`
    - **Action**: Replace direct query with canonical `is_st()` method
    - Use `.exists()` instead of `.count() > 0`

22. **Consolidate ST Check Logic in Template Tags**
    - **Files**: `core/templatetags/permissions.py:147-163`
    - **Impact**: LOW - Minor redundancy
    - **Issue**: The `is_st()` template tag reimplements admin/ST checking logic
    - **Action**: Investigate if object-specific ST checking is needed
    - If not, delegate to canonical `user.profile.is_st()` method

23. **Remove Unnecessary ApprovedUserContextMixin**
    - **Files**: `characters/views/core/character.py:112`, `core/mixins.py:197-213`
    - **Impact**: LOW - Minor code smell
    - **Issue**: Just adds `is_approved_user=True` to context when permission mixin already verified access
    - **Action**: Remove mixin and add context flags directly where needed

24. **Optimize at_freebie_step() QuerySet Method**
    - **Files**: `characters/models/core/character.py:68-84`
    - **Impact**: LOW - Performance issue but likely not called often
    - **Issue**: Method evaluates entire queryset to filter it
    - **Action**: Make `freebie_step` a database field or use annotations
    - Or remove queryset method and filter in Python where needed

25. **Reduce Hardcoded Field Lists in AbilityBlock**
    - **Files**: `characters/models/core/ability_block.py:13-45`
    - **Impact**: LOW - Maintenance burden but rarely changes
    - **Issue**: Ability names hardcoded in model class attributes, duplicating field definitions
    - **Action**: Use model introspection, move to constants, or generate fields programmatically

---

## 🟢 Low Priority - Feature Completeness

### Demon Gameline Implementation (CRITICAL GAP)

**Status**: 11 models defined but incomplete admin/views/templates

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
   - Complete production security configuration
   - Add authentication to unprotected views
   - Implement proper authorization checks

2. **Code Quality Cleanup** (High Priority) 🔥
   - Consolidate QuerySet/Manager methods (#6)
   - Eliminate duplicate Limited Edit Forms (#7)
   - Update deprecated mixin imports (#8)

3. **Permissions System - Staging Deployment** (High Priority) 🔥
   - Development complete - All tests passing (37/37)
   - Deploy to staging environment
   - Run automated tests in staging
   - Conduct user acceptance testing

4. **Validation System - Staging Deployment** (High Priority) 🔥
   - Development complete - All tests passing
   - Deploy to staging environment
   - Monitor for validation errors
   - Track performance impact

5. **Architecture Improvements** (Medium Priority)
   - Migrate dual XP tracking systems (#3)
   - Fix N+1 query problems
   - Replace `.get()` with `get_object_or_404()`
   - Add model validation
   - Improve test coverage

6. **Model Implementation Gaps** (Low Priority - but large scope)
   - **Priority 1**: Complete Demon character implementation (11 models)
   - **Priority 2**: Complete partial implementations (Vampire/Wraith/Changeling/Demon items and locations)
   - **Priority 3**: Enhance Game app models with better views/templates

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

## 📊 Summary Statistics

**Total Open Items**: ~60 items across all priorities

**By Priority**:
- 🔴 High Priority: 8 items (security + critical code quality)
- 🟡 Medium Priority: 17 items (performance + architecture + testing)
- 🟢 Low Priority: ~35 items (feature completeness + polish)
- 🔵 Deployment: 7 items (staging + production deployments)

**Estimated Effort**:
- High Priority Security/Code Quality: 16-32 hours
- Medium Priority Architecture: 20-40 hours
- Low Priority Features: 80-120 hours (large scope)
- Deployment: 8-16 hours per system (permissions + validation)

---

**Last Updated**: 2025-11-23
**Version**: 4.0 (Consolidated from TODO.md, TODO_REDUNDANCY.md, TODO_OVERCOMPLEX.md)
