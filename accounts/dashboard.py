"""Profile-bound dashboard queries and notification aggregation.

Notification aggregation translates existing profile selectors into display labels while
request authentication, caching, and fail-soft handling remain at the context-processor
boundary. Selector calls stay explicit and ordered so their query behavior remains visible;
future dashboard selectors extend this profile-bound object rather than the request adapter.
"""


def _add_count(breakdown: dict[str, int], label: str, value: int) -> int:
    """Add a positive notification count and return its contribution to the total."""
    if value <= 0:
        return 0

    breakdown[label] = value
    return value


class ProfileDashboard:
    """Build dashboard data for one profile."""

    def __init__(self, profile):
        self.profile = profile

    def notification_context(self) -> dict[str, object]:
        """Return the profile's positive notification counts and their total."""
        breakdown: dict[str, int] = {}
        count = self._player_notification_count(breakdown)
        if self.profile.is_st():
            count += self._storyteller_notification_count(breakdown)

        return {
            "notification_count": count,
            "notification_breakdown": breakdown,
        }

    def _player_notification_count(self, breakdown: dict[str, int]) -> int:
        count = 0
        count += _add_count(breakdown, "Unread Scenes", self.profile.unread_scenes().count())
        count += _add_count(
            breakdown,
            "Weekly XP Requests",
            len(self.profile.get_unfulfilled_weekly_xp_requests()),
        )
        return count

    def _storyteller_notification_count(self, breakdown: dict[str, int]) -> int:
        from game.models import Scene

        count = 0
        count += _add_count(breakdown, "Scene XP Requests", self.profile.xp_requests().count())
        count += _add_count(
            breakdown,
            "Characters to Approve",
            self.profile.characters_to_approve().count(),
        )
        count += _add_count(
            breakdown,
            "Locations to Approve",
            self.profile.locations_to_approve().count(),
        )
        count += _add_count(breakdown, "Items to Approve", self.profile.items_to_approve().count())
        count += _add_count(breakdown, "Rotes to Approve", len(self.profile.rotes_to_approve()))
        count += _add_count(
            breakdown, "Freebies to Approve", self.profile.freebies_to_approve().count()
        )
        count += _add_count(
            breakdown, "XP Spend Requests", self.profile.xp_spend_requests().count()
        )
        count += _add_count(
            breakdown,
            "Character Images to Approve",
            self.profile.character_images_to_approve().count(),
        )
        count += _add_count(
            breakdown,
            "Location Images to Approve",
            self.profile.location_images_to_approve().count(),
        )
        count += _add_count(
            breakdown,
            "Item Images to Approve",
            self.profile.item_images_to_approve().count(),
        )
        count += _add_count(
            breakdown, "Scenes Needing Attention", Scene.objects.waiting_for_st().count()
        )
        count += _add_count(
            breakdown, "Updated Journals", self.profile.get_updated_journals().count()
        )
        count += _add_count(
            breakdown,
            "Weekly XP to Approve",
            len(self.profile.get_unfulfilled_weekly_xp_requests_to_approve()),
        )
        return count
