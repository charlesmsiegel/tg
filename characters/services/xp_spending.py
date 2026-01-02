"""
XP Spending Service for World of Darkness characters.

This module provides a service layer for handling XP spending operations,
replacing the monolithic post() method with a clean handler registry pattern.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional

from django.core.exceptions import ValidationError


@dataclass
class XPSpendResult:
    """Result of an XP spending operation."""

    success: bool
    trait: str
    cost: int
    message: str
    error: Optional[str] = None


class XPSpendingService:
    """
    Base service class for XP spending operations.

    Uses a handler registry pattern to dispatch spending operations
    to appropriate handler methods based on category.
    """

    # Handler registry - maps category names to handler method names
    _handlers: dict[str, str] = {}

    def __init__(self, character):
        """
        Initialize the service with a character.

        Args:
            character: The character spending XP
        """
        self.character = character

    @classmethod
    def register(cls, category: str) -> Callable:
        """
        Decorator to register a handler for a category.

        Args:
            category: The category name this handler processes

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            cls._handlers[category] = func.__name__
            return func

        return decorator

    def spend(
        self,
        category: str,
        example: Any,
        value: Optional[int] = None,
        note: str = "",
        pooled: bool = False,
        resonance: str = "",
    ) -> XPSpendResult:
        """
        Spend XP on a trait.

        Args:
            category: The category of spending (e.g., "Attribute", "Ability")
            example: The trait object (Attribute, Ability, Sphere, etc.)
            value: Optional explicit value for the trait
            note: Optional note for backgrounds
            pooled: Whether this is pooled spending
            resonance: Resonance name for resonance spending

        Returns:
            XPSpendResult with success/failure info
        """
        handler_name = self._handlers.get(category)
        if handler_name is None:
            return XPSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=f"Unknown XP category: {category}",
            )

        handler = getattr(self, handler_name, None)
        if handler is None:
            return XPSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=f"Handler not implemented: {handler_name}",
            )

        try:
            return handler(
                example=example, value=value, note=note, pooled=pooled, resonance=resonance
            )
        except ValidationError as e:
            return XPSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=str(e),
            )


class MageXPSpendingService(XPSpendingService):
    """
    XP spending service for Mage characters.

    Handles all Mage-specific XP spending categories including
    Spheres, Arete, Practices, Tenets, and Resonance.
    """

    _handlers: dict[str, str] = {}

    @XPSpendingService.register("Attribute")
    def _handle_attribute(self, example, **kwargs) -> XPSpendResult:
        """Handle attribute XP spending."""
        trait = example.name
        trait_type = "attribute"
        current_value = getattr(self.character, example.property_name)
        new_value = current_value + 1
        cost = self.character.xp_cost("attribute", current_value)

        self.character.spend_xp(
            trait_name=example.property_name,
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @XPSpendingService.register("Ability")
    def _handle_ability(self, example, **kwargs) -> XPSpendResult:
        """Handle ability XP spending."""
        trait = example.name
        trait_type = "ability"
        current_value = getattr(self.character, example.property_name)
        new_value = current_value + 1
        cost = self.character.xp_cost("ability", current_value)

        self.character.spend_xp(
            trait_name=example.property_name,
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @XPSpendingService.register("New Background")
    def _handle_new_background(self, example, note="", **kwargs) -> XPSpendResult:
        """Handle new background XP spending."""
        if note:
            trait = example.name + f" ({note})"
        else:
            trait = example.name
        trait_type = "new-background"
        new_value = 1
        cost = self.character.xp_cost("new background", new_value)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on new background {trait}",
        )

    @XPSpendingService.register("Existing Background")
    def _handle_existing_background(self, example, **kwargs) -> XPSpendResult:
        """Handle existing background XP spending."""
        trait = example.bg.name + f" ({example.note})"
        trait_type = "background"
        current_value = example.rating
        new_value = current_value + 1
        cost = self.character.xp_cost("background", current_value)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @XPSpendingService.register("Willpower")
    def _handle_willpower(self, **kwargs) -> XPSpendResult:
        """Handle willpower XP spending."""
        trait = "Willpower"
        trait_type = "willpower"
        current_value = self.character.willpower
        new_value = current_value + 1
        cost = self.character.xp_cost("willpower", current_value)

        self.character.spend_xp(
            trait_name="willpower",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Willpower",
        )

    @XPSpendingService.register("MeritFlaw")
    def _handle_merit_flaw(self, example, value=None, **kwargs) -> XPSpendResult:
        """Handle merit/flaw XP spending."""
        current_rating = self.character.mf_rating(example)
        trait = example.name
        trait_type = "meritflaw"
        cost = self.character.xp_cost("meritflaw", value - current_rating)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @XPSpendingService.register("Sphere")
    def _handle_sphere(self, example, **kwargs) -> XPSpendResult:
        """Handle sphere XP spending."""
        trait = example.name
        trait_type = "sphere"
        current_value = getattr(self.character, example.property_name)
        new_value = current_value + 1
        cost = self.character.xp_cost(
            self.character.sphere_to_trait_type(example.property_name),
            current_value,
        )

        self.character.spend_xp(
            trait_name=example.property_name,
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @XPSpendingService.register("Rote Points")
    def _handle_rote_points(self, **kwargs) -> XPSpendResult:
        """Handle rote points XP spending."""
        trait = "Rote Points"
        trait_type = "rotes"
        cost = self.character.xp_cost("rotes", 1)
        new_value = self.character.total_effects() + self.character.rote_points + 3

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Rote Points",
        )

    @XPSpendingService.register("Resonance")
    def _handle_resonance(self, resonance="", **kwargs) -> XPSpendResult:
        """Handle resonance XP spending."""
        from characters.models.mage.resonance import Resonance

        trait = f"Resonance ({resonance})"
        r = Resonance.objects.get_or_create(name=resonance)[0]
        trait_type = "resonance"
        current_value = self.character.resonance_rating(r)
        cost = self.character.xp_cost("resonance", current_value)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=current_value + 1,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @XPSpendingService.register("Tenet")
    def _handle_tenet(self, example, **kwargs) -> XPSpendResult:
        """Handle tenet XP spending."""
        trait = example.name
        trait_type = "tenet"
        cost = self.character.xp_cost("tenet", 1)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=0,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on tenet {trait}",
        )

    @XPSpendingService.register("Remove Tenet")
    def _handle_remove_tenet(self, example, **kwargs) -> XPSpendResult:
        """Handle tenet removal XP spending."""
        trait = "Remove " + example.name
        trait_type = "remove tenet"
        cost = self.character.xp_cost("remove tenet", self.character.other_tenets.count() + 3)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=0,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on removing tenet",
        )

    @XPSpendingService.register("Practice")
    def _handle_practice(self, example, **kwargs) -> XPSpendResult:
        """Handle practice XP spending."""
        trait = example.name
        trait_type = "practice"
        current_value = self.character.practice_rating(example)
        new_value = current_value + 1
        cost = self.character.xp_cost("practice", current_value)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @XPSpendingService.register("Arete")
    def _handle_arete(self, **kwargs) -> XPSpendResult:
        """Handle Arete XP spending."""
        trait = "Arete"
        trait_type = "arete"
        current_value = self.character.arete
        new_value = current_value + 1
        cost = self.character.xp_cost("arete", current_value)

        self.character.spend_xp(
            trait_name="arete",
            trait_display=trait,
            cost=cost,
            category=trait_type,
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Arete",
        )


# Register handlers for MageXPSpendingService
MageXPSpendingService._handlers = {
    "Attribute": "_handle_attribute",
    "Ability": "_handle_ability",
    "New Background": "_handle_new_background",
    "Existing Background": "_handle_existing_background",
    "Willpower": "_handle_willpower",
    "MeritFlaw": "_handle_merit_flaw",
    "Sphere": "_handle_sphere",
    "Rote Points": "_handle_rote_points",
    "Resonance": "_handle_resonance",
    "Tenet": "_handle_tenet",
    "Remove Tenet": "_handle_remove_tenet",
    "Practice": "_handle_practice",
    "Arete": "_handle_arete",
}
