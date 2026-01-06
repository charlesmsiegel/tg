# Plan: Simplify Over-Engineered Code

## Summary of Findings

The codebase has several categories of over-engineering that can be simplified.

---

## Critical Priority

### 1. Bare Except Clauses (7 locations)
Silently swallowing errors, making debugging difficult.

| File | Lines |
|------|-------|
| `core/templatetags/field.py` | 11 |
| `characters/models/core/human.py` | 757, 779, 837, 852 |
| `characters/models/vampire/vampire.py` | 437, 561 |

**Fix:** Replace with specific exception handling or remove.

### 2. Trivial Getter/Setter Methods
**File:** `core/models.py:368-407`

Unused methods like `has_name()`, `set_name()`, `has_description()`, `set_description()`, etc. that wrap direct attribute access with unnecessary abstraction.

**Fix:** Delete entirely - direct attribute access is clearer.

---

## High Priority

### 3. Permission Delegation Wrappers
**File:** `core/models.py:250-325`

Methods like `user_can_view()`, `user_can_edit()` that just delegate to `PermissionManager` with circular imports inside each method.

**Fix:** Remove wrappers, use `PermissionManager` directly.

### 4. ProfileView.post() Mega-Method
**File:** `accounts/views.py:79-231`

149-line method handling 14+ POST actions with repeated patterns.

**Fix:** Refactor into dispatch pattern or separate view methods.

### 5. Duplicate XP/Freebie Approval Mixins
**File:** `core/mixins.py:538-717`

178 lines of nearly identical code in `XPApprovalMixin` and `FreebieApprovalMixin`.

**Fix:** Consolidate into single generic `ApprovalMixin`.

### 6. Redundant XP Validation
**File:** `characters/models/core/character.py:157-161, 199-201`

Same validation at DB constraint level AND clean() method.

**Fix:** Remove clean() validation, rely on DB constraint.

---

## Medium Priority

### 7. Unused Template Tags/Filters
| Filter | File | Status |
|--------|------|--------|
| `reverse` | `core/templatetags/reverse.py` | Unused |
| `lore_name` | `core/templatetags/dots.py:44-50` | Unused |
| `get_item` | `core/templatetags/json_filters.py:20-30` | Unused |

**Fix:** Delete unused filters.

### 8. Limited Edit Forms Factory
**Files:**
- `characters/forms/core/limited_edit.py:140-185`
- `items/forms/core/limited_edit.py` (54 lines)
- `locations/forms/core/limited_edit.py` (54 lines)

Generates 18 identical form classes that could be one dynamic form.

**Fix:** Simplify to single form with model parameter.

### 9. Hardcoded EXCLUDED_TYPES List
**File:** `game/forms.py:198-284`

87 lines of hardcoded exclusions.

**Fix:** Derive from model metadata or configuration.

### 10. ChronicleDataService Hardcoded Mappings
**File:** `core/services/chronicle_data.py:32-87`

50+ entry dictionaries for gameline mappings.

**Fix:** Derive from ContentType registry or settings.

### 11. Unused Grimoire Setter Methods
**File:** `items/models/mage/grimoire.py:63-162`

20+ `set_*()` and `has_*()` methods only used internally by `random()`.

**Fix:** Inline into random methods or use direct assignment.

---

## Low Priority

### 12. Single-Line Mixin Subclasses
**File:** `core/mixins.py`

Classes like `SpendXPPermissionMixin` that just set one class variable.

### 13. Duplicate Widget Class Application
**File:** `accounts/forms.py` (3 locations)

Same pattern for applying CSS classes to form widgets.

### 14. Over-Abstracted Permission Template Tags
**File:** `core/templatetags/permissions.py:25-204`

8 template tags doing nearly identical work.

---

## Implementation Plan

**Approach:** Moderate cleanup, ordered by impact (highest first). Test after each file.

---

### Phase 1: Add gameline Attribute + Consolidate get_heading (HIGH IMPACT)
**Files:**
- `core/models.py` (base Model class)
- `core/services/chronicle_data.py`
- All character models (add `gameline` attribute, remove `get_heading`)
- All location models (add `gameline` attribute, remove `get_heading`)
- All item models (add `gameline` attribute, remove `get_heading`)

**Part A: Add gameline attribute and consolidate get_heading**

1. Add `gameline = 'vtm'` (etc.) class attribute to each model
2. Add universal `get_heading()` to base `Model` class:
   ```python
   def get_heading(self):
       return f"{self.gameline}_heading" if self.gameline else "wod_heading"
   ```
3. **Delete 100+ duplicate `get_heading()` methods** from all subclasses
4. Use `gameline = 'wod'` for generic models (LocationModel, City, ItemModel) - they appear in all tabs

**Part B: Simplify ChronicleDataService with dynamic introspection**

5. Add helper to get all model names for a gameline:
   ```python
   @classmethod
   def get_model_names_for_gameline(cls, gameline, base_class):
       """Dynamically get model names for a gameline using class attributes."""
       return [m.__name__.lower() for m in base_class.__subclasses__()
               if getattr(m, 'gameline', None) in (gameline, 'wod')]
   ```
6. Replace hardcoded `CHAR_GAMELINE_MAP`, `LOC_GAMELINE_MAP`, `ITEM_GAMELINE_MAP` with calls to helper
7. Replace `GAMELINE_SHORT_NAMES` with `settings.GAMELINES[code]['short']`
8. Replace `GAMELINE_ORDER` with `list(settings.GAMELINES.keys())`
9. Run tests: `python manage.py test`

---

### Phase 2: Consolidate Duplicate Approval Mixins (HIGH IMPACT)
**File:** `core/mixins.py`

1. Create single `ApprovalMixin` base class with configurable behavior
2. Refactor `XPApprovalMixin` and `FreebieApprovalMixin` to use base (178 lines → ~30)
3. Run tests: `python manage.py test core`

---

### Phase 3: Simplify ProfileView.post() (HIGH IMPACT)
**File:** `accounts/views.py`

1. Extract approval handlers into dispatch dictionary or separate methods
2. Reduce 149-line method to manageable chunks
3. Run tests: `python manage.py test accounts`

---

### Phase 4: Remove Permission Delegation Wrappers (MEDIUM IMPACT)
**File:** `core/models.py:250-325`

1. Find all usages of wrapper methods
2. Replace with direct `PermissionManager` calls
3. Delete wrapper methods
4. Run tests: `python manage.py test`

---

### Phase 5: Simplify Limited Edit Forms Factory (MEDIUM IMPACT)
**Files:**
- `characters/forms/core/limited_edit.py:140-185`
- `items/forms/core/limited_edit.py` (entire file)
- `locations/forms/core/limited_edit.py` (entire file)

1. Create single `LimitedEditForm` that accepts model as parameter
2. Remove factory function and 18 generated form classes
3. Update all imports to use new form
4. Run tests: `python manage.py test characters items locations`

---

### Phase 6: Fix Bare Except Clauses (MEDIUM IMPACT - Bug Fix)
**Files:**
- `core/templatetags/field.py:11`
- `characters/models/core/human.py:757,779,837,852`
- `characters/models/vampire/vampire.py:437,561`

1. Replace each bare `except:` with specific exceptions
2. Run tests after each file

---

### Phase 7: Remove Unused Code (LOW IMPACT)
**Files:**
- `core/models.py:368-407` - Delete trivial getters/setters
- `core/templatetags/reverse.py` - Delete entire file
- `core/templatetags/dots.py:44-50` - Delete `lore_name` filter
- `core/templatetags/json_filters.py:20-30` - Delete `get_item` filter

Run tests after each deletion.

---

### Phase 8: Remove Redundant Validation (LOW IMPACT)
**File:** `characters/models/core/character.py:199-201`

1. Remove clean() XP validation (DB constraint is sufficient)
2. Run tests: `python manage.py test characters`

---

### Phase 9: Consolidate Single-Line Mixin Subclasses (LOW IMPACT)
**File:** `core/mixins.py`

Single-line mixins like:
```python
class SpendXPPermissionMixin(PermissionRequiredMixin):
    required_permission = Permission.SPEND_XP
```

1. Replace with direct use of `PermissionRequiredMixin(required_permission=X)` or inline
2. Update views to use base class with parameter
3. Delete empty subclasses
4. Run tests: `python manage.py test`

---

## Summary

| Phase | Description | Impact | Risk | Effort |
|-------|-------------|--------|------|--------|
| 1 | gameline attr + get_heading + ChronicleDataService | **High** | Medium | High |
| 2 | Approval Mixins consolidation | **High** | Medium | Medium |
| 3 | ProfileView.post() simplification | **High** | Medium | Medium |
| 4 | Permission Wrappers removal | Medium | Medium | Medium |
| 5 | Form Factory simplification | Medium | Low | Low |
| 6 | Bare Except Clauses fix | Medium | Low | Low |
| 7 | Unused Code deletion | Low | Low | Low |
| 8 | Redundant Validation removal | Low | Low | Low |
| 9 | Single-Line Mixins consolidation | Low | Low | Low |

**Phase 1 is now first** - deletes 100+ methods and adds dynamic gameline introspection.
