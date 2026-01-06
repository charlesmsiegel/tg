from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from game.models import Chronicle


def all_chronicles(request):
    return {"chronicles": Chronicle.objects.all()}


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
