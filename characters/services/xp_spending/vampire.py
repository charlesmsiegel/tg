"""
Vampire gameline XP Spending Services.

This module provides XP spending services for Vampire: The Masquerade characters:
- VtMHumanXPSpendingService - base for Vampire gameline humans (includes Virtues)
- VampireXPSpendingService - Kindred with Disciplines and Morality
- GhoulXPSpendingService - Blood-bound mortals with limited Disciplines
- RevenantXPSpendingService - Born ghouls with family Disciplines
"""

from characters.costs import get_xp_cost
from django.utils import timezone

from .base import (
    HumanXPSpendingService,
    XPApplyResult,
    XPSpendingServiceFactory,
    XPSpendResult,
    applier,
    handler,
)


class VtMHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Vampire gameline humans.

    Adds Virtue handling for mortals in the VtM setting.
    Virtues: Conscience, Self-Control, Courage (or Conviction, Instinct for some paths)
    """

    @handler("Virtue")
    def _handle_virtue(self, example, **kwargs) -> XPSpendResult:
        """Handle virtue XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Calculate cost: 2 × current value
        cost = get_xp_cost("virtue") * current_value

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="virtue",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("virtue")
    def _apply_virtue(self, xp_request, approver) -> XPApplyResult:
        """Apply approved virtue XP spending."""
        from characters.models.core.virtue import Virtue

        virtue = Virtue.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, virtue.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )


class VampireXPSpendingService(VtMHumanXPSpendingService):
    """
    XP spending service for Vampire characters.

    Handles Vampire-specific XP spending categories including
    Disciplines, and Morality (Humanity or Path).
    Inherits Virtue handling from VtMHumanXPSpendingService.
    """

    @handler("Discipline")
    def _handle_discipline(self, example, **kwargs) -> XPSpendResult:
        """Handle discipline XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Determine if this is a clan discipline
        is_clan = self.character.is_clan_discipline(example)

        # Calculate cost: new=10, clan=5×current, out-of-clan=7×current
        if current_value == 0:
            cost = 10  # New discipline
        elif is_clan:
            cost = get_xp_cost("discipline") * current_value  # 5×current (clan)
        else:
            cost = 7 * current_value  # 7×current (out-of-clan)

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="discipline",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Morality")
    def _handle_morality(self, **kwargs) -> XPSpendResult:
        """Handle morality (Humanity or Path) XP spending."""
        # Check if character is on a Path or using Humanity
        if hasattr(self.character, "path") and self.character.path:
            trait = f"Path of {self.character.path.name}"
            property_name = "path_rating"
            cost_type = "path_rating"
        else:
            trait = "Humanity"
            property_name = "humanity"
            cost_type = "humanity"

        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Calculate cost: 1 × current value
        cost = get_xp_cost(cost_type) * current_value

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="morality",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("discipline")
    def _apply_discipline(self, xp_request, approver) -> XPApplyResult:
        """Apply approved discipline XP spending."""
        from characters.models.vampire.discipline import Discipline

        discipline = Discipline.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, discipline.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("morality")
    def _apply_morality(self, xp_request, approver) -> XPApplyResult:
        """Apply approved morality XP spending."""
        # Determine property based on trait name
        if "Path" in xp_request.trait_name:
            property_name = "path_rating"
        else:
            property_name = "humanity"

        self.character.approve_xp_spend(
            xp_request.id, property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )


class GhoulXPSpendingService(VampireXPSpendingService):
    """
    XP spending service for Ghoul characters.

    Ghouls have access to limited Disciplines based on their domitor's clan.
    They inherit the Discipline handler but may have restrictions applied
    at the form/view level.
    """

    pass


class RevenantXPSpendingService(VampireXPSpendingService):
    """
    XP spending service for Revenant characters.

    Revenants are born ghouls from special bloodlines with inherent
    access to certain family Disciplines.
    """

    pass


# Register Vampire gameline character types
XPSpendingServiceFactory.register("vtm_human", VtMHumanXPSpendingService)
XPSpendingServiceFactory.register("vampire", VampireXPSpendingService)
XPSpendingServiceFactory.register("ghoul", GhoulXPSpendingService)
XPSpendingServiceFactory.register("revenant", RevenantXPSpendingService)
