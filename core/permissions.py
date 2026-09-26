"""
Permission management system for World of Darkness application.

Provides role-based access control with fine-grained permissions for
characters, items, locations, and other game objects.
"""

from enum import Enum

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db.models import OuterRef, Q


class Role(Enum):
    """User roles for permission checks."""

    OWNER = "owner"
    ADMIN = "admin"
    CHRONICLE_HEAD_ST = "chronicle_head_st"
    CHRONICLE_ST_VIEW = "chronicle_st_view"
    CHRONICLE_ST = "chronicle_st"
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
        Role.CHRONICLE_ST_VIEW: {
            Permission.VIEW_FULL,
            Permission.VIEW_PARTIAL,
        },
        Role.CHRONICLE_ST: {
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
    def invalidate_request_cache(request):
        """Call after membership/observer/ST writes before checking again.

        Owner and status are live inputs, not cached facts. A new request
        always starts fresh; nothing is stored globally or on ORM instances.
        """
        for name in (
            "_tg_permission_facts",
            "_tg_role_cache",
            "_tg_permission_snapshots",
            "_tg_scoped_role_cache",
            "_tg_permission_subjects",
        ):
            request.__dict__.pop(name, None)

    @staticmethod
    def _user_key(user):
        return (user.pk, bool(user.is_authenticated), bool(user.is_staff), bool(user.is_superuser))

    @staticmethod
    def _request_facts(user, request):
        """Five set-based reads, shared by every object on this request."""
        from characters.models.core.character import Character
        from core.models import Observer
        from game.models import Chronicle, STRelationship

        cache = request.__dict__.setdefault("_tg_permission_facts", {})
        key = PermissionManager._user_key(user)
        if key not in cache:
            cache[key] = {
                "head": set(Chronicle.objects.filter(head_st=user).values_list("pk", flat=True)),
                "game": set(
                    Chronicle.objects.filter(game_storytellers=user).values_list("pk", flat=True)
                ),
                "st": set(
                    STRelationship.objects.filter(user=user).values_list(
                        "chronicle_id", "gameline__name"
                    )
                ),
                "player": set(
                    Character.objects.filter(owner=user)
                    .exclude(chronicle=None)
                    .values_list("chronicle_id", flat=True)
                ),
                "observer": set(
                    Observer.objects.filter(user=user).values_list(
                        "content_type__app_label", "content_type__model", "object_id"
                    )
                ),
            }
        return cache[key]

    @staticmethod
    def _roles_from_facts(user, chronicle_id, gameline, facts):
        roles = {Role.AUTHENTICATED}
        if user.is_staff or user.is_superuser:
            roles.add(Role.ADMIN)
        if chronicle_id is not None:
            if chronicle_id in facts["head"]:
                roles.add(Role.CHRONICLE_HEAD_ST)
            if chronicle_id in facts["game"]:
                roles.add(Role.GAME_ST)
            if any(pk == chronicle_id for pk, _ in facts["st"]):
                roles.add(Role.CHRONICLE_ST_VIEW)
            name = settings.GAMELINES.get(gameline, {}).get("name")
            if name and (chronicle_id, name) in facts["st"]:
                roles.add(Role.CHRONICLE_ST)
        return roles

    @staticmethod
    def permission_subject(obj):
        """Do not mistake reverse inheritance links for record subjects."""
        from core.models import Model

        return obj if isinstance(obj, Model) else getattr(obj, "character", None) or obj

    @staticmethod
    def _real_subject(obj, request=None):
        """Resolve a base polymorphic row once; concrete rows need no fetch."""
        if not hasattr(obj, "get_real_instance_class") or obj.pk is None:
            return obj
        key = (obj._meta.label_lower, obj.pk)
        cache = (
            request.__dict__.setdefault("_tg_permission_subjects", {})
            if request is not None
            else {}
        )
        if key not in cache:
            cache[key] = (
                obj if obj.get_real_instance_class() is type(obj) else obj.get_real_instance()
            )
        # A caller can mutate a base row without saving it. Resolve its type,
        # but retain those live permission inputs rather than a stale DB copy.
        if type(cache[key]) is type(obj):
            return obj
        from copy import copy

        resolved = copy(cache[key])
        for name in ("owner_id", "user_id", "chronicle_id", "status", "gameline", "npc"):
            if name in obj.__dict__:
                setattr(resolved, name, obj.__dict__[name])
        return resolved

    @staticmethod
    def can_manage_scope(user, chronicle, gameline, request=None):
        """Whether a user can mutate a chronicle and gameline pair."""
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        roles = PermissionManager.get_scoped_roles(user, chronicle, gameline, request=request)
        return bool(roles & {Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST})

    @staticmethod
    def can_manage_chronicle(user, chronicle, request=None):
        """Chronicle-wide actions have no gameline and require its head ST."""
        if not user.is_authenticated:
            return False
        return bool(
            user.is_staff
            or user.is_superuser
            or (chronicle is not None and chronicle.head_st_id == user.pk)
        )

    @staticmethod
    def user_has_scoped_editor_role(user, obj, request=None):
        """Choose ST-only form fields without treating a draft owner as an ST."""
        return bool(
            PermissionManager.get_user_roles(user, obj, request=request)
            & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST}
        )

    @staticmethod
    def user_can_manage_creation(user, form, request=None):
        """Derive creation-page ST controls from the selected chronicle scope."""
        from game.models import Chronicle  # deferred: circular import

        value = None
        if form.is_bound:
            value = form.data.get(form.add_prefix("chronicle"))
        if not value and request is not None:
            value = request.GET.get("chronicle")
        if not value:
            value = form.initial.get("chronicle")
        if hasattr(value, "pk"):
            chronicle = value
        else:
            try:
                chronicle = Chronicle.objects.filter(pk=value).first() if value else None
            except (TypeError, ValueError):
                chronicle = None
        instance = getattr(form, "instance", None)
        if instance is None:
            model = getattr(getattr(form, "_meta", None), "model", None)
            instance = model() if model is not None else None
        gameline = getattr(instance, "gameline", None)
        if (
            not isinstance(gameline, str)
            and instance is not None
            and hasattr(instance, "get_gameline")
        ):
            gameline = instance.get_gameline()
        return PermissionManager.can_manage_scope(
            user, chronicle, gameline if isinstance(gameline, str) else None, request
        )

    @staticmethod
    def get_scoped_roles(user: User, chronicle, gameline, request=None) -> set[Role]:
        """Resolve ST roles once per request for a chronicle and gameline."""
        if not user.is_authenticated:
            return {Role.ANONYMOUS}
        if request is not None:
            return PermissionManager._roles_from_facts(
                user,
                getattr(chronicle, "pk", None),
                gameline,
                PermissionManager._request_facts(user, request),
            )
        roles = {Role.AUTHENTICATED}
        if user.is_staff or user.is_superuser:
            roles.add(Role.ADMIN)
        if chronicle is not None:
            if chronicle.head_st_id == user.pk:
                roles.add(Role.CHRONICLE_HEAD_ST)
            if chronicle.game_storytellers.filter(pk=user.pk).exists():
                roles.add(Role.GAME_ST)

            from game.models import STRelationship  # deferred: circular import

            relationships = list(
                STRelationship.objects.filter(
                    user_id=user.pk, chronicle_id=chronicle.pk
                ).select_related("gameline")
            )
            if relationships:
                roles.add(Role.CHRONICLE_ST_VIEW)
                name = settings.GAMELINES.get(gameline, {}).get("name")
                if name and any(
                    relation.gameline and relation.gameline.name == name
                    for relation in relationships
                ):
                    roles.add(Role.CHRONICLE_ST)

        return roles

    @staticmethod
    def get_user_roles(user: User, obj, request=None) -> set[Role]:
        """
        Determine all roles the user has for this object.

        Args:
            user: Django User instance
            obj: Object to check permissions for (Character, Item, etc.)

        Returns:
            Set of Role enums
        """
        if not user.is_authenticated:
            return {Role.ANONYMOUS}
        scope_obj = PermissionManager._real_subject(
            PermissionManager.permission_subject(obj), request
        )
        gameline = getattr(scope_obj, "gameline", None)
        if not isinstance(gameline, str) and hasattr(scope_obj, "get_gameline"):
            gameline = scope_obj.get_gameline()
        if not isinstance(gameline, str):
            gameline = None
        chronicle_id = getattr(obj, "chronicle_id", getattr(scope_obj, "chronicle_id", None))
        owner_id = getattr(obj, "owner_id", None)
        if owner_id is None and not hasattr(obj, "owner_id"):
            owner_id = getattr(getattr(obj, "owner", None), "pk", None)
        user_id = getattr(obj, "user_id", None)
        if user_id is None and not hasattr(obj, "user_id"):
            user_id = getattr(getattr(obj, "user", None), "pk", None)

        if request is not None:
            facts = PermissionManager._request_facts(user, request)
            key = (
                PermissionManager._user_key(user),
                getattr(getattr(obj, "_meta", None), "label_lower", type(obj)),
                getattr(obj, "pk", None) if getattr(obj, "pk", None) is not None else id(obj),
                owner_id,
                user_id,
                chronicle_id,
                gameline,
            )
            cache = request.__dict__.setdefault("_tg_role_cache", {})
            if key not in cache:
                roles = PermissionManager._roles_from_facts(user, chronicle_id, gameline, facts)
                if owner_id == user.pk or user_id == user.pk:
                    roles.add(Role.OWNER)
                if chronicle_id is not None and chronicle_id in facts["player"]:
                    roles.add(Role.PLAYER)
                if (
                    hasattr(obj, "observers")
                    and (scope_obj._meta.app_label, scope_obj._meta.model_name, obj.pk)
                    in facts["observer"]
                ):
                    roles.add(Role.OBSERVER)
                cache[key] = frozenset(roles)
            return set(cache[key])

        chronicle = getattr(obj, "chronicle", None) or getattr(scope_obj, "chronicle", None)
        roles = PermissionManager.get_scoped_roles(user, chronicle, gameline)
        if owner_id == user.pk or user_id == user.pk:
            roles.add(Role.OWNER)
        if chronicle is not None:
            from characters.models.core.character import Character

            if Character.objects.filter(owner=user, chronicle=chronicle).exists():
                roles.add(Role.PLAYER)
        if hasattr(obj, "observers") and scope_obj.observers.filter(user=user).exists():
            roles.add(Role.OBSERVER)
        return roles

    @staticmethod
    def user_has_permission(
        user: User, obj, permission: Permission, status_aware: bool = True, request=None
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
        roles = PermissionManager.get_user_roles(user, obj, request=request)

        if (
            permission == Permission.EDIT_FULL
            and Role.OWNER in roles
            and getattr(obj, "status", None) in {"Un", "Rev"}
        ):
            return True

        # Collect all permissions from all roles (union)
        user_permissions = set()
        for role in roles:
            user_permissions.update(PermissionManager.ROLE_PERMISSIONS.get(role, set()))

        # Check base permission
        if permission not in user_permissions:
            return False

        # Apply status-based restrictions for characters
        if status_aware and hasattr(obj, "status"):
            return PermissionManager._check_status_restrictions(user, obj, permission, roles)

        return True

    @staticmethod
    def _check_status_restrictions(
        user: User, obj, permission: Permission, roles: set[Role]
    ) -> bool:
        """Apply status-based permission restrictions."""
        status = obj.status
        scoped_editor = bool(roles & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST})
        if Role.OWNER in roles and not scoped_editor:
            if permission in {
                Permission.EDIT_LIMITED,
                Permission.DELETE,
                Permission.SPEND_FREEBIES,
            } and status not in {"Un", "Rev"}:
                return False
            if permission == Permission.SPEND_XP and status != "App":
                return False

        # Deceased characters are read-only for everyone except admins and head STs
        if status == "Dec":
            if permission in [
                Permission.EDIT_FULL,
                Permission.EDIT_LIMITED,
                Permission.DELETE,
                Permission.SPEND_XP,
            ]:
                return bool(roles & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST})

        # Submitted characters: owners have no permissions, only head ST/admin
        if status == "Sub":
            if permission in [
                Permission.EDIT_LIMITED,
                Permission.SPEND_XP,
                Permission.SPEND_FREEBIES,
            ]:
                return bool(roles & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST})

        # Unfinished: Owner can spend freebies only (not XP yet)
        if status == "Un":
            if (
                permission == Permission.SPEND_XP
                and Role.OWNER in roles
                and not roles & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST}
            ):
                # Can't spend XP until approved
                return False
            if permission == Permission.SPEND_FREEBIES:
                return True

        # Approved: Owner can spend XP (not freebies) and edit limited fields
        if status == "App":
            if (
                permission in {Permission.SPEND_FREEBIES, Permission.EDIT_LIMITED}
                and Role.OWNER in roles
                and not roles & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST}
            ):
                # Can't spend freebies after approval
                return False
            if permission == Permission.SPEND_XP:
                return True

        # Retired: Owner cannot make any changes
        if status == "Ret":
            if permission in [
                Permission.EDIT_LIMITED,
                Permission.SPEND_XP,
                Permission.SPEND_FREEBIES,
            ]:
                if Role.OWNER in roles and not roles & {
                    Role.ADMIN,
                    Role.CHRONICLE_HEAD_ST,
                    Role.CHRONICLE_ST,
                }:
                    return False

        return True

    @staticmethod
    def get_visibility_tier(user: User, obj, request=None) -> VisibilityTier:
        """
        Determine what visibility tier user has for object.

        Returns:
            VisibilityTier enum
        """
        # Check if user can view at all
        if not PermissionManager.user_can_view(user, obj, request=request):
            return VisibilityTier.NONE

        # Check if user has full access
        if PermissionManager.user_has_permission(user, obj, Permission.VIEW_FULL, request=request):
            return VisibilityTier.FULL

        # Check if user has partial access
        if PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_PARTIAL, request=request
        ):
            return VisibilityTier.PARTIAL

        return VisibilityTier.NONE

    @staticmethod
    def user_can_view(user: User, obj, request=None) -> bool:
        """Simplified view check."""
        return PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_FULL, request=request
        ) or PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_PARTIAL, request=request
        )

    @staticmethod
    def user_can_edit(user: User, obj, request=None) -> bool:
        """
        Simplified edit check.
        Returns True if user has EDIT_FULL permission.
        For limited editing (owner), use user_has_permission(EDIT_LIMITED).
        """
        return PermissionManager.user_has_permission(
            user, obj, Permission.EDIT_FULL, request=request
        )

    @staticmethod
    def user_can_spend_xp(user: User, obj, request=None) -> bool:
        """Check if user can spend XP on this object."""
        return PermissionManager.user_has_permission(
            user, obj, Permission.SPEND_XP, request=request
        )

    @staticmethod
    def user_can_spend_freebies(user: User, obj, request=None) -> bool:
        """Check if user can spend freebie points on this object."""
        return PermissionManager.user_has_permission(
            user, obj, Permission.SPEND_FREEBIES, request=request
        )

    def check_permission(self, user: User, obj, permission: str) -> bool:
        """
        Check if user has a specific permission for an object.

        This is a convenience method that accepts string permission names
        and converts them to Permission enums.

        Args:
            user: Django User instance
            obj: Object to check permissions for
            permission: Permission name as string (e.g., "view_full", "edit_full")

        Returns:
            Boolean permission result
        """
        # Convert string to Permission enum
        try:
            perm_enum = Permission(permission)
        except ValueError:
            # Try uppercase version
            try:
                perm_enum = Permission[permission.upper()]
            except KeyError:
                return False

        return PermissionManager.user_has_permission(user, obj, perm_enum)

    @staticmethod
    def _model_has_field(model, field_name: str) -> bool:
        """
        Check if model has a specific field.

        Args:
            model: Django model class
            field_name: Name of the field to check

        Returns:
            True if field exists, False otherwise
        """
        try:
            model._meta.get_field(field_name)
            return True
        except FieldDoesNotExist:
            return False

    @staticmethod
    def _get_chronicle_related_model(queryset):
        """
        Get the Chronicle model from a queryset's chronicle foreign key.

        Args:
            queryset: QuerySet to check

        Returns:
            Chronicle model class or None if no chronicle field exists
        """
        try:
            chronicle_field = queryset.model._meta.get_field("chronicle")
            return chronicle_field.related_model
        except FieldDoesNotExist:
            return None

    @staticmethod
    def _build_owner_filter(user: User, model) -> Q:
        """
        Build Q filter for objects owned by user.

        Args:
            user: Django User instance
            model: Model class to check

        Returns:
            Q object or empty Q() if no owner field
        """
        filters = Q(pk__in=[])
        for field in ("owner", "user"):
            if PermissionManager._model_has_field(model, field):
                filters |= Q(**{field: user})
        return filters

    @staticmethod
    def _build_chronicle_st_filters(user: User, chronicle_model) -> Q:
        """
        Build Q filters for chronicle storyteller relationships.

        Args:
            user: Django User instance
            chronicle_model: Chronicle model class

        Returns:
            Q object with all chronicle ST filters combined
        """
        filters = Q()

        # Head ST (ForeignKey)
        if PermissionManager._model_has_field(chronicle_model, "head_st"):
            filters |= Q(chronicle__head_st=user)

        # Game storytellers (M2M)
        if PermissionManager._model_has_field(chronicle_model, "game_storytellers"):
            filters |= Q(chronicle__game_storytellers=user)

        # Every assigned ST may read full objects in their chronicle, even
        # when their gameline assignment does not permit mutation.
        if PermissionManager._model_has_field(chronicle_model, "storytellers"):
            filters |= Q(chronicle__st_relationships__user=user)

        return filters

    @staticmethod
    def filter_queryset_for_user(user: User, queryset):
        """Filter private VIEW_FULL/VIEW_PARTIAL audiences, not public cards.

        SQL mirrors the role predicates; fixture matrices pin their parity.
        Observer subqueries correlate content type as well as object identity.
        """
        # Full/partial legacy querysets never render the public projection.
        # Anonymous public cards are handled by the route policy instead.
        if not user.is_authenticated:
            return queryset.none()

        # Admins see everything
        if user.is_superuser or user.is_staff:
            return queryset

        model = queryset.model

        # Build Q-based filters for owner and ST access (these are efficient joins)
        filters = Q(pk__in=[])

        # 1. Objects user owns
        filters |= PermissionManager._build_owner_filter(user, model)

        # 2. Chronicle storyteller access
        chronicle_model = PermissionManager._get_chronicle_related_model(queryset)
        if chronicle_model:
            filters |= PermissionManager._build_chronicle_st_filters(user, chronicle_model)

        # 3. Player chronicle access - fetch IDs once, then use pk__in
        if PermissionManager._model_has_field(model, "chronicle"):
            from characters.models import Character

            # PLAYER is based on any owned character in the chronicle.
            player_chronicle_ids = list(
                Character.objects.filter(owner=user)
                .exclude(chronicle__isnull=True)
                .values_list("chronicle_id", flat=True)
            )
            if player_chronicle_ids:
                filters |= Q(chronicle_id__in=player_chronicle_ids)

        # A generic relation's identity is (content type, PK), not PK alone.
        # Polymorphic rows carry their concrete type even in a base queryset.
        if PermissionManager._model_has_field(model, "observers"):
            from core.models import Observer

            content_type = (
                OuterRef("polymorphic_ctype_id")
                if PermissionManager._model_has_field(model, "polymorphic_ctype")
                else ContentType.objects.get_for_model(model).pk
            )
            filters |= Q(
                pk__in=Observer.objects.filter(
                    user=user,
                    content_type_id=content_type,
                ).values("object_id")
            )

        return queryset.filter(filters).distinct()
