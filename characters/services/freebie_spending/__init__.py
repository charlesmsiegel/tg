"""
Freebie Spending Services Package.

This package provides a service layer for handling freebie spending operations
across all World of Darkness character types during character creation.

Usage:
    from characters.services.freebie_spending import FreebieSpendingServiceFactory

    # Get the correct service for any character
    service = FreebieSpendingServiceFactory.get_service(character)

    # Spend freebies
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

    # Approve a freebie spending request
    apply_result = service.apply(freebie_request, approver)

    # Deny a freebie spending request (refunds freebies and reverts trait)
    deny_result = service.deny(freebie_request, denier)
"""

# Import base classes and factory
from .base import (
    FreebieApplyResult,
    FreebieSpendingService,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    applier,
    handler,
)
from .changeling import (
    ChangelingFreebieSpendingService,
    CtDHumanFreebieSpendingService,
    InanimaeFreebieSpendingService,
    NunnehiFreebieSpendingService,
)
from .demon import (
    DemonFreebieSpendingService,
    DtFHumanFreebieSpendingService,
    EarthboundFreebieSpendingService,
    ThrallFreebieSpendingService,
)
from .hunter import HtRHumanFreebieSpendingService, HunterFreebieSpendingService

# Import gameline services - these auto-register with the factory
from .mage import (
    CompanionFreebieSpendingService,
    MageFreebieSpendingService,
    MtAHumanFreebieSpendingService,
    SorcererFreebieSpendingService,
)
from .mummy import MtRHumanFreebieSpendingService, MummyFreebieSpendingService
from .vampire import (
    GhoulFreebieSpendingService,
    RevenantFreebieSpendingService,
    VampireFreebieSpendingService,
    VtMHumanFreebieSpendingService,
)
from .werewolf import (
    BastetFreebieSpendingService,
    CoraxFreebieSpendingService,
    FeraFreebieSpendingService,
    GarouFreebieSpendingService,
    GurahlFreebieSpendingService,
    KinfolkFreebieSpendingService,
    MokoleFreebieSpendingService,
    NuwishaFreebieSpendingService,
    RatkinFreebieSpendingService,
    WtAHumanFreebieSpendingService,
)
from .wraith import WraithFreebieSpendingService, WtOHumanFreebieSpendingService

__all__ = [
    # Core classes
    "FreebieSpendResult",
    "FreebieApplyResult",
    "FreebieSpendingService",
    "FreebieSpendingServiceFactory",
    "HumanFreebieSpendingService",
    "handler",
    "applier",
    # Mage gameline
    "MtAHumanFreebieSpendingService",
    "MageFreebieSpendingService",
    "SorcererFreebieSpendingService",
    "CompanionFreebieSpendingService",
    # Vampire gameline
    "VtMHumanFreebieSpendingService",
    "VampireFreebieSpendingService",
    "GhoulFreebieSpendingService",
    "RevenantFreebieSpendingService",
    # Werewolf gameline
    "WtAHumanFreebieSpendingService",
    "GarouFreebieSpendingService",
    "KinfolkFreebieSpendingService",
    "FeraFreebieSpendingService",
    "BastetFreebieSpendingService",
    "CoraxFreebieSpendingService",
    "GurahlFreebieSpendingService",
    "MokoleFreebieSpendingService",
    "NuwishaFreebieSpendingService",
    "RatkinFreebieSpendingService",
    # Wraith gameline
    "WtOHumanFreebieSpendingService",
    "WraithFreebieSpendingService",
    # Changeling gameline
    "CtDHumanFreebieSpendingService",
    "ChangelingFreebieSpendingService",
    "InanimaeFreebieSpendingService",
    "NunnehiFreebieSpendingService",
    # Demon gameline
    "DtFHumanFreebieSpendingService",
    "DemonFreebieSpendingService",
    "ThrallFreebieSpendingService",
    "EarthboundFreebieSpendingService",
    # Hunter gameline
    "HtRHumanFreebieSpendingService",
    "HunterFreebieSpendingService",
    # Mummy gameline
    "MtRHumanFreebieSpendingService",
    "MummyFreebieSpendingService",
]
