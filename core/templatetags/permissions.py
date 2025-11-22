"""
Template tags for permission checks.

Usage in templates:
    {% load permissions %}

    {% if user_can_view object %}
        ...
    {% endif %}

    {% visibility_tier object as tier %}
    {% if tier|is_full %}
        Show full details
    {% elif tier|is_partial %}
        Show partial details
    {% endif %}
"""

from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def user_can_view(context, obj):
    """Check if current user can view object."""
    user = context["request"].user
    return obj.user_can_view(user)


@register.simple_tag(takes_context=True)
def user_can_edit(context, obj):
    """Check if current user can edit object (EDIT_FULL)."""
    user = context["request"].user
    return obj.user_can_edit(user)


@register.simple_tag(takes_context=True)
def user_can_spend_xp(context, obj):
    """Check if current user can spend XP on object."""
    user = context["request"].user
    return obj.user_can_spend_xp(user)


@register.simple_tag(takes_context=True)
def user_can_spend_freebies(context, obj):
    """Check if current user can spend freebies on object."""
    user = context["request"].user
    return obj.user_can_spend_freebies(user)


@register.simple_tag(takes_context=True)
def user_has_permission(context, obj, permission_name):
    """
    Check if user has a specific permission.

    Args:
        obj: Object to check permission for
        permission_name: String name of permission (e.g., 'EDIT_FULL', 'VIEW_PARTIAL')

    Usage:
        {% user_has_permission object 'EDIT_LIMITED' as can_edit_notes %}
        {% if can_edit_notes %}...{% endif %}
    """
    user = context["request"].user
    try:
        permission = Permission[permission_name]
        return PermissionManager.user_has_permission(user, obj, permission)
    except KeyError:
        return False


@register.simple_tag(takes_context=True)
def visibility_tier(context, obj):
    """
    Get visibility tier for current user.

    Usage:
        {% visibility_tier object as tier %}
        {% if tier|is_full %}...{% endif %}
    """
    user = context["request"].user
    return obj.get_visibility_tier(user)


@register.simple_tag(takes_context=True)
def user_roles(context, obj):
    """
    Get all roles user has for object.

    Usage:
        {% user_roles object as roles %}
        {% for role in roles %}
            {{ role.value }}
        {% endfor %}
    """
    user = context["request"].user
    return obj.get_user_roles(user)


@register.filter
def is_full(tier):
    """
    Check if tier is FULL.

    Usage:
        {% if tier|is_full %}...{% endif %}
    """
    return tier == VisibilityTier.FULL


@register.filter
def is_partial(tier):
    """
    Check if tier is PARTIAL.

    Usage:
        {% if tier|is_partial %}...{% endif %}
    """
    return tier == VisibilityTier.PARTIAL


@register.filter
def is_none(tier):
    """
    Check if tier is NONE.

    Usage:
        {% if tier|is_none %}...{% endif %}
    """
    return tier == VisibilityTier.NONE


@register.simple_tag(takes_context=True)
def is_owner(context, obj):
    """Check if current user is owner of object."""
    user = context["request"].user
    if hasattr(obj, "owner"):
        return obj.owner == user
    elif hasattr(obj, "user"):
        return obj.user == user
    return False


@register.simple_tag(takes_context=True)
def is_st(context, obj):
    """Check if current user is ST of object's chronicle."""
    user = context["request"].user

    # Admin check
    if user.is_superuser or user.is_staff:
        return True

    # Chronicle ST check
    if hasattr(obj, "chronicle") and obj.chronicle:
        if hasattr(obj.chronicle, "head_st") and obj.chronicle.head_st == user:
            return True
        if hasattr(obj.chronicle, "head_storytellers"):
            if obj.chronicle.head_storytellers.filter(id=user.id).exists():
                return True

    return False


@register.simple_tag(takes_context=True)
def is_game_st(context, obj):
    """Check if current user is game ST (read-only) of object's chronicle."""
    user = context["request"].user

    if hasattr(obj, "chronicle") and obj.chronicle:
        if hasattr(obj.chronicle, "game_storytellers"):
            return obj.chronicle.game_storytellers.filter(id=user.id).exists()

    return False


@register.inclusion_tag("core/includes/permission_controls.html", takes_context=True)
def permission_controls(context, obj):
    """
    Render permission control buttons for an object.

    Usage:
        {% permission_controls object %}
    """
    user = context["request"].user

    return {
        "object": obj,
        "user": user,
        "can_view": obj.user_can_view(user),
        "can_edit": obj.user_can_edit(user),
        "can_spend_xp": obj.user_can_spend_xp(user),
        "can_spend_freebies": obj.user_can_spend_freebies(user),
        "is_owner": is_owner(context, obj),
        "is_st": is_st(context, obj),
        "visibility_tier": obj.get_visibility_tier(user),
    }
