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
        Uses database-level filtering with polymorphic_ctype to avoid loading all
        characters into memory.
        """
        # Map of character model names to their freebie_step values
        # This must match the freebie_step class attributes defined in each character type
        freebie_step_map = {
            # Humans (step 5)
            "vtmhuman": 5,
            "wtahuman": 5,
            "mtahuman": 5,
            "wtohuman": 5,
            "ctdhuman": 5,
            "dtfhuman": 5,
            "companion": 5,
            "kinfolk": 5,
            "werewolf": 5,  # inherits from WtAHuman
            "fomor": 5,  # inherits from WtAHuman
            # Step 6
            "ghoul": 6,
            "changeling": 6,
            "thrall": 6,
            # Step 7
            "vampire": 7,
            "wraith": 7,
            "mage": 7,
            "demon": 7,
            "earthbound": 7,
            # Step 8 - Fera and Sorcerers
            "fera": 8,
            "bastet": 8,  # inherits from Fera
            "corax": 8,  # inherits from Fera
            "gurahl": 8,  # inherits from Fera
            "mokole": 8,  # inherits from Fera
            "nuwisha": 8,  # inherits from Fera
            "ratkin": 8,  # inherits from Fera
            "sorcerer": 8,
            "linearsorcerer": 8,
        }

        # Build Q objects for each character type
        q_objects = Q()
        for model_name, freebie_step in freebie_step_map.items():
            q_objects |= Q(polymorphic_ctype__model=model_name, creation_status=freebie_step)

        return self.filter(q_objects)


# Create CharacterManager from ModelManager to inherit polymorphic_ctype optimization
CharacterManager = ModelManager.from_queryset(CharacterQuerySet)


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

    concept = models.CharField(max_length=100, db_index=True, default="", blank=True)
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
            # Note: Status constraint removed - 'status' is inherited from core.Model
            # and constraints can't reference non-local fields in multi-table inheritance.
            # Status validation is handled by Django field choices and clean() method.
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
        """
        Validate character data before saving.

        Status value validation is handled by:
        - Django field choices (soft validation)
        - Database constraint (hard validation via migration)

        XP balance validation is handled by database constraint
        (characters_character_xp_non_negative).

        This method focuses on status transition validation (state machine logic).
        """
        super().clean()

        # Validate status transition if character already exists
        if self.pk:
            try:
                old_instance = Character.objects.get(pk=self.pk)
                if old_instance.status != self.status:
                    self._validate_status_transition(old_instance.status, self.status)
            except Character.DoesNotExist:
                pass

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
        """
        Save the character.

        Args:
            skip_validation: If True, skip model validation (full_clean). Use with caution.
                            This is useful for data migrations or bulk operations where you
                            need to bypass validation temporarily. Handled by core.Model.save().

        Raises:
            ValidationError: If validation fails (unless skip_validation=True)
        """
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
        return self.type.replace("_", " ").title()

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

    @transaction.atomic
    def add_xp(self, amount):
        """Add XP to the character atomically.

        Uses select_for_update to prevent race conditions when multiple
        requests try to add XP simultaneously.

        Args:
            amount: Integer amount of XP to add.
        """
        # Use select_for_update to lock the row and prevent race conditions
        char = Character.objects.select_for_update().get(pk=self.pk)
        char.xp += amount
        char.save(update_fields=["xp"])
        # Update self to reflect the change
        self.xp = char.xp

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
            self.xp_spendings.filter(approved="Approved").aggregate(total=Sum("cost"))["total"] or 0
        )

        return total

    def total_xp(self):
        """Calculate total XP (earned XP).

        Returns:
            int: Total XP earned by this character
        """
        return self.xp

    def available_xp(self):
        """Calculate available (unspent) XP.

        This returns the current XP pool which already accounts for spending
        (XP is deducted when a spending request is created).

        Returns:
            int: Available XP to spend
        """
        return self.xp
