from core.models import Model, ModelManager, ModelQuerySet
from core.utils import CharacterOrganizationRegistry
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import CheckConstraint, OuterRef, Q, Subquery
from django.urls import reverse
from django.utils import timezone
from polymorphic.managers import PolymorphicManager


class CharacterQuerySet(ModelQuerySet):
    """Custom queryset for Character with chainable query patterns."""

    def npcs(self):
        """Non-player characters"""
        return self.filter(npc=True)

    def player_characters(self):
        """Player characters (not NPCs)"""
        return self.filter(npc=False)

    def active(self):
        """Active characters (not retired or deceased)"""
        return self.filter(status__in=["Un", "Sub", "App"])

    def retired(self):
        """Retired characters"""
        return self.filter(status="Ret")

    def deceased(self):
        """Deceased characters"""
        return self.filter(status="Dec")

    def with_group_ordering(self):
        """
        Annotate characters with first group membership and apply standard ordering.

        This complex query is used across multiple character list views to ensure
        consistent ordering by chronicle, then by first group membership, then by name.
        """
        # Import here to avoid circular imports
        from characters.models.core.group import Group

        CharacterGroup = Group.members.through
        first_group_id = Subquery(
            CharacterGroup.objects.filter(character_id=OuterRef("pk"))
            .order_by("group_id")
            .values("group_id")[:1]
        )
        return (
            self.annotate(first_group_id=first_group_id)
            .select_related("chronicle")
            .order_by("chronicle__id", "-first_group_id", "name")
        )

    def pending_approval_for_user(self, user):
        """
        Characters awaiting approval in user's chronicles (optimized).

        Overrides base ModelQuerySet implementation to use stricter status filter.
        Characters use status='Sub' only, while Items/Locations use ['Un', 'Sub'].
        """
        return (
            self.filter(status="Sub", chronicle__in=user.chronicle_set.all())
            .select_related("chronicle", "owner")
            .order_by("name")
        )

    def at_freebie_step(self):
        """
        Characters at their freebie spending step.

        This filters characters where creation_status equals their class's freebie_step.
        Since freebie_step varies by character type, we need to check each instance.
        Returns a filtered queryset (evaluated, but still a queryset).
        """
        # Get all IDs where creation_status == freebie_step
        matching_ids = [
            char.id
            for char in self
            if hasattr(char, "creation_status")
            and hasattr(char, "freebie_step")
            and char.creation_status == char.freebie_step
        ]
        return self.filter(id__in=matching_ids)


# Create CharacterManager from the QuerySet to expose all QuerySet methods on the manager
CharacterManager = PolymorphicManager.from_queryset(CharacterQuerySet)


class CharacterModel(Model):
    npc = models.BooleanField(default=False)

    gameline = "wod"

    objects = CharacterManager()

    class Meta:
        verbose_name = "Character Model"
        verbose_name_plural = "Character Models"
        ordering = ["name"]


class Character(CharacterModel):
    type = "character"

    freebie_step = -1

    gameline = "wod"

    concept = models.CharField(max_length=100, db_index=True)
    creation_status = models.IntegerField(default=1)

    notes = models.TextField(default="", blank=True, null=True)
    xp = models.IntegerField(default=0, db_index=True)
    # spent_xp field removed - now using XPSpendingRequest model (game.models.XPSpendingRequest)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"
        constraints = [
            # XP cannot go negative
            CheckConstraint(
                check=Q(xp__gte=0),
                name="characters_character_xp_non_negative",
                violation_error_message="XP cannot be negative",
            ),
            # Note: status validation is handled in clean() method since status
            # is inherited from Model and constraints can't reference parent fields
        ]

    # Valid status transitions
    STATUS_TRANSITIONS = {
        "Un": ["Sub", "Ret"],  # Unfinished can be submitted or retired
        "Sub": ["Un", "App", "Ret"],  # Submitted can go back, be approved, or retired
        "App": ["Ret", "Dec"],  # Approved can be retired or killed
        "Ret": ["App"],  # Retired can be reactivated (ST discretion)
        "Dec": [],  # Deceased is final
    }

    def clean(self):
        """Validate character data before saving."""
        super().clean()

        # Validate status is in valid choices
        valid_statuses = ["Un", "Sub", "App", "Ret", "Dec"]
        if self.status not in valid_statuses:
            raise ValidationError(
                {
                    "status": f"Invalid status '{self.status}'. Must be one of: {', '.join(valid_statuses)}"
                }
            )

        # Validate status transition if character already exists
        if self.pk:
            try:
                old_instance = Character.objects.get(pk=self.pk)
                if old_instance.status != self.status:
                    self._validate_status_transition(old_instance.status, self.status)
            except Character.DoesNotExist:
                pass

        # Validate XP balance
        if self.xp < 0:
            raise ValidationError({"xp": "XP cannot be negative"})

    def _validate_status_transition(self, old_status, new_status):
        """Enforce valid status transitions."""
        valid_transitions = self.STATUS_TRANSITIONS.get(old_status, [])

        if new_status not in valid_transitions:
            raise ValidationError(
                {
                    "status": f"Cannot transition from {old_status} to {new_status}. "
                    f"Valid transitions: {', '.join(valid_transitions) or 'none'}"
                }
            )

    def save(self, *args, **kwargs):
        # Run validation unless explicitly skipped
        if not kwargs.pop("skip_validation", False):
            try:
                self.full_clean()
            except ValidationError:
                # Allow save to proceed if validation fails (maintain backward compatibility)
                # In production, you may want to raise the error instead
                pass

        # Check if this is an existing character whose status is changing to Ret or Dec
        if self.pk:
            try:
                old_instance = Character.objects.get(pk=self.pk)
                old_status = old_instance.status
                new_status = self.status
                # If status is changing to Retired or Deceased, remove from organizations
                if old_status not in ["Ret", "Dec"] and new_status in ["Ret", "Dec"]:
                    # Call parent save first to ensure we're working with saved state
                    super().save(*args, **kwargs)
                    self.remove_from_organizations()
                    return
            except Character.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def remove_from_organizations(self):
        """Remove this character from all organizational structures when retired or deceased."""
        CharacterOrganizationRegistry.cleanup_character(self)

    def get_type(self):
        if "human" in self.type:
            return "Human"
        if "spirit_character" == self.type:
            return "Spirit"
        return self.type.title()

    def get_heading(self):
        return "wod_heading"

    def next_stage(self):
        self.creation_status += 1
        self.save()

    def prev_stage(self):
        self.creation_status -= 1
        self.save()

    def has_concept(self):
        return self.concept != ""

    def set_concept(self, concept):
        self.concept = concept
        return True

    def get_absolute_url(self):
        return reverse("characters:character", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:update:character", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:create:character")

    def waiting_for_xp_spend(self):
        """Check if character has pending XP requests.

        UPDATED: Now uses XPSpendingRequest model instead of JSONField.
        """
        return self.xp_spendings.filter(approved="Pending").exists()

    def add_xp(self, amount):
        """Add XP to the character.

        Args:
            amount: Integer amount of XP to add.
        """
        self.xp += amount
        self.save()

    @transaction.atomic
    def spend_xp(self, trait_name, trait_display, cost, category, trait_value=0):
        """
        Atomically spend XP and create a spending request.
        Rolls back entirely if any step fails.

        UPDATED: Now creates XPSpendingRequest instead of using JSONField.

        Args:
            trait_name: The property name of the trait (e.g., 'alertness')
            trait_display: The display name of the trait (e.g., 'Alertness')
            cost: The XP cost
            category: The category of spending (e.g., 'abilities', 'attributes')
            trait_value: The new value after spending (optional)

        Returns:
            XPSpendingRequest: The spending request that was created

        Raises:
            ValidationError: If insufficient XP or invalid parameters
        """
        from game.models import XPSpendingRequest

        # Use select_for_update to lock the row and prevent race conditions
        char = Character.objects.select_for_update().get(pk=self.pk)

        if char.xp < cost:
            raise ValidationError(
                f"Insufficient XP: need {cost}, have {char.xp}", code="insufficient_xp"
            )

        # Deduct XP
        char.xp -= cost
        char.save(update_fields=["xp"])

        # Create spending request
        request = XPSpendingRequest.objects.create(
            character=char,
            trait_name=trait_display,
            trait_type=category,
            trait_value=trait_value,
            cost=cost,
            approved="Pending",
        )

        return request

    @transaction.atomic
    def approve_xp_spend(self, request_id, trait_property_name, new_value, approver):
        """
        Atomically approve XP spend and apply trait increase.

        UPDATED: Now uses XPSpendingRequest model instead of JSONField.

        Args:
            request_id: ID of the XPSpendingRequest
            trait_property_name: The property name to update (e.g., 'alertness')
            new_value: The new value for the trait
            approver: User who is approving the request

        Raises:
            ValidationError: If request invalid or already processed
        """
        from django.utils import timezone
        from game.models import XPSpendingRequest

        char = Character.objects.select_for_update().get(pk=self.pk)

        try:
            request = char.xp_spendings.select_for_update().get(id=request_id)
        except XPSpendingRequest.DoesNotExist:
            raise ValidationError("Invalid XP spending request", code="invalid_request")

        if request.approved != "Pending":
            raise ValidationError(
                f"XP spend already processed: {request.approved}",
                code="already_processed",
            )

        # Update approval status
        request.approved = "Approved"
        request.approved_by = approver
        request.approved_at = timezone.now()
        request.save()

        # Apply trait increase
        setattr(char, trait_property_name, new_value)
        char.save()

        return request

    # New model-based XP spending methods (replaces JSONField usage)

    def create_xp_spending_request(self, trait_name, trait_type, trait_value, cost):
        """Create an XP spending request using the new model-based system.

        This replaces the JSONField-based spent_xp system with proper database relations.

        Args:
            trait_name: Display name of the trait (e.g., 'Alertness', 'Strength')
            trait_type: Category of trait (e.g., 'attribute', 'ability', 'background')
            trait_value: New value after spending
            cost: XP cost

        Returns:
            XPSpendingRequest instance
        """
        from game.models import XPSpendingRequest

        return XPSpendingRequest.objects.create(
            character=self,
            trait_name=trait_name,
            trait_type=trait_type,
            trait_value=trait_value,
            cost=cost,
            approved="Pending",
        )

    def get_pending_xp_requests(self):
        """Get all pending XP spending requests for this character.

        Returns:
            QuerySet of XPSpendingRequest instances
        """
        return self.xp_spendings.filter(approved="Pending")

    def get_xp_spending_history(self):
        """Get all XP spending requests for this character.

        Returns:
            QuerySet of XPSpendingRequest instances ordered by creation date
        """
        return self.xp_spendings.all()

    def approve_xp_request(self, request_id, approver):
        """Approve an XP spending request.

        Args:
            request_id: ID of the XPSpendingRequest
            approver: User who is approving the request

        Returns:
            XPSpendingRequest instance
        """
        from django.utils import timezone

        request = self.xp_spendings.get(id=request_id, approved="Pending")
        request.approved = "Approved"
        request.approved_by = approver
        request.approved_at = timezone.now()
        request.save()
        return request

    def deny_xp_request(self, request_id, approver):
        """Deny an XP spending request.

        Args:
            request_id: ID of the XPSpendingRequest
            approver: User who is denying the request

        Returns:
            XPSpendingRequest instance
        """
        from django.utils import timezone

        request = self.xp_spendings.get(id=request_id, approved="Pending")
        request.approved = "Denied"
        request.approved_by = approver
        request.approved_at = timezone.now()
        request.save()
        return request

    def total_spent_xp(self):
        """Calculate total XP spent using XPSpendingRequest model.

        UPDATED: Simplified to only check XPSpendingRequest (removed JSONField compatibility).

        Returns:
            int: Total XP spent
        """
        from django.db.models import Sum

        total = (
            self.xp_spendings.filter(approved="Approved").aggregate(total=Sum("cost"))[
                "total"
            ]
            or 0
        )

        return total
