"""Template capabilities are snapshots of PermissionManager, never authority.

Memberships belong to a request, while owner/status stay live on the object.
New actions extend the central permission matrix; templates consume booleans.
Public projections deliberately do not carry this private-object contract.
"""

from dataclasses import dataclass

from core.permissions import Permission, PermissionManager, Role, VisibilityTier


@dataclass(frozen=True)
class ObjectPermissions:
    can_view_full: bool
    can_view_partial: bool
    can_edit: bool
    can_edit_limited: bool
    can_spend_xp: bool
    can_spend_freebies: bool
    can_approve: bool
    can_approve_spending: bool
    can_delete: bool
    can_manage_observers: bool
    is_owner: bool
    is_chronicle_st: bool
    is_scoped_st: bool
    can_manage_character: bool
    can_chargen: bool
    visibility_tier: VisibilityTier


def permission_subject(obj, request=None):
    """Private character records reflect the linked character's capabilities."""
    return PermissionManager._real_subject(PermissionManager.permission_subject(obj), request)


def get_object_permissions(request, obj):
    from game.spending_approval import can_approve_spending

    obj = permission_subject(obj, request)
    user = request.user
    # Consult the request-cached roles before a snapshot hit: live owner or
    # chronicle changes can change capabilities even when status is unchanged.
    roles = frozenset(PermissionManager.get_user_roles(user, obj, request=request))
    key = (
        PermissionManager._user_key(user),
        obj._meta.label_lower,
        obj.pk if obj.pk is not None else id(obj),
        roles,
        getattr(obj, "status", None),
        getattr(obj, "npc", False),
    )
    cache = request.__dict__.setdefault("_tg_permission_snapshots", {})
    if key not in cache:
        granted = {
            p
            for p in Permission
            if PermissionManager.user_has_permission(user, obj, p, request=request)
        }
        full = Permission.VIEW_FULL in granted
        partial = Permission.VIEW_PARTIAL in granted
        scoped_st = bool(roles & {Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST})
        cache[key] = ObjectPermissions(
            can_view_full=full,
            can_view_partial=partial,
            can_edit=Permission.EDIT_FULL in granted,
            can_edit_limited=Permission.EDIT_LIMITED in granted,
            can_spend_xp=Permission.SPEND_XP in granted,
            can_spend_freebies=Permission.SPEND_FREEBIES in granted,
            can_approve=Permission.APPROVE in granted,
            can_approve_spending=can_approve_spending(user, obj, request=request),
            can_delete=Permission.DELETE in granted,
            can_manage_observers=Permission.MANAGE_OBSERVERS in granted,
            is_owner=Role.OWNER in roles,
            is_chronicle_st=bool(
                roles
                & {Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST_VIEW, Role.CHRONICLE_ST, Role.GAME_ST}
            ),
            is_scoped_st=scoped_st,
            can_manage_character=scoped_st or Role.ADMIN in roles,
            can_chargen=Permission.EDIT_FULL in granted
            and getattr(obj, "status", None) in {"Un", "Rev"},
            visibility_tier=(
                VisibilityTier.FULL
                if full
                else VisibilityTier.PARTIAL if partial else VisibilityTier.NONE
            ),
        )
    return cache[key]


def prepare_permission_objects(request, objects):
    """Warm only a materialized page, including polymorphic linked characters.

    Callers select_related('character') for records. Polymorphic hydration is
    bounded by the number of concrete types, not by the number of rows.
    """
    from collections import defaultdict

    from django.contrib.contenttypes.models import ContentType

    subjects = [PermissionManager.permission_subject(obj) for obj in objects]
    groups = defaultdict(list)
    ContentType.objects.get_for_models(*(type(obj) for obj in subjects))
    for obj in subjects:
        if (
            hasattr(obj, "get_real_instance_class")
            and obj.pk is not None
            and obj.get_real_instance_class() is not type(obj)
        ):
            groups[type(obj)].append(obj)
    cache = request.__dict__.setdefault("_tg_permission_subjects", {})
    for model, rows in groups.items():
        for real in model.objects.all().get_real_instances(rows):
            cache[(model._meta.label_lower, real.pk)] = real
    for obj in objects:
        get_object_permissions(request, obj)


def add_object_permissions(request, context):
    """Idempotent adapter shared by mixins and legacy TemplateResponses."""
    from core.models import Model

    obj = context.get("object")
    if isinstance(obj, Model) or (
        obj is not None
        and hasattr(obj, "_meta")
        and isinstance(PermissionManager.permission_subject(obj), Model)
    ):
        context["object_perms"] = get_object_permissions(request, obj)
    return context
