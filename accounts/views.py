from accounts.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    FreebieAwardForm,
    ProfileUpdateForm,
    SceneXP,
)
from accounts.models import Profile
from characters.models.core import Character
from characters.models.mage.rote import Rote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from game.forms import WeeklyXPRequestForm
from game.models import Scene, UserSceneReadStatus, Week, WeeklyXPRequest
from items.models.core import ItemModel
from locations.models.core.location import LocationModel


class SignUp(CreateView):
    """View for the Sign Up Page"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signup.html"


class ProfileView(LoginRequiredMixin, DetailView):
    """View for user profile. Requires authentication."""

    model = Profile
    template_name = "accounts/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scenes_waiting"] = []
        if self.object.is_st():
            context["scenes_waiting"] = Scene.objects.filter(waiting_for_st=True)
        context["scenexp_forms"] = [
            SceneXP(scene=s, prefix=f"scene_{s.pk}") for s in self.object.xp_requests()
        ]
        context["freebie_forms"] = [
            FreebieAwardForm(character=character)
            for character in self.object.freebies_to_approve()
        ]
        if "weekly_xp_request_forms" not in context:
            context["weekly_xp_request_forms"] = [
                WeeklyXPRequestForm(character=c, week=w)
                for c, w in self.object.get_unfulfilled_weekly_xp_requests()
            ]
        context["weekly_xp_request_forms_to_approve"] = [
            WeeklyXPRequestForm(
                character=c,
                week=w,
                instance=WeeklyXPRequest.objects.get(character=c, week=w),
            )
            for c, w in self.object.get_unfulfilled_weekly_xp_requests_to_approve()
        ]
        # story_xp_request_forms
        # story_xp_request_forms_to_approve
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        form_errors = False
        submitted_scene_id = request.POST.get("submit_scene")
        # Freebies
        submitted_freebies_id = request.POST.get("submit_freebies")

        # Object Approval
        approve_character_id = request.POST.get("approve_character")
        approve_location_id = request.POST.get("approve_location")
        approve_item_id = request.POST.get("approve_item")
        approve_rote_id = request.POST.get("approve_rote")

        # Image Approval
        approve_character_image_id = request.POST.get("approve_character_image")
        approve_location_image_id = request.POST.get("approve_location_image")
        approve_item_image_id = request.POST.get("approve_item_image")

        # Weekly XP
        submit_weekly_request_id = request.POST.get("submit_weekly_request")
        submit_weekly_approval_id = request.POST.get("submit_weekly_approval")

        # Story XP
        submit_story_request_id = request.POST.get("submit_story_request")
        submit_story_approval_id = request.POST.get("submit_story_approval")

        # Mark Scene Read
        mark_scene_id_read = request.POST.get("mark_scene_read")

        # Authorization: Only storytellers can approve things
        approval_actions = [
            approve_character_id,
            approve_location_id,
            approve_item_id,
            approve_rote_id,
            approve_character_image_id,
            approve_location_image_id,
            approve_item_image_id,
            submitted_scene_id,
            submitted_freebies_id,
            submit_weekly_approval_id,
        ]
        if any(approval_actions) and not request.user.profile.is_st():
            raise PermissionDenied("Only storytellers can perform approval actions")

        if submitted_scene_id is not None:
            scene = get_object_or_404(Scene, pk=submitted_scene_id)
            form = SceneXP(request.POST, scene=scene)
            if form.is_valid():
                form.save()
        if approve_character_id is not None:
            char = get_object_or_404(Character, pk=approve_character_id)
            char.status = "App"
            char.save()
            if hasattr(char, "group_set"):
                for g in char.group_set.all():
                    g.update_pooled_backgrounds()
        if approve_location_id is not None:
            loc = get_object_or_404(LocationModel, pk=approve_location_id)
            loc.status = "App"
            loc.save()
        if approve_item_id is not None:
            item = get_object_or_404(ItemModel, pk=approve_item_id)
            item.status = "App"
            item.save()
        if approve_rote_id is not None:
            rote = get_object_or_404(Rote, pk=approve_rote_id)
            rote.status = "App"
            rote.save()
        if approve_character_image_id is not None:
            approve_character_image_id = approve_character_image_id.split("-")[-1]
            char = get_object_or_404(Character, pk=approve_character_image_id)
            char.image_status = "app"
            char.save()
        if approve_location_image_id is not None:
            approve_location_image_id = approve_location_image_id.split("-")[-1]
            loc = get_object_or_404(LocationModel, pk=approve_location_image_id)
            loc.image_status = "app"
            loc.save()
        if approve_item_image_id is not None:
            approve_item_image_id = approve_item_image_id.split("-")[-1]
            item = get_object_or_404(ItemModel, pk=approve_item_image_id)
            item.image_status = "app"
            item.save()
        if submitted_freebies_id is not None:
            char = get_object_or_404(Character, pk=submitted_freebies_id)
            form = FreebieAwardForm(request.POST, character=char)
            if form.is_valid():
                form.save()
        if submit_weekly_request_id is not None:
            _, week_pk, _, char_pk = submit_weekly_request_id.split("-")
            week = get_object_or_404(Week, pk=week_pk)
            char = get_object_or_404(Character, pk=char_pk)
            # Check user owns this character
            if char.owner != request.user:
                raise PermissionDenied("You can only submit requests for your own characters")
            form = WeeklyXPRequestForm(request.POST, week=week, character=char)
            if form.is_valid():
                form.player_save()
            else:
                context["weekly_xp_request_forms"] = [
                    form
                ]  # Replace the list with the invalid form
                form_errors = True
        if submit_weekly_approval_id is not None:
            _, week_pk, _, char_pk = submit_weekly_approval_id.split("-")
            week = get_object_or_404(Week, pk=week_pk)
            char = get_object_or_404(Character, pk=char_pk)
            xp_request = get_object_or_404(WeeklyXPRequest, character=char, week=week)
            form = WeeklyXPRequestForm(
                request.POST,
                week=week,
                character=char,
                instance=xp_request,
            )
            if form.is_valid():
                form.st_save()
        if mark_scene_id_read is not None:
            scene = get_object_or_404(Scene, pk=mark_scene_id_read)
            status = UserSceneReadStatus.objects.get_or_create(
                scene=scene, user=self.object.user
            )[0]
            status.read = True
            status.save()
        elif "Edit Preferences" in request.POST.keys():
            return redirect("profile_update", pk=self.object.pk)
        if form_errors:
            return self.render_to_response(context)
        return redirect(reverse("profile", kwargs={"pk": context["object"].pk}))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user profile. Requires authentication."""

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/form.html"


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    
    def get_success_url(self):
        return self.request.user.profile.get_absolute_url()
