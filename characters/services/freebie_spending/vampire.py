"""
Vampire gameline Freebie Spending Services.

This module provides freebie spending services for Vampire: The Masquerade characters:
- VtMHumanFreebieSpendingService - base for Vampire gameline humans (includes Virtues)
- VampireFreebieSpendingService - Kindred with Disciplines and Morality
- GhoulFreebieSpendingService - Blood-bound mortals with limited Disciplines
- RevenantFreebieSpendingService - Born ghouls with family Disciplines
"""

from characters.costs import get_freebie_cost
from django.utils import timezone

from .base import (
    FreebieApplyResult,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    applier,
    handler,
)


class VtMHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Vampire gameline humans.

    Adds Virtue handling for mortals in the VtM setting.
    Virtues: Conscience, Self-Control, Courage (or Conviction, Instinct for some paths)
    """

    @handler("Virtue")
    def _handle_virtue(self, example, **kwargs) -> FreebieSpendResult:
        """Handle virtue freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = get_freebie_cost("virtue")

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value > 5:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Virtue at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "virtue", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("virtue")
    def _apply_virtue(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved virtue freebie spending."""
        if deny:
            from characters.models.core.virtue import Virtue

            virtue = Virtue.objects.filter(name=freebie_request.trait_name).first()
            if virtue:
                current_val = getattr(self.character, virtue.property_name, 1)
                if current_val > 1:
                    setattr(self.character, virtue.property_name, current_val - 1)
                    self.character.save()
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and reverted {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved {freebie_request.trait_name}",
        )


class VampireFreebieSpendingService(VtMHumanFreebieSpendingService):
    """
    Freebie spending service for Vampire characters.

    Handles Vampire-specific freebie spending categories including
    Disciplines, and Morality (Humanity or Path).
    Inherits Virtue handling from VtMHumanFreebieSpendingService.
    """

    @handler("Discipline")
    def _handle_discipline(self, example, **kwargs) -> FreebieSpendResult:
        """Handle discipline freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name, 0)
        new_value = current_value + 1

        # Determine if this is a clan discipline or out-of-clan
        is_clan = self.character.is_clan_discipline(example)
        cost = get_freebie_cost("discipline" if is_clan else "out_of_clan_discipline")

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value > 5:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Discipline at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "discipline", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Humanity")
    def _handle_humanity(self, **kwargs) -> FreebieSpendResult:
        """Handle Humanity freebie spending."""
        trait = "Humanity"
        cost = get_freebie_cost("humanity")
        current_value = self.character.humanity
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value > 10:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Humanity at maximum",
            )

        # Apply the change
        self.character.humanity = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "humanity", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Path Rating")
    def _handle_path_rating(self, **kwargs) -> FreebieSpendResult:
        """Handle Path rating freebie spending (for characters on Paths of Enlightenment)."""
        if not hasattr(self.character, "path") or not self.character.path:
            return FreebieSpendResult(
                success=False,
                trait="Path Rating",
                cost=0,
                message="",
                error="Character is not on a Path of Enlightenment",
            )

        trait = f"Path of {self.character.path.name}"
        cost = get_freebie_cost("path_rating")
        current_value = self.character.path_rating
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value > 10:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Path rating at maximum",
            )

        # Apply the change
        self.character.path_rating = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "path_rating", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("discipline")
    def _apply_discipline(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved discipline freebie spending."""
        if deny:
            from characters.models.vampire.discipline import Discipline

            discipline = Discipline.objects.filter(name=freebie_request.trait_name).first()
            if discipline:
                current_val = getattr(self.character, discipline.property_name, 0)
                if current_val > 0:
                    setattr(self.character, discipline.property_name, current_val - 1)
                    self.character.save()
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and reverted {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved {freebie_request.trait_name}",
        )

    @applier("humanity")
    def _apply_humanity(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved humanity freebie spending."""
        if deny:
            if self.character.humanity > 1:
                self.character.humanity -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Humanity",
                message="Denied and reverted Humanity",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Humanity",
            message="Approved Humanity",
        )

    @applier("path_rating")
    def _apply_path_rating(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved path rating freebie spending."""
        if deny:
            if hasattr(self.character, "path_rating") and self.character.path_rating > 1:
                self.character.path_rating -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Path Rating",
                message="Denied and reverted Path Rating",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Path Rating",
            message="Approved Path Rating",
        )


class GhoulFreebieSpendingService(VampireFreebieSpendingService):
    """
    Freebie spending service for Ghoul characters.

    Ghouls have access to limited Disciplines based on their domitor's clan.
    They inherit the Discipline handler but may have restrictions applied
    at the form/view level.
    """

    pass


class RevenantFreebieSpendingService(VampireFreebieSpendingService):
    """
    Freebie spending service for Revenant characters.

    Revenants are born ghouls from special bloodlines with inherent
    access to certain family Disciplines.
    """

    pass


# Register Vampire gameline character types
FreebieSpendingServiceFactory.register("vtm_human", VtMHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("vampire", VampireFreebieSpendingService)
FreebieSpendingServiceFactory.register("ghoul", GhoulFreebieSpendingService)
FreebieSpendingServiceFactory.register("revenant", RevenantFreebieSpendingService)
