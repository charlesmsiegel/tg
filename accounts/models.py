from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse

from accounts.dashboard import ProfileDashboard
from core.base import ValidatedSaveMixin
from core.constants import HeadingChoices, ThemeChoices
from game.models import Chronicle, STRelationship


class Profile(ValidatedSaveMixin, models.Model):
    """User profile extending Django's default User model.

    Architecture Decision: This project uses Django's default User model with a
    OneToOne Profile extension rather than a custom User model. While AbstractUser
    is recommended for new projects, this approach was chosen because:

    - The project was already in production when custom users became best practice
    - Migration would require complex data migration with high risk
    - Current approach works well with all Django/third-party packages
    - Performance is acceptable with proper use of select_related()

    For new Django projects, use AbstractUser from the start.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, help_text="The user this profile belongs to"
    )

    preferred_heading = models.CharField(
        max_length=30,
        choices=HeadingChoices.CHOICES,
        default=HeadingChoices.WOD,
        help_text="Choose the game system font style for headings",
    )

    theme = models.CharField(
        max_length=100,
        choices=ThemeChoices.CHOICES,
        default=ThemeChoices.LIGHT,
        help_text="Choose a color scheme",
    )

    highlight_text = models.BooleanField(
        default=True,
        help_text="When enabled, quotes and special text will be highlighted in theme colors",
    )

    discord_id = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Your Discord username for communication outside the game",
    )

    lines = models.TextField(
        default="",
        blank=True,
        null=True,
        help_text="Topics you prefer not to interact with at all during gameplay",
    )

    veils = models.TextField(
        default="",
        blank=True,
        null=True,
        help_text="Content you prefer not to have shown on screen, but can be referenced indirectly",
    )

    discord_toggle = models.BooleanField(
        default=False, help_text="Show your Discord ID to other players"
    )

    lines_toggle = models.BooleanField(default=False, help_text="Show your lines to other players")

    veils_toggle = models.BooleanField(default=False, help_text="Show your veils to other players")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def is_st(self):
        """Whether the user can act as a storyteller for at least one chronicle.

        True for the ``head_st`` of any chronicle and for the holder of any
        ``STRelationship`` row, the same people ``PermissionManager.can_manage_scope``
        accepts. Game storytellers (``Chronicle.game_storytellers``) are view-only and do
        not count; staff status is left to callers, which keeps this a data predicate.
        Callers that need the answer more than once per request should keep the result
        rather than call again: each call is one query.
        """
        return Chronicle.objects.filter(
            Q(head_st=self.user) | Q(st_relationships__user=self.user)
        ).exists()

    def is_st_for(self, chronicle):
        """Check if user is a storyteller for a specific chronicle.

        Returns True if:
        - User is the head_st of the chronicle, OR
        - User has an STRelationship for the chronicle

        Note: game_storytellers are view-only and cannot perform approval actions.

        Args:
            chronicle: The Chronicle object to check against

        Returns:
            bool: True if user can perform ST actions on this chronicle
        """
        if chronicle is None:
            return False
        # Check if user is head ST
        if hasattr(chronicle, "head_st") and chronicle.head_st == self.user:
            return True
        # Check if user has an STRelationship for this chronicle
        return STRelationship.objects.filter(user=self.user, chronicle=chronicle).exists()

    @property
    def dashboard(self):
        """Return the profile-bound dashboard selector."""
        return ProfileDashboard(self)

    def st_relations(self):
        """Return storyteller relationships grouped by chronicle."""
        return self.dashboard.st_relations()

    def my_characters(self):
        """Return characters owned by this user."""
        return self.dashboard.my_characters()

    def my_locations(self):
        """Return locations owned by this user."""
        return self.dashboard.my_locations()

    def my_items(self):
        """Return items owned by this user."""
        return self.dashboard.my_items()

    def xp_requests(self):
        """Return scenes awaiting XP awards for this user's chronicles."""
        return self.dashboard.xp_requests()

    def xp_story(self):
        """Return stories that have not had XP awarded."""
        return self.dashboard.xp_story()

    def characters_to_approve(self):
        """Return characters awaiting this storyteller's approval."""
        return self.dashboard.characters_to_approve()

    def items_to_approve(self):
        """Return items awaiting this storyteller's approval."""
        return self.dashboard.items_to_approve()

    def locations_to_approve(self):
        """Return locations awaiting this storyteller's approval."""
        return self.dashboard.locations_to_approve()

    def rotes_to_approve(self):
        """Return rotes awaiting approval with their associated mages."""
        return self.dashboard.rotes_to_approve()

    def objects_to_approve(self):
        """Return all objects awaiting this storyteller's approval."""
        return self.dashboard.objects_to_approve()

    def freebies_to_approve(self):
        """Return characters with unapproved freebie allocations."""
        return self.dashboard.freebies_to_approve()

    def character_images_to_approve(self):
        """Return characters with images awaiting approval."""
        return self.dashboard.character_images_to_approve()

    def location_images_to_approve(self):
        """Return locations with images awaiting approval."""
        return self.dashboard.location_images_to_approve()

    def item_images_to_approve(self):
        """Return items with images awaiting approval."""
        return self.dashboard.item_images_to_approve()

    @property
    def theme_list(self):
        """Return valid theme keys from ThemeChoices."""
        return [key for key, _ in ThemeChoices.CHOICES]

    def clean(self):
        """Validate profile data before saving."""
        super().clean()
        errors = {}

        # Validate theme is in valid choices
        if self.theme not in self.theme_list:
            errors["theme"] = (
                f"Invalid theme '{self.theme}'. Must be one of: {', '.join(self.theme_list)}"
            )

        # Validate preferred_heading is in valid choices
        valid_headings = [key for key, _ in HeadingChoices.CHOICES]
        if self.preferred_heading not in valid_headings:
            errors["preferred_heading"] = (
                f"Invalid preferred heading '{self.preferred_heading}'. Must be one of: {', '.join(valid_headings)}"
            )

        # Validate user is provided
        if not self.user_id:
            errors["user"] = "Profile must be associated with a user"

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.pk})

    def get_updated_journals(self):
        """Return journals with entries awaiting storyteller response."""
        return self.dashboard.get_updated_journals()

    def get_unfulfilled_weekly_xp_requests(self):
        """Return player character/week pairs needing XP requests."""
        return self.dashboard.get_unfulfilled_weekly_xp_requests()

    def get_unfulfilled_weekly_xp_requests_to_approve(self):
        """Return character/week pairs awaiting storyteller approval."""
        return self.dashboard.get_unfulfilled_weekly_xp_requests_to_approve()

    def xp_spend_requests(self):
        """Return characters with pending XP spending requests."""
        return self.dashboard.xp_spend_requests()

    def unread_scenes(self):
        """Return scenes the user has not marked as read."""
        return self.dashboard.unread_scenes()
