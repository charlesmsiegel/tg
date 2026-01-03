"""
XP Spending Service base classes and infrastructure.

This module provides the core architecture for XP spending operations,
including the metaclass for handler inheritance, factory pattern, and
the base HumanXPSpendingService with common handlers.

Also provides apply/deny infrastructure for processing approved/denied
XP spending requests.
"""

from dataclasses import dataclass
from typing import Any, Optional

from characters.costs import get_meritflaw_xp_cost, get_xp_cost
from django.core.exceptions import ValidationError
from django.utils import timezone


@dataclass
class XPSpendResult:
    """Result of an XP spending operation."""

    success: bool
    trait: str
    cost: int
    message: str
    error: Optional[str] = None


@dataclass
class XPApplyResult:
    """Result of applying or denying an XP spending request."""

    success: bool
    trait: str
    message: str
    error: Optional[str] = None


def handler(category: str):
    """
    Decorator to register a method as an XP spending handler for a category.

    Works with XPSpendingServiceMeta to properly register handlers per-class
    while supporting inheritance.

    Args:
        category: The category name this handler processes (e.g., "Attribute", "Ability")

    Returns:
        Decorator function that marks the method with its category
    """

    def decorator(func):
        func._xp_handler_category = category
        return func

    return decorator


def applier(category: str):
    """
    Decorator to register a method as an XP apply handler for a trait type.

    Works with XPSpendingServiceMeta to properly register appliers per-class
    while supporting inheritance. Used when approving XP spending requests.

    Args:
        category: The trait_type this applier processes (e.g., "attribute", "ability")
                  Must match the trait_type stored in XPSpendingRequest

    Returns:
        Decorator function that marks the method with its category
    """

    def decorator(func):
        func._xp_applier_category = category
        return func

    return decorator


class XPSpendingServiceMeta(type):
    """
    Metaclass that ensures each subclass gets its own handler and applier registries
    with parent handlers/appliers inherited.

    This fixes the broken decorator pattern in the original implementation
    where decorators modified the base class dict instead of the subclass.
    """

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Start with empty dicts for this class
        handlers = {}
        appliers = {}

        # Inherit handlers and appliers from parent classes
        for base in bases:
            if hasattr(base, "_handlers") and isinstance(base._handlers, dict):
                handlers.update(base._handlers)
            if hasattr(base, "_appliers") and isinstance(base._appliers, dict):
                appliers.update(base._appliers)

        # Register any methods decorated with @handler or @applier in this class
        for attr_name, attr_value in namespace.items():
            if hasattr(attr_value, "_xp_handler_category"):
                handlers[attr_value._xp_handler_category] = attr_name
            if hasattr(attr_value, "_xp_applier_category"):
                appliers[attr_value._xp_applier_category] = attr_name

        # Also check for handlers/appliers defined in the class after creation
        # (handles methods defined via other means)
        for attr_name in dir(cls):
            if attr_name.startswith("_"):
                try:
                    attr_value = getattr(cls, attr_name)
                    if hasattr(attr_value, "_xp_handler_category"):
                        if attr_value._xp_handler_category not in handlers:
                            handlers[attr_value._xp_handler_category] = attr_name
                    if hasattr(attr_value, "_xp_applier_category"):
                        if attr_value._xp_applier_category not in appliers:
                            appliers[attr_value._xp_applier_category] = attr_name
                except AttributeError:
                    pass

        cls._handlers = handlers
        cls._appliers = appliers
        return cls


class XPSpendingService(metaclass=XPSpendingServiceMeta):
    """
    Abstract base service class for XP spending operations.

    Uses a handler registry pattern with proper inheritance support
    via the XPSpendingServiceMeta metaclass.

    Provides:
    - spend(): Create pending XP spending requests
    - apply(): Apply approved XP spending requests
    - deny(): Deny and refund XP spending requests
    """

    _handlers: dict[str, str] = {}
    _appliers: dict[str, str] = {}

    def __init__(self, character):
        """
        Initialize the service with a character.

        Args:
            character: The character spending XP
        """
        self.character = character

    def spend(
        self,
        category: str,
        example: Any = None,
        value: Optional[int] = None,
        note: str = "",
        **kwargs,
    ) -> XPSpendResult:
        """
        Spend XP on a trait.

        Args:
            category: The category of spending (e.g., "Attribute", "Ability")
            example: The trait object (Attribute, Ability, Sphere, etc.)
            value: Optional explicit value for the trait
            note: Optional note for backgrounds
            **kwargs: Additional arguments passed to handler

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

        handler_method = getattr(self, handler_name, None)
        if handler_method is None:
            return XPSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=f"Handler not implemented: {handler_name}",
            )

        try:
            return handler_method(example=example, value=value, note=note, **kwargs)
        except ValidationError as e:
            return XPSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=str(e),
            )

    def apply(self, xp_request, approver) -> XPApplyResult:
        """
        Apply an approved XP spending request.

        Looks up the appropriate applier based on the request's trait_type,
        then applies the trait change to the character.

        Args:
            xp_request: XPSpendingRequest instance to apply
            approver: User approving the request

        Returns:
            XPApplyResult with success/failure info
        """
        trait_type = xp_request.trait_type
        applier_name = self._appliers.get(trait_type)

        if applier_name is None:
            return XPApplyResult(
                success=False,
                trait=xp_request.trait_name,
                message="",
                error=f"Unknown trait type for apply: {trait_type}",
            )

        applier_method = getattr(self, applier_name, None)
        if applier_method is None:
            return XPApplyResult(
                success=False,
                trait=xp_request.trait_name,
                message="",
                error=f"Applier not implemented: {applier_name}",
            )

        try:
            return applier_method(xp_request=xp_request, approver=approver)
        except Exception as e:
            return XPApplyResult(
                success=False,
                trait=xp_request.trait_name,
                message="",
                error=str(e),
            )

    def deny(self, xp_request, denier) -> XPApplyResult:
        """
        Deny an XP spending request and refund the XP.

        Args:
            xp_request: XPSpendingRequest instance to deny
            denier: User denying the request

        Returns:
            XPApplyResult with success/failure info
        """
        # Refund the XP cost
        self.character.xp += xp_request.cost
        self.character.save()

        # Mark as denied
        xp_request.approved = "Denied"
        xp_request.approved_by = denier
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Denied and refunded {xp_request.cost} XP for {xp_request.trait_name}",
        )

    @property
    def available_categories(self) -> list[str]:
        """Return list of XP categories this service supports."""
        return list(self._handlers.keys())

    @property
    def available_appliers(self) -> list[str]:
        """Return list of trait types this service can apply."""
        return list(self._appliers.keys())


class XPSpendingServiceFactory:
    """
    Factory to get the correct XP spending service for any character instance.

    Uses character.type to determine which service class to instantiate.
    """

    _service_map: dict[str, type[XPSpendingService]] = {}

    @classmethod
    def register(cls, character_type: str, service_class: type[XPSpendingService]):
        """
        Register a service class for a character type.

        Args:
            character_type: The character.type string (e.g., "mage", "vampire")
            service_class: The XPSpendingService subclass to use
        """
        cls._service_map[character_type] = service_class

    @classmethod
    def get_service(cls, character) -> XPSpendingService:
        """
        Get the appropriate XP spending service for a character.

        Args:
            character: Any Character instance

        Returns:
            Appropriate XPSpendingService subclass instance
        """
        char_type = character.type
        service_class = cls._service_map.get(char_type, HumanXPSpendingService)
        return service_class(character)

    @classmethod
    def get_categories_for_character(cls, character) -> list[str]:
        """Get available XP categories for a character type."""
        service = cls.get_service(character)
        return service.available_categories


class HumanXPSpendingService(XPSpendingService):
    """
    XP spending service for Human characters.

    Provides common handlers that all character types share:
    - Attribute
    - Ability
    - New Background
    - Existing Background
    - Willpower
    - MeritFlaw
    """

    @handler("Attribute")
    def _handle_attribute(self, example, **kwargs) -> XPSpendResult:
        """Handle attribute XP spending."""
        trait = example.name
        current_value = getattr(self.character, example.property_name)
        new_value = current_value + 1

        # Calculate cost: multiplier × current value (new attribute = 10)
        if current_value == 0:
            cost = 10  # New attribute
        else:
            cost = get_xp_cost("attribute") * current_value

        self.character.spend_xp(
            trait_name=example.property_name,
            trait_display=trait,
            cost=cost,
            category="attribute",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Ability")
    def _handle_ability(self, example, **kwargs) -> XPSpendResult:
        """Handle ability XP spending."""
        trait = example.name
        current_value = getattr(self.character, example.property_name)
        new_value = current_value + 1

        # Calculate cost: multiplier × current value (new ability = 3)
        if current_value == 0:
            cost = 3  # New ability
        else:
            cost = get_xp_cost("ability") * current_value

        self.character.spend_xp(
            trait_name=example.property_name,
            trait_display=trait,
            cost=cost,
            category="ability",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("New Background")
    def _handle_new_background(self, example, note="", **kwargs) -> XPSpendResult:
        """Handle new background XP spending."""
        if note:
            trait = example.name + f" ({note})"
        else:
            trait = example.name
        new_value = 1

        # New background base cost = 5, apply background multiplier
        multiplier = example.multiplier if hasattr(example, "multiplier") else 1
        cost = 5 * multiplier

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="new-background",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on new background {trait}",
        )

    @handler("Existing Background")
    def _handle_existing_background(self, example, **kwargs) -> XPSpendResult:
        """Handle existing background XP spending."""
        trait = example.bg.name + f" ({example.note})"
        current_value = example.rating
        new_value = current_value + 1

        # Calculate cost: multiplier × current value, apply background multiplier
        bg_multiplier = example.bg.multiplier if hasattr(example.bg, "multiplier") else 1
        cost = get_xp_cost("background") * current_value * bg_multiplier

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="background",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Willpower")
    def _handle_willpower(self, **kwargs) -> XPSpendResult:
        """Handle willpower XP spending."""
        trait = "Willpower"
        current_value = self.character.willpower
        new_value = current_value + 1

        # Calculate cost: multiplier × current value
        cost = get_xp_cost("willpower") * current_value

        self.character.spend_xp(
            trait_name="willpower",
            trait_display=trait,
            cost=cost,
            category="willpower",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Willpower",
        )

    @handler("MeritFlaw")
    def _handle_merit_flaw(self, example, value=None, **kwargs) -> XPSpendResult:
        """Handle merit/flaw XP spending."""
        current_rating = self.character.mf_rating(example)
        trait = example.name

        # Calculate cost: 3 × |new_rating - current_rating|
        cost = get_meritflaw_xp_cost(current_rating, value)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="meritflaw",
            trait_value=value,
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

    @applier("attribute")
    def _apply_attribute(self, xp_request, approver) -> XPApplyResult:
        """Apply approved attribute XP spending."""
        from characters.models.core.attribute_block import Attribute

        att = Attribute.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, att.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {att.name} increase to {xp_request.trait_value}",
        )

    @applier("ability")
    def _apply_ability(self, xp_request, approver) -> XPApplyResult:
        """Apply approved ability XP spending."""
        from characters.models.core.ability_block import Ability

        abb = Ability.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, abb.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {abb.name} increase to {xp_request.trait_value}",
        )

    @applier("background")
    def _apply_background(self, xp_request, approver) -> XPApplyResult:
        """Apply approved existing background XP spending."""
        # Parse background name and note from trait_name
        trait_name = xp_request.trait_name
        if " (" in trait_name:
            bg_name, note = trait_name.split(" (")
            note = note.rstrip(")")
        else:
            bg_name = trait_name
            note = ""

        bgr = self.character.backgrounds.filter(bg__name=bg_name, note=note).first()
        if bgr:
            bgr.rating += 1
            bgr.save()

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=trait_name,
            message=f"Approved {trait_name} increase",
        )

    @applier("new-background")
    def _apply_new_background(self, xp_request, approver) -> XPApplyResult:
        """Apply approved new background XP spending."""
        from characters.models.core.background_block import Background, BackgroundRating

        # Parse background name and note from trait_name
        trait_name = xp_request.trait_name
        if "(" in trait_name:
            bg_name, note = trait_name.split("(")
            note = note.rstrip(")").strip()
            bg_name = bg_name.strip()
        else:
            bg_name = trait_name.strip()
            note = ""

        bg = Background.objects.get(name=bg_name)
        BackgroundRating.objects.create(
            char=self.character,
            bg=bg,
            rating=xp_request.trait_value,
            note=note,
        )

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=trait_name,
            message=f"Approved new background {trait_name}",
        )

    @applier("willpower")
    def _apply_willpower(self, xp_request, approver) -> XPApplyResult:
        """Apply approved willpower XP spending."""
        self.character.approve_xp_spend(
            xp_request.id, "willpower", xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait="Willpower",
            message=f"Approved Willpower increase to {xp_request.trait_value}",
        )

    @applier("meritflaw")
    def _apply_merit_flaw(self, xp_request, approver) -> XPApplyResult:
        """Apply approved merit/flaw XP spending."""
        from characters.models.core.merit_flaw_block import MeritFlaw

        mf = MeritFlaw.objects.get(name=xp_request.trait_name)
        self.character.add_mf(mf, xp_request.trait_value)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved merit/flaw {xp_request.trait_name}",
        )


# Register base human type
XPSpendingServiceFactory.register("human", HumanXPSpendingService)
