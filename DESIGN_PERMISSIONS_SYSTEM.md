# Django Permissions System Design
## World of Darkness Character Management Application

**Version:** 1.1
**Date:** 2025-11-20
**Status:** Design Document - REVISED

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Requirements](#requirements)
3. [Architecture Overview](#architecture-overview)
4. [Role Definitions](#role-definitions)
5. [Permission Matrix](#permission-matrix)
6. [Visibility Tiers](#visibility-tiers)
7. [Object-Level Permission Model](#object-level-permission-model)
8. [Implementation Approach](#implementation-approach)
9. [Django Integration Patterns](#django-integration-patterns)
10. [Query Optimization](#query-optimization)
11. [Testing Strategy](#testing-strategy)
12. [Migration Path](#migration-path)

---

## Executive Summary

This document describes a comprehensive permissions system for controlling access and visibility to objects (Characters, Items, Locations) in the World of Darkness Django application. The system implements fine-grained, role-based access control with multiple visibility tiers, supporting owners, storytellers, admins, players, and observers.

**Key Features:**
- Role-based access control (RBAC) with context-aware roles
- Three-tier visibility system (Full, Partial, None)
- Object-level permissions with efficient querying
- Polymorphic model support
- Chronicle/game-aware permission contexts
- **Restricted owner permissions** - owners cannot directly modify stats, must use XP/freebie spending system
- **Hierarchical ST structure** - Chronicle Head STs (full control) vs Game STs (read-only)

### Revision Notes (v1.1)

**Critical Changes from Initial Design:**

1. **Owner Permissions Significantly Restricted**
   - Owners can NO LONGER directly edit character stats (e.g., cannot change Strength 3→4)
   - Owners can ONLY: create characters, spend XP/freebies through the spending system, edit notes/journals
   - New permissions: `SPEND_XP` and `SPEND_FREEBIES` separate from general `EDIT` permission

2. **Chronicle ST Hierarchy Clarified**
   - **Chronicle Head ST**: Primary ST with full edit control over all chronicle objects
   - **Game ST**: Subordinate ST for specific games within a chronicle
   - Game STs have FULL VIEW access but NO EDIT permissions (read-only for most objects)
   - Multiple games can exist within one chronicle, each with their own Game STs

3. **Permission Types Expanded**
   - `EDIT` split into `EDIT_FULL` (direct stat modification) and `EDIT_LIMITED` (notes/journals only)
   - Added `SPEND_XP` - for purchasing stat increases via XP system
   - Added `SPEND_FREEBIES` - for allocating freebie points during creation

4. **Status-Based XP/Freebie Restrictions**
   - Unfinished (Un): Can spend freebies, cannot spend XP
   - Approved (App): Can spend XP, cannot spend freebies
   - Submitted/Retired/Deceased: Owner cannot spend either

---

## Requirements

### Functional Requirements

1. **User Groups** - System must distinguish between:
   - Object owner
   - Chronicle storytellers (STs)
   - Game storytellers
   - Site administrators
   - Players in the same chronicle/game
   - Observers (opt-in)
   - Anonymous/other users

2. **Permission Types:**
   - **View** - Ability to see the object
   - **Edit** - Ability to modify the object
   - **Delete** - Ability to remove the object
   - **Approve** - Ability to approve submissions (ST/admin only)

3. **Visibility Granularity:**
   - **Full Access** - Complete object data (owners, STs, admins)
   - **Partial Access** - Limited public information (players, observers)
   - **No Access** - Object completely hidden (unauthorized users)

### Non-Functional Requirements

1. **Performance** - Permission checks must be efficient (< 50ms per check)
2. **Maintainability** - Clear, testable permission logic
3. **Extensibility** - Easy to add new roles or permission types
4. **Security** - Default-deny approach (explicit permissions required)

---

## Architecture Overview

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Request Layer                           │
│  (View receives request + user + object)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 Permission Manager                           │
│  - Determines user's role(s) for object                     │
│  - Evaluates permission rules                               │
│  - Returns permission decision + visibility tier            │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Role      │ │ Permission  │ │ Visibility  │
│ Resolver    │ │   Rules     │ │   Filters   │
└─────────────┘ └─────────────┘ └─────────────┘
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                 │
│  - User/Profile models                                      │
│  - Chronicle/Game models                                    │
│  - Polymorphic object models                                │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

1. **PermissionManager** - Central service for permission checks
2. **RoleResolver** - Determines user roles for a given object
3. **PermissionRules** - Defines role → permission mappings
4. **VisibilityFilter** - Filters object data based on tier
5. **PermissionMixin** - Model mixin for permission methods
6. **PermissionDecorator** - View decorator for access control

---

## Role Definitions

### Role Hierarchy

Roles are **context-specific** - a user may have different roles for different objects.

#### 1. **OWNER**
- **Definition:** User who created/owns the object
- **Determined by:** `object.owner == user` or `object.user == user`
- **Scope:** Single object
- **Inherits from:** None
- **Priority:** Medium (for that object)
- **Special Permissions:** Can spend freebies/XP, edit notes/journals, but CANNOT directly modify stats (e.g., cannot change Strength from 3→4 directly - must go through XP spending system)

#### 2. **ADMIN**
- **Definition:** Site administrator with full privileges
- **Determined by:** `user.is_superuser` or `user.is_staff`
- **Scope:** All objects site-wide
- **Inherits from:** All roles
- **Priority:** Highest (global)

#### 3. **CHRONICLE_HEAD_ST**
- **Definition:** Primary/head storyteller of the chronicle (has full control)
- **Determined by:** `object.chronicle.head_st == user` or `user in object.chronicle.head_storytellers.all()`
- **Scope:** All objects in their chronicle(s)
- **Inherits from:** None
- **Priority:** Highest
- **Permissions:** Full edit access to all characters, items, locations in the chronicle. Can approve, modify stats directly, manage all aspects.

#### 4. **GAME_ST**
- **Definition:** Storyteller for a specific game within a chronicle (subordinate to head ST)
- **Determined by:** `user in object.chronicle.game_storytellers.all()` or via Game model relationship
- **Scope:** Can view all objects in the chronicle
- **Inherits from:** None
- **Priority:** High
- **Permissions:** Can VIEW everything in the chronicle (full visibility), but CANNOT edit most aspects. May have limited edit permissions for game-specific items (scenes, journals, etc.) but not character stats/items/locations.
- **Note:** Multiple games can exist within a single chronicle, each with their own GMs/STs.

#### 5. **PLAYER**
- **Definition:** Player in the same chronicle/game as the object
- **Determined by:** `user.characters.filter(chronicle=object.chronicle).exists()`
- **Scope:** Objects in chronicles they participate in
- **Inherits from:** None
- **Priority:** Medium

#### 6. **OBSERVER**
- **Definition:** User granted explicit observer access
- **Determined by:** `object.observers.filter(user=user).exists()`
- **Scope:** Specific objects they're granted access to
- **Inherits from:** None
- **Priority:** Medium
- **Note:** Opt-in; requires new Observer model

#### 7. **AUTHENTICATED**
- **Definition:** Any logged-in user
- **Determined by:** `user.is_authenticated`
- **Scope:** All objects (but with minimal permissions)
- **Inherits from:** None
- **Priority:** Low

#### 8. **ANONYMOUS**
- **Definition:** Non-authenticated user
- **Determined by:** `not user.is_authenticated`
- **Scope:** Public objects only
- **Inherits from:** None
- **Priority:** Lowest

### Role Priority & Composition

A user may have **multiple roles** for a single object. Permission checks should:
1. Collect all applicable roles
2. For **view** permissions, apply the most permissive rule (union of permissions)
3. For **edit** permissions, check specific permission rules per role

**Example:**
- User Alice owns a character in Chronicle "Dark Nights"
- Alice has roles: [OWNER, PLAYER, AUTHENTICATED]
  - Can view full character sheet
  - Can spend XP/freebies, edit notes
  - CANNOT directly modify stats
- Bob is the head ST of "Dark Nights" chronicle
- Bob has roles: [CHRONICLE_HEAD_ST, AUTHENTICATED]
  - Can view everything, edit everything, approve characters
- Carol is a Game ST for one of the games in "Dark Nights"
- Carol has roles: [GAME_ST, AUTHENTICATED]
  - Can view everything (full visibility)
  - CANNOT edit characters/items/locations (read-only for most objects)
- David is an admin
- David has roles: [ADMIN, AUTHENTICATED]
  - Full access to everything site-wide

---

## Permission Matrix

### Permission Types

| Permission | Description | Allows |
|-----------|-------------|--------|
| `view_full` | View complete object | All fields, including private notes, secrets, XP |
| `view_partial` | View public object data | Name, basic stats, public background |
| `edit_full` | Full modification rights | Update any field, including stats, status, everything |
| `edit_limited` | Limited modification rights | Owner rights: spend XP/freebies, edit notes/journals only |
| `spend_xp` | Spend experience points | Purchase stat increases via XP system |
| `spend_freebies` | Spend freebie points | Allocate freebies during character creation |
| `delete` | Remove object | Permanent deletion |
| `approve` | Approve submissions | Change status from SUB → APP |
| `manage_observers` | Add/remove observers | Grant observer access |

### Role → Permission Mapping

| Role | view_full | view_partial | edit_full | edit_limited | spend_xp | spend_freebies | delete | approve | manage_observers |
|------|-----------|--------------|-----------|--------------|----------|----------------|--------|---------|------------------|
| OWNER | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| ADMIN | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CHRONICLE_HEAD_ST | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓* | ✓ | ✓ |
| GAME_ST | ✓ | ✓ | — | — | — | — | — | — | — |
| PLAYER | — | ✓ | — | — | — | — | — | — | — |
| OBSERVER | — | ✓ | — | — | — | — | — | — | — |
| AUTHENTICATED | — | — | — | — | — | — | — | — | — |
| ANONYMOUS | — | — | — | — | — | — | — | — | — |

**Notes:**
- `✓` = Has permission
- `✓*` = Conditional permission (Chronicle Head ST may not be able to delete certain system objects)
- `—` = No permission
- **OWNER** has very limited edit rights: can spend XP/freebies, edit notes/journals, but CANNOT directly modify stats
- **GAME_ST** has full view access but NO edit permissions (read-only)
- **CHRONICLE_HEAD_ST** has full control over their chronicle
- OWNER cannot approve their own submissions (requires CHRONICLE_HEAD_ST/ADMIN)

### Status-Based Restrictions

Character status affects permissions:

| Status | Owner Can Edit | Owner Can Spend XP/Freebies | Head ST Can Edit | Game ST Can View | Visible to Players |
|--------|----------------|----------------------------|------------------|------------------|-------------------|
| Un (Unfinished) | Limited (notes/journals) | ✓ (freebies only) | ✓ | ✓ (full) | — |
| Sub (Submitted) | — | — | ✓ | ✓ (full) | — |
| App (Approved) | Limited (notes/journals) | ✓ (XP only) | ✓ | ✓ (full) | ✓ (partial) |
| Ret (Retired) | — | — | ✓ | ✓ (full) | ✓ (partial) |
| Dec (Deceased) | — | — | ✓* | ✓ (full) | ✓ (partial) |

**Key Points:**
- **Owner** can NEVER directly edit stats (Strength, Dexterity, etc.) - must use XP spending system
- **Owner** can spend freebies during character creation (Un status)
- **Owner** can spend XP once character is approved (App status)
- **Game ST** has read-only access (full visibility) but cannot edit
- **Chronicle Head ST** can always edit (except deceased characters may be locked*)
- `✓*` = May be configurable to lock deceased characters entirely

---

## Visibility Tiers

### Tier 1: Full Visibility
**Who:** OWNER, ADMIN, CHRONICLE_HEAD_ST, GAME_ST

**Includes:**
- All character attributes, abilities, backgrounds
- Private notes, journals (owner's and ST's)
- Experience points (earned, spent, pending, approval history)
- Secrets, flaws, derangements
- ST notes and approval history
- Complete equipment and inventory
- All relationships and connections
- Freebie point allocation breakdown

**Implementation:** Return complete object serialization

**Note:** GAME_ST receives full visibility for informational purposes but cannot edit most fields (read-only access).

### Tier 2: Partial Visibility
**Who:** PLAYER, OBSERVER

**Includes:**
- Character name, concept, nature, demeanor
- Public physical description
- Visible attributes (not hidden)
- Known abilities (public skills)
- Public backgrounds (not "Secret")
- Basic equipment (not magical/hidden items)
- Public relationships

**Excludes:**
- XP totals and expenditures
- Private notes, secrets
- Hidden flaws/merits
- ST notes
- Exact freebie point allocation
- Private backgrounds (e.g., Secret Society)

**Implementation:** Return filtered object with subset of fields

### Tier 3: No Visibility
**Who:** AUTHENTICATED (without other roles), ANONYMOUS

**Includes:** Nothing - object appears as if it doesn't exist

**Implementation:**
- List views: Exclude from queryset
- Detail views: Return 404 (not 403, to avoid information leakage)

### Configurable Visibility

Each object should support optional visibility settings:

```python
class VisibilitySettings:
    PUBLIC = 'PUB'      # Partial visibility to all authenticated users
    PRIVATE = 'PRI'     # Only owner/STs/admins
    CHRONICLE = 'CHR'   # Only chronicle members (players)
    CUSTOM = 'CUS'      # Custom observer list
```

Owner/ST can set this to control baseline visibility before role-based rules apply.

---

## Object-Level Permission Model

### Database Schema

#### 1. Observer Model (New)

```python
class Observer(models.Model):
    """Grants specific users observer access to an object."""

    # Polymorphic reference to any object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Who can observe
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observing')

    # Metadata
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [['content_type', 'object_id', 'user']]
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]
```

#### 2. PermissionMixin (Add to existing models)

```python
class PermissionMixin(models.Model):
    """Mixin for permission-controlled objects."""

    visibility = models.CharField(
        max_length=3,
        choices=[
            ('PUB', 'Public'),
            ('PRI', 'Private'),
            ('CHR', 'Chronicle Only'),
            ('CUS', 'Custom'),
        ],
        default='PRI',
    )

    # Generic relation to observers
    observers = GenericRelation('core.Observer')

    class Meta:
        abstract = True

    def get_user_roles(self, user):
        """Returns list of roles user has for this object."""
        # Implemented by PermissionManager
        pass

    def user_can_view(self, user):
        """Check if user can view this object at all."""
        pass

    def user_can_edit(self, user):
        """Check if user can edit this object."""
        pass

    def get_visibility_tier(self, user):
        """Returns 'full', 'partial', or 'none'."""
        pass
```

#### 3. Chronicle Updates

```python
# Add to existing Chronicle model
class Chronicle(Model):
    # ... existing fields ...

    # Head storyteller (primary ST with full control)
    # Option 1: Single head ST
    head_st = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chronicles_as_head_st',
        help_text="Primary storyteller with full chronicle control"
    )

    # Option 2: Multiple head STs (if preferred)
    # head_storytellers = models.ManyToManyField(
    #     User,
    #     related_name='chronicles_as_head_st',
    #     blank=True,
    #     help_text="Primary storytellers with full chronicle control"
    # )

    # Game storytellers (subordinate STs with view-only access)
    game_storytellers = models.ManyToManyField(
        User,
        related_name='chronicles_as_game_st',
        blank=True,
        help_text="Game STs can view all chronicle data but cannot edit most objects"
    )

    # Add players helper property
    @property
    def players(self):
        """Returns queryset of Users with characters in this chronicle."""
        return User.objects.filter(
            characters__chronicle=self
        ).distinct()

    # Helper methods
    def is_head_st(self, user):
        """Check if user is head ST of this chronicle."""
        if hasattr(self, 'head_st'):
            return self.head_st == user
        elif hasattr(self, 'head_storytellers'):
            return self.head_storytellers.filter(id=user.id).exists()
        return False

    def is_game_st(self, user):
        """Check if user is a game ST in this chronicle."""
        return self.game_storytellers.filter(id=user.id).exists()
```

---

## Implementation Approach

### Phase 1: Core Permission Infrastructure

#### Step 1.1: Create Permission Manager Service

**File:** `core/permissions.py`

```python
from typing import List, Set, Literal
from enum import Enum
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class Role(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    CHRONICLE_HEAD_ST = "chronicle_head_st"
    GAME_ST = "game_st"
    PLAYER = "player"
    OBSERVER = "observer"
    AUTHENTICATED = "authenticated"
    ANONYMOUS = "anonymous"

class VisibilityTier(Enum):
    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"

class Permission(Enum):
    VIEW_FULL = "view_full"
    VIEW_PARTIAL = "view_partial"
    EDIT_FULL = "edit_full"
    EDIT_LIMITED = "edit_limited"
    SPEND_XP = "spend_xp"
    SPEND_FREEBIES = "spend_freebies"
    DELETE = "delete"
    APPROVE = "approve"
    MANAGE_OBSERVERS = "manage_observers"

class PermissionManager:
    """Central service for all permission checks."""

    # Permission matrix: Role -> Set of Permissions
    ROLE_PERMISSIONS = {
        Role.OWNER: {
            Permission.VIEW_FULL,
            Permission.VIEW_PARTIAL,
            Permission.EDIT_LIMITED,  # Can edit notes/journals only
            Permission.SPEND_XP,
            Permission.SPEND_FREEBIES,
            Permission.DELETE,
            Permission.MANAGE_OBSERVERS,
        },
        Role.ADMIN: {
            Permission.VIEW_FULL,
            Permission.VIEW_PARTIAL,
            Permission.EDIT_FULL,
            Permission.EDIT_LIMITED,
            Permission.SPEND_XP,
            Permission.SPEND_FREEBIES,
            Permission.DELETE,
            Permission.APPROVE,
            Permission.MANAGE_OBSERVERS,
        },
        Role.CHRONICLE_HEAD_ST: {
            Permission.VIEW_FULL,
            Permission.VIEW_PARTIAL,
            Permission.EDIT_FULL,  # Can edit everything
            Permission.EDIT_LIMITED,
            Permission.SPEND_XP,
            Permission.SPEND_FREEBIES,
            Permission.DELETE,
            Permission.APPROVE,
            Permission.MANAGE_OBSERVERS,
        },
        Role.GAME_ST: {
            Permission.VIEW_FULL,  # Full view access
            Permission.VIEW_PARTIAL,
            # No edit permissions - read-only
        },
        Role.PLAYER: {
            Permission.VIEW_PARTIAL,
        },
        Role.OBSERVER: {
            Permission.VIEW_PARTIAL,
        },
        Role.AUTHENTICATED: set(),
        Role.ANONYMOUS: set(),
    }

    @staticmethod
    def get_user_roles(user: User, obj) -> Set[Role]:
        """
        Determine all roles the user has for this object.

        Args:
            user: Django User instance
            obj: Object to check permissions for (Character, Item, etc.)

        Returns:
            Set of Role enums
        """
        roles = set()

        # Anonymous check
        if not user.is_authenticated:
            roles.add(Role.ANONYMOUS)
            return roles

        # All authenticated users get this role
        roles.add(Role.AUTHENTICATED)

        # Admin check
        if user.is_superuser or user.is_staff:
            roles.add(Role.ADMIN)

        # Owner check
        if hasattr(obj, 'owner') and obj.owner == user:
            roles.add(Role.OWNER)
        elif hasattr(obj, 'user') and obj.user == user:
            roles.add(Role.OWNER)

        # Chronicle Head ST check
        if hasattr(obj, 'chronicle') and obj.chronicle:
            # Check if user is head ST of the chronicle
            if hasattr(obj.chronicle, 'head_st') and obj.chronicle.head_st == user:
                roles.add(Role.CHRONICLE_HEAD_ST)
            elif hasattr(obj.chronicle, 'head_storytellers'):
                if obj.chronicle.head_storytellers.filter(id=user.id).exists():
                    roles.add(Role.CHRONICLE_HEAD_ST)

            # Check if user is a game ST in the chronicle
            if hasattr(obj.chronicle, 'game_storytellers'):
                if obj.chronicle.game_storytellers.filter(id=user.id).exists():
                    roles.add(Role.GAME_ST)

            # Player check - user has a character in same chronicle
            if user.characters.filter(chronicle=obj.chronicle).exists():
                roles.add(Role.PLAYER)

        # Observer check (uses generic relation)
        if hasattr(obj, 'observers'):
            ct = ContentType.objects.get_for_model(obj)
            from core.models import Observer
            if Observer.objects.filter(
                content_type=ct,
                object_id=obj.id,
                user=user
            ).exists():
                roles.add(Role.OBSERVER)

        return roles

    @staticmethod
    def user_has_permission(
        user: User,
        obj,
        permission: Permission,
        status_aware: bool = True
    ) -> bool:
        """
        Check if user has a specific permission for an object.

        Args:
            user: Django User
            obj: Object to check
            permission: Permission enum to check
            status_aware: Whether to apply status-based restrictions

        Returns:
            Boolean permission result
        """
        roles = PermissionManager.get_user_roles(user, obj)

        # Collect all permissions from all roles (union)
        user_permissions = set()
        for role in roles:
            user_permissions.update(
                PermissionManager.ROLE_PERMISSIONS.get(role, set())
            )

        # Check base permission
        if permission not in user_permissions:
            return False

        # Apply status-based restrictions for characters
        if status_aware and hasattr(obj, 'status'):
            return PermissionManager._check_status_restrictions(
                user, obj, permission, roles
            )

        return True

    @staticmethod
    def _check_status_restrictions(
        user: User,
        obj,
        permission: Permission,
        roles: Set[Role]
    ) -> bool:
        """Apply status-based permission restrictions."""
        status = obj.status

        # Deceased characters are read-only for everyone except admins and head STs
        if status == 'Dec':
            if permission in [Permission.EDIT_FULL, Permission.EDIT_LIMITED,
                            Permission.DELETE, Permission.SPEND_XP]:
                return (Role.ADMIN in roles or
                       Role.CHRONICLE_HEAD_ST in roles)

        # Submitted characters: owners have no permissions, only head ST/admin
        if status == 'Sub':
            if permission in [Permission.EDIT_LIMITED, Permission.SPEND_XP,
                            Permission.SPEND_FREEBIES]:
                if Role.OWNER in roles:
                    return False
                return (Role.CHRONICLE_HEAD_ST in roles or
                       Role.ADMIN in roles)

        # Unfinished: Owner can spend freebies only (not XP yet)
        if status == 'Un':
            if permission == Permission.SPEND_XP and Role.OWNER in roles:
                # Can't spend XP until approved
                return False
            if permission == Permission.SPEND_FREEBIES:
                return True

        # Approved: Owner can spend XP (not freebies) and edit limited fields
        if status == 'App':
            if permission == Permission.SPEND_FREEBIES and Role.OWNER in roles:
                # Can't spend freebies after approval
                return False
            if permission in [Permission.SPEND_XP, Permission.EDIT_LIMITED]:
                return True

        # Retired: Owner cannot make any changes
        if status == 'Ret':
            if permission in [Permission.EDIT_LIMITED, Permission.SPEND_XP,
                            Permission.SPEND_FREEBIES]:
                if Role.OWNER in roles:
                    return False

        return True

    @staticmethod
    def get_visibility_tier(user: User, obj) -> VisibilityTier:
        """
        Determine what visibility tier user has for object.

        Returns:
            VisibilityTier enum
        """
        # Check if user can view at all
        if not PermissionManager.user_can_view(user, obj):
            return VisibilityTier.NONE

        # Check if user has full access
        if PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_FULL
        ):
            return VisibilityTier.FULL

        # Check if user has partial access
        if PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_PARTIAL
        ):
            return VisibilityTier.PARTIAL

        return VisibilityTier.NONE

    @staticmethod
    def user_can_view(user: User, obj) -> bool:
        """Simplified view check."""
        return PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_FULL
        ) or PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_PARTIAL
        )

    @staticmethod
    def user_can_edit(user: User, obj) -> bool:
        """
        Simplified edit check.
        Returns True if user has EDIT_FULL permission.
        For limited editing (owner), use user_has_permission(EDIT_LIMITED).
        """
        return PermissionManager.user_has_permission(
            user, obj, Permission.EDIT_FULL
        )

    @staticmethod
    def user_can_spend_xp(user: User, obj) -> bool:
        """Check if user can spend XP on this object."""
        return PermissionManager.user_has_permission(
            user, obj, Permission.SPEND_XP
        )

    @staticmethod
    def user_can_spend_freebies(user: User, obj) -> bool:
        """Check if user can spend freebie points on this object."""
        return PermissionManager.user_has_permission(
            user, obj, Permission.SPEND_FREEBIES
        )

    @staticmethod
    def filter_queryset_for_user(user: User, queryset):
        """
        Filter queryset to only objects user can view.

        This is complex and requires careful Q() object construction.
        See "Query Optimization" section.
        """
        from django.db.models import Q
        from django.contrib.contenttypes.models import ContentType

        if not user.is_authenticated:
            # Anonymous users see nothing (or only PUBLIC visibility)
            return queryset.filter(visibility='PUB')

        # Admins see everything
        if user.is_superuser or user.is_staff:
            return queryset

        # Build complex Q object
        filters = Q()

        # Objects user owns
        if queryset.model._meta.get_field('owner'):
            filters |= Q(owner=user)

        # Objects in chronicles where user is head ST
        if hasattr(queryset.model, 'chronicle'):
            filters |= Q(chronicle__head_st=user)
            # Or if using M2M for head storytellers
            if hasattr(queryset.model, 'chronicle__head_storytellers'):
                filters |= Q(chronicle__head_storytellers=user)

        # Objects in chronicles where user is game ST (can view all)
        if hasattr(queryset.model, 'chronicle'):
            if hasattr(queryset.model, 'chronicle__game_storytellers'):
                filters |= Q(chronicle__game_storytellers=user)

        # Objects in chronicles user plays in
        if hasattr(queryset.model, 'chronicle'):
            # User has a character in the chronicle
            filters |= Q(
                chronicle__character__user=user,
                status='App'  # Only show approved characters to players
            )

        # Objects user is explicitly observing
        ct = ContentType.objects.get_for_model(queryset.model)
        observer_ids = Observer.objects.filter(
            content_type=ct,
            user=user
        ).values_list('object_id', flat=True)
        filters |= Q(id__in=observer_ids)

        return queryset.filter(filters).distinct()
```

#### Step 1.2: Add Permission Mixin to Models

**File:** `core/models.py`

```python
from django.contrib.contenttypes.fields import GenericRelation
from core.permissions import PermissionManager, VisibilityTier

class PermissionMixin(models.Model):
    """Add to Character, ItemModel, LocationModel."""

    visibility = models.CharField(
        max_length=3,
        choices=[
            ('PUB', 'Public'),
            ('PRI', 'Private'),
            ('CHR', 'Chronicle Only'),
            ('CUS', 'Custom'),
        ],
        default='PRI',
        help_text="Controls baseline visibility"
    )

    # Generic relation for observers
    observers = GenericRelation(
        'Observer',
        related_query_name='%(class)s'
    )

    class Meta:
        abstract = True

    def get_user_roles(self, user):
        """Get all roles user has for this object."""
        return PermissionManager.get_user_roles(user, self)

    def user_can_view(self, user):
        """Check if user can view this object."""
        return PermissionManager.user_can_view(user, self)

    def user_can_edit(self, user):
        """Check if user can edit this object."""
        return PermissionManager.user_can_edit(user, self)

    def get_visibility_tier(self, user):
        """Get visibility tier for user."""
        return PermissionManager.get_visibility_tier(user, self)

    def add_observer(self, user, granted_by):
        """Grant observer access to a user."""
        from core.models import Observer
        Observer.objects.get_or_create(
            content_object=self,
            user=user,
            defaults={'granted_by': granted_by}
        )

    def remove_observer(self, user):
        """Remove observer access."""
        self.observers.filter(user=user).delete()
```

#### Step 1.3: Create Observer Model

**File:** `core/models.py`

```python
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Observer(Model):
    """
    Grants specific users observer access to any object.
    Uses generic foreign key to support Characters, Items, Locations, etc.
    """

    # Generic FK to any object
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Who can observe
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='observing'
    )

    # Metadata
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='granted_observer_access'
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [['content_type', 'object_id', 'user']]
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]
        verbose_name = "Observer"
        verbose_name_plural = "Observers"

    def __str__(self):
        return f"{self.user.username} observing {self.content_object}"
```

### Phase 2: View Integration

#### Step 2.1: Permission Decorators

**File:** `core/decorators.py`

```python
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import Http404
from core.permissions import Permission, PermissionManager

def require_permission(permission: Permission, lookup='pk', raise_404=True):
    """
    Decorator for views requiring specific permission.

    Args:
        permission: Permission enum required
        lookup: How to lookup object (default 'pk')
        raise_404: If True, raise 404 instead of 403 for unauthorized

    Usage:
        @require_permission(Permission.EDIT)
        def update_character(request, pk):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get object
            obj_id = kwargs.get(lookup)
            model_class = get_model_for_view(view_func)
            obj = get_object_or_404(model_class, pk=obj_id)

            # Check permission
            if not PermissionManager.user_has_permission(
                request.user, obj, permission
            ):
                if raise_404:
                    raise Http404("Object not found")
                else:
                    raise PermissionDenied("You don't have permission")

            # Attach object to request for convenience
            request.permission_object = obj

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_view_permission(view_func):
    """Shortcut for view permission."""
    return require_permission(Permission.VIEW_FULL, raise_404=True)(view_func)

def require_edit_permission(view_func):
    """Shortcut for edit permission."""
    return require_permission(Permission.EDIT, raise_404=False)(view_func)
```

#### Step 2.2: Class-Based View Mixin

**File:** `core/mixins.py`

```python
from django.core.exceptions import PermissionDenied
from django.http import Http404
from core.permissions import Permission, PermissionManager, VisibilityTier

class PermissionRequiredMixin:
    """Mixin for CBVs requiring permission checks."""

    required_permission = None  # Set in subclass
    raise_404_on_deny = True

    def dispatch(self, request, *args, **kwargs):
        """Check permissions before dispatching."""
        if not self.has_permission():
            if self.raise_404_on_deny:
                raise Http404("Object not found")
            else:
                raise PermissionDenied("Insufficient permissions")
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        """Override to implement permission logic."""
        obj = self.get_object()
        return PermissionManager.user_has_permission(
            self.request.user,
            obj,
            self.required_permission
        )

class ViewPermissionMixin(PermissionRequiredMixin):
    """Require view permission."""
    required_permission = Permission.VIEW_FULL
    raise_404_on_deny = True

class EditPermissionMixin(PermissionRequiredMixin):
    """Require edit permission."""
    required_permission = Permission.EDIT
    raise_404_on_deny = False

class VisibilityFilterMixin:
    """Mixin to filter querysets by user permissions."""

    def get_queryset(self):
        """Filter queryset to only viewable objects."""
        qs = super().get_queryset()
        return PermissionManager.filter_queryset_for_user(
            self.request.user,
            qs
        )

    def get_context_data(self, **kwargs):
        """Add visibility tier to context."""
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'object') and self.object:
            context['visibility_tier'] = PermissionManager.get_visibility_tier(
                self.request.user,
                self.object
            )
            context['user_can_edit'] = PermissionManager.user_can_edit(
                self.request.user,
                self.object
            )
        return context
```

### Phase 3: Template Integration

#### Step 3.1: Context Processor

**File:** `core/context_processors.py`

```python
from core.permissions import VisibilityTier

def permissions(request):
    """Add permission helpers to template context."""
    return {
        'VisibilityTier': VisibilityTier,
        'user_can_view': lambda obj: obj.user_can_view(request.user),
        'user_can_edit': lambda obj: obj.user_can_edit(request.user),
    }
```

**Add to settings.py:**
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... existing ...
                'core.context_processors.permissions',
            ],
        },
    },
]
```

#### Step 3.2: Template Tags

**File:** `core/templatetags/permissions.py`

```python
from django import template
from core.permissions import PermissionManager, VisibilityTier

register = template.Library()

@register.simple_tag(takes_context=True)
def user_can_view(context, obj):
    """Check if current user can view object."""
    user = context['request'].user
    return obj.user_can_view(user)

@register.simple_tag(takes_context=True)
def user_can_edit(context, obj):
    """Check if current user can edit object."""
    user = context['request'].user
    return obj.user_can_edit(user)

@register.simple_tag(takes_context=True)
def visibility_tier(context, obj):
    """Get visibility tier for current user."""
    user = context['request'].user
    return obj.get_visibility_tier(user)

@register.filter
def is_full(tier):
    """Check if tier is FULL."""
    return tier == VisibilityTier.FULL

@register.filter
def is_partial(tier):
    """Check if tier is PARTIAL."""
    return tier == VisibilityTier.PARTIAL
```

#### Step 3.3: Template Usage

```html
{% load permissions %}

{# In detail view #}
{% visibility_tier object as tier %}

{% if tier|is_full %}
    {# Show complete character sheet #}
    <div class="tg-card">
        <div class="tg-card-header">
            <h6>Private Notes</h6>
        </div>
        <div class="tg-card-body">
            {{ object.notes|sanitize_html }}
        </div>
    </div>

    <div class="tg-card">
        <div class="tg-card-header">
            <h6>Experience Points</h6>
        </div>
        <div class="tg-card-body">
            <p>Total XP: {{ object.xp }}</p>
            <p>Spent XP: {{ object.spent_xp }}</p>
        </div>
    </div>
{% elif tier|is_partial %}
    {# Show limited character sheet #}
    <div class="tg-card">
        <div class="tg-card-header">
            <h6>Public Information</h6>
        </div>
        <div class="tg-card-body">
            <p><strong>Name:</strong> {{ object.name }}</p>
            <p><strong>Concept:</strong> {{ object.concept }}</p>
        </div>
    </div>
{% else %}
    {# This shouldn't render if permissions work correctly #}
    <p>You don't have access to view this character.</p>
{% endif %}

{# Edit button #}
{% if user_can_edit object %}
    <a href="{% url 'characters:update' object.pk %}" class="btn btn-primary">
        Edit Character
    </a>
{% endif %}
```

### Phase 4: Visibility Filtering

#### Step 4.1: Serializer/Form Filtering

**File:** `core/serializers.py`

```python
from rest_framework import serializers
from core.permissions import VisibilityTier

class VisibilityAwareSerializer(serializers.ModelSerializer):
    """Base serializer that respects visibility tiers."""

    # Define field sets for each tier
    FULL_FIELDS = []  # All fields
    PARTIAL_FIELDS = []  # Public fields only

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get visibility tier from context
        request = self.context.get('request')
        instance = self.instance

        if request and instance:
            tier = instance.get_visibility_tier(request.user)

            if tier == VisibilityTier.PARTIAL:
                # Remove fields not in PARTIAL_FIELDS
                allowed = set(self.PARTIAL_FIELDS)
                for field_name in list(self.fields.keys()):
                    if field_name not in allowed:
                        self.fields.pop(field_name)
            elif tier == VisibilityTier.NONE:
                # Shouldn't happen, but clear all fields
                self.fields.clear()

class CharacterSerializer(VisibilityAwareSerializer):
    """Example character serializer."""

    FULL_FIELDS = [
        'id', 'name', 'player', 'chronicle', 'concept', 'nature',
        'demeanor', 'essence', 'attributes', 'abilities', 'backgrounds',
        'willpower', 'derangements', 'flaws', 'merits', 'notes',
        'xp', 'spent_xp', 'freebies', 'status'
    ]

    PARTIAL_FIELDS = [
        'id', 'name', 'concept', 'nature', 'demeanor', 'essence',
        'attributes', 'abilities'  # Could filter specific abilities too
    ]

    class Meta:
        model = Character
        fields = FULL_FIELDS
```

---

## Django Integration Patterns

### Pattern 1: DetailView with Permissions

```python
from django.views.generic import DetailView
from core.mixins import ViewPermissionMixin, VisibilityFilterMixin

class CharacterDetailView(ViewPermissionMixin, VisibilityFilterMixin, DetailView):
    model = Character
    template_name = 'characters/character/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # visibility_tier already added by VisibilityFilterMixin
        # user_can_edit already added by VisibilityFilterMixin
        return context
```

### Pattern 2: ListView with Filtering

```python
from django.views.generic import ListView
from core.mixins import VisibilityFilterMixin

class CharacterListView(VisibilityFilterMixin, ListView):
    model = Character
    template_name = 'characters/character/list.html'

    # get_queryset() automatically filtered by VisibilityFilterMixin
```

### Pattern 3: UpdateView with Permissions

```python
from django.views.generic import UpdateView
from core.mixins import EditPermissionMixin

class CharacterUpdateView(EditPermissionMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = 'characters/character/update.html'

    def form_valid(self, form):
        # Additional status checks could go here
        return super().form_valid(form)
```

### Pattern 4: Function-Based View

```python
from django.shortcuts import render, get_object_or_404
from core.decorators import require_edit_permission

@require_edit_permission
def update_character(request, pk):
    # Object automatically loaded and checked by decorator
    character = request.permission_object

    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect('characters:detail', pk=pk)
    else:
        form = CharacterForm(instance=character)

    return render(request, 'characters/character/update.html', {
        'form': form,
        'character': character,
    })
```

### Pattern 5: API ViewSet

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import PermissionManager, Permission

class ObjectPermission(permissions.BasePermission):
    """DRF permission class using our PermissionManager."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return PermissionManager.user_can_view(request.user, obj)
        else:
            return PermissionManager.user_can_edit(request.user, obj)

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated, ObjectPermission]

    def get_queryset(self):
        """Filter to viewable objects."""
        return PermissionManager.filter_queryset_for_user(
            self.request.user,
            super().get_queryset()
        )
```

---

## Query Optimization

### Challenge: N+1 Queries

Permission checks can cause N+1 query problems if not careful:

```python
# BAD: Causes N queries for chronicle lookups
for character in Character.objects.all():
    if character.user_can_view(request.user):  # Queries chronicle each time
        print(character.name)

# GOOD: Prefetch related data
characters = Character.objects.select_related(
    'owner',
    'chronicle'
).prefetch_related(
    'chronicle__storytellers',
    'observers'
)
for character in characters:
    if character.user_can_view(request.user):  # No additional queries
        print(character.name)
```

### Optimized filter_queryset_for_user

```python
@staticmethod
def filter_queryset_for_user(user: User, queryset):
    """
    Optimized queryset filtering with minimal queries.
    """
    if not user.is_authenticated:
        # Anonymous users only see public objects
        return queryset.filter(visibility='PUB')

    # Admins see everything
    if user.is_superuser or user.is_staff:
        return queryset.select_related('owner', 'chronicle').prefetch_related(
            'chronicle__storytellers',
            'observers'
        )

    # Build complex filter
    from django.db.models import Q, Exists, OuterRef
    from django.contrib.contenttypes.models import ContentType

    model_class = queryset.model
    ct = ContentType.objects.get_for_model(model_class)

    # Subquery for observer check
    observer_subquery = Observer.objects.filter(
        content_type=ct,
        object_id=OuterRef('pk'),
        user=user
    )

    # Build Q filters
    filters = Q()

    # Owner check
    if hasattr(model_class, 'owner'):
        filters |= Q(owner=user)

    # Chronicle ST check
    if hasattr(model_class, 'chronicle'):
        filters |= Q(chronicle__storytellers=user)

        # Player check - has character in same chronicle
        from characters.models import Character
        player_chronicle_subquery = Character.objects.filter(
            user=user,
            chronicle=OuterRef('chronicle'),
            status='App'
        )
        filters |= Q(Exists(player_chronicle_subquery))

    # Observer check using subquery
    filters |= Q(Exists(observer_subquery))

    # Apply filters with optimized select/prefetch
    return queryset.filter(filters).select_related(
        'owner',
        'chronicle'
    ).prefetch_related(
        'chronicle__storytellers',
        'observers'
    ).distinct()
```

### Caching Strategy

For expensive permission checks on frequently accessed objects:

```python
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType

class PermissionManager:

    @staticmethod
    def get_cache_key(user_id, obj, permission):
        """Generate cache key for permission check."""
        ct = ContentType.objects.get_for_model(obj)
        return f"perm:{user_id}:{ct.id}:{obj.id}:{permission.value}"

    @staticmethod
    def user_has_permission_cached(user, obj, permission, ttl=300):
        """
        Cached permission check.

        Args:
            ttl: Cache time-to-live in seconds (default 5 min)
        """
        cache_key = PermissionManager.get_cache_key(user.id, obj, permission)

        # Try cache first
        result = cache.get(cache_key)
        if result is not None:
            return result

        # Compute and cache
        result = PermissionManager.user_has_permission(user, obj, permission)
        cache.set(cache_key, result, ttl)
        return result

    @staticmethod
    def invalidate_cache(obj):
        """Invalidate all cached permissions for an object."""
        # This is expensive - consider using cache versioning instead
        ct = ContentType.objects.get_for_model(obj)
        pattern = f"perm:*:{ct.id}:{obj.id}:*"
        # Note: Cache clearing by pattern requires Redis or similar
        cache.delete_pattern(pattern)
```

### Database Indexes

**Migration to add indexes:**

```python
class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # Index on Character.chronicle for filtering
        migrations.AddIndex(
            model_name='character',
            index=models.Index(fields=['chronicle'], name='char_chronicle_idx'),
        ),

        # Index on Character.owner for filtering
        migrations.AddIndex(
            model_name='character',
            index=models.Index(fields=['owner'], name='char_owner_idx'),
        ),

        # Composite index for status + chronicle (common filter)
        migrations.AddIndex(
            model_name='character',
            index=models.Index(
                fields=['status', 'chronicle'],
                name='char_status_chron_idx'
            ),
        ),

        # Observer indexes already defined in model
    ]
```

---

## Testing Strategy

### Unit Tests

**File:** `core/tests/test_permissions.py`

```python
import pytest
from django.contrib.auth.models import User
from core.permissions import PermissionManager, Permission, Role, VisibilityTier
from characters.models import Character
from game.models import Chronicle

@pytest.mark.django_db
class TestPermissionManager:

    @pytest.fixture
    def users(self):
        """Create test users."""
        return {
            'owner': User.objects.create_user('owner', 'owner@test.com'),
            'head_st': User.objects.create_user('head_st', 'head_st@test.com'),
            'game_st': User.objects.create_user('game_st', 'game_st@test.com'),
            'player': User.objects.create_user('player', 'player@test.com'),
            'observer': User.objects.create_user('observer', 'observer@test.com'),
            'stranger': User.objects.create_user('stranger', 'stranger@test.com'),
            'admin': User.objects.create_user(
                'admin', 'admin@test.com', is_staff=True
            ),
        }

    @pytest.fixture
    def chronicle(self, users):
        """Create test chronicle."""
        chron = Chronicle.objects.create(
            name="Test Chronicle",
            head_st=users['head_st']  # Set head ST
        )
        # Add game ST
        chron.game_storytellers.add(users['game_st'])
        return chron

    @pytest.fixture
    def character(self, users, chronicle):
        """Create test character."""
        char = Character.objects.create(
            name="Test Character",
            owner=users['owner'],
            chronicle=chronicle,
            status='App'
        )

        # Add observer
        char.add_observer(users['observer'], users['owner'])

        # Add player character to chronicle
        Character.objects.create(
            name="Player's Character",
            owner=users['player'],
            chronicle=chronicle,
            status='App'
        )

        return char

    def test_role_detection_owner(self, users, character):
        """Test that owner role is detected."""
        roles = PermissionManager.get_user_roles(users['owner'], character)
        assert Role.OWNER in roles

    def test_role_detection_head_st(self, users, character):
        """Test that chronicle head ST role is detected."""
        roles = PermissionManager.get_user_roles(users['head_st'], character)
        assert Role.CHRONICLE_HEAD_ST in roles

    def test_role_detection_game_st(self, users, character):
        """Test that game ST role is detected."""
        roles = PermissionManager.get_user_roles(users['game_st'], character)
        assert Role.GAME_ST in roles

    def test_role_detection_player(self, users, character):
        """Test that player role is detected."""
        roles = PermissionManager.get_user_roles(users['player'], character)
        assert Role.PLAYER in roles

    def test_role_detection_observer(self, users, character):
        """Test that observer role is detected."""
        roles = PermissionManager.get_user_roles(users['observer'], character)
        assert Role.OBSERVER in roles

    def test_role_detection_stranger(self, users, character):
        """Test that stranger has no special roles."""
        roles = PermissionManager.get_user_roles(users['stranger'], character)
        assert Role.OWNER not in roles
        assert Role.CHRONICLE_HEAD_ST not in roles
        assert Role.GAME_ST not in roles
        assert Role.PLAYER not in roles
        assert Role.OBSERVER not in roles
        assert Role.AUTHENTICATED in roles

    def test_owner_can_view_full(self, users, character):
        """Test owner has full view permission."""
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.VIEW_FULL
        )

    def test_owner_cannot_edit_full(self, users, character):
        """Test owner does NOT have full edit permission."""
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_FULL
        )

    def test_owner_can_edit_limited(self, users, character):
        """Test owner has limited edit permission (notes/journals)."""
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_LIMITED
        )

    def test_owner_can_spend_xp_when_approved(self, users, character):
        """Test owner can spend XP on approved character."""
        character.status = 'App'
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )

    def test_owner_cannot_spend_xp_when_unfinished(self, users, character):
        """Test owner cannot spend XP on unfinished character."""
        character.status = 'Un'
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )

    def test_owner_can_spend_freebies_when_unfinished(self, users, character):
        """Test owner can spend freebies on unfinished character."""
        character.status = 'Un'
        assert PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_FREEBIES
        )

    def test_head_st_can_view_full(self, users, character):
        """Test head ST has full view permission."""
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.VIEW_FULL
        )

    def test_head_st_can_edit_full(self, users, character):
        """Test head ST has full edit permission."""
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.EDIT_FULL
        )

    def test_game_st_can_view_full(self, users, character):
        """Test game ST has full view permission."""
        assert PermissionManager.user_has_permission(
            users['game_st'], character, Permission.VIEW_FULL
        )

    def test_game_st_cannot_edit(self, users, character):
        """Test game ST does NOT have edit permission (read-only)."""
        assert not PermissionManager.user_has_permission(
            users['game_st'], character, Permission.EDIT_FULL
        )
        assert not PermissionManager.user_has_permission(
            users['game_st'], character, Permission.EDIT_LIMITED
        )

    def test_head_st_can_approve(self, users, character):
        """Test head ST has approve permission."""
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.APPROVE
        )

    def test_player_can_view_partial(self, users, character):
        """Test player has partial view permission."""
        assert PermissionManager.user_has_permission(
            users['player'], character, Permission.VIEW_PARTIAL
        )

    def test_player_cannot_view_full(self, users, character):
        """Test player does NOT have full view permission."""
        assert not PermissionManager.user_has_permission(
            users['player'], character, Permission.VIEW_FULL
        )

    def test_player_cannot_edit(self, users, character):
        """Test player cannot edit."""
        assert not PermissionManager.user_has_permission(
            users['player'], character, Permission.EDIT_FULL
        )
        assert not PermissionManager.user_has_permission(
            users['player'], character, Permission.EDIT_LIMITED
        )

    def test_observer_can_view_partial(self, users, character):
        """Test observer has partial view permission."""
        assert PermissionManager.user_has_permission(
            users['observer'], character, Permission.VIEW_PARTIAL
        )

    def test_stranger_cannot_view(self, users, character):
        """Test stranger has no view permission."""
        assert not PermissionManager.user_has_permission(
            users['stranger'], character, Permission.VIEW_FULL
        )
        assert not PermissionManager.user_has_permission(
            users['stranger'], character, Permission.VIEW_PARTIAL
        )

    def test_admin_can_do_everything(self, users, character):
        """Test admin has all permissions."""
        admin = users['admin']
        assert PermissionManager.user_has_permission(
            admin, character, Permission.VIEW_FULL
        )
        assert PermissionManager.user_has_permission(
            admin, character, Permission.EDIT_FULL
        )
        assert PermissionManager.user_has_permission(
            admin, character, Permission.DELETE
        )
        assert PermissionManager.user_has_permission(
            admin, character, Permission.APPROVE
        )

    def test_visibility_tier_owner(self, users, character):
        """Test owner gets FULL visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['owner'], character)
        assert tier == VisibilityTier.FULL

    def test_visibility_tier_game_st(self, users, character):
        """Test game ST gets FULL visibility tier (but can't edit)."""
        tier = PermissionManager.get_visibility_tier(users['game_st'], character)
        assert tier == VisibilityTier.FULL

    def test_visibility_tier_player(self, users, character):
        """Test player gets PARTIAL visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['player'], character)
        assert tier == VisibilityTier.PARTIAL

    def test_visibility_tier_stranger(self, users, character):
        """Test stranger gets NONE visibility tier."""
        tier = PermissionManager.get_visibility_tier(users['stranger'], character)
        assert tier == VisibilityTier.NONE

    def test_status_restriction_submitted(self, users, character):
        """Test owner cannot spend XP/freebies on submitted character."""
        character.status = 'Sub'
        character.save()

        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_FREEBIES
        )

        # But head ST still can
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.EDIT_FULL
        )

    def test_status_restriction_deceased(self, users, character):
        """Test owner cannot edit deceased character, but head ST and admin can."""
        character.status = 'Dec'
        character.save()

        # Owner cannot edit
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.SPEND_XP
        )
        assert not PermissionManager.user_has_permission(
            users['owner'], character, Permission.EDIT_LIMITED
        )

        # Head ST can still edit (configurable)
        assert PermissionManager.user_has_permission(
            users['head_st'], character, Permission.EDIT_FULL
        )

        # Admin can still edit
        assert PermissionManager.user_has_permission(
            users['admin'], character, Permission.EDIT_FULL
        )
```

### Integration Tests

**File:** `core/tests/test_permission_views.py`

```python
import pytest
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
class TestPermissionViews:

    @pytest.fixture
    def client(self):
        return Client()

    def test_detail_view_as_owner(self, client, users, character):
        """Test owner can view detail page."""
        client.force_login(users['owner'])
        response = client.get(
            reverse('characters:detail', kwargs={'pk': character.pk})
        )
        assert response.status_code == 200
        assert 'Private Notes' in response.content.decode()

    def test_detail_view_as_player(self, client, users, character):
        """Test player sees partial view."""
        client.force_login(users['player'])
        response = client.get(
            reverse('characters:detail', kwargs={'pk': character.pk})
        )
        assert response.status_code == 200
        assert 'Public Information' in response.content.decode()
        assert 'Private Notes' not in response.content.decode()

    def test_detail_view_as_stranger(self, client, users, character):
        """Test stranger gets 404."""
        client.force_login(users['stranger'])
        response = client.get(
            reverse('characters:detail', kwargs={'pk': character.pk})
        )
        assert response.status_code == 404

    def test_edit_view_as_owner(self, client, users, character):
        """Test owner can access edit page."""
        client.force_login(users['owner'])
        response = client.get(
            reverse('characters:update', kwargs={'pk': character.pk})
        )
        assert response.status_code == 200

    def test_edit_view_as_player(self, client, users, character):
        """Test player cannot access edit page."""
        client.force_login(users['player'])
        response = client.get(
            reverse('characters:update', kwargs={'pk': character.pk})
        )
        assert response.status_code == 403

    def test_list_view_filtering(self, client, users, chronicle):
        """Test list view only shows permitted characters."""
        # Create multiple characters
        char1 = Character.objects.create(
            name="Char 1", owner=users['owner'], chronicle=chronicle
        )
        char2 = Character.objects.create(
            name="Char 2", owner=users['stranger'], chronicle=chronicle
        )

        client.force_login(users['player'])
        response = client.get(reverse('characters:list'))

        content = response.content.decode()
        # Player's own character should appear
        # Char1 should appear (same chronicle)
        # Char2 should appear (same chronicle)
        assert 'Char 1' in content
        assert 'Char 2' in content
```

### Performance Tests

```python
import pytest
from django.test.utils import override_settings
from django.db import connection
from django.test.utils import CaptureQueriesContext

@pytest.mark.django_db
class TestPermissionPerformance:

    def test_queryset_filtering_query_count(self, users, chronicle):
        """Test that filtering doesn't cause N+1 queries."""
        # Create 50 characters
        for i in range(50):
            Character.objects.create(
                name=f"Char {i}",
                owner=users['owner'],
                chronicle=chronicle
            )

        with CaptureQueriesContext(connection) as context:
            qs = Character.objects.all()
            filtered = PermissionManager.filter_queryset_for_user(
                users['player'], qs
            )
            list(filtered)  # Force evaluation

        # Should be constant queries regardless of character count
        # Exact number depends on implementation, but < 10 is good
        assert len(context.captured_queries) < 10

    def test_permission_check_performance(self, users, character):
        """Test that permission check is fast."""
        import time

        start = time.time()
        for _ in range(100):
            PermissionManager.user_has_permission(
                users['owner'], character, Permission.VIEW_FULL
            )
        end = time.time()

        # 100 checks should take < 100ms
        assert (end - start) < 0.1
```

---

## Migration Path

### Phase 1: Foundation (Week 1)
1. Create `Observer` model
2. Create `PermissionManager` service
3. Create `PermissionMixin`
4. Write unit tests for core permission logic
5. Add migrations

### Phase 2: Model Integration (Week 2)
1. Add `PermissionMixin` to `Character` model
2. Add `PermissionMixin` to `ItemModel`
3. Add `PermissionMixin` to `LocationModel`
4. Update `Chronicle` to have explicit `storytellers` M2M
5. Create database indexes
6. Run migrations on development environment

### Phase 3: View Integration (Week 3)
1. Create view mixins and decorators
2. Update `CharacterDetailView` to use permissions
3. Update `CharacterListView` to filter by permissions
4. Update `CharacterUpdateView` to check permissions
5. Add integration tests

### Phase 4: Template Integration (Week 4)
1. Create template tags and context processors
2. Update character detail templates to use visibility tiers
3. Update item/location templates
4. Add visual indicators for permission levels

### Phase 5: Observer System (Week 5)
1. Create observer management views
2. Add "Add Observer" button to detail pages
3. Create observer list page
4. Add notifications for observer grants

### Phase 6: Testing & Optimization (Week 6)
1. Write comprehensive test suite
2. Performance testing and optimization
3. Add caching where needed
4. Documentation for developers

### Phase 7: Rollout (Week 7)
1. Deploy to staging environment
2. User acceptance testing
3. Fix bugs and edge cases
4. Deploy to production
5. Monitor for issues

---

## Migration Script Example

**File:** `core/migrations/0002_add_permissions.py`

```python
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        # Create Observer model
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('object_id', models.PositiveIntegerField()),
                ('granted_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
                ('content_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='contenttypes.contenttype'
                )),
                ('granted_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='granted_observer_access',
                    to=settings.AUTH_USER_MODEL
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='observing',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Observer',
                'verbose_name_plural': 'Observers',
            },
        ),

        # Add unique constraint
        migrations.AddConstraint(
            model_name='observer',
            constraint=models.UniqueConstraint(
                fields=['content_type', 'object_id', 'user'],
                name='unique_observer_per_object'
            ),
        ),

        # Add indexes
        migrations.AddIndex(
            model_name='observer',
            index=models.Index(
                fields=['content_type', 'object_id'],
                name='observer_ct_oid_idx'
            ),
        ),
        migrations.AddIndex(
            model_name='observer',
            index=models.Index(
                fields=['user'],
                name='observer_user_idx'
            ),
        ),
    ]
```

**File:** `characters/migrations/0XXX_add_visibility.py`

```python
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0XXX_previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='visibility',
            field=models.CharField(
                choices=[
                    ('PUB', 'Public'),
                    ('PRI', 'Private'),
                    ('CHR', 'Chronicle Only'),
                    ('CUS', 'Custom')
                ],
                default='PRI',
                help_text='Controls baseline visibility',
                max_length=3
            ),
        ),
    ]
```

---

## Summary

This permissions system provides:

1. **Flexible Role-Based Access** - Context-aware roles that change per object
2. **Fine-Grained Visibility** - Three-tier system (Full, Partial, None)
3. **Performance** - Optimized queries with select_related/prefetch_related
4. **Extensibility** - Easy to add new roles, permissions, or visibility tiers
5. **Security** - Default-deny with explicit permission grants
6. **Django Integration** - Mixins, decorators, template tags for easy use
7. **Testability** - Clear separation of concerns, comprehensive test coverage

The system integrates seamlessly with existing WoD models (Character, Chronicle, etc.) and provides a consistent permission model across all object types.

---

## Next Steps

1. Review this design document with the team
2. Identify any edge cases or special requirements
3. Create implementation tasks/tickets
4. Begin Phase 1 implementation
5. Set up continuous testing during development

---

## Appendix: Configuration Reference

### Settings.py

```python
# Permission system settings
PERMISSION_CACHE_TTL = 300  # 5 minutes
PERMISSION_DEFAULT_VISIBILITY = 'PRI'  # Private by default
PERMISSION_ALLOW_OWNER_DELETION = True
PERMISSION_STATUS_RESTRICTIONS = True  # Enable status-based restrictions
```

### Environment Variables

```bash
# .env
PERMISSION_CACHE_ENABLED=true
PERMISSION_CACHE_BACKEND=redis
```

---

**Document End**
