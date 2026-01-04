from accounts.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    FreebieAwardForm,
    ProfileUpdateForm,
    SceneXP,
)
from accounts.models import Profile
from characters.models.core import Character
from core.mixins import MessageMixin
from core.services import ApprovalService
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from game.forms import WeeklyXPRequestForm
from game.models import Scene, UserSceneReadStatus, Week, WeeklyXPRequest


class SignUp(MessageMixin, CreateView):
    """View for the Sign Up Page"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signup.html"
    success_message = "Account created successfully! Welcome to Tellurium Games."
    error_message = "Failed to create account. Please correct the errors below."


class ProfileView(LoginRequiredMixin, DetailView):
    """View for user profile. Requires authentication."""

    model = Profile
    template_name = "accounts/detail.html"

    def get_context_data(self, **kwargs):
        """Build context for the profile detail page.

        Adds forms for XP requests, freebie approvals, and weekly XP management.
        Only storytellers see the scenes_waiting list.

        Returns:
            dict: Context with profile data, XP forms, and approval queues.
        """
        context = super().get_context_data(**kwargs)
        context["scenes_waiting"] = []
        if self.object.is_st():
            context["scenes_waiting"] = Scene.objects.waiting_for_st()

        # Optimize queries with select_related
        scenes = self.object.xp_requests().select_related("chronicle", "location")
        characters = self.object.freebies_to_approve().select_related("owner", "chronicle")

        context["scenexp_forms"] = [SceneXP(scene=s, prefix=f"scene_{s.pk}") for s in scenes]
        context["freebie_forms"] = [
            FreebieAwardForm(character=character) for character in characters
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
                instance=get_object_or_404(WeeklyXPRequest, character=c, week=w),
            )
            for c, w in self.object.get_unfulfilled_weekly_xp_requests_to_approve()
        ]
        # story_xp_request_forms
        # story_xp_request_forms_to_approve
        return context

    def post(self, request, *args, **kwargs):
        """Handle profile page form submissions.

        Processes various approval and XP-related actions including:
        - Scene XP awards
        - Character/location/item/rote approvals
        - Image approvals
        - Weekly XP request submissions and approvals
        - Marking scenes as read

        Only storytellers can perform approval actions.

        Returns:
            HttpResponse: Redirect to profile on success, or re-render on error.
        """
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
            messages.error(request, "Only storytellers can perform approval actions.")
            raise PermissionDenied("Only storytellers can perform approval actions")

        if submitted_scene_id is not None:
            scene = get_object_or_404(Scene, pk=submitted_scene_id)
            form = SceneXP(request.POST, scene=scene)
            if form.is_valid():
                form.save()
                messages.success(request, f"XP awarded for scene '{scene.name}'!")
            else:
                messages.error(request, "Failed to award XP. Please check your input.")

        # Object approvals using ApprovalService
        if approve_character_id is not None:
            _, msg = ApprovalService.approve_object("character", approve_character_id)
            messages.success(request, msg)
        if approve_location_id is not None:
            _, msg = ApprovalService.approve_object("location", approve_location_id)
            messages.success(request, msg)
        if approve_item_id is not None:
            _, msg = ApprovalService.approve_object("item", approve_item_id)
            messages.success(request, msg)
        if approve_rote_id is not None:
            _, msg = ApprovalService.approve_object("rote", approve_rote_id)
            messages.success(request, msg)

        # Image approvals using ApprovalService
        if approve_character_image_id is not None:
            parsed_id = ApprovalService.parse_image_id(approve_character_image_id)
            _, msg = ApprovalService.approve_image("character", parsed_id)
            messages.success(request, msg)
        if approve_location_image_id is not None:
            parsed_id = ApprovalService.parse_image_id(approve_location_image_id)
            _, msg = ApprovalService.approve_image("location", parsed_id)
            messages.success(request, msg)
        if approve_item_image_id is not None:
            parsed_id = ApprovalService.parse_image_id(approve_item_image_id)
            _, msg = ApprovalService.approve_image("item", parsed_id)
            messages.success(request, msg)
        if submitted_freebies_id is not None:
            char = get_object_or_404(Character, pk=submitted_freebies_id)
            form = FreebieAwardForm(request.POST, character=char)
            if form.is_valid():
                form.save()
                messages.success(request, f"Freebies awarded to '{char.name}'!")
            else:
                messages.error(request, "Failed to award freebies. Please check your input.")
        if submit_weekly_request_id is not None:
            _, week_pk, _, char_pk = submit_weekly_request_id.split("-")
            week = get_object_or_404(Week, pk=week_pk)
            char = get_object_or_404(Character, pk=char_pk)
            # Check user owns this character
            if char.owner != request.user:
                messages.error(request, "You can only submit requests for your own characters.")
                raise PermissionDenied("You can only submit requests for your own characters")
            form = WeeklyXPRequestForm(request.POST, week=week, character=char)
            if form.is_valid():
                form.player_save()
                messages.success(request, f"Weekly XP request submitted for '{char.name}'!")
            else:
                context["weekly_xp_request_forms"] = [
                    form
                ]  # Replace the list with the invalid form
                form_errors = True
                messages.error(request, "Failed to submit XP request. Please check your input.")
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
                messages.success(request, f"Weekly XP request approved for '{char.name}'!")
            else:
                messages.error(request, "Failed to approve XP request. Please check your input.")
        if mark_scene_id_read is not None:
            with transaction.atomic():
                scene = get_object_or_404(Scene, pk=mark_scene_id_read)
                status, created = UserSceneReadStatus.objects.get_or_create(
                    scene=scene, user=self.object.user
                )
                status.read = True
                status.save()
            messages.success(request, f"Scene '{scene.name}' marked as read!")
        elif "Edit Preferences" in request.POST.keys():
            return redirect("profile_update", pk=self.object.pk)
        if form_errors:
            return self.render_to_response(context)
        return redirect(reverse("profile", kwargs={"pk": context["object"].pk}))


class ProfileUpdateView(MessageMixin, LoginRequiredMixin, UpdateView):
    """View for updating user profile. Requires authentication."""

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/form.html"
    success_message = "Profile updated successfully!"
    error_message = "Failed to update profile. Please correct the errors below."


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        """Get URL to redirect to after successful login.

        Adds a welcome message and redirects to the user's profile page.

        Returns:
            str: URL to the user's profile page.
        """
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return self.request.user.profile.get_absolute_url()

    def form_invalid(self, form):
        """Handle invalid login form submission.

        Displays an error message when login credentials are incorrect.

        Returns:
            HttpResponse: Rendered login form with error message.
        """
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
