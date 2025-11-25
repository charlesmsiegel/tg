# TODO List

This document tracks remaining work across the codebase with context about what needs to be done.

---

## 🔴 High Priority

### Security

1. **Address dependency vulnerabilities**
   - **Status**: 9 vulnerabilities detected (1 critical, 3 high, 4 moderate, 1 low)
   - **Action**: Review and update vulnerable dependencies
   - **Check**: https://github.com/charlesmsiegel/tg/security/dependabot
   - **Context**: Run `pip list --outdated` and check Dependabot alerts
   - **Independence**: Standalone task - can be done independently

2. **Add authentication to views**
   - **Files**: `game/views.py` - ChronicleDetailView, SceneDetailView, ChronicleScenesDetailView
   - **Issue**: Views lack `LoginRequiredMixin`, allowing unauthenticated access
   - **Action**:
     - Import: `from django.contrib.auth.mixins import LoginRequiredMixin`
     - Add `LoginRequiredMixin` as first parent class to each view
     - Example: `class ChronicleDetailView(LoginRequiredMixin, View):`
   - **Context**: LoginRequiredMixin redirects unauthenticated users to login page
   - **Independence**: Standalone task - can be done independently

3. **Implement authorization checks**
   - **Files**: `game/views.py` throughout
   - **Issue**: Users can close any scene, post as any character, approve XP without ST status
   - **Action**:
     - Check if user has permission before allowing scene closing, posting, XP approval
     - Use existing `user.profile.is_st()` method for ST-only actions
     - Add checks like `if not request.user.profile.is_st(): return HttpResponseForbidden()`
   - **Context**: See `core/permissions.py` for PermissionManager and `accounts/models.py` for is_st() method
   - **Dependencies**: Requires authentication (task #2) to be in place
   - **Independence**: Can be done after task #2 is complete

### Code Quality & Redundancy Cleanup

**Note**: Task #6 "Eliminate Duplicate Limited Edit Forms" was completed - factory function implemented in `characters/forms/core/limited_edit.py`.

6. **Update Deprecated Mixin Import Paths**
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
   - **Action**:
     1. In each file, replace old imports:
        - FROM: `from core.views.approved_user_mixin import SpecialUserMixin`
        - TO: `from core.mixins import SpecialUserMixin`
     2. After all files updated, delete backward compatibility shims:
        - `core/views/message_mixin.py`
        - `core/views/approved_user_mixin.py`
   - **Context**: All mixins consolidated in `core/mixins.py` (see CLAUDE.md coding standards)
   - **Independence**: Standalone task - can be done independently

---

## 🟡 Medium Priority

### Performance

1. **Fix N+1 query problems**
   - **Files**:
     - `accounts/models.py:115-121` - st_relations() causes N queries
     - `game/models.py:196-205` - weekly_characters() queries per scene
     - `accounts/models.py:163-170` - rotes_to_approve() queries per rote
   - **Issue**: Methods iterate without prefetching related objects
   - **Action**:
     - Use `select_related()` for ForeignKey/OneToOne relationships
     - Use `prefetch_related()` for ManyToMany/reverse ForeignKey relationships
     - Example: `self.storyteller_relationships.select_related('chronicle').all()`
   - **Context**: See CLAUDE.md "Preventing N+1 Queries" section for examples
   - **How to verify**: Install Django Debug Toolbar (task Medium #11) to see query counts
   - **Independence**: Standalone task - can be done independently

2. **Add database indexes**
   - **File**: `game/models.py:322-328` - Post model
   - **Issue**: Post model lacks indexes on frequently queried fields
   - **Action**:
     - Add `db_index=True` to datetime_created field
     - Add Meta.indexes for composite queries:
       ```python
       class Meta:
           indexes = [
               models.Index(fields=['scene', '-datetime_created']),
               models.Index(fields=['character', '-datetime_created']),
           ]
       ```
     - Create and run migration: `python manage.py makemigrations`
   - **Context**: Indexes speed up filtering and ordering queries
   - **Independence**: Standalone task - can be done independently

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
     2. Find all views using `spent_xp` JSONField (grep for "spent_xp")
     3. Update views to use XPSpendingRequest queryset
     4. Find all templates displaying `spent_xp` (grep in templates/)
     5. Update templates to display XPSpendingRequest objects
     6. Remove old methods (lines 294-374)
     7. Remove `spent_xp` field from Character model
     8. Remove compatibility methods (lines 491-530)
   - **Context**: XPSpendingRequest is in `characters/models/core/xp.py`
   - **Dependencies**: Large refactor - should audit all XP-related code first
   - **Independence**: Complex task - requires careful planning and testing

4. **Move business logic out of forms**
   - **File**: `accounts/forms.py:89-96` - SceneXP form
   - **Issue**: Form's save() method contains business logic for XP awards
   - **Action**:
     1. Create method in Scene model: `award_xp_to_character(character, amount, chronicle)`
     2. Move XP award logic from form.save() to this model method
     3. Update form.save() to call `self.instance.scene.award_xp_to_character(...)`
   - **Context**: Forms should validate data, models should handle business logic (Django best practice)
   - **Independence**: Standalone task - can be done independently

5. **Address fat models with complex inheritance**
   - **Files**: `characters/models/core/human.py`
   - **Issue**: Human class has 7+ parent classes, creating complex inheritance chain
   - **Current Inheritance**: Human → Character → (AttributeBlock, AbilityBlock, AdvantageBlock, etc.)
   - **Action**:
     1. Review Human class and all parent classes
     2. Identify which mixins could be converted to composition (has-a vs is-a)
     3. Consider creating explicit ForeignKey relationships instead of multiple inheritance
     4. Example: Instead of inheriting AttributeBlock, use `attributes = models.OneToOneField(AttributeBlock)`
   - **Context**: Complex inheritance makes debugging difficult and increases coupling
   - **Dependencies**: Large refactor - should create detailed plan first
   - **Independence**: Complex task - requires architectural decisions

6. **Move signal registration to apps.py**
   - **File**: `accounts/models.py:264-268`
   - **Issue**: Signal registered at module level in models.py instead of apps.py
   - **Action**:
     1. Create `accounts/signals.py` with signal handler:
        ```python
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from django.contrib.auth.models import User
        from .models import Profile

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)
        ```
     2. In `accounts/apps.py`, import signals in ready() method:
        ```python
        def ready(self):
            import accounts.signals
        ```
     3. Remove signal registration from `accounts/models.py:264-268`
   - **Context**: Django best practice - signals should be in apps.py to avoid import ordering issues
   - **Independence**: Standalone task - can be done independently

7. **Simplify remove_from_organizations() Method**
   - **Files**: `characters/models/core/character.py:206-258`
   - **Impact**: MEDIUM - Tight coupling, hard to extend
   - **Issue**: Method has 9 different `hasattr()` checks for different organizational structures
   - **Action**:
     1. Create `pre_delete` signal in Character model
     2. In each organization model (Pack, Cabal, Coterie, etc.), create signal handler:
        ```python
        @receiver(pre_delete, sender=Character)
        def remove_from_pack(sender, instance, **kwargs):
            if hasattr(instance, 'pack'):
                instance.pack.remove_character(instance)
        ```
     3. Remove remove_from_organizations() method from Character
   - **Context**: Signals decouple character from organization-specific logic
   - **Independence**: Standalone task - can be done independently

8. **Simplify Custom QuerySet Initialization**
   - **Files**: `core/models.py:25-34`
   - **Impact**: MEDIUM - Fragile internal query manipulation
   - **Issue**: `ModelQuerySet.__init__()` manually manipulates internal `query.select_related` dictionary
   - **Action**:
     1. Test if removing custom __init__() breaks anything (run full test suite)
     2. If tests pass, remove __init__() override and rely on polymorphic library
     3. If tests fail, refactor to use standard queryset methods instead of internal manipulation
   - **Context**: Manipulating `query._` internals is fragile and may break with Django updates
   - **Independence**: Standalone task - can be done independently with thorough testing

9. **Simplify filter_queryset_for_user Implementation**
   - **Files**: `core/permissions.py:310-381`
   - **Impact**: MEDIUM - Hard to maintain, performance concerns
   - **Issue**: Uses broad exception handling and complex subqueries
   - **Action**:
     1. Replace `except Exception:` with specific field existence check:
        ```python
        if hasattr(model, 'owner') and hasattr(model.owner.field, 'related_model'):
        ```
     2. Break method into smaller methods: `_filter_by_owner()`, `_filter_by_chronicle()`, etc.
     3. Profile performance with Django Debug Toolbar
     4. Compare current vs refactored approach
   - **Context**: Broad exception handling masks bugs and makes debugging difficult
   - **Independence**: Standalone task - can be done independently

### Model & Data Validation

10. **Add model validation for Character status field**
    - **Files**: `characters/models/core/character.py`
    - **Issue**: Most models lack `clean()` methods for data integrity validation
    - **Action**:
      1. Add clean() method to Character model:
         ```python
         def clean(self):
             if self.status == 'App' and self.total_freebies() > 0:
                 raise ValidationError("Cannot approve character with unspent freebies")
         ```
      2. Call full_clean() in save():
         ```python
         def save(self, *args, **kwargs):
             if not kwargs.pop('skip_validation', False):
                 self.full_clean()
             super().save(*args, **kwargs)
         ```
      3. Test with existing characters to identify validation issues
    - **Context**: This is a specific, actionable subset of broader validation work
    - **Independence**: Standalone task - can be done independently

11. **Fix Status Validation Redundancy**
    - **Files**: `characters/models/core/character.py:122-188`
    - **Impact**: LOW - Confusing but functional
    - **Issue**: Status validation happens in three places with contradictory behavior:
      1. `clean()` method raises ValidationError
      2. `save()` method has try/except that swallows ValidationError
      3. Custom save has different validation logic
    - **Action**:
      1. Decide on validation strategy: strict (always validate), lenient (allow skip), or opt-out
      2. Remove try/except that swallows ValidationError in save()
      3. Add `skip_validation` parameter if needed for migrations/fixtures
      4. Document when validation is skipped
    - **Context**: Swallowing ValidationError makes debugging impossible
    - **Independence**: Standalone task - can be done independently

### Testing

12. **Add tests for Character model**
    - **Current**: Only `accounts/tests.py` has substantial tests
    - **Goal**: Add comprehensive tests for Character model as starting point
    - **Files**: Create `characters/tests/core/test_character.py`
    - **Action**:
      1. Create test file with CharacterTestCase class
      2. Add tests for:
         - Character creation and validation
         - XP spending and approval
         - Status transitions (Un → Sub → App)
         - Freebie point spending
         - Organization membership
      3. Run tests: `python manage.py test characters.tests.core.test_character`
    - **Context**: Use Django's unittest framework (see existing `accounts/tests.py` as template)
    - **Independence**: Standalone task - can be done independently

13. **Standardize CBV patterns in game/views.py**
    - **File**: `game/views.py`
    - **Issue**: Views inherit from View but don't follow CBV patterns
    - **Action**:
      1. Identify views that should be DetailView (show single object)
      2. Identify views that should be ListView (show multiple objects)
      3. Refactor one view at a time:
         - Replace `View` with appropriate generic view
         - Move context building to `get_context_data()`
         - Move queryset logic to `get_queryset()`
      4. Example:
         ```python
         # Before: class ChronicleDetailView(View)
         # After:
         class ChronicleDetailView(LoginRequiredMixin, DetailView):
             model = Chronicle
             template_name = 'game/chronicle_detail.html'

             def get_context_data(self, **kwargs):
                 context = super().get_context_data(**kwargs)
                 context['scenes'] = self.object.scenes.all()
                 return context
         ```
    - **Context**: Generic views reduce boilerplate and follow Django best practices
    - **Independence**: Can be done view-by-view incrementally

### Development Tools

14. **Add Django Debug Toolbar**
    - **Files**: `tg/settings.py`, `requirements.txt`, `tg/urls.py`
    - **Issue**: No visibility into query performance and N+1 issues
    - **Action**:
      1. Add to requirements.txt: `django-debug-toolbar==4.2.0`
      2. Install: `pip install django-debug-toolbar`
      3. Add to INSTALLED_APPS: `'debug_toolbar',`
      4. Add to MIDDLEWARE (after CommonMiddleware): `'debug_toolbar.middleware.DebugToolbarMiddleware',`
      5. Add to urls.py:
         ```python
         if settings.DEBUG:
             import debug_toolbar
             urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
         ```
      6. Add to settings.py: `INTERNAL_IPS = ['127.0.0.1']`
    - **Context**: Toolbar shows queries, templates, cache hits, etc. in browser
    - **Independence**: Standalone task - can be done independently

15. **Configure structured logging**
    - **Files**: `tg/settings.py`
    - **Issue**: No logging configuration makes debugging production issues difficult
    - **Action**:
      1. Add LOGGING configuration to settings.py:
         ```python
         LOGGING = {
             'version': 1,
             'disable_existing_loggers': False,
             'formatters': {
                 'verbose': {
                     'format': '{levelname} {asctime} {module} {message}',
                     'style': '{',
                 },
             },
             'handlers': {
                 'file': {
                     'level': 'INFO',
                     'class': 'logging.FileHandler',
                     'filename': 'logs/django.log',
                     'formatter': 'verbose',
                 },
                 'console': {
                     'level': 'DEBUG',
                     'class': 'logging.StreamHandler',
                     'formatter': 'verbose',
                 },
             },
             'root': {
                 'handlers': ['console', 'file'],
                 'level': 'INFO',
             },
             'loggers': {
                 'django': {
                     'handlers': ['console', 'file'],
                     'level': 'INFO',
                     'propagate': False,
                 },
             },
         }
         ```
      2. Create logs/ directory: `mkdir logs`
      3. Add logs/ to .gitignore
    - **Context**: Structured logging helps track errors and debug issues in production
    - **Independence**: Standalone task - can be done independently

16. **Add caching configuration**
    - **Files**: `tg/settings.py`
    - **Issue**: No caching configured, expensive queries run repeatedly
    - **Action**:
      1. For development, use local-memory cache in settings.py:
         ```python
         CACHES = {
             'default': {
                 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                 'LOCATION': 'unique-snowflake',
             }
         }
         ```
      2. For production, document Redis setup in deployment guide:
         - Install Redis: `pip install django-redis`
         - Configure Redis backend in production settings
      3. Add cache to expensive views:
         ```python
         from django.views.decorators.cache import cache_page

         @cache_page(60 * 15)  # Cache for 15 minutes
         def expensive_view(request):
             ...
         ```
    - **Context**: Start with local-memory cache, upgrade to Redis in production
    - **Independence**: Standalone task - can be done independently

17. **Centralize hardcoded choices**
    - **Files**: `game/models.py:18-35`, `accounts/models.py:28-48`
    - **Issue**: Choices duplicated across files (status choices, relationship types, etc.)
    - **Action**:
      1. Create `core/constants.py`:
         ```python
         # Status choices used by Character, Location, Item
         STATUS_CHOICES = [
             ('Un', 'Unfinished'),
             ('Sub', 'Submitted'),
             ('App', 'Approved'),
             ('Ret', 'Retired'),
             ('Dec', 'Deceased'),
         ]

         # Add other shared choices here
         ```
      2. Update models to import from constants:
         ```python
         from core.constants import STATUS_CHOICES

         class Character(Model):
             status = models.CharField(max_length=3, choices=STATUS_CHOICES)
         ```
      3. Search for duplicate choice definitions and replace
    - **Context**: DRY principle - define choices once, use everywhere
    - **Independence**: Standalone task - can be done independently

### Code Quality Improvements

18. **Simplify Gameline Detection**
    - **Files**: `core/models.py:352-372`
    - **Impact**: LOW - Fragile string parsing
    - **Issue**: Models detect gameline by parsing class module path strings
    - **Current**: Parses `'characters.models.vampire.vtmhuman'` to extract 'vampire'
    - **Action**:
      1. Add gameline attribute to model classes:
         ```python
         class VtMHuman(Human):
             gameline = 'vtm'
         ```
      2. Update `get_gameline()` to check attribute first:
         ```python
         def get_gameline(self):
             if hasattr(self, 'gameline'):
                 return self.gameline
             # Fall back to existing string parsing
         ```
      3. Use existing `get_gameline_name()` from `core/utils.py:75-87` for display names
    - **Context**: Explicit is better than implicit - fragile string parsing can break with refactoring
    - **Independence**: Standalone task - can be done independently

19. **Simplify Observer Permission Check**
    - **Files**: `core/permissions.py:156-164`
    - **Impact**: LOW - Works but could be cleaner
    - **Issue**: Checking observer status requires ContentType lookup
    - **Current**: Uses `ContentType.objects.get_for_model()` to check GenericForeignKey
    - **Action**:
      1. Add GenericRelation to observed objects:
         ```python
         from django.contrib.contenttypes.fields import GenericRelation

         class Character(Model):
             observers = GenericRelation('core.Observer', related_query_name='character')
         ```
      2. Update permission check to use relation:
         ```python
         return obj.observers.filter(user=user).exists()
         ```
    - **Context**: GenericRelation provides cleaner reverse lookup than ContentType queries
    - **Independence**: Standalone task - can be done independently

21. **Refactor SpecialUserMixin ST Check**
    - **Files**: `core/mixins.py:250`
    - **Impact**: LOW - Minor redundancy
    - **Issue**: Queries `STRelationship` directly instead of using canonical `user.profile.is_st()`
    - **Current**: `STRelationship.objects.filter(st=request.user).count() > 0`
    - **Action**:
      1. Replace with canonical method:
         ```python
         return request.user.profile.is_st()
         ```
      2. If object-specific ST check needed, use:
         ```python
         return request.user.profile.is_st() or obj.chronicle.storytellers.filter(pk=request.user.pk).exists()
         ```
    - **Context**: DRY principle - use existing is_st() method
    - **Independence**: Standalone task - can be done independently

22. **Consolidate ST Check Logic in Template Tags**
    - **Files**: `core/templatetags/permissions.py:147-163`
    - **Impact**: LOW - Minor redundancy
    - **Issue**: The `is_st()` template tag reimplements admin/ST checking logic
    - **Action**:
      1. Review if object-specific ST checking is needed in templates
      2. If not needed, simplify to:
         ```python
         @register.simple_tag
         def is_st(user):
             return user.profile.is_st()
         ```
      3. If object-specific check needed, add parameter:
         ```python
         @register.simple_tag
         def is_st(user, obj=None):
             if obj and hasattr(obj, 'chronicle'):
                 return obj.chronicle.storytellers.filter(pk=user.pk).exists()
             return user.profile.is_st()
         ```
    - **Context**: Delegate to canonical is_st() method instead of reimplementing
    - **Independence**: Standalone task - can be done independently

23. **Remove Unnecessary ApprovedUserContextMixin**
    - **Files**: `characters/views/core/character.py:112`, `core/mixins.py:197-213`
    - **Impact**: LOW - Minor code smell
    - **Issue**: Mixin only adds `is_approved_user=True` to context after permission check
    - **Action**:
      1. Find all views using ApprovedUserContextMixin (grep codebase)
      2. Remove mixin from view inheritance
      3. Add context variable directly in get_context_data() where needed:
         ```python
         def get_context_data(self, **kwargs):
             context = super().get_context_data(**kwargs)
             context['is_approved_user'] = True
             return context
         ```
      4. Delete ApprovedUserContextMixin from `core/mixins.py` after all uses removed
    - **Context**: Unnecessary abstraction - permission mixin already verified access
    - **Independence**: Standalone task - can be done independently

24. **Optimize at_freebie_step() QuerySet Method**
    - **Files**: `characters/models/core/character.py:68-84`
    - **Impact**: LOW - Performance issue but likely not called often
    - **Issue**: Method evaluates entire queryset to filter it (loads all characters into memory)
    - **Current**: `return [char for char in self.all() if char.freebie_step()]`
    - **Action**:
      1. Option A: Add `freebie_step_complete` boolean field to Character model
      2. Option B: Remove queryset method, filter in Python where needed
      3. Option C: Use annotation if logic allows database calculation
    - **Context**: List comprehension defeats queryset lazy evaluation
    - **Independence**: Standalone task - can be done independently

25. **Reduce Hardcoded Field Lists in AbilityBlock**
    - **Files**: `characters/models/core/ability_block.py:13-45`
    - **Impact**: LOW - Maintenance burden but rarely changes
    - **Issue**: Ability names hardcoded in class attributes, duplicating field definitions
    - **Current**: `TALENTS = ['alertness', 'athletics', 'brawl', ...]` then define each as field
    - **Action**:
      1. Option A: Generate fields programmatically from TALENTS/SKILLS/KNOWLEDGES lists
      2. Option B: Move lists to `core/constants.py` for single source of truth
      3. Option C: Use model introspection: `self._meta.get_fields()` to get ability fields
    - **Context**: Field lists are stable (from WoD rulebooks), but duplication is maintenance risk
    - **Independence**: Standalone task - can be done independently

---

## 🟢 Low Priority - Feature Completeness

### Demon Gameline Implementation (CRITICAL GAP)

**Status**: 11 models defined but incomplete admin/views/templates
**Context**: Models exist in `characters/models/demon/` but lack full CRUD implementation
**Pattern**: Follow existing gameline implementations (vampire, werewolf, mage) as templates

Models needing full implementation:

1. **Demon** - Base demon character class
   - **File**: `characters/models/demon/demon.py`
   - **Needs**: Admin, views, forms, templates, URLs
   - **Template**: Copy structure from `characters/models/vampire/vampire.py`
   - **Independence**: Standalone - can implement admin/views/templates separately

2. **DtFHuman** - Demon in human form (playable character)
   - **File**: `characters/models/demon/dtfhuman.py`
   - **Needs**: Admin, character creation views, detail/update views, templates
   - **Fields**: House, Faction, Torment, Faith, Lores, Apocalyptic Form
   - **Template**: Copy structure from `characters/views/vampire/vampire.py` and templates
   - **Independence**: Depends on Demon, Visage, Lore, DemonHouse, DemonFaction models having admin

3. **Visage** - Demonic visage/appearance
   - **File**: `characters/models/demon/visage.py`
   - **Needs**: Admin registration, reference data views, populate script
   - **Template**: Similar to `characters/models/vampire/clan.py`
   - **Independence**: Standalone - can implement independently

4. **Lore** - Demonic lore/knowledge
   - **File**: `characters/models/demon/lore.py`
   - **Needs**: Admin registration, reference data views, populate script
   - **Template**: Similar to `characters/models/vampire/discipline.py`
   - **Independence**: Standalone - can implement independently

5. **Pact** - Demonic pact
   - **File**: `characters/models/demon/pact.py`
   - **Needs**: Admin registration, creation/management views, templates
   - **Template**: Similar to familiar or retainer from other gamelines
   - **Independence**: Depends on DtFHuman having views

6. **Thrall** - Demon servant/thrall
   - **File**: `characters/models/demon/thrall.py`
   - **Needs**: Admin registration, creation/management views, templates
   - **Template**: Similar to `characters/models/vampire/ghoul.py`
   - **Independence**: Depends on DtFHuman having views

7. **DemonFaction** - Demon faction
   - **File**: `characters/models/demon/faction.py`
   - **Needs**: Admin registration, reference data views, populate script
   - **Template**: Similar to `characters/models/werewolf/tribe.py`
   - **Independence**: Standalone - can implement independently

8. **DemonHouse** - Demonic house
   - **File**: `characters/models/demon/house.py`
   - **Needs**: Admin registration, reference data views, populate script
   - **Template**: Similar to `characters/models/changeling/house.py`
   - **Independence**: Standalone - can implement independently

9. **LoreBlock** - Container for character's lores
   - **File**: `characters/models/demon/lore.py`
   - **Needs**: Verify if admin/views needed (likely internal model)
   - **Template**: Similar to `characters/models/core/ability_block.py`
   - **Independence**: Standalone - internal model

10. **LoreRating** - Individual lore rating
    - **File**: `characters/models/demon/lore.py`
    - **Needs**: Verify if admin/views needed (likely internal model)
    - **Template**: Similar to ability ratings
    - **Independence**: Standalone - internal model

11. **ApocalypticFormTrait** - Apocalyptic form special ability
    - **File**: `characters/models/demon/apocalyptic_form.py`
    - **Needs**: Verify if admin/views needed
    - **Template**: Similar to other special abilities
    - **Independence**: Depends on DtFHuman character implementation

### Game App Models - Limited Implementations

**Context**: Models exist and have admin, need better user-facing views/templates

1. **Journal** - Character journal
   - **File**: `game/models.py`
   - **Status**: NOT in admin
   - **Needs**: Admin registration, list/create/update/delete views, templates
   - **Template**: Similar to other game models (Scene, Story)
   - **Independence**: Standalone - can implement independently

2. **JournalEntry** - Individual journal entry
   - **File**: `game/models.py`
   - **Status**: NOT in admin
   - **Needs**: Admin registration, create/edit/delete views, templates
   - **Template**: Similar to Post model
   - **Independence**: Depends on Journal having views

3. **Week** - Weekly time period
   - **Status**: Admin ✅, Views ⚠️, Templates ⚠️
   - **Needs**: Full CRUD views and templates for week management
   - **Template**: Standard Django CRUD pattern
   - **Independence**: Standalone - can implement independently

4. **Post** - Scene post/message
   - **Status**: Admin ✅, Views ⚠️ (embedded in scenes), Templates ⚠️
   - **Needs**: Verify if standalone post management views required
   - **Context**: Currently managed through scene detail views
   - **Independence**: Standalone - verify requirements first

5. **WeeklyXPRequest** - Weekly XP request
   - **Status**: Admin ✅, Views ⚠️ (basic), Templates ⚠️
   - **Needs**: Enhanced views for request creation, approval workflow, templates
   - **Template**: Similar to XPSpendingRequest workflow
   - **Independence**: Standalone - can implement independently

6. **StoryXPRequest** - Story milestone XP request
   - **Status**: Admin ✅, Views ⚠️ (basic), Templates ⚠️
   - **Needs**: Enhanced views for story completion tracking, approval workflow
   - **Template**: Similar to WeeklyXPRequest
   - **Independence**: Standalone - can implement independently

7. **UserSceneReadStatus** - Track scene read status
   - **Status**: Admin ✅, Views ⚠️ (background tracking)
   - **Needs**: Verify views are sufficient for functionality
   - **Context**: Likely internal model, check if user-facing views needed
   - **Independence**: Standalone - verify requirements first

8. **STRelationship** - Storyteller to chronicle relationship
   - **Status**: Admin ✅, Views ⚠️ (admin management), Templates ⚠️
   - **Needs**: User-facing views for ST management
   - **Context**: Currently managed through admin, consider user-facing interface
   - **Independence**: Standalone - can implement independently

9. **ObjectType** - Object type registry
   - **Status**: Admin ✅, Views ⚠️ (internal tracking)
   - **Needs**: Verify views are sufficient for functionality
   - **Context**: Internal tracking model, likely doesn't need user views
   - **Independence**: Standalone - verify requirements first

10. **SettingElement** - Common knowledge/lore
    - **Status**: Admin ✅, Views ⚠️, Templates ⚠️
    - **Needs**: Full implementation for chronicle lore management
    - **Template**: Similar to other game content models
    - **Independence**: Standalone - can implement independently

11. **Gameline** - Gameline definition
    - **Status**: Admin ✅, Views ⚠️ (configuration model)
    - **Needs**: Verify views are sufficient for configuration
    - **Context**: Configuration model, may only need admin interface
    - **Independence**: Standalone - verify requirements first

### Items - Partial Implementations

**Context**: Models have admin, need complete views and templates
**Template**: Follow pattern from completed item implementations

**Vampire Items (2 models)**:
1. **Artifact** (Vampire) - Vampire artifact
   - **File**: `items/models/vampire/artifact.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation (create, detail, update, delete views + templates)
   - **Independence**: Standalone - can implement independently

2. **Bloodstone** - Mystical bloodstone
   - **File**: `items/models/vampire/bloodstone.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation
   - **Independence**: Standalone - can implement independently

**Wraith Items (2 models)**:
3. **WraithRelic** - Wraith relic from life
   - **File**: `items/models/wraith/relic.py`
   - **Status**: Admin ✅, Views ⚠️, Templates ⚠️
   - **Needs**: Complete views and templates (admin exists)
   - **Independence**: Standalone - can implement independently

4. **Artifact** (Wraith) - Wraith artifact
   - **File**: `items/models/wraith/artifact.py`
   - **Status**: Admin ✅, Views ⚠️, Templates ⚠️
   - **Needs**: Complete views and templates (admin exists)
   - **Independence**: Standalone - can implement independently

**Changeling Items (1 model)**:
5. **Treasure** - Changeling treasure
   - **File**: `items/models/changeling/treasure.py`
   - **Status**: Admin ✅, Views ⚠️, Templates ⚠️
   - **Needs**: Complete views and templates (admin exists)
   - **Independence**: Standalone - can implement independently

**Demon Items (1 model)**:
6. **Relic** (Demon) - Demon relic
   - **File**: `items/models/demon/relic.py`
   - **Status**: Admin ✅, Views ⚠️, Templates ⚠️
   - **Needs**: Complete views and templates (admin exists)
   - **Independence**: Standalone - can implement independently

### Locations - Partial Implementations

**Context**: Models exist, need complete admin, views, and templates
**Template**: Follow pattern from completed location implementations (e.g., Node, Caern)

**Vampire Locations (4 models)**:
1. **Domain** - Territory controlled by a vampire
   - **File**: `locations/models/vampire/domain.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation
   - **Independence**: Standalone - can implement independently

2. **Haven** - Vampire's private sanctuary
   - **File**: `locations/models/vampire/haven.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation
   - **Independence**: Standalone - can implement independently

3. **Elysium** - Neutral ground for vampire society
   - **File**: `locations/models/vampire/elysium.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation
   - **Independence**: Standalone - can implement independently

4. **Rack** - Quality hunting grounds
   - **File**: `locations/models/vampire/rack.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation
   - **Independence**: Standalone - can implement independently

**Demon Locations (2 models)**:
5. **Bastion** - Fortified stronghold of the Earthbound
   - **File**: `locations/models/demon/bastion.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation
   - **Independence**: Standalone - can implement independently

6. **Reliquary** - Location that serves as an Earthbound's vessel
   - **File**: `locations/models/demon/reliquary.py`
   - **Status**: Admin ⚠️, Views ⚠️, Templates ⚠️
   - **Needs**: Complete CRUD implementation
   - **Independence**: Standalone - can implement independently

**Changeling Locations**:
7. **Changeling location models** - NOT STARTED
   - **Status**: No location models exist for Changeling gameline
   - **Needs**:
     1. Research Changeling: the Dreaming source material
     2. Define models (consider: Freehold, Trod, Hollow, Dreamscape)
     3. Create models in `locations/models/changeling/`
     4. Implement admin, views, forms, templates, URLs
     5. Create populate scripts for reference data
   - **Context**: Major feature gap - requires research and design
   - **Independence**: Standalone but large scope - should break into subtasks

---

## 🔵 Deployment & Environment

### Permissions System Deployment

**Status**: ✅ **READY FOR STAGING** - Development complete
**Documentation**: `docs/deployment/` - All deployment guides
**Branch**: `claude/deploy-permissions-system-01VmQQEaQuGQX8RgsTfnxLY4`
**Independence**: Deployment tasks are sequential within each phase

#### Staging Phase (PENDING)

1. **Deploy to staging**
   - **Action**:
     - Deploy permissions system to staging environment
     - Run `python test_permissions_deployment.py` (expect 37/37 passing)
     - Performance testing under load
     - Follow `docs/deployment/permissions_staging_checklist.md`
   - **Context**: Follow deployment guide step-by-step
   - **Dependencies**: None - ready to deploy

2. **User acceptance testing**
   - **Action**:
     - Get feedback from real users in staging
     - Test edge cases in production-like environment
     - Verify no usability issues
     - Document any issues found
   - **Context**: Gather user feedback before production deployment
   - **Dependencies**: Requires staging deployment (task #1) to be complete

#### Production Phase (PENDING)

3. **Deploy to production**
   - **Action**:
     - Final deployment of permissions system
     - Monitor error logs closely for first 24 hours
     - Be ready to rollback if issues arise
     - Follow production procedures in deployment guide
   - **Context**: Production deployment after successful staging validation
   - **Dependencies**: Requires successful staging validation (task #2)

### Validation System Deployment

**Status**: ✅ **READY FOR STAGING** - Development complete
**Documentation**: `docs/deployment/` - All deployment guides
**Tools**:
- `core/management/commands/validate_data_integrity.py`
- `core/management/commands/monitor_validation.py`
**Independence**: Deployment tasks are sequential within each phase

#### Staging Phase (PENDING)

1. **Deploy to staging**
   - **Action**:
     - Run `python manage.py validate_data_integrity --fix` to prepare data
     - Apply migrations to add database constraints
     - Test XP spending workflows (player and ST)
     - Test scene XP award workflow
     - Verify constraint violations are caught and handled gracefully
     - Monitor for 1 week (see staging deployment guide)
   - **Context**: Follow staging deployment guide in `docs/deployment/`
   - **Dependencies**: None - ready to deploy

2. **Monitor for validation errors in staging**
   - **Action**:
     - Run `python manage.py monitor_validation` daily
     - Watch logs for CheckConstraint violations
     - Monitor for transaction rollbacks
     - Track performance impact (< 10% degradation target)
     - Collect user feedback from STs and players
   - **Context**: Week-long soak period to identify issues
   - **Dependencies**: Requires staging deployment (task #1) to be complete

#### Production Phase (PENDING)

3. **Deploy to production**
   - **Action**:
     - Complete staging sign-off (1 week soak period)
     - Schedule maintenance window
     - Backup production database
     - Follow production deployment checklist
     - Apply migrations to add constraints
     - Monitor actively for 24 hours
   - **Context**: Production deployment after successful staging validation
   - **Dependencies**: Requires successful staging validation (task #2)

4. **Monitor database constraint violations in production**
   - **Action**:
     - Set up hourly cron job: `python manage.py monitor_validation --json`
     - Configure alerts for health score < 90
     - Log violations for analysis
     - Track metrics: XP success rate, response times, constraint violations
     - Weekly review of validation health reports
   - **Context**: Ongoing monitoring after production deployment
   - **Dependencies**: Requires production deployment (task #3) to be complete

---

## 🎯 Recommended Next Steps

**Start with high-impact, independent tasks:**

1. **Security Quick Wins** (High Priority - Independent) 🔥
   - Fix class name typo (Medium #11) - 5 minutes
   - Add authentication to views (High #3) - 1 hour
   - Update deprecated mixin imports (High #6) - 1-2 hours

2. **Code Quality Cleanup** (High Priority - Independent) 🔥
   - ✅ ~~Eliminate duplicate Limited Edit Forms~~ - COMPLETED
   - Centralize hardcoded choices (Medium #18) - 2-3 hours
   - Move signal registration to apps.py (Medium #6) - 30 minutes

3. **Development Tools** (Medium Priority - Independent) 🔥
   - Add Django Debug Toolbar (Medium #15) - 30 minutes
   - Configure structured logging (Medium #16) - 1 hour
   - Add caching configuration (Medium #17) - 1 hour

4. **Testing & Validation** (Medium Priority - Independent)
   - Add tests for Character model (Medium #13) - 3-4 hours
   - Add model validation for Character status (Medium #10) - 2-3 hours

5. **Deployment** (High Priority - Sequential) 🔥
   - Deploy Permissions System to staging (Deployment #1)
   - Deploy Validation System to staging (Deployment #1)
   - Monitor and validate in staging
   - Deploy to production after sign-off

6. **Performance Improvements** (Medium Priority - Independent)
   - Fix N+1 query problems (Medium #1) - requires Debug Toolbar
   - Add database indexes (Medium #2) - 1-2 hours

---

## 📚 Long-term Improvements

**Context**: Strategic improvements for future consideration

1. **Add migration best practices**
   - **Action**:
     - Create data migrations for schema changes
     - Periodically squash old migrations: `python manage.py squashmigrations`
     - Test migrations in CI/CD pipeline
   - **Context**: Keeps migration history manageable
   - **Independence**: Ongoing practice, not a one-time task

2. **Improve code style consistency**
   - **Issues**:
     - `accounts/models.py:116` - `str` variable shadows built-in
     - Missing docstrings on complex methods
     - Inconsistent formatting
   - **Action**:
     - Install and configure black: `pip install black`
     - Install ruff for linting: `pip install ruff`
     - Consider mypy for type checking: `pip install mypy`
     - Run formatters in pre-commit hook
   - **Context**: Automated formatting ensures consistency
   - **Independence**: Standalone - can implement incrementally

---

## 📊 Summary Statistics

**Total Open Items**: ~54 items across all priorities

**By Priority**:
- 🔴 High Priority: 6 items (security + critical code quality)
- 🟡 Medium Priority: 25 items (performance + architecture + testing + tools)
- 🟢 Low Priority: ~50 items (feature completeness + polish)
- 🔵 Deployment: 7 items (staging + production deployments)

**By Independence**:
- ✅ Fully Independent: ~39 items (can be done immediately)
- ⚠️ Minor Dependencies: ~10 items (depends on 1-2 other tasks)
- 🔗 Complex Dependencies: ~5 items (large refactors requiring planning)

**Estimated Effort** (for independent tasks):
- High Priority Quick Wins: 3.5-7.5 hours
- Medium Priority Tools & Testing: 8-16 hours
- Performance Improvements: 4-8 hours
- Code Quality Cleanup: 4-8 hours

---

**Last Updated**: 2025-11-23
**Version**: 5.1 (Removed completed 404 error handling task)
