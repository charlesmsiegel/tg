"""
Mixins for class-based views.

This module consolidates all view mixins used throughout the application:
- Permission mixins: For controlling access to views and objects
- Message mixins: For displaying success/error messages
- User verification mixins: For checking special user status
"""


from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from characters.models.core import CharacterModel
from core.models import Model
from core.permission_context import add_object_permissions, prepare_permission_objects
from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from core.template_resolution import shared_template_names
from game.models import Chronicle, STRelationship
from game.security import readable_chronicles


class SharedTemplateMixin:
    """Render ``template_name`` if it exists, else ``shared_template_name``.

    The specific name stays declared as the override slot; see
    ``core.template_resolution``.
    """

    shared_template_name = None

    def get_template_names(self):
        try:
            names = super().get_template_names()
        except ImproperlyConfigured:
            if not self.shared_template_name:
                raise
            names = []  # no specific template declared: the shared one is the page
        return shared_template_names(names, self.shared_template_name)


class ListHeadingMixin:
    """``list_title`` and ``list_heading`` for shared list pages.

    ``list_title`` defaults to the model's ``verbose_name_plural`` and
    ``list_heading`` to its gameline heading class (``vtm_heading``, ...).
    """

    list_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("list_title", self.list_title or self.model._meta.verbose_name_plural)
        context.setdefault("list_heading", f"{getattr(self.model, 'gameline', 'wod')}_heading")
        return context


class ObjectCachingMixin:
    """
    Mixin that caches the result of get_object() to avoid duplicate DB queries.

    This is useful when dispatch() needs to access the object for permission
    checking before the view's standard get_object() call in get()/post().

    Without this caching, the same object would be fetched twice per request:
    once during permission checking in dispatch(), and again when the view
    prepares context data.

    Usage:
        class MyView(ObjectCachingMixin, DetailView):
            model = MyModel
    """

    def get_object(self, queryset=None):
        """Return the object, caching the result for subsequent calls."""
        if not hasattr(self, "_cached_object"):
            self._cached_object = super().get_object(queryset)
        return self._cached_object


class PermissionContextMixin:
    """Expose the primary object's immutable, request-local capabilities."""

    def get_context_data(self, **kwargs):
        return add_object_permissions(self.request, super().get_context_data(**kwargs))


class PermissionRequiredMixin(PermissionContextMixin, ObjectCachingMixin):
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
            self.request.user, obj, self.required_permission, request=self.request
        )


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


class ScopedEditFormMixin:
    """Select the reviewed full form only for an editor of this object's scope.

    Keep the supplied limited form intact: its model and widgets are deliberate,
    even when the view edits a subclass. EditPermissionMixin still controls access
    to the endpoint; this mixin limits what an authorized owner may submit.
    """

    limited_form_class = None

    def get_form_class(self):
        if PermissionManager.user_has_scoped_editor_role(
            self.request.user, self.get_object(), request=self.request
        ):
            return super().get_form_class()
        if self.limited_form_class is None:
            raise ValueError("limited_form_class must be set")
        return self.limited_form_class


class SpendFreebiesPermissionMixin(PermissionRequiredMixin):
    """
    Require freebie spending permission for CBV.
    Raises 403 if user cannot spend freebies.
    """

    required_permission = Permission.SPEND_FREEBIES
    raise_404_on_deny = False


class VisibilityFilterMixin(PermissionContextMixin):
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

        if context.get("paginator") is not None:
            prepare_permission_objects(self.request, list(context["object_list"]))

        # For detail views, add visibility information
        if hasattr(self, "object") and self.object:
            context["visibility_tier"] = PermissionManager.get_visibility_tier(
                self.request.user, self.object, request=self.request
            )
            context["user_can_edit"] = PermissionManager.user_can_edit(
                self.request.user, self.object, request=self.request
            )
            context["user_can_spend_xp"] = PermissionManager.user_can_spend_xp(
                self.request.user, self.object, request=self.request
            )
            context["user_can_spend_freebies"] = PermissionManager.user_can_spend_freebies(
                self.request.user, self.object, request=self.request
            )
            # Add the VisibilityTier enum to context for template comparisons
            context["VisibilityTier"] = VisibilityTier

        return context


class OwnerRequiredMixin(ObjectCachingMixin):
    """
    Mixin that restricts access to object owners only.

    Basic Usage (checks self.get_object()):
        class CharacterDeleteView(OwnerRequiredMixin, DeleteView):
            model = Character

    URL-based Character Lookup (checks a character from URL kwargs):
        class WeeklyXPRequestCreateView(OwnerRequiredMixin, CreateView):
            owner_check_model = CharacterModel
            owner_check_kwarg = "character_pk"
            owner_check_attr = "character"
            owner_check_message = "You can only submit requests for your own characters."

        After dispatch, self.character will contain the looked-up character.

    URL pattern requirements:
        The URL must include the specified kwarg. Example:
        path('xp/<int:character_pk>/', view, name='create')
    """

    # URL-based ownership check configuration
    owner_check_model = None  # Set to model class (e.g., CharacterModel) to look up from URL
    owner_check_kwarg = "character_pk"  # URL kwarg containing the PK
    owner_check_attr = "character"  # Attribute name to store the looked-up object
    owner_check_message = "You can only access your own characters."

    def dispatch(self, request, *args, **kwargs):
        """Check if user is owner before dispatching."""
        # URL-based ownership check
        if self.owner_check_model is not None:
            obj = get_object_or_404(self.owner_check_model, pk=kwargs.get(self.owner_check_kwarg))
            setattr(self, self.owner_check_attr, obj)

            # Check ownership
            is_owner = False
            if hasattr(obj, "owner") and obj.owner == request.user:
                is_owner = True
            elif hasattr(obj, "user") and obj.user == request.user:
                is_owner = True

            # Also allow admins
            is_admin = request.user.is_superuser or request.user.is_staff

            if not (is_owner or is_admin):
                raise PermissionDenied(self.owner_check_message)

            return super().dispatch(request, *args, **kwargs)

        # Standard ownership check on self.get_object()
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


class SpecialUserMixin(PermissionContextMixin):
    """Compatibility helper for full-read checks, plus explicit capabilities."""

    def check_if_special_user(self, obj, user):
        """
        Check if user has special access to the object.

        Args:
            obj: The object to check access for
            user: The user to check

        Returns:
            bool: True if user has special access
        """
        return PermissionManager.user_has_permission(
            user, obj, Permission.VIEW_FULL, request=getattr(self, "request", None)
        )


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


class ScopedCreationFormMixin:
    """Limit creation forms to chronicles the current user can access."""

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if "chronicle" in form.fields:
            form.fields["chronicle"].queryset = readable_chronicles(self.request.user)
        return form


def prepare_created_object(form, request):
    """Bind new core.Model rows to their creator before any form saves them."""
    obj = getattr(form, "instance", None)
    if not isinstance(obj, Model) or obj.pk is not None:
        return
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied("Login required to create objects")
    chronicle = getattr(obj, "chronicle", None)
    if chronicle is not None:
        if not readable_chronicles(user).filter(pk=chronicle.pk).exists():
            raise PermissionDenied("Cannot create an object in this chronicle")
    gameline = getattr(obj, "gameline", None)
    if not isinstance(gameline, str):
        gameline = obj.get_gameline() if hasattr(obj, "get_gameline") else None
    roles = PermissionManager.get_scoped_roles(user, chronicle, gameline, request)
    shared_allowed = bool(roles & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST})
    obj.owner = None if shared_allowed and request.POST.get("shared") == "1" else user
    if Role.ADMIN not in roles:
        obj.status = "Un"


class MessageMixin(SuccessMessageMixin, ErrorMessageMixin):
    """
    Combined mixin for both success and error messages.

    Usage:
        class MyCreateView(MessageMixin, CreateView):
            model = MyModel
            success_message = "{name} created successfully!"
            error_message = "Failed to create {model_name}. Please check the form."
    """

    def form_valid(self, form):
        if isinstance(self, CreateView):
            prepare_created_object(form, self.request)
        return super().form_valid(form)


class StorytellerRequiredMixin:
    """
    Restrict writes to staff or storytellers scoped to the target chronicle
    and gameline. Chronicle-wide targets require the head storyteller.

    Usage:
        class StoryCreateView(StorytellerRequiredMixin, CreateView):
            model = Story
    """

    def dispatch(self, request, *args, **kwargs):
        """Authorize the target scope before any subclass handler runs."""
        if not request.user.is_authenticated:
            raise PermissionDenied("Login required")
        if request.user.is_staff or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        model = getattr(self, "model", None)
        obj = None
        if kwargs.get("pk") is not None and hasattr(self, "get_object"):
            obj = self.get_object()
        chronicle = obj if isinstance(obj, Chronicle) else getattr(obj, "chronicle", None)
        if chronicle is None and obj is not None:
            character = getattr(obj, "character", None)
            chronicle = getattr(character, "chronicle", None)
        if chronicle is None and kwargs.get("chronicle_pk") is not None:
            chronicle = get_object_or_404(Chronicle, pk=kwargs["chronicle_pk"])
        if chronicle is None and kwargs.get("character_pk") is not None:
            character = get_object_or_404(CharacterModel, pk=kwargs["character_pk"])
            chronicle = character.chronicle
        else:
            character = getattr(obj, "character", None)
        gameline = getattr(obj, "gameline", None)
        if gameline is None and obj is not None:
            gameline = getattr(character, "gameline", None)
            if gameline is None and hasattr(character, "get_gameline"):
                gameline = character.get_gameline()
        if gameline is None and hasattr(character, "get_gameline"):
            gameline = character.get_gameline()
        if gameline is None and model is not Chronicle:
            gameline = request.POST.get("gameline") if request.method == "POST" else None
        allowed = (
            PermissionManager.can_manage_chronicle(request.user, chronicle, request)
            if model is Chronicle or gameline is None
            else PermissionManager.can_manage_scope(request.user, chronicle, gameline, request)
        )
        if (
            getattr(model, "__name__", None) == "Scene"
            and obj is None
            and request.method in {"GET", "HEAD"}
        ):
            allowed = allowed or bool(
                chronicle
                and STRelationship.objects.filter(chronicle=chronicle, user=request.user).exists()
            )
        if not allowed:
            raise PermissionDenied("Matching chronicle storyteller required")
        return super().dispatch(request, *args, **kwargs)


class CharacterOwnerOrSTMixin(PermissionContextMixin, ObjectCachingMixin):
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

        character = getattr(obj, "character", None)
        if character and PermissionManager.user_has_permission(
            request.user, character, Permission.VIEW_FULL, request=request
        ):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Only the character owner or storytellers can access this")
