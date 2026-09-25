"""
Mixins for class-based views.

This module consolidates all view mixins used throughout the application:
- Permission mixins: For controlling access to views and objects
- Message mixins: For displaying success/error messages
- User verification mixins: For checking special user status
"""

import re

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import CreateView

from characters.models.core import CharacterModel
from core.models import Model
from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from game.models import Chronicle, STRelationship
from game.security import readable_chronicles
from game.spending_approval import SpendingDecisionError, decide_spending_request


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


class PermissionRequiredMixin(ObjectCachingMixin):
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

    def get_context_data(self, **kwargs):
        """Expose full-read capability to legacy detail templates."""
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = PermissionManager.user_has_permission(
            self.request.user,
            self.get_object(),
            Permission.VIEW_FULL,
            request=self.request,
        )
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


class STRequiredMixin(ObjectCachingMixin):
    """
    Mixin that restricts access to chronicle STs and admins only.

    Usage:
        class CharacterApproveView(STRequiredMixin, UpdateView):
            model = Character
    """

    def dispatch(self, request, *args, **kwargs):
        """Check if user is ST before dispatching."""
        obj = self.get_object()

        if PermissionManager.user_has_permission(
            request.user, obj, Permission.APPROVE, request=request
        ):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Only storytellers can perform this action")


class SpecialUserMixin:
    """
    Mixin for checking if a user has special access to an object.

    Special users are users with VIEW_FULL for this object.

    Templates gating on ``is_approved_user`` should set it via
    get_is_approved_user(); auto-setting it for all such views is in #1459.
    """

    def get_is_approved_user(self, obj):
        """is_approved_user value for templates: staff OR special-user access.

        Combines the middleware/context-processor staff flag with the
        per-object special-user check so neither audience is excluded.
        """
        return getattr(self.request, "is_approved_user", False) or (
            self.check_if_special_user(obj, self.request.user)
        )

    def check_if_special_user(self, obj, user):
        """
        Check if user has special access to the object.

        Args:
            obj: The object to check access for
            user: The user to check

        Returns:
            bool: True if user has special access
        """
        return PermissionManager.user_has_permission(user, obj, Permission.VIEW_FULL)


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


class CharacterOwnerOrSTMixin(ObjectCachingMixin):
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


class AjaxLoginRequiredMixin:
    """
    Mixin for AJAX views that require login.

    Returns a JSON error response for unauthenticated users instead of redirecting
    to the login page (which would cause issues for AJAX requests).

    Usage:
        class MyAjaxView(AjaxLoginRequiredMixin, View):
            def get(self, request, *args, **kwargs):
                return JsonResponse({'data': 'value'})
    """

    def dispatch(self, request, *args, **kwargs):
        from django.http import JsonResponse

        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        return super().dispatch(request, *args, **kwargs)


class DropdownOptionsView(AjaxLoginRequiredMixin, View):
    """
    Base class for AJAX views that return dropdown options.

    Subclasses should override get_queryset() or get_options() to return
    the queryset or list of options.

    Attributes:
        value_attr: Attribute name for option value (default: 'pk')
        label_attr: Attribute name for option label (default: 'name')

    Usage:
        class LoadFactionsView(DropdownOptionsView):
            label_attr = 'name'

            def get_queryset(self):
                affiliation_id = self.request.GET.get('affiliation')
                return MageFaction.objects.filter(parent=affiliation_id)
    """

    value_attr = "pk"
    label_attr = "name"

    def get_queryset(self):
        """Override to return queryset of options."""
        return []

    def get_options(self):
        """Override for custom option generation (default: use get_queryset)."""
        return self.get_queryset()

    def get(self, request, *args, **kwargs):
        from core.ajax import dropdown_options_response

        options = self.get_options()
        return dropdown_options_response(
            options, value_attr=self.value_attr, label_attr=self.label_attr
        )


class SimpleValuesView(AjaxLoginRequiredMixin, View):
    """
    Base class for AJAX views that return simple value lists.

    Subclasses should override get_values() to return the list of values.

    Usage:
        class LoadRatingsView(SimpleValuesView):
            def get_values(self):
                mf = get_object_or_404(MeritFlaw, pk=self.request.GET.get('mf'))
                return mf.ratings.values_list('value', flat=True)
    """

    def get_values(self):
        """Override to return list of values."""
        return []

    def get(self, request, *args, **kwargs):
        from core.ajax import simple_values_response

        values = self.get_values()
        return simple_values_response(values)


class JsonListView(AjaxLoginRequiredMixin, View):
    """
    Base class for AJAX views that return a JSON list of objects.

    Subclasses should override get_items() to return the list of dicts.

    Usage:
        class GetAbilitiesView(JsonListView):
            def get_items(self):
                practice = get_object_or_404(Practice, id=self.request.GET.get('practice_id'))
                abilities = practice.abilities.all()
                return [{'id': a.id, 'name': a.name} for a in abilities]
    """

    include_empty_option = True
    empty_option_label = "--------"

    def get_items(self):
        """Override to return list of dicts."""
        return []

    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse

        items = self.get_items()
        if self.include_empty_option:
            items = [{"id": "", "name": self.empty_option_label}] + list(items)
        return JsonResponse(items, safe=False)


class ApprovalMixin:
    """
    Base mixin for handling spending request approval and denial in character detail views.

    Subclasses configure the specific approval type (XP, freebie) via class attributes.

    Class Attributes:
        approve_button_value: Button value to match for approve action
        reject_button_value: Button value to match for reject action
        spendings_related_name: Related manager name on character (e.g., 'xp_spendings')
        request_key_prefix: Prefix for parsing request IDs (e.g., 'xp_request_')
        spending_type: Human-readable name for messages (e.g., 'XP spending')
    """

    approve_button_value = None  # Override in subclass
    reject_button_value = None  # Override in subclass
    spendings_related_name = None  # Override in subclass
    request_key_prefix = None  # Override in subclass
    spending_type = None  # Override in subclass

    def get_service_factory(self):
        """Return the service factory for this approval type. Override in subclass."""
        raise NotImplementedError("Subclasses must implement get_service_factory()")

    def get_request_model(self):
        """Return the model class for this spending request type. Override in subclass."""
        raise NotImplementedError("Subclasses must implement get_request_model()")

    def _get_spendings_manager(self):
        """Get the related manager for spending requests."""
        return getattr(self.object, self.spendings_related_name)

    def _parse_request_id(self, request, button_value):
        """Accept exactly one correctly named approval or rejection button."""
        from django.core.exceptions import ValidationError

        matching_keys = [k for k, v in request.POST.items() if v == button_value]
        if len(matching_keys) != 1 or not self.request_key_prefix:
            raise ValidationError("Invalid request: exactly one action button is required")
        suffix = "approve" if button_value == self.approve_button_value else "reject"
        match = re.fullmatch(
            rf"{re.escape(self.request_key_prefix)}([1-9][0-9]*)_{suffix}",
            matching_keys[0],
        )
        if match is None:
            raise ValidationError("Invalid request: malformed action key")
        return int(match.group(1))

    def post(self, request, *args, **kwargs):
        from django.core.exceptions import ValidationError
        from django.shortcuts import redirect
        from django.urls import reverse

        self.object = self.get_object()
        decision = None
        button = None
        if self.approve_button_value in request.POST.values():
            decision, button = "approve", self.approve_button_value
        elif self.reject_button_value in request.POST.values():
            decision, button = "deny", self.reject_button_value

        if decision is not None:
            try:
                request_id = self._parse_request_id(request, button)
            except ValidationError as exc:
                messages.error(request, str(exc))
            else:
                try:
                    result = decide_spending_request(
                        self.get_request_model(),
                        self.object,
                        request_id,
                        request.user,
                        decision,
                    )
                except SpendingDecisionError as exc:
                    messages.error(request, str(exc))
                else:
                    messages.success(request, result.message)
            return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

        if hasattr(super(), "post"):
            return super().post(request, *args, **kwargs)
        return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))


class XPApprovalMixin(ApprovalMixin):
    """
    Mixin for handling XP spending request approval and denial.

    Usage:
        class VampireDetailView(XPApprovalMixin, HumanDetailView):
            model = Vampire
            template_name = "characters/vampire/vampire/detail.html"
    """

    approve_button_value = "Approve"
    reject_button_value = "Reject"
    spendings_related_name = "xp_spendings"
    request_key_prefix = "xp_request_"
    spending_type = "XP spending"

    def get_service_factory(self):
        from characters.services.xp_spending import XPSpendingServiceFactory

        return XPSpendingServiceFactory

    def get_request_model(self):
        from game.models import XPSpendingRequest

        return XPSpendingRequest


class FreebieApprovalMixin(ApprovalMixin):
    """
    Mixin for handling freebie spending request approval and denial.

    Usage:
        class VampireDetailView(FreebieApprovalMixin, HumanDetailView):
            model = Vampire
            template_name = "characters/vampire/vampire/detail.html"
    """

    approve_button_value = "Approve Freebie"
    reject_button_value = "Reject Freebie"
    spendings_related_name = "freebie_spendings"
    request_key_prefix = "freebie_request_"
    spending_type = "Freebie spending"

    def get_service_factory(self):
        from characters.services.freebie_spending import FreebieSpendingServiceFactory

        return FreebieSpendingServiceFactory

    def get_request_model(self):
        from game.models import FreebieSpendingRecord

        return FreebieSpendingRecord
