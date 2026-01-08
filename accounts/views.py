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
    success_url = reverse_lazy("core:home")
    template_name = "accounts/signup.html"
    success_message = "Account created successfully! Welcome to Tellurium Games."
    error_message = "Failed to create account. Please correct the errors below."


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

    # POST actions that require storyteller privileges
    ST_ONLY_ACTIONS = frozenset(
        [
            "submit_scene",
            "submit_freebies",
            "approve_character",
            "approve_location",
            "approve_item",
            "approve_rote",
            "approve_character_image",
            "approve_location_image",
            "approve_item_image",
            "submit_weekly_approval",
        ]
    )

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

    def _check_st_permission(self, request):
        """Check if a storyteller-only action is being attempted by a non-ST.

        Note: This is a preliminary check. Each handler must also verify
        chronicle-specific permissions using _verify_st_for_chronicle().
        """
        attempted_st_action = any(request.POST.get(action) for action in self.ST_ONLY_ACTIONS)
        if attempted_st_action and not request.user.profile.is_st():
            messages.error(request, "Only storytellers can perform approval actions.")
            raise PermissionDenied("Only storytellers can perform approval actions")

    def _verify_st_for_chronicle(self, request, chronicle, action_description="this action"):
        """Verify user is an ST for a specific chronicle.

        Args:
            request: The HTTP request
            chronicle: The Chronicle object to check against
            action_description: Description for error message

        Raises:
            PermissionDenied: If user is not an ST for the chronicle
        """
        if not request.user.profile.is_st_for(chronicle):
            msg = f"You are not a storyteller for this chronicle. Cannot perform {action_description}."
            messages.error(request, msg)
            raise PermissionDenied(msg)

    def _handle_scene_xp(self, request, scene_id):
        """Handle scene XP award submission."""
        scene = get_object_or_404(Scene, pk=scene_id)
        self._verify_st_for_chronicle(request, scene.chronicle, "scene XP award")
        form = SceneXP(request.POST, scene=scene, prefix=f"scene_{scene.pk}")
        if form.is_valid():
            form.save()
            messages.success(request, f"XP awarded for scene '{scene.name}'!")
        else:
            messages.error(request, "Failed to award XP. Please check your input.")

    def _handle_object_approval(self, request, object_type, object_id):
        """Handle object (character/location/item/rote) approval."""
        # Get the object first to verify chronicle permissions
        model_class = ApprovalService.OBJECT_MODEL_MAP.get(object_type)
        if model_class:
            obj = get_object_or_404(model_class, pk=object_id)
            chronicle = getattr(obj, "chronicle", None)
            self._verify_st_for_chronicle(request, chronicle, f"{object_type} approval")
        _, msg = ApprovalService.approve_object(object_type, object_id)
        messages.success(request, msg)

    def _handle_image_approval(self, request, object_type, image_id):
        """Handle image approval for an object type."""
        parsed_id = ApprovalService.parse_image_id(image_id)
        # Get the object first to verify chronicle permissions
        model_class = ApprovalService.IMAGE_MODEL_MAP.get(object_type)
        if model_class:
            obj = get_object_or_404(model_class, pk=parsed_id)
            chronicle = getattr(obj, "chronicle", None)
            self._verify_st_for_chronicle(request, chronicle, f"{object_type} image approval")
        _, msg = ApprovalService.approve_image(object_type, parsed_id)
        messages.success(request, msg)

    def _handle_freebies(self, request, char_id):
        """Handle freebie award submission."""
        char = get_object_or_404(Character, pk=char_id)
        self._verify_st_for_chronicle(request, char.chronicle, "freebie approval")
        form = FreebieAwardForm(request.POST, character=char)
        if form.is_valid():
            form.save()
            messages.success(request, f"Freebies awarded to '{char.name}'!")
        else:
            messages.error(request, "Failed to award freebies. Please check your input.")

    def _handle_weekly_request(self, request, request_id, context):
        """Handle weekly XP request submission. Returns True if form has errors."""
        _, week_pk, _, char_pk = request_id.split("-")
        week = get_object_or_404(Week, pk=week_pk)
        char = get_object_or_404(Character, pk=char_pk)
        if char.owner != request.user:
            messages.error(request, "You can only submit requests for your own characters.")
            raise PermissionDenied("You can only submit requests for your own characters")
        form = WeeklyXPRequestForm(request.POST, week=week, character=char)
        if form.is_valid():
            form.player_save()
            messages.success(request, f"Weekly XP request submitted for '{char.name}'!")
            return False
        context["weekly_xp_request_forms"] = [form]
        messages.error(request, "Failed to submit XP request. Please check your input.")
        return True

    def _handle_weekly_approval(self, request, approval_id):
        """Handle weekly XP request approval."""
        _, week_pk, _, char_pk = approval_id.split("-")
        week = get_object_or_404(Week, pk=week_pk)
        char = get_object_or_404(Character, pk=char_pk)
        self._verify_st_for_chronicle(request, char.chronicle, "weekly XP approval")
        xp_request = get_object_or_404(WeeklyXPRequest, character=char, week=week)
        form = WeeklyXPRequestForm(request.POST, week=week, character=char, instance=xp_request)
        if form.is_valid():
            form.st_save()
            messages.success(request, f"Weekly XP request approved for '{char.name}'!")
        else:
            messages.error(request, "Failed to approve XP request. Please check your input.")

    def _handle_mark_scene_read(self, request, scene_id):
        """Handle marking a scene as read."""
        with transaction.atomic():
            scene = get_object_or_404(Scene, pk=scene_id)
            status, _ = UserSceneReadStatus.objects.get_or_create(
                scene=scene, user=self.object.user
            )
            status.read = True
            status.save()
        messages.success(request, f"Scene '{scene.name}' marked as read!")

    def post(self, request, *args, **kwargs):
        """Handle profile page form submissions.

        Dispatches to handler methods based on POST parameters.
        Only storytellers can perform approval actions.

        Returns:
            HttpResponse: Redirect to profile on success, or re-render on error.
        """
        self.object = self.get_object()
        context = self.get_context_data()
        self._check_st_permission(request)
        form_errors = False

        # Scene XP
        if scene_id := request.POST.get("submit_scene"):
            self._handle_scene_xp(request, scene_id)

        # Object approvals
        for obj_type in ("character", "location", "item", "rote"):
            if obj_id := request.POST.get(f"approve_{obj_type}"):
                self._handle_object_approval(request, obj_type, obj_id)

        # Image approvals
        for obj_type in ("character", "location", "item"):
            if img_id := request.POST.get(f"approve_{obj_type}_image"):
                self._handle_image_approval(request, obj_type, img_id)

        # Freebies
        if char_id := request.POST.get("submit_freebies"):
            self._handle_freebies(request, char_id)

        # Weekly XP
        if request_id := request.POST.get("submit_weekly_request"):
            form_errors = self._handle_weekly_request(request, request_id, context)
        if approval_id := request.POST.get("submit_weekly_approval"):
            self._handle_weekly_approval(request, approval_id)

        # Mark scene read
        if scene_id := request.POST.get("mark_scene_read"):
            self._handle_mark_scene_read(request, scene_id)
        elif "Edit Preferences" in request.POST.keys():
            return redirect("accounts:profile_update", pk=self.object.pk)

        if form_errors:
            return self.render_to_response(context)
        return redirect(reverse("accounts:profile", kwargs={"pk": context["object"].pk}))


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
