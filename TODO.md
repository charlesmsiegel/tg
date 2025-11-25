# TODO List

This document tracks remaining work across the codebase with context about what needs to be done.

**Legend:**
- ✅ Completed items have been **deleted** from this list
- ⚠️ Partially completed - shows what's done and what remains
- ❌ Not started - detailed description of what needs to be done

---

## 🟢 Low Priority - Feature Completeness

### Mummy Gameline Implementation (CRITICAL GAP)

⚠️ **Status**: Models exist, detail views exist, but NO create/update implementation

**What's done:**
- Models defined in `characters/models/mummy/`
- Detail templates exist
- Basic detail views work

**What remains:**

1. ❌ **Mummy character creation views**
   - Create `MummyCreateView`, `MtRHumanCreateView` in `characters/views/mummy/`
   - Create form classes in `characters/forms/mummy/`
   - Create URL patterns in `characters/urls/mummy/create.py`
   - Create form templates

2. ❌ **Mummy character update views**
   - Create `MummyUpdateView`, `MtRHumanUpdateView`
   - Create limited edit forms for owners
   - Create URL patterns in `characters/urls/mummy/update.py`

3. ❌ **Mummy reference data views**
   - Dynasty list/detail/create/update views
   - MummyTitle list/detail/create/update views
   - Populate scripts in `populate_db/`

4. ❌ **Mummy locations CRUD**
   - Tomb, UndergroundSanctuary, CultTemple need create/update views
   - Currently only detail views exist

### Hunter Gameline Implementation

⚠️ **Status**: Models exist but very limited implementation

**What remains:**

1. ❌ **Hunter character views** - Need full CRUD for Hunter, HtRHuman
2. ❌ **Hunter reference data** - Creed, Edge, HunterOrganization need views
3. ❌ **Hunter items** - HunterGear, HunterRelic need views
4. ❌ **Hunter locations** - Safehouse, HuntingGround need views

### Game App - Enhancement Opportunities

These models work but could have better user-facing views:

1. ⚠️ **Journal/JournalEntry**
   - **Done**: Model exists, basic display in character detail
   - **Remains**: Dedicated journal list view, entry creation UI improvements

2. ⚠️ **WeeklyXPRequest / StoryXPRequest**
   - **Done**: Basic CRUD exists
   - **Remains**: Enhanced approval workflow UI, batch approval for STs

---

## 🔵 Deployment & Environment

### Permissions System Deployment

**Status**: ✅ Development complete, ready for staging

1. ❌ **Deploy to staging**
   - Run `python test_permissions_deployment.py` (expect 37/37 passing)
   - Performance test under load
   - Follow `docs/deployment/permissions_staging_checklist.md`

2. ❌ **User acceptance testing in staging**
   - Get feedback from real users
   - Test edge cases
   - Document issues found

3. ❌ **Deploy to production**
   - After successful staging validation
   - Monitor error logs for 24 hours
   - Be ready to rollback

### Validation System Deployment

**Status**: ✅ Development complete, ready for staging

1. ❌ **Deploy to staging**
   - Run `python manage.py validate_data_integrity --fix`
   - Apply migrations for database constraints
   - Test XP workflows
   - Monitor for 1 week

2. ❌ **Monitor in staging**
   - Run `python manage.py monitor_validation` daily
   - Track constraint violations
   - Verify < 10% performance degradation

3. ❌ **Deploy to production**
   - Complete staging sign-off
   - Schedule maintenance window
   - Backup database before migration

---

## 📊 Summary Statistics

**Total Open Items**: ~8 items

**By Priority**:
- 🟢 Low Priority: ~4 items (feature completeness - Mummy, Hunter, Game enhancements)
- 🔵 Deployment: 6 items (staging + production)

---

## ✅ Recently Completed (removed from list)

The following items were verified as complete and removed:

### Removed 2025-11-25 (v7.5)
- **Dross (Changeling) CRUD views** - Created DrossDetailView, DrossCreateView, DrossUpdateView, DrossListView in `items/views/changeling/`. Added detail, form, and list templates. Fixed changeling URL structure to match standard pattern.

### Removed 2025-11-25 (v7.4)
- **Improve code style consistency** - Added black (24.3.0), ruff (0.3.4), pre-commit (3.7.0) to requirements. Created `.pre-commit-config.yaml` and configured `pyproject.toml` with formatting rules.

### Removed 2025-11-25 (v7.3)
- **Address dependency vulnerabilities** - Security pins applied: setuptools>=78.1.1 (CVE-2024-6345, CVE-2025-47273), cryptography>=46.0.0, bleach 6.3.0, Django 5.2.8. Periodic monitoring via Dependabot.

### Removed 2025-11-25 (v7.2)
- **Add caching configuration** - Development uses LocMemCache, production uses Redis with full configuration in `production.py`, documentation added to `docs/deployment/README.md`

### Removed 2025-11-25 (v7.1)
- **Implement authorization checks in game/views.py** - Chronicle-specific ST check for scene closing, character ownership checks for adding/posting
- **Simplify filter_queryset_for_user** - Refactored into helper methods, removed duplicate observer filter code

### Removed 2025-11-25 (v7.0)
- **Fix N+1 query problems** - All methods optimized: `st_relations()` uses `for_user_optimized()`, `weekly_characters()` uses `select_related()`, `rotes_to_approve()` uses `prefetch_related()` with Prefetch
- **Dual XP Tracking Systems** - JSONField removed, `XPSpendingRequest` model fully implemented with proper ForeignKey relationships
- **Move business logic out of forms** - `SceneXP.save()` and `StoryXP.save()` properly delegate to model methods `Scene.award_xp()` and `Story.award_xp()`
- **Simplify remove_from_organizations()** - Refactored to use `CharacterOrganizationRegistry` pattern in `core/utils.py`
- **Add model validation for Character status field** - Implemented with `STATUS_TRANSITIONS` state machine and `clean()` method
- **Add tests for Character model** - 288 test methods exist across test files including comprehensive validation tests in `characters/tests/core/`
- **Refactor SpecialUserMixin ST Check** - Already uses canonical `user.profile.is_st()` at `core/mixins.py:237`
- **Reduce Hardcoded Field Lists in AbilityBlock** - Already imports from `core/constants.py` AbilityFields
- **Address fat models with complex inheritance** - Current composition approach is sufficient; manager-based composition implemented

### Previously Removed
- **Add authentication to views** - LoginRequiredMixin now used throughout game/views.py
- **Update deprecated mixin import paths** - All code uses `core.mixins`, only docs have old references
- **Move signal registration to apps.py** - `accounts/signals.py` exists and is properly imported
- **Standardize CBV patterns in game/views.py** - All views now use proper DetailView, ListView, CreateView
- **Add Django Debug Toolbar** - Configured in `tg/settings/development.py`
- **Configure structured logging** - LOGGING configured in `tg/settings/base.py` with dev/prod customizations
- **Add database indexes** - `models.Index` entries added to Post, JournalEntry, WeeklyXPRequest, XPSpendingRequest
- **Centralize hardcoded choices** - `core/constants.py` has CharacterStatus, AbilityFields, XPApprovalStatus, etc.
- **Simplify Custom QuerySet Initialization** - Refactored to use Django's standard manager pattern
- **Remove Unnecessary ApprovedUserContextMixin** - Removed from all views
- **Fix Status Validation Redundancy** - Recent commit "Fix status validation redundancy in Character model"
- **Vampire locations** - Haven, Domain, Elysium, Rack all have full CRUD views in `locations/views/vampire/__init__.py`
- **Changeling locations** - Freehold, Holding, Trod, DreamRealm models exist in `locations/models/changeling/`
- **Demon gameline views** - Views exist for Demon, DtFHuman, Earthbound, Faction, House, Lore, Pact, Thrall, Visage
- **Demon gameline templates** - Templates exist for all demon character types

---

**Last Updated**: 2025-11-25
**Version**: 7.5 (Added Dross CRUD views and templates)
