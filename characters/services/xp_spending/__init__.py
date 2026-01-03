"""
XP Spending Services Package.

This package provides a service layer for handling XP spending operations
across all World of Darkness character types.

Usage:
    from characters.services.xp_spending import XPSpendingServiceFactory

    # Get the correct service for any character
    service = XPSpendingServiceFactory.get_service(character)

    # Spend XP
    result = service.spend(
        category="Sphere",
        example=sphere_obj,
        value=None,
        note="",
    )

    if result.success:
        print(result.message)
    else:
        print(result.error)
"""

# Import base classes and factory
from .base import (
    HumanXPSpendingService,
    XPApplyResult,
    XPSpendingService,
    XPSpendingServiceFactory,
    XPSpendResult,
    applier,
    handler,
)
from .changeling import (
    ChangelingXPSpendingService,
    CtDHumanXPSpendingService,
    InanimaeXPSpendingService,
    NunnehiXPSpendingService,
)
from .demon import (
    DemonXPSpendingService,
    DtFHumanXPSpendingService,
    EarthboundXPSpendingService,
    ThrallXPSpendingService,
)
from .hunter import HtRHumanXPSpendingService, HunterXPSpendingService

# Import gameline services - these auto-register with the factory
from .mage import (
    CompanionXPSpendingService,
    MageXPSpendingService,
    MtAHumanXPSpendingService,
    SorcererXPSpendingService,
)
from .mummy import MtRHumanXPSpendingService, MummyXPSpendingService
from .vampire import (
    GhoulXPSpendingService,
    RevenantXPSpendingService,
    VampireXPSpendingService,
    VtMHumanXPSpendingService,
)
from .werewolf import (
    BastetXPSpendingService,
    CoraxXPSpendingService,
    FeraXPSpendingService,
    GarouXPSpendingService,
    GurahlXPSpendingService,
    KinfolkXPSpendingService,
    MokoleXPSpendingService,
    NuwishaXPSpendingService,
    RatkinXPSpendingService,
    WtAHumanXPSpendingService,
)
from .wraith import WraithXPSpendingService, WtOHumanXPSpendingService

__all__ = [
    # Core classes
    "XPSpendResult",
    "XPApplyResult",
    "XPSpendingService",
    "XPSpendingServiceFactory",
    "HumanXPSpendingService",
    "handler",
    "applier",
    # Mage gameline
    "MtAHumanXPSpendingService",
    "MageXPSpendingService",
    "SorcererXPSpendingService",
    "CompanionXPSpendingService",
    # Vampire gameline
    "VtMHumanXPSpendingService",
    "VampireXPSpendingService",
    "GhoulXPSpendingService",
    "RevenantXPSpendingService",
    # Werewolf gameline
    "WtAHumanXPSpendingService",
    "GarouXPSpendingService",
    "KinfolkXPSpendingService",
    "FeraXPSpendingService",
    "BastetXPSpendingService",
    "CoraxXPSpendingService",
    "GurahlXPSpendingService",
    "MokoleXPSpendingService",
    "NuwishaXPSpendingService",
    "RatkinXPSpendingService",
    # Wraith gameline
    "WtOHumanXPSpendingService",
    "WraithXPSpendingService",
    # Changeling gameline
    "CtDHumanXPSpendingService",
    "ChangelingXPSpendingService",
    "InanimaeXPSpendingService",
    "NunnehiXPSpendingService",
    # Demon gameline
    "DtFHumanXPSpendingService",
    "DemonXPSpendingService",
    "ThrallXPSpendingService",
    "EarthboundXPSpendingService",
    # Hunter gameline
    "HtRHumanXPSpendingService",
    "HunterXPSpendingService",
    # Mummy gameline
    "MtRHumanXPSpendingService",
    "MummyXPSpendingService",
]
