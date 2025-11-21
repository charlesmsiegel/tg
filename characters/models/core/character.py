from core.models import Model, ModelManager, ModelQuerySet
from django.db import models
from django.db.models import OuterRef, Subquery
from django.urls import reverse
from polymorphic.managers import PolymorphicManager


class CharacterQuerySet(ModelQuerySet):
    """Custom queryset for Character with chainable query patterns."""

    def npcs(self):
        """Non-player characters"""
        return self.filter(npc=True)

    def player_characters(self):
        """Player characters (not NPCs)"""
        return self.filter(npc=False)

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
        """Characters awaiting approval in user's chronicles (optimized for items vs characters)"""
        # Characters use status='Sub' only, items use status in ['Un', 'Sub']
        return (
            self.filter(status="Sub", chronicle__in=user.chronicle_set.all())
            .select_related("chronicle", "owner")
            .order_by("name")
        )


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

    concept = models.CharField(max_length=100)
    creation_status = models.IntegerField(default=1)

    notes = models.TextField(default="", blank=True, null=True)
    xp = models.IntegerField(default=0)
    spent_xp = models.JSONField(default=list)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def save(self, *args, **kwargs):
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
        # Import here to avoid circular imports
        from characters.models.core.group import Group

        # Remove from Group memberships
        for group in Group.objects.filter(members=self):
            group.members.remove(self)

        # Remove from Group leadership positions
        for group in Group.objects.filter(leader=self):
            group.leader = None
            group.save()

        # Handle Human-specific relationships (Chantry)
        # Check if this character is a Human (or subclass) for Chantry relations
        if hasattr(self, "member_of"):
            # Remove from Chantry memberships
            for chantry in self.member_of.all():
                chantry.members.remove(self)

        if hasattr(self, "chantry_leader_at"):
            # Remove from Chantry leadership
            for chantry in self.chantry_leader_at.all():
                chantry.leaders.remove(self)

        if hasattr(self, "ambassador_from"):
            # Remove from ambassador positions
            for chantry in self.ambassador_from.all():
                chantry.ambassador = None
                chantry.save()

        if hasattr(self, "tends_node_at"):
            # Remove from node tender positions
            for chantry in self.tends_node_at.all():
                chantry.node_tender = None
                chantry.save()

        if hasattr(self, "investigator_at"):
            # Remove from investigator roles
            for chantry in self.investigator_at.all():
                chantry.investigator.remove(self)

        if hasattr(self, "guardian_of"):
            # Remove from guardian roles
            for chantry in self.guardian_of.all():
                chantry.guardian.remove(self)

        if hasattr(self, "teacher_at"):
            # Remove from teacher roles
            for chantry in self.teacher_at.all():
                chantry.teacher.remove(self)

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

    def xp_spend_record(self, trait, trait_type, value, cost=None):
        if cost is None:
            cost = self.xp_cost(trait_type, value)
        return {
            "index": f"{self.id}_{trait_type}_{trait}_{value}".replace(" ", "-"),
            "trait": trait,
            "value": value,
            "cost": cost,
            "approved": "Pending",
        }

    def waiting_for_xp_spend(self):
        for d in self.spent_xp:
            if d["approved"] == "Pending":
                return True
        return False

    def add_xp(self, amount):
        """Add XP to the character.

        Args:
            amount: Integer amount of XP to add.
        """
        self.xp += amount
        self.save()

    def add_to_spend(self, trait, value, cost):
        """Add an XP expenditure record to the spent_xp list.

        Args:
            trait: Name of the trait being increased (string)
            value: New value of the trait after spending
            cost: XP cost of the expenditure
        """
        record = self.xp_spend_record(trait, trait, value, cost)
        self.spent_xp.append(record)
        self.save()
