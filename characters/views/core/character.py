from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from characters.forms.core.limited_edit import OwnerUnapprovedCharacterEditForm
from characters.models.core import Character
from core.cache import CACHE_TIMEOUT_MEDIUM, cache_function
from core.mixins import (
    EditPermissionMixin,
    ViewPermissionMixin,
    prepare_created_object,
)
from core.permissions import Permission, PermissionManager, Role
from game.models import Scene
from game.security import filter_scenes


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
        # Cache the candidate scenes, then apply the current request's audience.
        # Visibility may change while a cached character sheet is still warm.
        scenes = self.get_character_scenes(context["object"].id)
        visible_ids = set(
            filter_scenes(
                Scene.objects.filter(pk__in=[scene.pk for scene in scenes]),
                self.request.user,
            ).values_list("pk", flat=True)
        )
        context["scenes"] = [scene for scene in scenes if scene.pk in visible_ids]
        can_edit = PermissionManager.user_has_permission(
            self.request.user, self.object, Permission.EDIT_FULL, request=self.request
        )
        context["can_retire"] = self.object.status != "Dec" and (
            can_edit or self.object.owner_id == self.request.user.pk
        )
        context["can_decease"] = PermissionManager.user_has_scoped_editor_role(
            self.request.user, self.object, request=self.request
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if user has permission to change status
        can_change_status = PermissionManager.user_has_scoped_editor_role(
            request.user, self.object, request=request
        )

        # Use atomic transaction for status changes
        with transaction.atomic():
            if not can_change_status:
                # Only owners can retire their own characters
                if (
                    "retire" in request.POST
                    and self.object.owner == request.user
                    and self.object.status != "Dec"
                ):
                    self.object.status = "Ret"
                    self.object.save()
                # STs/Admins can mark as deceased
                elif "decease" in request.POST:
                    return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))
            else:
                # Handle retirement and death status changes
                if "retire" in request.POST and self.object.status != "Dec":
                    self.object.status = "Ret"
                    self.object.save()
                if "decease" in request.POST:
                    self.object.status = "Dec"
                    self.object.save()

        return redirect(reverse("characters:character", kwargs={"pk": self.object.pk}))


class CharacterCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for characters.
    Automatically sets the owner to the current user.

    Security: Uses explicit field whitelist to prevent mass assignment of
    sensitive fields like status, xp, owner, freebies_approved, etc.
    """

    model = Character
    fields = ["name", "concept", "description", "public_info", "chronicle", "npc"]
    template_name = "characters/core/character/form.html"
    success_message = "Character '{name}' created successfully!"
    error_message = "Failed to create Character. Please correct the errors below."

    def form_valid(self, form):
        prepare_created_object(form, self.request)
        return super().form_valid(form)


class CharacterUpdateView(EditPermissionMixin, UpdateView):
    """
    Update view for characters.
    Automatically enforces edit permissions.

    - Chronicle Head STs can edit everything (via ST_EDIT_FIELDS)
    - Owners can edit safe draft fields while an object is unfinished or returned.

    Security: Uses explicit field whitelist to prevent mass assignment attacks.
    """

    model = Character
    # Fields available to STs with full edit permission
    # Owners receive a draft form without approval or ST-only fields.
    ST_EDIT_FIELDS = [
        "name",
        "concept",
        "description",
        "public_info",
        "notes",
        "image",
        "st_notes",
        "display",
        "visibility",
    ]
    fields = ST_EDIT_FIELDS
    template_name = "characters/core/character/form.html"
    success_message = "Character '{name}' updated successfully!"
    error_message = "Failed to update Character. Please correct the errors below."

    def get_form_class(self):
        """
        Return different form based on user permissions.
        Owners get draft fields without approval or ST-only fields.
        STs and admins get full access via the default form with ST_EDIT_FIELDS.
        """
        roles = PermissionManager.get_user_roles(self.request.user, self.get_object())
        if roles & {Role.ADMIN, Role.CHRONICLE_HEAD_ST, Role.CHRONICLE_ST}:
            return super().get_form_class()
        return OwnerUnapprovedCharacterEditForm
