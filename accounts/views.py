from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView

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
from game.forms import WeeklyXPRequestForm
from game.models import Scene, UserSceneReadStatus, Week, WeeklyXPRequest


class SignUp(MessageMixin, CreateView):
    """View for the Sign Up Page"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("core:home")
    template_name = "accounts/signup.html"
    success_message = "Account created successfully! Welcome to Tellurium Games."
    error_message = "Failed to create account. Please correct the errors below."


def verify_st_for_chronicle(request, chronicle, action_description="this action"):
    """Verify the requesting user is an ST for the given chronicle.

    chronicle may be None (object with no chronicle); is_st_for(None)
    returns False, so access is denied in that case.

    Raises PermissionDenied with a descriptive message if not.
    """
    if not request.user.profile.is_st_for(chronicle):
        msg = f"You are not a storyteller for this chronicle. Cannot perform {action_description}."
        messages.error(request, msg)
        raise PermissionDenied(msg)


class SceneXPAwardView(LoginRequiredMixin, View):
    """Award XP for a completed scene. ST only."""

    http_method_names = ["post"]

    def post(self, request, scene_pk):
        scene = get_object_or_404(Scene, pk=scene_pk)
        verify_st_for_chronicle(request, scene.chronicle, "scene XP award")
        form = SceneXP(request.POST, scene=scene, prefix=f"scene_{scene.pk}")
        if form.is_valid():
            form.save()
            messages.success(request, f"XP awarded for scene '{scene.name}'!")
        else:
            messages.error(request, "Failed to award XP. Please check your input.")
        return redirect("accounts:profile", pk=request.user.profile.pk)


class ObjectApprovalView(LoginRequiredMixin, View):
    """Approve a character, location, item, or rote. ST only."""

    http_method_names = ["post"]

    def post(self, request, object_type, pk):
        model_class = ApprovalService.OBJECT_MODEL_MAP.get(object_type)
        if not model_class:
            raise Http404
        obj = get_object_or_404(model_class, pk=pk)
        chronicle = getattr(obj, "chronicle", None)
        verify_st_for_chronicle(request, chronicle, f"{object_type} approval")
        _, msg = ApprovalService.approve_object(object_type, pk)
        messages.success(request, msg)
        return redirect("accounts:profile", pk=request.user.profile.pk)


class ImageApprovalView(LoginRequiredMixin, View):
    """Approve a pending image for a character, location, or item. ST only."""

    http_method_names = ["post"]

    def post(self, request, object_type, pk):
        model_class = ApprovalService.IMAGE_MODEL_MAP.get(object_type)
        if not model_class:
            raise Http404
        obj = get_object_or_404(model_class, pk=pk)
        chronicle = getattr(obj, "chronicle", None)
        verify_st_for_chronicle(request, chronicle, f"{object_type} image approval")
        _, msg = ApprovalService.approve_image(object_type, pk)
        messages.success(request, msg)
        return redirect("accounts:profile", pk=request.user.profile.pk)


class FreebieAwardView(LoginRequiredMixin, View):
    """Award backstory freebies to a character. ST only."""

    http_method_names = ["post"]

    def post(self, request, character_pk):
        char = get_object_or_404(Character, pk=character_pk)
        verify_st_for_chronicle(request, char.chronicle, "freebie approval")
        form = FreebieAwardForm(request.POST, character=char)
        if form.is_valid():
            form.save()
            messages.success(request, f"Freebies awarded to '{char.name}'!")
        else:
            messages.error(request, "Failed to award freebies. Please check your input.")
        return redirect("accounts:profile", pk=request.user.profile.pk)


class WeeklyXPRequestView(LoginRequiredMixin, View):
    """Submit a weekly XP request. Character owner only."""

    http_method_names = ["post"]

    def post(self, request, week_pk, character_pk):
        week = get_object_or_404(Week, pk=week_pk)
        char = get_object_or_404(Character, pk=character_pk)
        if char.owner != request.user:
            messages.error(request, "You can only submit requests for your own characters.")
            raise PermissionDenied("You can only submit requests for your own characters.")
        form = WeeklyXPRequestForm(request.POST, week=week, character=char)
        if form.is_valid():
            form.player_save()
            messages.success(request, f"Weekly XP request submitted for '{char.name}'!")
        else:
            messages.error(request, "Failed to submit XP request. Please check your input.")
        return redirect("accounts:profile", pk=request.user.profile.pk)


class WeeklyXPApprovalView(LoginRequiredMixin, View):
    """Approve a weekly XP request. ST only."""

    http_method_names = ["post"]

    def post(self, request, week_pk, character_pk):
        week = get_object_or_404(Week, pk=week_pk)
        char = get_object_or_404(Character, pk=character_pk)
        verify_st_for_chronicle(request, char.chronicle, "weekly XP approval")
        xp_request = get_object_or_404(WeeklyXPRequest, character=char, week=week)
        form = WeeklyXPRequestForm(request.POST, week=week, character=char, instance=xp_request)
        if form.is_valid():
            form.st_save()
            messages.success(request, f"Weekly XP request approved for '{char.name}'!")
        else:
            messages.error(request, "Failed to approve XP request. Please check your input.")
        return redirect("accounts:profile", pk=request.user.profile.pk)


class MarkSceneReadView(LoginRequiredMixin, View):
    """Mark a scene as read. Any logged-in user.

    Uses request.user (the old ProfileView handler used the viewed
    profile's user — always the same person, since ProfileView only
    allows viewing your own profile).
    """

    http_method_names = ["post"]

    def post(self, request, scene_pk):
        with transaction.atomic():
            scene = get_object_or_404(Scene, pk=scene_pk)
            status, _ = UserSceneReadStatus.objects.get_or_create(scene=scene, user=request.user)
            status.read = True
            status.save()
        messages.success(request, f"Scene '{scene.name}' marked as read!")
        return redirect("accounts:profile", pk=request.user.profile.pk)


class ProfileView(LoginRequiredMixin, DetailView):
    """View for user profile. Requires authentication.

    Security: Users can only view their own profile unless they are staff.
    This prevents IDOR (Insecure Direct Object Reference) attacks.
    """

    model = Profile
    template_name = "accounts/detail.html"

    def get_object(self, queryset=None):
        """Get profile object with authorization check.

        Only the profile owner or staff members can view the profile.

        Returns:
            Profile: The requested profile if authorized.

        Raises:
            PermissionDenied: If user is not authorized to view this profile.
        """
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only view your own profile.")
        return obj

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
        # Include polymorphic_ctype for subclass-specific method calls in templates
        characters = self.object.freebies_to_approve().select_related(
            "polymorphic_ctype", "owner", "chronicle"
        )

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


class ProfileUpdateView(MessageMixin, LoginRequiredMixin, UpdateView):
    """View for updating user profile. Requires authentication.

    Security: Users can only update their own profile unless they are staff.
    This prevents IDOR (Insecure Direct Object Reference) attacks.
    """

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/form.html"
    success_message = "Profile updated successfully!"
    error_message = "Failed to update profile. Please correct the errors below."

    def get_object(self, queryset=None):
        """Get profile object with authorization check.

        Only the profile owner or staff members can update the profile.

        Returns:
            Profile: The requested profile if authorized.

        Raises:
            PermissionDenied: If user is not authorized to update this profile.
        """
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only update your own profile.")
        return obj


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
