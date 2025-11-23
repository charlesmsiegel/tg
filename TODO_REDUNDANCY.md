# TODO: Redundancy Cleanup

This document tracks redundant systems, duplicate code, and overlapping functionality discovered in the codebase. Items are prioritized by impact and complexity.

**Last Updated:** 2025-11-23
**Status:** 🔴 22 files affected, ~164 lines of redundant code identified

---

## 🔴 HIGH PRIORITY

### 1. Consolidate QuerySet and Manager Methods

**File:** `core/models.py` (lines 36-106)

**Issue:** Six methods are duplicated identically between `ModelQuerySet` and `ModelManager` classes. This violates DRY principle and creates maintenance burden.

**Duplicated Methods:**
- `pending_approval_for_user()` - lines 36-48 (QuerySet) vs 74-86 (Manager)
- `visible()` - lines 50-52 vs 88-90
- `for_chronicle()` - lines 54-56 vs 92-94
- `owned_by()` - lines 58-60 vs 96-98
- `with_pending_images()` - lines 62-64 vs 100-102
- `for_user_chronicles()` - lines 66-68 vs 104-106

**Impact:** ~70 lines of duplicate code

**Recommended Solution:**
```python
# Keep methods only in ModelQuerySet class
class ModelQuerySet(PolymorphicQuerySet):
    def pending_approval_for_user(self, user):
        # ... existing implementation ...

    def visible(self):
        # ... existing implementation ...

    # ... other methods ...

# Use as_manager() to create manager automatically
class Model(PolymorphicModel):
    objects = ModelQuerySet.as_manager()
```

**Context:**
- Django's `QuerySet.as_manager()` automatically creates a manager that delegates to the queryset
- This is Django's recommended pattern for custom managers with chainable methods
- Removes need to maintain duplicate method definitions
- All existing code will continue to work (e.g., `Character.objects.visible()`)

**Testing Required:**
- Run full test suite to ensure manager methods still work
- Test method chaining: `Model.objects.visible().for_chronicle(chronicle)`
- Verify polymorphic queries still work correctly

---

### 2. Eliminate Duplicate Limited Edit Forms

**File:** `characters/forms/core/limited_edit.py` (lines 125-207)

**Issue:** 12 form classes that differ ONLY by their `Meta.model` attribute. Each inherits from `LimitedHumanEditForm` and only overrides the model.

**Duplicated Forms:**
1. `LimitedMageEditForm` (lines 125-129) - model: Mage
2. `LimitedMtAHumanEditForm` (lines 132-136) - model: MtAHuman
3. `LimitedVampireEditForm` (lines 139-143) - model: Vampire
4. `LimitedVtMHumanEditForm` (lines 146-150) - model: VtMHuman
5. `LimitedGarouEditForm` (lines 153-157) - model: Garou
6. `LimitedWtAHumanEditForm` (lines 160-164) - model: WtAHuman
7. `LimitedChangelingEditForm` (lines 167-171) - model: Changeling
8. `LimitedCtDHumanEditForm` (lines 174-178) - model: CtDHuman
9. `LimitedWraithEditForm` (lines 181-185) - model: Wraith
10. `LimitedWtOHumanEditForm` (lines 188-192) - model: WtOHuman
11. `LimitedDemonEditForm` (lines 195-199) - model: Demon
12. `LimitedDtFHumanEditForm` (lines 202-206) - model: DtFHuman

**Impact:** ~82 lines of boilerplate code

**Recommended Solution - Option A (Factory Function):**
```python
def create_limited_edit_form(model_class):
    """
    Factory function to create a limited edit form for a specific model.

    Args:
        model_class: The character model class

    Returns:
        A form class configured for limited editing
    """
    class GeneratedLimitedEditForm(LimitedHumanEditForm):
        class Meta(LimitedHumanEditForm.Meta):
            model = model_class

    GeneratedLimitedEditForm.__name__ = f'Limited{model_class.__name__}EditForm'
    return GeneratedLimitedEditForm

# Usage in views:
from characters.models.mage.mage import Mage
LimitedMageEditForm = create_limited_edit_form(Mage)
```

**Recommended Solution - Option B (Generic Form):**
```python
class LimitedCharacterEditForm(LimitedHumanEditForm):
    """
    Generic limited edit form for any character type.
    Automatically uses the model from the view's get_form_kwargs().
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Model is set by the view via instance
        if hasattr(self, 'instance') and self.instance:
            self._meta.model = type(self.instance)
```

**Context:**
- All 12 forms have identical fields (inherited from `LimitedHumanEditForm`)
- Only difference is the `Meta.model` attribute
- Forms are used in character update views when user is owner (not ST)
- See `docs/guides/limited_owner_forms.md` for usage pattern

**Files to Update:**
- `characters/forms/core/limited_edit.py` - implement factory/generic form
- All character update views that reference these forms (check imports)
- Update `docs/guides/limited_owner_forms.md` with new pattern

**Testing Required:**
- Test each gameline's character update view with owner permissions
- Verify only allowed fields are editable (notes, description, public_info, image)
- Ensure form validation still works correctly
- Test with polymorphic character types

---

## 🟡 MEDIUM PRIORITY

### 3. Update Deprecated Mixin Import Paths

**Files Affected:** 18 character view files

**Issue:** Despite consolidation to `core.mixins` (documented in CLAUDE.md), many files still import from deprecated backward-compatibility shims in `core/views/`.

**Deprecated Shim Files:**
- `core/views/message_mixin.py` (27 lines) - imports from `core.mixins`
- `core/views/approved_user_mixin.py` (12 lines) - imports from `core.mixins`

**Files Using Old Imports:**
1. `characters/views/wraith/wtohuman.py`
2. `characters/views/werewolf/wtahuman.py`
3. `characters/views/werewolf/garou.py`
4. `characters/views/werewolf/fomor.py`
5. `characters/views/vampire/vtmhuman.py`
6. `characters/views/mage/sorcerer.py`
7. `characters/views/mage/mtahuman.py`
8. `characters/views/mage/mage.py`
9. `characters/views/mage/companion.py`
10. `characters/views/changeling/changeling.py`
11. `characters/views/changeling/ctdhuman.py`
12. `characters/views/demon/demon_chargen.py`
13. `characters/views/demon/dtfhuman_chargen.py`
14. `characters/views/demon/thrall_chargen.py`
15. `characters/views/vampire/ghoul_chargen.py`
16. `characters/views/vampire/vampire_chargen.py`
17. `characters/views/werewolf/fera.py`
18. `characters/views/wraith/wraith_chargen.py`

**Impact:** Confusing import patterns, extra files to maintain

**Recommended Solution:**

**Step 1:** Update each file's imports from:
```python
# Old (deprecated)
from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import SuccessMessageMixin
```

To:
```python
# New (correct)
from core.mixins import SpecialUserMixin, SuccessMessageMixin
```

**Step 2:** After all imports updated, delete deprecated shim files:
- `core/views/message_mixin.py`
- `core/views/approved_user_mixin.py`

**Context:**
- All view mixins consolidated to `core.mixins` per CLAUDE.md guidelines
- Backward compatibility shims were kept to avoid breaking existing code
- 130+ files already use correct imports, these 18 are stragglers
- Safe to update: shims just re-export from `core.mixins`

**Search Command to Find Usage:**
```bash
grep -r "from core\.views\.(message_mixin|approved_user_mixin) import" --include="*.py"
```

**Testing Required:**
- Import each updated view file to check for import errors
- Run character view tests: `python manage.py test characters.tests`
- Verify no other code imports from deprecated paths

---

## 🟢 LOW PRIORITY

### 4. Consolidate ST Check Logic in Template Tags

**File:** `core/templatetags/permissions.py` (lines 147-163)

**Issue:** The `is_st()` template tag reimplements admin/ST checking logic instead of delegating to the canonical `user.profile.is_st()` method.

**Current Implementation (Redundant):**
```python
@register.simple_tag(takes_context=True)
def is_st(context, obj):
    """Check if current user is ST of object's chronicle."""
    user = context["request"].user

    # Admin check - DUPLICATE of Profile.is_st()
    if user.is_superuser or user.is_staff:
        return True

    # Chronicle ST check - DUPLICATE logic
    if hasattr(obj, "chronicle") and obj.chronicle:
        if hasattr(obj.chronicle, "head_st") and obj.chronicle.head_st == user:
            return True
        if hasattr(obj.chronicle, "head_storytellers"):
            if obj.chronicle.head_storytellers.filter(id=user.id).exists():
                return True

    return False
```

**Recommended Solution:**
```python
@register.simple_tag(takes_context=True)
def is_st(context, obj):
    """Check if current user is ST of object's chronicle."""
    user = context["request"].user

    # Delegate to canonical implementation
    return user.profile.is_st()
```

**Context:**
- `accounts/models.py` lines 109-111 has canonical `is_st()` implementation
- Template tag should delegate to model method to avoid duplication
- Current implementation has ~15 lines vs proposed 2 lines
- Lines 152-153 duplicate the admin check that `Profile.is_st()` already performs

**Note:** The current template tag checks if user is ST *of a specific chronicle* (via the `obj` parameter), while `Profile.is_st()` checks if user is ST *of any chronicle*. If object-specific checking is needed, this may not be pure redundancy. Investigate usage in templates to determine correct approach.

**Investigation Required:**
- Search template usage: `{% is_st object %}` vs `{% if user.profile.is_st %}`
- Determine if object-specific ST checking is actually used
- If not used object-specifically, consolidate to `user.profile.is_st()`
- If object-specific checking is needed, document the distinction

**Testing Required:**
- Review all templates using `{% is_st %}` tag
- Ensure ST permissions display correctly after change
- Test with: admin users, chronicle STs, and regular users

---

### 5. Refactor SpecialUserMixin ST Check

**File:** `core/mixins.py` (line 250)

**Issue:** `SpecialUserMixin.check_if_special_user()` queries `STRelationship` directly instead of using the existing `user.profile.is_st()` method.

**Current Implementation:**
```python
def check_if_special_user(self, user, obj):
    """
    Check if user has special access (owner, ST, or unowned object).

    Args:
        user: User to check
        obj: Object to check access for

    Returns:
        bool: True if user has special access
    """
    if obj.owner is None:
        return True
    if user == obj.owner:
        return True
    if not user.is_authenticated:
        return False
    # LINE 250 - Direct query instead of using is_st()
    if STRelationship.objects.filter(user=user).count() > 0:
        return True
    return False
```

**Recommended Solution:**
```python
def check_if_special_user(self, user, obj):
    """
    Check if user has special access (owner, ST, or unowned object).

    Args:
        user: User to check
        obj: Object to check access for

    Returns:
        bool: True if user has special access
    """
    if obj.owner is None:
        return True
    if user == obj.owner:
        return True
    if not user.is_authenticated:
        return False
    # Use canonical is_st() method
    if user.profile.is_st():
        return True
    return False
```

**Context:**
- `accounts/models.py` lines 109-111 has canonical `is_st()` method
- `is_st()` already checks `STRelationship.objects.filter(st=user.profile).exists()`
- Direct query bypasses any future improvements to ST checking logic
- Using `.count() > 0` instead of `.exists()` is also less efficient

**Impact:** Minor - 2 lines of redundant code, but important for consistency

**Testing Required:**
- Test views that use `SpecialUserMixin` (search for inheritance)
- Verify ST users still get special access
- Ensure regular users are properly restricted

---

## ✅ VERIFIED AS INTENTIONAL (Not Redundant)

### Gameline Model Structures
**Status:** NOT REDUNDANT - Proper polymorphic inheritance

**Finding:** While characters/items/locations have similar structures across 6 gamelines (vtm, wta, mta, wto, ctd, dtf), this is intentional design:
- Each inherits from gameline-specific base classes
- Each defines unique fields and game mechanics
- `freebie_step` values vary intentionally by gameline
- Proper use of Django Polymorphic pattern

**No Action Required**

---

### XP Form Inheritance Pattern
**Status:** NOT REDUNDANT - Proper inheritance

**Finding:** `MageXPForm` extends base `XPForm` with gameline-specific categories. This is proper inheritance pattern for future gameline-specific forms.

**Files:**
- `characters/forms/core/xp.py` - Base form (~237 lines)
- `characters/forms/mage/xp.py` - Mage-specific additions

**No Action Required**

---

## 📊 Impact Summary

| Priority | Issues | Files | Lines of Redundant Code |
|----------|--------|-------|------------------------|
| 🔴 High | 2 | 2 | ~152 lines |
| 🟡 Medium | 1 | 20 | N/A (import cleanup) |
| 🟢 Low | 2 | 2 | ~12 lines |
| **TOTAL** | **5** | **24** | **~164 lines** |

---

## 🎯 Recommended Implementation Order

### Phase 1: High Impact (Est. 2-4 hours)
1. ✅ Consolidate QuerySet/Manager methods (HIGH)
   - Modify `core/models.py`
   - Run full test suite
   - Verify polymorphic queries work

2. ✅ Create limited form factory/generic (HIGH)
   - Modify `characters/forms/core/limited_edit.py`
   - Update view imports if needed
   - Test all gameline character updates

### Phase 2: Clean Up (Est. 1-2 hours)
3. ✅ Update deprecated mixin imports (MEDIUM)
   - Update 18 character view files
   - Delete backward compatibility shims
   - Run character tests

### Phase 3: Polish (Est. 1 hour)
4. ✅ Consolidate template tag ST check (LOW)
   - Investigate template usage first
   - Update `core/templatetags/permissions.py`
   - Test template rendering

5. ✅ Refactor SpecialUserMixin ST check (LOW)
   - Update `core/mixins.py` line 250
   - Test views using SpecialUserMixin

---

## 📝 Notes

- **Testing Critical:** Full test suite should pass after each phase
- **Backward Compatibility:** Changes are internal refactoring, APIs remain same
- **Documentation:** Update `docs/guides/limited_owner_forms.md` after Phase 1, item 2
- **Git Strategy:** Each phase should be a separate commit/PR for easier review

---

## 🔍 Discovery Methodology

This document was generated through systematic analysis:
1. Permission system analysis (PermissionManager vs is_st())
2. View mixin consolidation review
3. Gameline implementation pattern analysis
4. Form pattern duplication detection
5. Utility function and template pattern review

**Analysis Date:** 2025-11-23
**Analyzer:** Claude Code systematic codebase exploration
**Scope:** Full repository scan focusing on inheritance, imports, and method duplication
