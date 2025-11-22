# Code Consistency Improvements

## Summary

This document describes the code consistency improvements implemented to address issues outlined in the original task.

## Changes Implemented

### 1. Centralized Gameline Configuration ✅

**Problem:** Gameline strings were hardcoded in multiple places (core/utils.py, core/models.py, management commands), making it difficult to add or modify gamelines.

**Solution:** Created centralized gameline configuration in `tg/settings.py`:

```python
GAMELINES = {
    'wod': {'name': 'World of Darkness', 'short': '', 'app_name': 'wod'},
    'vtm': {'name': 'Vampire: the Masquerade', 'short': 'VtM', 'app_name': 'vampire'},
    'wta': {'name': 'Werewolf: the Apocalypse', 'short': 'WtA', 'app_name': 'werewolf'},
    'mta': {'name': 'Mage: the Ascension', 'short': 'MtA', 'app_name': 'mage'},
    'wto': {'name': 'Wraith: the Oblivion', 'short': 'WtO', 'app_name': 'wraith'},
    'ctd': {'name': 'Changeling: the Dreaming', 'short': 'CtD', 'app_name': 'changeling'},
    'dtf': {'name': 'Demon: the Fallen', 'short': 'DtF', 'app_name': 'demon'},
}

GAMELINE_CHOICES = [(key, val['name']) for key, val in GAMELINES.items()]
```

**Files Modified:**
- `tg/settings.py` - Added GAMELINES and GAMELINE_CHOICES
- `core/utils.py` - Updated `get_gameline_name()` and `get_short_gameline_name()` to use settings
- `core/models.py` - Updated Book and HouseRule models to use `settings.GAMELINE_CHOICES`

**Benefits:**
- Single source of truth for gameline configuration
- Easy to add new gamelines (just update settings.py)
- Consistent gameline data across the application
- Added missing 'dtf' (Demon: the Fallen) gameline

**Impact:**
- Affects 2 models (Book, HouseRule)
- Affects 2 utility functions
- Future management commands can import from settings instead of hardcoding

### 2. Consolidated Mixins ✅

**Problem:** Mixins were scattered across 3 files:
- `core/mixins.py` (188 lines) - Permission mixins
- `core/views/approved_user_mixin.py` (15 lines) - SpecialUserMixin
- `core/views/message_mixin.py` (130 lines) - Message mixins

**Solution:** Consolidated all mixins into `core/mixins.py`:

**Mixins Now Available in `core.mixins`:**

*Permission Mixins:*
- `PermissionRequiredMixin` - Base permission mixin
- `ViewPermissionMixin` - Requires VIEW_FULL permission
- `EditPermissionMixin` - Requires EDIT_FULL permission
- `SpendXPPermissionMixin` - Requires SPEND_XP permission
- `SpendFreebiesPermissionMixin` - Requires SPEND_FREEBIES permission
- `VisibilityFilterMixin` - Filters querysets by user permissions
- `OwnerRequiredMixin` - Restricts to object owner
- `STRequiredMixin` - Restricts to storytellers

*Message Mixins:*
- `SuccessMessageMixin` - Adds success messages
- `ErrorMessageMixin` - Adds error messages
- `MessageMixin` - Combined success/error messages
- `DeleteMessageMixin` - Message for deletions

*User Check Mixins:*
- `SpecialUserMixin` - Check for special user access

**Files Modified:**
- `core/mixins.py` - Added SpecialUserMixin and all message mixins
- `core/views/approved_user_mixin.py` - Now imports from core.mixins (backward compatibility)
- `core/views/message_mixin.py` - Now imports from core.mixins (backward compatibility)

**Benefits:**
- Single location for all view mixins
- Easier to find and maintain mixins
- Consistent imports across the codebase
- Backward compatibility maintained

**Impact:**
- Existing code continues to work (backward compatible)
- New code should import from `core.mixins`
- Old import paths deprecated but functional

### 3. Permission System Standardization Documentation ✅

**Problem:** Two different permission systems used inconsistently:
- `PermissionManager` - Object-level permissions
- `is_st()` - Role-based checks

**Solution:** Created comprehensive documentation in `PERMISSION_STANDARDIZATION.md`

**Key Guidelines:**

*Use PermissionManager when:*
- Checking permissions on a specific object
- Need different permission levels (view vs edit vs spend XP)
- In detail/update/delete views for objects

*Use is_st() when:*
- Checking if user is a storyteller in general
- In forms to determine available options
- In templates to show/hide ST-only UI elements

**Files Created:**
- `PERMISSION_STANDARDIZATION.md` - Comprehensive guide with examples

**Benefits:**
- Clear guidance on which permission system to use
- Examples of proper patterns
- Migration path for existing code
- Documents consolidated mixin locations

**Impact:**
- Provides clear standards for future development
- Helps developers make consistent permission choices
- Documents best practices

## Files Changed

### Modified Files (6)
1. `tg/settings.py` - Added GAMELINES configuration
2. `core/utils.py` - Updated gameline functions
3. `core/models.py` - Updated gameline choices
4. `core/mixins.py` - Consolidated all mixins
5. `core/views/approved_user_mixin.py` - Deprecated, imports from core.mixins
6. `core/views/message_mixin.py` - Deprecated, imports from core.mixins

### Created Files (2)
1. `PERMISSION_STANDARDIZATION.md` - Permission system documentation
2. `CODE_CONSISTENCY_IMPROVEMENTS.md` - This file

## Not Addressed (Out of Scope)

### Template Organization
The template organization issue (598 templates, 409 in characters alone) was not addressed as it would require:
- Significant structural reorganization
- Careful analysis of dependencies
- Risk of breaking existing functionality
- Extensive testing of all templates

**Recommendation:** This should be a separate, dedicated refactoring project with thorough testing.

### URL Config Standardization
URL configs were not modified as they currently use Django's standard `include()` pattern and don't have hardcoded gameline strings in the main configuration.

### Management Command Updates
Management commands were not updated as part of this change. Future commands should import from `settings.GAMELINES` instead of hardcoding gameline lists.

## Testing

All Python files were verified to compile successfully:
- `tg/settings.py` ✅
- `core/utils.py` ✅
- `core/models.py` ✅
- `core/mixins.py` ✅

Logic testing confirmed:
- Gameline lookup functions work correctly
- GAMELINE_CHOICES properly formatted
- All gamelines accessible (including new 'dtf')

## Migration Notes

### For Developers

**Gamelines:**
```python
# Old (hardcoded)
if gameline == "vtm":
    return "Vampire: the Masquerade"

# New (use settings)
from django.conf import settings
return settings.GAMELINES.get(gameline, {}).get('name', gameline)
```

**Mixins:**
```python
# Old (scattered imports)
from core.views.message_mixin import SuccessMessageMixin
from core.views.approved_user_mixin import SpecialUserMixin

# New (consolidated)
from core.mixins import SuccessMessageMixin, SpecialUserMixin
```

**Permissions:**
- See `PERMISSION_STANDARDIZATION.md` for detailed guidance

## Benefits Summary

1. **Maintainability** - Single source of truth for gamelines and mixins
2. **Extensibility** - Easy to add new gamelines or mixins
3. **Consistency** - Clear patterns for common tasks
4. **Documentation** - Comprehensive guides for developers
5. **Backward Compatibility** - Existing code continues to work

## Future Improvements

1. Update management commands to use `settings.GAMELINES`
2. Migrate existing views to use consolidated mixins
3. Apply permission standardization patterns throughout codebase
4. Consider template organization refactoring (separate project)
5. Add automated tests for gameline configuration
