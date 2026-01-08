from characters.models.core.character import Character
from characters.models.mage.mage import Mage
from characters.models.mage.rote import Rote
from core.constants import HeadingChoices, ThemeChoices
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from game.models import Journal, Scene, Story, STRelationship, Week, WeeklyXPRequest
from items.models.core.item import ItemModel
from locations.models.core.location import LocationModel


class Profile(models.Model):
    """User profile extending Django's default User model.

    Architecture Decision: This project uses Django's default User model with a
    OneToOne Profile extension rather than a custom User model. While AbstractUser
    is recommended for new projects, this approach was chosen because:

    - The project was already in production when custom users became best practice
    - Migration would require complex data migration with high risk
    - Current approach works well with all Django/third-party packages
    - Performance is acceptable with proper use of select_related()

    See docs/design/user_model_architecture.md for detailed trade-off analysis.

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

    def get_theme_css_path(self):
        """Returns the appropriate CSS path based on theme selections."""
        base = f"themes/{self.theme}.css"
        return base

    def is_st(self):
        """Check if user is a storyteller for any chronicle."""
        return STRelationship.objects.filter(user=self.user).exists()

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

    def st_relations(self):
        """Get all storyteller relationships organized by chronicle.

        Returns a dict mapping Chronicle objects to lists of STRelationship objects.
        Optimized to avoid N+1 query issues.
        """
        relationships = STRelationship.objects.for_user_optimized(self.user)

        d = {}
        for rel in relationships:
            if rel.chronicle not in d:
                d[rel.chronicle] = []
            d[rel.chronicle].append(rel)
        return d

    def my_characters(self):
        """Get all characters owned by this user.

        Returns:
            QuerySet[Character]: Characters owned by this user, ordered by name.
            Includes polymorphic_ctype for subclass-specific method calls in templates.
        """
        return Character.objects.owned_by(self.user).with_polymorphic_ctype()

    def my_locations(self):
        """Get all locations owned by this user.

        Returns:
            QuerySet[LocationModel]: Locations owned by this user, ordered by name.
            Includes polymorphic_ctype for subclass-specific method calls in templates.
        """
        return LocationModel.objects.owned_by(self.user).with_polymorphic_ctype()

    def my_items(self):
        """Get all items owned by this user.

        Returns:
            QuerySet[ItemModel]: Items owned by this user, ordered by name.
            Includes polymorphic_ctype for subclass-specific method calls in templates.
        """
        return ItemModel.objects.owned_by(self.user).with_polymorphic_ctype()

    def xp_requests(self):
        """Get scenes awaiting XP awards for this user's chronicles.

        Returns:
            QuerySet[Scene]: Finished scenes that haven't had XP awarded yet.
        """
        return Scene.objects.awaiting_xp().for_user_chronicles(self.user)

    def xp_story(self):
        """Get stories that haven't had XP awarded yet.

        Returns:
            QuerySet[Story]: Stories where xp_given is False.
        """
        return Story.objects.filter(xp_given=False)

    def xp_weekly(self):
        """Get weeks that haven't had XP awarded yet.

        Returns:
            QuerySet[Week]: Weeks where xp_given is False.
        """
        return Week.objects.filter(xp_given=False)

    def characters_to_approve(self):
        """Get characters pending approval for this user's chronicles.

        Returns:
            QuerySet[Character]: Characters awaiting ST approval in chronicles
            where this user is a storyteller.
        """
        return Character.objects.pending_approval_for_user(self.user)

    def items_to_approve(self):
        """Get items pending approval for this user's chronicles.

        Returns:
            QuerySet[ItemModel]: Items awaiting ST approval in chronicles
            where this user is a storyteller.
        """
        return ItemModel.objects.pending_approval_for_user(self.user)

    def locations_to_approve(self):
        """Get locations pending approval for this user's chronicles.

        Returns:
            QuerySet[LocationModel]: Locations awaiting ST approval in chronicles
            where this user is a storyteller.
        """
        return LocationModel.objects.pending_approval_for_user(self.user)

    def rotes_to_approve(self):
        """Get rotes pending approval with their associated mages.

        Optimized to avoid N+1 query issues by using select_related and prefetch_related.
        """
        from django.db.models import Prefetch

        rotes = (
            Rote.objects.filter(
                status__in=["Un", "Sub"],
                chronicle__in=self.user.chronicle_set.all(),
            )
            .select_related("chronicle")
            .prefetch_related(Prefetch("mage_set", queryset=Mage.objects.select_related("owner")))
            .order_by("name")
        )
        return {r: list(r.mage_set.all()) for r in rotes}

    def objects_to_approve(self):
        """Get all objects pending approval for this user's chronicles.

        Returns a combined list of characters, items, locations, and rotes
        that are pending approval for chronicles where this user is a storyteller.
        """
        to_approve = list(self.characters_to_approve())
        to_approve.extend(list(self.items_to_approve()))
        to_approve.extend(list(self.locations_to_approve()))
        to_approve.extend(list(self.rotes_to_approve()))
        return to_approve

    def freebies_to_approve(self):
        """Get characters with unapproved freebie point allocations.

        Returns:
            QuerySet[Character]: Characters at the freebie spending step
            that haven't been approved yet.
        """
        return Character.objects.filter(
            chronicle__in=self.user.chronicle_set.all(), freebies_approved=False
        ).at_freebie_step()

    def character_images_to_approve(self):
        """Get characters with pending image uploads for this user's chronicles.

        Returns:
            QuerySet[Character]: Characters with images awaiting ST approval.
            Includes polymorphic_ctype for subclass-specific method calls in templates.
        """
        return (
            Character.objects.with_pending_images()
            .for_user_chronicles(self.user)
            .with_polymorphic_ctype()
        )

    def location_images_to_approve(self):
        """Get locations with pending image uploads for this user's chronicles.

        Returns:
            QuerySet[LocationModel]: Locations with images awaiting ST approval.
            Includes polymorphic_ctype for subclass-specific method calls in templates.
        """
        return (
            LocationModel.objects.with_pending_images()
            .for_user_chronicles(self.user)
            .with_polymorphic_ctype()
        )

    def item_images_to_approve(self):
        """Get items with pending image uploads for this user's chronicles.

        Returns:
            QuerySet[ItemModel]: Items with images awaiting ST approval.
            Includes polymorphic_ctype for subclass-specific method calls in templates.
        """
        return (
            ItemModel.objects.with_pending_images()
            .for_user_chronicles(self.user)
            .with_polymorphic_ctype()
        )

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
        valid_headings = [
            "wod_heading",
            "vtm_heading",
            "wta_heading",
            "mta_heading",
            "ctd_heading",
            "wto_heading",
        ]
        if self.preferred_heading not in valid_headings:
            errors["preferred_heading"] = (
                f"Invalid preferred heading '{self.preferred_heading}'. Must be one of: {', '.join(valid_headings)}"
            )

        # Validate user is provided
        if not self.user_id:
            errors["user"] = "Profile must be associated with a user"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.pk})

    def get_updated_journals(self):
        """Get journals with entries awaiting ST response.

        Returns:
            QuerySet[Journal]: Journals containing entries where the ST hasn't
            yet provided a message/response.
        """
        return Journal.objects.filter(entries__st_message="").distinct()

    def get_unfulfilled_weekly_xp_requests(self):
        """Get character/week pairs that need XP requests created.

        Returns a list of (character, week) tuples where:
        - The character belongs to this user
        - The character is associated with the week
        - No WeeklyXPRequest exists for this character/week combination
        - The character is not an NPC

        This helps track which weekly XP requests the user still needs to submit.
        """
        char_list = self.my_characters()
        char_week_pairs = Week.characters.through.objects.filter(
            charactermodel_id__in=char_list
        ).values_list("charactermodel_id", "week_id")

        existing_requests = set(
            WeeklyXPRequest.objects.filter(
                character_id__in=[c for (c, w) in char_week_pairs],
                week_id__in=[w for (c, w) in char_week_pairs],
            ).values_list("character_id", "week_id")
        )

        missing_pairs = []
        for char_id, week_id in char_week_pairs:
            if (char_id, week_id) not in existing_requests:
                missing_pairs.append((char_id, week_id))

        # Early return if no missing pairs
        if not missing_pairs:
            return []

        char_map = {c.pk: c for c in char_list}
        # Only fetch weeks that are actually needed (not all weeks in the database)
        week_ids = set(w for (c, w) in missing_pairs)
        week_map = {w.pk: w for w in Week.objects.filter(pk__in=week_ids)}

        results = [(char_map[c], week_map[w]) for (c, w) in missing_pairs]
        return [pair for pair in results if not pair[0].npc]

    def get_unfulfilled_weekly_xp_requests_to_approve(self):
        """Get all character/week pairs with unapproved XP requests for storyteller review.

        Returns a list of (character, week) tuples where:
        - A WeeklyXPRequest exists for the character/week combination
        - The request has not yet been approved
        - The character is in a chronicle where this user is ST

        This is used by storytellers to review and approve pending weekly XP requests.
        """
        # Only fetch characters in chronicles where this user is ST
        char_list = Character.objects.filter(chronicle__st_relationships__user=self.user)

        char_week_pairs = Week.characters.through.objects.filter(
            charactermodel_id__in=char_list
        ).values_list("charactermodel_id", "week_id")

        unapproved_reqs = set(
            WeeklyXPRequest.objects.filter(
                approved=False,
                character_id__in=[c for (c, w) in char_week_pairs],
                week_id__in=[w for (c, w) in char_week_pairs],
            ).values_list("character_id", "week_id")
        )

        result_pairs = list(unapproved_reqs)

        # Early return if no unapproved requests
        if not result_pairs:
            return []

        char_map = {c.pk: c for c in char_list}
        # Only fetch weeks that are actually needed (not all weeks in the database)
        week_ids = set(w for (c, w) in result_pairs)
        week_map = {w.pk: w for w in Week.objects.filter(pk__in=week_ids)}
        return [(char_map[c], week_map[w]) for (c, w) in result_pairs]

    def xp_spend_requests(self):
        """Get all characters waiting for XP spend approval.

        Returns a queryset of characters that have pending XP spending requests
        awaiting storyteller approval.

        UPDATED: Optimized to use a single database query instead of N+1 queries.
        """
        return Character.objects.filter(xp_spendings__approved="Pending").distinct()

    def unread_scenes(self):
        """Get scenes that the user has not marked as read.

        Returns:
            QuerySet[Scene]: Scenes where the user's read status is False.
        """
        return Scene.objects.filter(
            user_read_statuses__user=self.user, user_read_statuses__read=False
        ).distinct()
