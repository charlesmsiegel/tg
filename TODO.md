# TODO List

This document tracks remaining work across the codebase with context about what needs to be done.

**Legend:**
- ✅ Completed items have been **deleted** from this list
- ⚠️ Partially completed - shows what's done and what remains
- ❌ Not started - detailed description of what needs to be done
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

8. **✅ Simplify Custom QuerySet Initialization** - COMPLETED
   - **Files**: `core/models.py`, `characters/models/core/character.py`, `items/models/core/item.py`, `locations/models/core/location.py`
   - **Impact**: MEDIUM - Fragile internal query manipulation
   - **Status**: ✅ **COMPLETED** - Refactored to use Django's standard manager pattern
   - **Changes Made**:
     1. Removed fragile `ModelQuerySet.__init__()` that manipulated `query.select_related` directly
     2. Converted `ModelManager` from simple assignment to proper class with `get_queryset()` override
     3. Updated CharacterManager, ItemModelManager, and LocationModelManager to inherit from ModelManager
     4. Uses Django's standard `select_related('polymorphic_ctype')` in manager's `get_queryset()`
   - **Context**: Now uses Django best practices instead of internal query manipulation
   - **Independence**: Standalone task - completed independently

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

### Location Model Improvements

30. **Replace Location `parent` ForeignKey with `contained_within` ManyToMany**
    - **File**: `locations/models/core/location.py`
    - **Impact**: MEDIUM - Current single-parent model can't represent overlapping regions
    - **Issue**: Locations can only have one parent, but physical spaces often exist within multiple conceptual containers:
      - Pike Place Market Node is geographically in Pike Place Market, but organizationally managed by Traditions
      - Underground Seattle contains Vampire Elysium, Wraith Necropolis, and Changeling Trod simultaneously
      - Puget Sound hosts Mage Node, Wraith Nihil, Demon Earthbound, and Werewolf Umbral location
    - **Current State**: `parent = models.ForeignKey("LocationModel", ...)` - single parent only
    - **Action**:
      1. Add new field: `contained_within = models.ManyToManyField("LocationModel", blank=True, related_name="contains")`
      2. Create data migration to copy existing `parent` relationships to `contained_within`
      3. Update views and templates to use `contained_within` instead of `parent`
      4. Update `top_level()` queryset method to filter on `contained_within__isnull=True` or empty
      5. Consider keeping `parent` temporarily for backwards compatibility, then deprecate
      6. Update all location population scripts to use new field
    - **Benefits**:
      - Geographic containment: Pike Place Node → Pike Place Market region
      - Overlapping territories: Ghost Market → Pike Place + Underground Seattle
      - Cross-gameline shared spaces: Puget Sound → multiple supernatural sites
    - **Context**: Enables proper representation of how supernatural locations relate to physical geography
    - **Independence**: Medium complexity - requires migration and view updates

31. **Support Multiple Identities for Single Physical Spaces**
    - **Files**: `locations/models/core/location.py`, possibly new model
    - **Impact**: MEDIUM - Same physical location can have different supernatural identities
    - **Issue**: A single physical location may be multiple things simultaneously:
      - Seattle is a City (mundane), a Duchy/Holding (Changeling), contains Domains (Vampire), etc.
      - Pike Place Market is a mundane location, a Node (Mage), part of a Freehold (Changeling), a Rack (Vampire)
      - A church might be an Elysium (Vampire), a Haunt (Wraith), and a Web of Faith node (Mummy)
    - **Current State**: Each gameline creates separate location objects with no explicit link
    - **Options**:
      - **Option A**: Add `physical_location` ForeignKey to a new `PhysicalPlace` model that all gameline locations reference
      - **Option B**: Add `same_location_as` ManyToMany self-referential field to link equivalent locations
      - **Option C**: Add `mundane_counterpart` ForeignKey to base LocationModel pointing to a "mundane" location
    - **Action** (Option A - Recommended):
      1. Create new `PhysicalPlace` model with mundane attributes (address, coordinates, description)
      2. Add `physical_place = models.ForeignKey(PhysicalPlace, null=True, blank=True, ...)` to LocationModel
      3. Multiple supernatural locations can reference same PhysicalPlace
      4. Create views to show "all supernatural aspects of this place"
      5. Update templates to display linked locations
    - **Benefits**:
      - Query all supernatural activity at a physical location
      - Show players "what's really happening at Pike Place Market" across gamelines
      - Enable cross-gameline plot hooks and shared spaces
    - **Context**: Reflects WoD setting where multiple supernatural groups often share or contest the same physical spaces
    - **Independence**: Can be implemented after or alongside TODO #30

### Character Group Model Consistency

24. **Rename Demon Group Model from Conclave to Court**
    - **File**: `characters/models/demon/conclave.py`
    - **Impact**: MEDIUM - Model name doesn't match World of Darkness terminology
    - **Issue**: The Demon group model is named `Conclave` but WoD terminology uses "Court" for demon groups
    - **Current State**: `Conclave` model exists and works, but naming is inconsistent with source material
    - **Action**:
      1. Create new model `Court` in `characters/models/demon/court.py`:
         ```python
         class Court(Group):
             type = "court"
             gameline = "dtf"

             def get_heading(self):
                 return "dtf_heading"
         ```
      2. Create data migration to rename table and migrate existing data:
         ```python
         # migrations/XXXX_rename_conclave_to_court.py
         from django.db import migrations

         def migrate_conclaves_to_courts(apps, schema_editor):
             Conclave = apps.get_model('characters', 'Conclave')
             Court = apps.get_model('characters', 'Court')
             for conclave in Conclave.objects.all():
                 Court.objects.create(
                     name=conclave.name,
                     description=conclave.description,
                     # ... copy all fields
                 )
         ```
      3. Update all imports: `from characters.models.demon import Court` (was Conclave)
      4. Update URLs: `characters:demon:create:court`, `characters:demon:update:court`
      5. Update templates referencing "conclave" to "court"
      6. Update admin registration
      7. Remove old `Conclave` model after migration verified
    - **Files to Update**:
      - `characters/models/demon/__init__.py`
      - `characters/models/demon/conclave.py` → `court.py`
      - `characters/admin.py` (demon section)
      - `characters/urls/demon/` (create and update URLs)
      - `characters/views/demon/` (any conclave views)
      - `characters/templates/characters/demon/` (conclave templates)
      - `populate_db/chronicle/test/groups.py`
    - **Context**: Consistency with WoD source material improves usability for players familiar with the game
    - **Independence**: Standalone - can be done independently but requires careful migration

25. **Create Cell Model as Group Subclass for Hunter**
    - **File**: `characters/models/hunter/organization.py`
    - **Impact**: MEDIUM - Hunter uses different pattern than other gamelines
    - **Issue**: Hunter groups use `HunterOrganization` model which:
      - Does NOT inherit from `Group` base class
      - Has different fields (`philosophy`, `goals`, `organization_type`, `resources`)
      - Uses `Hunter` foreign key instead of generic `Character`
      - Lacks integration with Group-based features (pooled backgrounds, etc.)
    - **Current State**: `HunterOrganization` works but is architecturally inconsistent
    - **Options**:
      - **Option A**: Create `Cell` as Group subclass, keep `HunterOrganization` for larger structures
      - **Option B**: Refactor `HunterOrganization` to inherit from `Group`
      - **Option C**: Keep current design, document as intentional difference
    - **Action** (Option A - Recommended):
      1. Create new model `Cell` in `characters/models/hunter/cell.py`:
         ```python
         class Cell(Group):
             type = "cell"
             gameline = "htr"

             # Hunter-specific fields
             philosophy = models.TextField(blank=True)
             goals = models.TextField(blank=True)

             def get_heading(self):
                 return "htr_heading"
         ```
      2. Keep `HunterOrganization` for compacts/conspiracies (larger structures)
      3. Update populate scripts to use `Cell` for small groups
      4. Create views and templates for Cell model
      5. Add URLs following standard Group pattern
    - **Files to Create/Update**:
      - `characters/models/hunter/cell.py` (new)
      - `characters/models/hunter/__init__.py`
      - `characters/admin.py` (hunter section)
      - `characters/urls/hunter/` (add cell URLs)
      - `characters/views/hunter/` (add cell views)
      - `characters/templates/characters/hunter/cell/` (new templates)
      - `populate_db/chronicle/test/groups.py`
    - **Context**: Architectural consistency across gamelines simplifies maintenance and user expectations
    - **Independence**: Standalone - can be done independently

26. **Create Cult Model for Mummy Groups**
    - **File**: `characters/models/mummy/` (no group model exists)
    - **Impact**: MEDIUM - Mummy gameline lacks group functionality
    - **Issue**: Mummy has no group model at all; currently using generic `Group` as workaround
    - **Current State**: Test chronicle uses `Group` objects for mummy "cults" which:
      - Lacks mummy-specific styling (no `get_heading()` returning `mtr_heading`)
      - Shows as generic "Group" instead of "Cult" in UI
      - Can't have mummy-specific fields if needed later
    - **Action**:
      1. Create new model `Cult` in `characters/models/mummy/cult.py`:
         ```python
         from characters.models.core import Group

         class Cult(Group):
             type = "cult"
             gameline = "mtr"

             def get_heading(self):
                 return "mtr_heading"

             @classmethod
             def get_creation_url(cls):
                 return reverse("characters:mummy:create:cult")

             def get_update_url(self):
                 return reverse("characters:mummy:update:cult", kwargs={"pk": self.pk})
         ```
      2. Register in admin
      3. Create URLs following standard Group pattern:
         - `characters:mummy:create:cult`
         - `characters:mummy:update:cult`
      4. Create views (can copy from other Group subclasses like Coterie)
      5. Create templates in `characters/templates/characters/mummy/cult/`
      6. Update `populate_db/chronicle/test/groups.py` to use `Cult` instead of `Group`
      7. Migrate existing test data from `Group` to `Cult`
    - **Files to Create**:
      - `characters/models/mummy/cult.py` (new)
      - `characters/models/mummy/__init__.py` (update exports)
      - `characters/urls/mummy/create.py` (add cult URL)
      - `characters/urls/mummy/update.py` (add cult URL)
      - `characters/views/mummy/cult.py` (new)
      - `characters/templates/characters/mummy/cult/` (new directory)
        - `detail.html`
        - `form.html`
    - **Context**: Completes mummy gameline's group functionality, matching other gamelines
    - **Independence**: Standalone - can be done independently

### Demon & Servant Character Relationships

27. **Demon Characters Should Identify by Host Name**
    - **Files**: `characters/models/demon/demon.py`, templates, views
    - **Impact**: MEDIUM - Confusing display for users
    - **Issue**: Demon characters have separate `name` (celestial name) and `host_name` fields, but should primarily identify by their host name since that's the mortal identity they use
    - **Current State**: Name field is treated as primary identifier in lists, detail views, etc.
    - **Action**:
      1. Update display logic to show host_name as primary identifier
      2. Consider making host_name the `name` field and celestial_name a separate field
      3. Update `__str__` method to return host_name
      4. Update templates and admin to display appropriately
    - **Context**: In Demon: The Fallen, the host is the primary identity; celestial name is secret/formal
    - **Independence**: Standalone - can be done independently

28. **Thrall.master Should Be ForeignKey to Demon**
    - **File**: `characters/models/demon/thrall.py`
    - **Impact**: MEDIUM - Currently stores string name, not proper relationship
    - **Issue**: Thrall's `master` field should be a ForeignKey to Demon model for proper relational integrity
    - **Current State**: Thralls reference masters by name string (in test data) or unclear relationship
    - **Action**:
      1. Add/verify ForeignKey field: `master = models.ForeignKey('Demon', ...)`
      2. Create migration if field type needs to change
      3. Update forms to use ModelChoiceField for master selection
      4. **Important**: During character creation, allow creating a NEW Demon NPC as master (not just selecting existing characters) - integrate with standard NPC creation workflow
      5. Update admin to show proper relationship
    - **Context**: Proper ForeignKey enables cascade delete, reverse lookups, and data integrity
    - **Independence**: Standalone - can be done independently

29. **Ghoul.domitor Should Be ForeignKey to Vampire**
    - **File**: `characters/models/vampire/ghoul.py`
    - **Impact**: MEDIUM - Currently stores string name, not proper relationship
    - **Issue**: Ghoul's domitor should be a ForeignKey to Vampire model for proper relational integrity
    - **Current State**: Ghouls reference domitors by name string (in test data) or unclear relationship
    - **Action**:
      1. Add/verify ForeignKey field: `domitor = models.ForeignKey('Vampire', ...)`
      2. Create migration if field type needs to change
      3. Update forms to use ModelChoiceField for domitor selection
      4. **Important**: During character creation, allow creating a NEW Vampire NPC as domitor (not just selecting existing characters) - integrate with standard NPC creation workflow
      5. Update admin to show proper relationship
      6. Consider allowing null domitor for independent/abandoned ghouls
    - **Context**: Proper ForeignKey enables cascade delete, reverse lookups, and data integrity
    - **Independence**: Standalone - can be done independently

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

23. **Remove Unnecessary ApprovedUserContextMixin** ✅ COMPLETED
    - **Status**: Completed - ApprovedUserContextMixin has been removed
    - **Changes Made**:
      1. Added `is_approved_user=True` flag directly to `PermissionRequiredMixin.get_context_data()` in `core/mixins.py:53-58`
      2. Removed `ApprovedUserContextMixin` from all 27 view files in `characters/views/`
      3. Removed `ApprovedUserContextMixin` imports from all affected files
      4. Deleted `ApprovedUserContextMixin` class definition from `core/mixins.py`
    - **Result**: All views using permission mixins now automatically get `is_approved_user=True` in their context without needing a separate mixin

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

✅ **Status**: Full CRUD implementation complete

**What's done:**
- Hunter and HtRHuman character views (detail, create, update, list)
- Creed, Edge, HunterOrganization reference data views (detail, create, update, list)
- HunterGear, HunterRelic item views (detail, create, update, list)
- Safehouse, HuntingGround location views (detail, create, update, list)
- All templates for character, item, and location types
- URL patterns for all Hunter routes
- Limited edit forms for owner editing

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

**Total Open Items**: ~7 items

**By Priority**:
- 🟢 Low Priority: ~1 item (feature completeness - Mummy gameline)
- 🔵 Deployment: 6 items (staging + production)

---

## ✅ Recently Completed (removed from list)

The following items were verified as complete and removed:

### Removed 2025-11-25 (v7.8)
- **Hunter Gameline Implementation** - Full CRUD for Hunter, HtRHuman, Creed, Edge, HunterOrganization, HunterGear, HunterRelic, Safehouse, HuntingGround. Views, URL patterns, templates, and limited edit forms all implemented.

### Removed 2025-11-25 (v7.7)
- **WeeklyXPRequest batch approval** - Added `WeeklyXPRequestBatchApproveView` for STs to approve multiple XP requests at once. Updated week detail template with checkbox selection, "Select All" functionality, and batch approve button with live count display.

### Removed 2025-11-25 (v7.6)
- **Journal/JournalEntry enhancements** - Enhanced JournalListView with pagination, filtering (all/mine/ST chronicles), entry counts, and latest entry dates. Improved detail template with better form layout, help text, placeholders, entry timestamps, and navigation links. Added `get_item` and `add_attr` template filters.

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
**Version**: 7.8 (Added full Hunter gameline CRUD implementation)
**Total Open Items**: ~57 items across all priorities
**Total Open Items**: ~59 items across all priorities

**By Priority**:
- 🔴 High Priority: 6 items (security + critical code quality)
- 🟡 Medium Priority: 30 items (performance + architecture + testing + tools + group models + location improvements)
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

**Last Updated**: 2025-11-25
**Version**: 5.2 (Added character group model consistency issues #24-26)
