from characters.models.core.character import Character
from characters.models.mage.mage import Mage
from characters.models.mage.rote import Rote
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
        choices=zip(
            [
                "wod_heading",
                "vtm_heading",
                "wta_heading",
                "mta_heading",
                "ctd_heading",
                "wto_heading",
            ],
            [
                "World of Darkness",
                "Vampire: the Masquerade",
                "Werewolf: the Apocalypse",
                "Mage: the Ascension",
                "Changeling: the Dreaming",
                "Wraith: the Oblivion",
            ],
        ),
        default="wod_heading",
        help_text="Choose the game system font style for headings",
    )

    theme_list = ["light", "dark"]

    theme = models.CharField(
        max_length=100,
        choices=zip(
            theme_list,
            [x.replace("_", " ").title() for x in theme_list],
        ),
        default="light",
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

    lines_toggle = models.BooleanField(
        default=False, help_text="Show your lines to other players"
    )

    veils_toggle = models.BooleanField(
        default=False, help_text="Show your veils to other players"
    )

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
        return Character.objects.owned_by(self.user)

    def my_locations(self):
        return LocationModel.objects.owned_by(self.user)

    def my_items(self):
        return ItemModel.objects.owned_by(self.user)

    def xp_requests(self):
        return Scene.objects.awaiting_xp().for_user_chronicles(self.user)

    def xp_story(self):
        return Story.objects.filter(xp_given=False)

    def xp_weekly(self):
        return Week.objects.filter(xp_given=False)

    def characters_to_approve(self):
        return Character.objects.pending_approval_for_user(self.user)

    def items_to_approve(self):
        return ItemModel.objects.pending_approval_for_user(self.user)

    def locations_to_approve(self):
        return LocationModel.objects.pending_approval_for_user(self.user)

    def rotes_to_approve(self):
        """Get rotes pending approval with their associated mages.

        Optimized to avoid N+1 query issues by using prefetch_related.
        """
        from django.db.models import Prefetch

        rotes = (
            Rote.objects.filter(
                status__in=["Un", "Sub"],
                chronicle__in=self.user.chronicle_set.all(),
            )
            .prefetch_related(Prefetch("mage_set", queryset=Mage.objects.all()))
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
        return Character.objects.filter(
            chronicle__in=self.user.chronicle_set.all(), freebies_approved=False
        ).at_freebie_step()

    def character_images_to_approve(self):
        return Character.objects.with_pending_images().for_user_chronicles(self.user)

    def location_images_to_approve(self):
        return LocationModel.objects.with_pending_images().for_user_chronicles(
            self.user
        )

    def item_images_to_approve(self):
        return ItemModel.objects.with_pending_images().for_user_chronicles(self.user)

    def clean(self):
        """Validate profile data before saving."""
        super().clean()
        errors = {}

        # Validate theme is in valid choices
        if self.theme not in self.theme_list:
            errors["theme"] = f"Invalid theme '{self.theme}'. Must be one of: {', '.join(self.theme_list)}"

        # Validate preferred_heading is in valid choices
        valid_headings = ["wod_heading", "vtm_heading", "wta_heading", "mta_heading", "ctd_heading", "wto_heading"]
        if self.preferred_heading not in valid_headings:
            errors["preferred_heading"] = f"Invalid preferred heading '{self.preferred_heading}'. Must be one of: {', '.join(valid_headings)}"

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
        return reverse("profile", kwargs={"pk": self.pk})

    def get_updated_journals(self):
        return Journal.objects.filter(journalentry__st_message="").distinct()

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

        char_map = {c.pk: c for c in char_list}
        all_weeks = {w.pk: w for w in Week.objects.all()}

        results = [(char_map[c], all_weeks[w]) for (c, w) in missing_pairs]
        return [pair for pair in results if not pair[0].npc]

    def get_unfulfilled_weekly_xp_requests_to_approve(self):
        """Get all character/week pairs with unapproved XP requests for storyteller review.

        Returns a list of (character, week) tuples where:
        - A WeeklyXPRequest exists for the character/week combination
        - The request has not yet been approved
        - The character is associated with the week

        This is used by storytellers to review and approve pending weekly XP requests.
        """
        char_list = Character.objects.all()

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
        char_map = {c.pk: c for c in char_list}
        all_weeks = {w.pk: w for w in Week.objects.all()}
        return [(char_map[c], all_weeks[w]) for (c, w) in result_pairs]

    def xp_spend_requests(self):
        """Get all characters waiting for XP spend approval.

        Returns a list of characters that have pending XP spending requests
        awaiting storyteller approval.
        """
        chars = Character.objects.all()
        return [x for x in chars if x.waiting_for_xp_spend()]

    def unread_scenes(self):
        return Scene.objects.filter(
            userscenereadstatus__user=self.user, userscenereadstatus__read=False
        ).distinct()
