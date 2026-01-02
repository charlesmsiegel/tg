# Permissions System Design

## Overview

The permissions system provides role-based access control (RBAC) with fine-grained permissions for World of Darkness game objects including characters, items, and locations.

## Architecture

### Core Components

1. **PermissionManager** (`core/permissions.py`) - Central service for all permission checks
2. **View Mixins** (`core/mixins.py`) - Django CBV integration
3. **Template Tags** (`core/templatetags/permissions.py`) - Template-level permission checks

### Role Hierarchy

| Role | Description | Scope |
|------|-------------|-------|
| `ADMIN` | Site administrators (superuser/staff) | Global |
| `CHRONICLE_HEAD_ST` | Head storyteller of a chronicle | Chronicle-specific |
| `GAME_ST` | Game storyteller (read-only) | Chronicle-specific |
| `OWNER` | Object owner | Object-specific |
| `PLAYER` | Has approved character in same chronicle | Chronicle-specific |
| `OBSERVER` | Granted observer access | Object-specific |
| `AUTHENTICATED` | Any logged-in user | Global |
| `ANONYMOUS` | Not logged in | Global |

### Permission Types

| Permission | Description |
|------------|-------------|
| `VIEW_FULL` | Full read access to all object data |
| `VIEW_PARTIAL` | Limited read access (public info only) |
| `EDIT_FULL` | Full write access to all fields |
| `EDIT_LIMITED` | Limited write access (notes, journals) |
| `SPEND_XP` | Can spend experience points |
| `SPEND_FREEBIES` | Can spend freebie points |
| `DELETE` | Can delete the object |
| `APPROVE` | Can approve/reject submissions |
| `MANAGE_OBSERVERS` | Can add/remove observers |

### Role-Permission Matrix

| Role | VIEW_FULL | VIEW_PARTIAL | EDIT_FULL | EDIT_LIMITED | SPEND_XP | SPEND_FREEBIES | DELETE | APPROVE | MANAGE_OBSERVERS |
|------|-----------|--------------|-----------|--------------|----------|----------------|--------|---------|------------------|
| ADMIN | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CHRONICLE_HEAD_ST | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| GAME_ST | ✓ | ✓ | - | - | - | - | - | - | - |
| OWNER | ✓ | ✓ | - | ✓ | ✓ | ✓ | ✓ | - | ✓ |
| PLAYER | - | ✓ | - | - | - | - | - | - | - |
| OBSERVER | - | ✓ | - | - | - | - | - | - | - |
| AUTHENTICATED | - | - | - | - | - | - | - | - | - |
| ANONYMOUS | - | - | - | - | - | - | - | - | - |

## Status-Based Restrictions

Character status affects which permissions apply:

### Unfinished (`Un`)
- Owner can spend freebies (not XP)
- Owner can edit limited fields
- ST/Admin have full access

### Submitted (`Sub`)
- Owner loses edit/spend permissions
- Only Head ST/Admin can edit
- Awaiting approval

### Approved (`App`)
- Owner can spend XP (not freebies)
- Owner can edit limited fields
- ST/Admin have full access

### Retired (`Ret`)
- Owner cannot make changes
- ST/Admin can still edit

### Deceased (`Dec`)
- Read-only for all except ST/Admin
- ST/Admin can still edit

## Visibility Tiers

Three-tier visibility system for object data:

1. **FULL** - All data visible (owner, ST, admin)
2. **PARTIAL** - Limited public data (players, observers)
3. **NONE** - No access (strangers)

## Integration Points

### View Mixins

```python
from core.mixins import (
    ViewPermissionMixin,      # Requires VIEW_FULL
    EditPermissionMixin,      # Requires EDIT_FULL
    SpendXPPermissionMixin,   # Requires SPEND_XP
    SpendFreebiesPermissionMixin,  # Requires SPEND_FREEBIES
    VisibilityFilterMixin,    # Filters querysets by visibility
    OwnerRequiredMixin,       # Owner or admin only
    STRequiredMixin,          # Chronicle ST or admin only
)
```

### Template Tags

```django
{% load permissions %}

{% user_can_view object as can_view %}
{% user_can_edit object as can_edit %}
{% user_can_spend_xp object as can_spend_xp %}
{% user_has_permission object 'EDIT_LIMITED' as can_edit_notes %}
{% visibility_tier object as tier %}
{% is_owner object as is_obj_owner %}
{% is_st as user_is_st %}
```

### Direct Permission Checks

```python
from core.permissions import Permission, PermissionManager

# Check specific permission
can_edit = PermissionManager.user_has_permission(
    user, character, Permission.EDIT_FULL
)

# Get all user roles for object
roles = PermissionManager.get_user_roles(user, character)

# Filter queryset to visible objects
visible_chars = PermissionManager.filter_queryset_for_user(
    user, Character.objects.all()
)
```

## Security Considerations

1. **Defense in Depth**: Permissions checked at view, queryset, and template levels
2. **Fail Secure**: Unknown permissions default to denied
3. **Status Awareness**: Permission checks respect character lifecycle
4. **Audit Trail**: All permission decisions are deterministic and testable

## Test Coverage

See `core/tests/permissions/test_permission_manager.py` for comprehensive test coverage including:
- Role assignment tests
- Permission matrix verification
- Status-based restriction tests
- Visibility tier tests
- Queryset filtering tests
