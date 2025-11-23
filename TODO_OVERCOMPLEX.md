# Over-Engineered Solutions - Refactoring TODO

This document tracks over-engineered solutions in the codebase that should be simplified. Each item includes context, the problem, and concrete steps to resolve it.

---

## 🔴 High Priority - Significant Complexity Reduction

### 1. Duplicate QuerySet and Manager Methods

**Impact**: HIGH - 70+ lines of duplicate code, maintenance burden

**Location**: `core/models.py:16-107`

**Problem**:
`ModelQuerySet` and `ModelManager` contain identical method implementations. Every method appears twice:
- `pending_approval_for_user()`
- `visible()`
- `for_chronicle()`
- `owned_by()`
- `with_pending_images()`
- `for_user_chronicles()`

Django's `PolymorphicManager.from_queryset()` pattern automatically exposes QuerySet methods on the Manager, making the Manager duplicates unnecessary.

**Resolution Steps**:
1. ✅ Verify all methods work correctly when called from QuerySet
2. Delete all method implementations from `ModelManager` (lines 74-106)
3. Replace `ModelManager` class with:
   ```python
   ModelManager = PolymorphicManager.from_queryset(ModelQuerySet)
   ```
4. Run tests to ensure no breakage: `python manage.py test`
5. Search codebase for any direct `ModelManager` method calls and verify they still work

**Testing**:
```bash
python manage.py test core
python manage.py test characters
```

**References**:
- Django docs: https://docs.djangoproject.com/en/5.1/topics/db/managers/#from-queryset
- Pattern already used correctly in `CharacterManager` (line 88)

---

### 2. Dual XP Tracking Systems

**Impact**: HIGH - Two parallel systems creating maintenance burden and confusion

**Location**: `characters/models/core/character.py:116-530`

**Problem**:
Character maintains TWO complete XP tracking implementations:

**Old JSONField System** (deprecated but still active):
- `spent_xp = models.JSONField(default=list)` (line 117)
- Methods: `add_to_spend()`, `spend_xp()`, `approve_xp_spend()`, `waiting_for_xp_spend()`

**New Model-Based System**:
- `XPSpendingRequest` model with proper relations
- Methods: `create_xp_spending_request()`, `get_pending_xp_requests()`, `approve_xp_request()`, `deny_xp_request()`

**Compatibility Layer** (should be temporary):
- `has_pending_xp_or_model_requests()` - checks BOTH systems
- `total_spent_xp_combined()` - aggregates across BOTH systems

Comment on line 116 says "DEPRECATED: Use XPSpendingRequest model instead" but system is still fully functional.

**Resolution Steps**:
1. ✅ Audit codebase for all uses of old JSONField system:
   ```bash
   grep -r "spent_xp" --include="*.py" --include="*.html"
   grep -r "add_to_spend\|waiting_for_xp_spend" --include="*.py"
   ```
2. Create data migration to convert existing JSONField data to XPSpendingRequest records:
   ```python
   # Migration pseudocode:
   for char in Character.objects.exclude(spent_xp=[]):
       for record in char.spent_xp:
           XPSpendingRequest.objects.create(
               character=char,
               trait_name=record['trait'],
               cost=record['cost'],
               approved=record['approved'],
               # ... map other fields
           )
   ```
3. Update all views using old system (search for `add_to_spend`, `waiting_for_xp_spend`)
4. Update all templates displaying `spent_xp` JSONField
5. Remove old methods from Character model (lines 294-374)
6. Remove `spent_xp` field (keep in migration, add to model with `deprecated=True` first)
7. Remove compatibility methods (lines 491-530)
8. Update documentation in `JSONFIELD_MIGRATION_GUIDE.md`

**Testing**:
```bash
python manage.py test characters.tests --pattern="*xp*"
python manage.py test game.tests --pattern="*xp*"
```

**Migration File Template**:
```python
# characters/migrations/XXXX_migrate_xp_to_model.py
from django.db import migrations

def migrate_jsonfield_to_model(apps, schema_editor):
    Character = apps.get_model('characters', 'Character')
    XPSpendingRequest = apps.get_model('game', 'XPSpendingRequest')

    for char in Character.objects.exclude(spent_xp=[]):
        for idx, record in enumerate(char.spent_xp):
            XPSpendingRequest.objects.create(
                character=char,
                trait_name=record.get('trait', 'Unknown'),
                trait_type=record.get('category', 'other'),
                trait_value=record.get('value', ''),
                cost=record.get('cost', 0),
                approved=record.get('approved', 'Pending'),
                created_at=record.get('timestamp', timezone.now()),
            )

class Migration(migrations.Migration):
    dependencies = [
        ('characters', 'PREVIOUS_MIGRATION'),
        ('game', 'xp_spending_request_migration'),
    ]

    operations = [
        migrations.RunPython(migrate_jsonfield_to_model),
    ]
```

**References**:
- See `JSONFIELD_MIGRATION_GUIDE.md` for context
- Related TODO in main TODO.md under "Code Architecture"

---

## 🟡 Medium Priority - Architectural Simplification

### 3. Wrapper Methods in PermissionMixin

**Impact**: MEDIUM - Unnecessary indirection, confusing API

**Location**: `core/models.py:219-253`

**Problem**:
`PermissionMixin` has 6 methods that are thin wrappers around `PermissionManager` static methods:
- `get_user_roles(user)` → `PermissionManager.get_user_roles(user, self)`
- `user_can_view(user)` → `PermissionManager.user_can_view(user, self)`
- `user_can_edit(user)` → `PermissionManager.user_can_edit(user, self)`
- `user_can_spend_xp(user)` → `PermissionManager.user_can_spend_xp(user, self)`
- `user_can_spend_freebies(user)` → `PermissionManager.user_can_spend_freebies(user, self)`
- `get_visibility_tier(user)` → `PermissionManager.get_visibility_tier(user, self)`

These add no logic, just change `PermissionManager.method(user, obj)` to `obj.method(user)`.

**Resolution Steps**:
1. ✅ Search for all uses of these wrapper methods:
   ```bash
   grep -r "\.user_can_view\|\.user_can_edit\|\.get_user_roles" --include="*.py" --include="*.html"
   ```
2. Decide: Keep object-oriented API or use PermissionManager directly?

   **Option A (Recommended)**: Remove wrappers, use PermissionManager everywhere
   - More explicit and clear where permission logic lives
   - Consistent with existing code (PermissionManager already used directly in many places)

   **Option B**: Keep wrappers but make them more useful
   - Add caching/memoization to avoid repeated permission checks
   - Add logging/debugging capabilities

3. If choosing Option A:
   - Replace all `obj.user_can_view(user)` with `PermissionManager.user_can_view(user, obj)`
   - Replace all `obj.user_can_edit(user)` with `PermissionManager.user_can_edit(user, obj)`
   - Remove methods from PermissionMixin (lines 219-253)
   - Keep `add_observer()` and `remove_observer()` (lines 255-263) - these actually do something

4. Update templates using these methods (search for in templates)

**Testing**:
```bash
python manage.py test core.tests
python manage.py test characters.tests
```

**Decision Point**: Discuss with team whether OO API (`obj.user_can_view(user)`) or procedural API (`PermissionManager.user_can_view(user, obj)`) is preferred.

---

### 4. Custom QuerySet Initialization Complexity

**Impact**: MEDIUM - Fragile internal query manipulation

**Location**: `core/models.py:25-34`

**Problem**:
`ModelQuerySet.__init__()` manually manipulates internal `query.select_related` dictionary:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._result_cache = None  # Redundant - parent already does this
    # Manually set up select_related for polymorphic_ctype
    if self.query.select_related is False:
        self.query.select_related = {}
    if "polymorphic_ctype" not in self.query.select_related:
        self.query.select_related["polymorphic_ctype"] = {}
```

This manipulates Django's internal query structure, which is fragile and can break with Django updates.

**Resolution Steps**:
1. ✅ Test if polymorphic library already handles this optimization
2. Check django-polymorphic documentation for recommended patterns
3. **Option A**: Remove entirely and rely on polymorphic library
   - Delete the custom `__init__` method
   - Run performance tests to verify no N+1 queries appear

4. **Option B**: Use cleaner override pattern:
   ```python
   def _clone(self):
       clone = super()._clone()
       # Apply optimization only if not already present
       if 'polymorphic_ctype' not in clone.query.select_related:
           clone = clone.select_related('polymorphic_ctype')
       return clone
   ```

5. **Option C**: Add a manager method instead:
   ```python
   # In ModelManager/ModelQuerySet
   def with_polymorphic_optimization(self):
       """Apply polymorphic ContentType optimization to prevent N+1 queries."""
       return self.select_related('polymorphic_ctype')
   ```
   Then call explicitly where needed: `Character.objects.with_polymorphic_optimization()`

6. Remove `self._result_cache = None` line (redundant)

**Testing**:
```bash
# Install django-debug-toolbar if not already
pip install django-debug-toolbar

# Run with query logging
python manage.py test --debug-mode
# Check for N+1 queries when accessing polymorphic types
```

**References**:
- django-polymorphic docs: https://django-polymorphic.readthedocs.io/
- Check if library version has built-in optimization

---

### 5. Complex filter_queryset_for_user Implementation

**Impact**: MEDIUM - Hard to maintain, performance concerns

**Location**: `core/permissions.py:310-381`

**Problem**:
The permission filter uses broad exception handling and complex subqueries:

```python
# Checking for field existence with broad exceptions
try:
    queryset.model._meta.get_field("owner")
    filters |= Q(owner=user)
except Exception:  # Too broad!
    pass

# Complex subquery for player chronicles
from characters.models import Character
player_chronicle_subquery = Character.objects.filter(
    user=user, chronicle=OuterRef("chronicle"), status="App"
)
filters |= Q(Exists(player_chronicle_subquery), status="App")
```

**Resolution Steps**:
1. Replace broad `except Exception` with proper field checking:
   ```python
   # Instead of try/except
   if hasattr(queryset.model, 'owner'):
       filters |= Q(owner=user)

   # Or use model meta properly
   opts = queryset.model._meta
   if 'owner' in [f.name for f in opts.get_fields()]:
       filters |= Q(owner=user)
   ```

2. Consider caching chronicle membership:
   ```python
   # Cache user's chronicle IDs to avoid repeated queries
   user_chronicle_ids = list(user.chronicle_set.values_list('id', flat=True))

   # Then use simple filter
   if hasattr(queryset.model, 'chronicle'):
       filters |= Q(chronicle_id__in=user_chronicle_ids)
   ```

3. Profile the subquery approach vs. simpler filtering:
   ```python
   # Current complex approach
   player_chronicle_subquery = Character.objects.filter(...)
   filters |= Q(Exists(player_chronicle_subquery), status="App")

   # Simpler alternative (may be faster)
   player_chronicle_ids = Character.objects.filter(
       owner=user, status="App"
   ).values_list('chronicle_id', flat=True)
   filters |= Q(chronicle_id__in=player_chronicle_ids, status="App")
   ```

4. Add query logging to measure actual performance impact

5. Consider breaking into smaller, testable methods:
   ```python
   @staticmethod
   def _get_owner_filter(user, queryset):
       """Get Q filter for objects user owns."""
       if hasattr(queryset.model, 'owner'):
           return Q(owner=user)
       return Q()

   @staticmethod
   def _get_chronicle_st_filter(user, queryset):
       """Get Q filter for chronicles where user is ST."""
       # ...implementation

   @staticmethod
   def filter_queryset_for_user(user, queryset):
       filters = (
           PermissionManager._get_owner_filter(user, queryset) |
           PermissionManager._get_chronicle_st_filter(user, queryset) |
           # ... other filters
       )
       return queryset.filter(filters).distinct()
   ```

**Testing**:
```bash
# Performance testing
python manage.py shell
from django.test.utils import override_settings
from django.db import connection
from django.test import TestCase

# Compare query counts for both approaches
```

---

### 6. remove_from_organizations() Complexity

**Impact**: MEDIUM - Tight coupling, hard to extend

**Location**: `characters/models/core/character.py:206-258`

**Problem**:
Method has 9 different `hasattr()` checks for different organizational structures. The Character model needs intimate knowledge of Group, Chantry, and all their reverse relations.

```python
def remove_from_organizations(self):
    # Groups
    for group in Group.objects.filter(members=self):
        group.members.remove(self)
    for group in Group.objects.filter(leader=self):
        group.leader = None
        group.save()

    # Chantries (only for Humans)
    if hasattr(self, "member_of"):
        for chantry in self.member_of.all():
            chantry.members.remove(self)

    if hasattr(self, "chantry_leader_at"):
        # ... more checks

    # 7 more hasattr checks for different roles
```

**Resolution Steps**:
1. **Refactor using Django signals** (Recommended):
   ```python
   # characters/signals.py
   from django.db.models.signals import pre_save
   from django.dispatch import receiver
   from characters.models import Character

   @receiver(pre_save, sender=Character)
   def handle_character_retirement(sender, instance, **kwargs):
       """Remove retired/deceased characters from organizations."""
       if not instance.pk:
           return  # New character, nothing to do

       try:
           old = Character.objects.get(pk=instance.pk)
       except Character.DoesNotExist:
           return

       # Check if status changed to Ret or Dec
       if old.status not in ['Ret', 'Dec'] and instance.status in ['Ret', 'Dec']:
           # Trigger cleanup
           instance._needs_org_cleanup = True

   # Then in Character.save():
   def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       if getattr(self, '_needs_org_cleanup', False):
           # Let related models handle their own cleanup
           from characters.signals import cleanup_organizations
           cleanup_organizations.send(sender=self.__class__, instance=self)
   ```

2. **Let each related model handle its own cleanup**:
   ```python
   # characters/models/core/group.py
   from django.db.models.signals import m2m_changed

   @receiver(cleanup_organizations, sender=Character)
   def remove_from_groups(sender, instance, **kwargs):
       """Remove character from groups when retired/deceased."""
       Group.objects.filter(members=instance).update(members__remove=instance)
       Group.objects.filter(leader=instance).update(leader=None)

   # characters/models/mage/chantry.py
   @receiver(cleanup_organizations, sender=Character)
   def remove_from_chantries(sender, instance, **kwargs):
       """Remove character from chantries when retired/deceased."""
       if hasattr(instance, 'member_of'):
           for chantry in instance.member_of.all():
               chantry.members.remove(instance)
       # ... handle other roles
   ```

3. **Or use a registry pattern**:
   ```python
   # core/organizations.py
   class OrganizationRegistry:
       _cleanup_handlers = []

       @classmethod
       def register_cleanup(cls, handler):
           cls._cleanup_handlers.append(handler)

       @classmethod
       def cleanup_character(cls, character):
           for handler in cls._cleanup_handlers:
               handler(character)

   # In each organizational model
   def cleanup_group_memberships(character):
       Group.objects.filter(members=character).update(...)

   OrganizationRegistry.register_cleanup(cleanup_group_memberships)
   ```

4. Remove the monolithic `remove_from_organizations()` method
5. Update Character.save() to use new signal-based approach

**Testing**:
```bash
python manage.py test characters.tests.test_character_retirement
# Create comprehensive tests for all org types
```

**Benefits**:
- Each model manages its own cleanup (Single Responsibility)
- Easy to add new organizational types
- Character model doesn't need to know about all organizations
- More testable (can test each org type independently)

---

## 🟢 Low Priority - Code Quality Improvements

### 7. Gameline Detection via String Parsing

**Impact**: LOW - Fragile but rarely breaks, mostly aesthetic issue

**Location**: `core/models.py:352-372`

**Problem**:
Models detect gameline by parsing class module path strings:

```python
def get_gameline(self):
    s = str(self.__class__).split(" ")[-1].split(".")[2]
    if s == "core":
        return "World of Darkness"
    return str(self.__class__).split(" ")[-1].split(".")[2].title()

def get_full_gameline(self):
    short = self.get_gameline()
    if short == "World of Darkness":
        return short
    elif short == "Vampire":
        return "Vampire: the Masquerade"
    elif short == "Werewolf":
        return "Werewolf: the Apocalypse"
    # ... more hardcoded mappings
```

**Resolution Steps**:
1. Each model already has or should have a `gameline` class attribute:
   ```python
   class Character(CharacterModel):
       gameline = "wod"  # Already exists!

   class Vampire(Character):
       gameline = "vtm"

   class Mage(Character):
       gameline = "mta"
   ```

2. Replace `get_gameline()` with simple attribute access:
   ```python
   def get_gameline(self):
       """Get gameline short code (e.g., 'vtm', 'wta')."""
       return getattr(self, 'gameline', 'wod')
   ```

3. Replace `get_full_gameline()` with settings lookup:
   ```python
   def get_full_gameline(self):
       """Get full gameline name (e.g., 'Vampire: the Masquerade')."""
       from django.conf import settings
       from core.utils import get_gameline_name
       return get_gameline_name(self.get_gameline())
   ```

   Note: `get_gameline_name()` already exists in `core/utils.py:75-87`!

4. Search codebase for any code relying on the string parsing behavior
5. Update all subclasses to ensure they have `gameline` attribute set
6. Remove the complex string parsing logic

**Testing**:
```bash
python manage.py test characters
python manage.py test items
python manage.py test locations
```

**Files to Update**:
- Ensure all Character subclasses have `gameline` attribute
- Ensure all ItemModel subclasses have `gameline` attribute
- Ensure all LocationModel subclasses have `gameline` attribute

---

### 8. Observer Permission Check with ContentType

**Impact**: LOW - Works but could be cleaner

**Location**: `core/permissions.py:156-164`

**Problem**:
Checking observer status requires ContentType lookup:

```python
if hasattr(obj, "observers"):
    ct = ContentType.objects.get_for_model(obj)
    from core.models import Observer
    if Observer.objects.filter(
        content_type=ct, object_id=obj.id, user=user
    ).exists():
        roles.add(Role.OBSERVER)
```

**Resolution Steps**:
1. Use the GenericRelation directly (already defined in PermissionMixin):
   ```python
   # Current complex approach
   ct = ContentType.objects.get_for_model(obj)
   if Observer.objects.filter(content_type=ct, object_id=obj.id, user=user).exists():
       roles.add(Role.OBSERVER)

   # Simpler approach using reverse relation
   if hasattr(obj, "observers") and obj.observers.filter(user=user).exists():
       roles.add(Role.OBSERVER)
   ```

2. Update the code in `core/permissions.py:156-164`

3. Test that it still works correctly

**Testing**:
```bash
python manage.py test core.tests.test_permissions
```

**Performance Note**: Both approaches likely have similar performance (GenericRelation uses ContentType under the hood), but the second is more idiomatic Django.

---

### 9. Status Validation Redundancy

**Impact**: LOW - Confusing but functional

**Location**: `characters/models/core/character.py:122-188`

**Problem**:
Status validation happens in three places with contradictory behavior:

1. **Database constraint** (lines 122-131): Attempted but can't reference parent field
2. **clean() method** (lines 142-178): Validates status transitions
3. **save() method** (lines 180-188): Calls validation but ignores errors!

```python
def save(self, *args, **kwargs):
    if not kwargs.pop("skip_validation", False):
        try:
            self.full_clean()
        except ValidationError:
            # Allow save to proceed if validation fails (!)
            pass
    # ...
```

**Resolution Steps**:
1. **Decide on validation strategy**:

   **Option A (Strict)**: Enforce validation, raise errors
   ```python
   def save(self, *args, **kwargs):
       # Always validate unless explicitly skipped
       if not kwargs.pop("skip_validation", False):
           self.full_clean()  # Let ValidationError propagate
       super().save(*args, **kwargs)
   ```

   **Option B (Lenient)**: Remove automatic validation
   ```python
   def save(self, *args, **kwargs):
       # Don't auto-validate - let callers decide
       # Forms will still call clean() automatically
       super().save(*args, **kwargs)
   ```

   **Option C (Recommended)**: Validate but with clear opt-out
   ```python
   def save(self, *args, **kwargs):
       validate = kwargs.pop("validate", True)
       if validate:
           self.full_clean()
       super().save(*args, **kwargs)
   ```

2. Search for places that rely on validation being bypassed:
   ```bash
   grep -r "skip_validation" --include="*.py"
   grep -r "\.save()" --include="*.py" | grep -i character
   ```

3. Update any code that needs to bypass validation to use clear parameter

4. Remove the try/except that swallows ValidationError

5. Document the validation behavior in docstring

**Testing**:
```bash
python manage.py test characters.tests.test_character_validation
```

**Breaking Change Alert**: This could break existing code that relies on invalid saves succeeding. Audit carefully.

---

### 10. at_freebie_step() Full QuerySet Evaluation

**Impact**: LOW - Performance issue but likely not called often

**Location**: `characters/models/core/character.py:68-84`

**Problem**:
Method evaluates entire queryset to filter it:

```python
def at_freebie_step(self):
    """Characters at their freebie spending step."""
    matching_ids = [
        char.id
        for char in self  # Loads ALL characters into memory!
        if hasattr(char, "creation_status")
        and hasattr(char, "freebie_step")
        and char.creation_status == char.freebie_step
    ]
    return self.filter(id__in=matching_ids)
```

**Resolution Steps**:
1. **Option A**: Make `freebie_step` a database field if it doesn't vary by subclass:
   ```python
   # In Character model
   freebie_step = models.IntegerField(default=0)

   # Then the filter becomes trivial
   def at_freebie_step(self):
       return self.filter(creation_status=F('freebie_step'))
   ```

2. **Option B**: If `freebie_step` varies by character type, use annotations:
   ```python
   from django.db.models import Case, When, Value

   def at_freebie_step(self):
       # Annotate with freebie_step based on polymorphic type
       return self.annotate(
           freebie_step_value=Case(
               When(polymorphic_ctype__model='vampire', then=Value(5)),
               When(polymorphic_ctype__model='mage', then=Value(6)),
               # ... other types
               default=Value(-1),
           )
       ).filter(creation_status=F('freebie_step_value'))
   ```

3. **Option C**: Remove the queryset method, filter in Python where needed:
   ```python
   # Instead of: characters.at_freebie_step()
   # Use: [c for c in characters if c.creation_status == c.freebie_step]
   # More honest about what it's doing (not a real DB filter)
   ```

4. Search for uses of `at_freebie_step()`:
   ```bash
   grep -r "at_freebie_step" --include="*.py" --include="*.html"
   ```

5. Choose solution based on usage patterns and performance needs

**Testing**:
```bash
# Performance comparison
python manage.py shell
from characters.models import Character
import time

# Time current approach
start = time.time()
chars = Character.objects.all().at_freebie_step()
print(f"Current: {time.time() - start}s, {chars.count()} characters")

# Time proposed approach
# ... test alternative
```

---

### 11. Unnecessary ApprovedUserContextMixin

**Impact**: LOW - Minor code smell

**Location**: `characters/views/core/character.py:112`, `core/mixins.py:197-213`

**Problem**:
`ApprovedUserContextMixin` just adds `is_approved_user=True` to context. Used with permission mixins that already guarantee user has access:

```python
class CharacterUpdateView(ApprovedUserContextMixin, EditPermissionMixin, UpdateView):
    # If EditPermissionMixin allowed access, user is already "approved"
```

The mixin adds no value since `EditPermissionMixin` already verified permissions.

**Resolution Steps**:
1. Search for all uses of `ApprovedUserContextMixin`:
   ```bash
   grep -r "ApprovedUserContextMixin" --include="*.py"
   ```

2. For each use, check if it's combined with a permission mixin:
   - If YES: Remove `ApprovedUserContextMixin`, add `is_approved_user` in `get_context_data()` if needed
   - If NO: Keep it but consider renaming to clarify purpose

3. **Option A**: Remove the mixin entirely:
   ```python
   # Before
   class CharacterUpdateView(ApprovedUserContextMixin, EditPermissionMixin, UpdateView):
       pass

   # After
   class CharacterUpdateView(EditPermissionMixin, UpdateView):
       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['is_approved_user'] = True  # We got past permission check
           return context
   ```

4. **Option B**: Make the mixin more useful:
   ```python
   class ApprovedUserContextMixin:
       """Adds permission context for templates."""
       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           if hasattr(self, 'object') and self.object:
               context['is_approved_user'] = True
               context['user_can_edit'] = PermissionManager.user_can_edit(
                   self.request.user, self.object
               )
               context['user_can_view'] = PermissionManager.user_can_view(
                   self.request.user, self.object
               )
           return context
   ```
   (But note: `VisibilityFilterMixin` already does this)

5. Most likely: Delete `ApprovedUserContextMixin` and set context flags directly where needed

**Testing**:
```bash
python manage.py test characters.tests.test_views
# Check that templates still have access to needed context
```

---

### 12. Hardcoded Field Lists in AbilityBlock

**Impact**: LOW - Maintenance burden but rarely changes

**Location**: `characters/models/core/ability_block.py:13-45`

**Problem**:
Ability names hardcoded in model class attributes, duplicating information already in field definitions:

```python
class AbilityBlock(models.Model):
    talents = ["alertness", "athletics", "brawl", ...]
    skills = ["crafts", "drive", "etiquette", ...]
    primary_abilities = ["alertness", "athletics", ...]  # Duplicates above!

    # Then all the fields are defined separately:
    alertness = models.IntegerField(...)
    athletics = models.IntegerField(...)
    # ... etc
```

**Resolution Steps**:
1. **Option A**: Use model introspection to generate lists dynamically:
   ```python
   class AbilityBlock(models.Model):
       # Define field names as constants for reference
       TALENT_FIELDS = [
           "alertness", "athletics", "brawl", "empathy",
           "expression", "intimidation", "streetwise", "subterfuge"
       ]
       SKILL_FIELDS = [
           "crafts", "drive", "etiquette", "firearms", "melee", "stealth"
       ]
       KNOWLEDGE_FIELDS = [
           "academics", "computer", "investigation", "medicine", "science"
       ]

       @classmethod
       @property
       def talents(cls):
           """Get list of talent field names."""
           return cls.TALENT_FIELDS

       @classmethod
       @property
       def primary_abilities(cls):
           """Get list of all primary ability field names."""
           return cls.TALENT_FIELDS + cls.SKILL_FIELDS + cls.KNOWLEDGE_FIELDS
   ```

2. **Option B**: Move to settings/constants:
   ```python
   # core/constants.py
   ABILITIES = {
       'talents': ["alertness", "athletics", "brawl", ...],
       'skills': ["crafts", "drive", "etiquette", ...],
       'knowledges': ["academics", "computer", "investigation", ...],
   }

   # Then in model
   from core.constants import ABILITIES

   class AbilityBlock(models.Model):
       talents = ABILITIES['talents']
       # ... define fields
   ```

3. **Option C**: Generate fields programmatically (advanced):
   ```python
   # core/fields.py
   def create_ability_field():
       return models.IntegerField(
           default=0,
           validators=[MinValueValidator(0), MaxValueValidator(10)]
       )

   # In model
   class AbilityBlock(models.Model):
       # Use __init_subclass__ or metaclass to generate fields
       # More complex but eliminates all duplication
   ```

4. Search for code using these class attributes:
   ```bash
   grep -r "\.talents\|\.skills\|\.knowledges\|\.primary_abilities" --include="*.py"
   ```

5. Choose solution based on how these lists are used

6. Update any code relying on the old structure

**Testing**:
```bash
python manage.py test characters.tests.test_abilities
```

**Note**: This is low priority because the lists rarely change and the current approach works. Only refactor if you're already touching this code.

---

## Summary Statistics

**Total Issues**: 12
- 🔴 High Priority: 2 issues (~140 lines of code to remove/simplify)
- 🟡 Medium Priority: 4 issues (architectural improvements)
- 🟢 Low Priority: 6 issues (code quality polish)

**Estimated Effort**:
- High Priority: 8-16 hours (includes testing and migration)
- Medium Priority: 12-20 hours (requires design decisions)
- Low Priority: 4-8 hours (straightforward refactoring)

**Recommended Order**:
1. Fix #1 (Duplicate QuerySet/Manager) - Quick win, big cleanup
2. Fix #7 (Gameline detection) - Simple, prevents future bugs
3. Fix #8 (Observer check) - One-line change
4. Fix #11 (ApprovedUserContextMixin) - Easy cleanup
5. Design decision for #3 (Permission wrappers) - impacts API
6. Plan #2 (Dual XP systems) - requires data migration strategy
7. Refactor #6 (remove_from_organizations) - requires architecture discussion
8. Remaining items as time permits

---

## Notes

- **Backward Compatibility**: Several changes may break existing code. Search thoroughly and test comprehensively.
- **Performance Testing**: Use Django Debug Toolbar and query logging to verify optimizations actually improve performance.
- **Team Discussion**: Items marked with "Decision Point" should be discussed with the team before implementing.
- **Migration Safety**: For #2 (XP systems), test the data migration extensively in staging before production.

---

**Document Version**: 1.0
**Last Updated**: 2025-11-23
**Related Docs**:
- `TODO.md` - Main project TODO list
- `JSONFIELD_MIGRATION_GUIDE.md` - XP system migration context
- `docs/design/permissions_system.md` - Permission architecture
- `docs/guides/limited_owner_forms.md` - Form permission patterns
