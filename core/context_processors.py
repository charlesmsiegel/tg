from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from django.contrib.auth.models import AnonymousUser
from game.models import Scene
from game.security import filter_scenes, readable_chronicles


def all_chronicles(request):
    user = getattr(request, "user", AnonymousUser())
    chronicles = readable_chronicles(user)
    visible_scenes = filter_scenes(
        Scene.objects.filter(finished=False, chronicle__in=chronicles), user
    ).select_related("chronicle")
    by_chronicle = {chronicle.pk: [] for chronicle in chronicles}
    for scene in visible_scenes:
        by_chronicle[scene.chronicle_id].append(scene)
    return {
        "chronicles": chronicles,
        "navigation_chronicles": [
            {"chronicle": chronicle, "scenes": by_chronicle[chronicle.pk]}
            for chronicle in chronicles
        ],
    }


def add_special_user_flag(request):
    return {
        "is_approved_user": getattr(request, "is_approved_user", False),
    }


def permissions(request):
    """
    Add permission helpers to template context.

    Makes the following available in all templates:
    - VisibilityTier: Enum for checking visibility levels
    - Permission: Enum for permission types
    - Role: Enum for user roles
    - user_can_view(obj): Helper function
    - user_can_edit(obj): Helper function

    Usage in template:
        {% if visibility_tier == VisibilityTier.FULL %}
            ...
        {% endif %}
    """
    return {
        "VisibilityTier": VisibilityTier,
        "Permission": Permission,
        "Role": Role,
        "user_can_view": lambda obj: PermissionManager.user_can_view(request.user, obj),
        "user_can_edit": lambda obj: PermissionManager.user_can_edit(request.user, obj),
    }
