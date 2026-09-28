"""Spend XP (Spread M8): what a selected spend would cost, and the spend itself.

Costs are never computed here. The preview runs the character's own XP spending
service (characters.services.xp_spending) inside a savepoint that is always rolled
back, so it shows exactly what the spend will charge: new-trait prices, affinity
Spheres, background multipliers, merit and flaw rating changes.
"""

from dataclasses import dataclass

from django.db import transaction

from characters.services.xp_spending import XPSpendingServiceFactory
from game.models import XPSpendingRequest

DOTS_SHOWN = 5
DOTS_MAX = 10


@dataclass(frozen=True)
class SpendPreview:
    trait: str
    current: int
    new: int
    cost: int
    unspent_after: int
    rule: str
    # One "on" / "new" / "off" per dot, or () when a rating has no dots (a flaw).
    dots: tuple

    @property
    def dot_total(self):
        return len(self.dots)


@dataclass(frozen=True)
class SpendRefusal:
    error: str


def spend_arguments(cleaned_data):
    """The XP service's spend() arguments for a valid XPSpendFormMixin selection."""
    return {
        "category": cleaned_data["category"],
        "example": cleaned_data.get("example"),
        "value": cleaned_data.get("value"),
        "note": cleaned_data.get("note") or "",
    }


def spend(character, cleaned_data):
    """Deduct the XP and file the pending request, as the character sheet's form does."""
    with XPSpendingServiceFactory.locked(character) as service:
        return service.spend(**spend_arguments(cleaned_data))


def preview(character, cleaned_data):
    """A SpendPreview of the selection, or a SpendRefusal with the service's reason."""
    arguments = spend_arguments(cleaned_data)
    with transaction.atomic():
        result = XPSpendingServiceFactory.get_service(character).spend(**arguments)
        request = (
            XPSpendingRequest.objects.filter(character_id=character.pk).order_by("-pk").first()
            if result.success
            else None
        )
        transaction.set_rollback(True)
    if not result.success:
        return SpendRefusal(result.error or "This trait cannot be raised now.")
    new = request.trait_value
    if arguments["category"] == "MeritFlaw":
        current = character.mf_rating(arguments["example"])
    else:
        current = new - 1
    return SpendPreview(
        trait=result.trait,
        current=current,
        new=new,
        cost=result.cost,
        unspent_after=character.xp - result.cost,
        rule=rule_text(arguments["category"], current, new, result.cost),
        dots=dot_states(current, new),
    )


def rule_text(category, current, new, cost):
    """The pricing the charged cost follows, read back from the cost itself."""
    if category == "MeritFlaw":
        change = abs(new - current)
        return f"{cost // change} XP per point of change." if change else ""
    if current == 0:
        return "A new trait: a flat price."
    if cost % current == 0:
        return f"Current rating × {cost // current}."
    return ""


def dot_states(current, new):
    if current < 0 or new < 0:
        return ()
    total = min(max(DOTS_SHOWN, current, new), DOTS_MAX)
    low, high = min(current, new), max(current, new)
    return tuple(
        "on" if i < low else "new" if i < high and new > current else "off" for i in range(total)
    )
