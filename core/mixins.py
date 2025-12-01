"""
Mixins for class-based views.

This module consolidates all view mixins used throughout the application:
- Permission mixins: For controlling access to views and objects
- Message mixins: For displaying success/error messages
- User verification mixins: For checking special user status
"""

from core.permissions import Permission, PermissionManager, VisibilityTier
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404


class PermissionRequiredMixin:
    """
    Mixin for CBVs requiring permission checks.

    Set required_permission to specify which permission is needed.
    Set raise_404_on_deny to True to return 404 instead of 403.

    Usage:
        class CharacterUpdateView(PermissionRequiredMixin, UpdateView):
            model = Character
            required_permission = Permission.EDIT_FULL
            raise_404_on_deny = False
    """

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
        if self.required_permission is None:
            raise ValueError("required_permission must be set")

        obj = self.get_object()
        return PermissionManager.user_has_permission(
            self.request.user, obj, self.required_permission
        )

    def get_context_data(self, **kwargs):
        """Add is_approved_user flag to context."""
        context = super().get_context_data(**kwargs)
        # If we got here, user has passed permission checks
        context["is_approved_user"] = True
        return context


class ViewPermissionMixin(PermissionRequiredMixin):
    """
    Require view permission for CBV.
    Raises 404 if user cannot view the object.
    """

    required_permission = Permission.VIEW_FULL
    raise_404_on_deny = True


class EditPermissionMixin(PermissionRequiredMixin):
    """
    Require full edit permission for CBV.
    Raises 403 if user cannot edit the object.
    """

    required_permission = Permission.EDIT_FULL
    raise_404_on_deny = False


class SpendXPPermissionMixin(PermissionRequiredMixin):
    """
    Require XP spending permission for CBV.
    Raises 403 if user cannot spend XP.
    """

    required_permission = Permission.SPEND_XP
    raise_404_on_deny = False


class SpendFreebiesPermissionMixin(PermissionRequiredMixin):
    """
    Require freebie spending permission for CBV.
    Raises 403 if user cannot spend freebies.
    """

    required_permission = Permission.SPEND_FREEBIES
    raise_404_on_deny = False


class VisibilityFilterMixin:
    """
    Mixin to filter querysets by user permissions.

    Automatically filters list views to only show objects the user can view.
    Adds visibility tier and edit permission to context for detail views.

    Usage:
        class CharacterListView(VisibilityFilterMixin, ListView):
            model = Character
    """

    def get_queryset(self):
        """Filter queryset to only viewable objects."""
        qs = super().get_queryset()
        return PermissionManager.filter_queryset_for_user(self.request.user, qs)

    def get_context_data(self, **kwargs):
        """Add visibility tier to context."""
        context = super().get_context_data(**kwargs)

        # For detail views, add visibility information
        if hasattr(self, "object") and self.object:
            context["visibility_tier"] = PermissionManager.get_visibility_tier(
                self.request.user, self.object
            )
            context["user_can_edit"] = PermissionManager.user_can_edit(
                self.request.user, self.object
            )
            context["user_can_spend_xp"] = PermissionManager.user_can_spend_xp(
                self.request.user, self.object
            )
            context["user_can_spend_freebies"] = PermissionManager.user_can_spend_freebies(
                self.request.user, self.object
            )
            # Add the VisibilityTier enum to context for template comparisons
            context["VisibilityTier"] = VisibilityTier

        return context


class OwnerRequiredMixin:
    """
    Mixin that restricts access to object owners only.

    Usage:
        class CharacterDeleteView(OwnerRequiredMixin, DeleteView):
            model = Character
    """

    def dispatch(self, request, *args, **kwargs):
        """Check if user is owner before dispatching."""
        obj = self.get_object()

        # Check if user is owner
        is_owner = False
        if hasattr(obj, "owner") and obj.owner == request.user:
            is_owner = True
        elif hasattr(obj, "user") and obj.user == request.user:
            is_owner = True

        # Also allow admins
        is_admin = request.user.is_superuser or request.user.is_staff

        if not (is_owner or is_admin):
            raise PermissionDenied("Only the owner can perform this action")

        return super().dispatch(request, *args, **kwargs)


class STRequiredMixin:
    """
    Mixin that restricts access to chronicle STs and admins only.

    Usage:
        class CharacterApproveView(STRequiredMixin, UpdateView):
            model = Character
    """

    def dispatch(self, request, *args, **kwargs):
        """Check if user is ST before dispatching."""
        obj = self.get_object()

        # Check if user is admin
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # Check if user is head ST of the chronicle
        if hasattr(obj, "chronicle") and obj.chronicle:
            if hasattr(obj.chronicle, "head_st") and obj.chronicle.head_st == request.user:
                return super().dispatch(request, *args, **kwargs)
            elif hasattr(obj.chronicle, "head_storytellers"):
                if obj.chronicle.head_storytellers.filter(id=request.user.id).exists():
                    return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Only storytellers can perform this action")


class SpecialUserMixin:
    """
    Mixin for checking if a user has special access to an object.

    Special users include:
    - The object owner
    - Any authenticated storyteller (ST)
    - Anyone if the object has no owner

    Usage:
        class MyView(SpecialUserMixin, DetailView):
            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['is_special'] = self.check_if_special_user(self.object, self.request.user)
                return context
    """

    def check_if_special_user(self, obj, user):
        """
        Check if user has special access to the object.

        Args:
            obj: The object to check access for
            user: The user to check

        Returns:
            bool: True if user has special access
        """
        if obj.owner is None:
            return True
        if user == obj.owner:
            return True
        if not user.is_authenticated:
            return False
        if user.profile.is_st():
            return True
        return False


class SuccessMessageMixin:
    """
    Mixin to add a success message when a form is successfully saved.

    Usage:
        class MyCreateView(SuccessMessageMixin, CreateView):
            model = MyModel
            success_message = "{name} created successfully!"

    The success_message can use field names from the object in curly braces.
    For safety, it only allows access to string fields and limits length.
    """

    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            message = self.get_success_message(form.cleaned_data)
            if message:
                messages.success(self.request, message)
        return response

    def get_success_message(self, cleaned_data):
        """
        Generate the success message from the template string.
        Uses self.object for formatting to ensure we have saved data.
        """
        if not self.success_message:
            return ""

        # Get safe formatting dict from object
        format_dict = self.get_message_format_dict()

        try:
            return self.success_message.format(**format_dict)
        except (KeyError, AttributeError, ValueError):
            # Fallback to unformatted message if formatting fails
            return self.success_message

    def get_message_format_dict(self):
        """
        Create a dictionary of safe values for message formatting.
        Only includes basic string representations to avoid security issues.
        """
        if not hasattr(self, "object") or not self.object:
            return {}

        format_dict = {}

        # Add common safe attributes
        safe_attrs = ["name", "id", "pk"]
        for attr in safe_attrs:
            if hasattr(self.object, attr):
                value = getattr(self.object, attr)
                # Convert to string and limit length for safety
                format_dict[attr] = str(value)[:100]

        # Add model name for generic messages
        format_dict["model_name"] = self.object._meta.verbose_name
        format_dict["model_name_plural"] = self.object._meta.verbose_name_plural

        return format_dict


class ErrorMessageMixin:
    """
    Mixin to add error messages when form validation fails.

    Usage:
        class MyCreateView(ErrorMessageMixin, CreateView):
            model = MyModel
            error_message = "Please correct the errors below."
    """

    error_message = "Please correct the errors below."

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.error_message:
            messages.error(self.request, self.error_message)
        return response


class MessageMixin(SuccessMessageMixin, ErrorMessageMixin):
    """
    Combined mixin for both success and error messages.

    Usage:
        class MyCreateView(MessageMixin, CreateView):
            model = MyModel
            success_message = "{name} created successfully!"
            error_message = "Failed to create {model_name}. Please check the form."
    """

    pass


class DeleteMessageMixin:
    """
    Mixin to add a success message when an object is deleted.

    Usage:
        class MyDeleteView(DeleteMessageMixin, DeleteView):
            model = MyModel
            success_message = "{name} deleted successfully!"
    """

    success_message = ""

    def delete(self, request, *args, **kwargs):
        # Store object info before deletion
        self.object = self.get_object()
        object_name = str(self.object)

        # Format success message before deleting object
        if self.success_message:
            format_dict = {"name": object_name[:100], "pk": self.object.pk}
            try:
                message = self.success_message.format(**format_dict)
            except (KeyError, ValueError):
                message = self.success_message
            messages.success(request, message)

        return super().delete(request, *args, **kwargs)


class StorytellerRequiredMixin:
    """
    Mixin that restricts access to storytellers and admins only.

    Checks if the user has storyteller status via profile.is_st().
    This is for general ST-only operations, not chronicle-specific.

    Usage:
        class StoryCreateView(StorytellerRequiredMixin, CreateView):
            model = Story
    """

    def dispatch(self, request, *args, **kwargs):
        """Check if user is ST before dispatching."""
        # Allow admins
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # Check if user is a storyteller
        if not request.user.is_authenticated or not request.user.profile.is_st():
            raise PermissionDenied("Only storytellers can perform this action")

        return super().dispatch(request, *args, **kwargs)


class CharacterOwnerOrSTMixin:
    """
    Mixin that restricts access to character owners, storytellers, and admins.

    This is for views related to objects that have a 'character' attribute
    (like XP requests, journal entries, etc.).

    Usage:
        class WeeklyXPRequestDetailView(CharacterOwnerOrSTMixin, DetailView):
            model = WeeklyXPRequest
    """

    def dispatch(self, request, *args, **kwargs):
        """Check if user is owner or ST before dispatching."""
        # Get the object first
        obj = self.get_object()

        # Allow admins
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # Check if user is a storyteller
        if request.user.is_authenticated and request.user.profile.is_st():
            return super().dispatch(request, *args, **kwargs)

        # Check if user is the character owner
        if hasattr(obj, "character") and obj.character:
            if obj.character.owner == request.user:
                return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Only the character owner or storytellers can access this")
