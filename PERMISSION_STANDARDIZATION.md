# Permission System Standardization Guide

## Overview

This document outlines the standardized approach to handling permissions in the codebase. Two different permission patterns were previously used inconsistently. This guide establishes when to use each pattern.

## The Two Permission Systems

### 1. PermissionManager (Object-Level Permissions)

**Location:** `core/permissions.py`

**Purpose:** Granular, object-level permission checks with multiple permission levels.

**Permission Levels:**
- `Permission.VIEW_FULL` - Can view all object details
- `Permission.EDIT_FULL` - Can edit object
- `Permission.SPEND_XP` - Can spend XP (characters)
- `Permission.SPEND_FREEBIES` - Can spend freebies (characters)

**Usage:** For checking if a specific user can perform a specific action on a specific object.

**Example:**
```python
from core.permissions import Permission, PermissionManager

# In a view
can_edit = PermissionManager.user_has_permission(
    request.user,
    character_obj,
    Permission.EDIT_FULL
)
```

**Best Practice:** Use permission mixins from `core.mixins`:
```python
from core.mixins import EditPermissionMixin, ViewPermissionMixin

class CharacterUpdateView(EditPermissionMixin, UpdateView):
    model = Character
    # Automatically checks EDIT_FULL permission
```

### 2. is_st() Method (Role-Based Checks)

**Location:** `accounts/models.py` (Profile model)

**Purpose:** Simple role-based check - is the user a storyteller at all?

**Usage:** For checking if a user has storyteller privileges generally (not tied to a specific object).

**Example:**
```python
# In forms or context preparation
if request.user.profile.is_st():
    # Show additional ST-only options
    context['show_approval_buttons'] = True
```

**Best Practice:** For views requiring ST access, use `STRequiredMixin` from `core.mixins`:
```python
from core.mixins import STRequiredMixin

class ApprovalView(STRequiredMixin, UpdateView):
    model = Character
    # Automatically restricts to STs
```

Or use the existing `StorytellerRequiredMixin` in `game/views.py` (consider consolidating):
```python
from django.contrib.auth.mixins import UserPassesTestMixin

class StorytellerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.is_st()
```

## When to Use Which System

### Use PermissionManager when:
- Checking permissions on a **specific object** (character, location, item)
- Need different permission levels (view vs edit vs spend XP)
- In detail/update/delete views for objects
- Filtering querysets by user permissions

### Use is_st() when:
- Checking if user is a storyteller **in general**
- In forms to determine available options
- In templates to show/hide ST-only UI elements
- For approval workflows not tied to specific objects

## Recommended Pattern

### For Class-Based Views

**Bad** (inconsistent):
```python
class CharacterUpdateView(UpdateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_st():
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
```

**Good** (use mixins):
```python
from core.mixins import EditPermissionMixin

class CharacterUpdateView(EditPermissionMixin, UpdateView):
    model = Character
    # Permission check handled automatically
```

### For Function-Based Views

**Bad** (inconsistent):
```python
def approve_character(request, pk):
    if not request.user.profile.is_st():
        raise PermissionDenied()
    # ... rest of logic
```

**Good** (use decorator):
```python
from core.decorators import storyteller_required

@storyteller_required
def approve_character(request, pk):
    # ... rest of logic
```

### For Templates

Use template tags from `core/templatetags/permissions.py`:
```django
{% load permissions %}

{% if user|can_edit:character %}
    <a href="{% url 'characters:update' character.pk %}">Edit</a>
{% endif %}
```

## Migration Path

For existing code using inconsistent patterns:

1. **Views with object-specific checks** → Use `PermissionManager` or mixins from `core.mixins`
2. **Views with ST-only checks** → Use `STRequiredMixin` from `core.mixins`
3. **Forms with permission logic** → Use `is_st()` for role checks, `PermissionManager` for object checks
4. **Templates** → Use permission template tags

## Consolidated Mixins

All permission and message mixins are now consolidated in **`core.mixins`**:

### Permission Mixins
- `PermissionRequiredMixin` - Base permission mixin
- `ViewPermissionMixin` - Requires VIEW_FULL permission
- `EditPermissionMixin` - Requires EDIT_FULL permission
- `SpendXPPermissionMixin` - Requires SPEND_XP permission
- `SpendFreebiesPermissionMixin` - Requires SPEND_FREEBIES permission
- `VisibilityFilterMixin` - Filters querysets by user permissions
- `OwnerRequiredMixin` - Restricts to object owner
- `STRequiredMixin` - Restricts to storytellers

### Message Mixins
- `SuccessMessageMixin` - Adds success messages
- `ErrorMessageMixin` - Adds error messages
- `MessageMixin` - Combined success/error messages
- `DeleteMessageMixin` - Message for deletions

### User Check Mixins
- `SpecialUserMixin` - Check for special user access

**Note:** Old mixin locations (`core/views/approved_user_mixin.py`, `core/views/message_mixin.py`) are deprecated but maintained for backward compatibility.

## Summary

- **Object permissions** → Use `PermissionManager` and mixins from `core.mixins`
- **Role checks** → Use `is_st()` or `STRequiredMixin`
- **All mixins** → Import from `core.mixins` (consolidated location)
- **Templates** → Use permission template tags
- **Consistency** → Always use the same pattern for the same type of check
