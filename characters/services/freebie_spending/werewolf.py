"""
Werewolf gameline Freebie Spending Services.

This module provides freebie spending services for Werewolf: The Apocalypse characters:
- WtAHumanFreebieSpendingService - base for Werewolf gameline humans
- GarouFreebieSpendingService - Werewolves with Gifts, Rites, Rage, Gnosis
- KinfolkFreebieSpendingService - Werewolf kin (limited/no Gifts)
- FeraFreebieSpendingService - Base for all Changing Breeds
- Per-breed services for each Fera type
"""

from django.utils import timezone

from .base import (
    FreebieApplyResult,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    applier,
    handler,
)


class WtAHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Werewolf gameline humans.

    Inherits all common human handlers. Currently no additional
    WtA-gameline-specific traits for mortals.
    """

    pass


class GarouFreebieSpendingService(WtAHumanFreebieSpendingService):
    """
    Freebie spending service for Garou (Werewolf) characters.

    Handles Garou-specific freebie spending categories including
    Gifts, Rites, Rage, and Gnosis.

    Note: Renown (Glory, Honor, Wisdom) can be spent with freebies at creation.
    """

    @handler("Gift")
    def _handle_gift(self, example, **kwargs) -> FreebieSpendResult:
        """Handle gift freebie spending."""
        trait = example.name
        cost = self.character.freebie_cost("gift")
        gift_level = example.rank if hasattr(example, "rank") else 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.gifts.add(example)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "gift", gift_level, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Gift: {trait}",
        )

    @handler("Rite")
    def _handle_rite(self, example, **kwargs) -> FreebieSpendResult:
        """Handle rite freebie spending."""
        trait = example.name
        # Rite cost is typically per level
        rite_level = example.level if hasattr(example, "level") else 1
        cost = self.character.freebie_cost("rite") * rite_level

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.rites.add(example)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "rite", rite_level, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Rite: {trait}",
        )

    @handler("Rage")
    def _handle_rage(self, **kwargs) -> FreebieSpendResult:
        """Handle Rage freebie spending."""
        trait = "Rage"
        cost = self.character.freebie_cost("rage")
        current_value = self.character.rage
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
                error="Rage at maximum",
            )

        # Apply the change
        self.character.rage = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "rage", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Rage",
        )

    @handler("Gnosis")
    def _handle_gnosis(self, **kwargs) -> FreebieSpendResult:
        """Handle Gnosis freebie spending."""
        trait = "Gnosis"
        cost = self.character.freebie_cost("gnosis")
        current_value = self.character.gnosis
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
                error="Gnosis at maximum",
            )

        # Apply the change
        self.character.gnosis = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "gnosis", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Gnosis",
        )

    @handler("Glory")
    def _handle_glory(self, **kwargs) -> FreebieSpendResult:
        """Handle Glory (temporary renown) freebie spending."""
        trait = "Glory"
        cost = self.character.freebie_cost("glory")
        current_value = self.character.temporary_glory
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.temporary_glory = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "glory", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Glory",
        )

    @handler("Honor")
    def _handle_honor(self, **kwargs) -> FreebieSpendResult:
        """Handle Honor (temporary renown) freebie spending."""
        trait = "Honor"
        cost = self.character.freebie_cost("honor")
        current_value = self.character.temporary_honor
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.temporary_honor = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "honor", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Honor",
        )

    @handler("Wisdom")
    def _handle_wisdom(self, **kwargs) -> FreebieSpendResult:
        """Handle Wisdom (temporary renown) freebie spending."""
        trait = "Wisdom"
        cost = self.character.freebie_cost("wisdom")
        current_value = self.character.temporary_wisdom
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.temporary_wisdom = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "wisdom", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Wisdom",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("gift")
    def _apply_gift(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved gift freebie spending."""
        if deny:
            from characters.models.werewolf.gift import Gift

            gift = Gift.objects.filter(name=freebie_request.trait_name).first()
            if gift:
                self.character.gifts.remove(gift)
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed Gift {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved Gift: {freebie_request.trait_name}",
        )

    @applier("rite")
    def _apply_rite(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved rite freebie spending."""
        if deny:
            from characters.models.werewolf.rite import Rite

            rite = Rite.objects.filter(name=freebie_request.trait_name).first()
            if rite:
                self.character.rites.remove(rite)
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed Rite {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved Rite: {freebie_request.trait_name}",
        )

    @applier("rage")
    def _apply_rage(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Rage freebie spending."""
        if deny:
            if self.character.rage > 1:
                self.character.rage -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Rage",
                message="Denied and reverted Rage",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Rage",
            message="Approved Rage",
        )

    @applier("gnosis")
    def _apply_gnosis(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Gnosis freebie spending."""
        if deny:
            if self.character.gnosis > 1:
                self.character.gnosis -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Gnosis",
                message="Denied and reverted Gnosis",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Gnosis",
            message="Approved Gnosis",
        )

    @applier("glory")
    def _apply_glory(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Glory freebie spending."""
        if deny:
            if self.character.temporary_glory > 0:
                self.character.temporary_glory -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Glory",
                message="Denied and reverted Glory",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Glory",
            message="Approved Glory",
        )

    @applier("honor")
    def _apply_honor(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Honor freebie spending."""
        if deny:
            if self.character.temporary_honor > 0:
                self.character.temporary_honor -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Honor",
                message="Denied and reverted Honor",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Honor",
            message="Approved Honor",
        )

    @applier("wisdom")
    def _apply_wisdom(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Wisdom freebie spending."""
        if deny:
            if self.character.temporary_wisdom > 0:
                self.character.temporary_wisdom -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Wisdom",
                message="Denied and reverted Wisdom",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Wisdom",
            message="Approved Wisdom",
        )


class KinfolkFreebieSpendingService(WtAHumanFreebieSpendingService):
    """
    Freebie spending service for Kinfolk characters.

    Kinfolk are human relatives of werewolves. They typically
    don't have access to Gifts, Rage, or Gnosis.
    """

    pass


class FeraFreebieSpendingService(GarouFreebieSpendingService):
    """
    Base Freebie spending service for Fera (Changing Breeds).

    Fera share the same basic freebie categories as Garou:
    Gifts, Rites, Rage, Gnosis. Breed-specific variations
    can be added in subclasses.
    """

    pass


class BastetFreebieSpendingService(FeraFreebieSpendingService):
    """Freebie spending service for Bastet (Werecats)."""

    pass


class CoraxFreebieSpendingService(FeraFreebieSpendingService):
    """Freebie spending service for Corax (Wereravens)."""

    pass


class GurahlFreebieSpendingService(FeraFreebieSpendingService):
    """Freebie spending service for Gurahl (Werebears)."""

    pass


class MokoleFreebieSpendingService(FeraFreebieSpendingService):
    """Freebie spending service for Mokole (Werelizards)."""

    pass


class NuwishaFreebieSpendingService(FeraFreebieSpendingService):
    """Freebie spending service for Nuwisha (Werecoyotes)."""

    pass


class RatkinFreebieSpendingService(FeraFreebieSpendingService):
    """Freebie spending service for Ratkin (Wererats)."""

    pass


# Register Werewolf gameline character types
FreebieSpendingServiceFactory.register("wta_human", WtAHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("werewolf", GarouFreebieSpendingService)
FreebieSpendingServiceFactory.register("kinfolk", KinfolkFreebieSpendingService)
FreebieSpendingServiceFactory.register("fera", FeraFreebieSpendingService)
FreebieSpendingServiceFactory.register("bastet", BastetFreebieSpendingService)
FreebieSpendingServiceFactory.register("corax", CoraxFreebieSpendingService)
FreebieSpendingServiceFactory.register("gurahl", GurahlFreebieSpendingService)
FreebieSpendingServiceFactory.register("mokole", MokoleFreebieSpendingService)
FreebieSpendingServiceFactory.register("nuwisha", NuwishaFreebieSpendingService)
FreebieSpendingServiceFactory.register("ratkin", RatkinFreebieSpendingService)
