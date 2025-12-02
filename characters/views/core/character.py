from typing import Any

from characters.forms.core import LimitedCharacterForm
from characters.forms.core.limited_edit import LimitedCharacterEditForm
from characters.models.core import Character
from core.cache import CACHE_TIMEOUT_MEDIUM, cache_function
from core.mixins import EditPermissionMixin, ViewPermissionMixin, VisibilityFilterMixin
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

    @staticmethod
    @cache_function(timeout=CACHE_TIMEOUT_MEDIUM, key_prefix="character_scenes")
    def get_character_scenes(character_id):
        """
        Get scenes for a character with proper prefetching.
        This is cached to avoid N+1 queries on repeated views.
        """
        return list(
            Scene.objects.filter(characters__id=character_id)
            .select_related("chronicle", "location")
            .prefetch_related("characters")
            .order_by("-date_of_scene")
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Use cached queryset for scenes
        context["scenes"] = self.get_character_scenes(context["object"].id)
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
                return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))
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


class CharacterUpdateView(EditPermissionMixin, UpdateView):
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
        Owners get limited fields (notes, description, etc.) via LimitedCharacterEditForm.
        STs and admins get full access to all fields via the default form.
        """
        # Check if user has full edit permission
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )

        if has_full_edit:
            # STs and admins get all fields (ModelForm with fields="__all__")
            return super().get_form_class()
        else:
            # Owners get limited fields (notes, description, public_info, image)
            return LimitedCharacterEditForm
