"""
Permission management system for World of Darkness application.

Provides role-based access control with fine-grained permissions for
characters, items, locations, and other game objects.
"""

from enum import Enum
from typing import Set

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, OuterRef, Q


class Role(Enum):
    """User roles for permission checks."""

    OWNER = "owner"
    ADMIN = "admin"
    CHRONICLE_HEAD_ST = "chronicle_head_st"
    GAME_ST = "game_st"
    PLAYER = "player"
    OBSERVER = "observer"
    AUTHENTICATED = "authenticated"
    ANONYMOUS = "anonymous"


class VisibilityTier(Enum):
    """Visibility levels for object data."""

    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"


class Permission(Enum):
    """Specific permissions that can be granted."""

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
        if hasattr(obj, "owner") and obj.owner == user:
            roles.add(Role.OWNER)
        elif hasattr(obj, "user") and obj.user == user:
            roles.add(Role.OWNER)
        elif hasattr(obj, "owned_by") and obj.owned_by and hasattr(obj.owned_by, "owner") and obj.owned_by.owner == user:
            # For locations/items owned through characters
            roles.add(Role.OWNER)

        # Chronicle Head ST check
        if hasattr(obj, "chronicle") and obj.chronicle:
            # Check if user is head ST of the chronicle
            if hasattr(obj.chronicle, "head_st") and obj.chronicle.head_st == user:
                roles.add(Role.CHRONICLE_HEAD_ST)
            elif hasattr(obj.chronicle, "head_storytellers"):
                if obj.chronicle.head_storytellers.filter(id=user.id).exists():
                    roles.add(Role.CHRONICLE_HEAD_ST)

            # Check if user is a game ST in the chronicle
            if hasattr(obj.chronicle, "game_storytellers"):
                if obj.chronicle.game_storytellers.filter(id=user.id).exists():
                    roles.add(Role.GAME_ST)

            # Player check - user has a character in same chronicle
            if hasattr(user, "characters"):
                if user.characters.filter(chronicle=obj.chronicle).exists():
                    roles.add(Role.PLAYER)

        # Observer check (uses generic relation)
        if hasattr(obj, "observers"):
            ct = ContentType.objects.get_for_model(obj)
            from core.models import Observer

            if Observer.objects.filter(
                content_type=ct, object_id=obj.id, user=user
            ).exists():
                roles.add(Role.OBSERVER)

        return roles

    @staticmethod
    def user_has_permission(
        user: User, obj, permission: Permission, status_aware: bool = True
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
            user_permissions.update(PermissionManager.ROLE_PERMISSIONS.get(role, set()))

        # Check base permission
        if permission not in user_permissions:
            return False

        # Apply status-based restrictions for characters
        if status_aware and hasattr(obj, "status"):
            return PermissionManager._check_status_restrictions(
                user, obj, permission, roles
            )

        return True

    @staticmethod
    def _check_status_restrictions(
        user: User, obj, permission: Permission, roles: Set[Role]
    ) -> bool:
        """Apply status-based permission restrictions."""
        status = obj.status

        # Deceased characters are read-only for everyone except admins and head STs
        if status == "Dec":
            if permission in [
                Permission.EDIT_FULL,
                Permission.EDIT_LIMITED,
                Permission.DELETE,
                Permission.SPEND_XP,
            ]:
                return Role.ADMIN in roles or Role.CHRONICLE_HEAD_ST in roles

        # Submitted characters: owners have no permissions, only head ST/admin
        if status == "Sub":
            if permission in [
                Permission.EDIT_LIMITED,
                Permission.SPEND_XP,
                Permission.SPEND_FREEBIES,
            ]:
                if Role.OWNER in roles:
                    return False
                return Role.CHRONICLE_HEAD_ST in roles or Role.ADMIN in roles

        # Unfinished: Owner can spend freebies only (not XP yet)
        if status == "Un":
            if permission == Permission.SPEND_XP and Role.OWNER in roles:
                # Can't spend XP until approved
                return False
            if permission == Permission.SPEND_FREEBIES:
                return True

        # Approved: Owner can spend XP (not freebies) and edit limited fields
        if status == "App":
            if permission == Permission.SPEND_FREEBIES and Role.OWNER in roles:
                # Can't spend freebies after approval
                return False
            if permission in [Permission.SPEND_XP, Permission.EDIT_LIMITED]:
                return True

        # Retired: Owner cannot make any changes
        if status == "Ret":
            if permission in [
                Permission.EDIT_LIMITED,
                Permission.SPEND_XP,
                Permission.SPEND_FREEBIES,
            ]:
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
        if PermissionManager.user_has_permission(user, obj, Permission.VIEW_FULL):
            return VisibilityTier.FULL

        # Check if user has partial access
        if PermissionManager.user_has_permission(user, obj, Permission.VIEW_PARTIAL):
            return VisibilityTier.PARTIAL

        return VisibilityTier.NONE

    @staticmethod
    def user_can_view(user: User, obj) -> bool:
        """Simplified view check."""
        return PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_FULL
        ) or PermissionManager.user_has_permission(user, obj, Permission.VIEW_PARTIAL)

    @staticmethod
    def user_can_edit(user: User, obj) -> bool:
        """
        Simplified edit check.
        Returns True if user has EDIT_FULL permission.
        For limited editing (owner), use user_has_permission(EDIT_LIMITED).
        """
        return PermissionManager.user_has_permission(user, obj, Permission.EDIT_FULL)

    @staticmethod
    def user_can_spend_xp(user: User, obj) -> bool:
        """Check if user can spend XP on this object."""
        return PermissionManager.user_has_permission(user, obj, Permission.SPEND_XP)

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
        Optimized to minimize database queries.

        Args:
            user: Django User instance
            queryset: QuerySet to filter

        Returns:
            Filtered QuerySet
        """
        if not user.is_authenticated:
            # Anonymous users see nothing (or only PUBLIC visibility)
            if hasattr(queryset.model, "visibility"):
                return queryset.filter(visibility="PUB")
            return queryset.none()

        # Admins see everything
        if user.is_superuser or user.is_staff:
            return queryset

        # Build complex Q object
        filters = Q()

        # Objects user owns
        try:
            queryset.model._meta.get_field("owner")
            filters |= Q(owner=user)
        except Exception:
            pass

        # Objects in chronicles where user is head ST
        if hasattr(queryset.model, "chronicle"):
            filters |= Q(chronicle__head_st=user)
            # Or if using M2M for head storytellers
            try:
                if hasattr(queryset.model, "chronicle__head_storytellers"):
                    filters |= Q(chronicle__head_storytellers=user)
            except Exception:
                pass

        # Objects in chronicles where user is game ST (can view all)
        if hasattr(queryset.model, "chronicle"):
            try:
                if hasattr(queryset.model, "chronicle__game_storytellers"):
                    filters |= Q(chronicle__game_storytellers=user)
            except Exception:
                pass

        # Objects in chronicles user plays in
        if hasattr(queryset.model, "chronicle"):
            # User has a character in the chronicle
            from characters.models import Character

            player_chronicle_subquery = Character.objects.filter(
                user=user, chronicle=OuterRef("chronicle"), status="App"
            )
            filters |= Q(Exists(player_chronicle_subquery), status="App")

        # Objects user is explicitly observing
        ct = ContentType.objects.get_for_model(queryset.model)
        from core.models import Observer

        observer_ids = Observer.objects.filter(content_type=ct, user=user).values_list(
            "object_id", flat=True
        )
        filters |= Q(id__in=observer_ids)

        return queryset.filter(filters).distinct()
