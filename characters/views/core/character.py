from typing import Any

from characters.forms.core import LimitedCharacterForm
from characters.models.core import Character
from core.mixins import (
    ApprovedUserContextMixin,
    EditPermissionMixin,
    ViewPermissionMixin,
    VisibilityFilterMixin,
)
from core.permissions import Permission, PermissionManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from game.models import Scene


class CharacterDetailView(ViewPermissionMixin, DetailView):
    """
    Detail view for characters.
    Automatically enforces view permissions and provides visibility tier in context.
    """

    model = Character
    template_name = "characters/core/character/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["scenes"] = (
            Scene.objects.filter(characters=context["object"])
            .select_related("chronicle", "location", "st")
            .prefetch_related("characters", "participants")
            .order_by("-date_of_scene")
        )
        # Backward compatibility: is_approved_user now means "can edit"
        context["is_approved_user"] = PermissionManager.user_can_edit(
            self.request.user, self.object
        ) or PermissionManager.user_has_permission(
            self.request.user, self.object, Permission.EDIT_LIMITED
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if user has permission to change status
        can_change_status = PermissionManager.user_has_permission(
            request.user, self.object, Permission.EDIT_FULL
        )

        if not can_change_status:
            # Only owners can retire their own characters
            if "retire" in request.POST and self.object.owner == request.user:
                self.object.status = "Ret"
                self.object.save()
            # STs/Admins can mark as deceased
            elif "decease" in request.POST:
                return redirect(
                    reverse("characters:character", kwargs={"pk": self.object.pk})
                )
        else:
            # Handle retirement and death status changes
            if "retire" in request.POST:
                self.object.status = "Ret"
                self.object.save()
            if "decease" in request.POST:
                self.object.status = "Dec"
                self.object.save()

        return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))


class CharacterListView(VisibilityFilterMixin, ListView):
    """
    List view for characters.
    Automatically filters to only characters the user can view.
    """

    model = Character
    template_name = "characters/core/character/list.html"
    context_object_name = "characters"
    paginate_by = 50

    def get_queryset(self):
        """Get filtered queryset based on permissions."""
        qs = super().get_queryset()
        # Additional filtering can be added here (e.g., by status, chronicle, etc.)
        return qs.order_by("name")


class CharacterCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for characters.
    Automatically sets the owner to the current user.
    """

    model = Character
    fields = "__all__"
    template_name = "characters/core/character/form.html"
    success_message = "Character '{name}' created successfully!"
    error_message = "Failed to create Character. Please correct the errors below."

    def form_valid(self, form):
        # Set owner to current user if not already set
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class CharacterUpdateView(ApprovedUserContextMixin, EditPermissionMixin, UpdateView):
    """
    Update view for characters.
    Automatically enforces edit permissions.

    - Chronicle Head STs can edit everything
    - Owners can only edit limited fields (enforced by form)
    """

    model = Character
    fields = "__all__"
    template_name = "characters/core/character/form.html"
    success_message = "Character '{name}' updated successfully!"
    error_message = "Failed to update Character. Please correct the errors below."

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get limited fields, STs get full access.
        """
        # Check if user has full edit permission
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )

        if has_full_edit:
            # STs and admins get all fields
            return super().get_form_class()
        else:
            # Owners get limited fields (descriptive only)
            return LimitedCharacterForm
