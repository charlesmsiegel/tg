"""
Permission decorators for function-based views.
"""

from functools import wraps

from core.permissions import Permission, PermissionManager
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404


def require_permission(permission: Permission, lookup="pk", raise_404=True):
    """
    Decorator for views requiring specific permission.

    Args:
        permission: Permission enum required
        lookup: How to lookup object (default 'pk')
        raise_404: If True, raise 404 instead of 403 for unauthorized

    Usage:
        @require_permission(Permission.EDIT_FULL)
        def update_character(request, pk):
            # Object available as request.permission_object
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get object ID from kwargs
            obj_id = kwargs.get(lookup)

            # Try to get model class from view's attributes or module
            # This is a simplified approach - in practice you might want
            # to pass the model class as a parameter
            model_class = getattr(view_func, "model", None)

            if model_class is None:
                # Try to infer from URL pattern or raise error
                raise ValueError(
                    f"Model class not specified for view {view_func.__name__}. "
                    "Either set view_func.model or pass model_class parameter."
                )

            obj = get_object_or_404(model_class, pk=obj_id)

            # Check permission
            if not PermissionManager.user_has_permission(request.user, obj, permission):
                if raise_404:
                    raise Http404("Object not found")
                else:
                    raise PermissionDenied(
                        "You don't have permission to access this resource"
                    )

            # Attach object to request for convenience
            request.permission_object = obj

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_view_permission(view_func):
    """
    Shortcut decorator for view permission.
    Raises 404 if user cannot view the object.
    """
    return require_permission(Permission.VIEW_FULL, raise_404=True)(view_func)


def require_edit_permission(view_func):
    """
    Shortcut decorator for edit permission.
    Raises 403 if user cannot edit the object.
    """
    return require_permission(Permission.EDIT_FULL, raise_404=False)(view_func)


def require_spend_xp_permission(view_func):
    """
    Shortcut decorator for XP spending permission.
    Raises 403 if user cannot spend XP.
    """
    return require_permission(Permission.SPEND_XP, raise_404=False)(view_func)


def require_spend_freebies_permission(view_func):
    """
    Shortcut decorator for freebie spending permission.
    Raises 403 if user cannot spend freebies.
    """
    return require_permission(Permission.SPEND_FREEBIES, raise_404=False)(view_func)


def require_model_permission(
    model_class, permission: Permission, lookup="pk", raise_404=True
):
    """
    Decorator that explicitly specifies the model class.

    Args:
        model_class: Django model class to query
        permission: Permission enum required
        lookup: How to lookup object (default 'pk')
        raise_404: If True, raise 404 instead of 403 for unauthorized

    Usage:
        @require_model_permission(Character, Permission.EDIT_FULL)
        def update_character(request, pk):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get object ID from kwargs
            obj_id = kwargs.get(lookup)
            obj = get_object_or_404(model_class, pk=obj_id)

            # Check permission
            if not PermissionManager.user_has_permission(request.user, obj, permission):
                if raise_404:
                    raise Http404("Object not found")
                else:
                    raise PermissionDenied(
                        "You don't have permission to access this resource"
                    )

            # Attach object to request for convenience
            request.permission_object = obj

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
