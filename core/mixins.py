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
from django.views import View


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
        """Parse the request ID from POST data matching the button value.

        Validates that:
        - A matching POST key exists
        - The key has at least 3 underscore-separated parts
        - The third part is a positive integer

        Raises:
            ValidationError: If the POST data is malformed or missing required keys
        """
        from django.core.exceptions import ValidationError

        # Find matching keys
        matching_keys = [k for k, v in request.POST.items() if v == button_value]
        if not matching_keys:
            raise ValidationError("Invalid request: no matching action key found")

        request_key = matching_keys[0]
        parts = request_key.split("_")

        # Validate key format (needs at least 3 parts: prefix_type_id)
        if len(parts) < 3:
            raise ValidationError("Invalid request: malformed action key format")

        # Validate ID is a positive integer
        try:
            request_id = int(parts[2])
            if request_id < 0:
                raise ValidationError("Invalid request: ID must be a positive integer")
            return request_id
        except ValueError:
            raise ValidationError("Invalid request: ID must be a valid integer")

    def post(self, request, *args, **kwargs):
        import logging

        from django.core.exceptions import ValidationError
        from django.db import transaction
        from django.shortcuts import redirect
        from django.urls import reverse

        logger = logging.getLogger(__name__)
        self.object = self.get_object()
        request_model = self.get_request_model()

        if self.approve_button_value in request.POST.values():
            try:
                request_id = self._parse_request_id(request, self.approve_button_value)
            except ValidationError as e:
                messages.error(request, str(e.message))
                return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

            try:
                spending_request = self._get_spendings_manager().get(
                    id=request_id, approved="Pending"
                )
            except request_model.DoesNotExist:
                messages.error(
                    request, f"{self.spending_type} request not found or already processed"
                )
                return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

            try:
                with transaction.atomic():
                    service = self.get_service_factory().get_service(self.object)
                    result = service.apply(spending_request, request.user)

                    if result.success:
                        messages.success(request, result.message)
                    else:
                        messages.error(
                            request, result.error or f"Failed to apply {self.spending_type}"
                        )
            except Exception as e:
                logger.error(
                    f"Error approving {self.spending_type} for character {self.object.id}: {e}",
                    exc_info=True,
                )
                messages.error(request, f"Error approving {self.spending_type}: {str(e)}")

            return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

        if self.reject_button_value in request.POST.values():
            try:
                request_id = self._parse_request_id(request, self.reject_button_value)
            except ValidationError as e:
                messages.error(request, str(e.message))
                return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

            try:
                with transaction.atomic():
                    spending_request = (
                        self._get_spendings_manager()
                        .select_for_update()
                        .get(id=request_id, approved="Pending")
                    )

                    service = self.get_service_factory().get_service(self.object)
                    result = service.deny(spending_request, request.user)

                    if result.success:
                        messages.success(request, result.message)
                    else:
                        messages.error(
                            request, result.error or f"Failed to deny {self.spending_type}"
                        )
            except request_model.DoesNotExist:
                messages.error(
                    request, f"{self.spending_type} request not found or already processed"
                )

            return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))

        # Call parent post() for other actions (retire, decease, etc.)
        if hasattr(super(), "post"):
            return super().post(request, *args, **kwargs)
        # If parent doesn't have post(), return to detail view
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
