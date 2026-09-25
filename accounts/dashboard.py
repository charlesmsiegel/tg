"""Profile-bound dashboard queries and notification aggregation.

Notification aggregation translates existing profile selectors into display labels while
request authentication, caching, and fail-soft handling remain at the context-processor
boundary. Selector calls stay explicit and ordered so their query behavior remains visible;
future dashboard selectors extend this profile-bound object rather than the request adapter.
"""

from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Prefetch

from characters.models.core.character import Character
from characters.models.mage.mage import Mage
from characters.models.mage.rote import Rote
from game.models import Journal, Scene, Story, STRelationship, Week, WeeklyXPRequest
from game.security import filter_private_records, filter_scenes, staffed_chronicles
from items.models.core.item import ItemModel
from locations.models.core.location import LocationModel

if TYPE_CHECKING:
    from accounts.models import Profile


def _add_count(breakdown: dict[str, int], label: str, value: int) -> int:
    """Add a positive notification count and return its contribution to the total."""
    if value <= 0:
        return 0

    breakdown[label] = value
    return value


def _owned(model: type[models.Model], user) -> models.QuerySet:
    return model.objects.owned_by(user).with_polymorphic_ctype()


def _pending_approval(model: type[models.Model], user) -> models.QuerySet:
    return model.objects.pending_approval_for_user(user)


def _pending_image(model: type[models.Model], user) -> models.QuerySet:
    return model.objects.with_pending_images().for_user_chronicles(user).with_polymorphic_ctype()


class ProfileDashboard:
    """Build dashboard data for one profile."""

    def __init__(self, profile: "Profile"):
        self.profile = profile

    def st_relations(self):
        """Return storyteller relationships grouped by chronicle."""
        relationships = STRelationship.objects.for_user_optimized(self.profile.user)
        grouped = {}
        for relationship in relationships:
            grouped.setdefault(relationship.chronicle, []).append(relationship)
        return grouped

    def my_characters(self):
        return _owned(Character, self.profile.user)

    def my_locations(self):
        return _owned(LocationModel, self.profile.user)

    def my_items(self):
        return _owned(ItemModel, self.profile.user)

    def xp_requests(self):
        return Scene.objects.awaiting_xp().for_user_chronicles(self.profile.user)

    def xp_story(self):
        return Story.objects.filter(xp_given=False)

    def xp_weekly(self):
        return Week.objects.filter(xp_given=False)

    def characters_to_approve(self):
        return _pending_approval(Character, self.profile.user)

    def items_to_approve(self):
        return _pending_approval(ItemModel, self.profile.user)

    def locations_to_approve(self):
        return _pending_approval(LocationModel, self.profile.user)

    def rotes_to_approve(self):
        rotes = (
            Rote.objects.for_user_chronicles(self.profile.user)
            .filter(
                status="Sub",
            )
            .select_related("chronicle")
            .prefetch_related(Prefetch("mage_set", queryset=Mage.objects.select_related("owner")))
            .order_by("name")
        )
        return {rote: list(rote.mage_set.all()) for rote in rotes}

    def objects_to_approve(self):
        to_approve = list(self.characters_to_approve())
        to_approve.extend(self.items_to_approve())
        to_approve.extend(self.locations_to_approve())
        to_approve.extend(self.rotes_to_approve())
        return to_approve

    def freebies_to_approve(self):
        return (
            Character.objects.for_user_chronicles(self.profile.user)
            .filter(
                freebies_approved=False,
            )
            .at_freebie_step()
        )

    def character_images_to_approve(self):
        return _pending_image(Character, self.profile.user)

    def location_images_to_approve(self):
        return _pending_image(LocationModel, self.profile.user)

    def item_images_to_approve(self):
        return _pending_image(ItemModel, self.profile.user)

    def get_updated_journals(self):
        return filter_private_records(
            Journal.objects.filter(entries__st_message="").select_related("character"),
            self.profile.user,
        )

    def get_unfulfilled_weekly_xp_requests(self):
        char_list = self.my_characters()
        char_week_pairs = Week.characters.through.objects.filter(
            charactermodel_id__in=char_list
        ).values_list("charactermodel_id", "week_id")
        existing_requests = set(
            WeeklyXPRequest.objects.filter(
                character_id__in=[character for character, _week in char_week_pairs],
                week_id__in=[week for _character, week in char_week_pairs],
            ).values_list("character_id", "week_id")
        )
        missing_pairs = [pair for pair in char_week_pairs if pair not in existing_requests]
        if not missing_pairs:
            return []

        char_map = {character.pk: character for character in char_list}
        week_ids = {week for _character, week in missing_pairs}
        week_map = {week.pk: week for week in Week.objects.filter(pk__in=week_ids)}
        return [
            (char_map[character], week_map[week])
            for character, week in missing_pairs
            if not char_map[character].npc
        ]

    def get_unfulfilled_weekly_xp_requests_to_approve(self):
        char_list = Character.objects.for_user_chronicles(self.profile.user)
        char_week_pairs = Week.characters.through.objects.filter(
            charactermodel_id__in=char_list
        ).values_list("charactermodel_id", "week_id")
        result_pairs = list(
            WeeklyXPRequest.objects.filter(
                approved=False,
                character_id__in=[character for character, _week in char_week_pairs],
                week_id__in=[week for _character, week in char_week_pairs],
            ).values_list("character_id", "week_id")
        )
        if not result_pairs:
            return []

        char_map = {character.pk: character for character in char_list}
        week_ids = {week for _character, week in result_pairs}
        week_map = {week.pk: week for week in Week.objects.filter(pk__in=week_ids)}
        return [(char_map[character], week_map[week]) for character, week in result_pairs]

    def xp_spend_requests(self):
        return Character.objects.filter(
            xp_spendings__approved="Pending",
            chronicle__in=staffed_chronicles(self.profile.user),
        ).distinct()

    def unread_scenes(self):
        return filter_scenes(
            Scene.objects.filter(
                user_read_statuses__user=self.profile.user,
                user_read_statuses__read=False,
            ),
            self.profile.user,
        ).distinct()

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
        count += _add_count(breakdown, "Unread Scenes", self.unread_scenes().count())
        count += _add_count(
            breakdown,
            "Weekly XP Requests",
            len(self.get_unfulfilled_weekly_xp_requests()),
        )
        return count

    def _storyteller_notification_count(self, breakdown: dict[str, int]) -> int:
        count = 0
        count += _add_count(breakdown, "Scene XP Requests", self.xp_requests().count())
        count += _add_count(
            breakdown,
            "Characters to Approve",
            self.characters_to_approve().count(),
        )
        count += _add_count(
            breakdown,
            "Locations to Approve",
            self.locations_to_approve().count(),
        )
        count += _add_count(breakdown, "Items to Approve", self.items_to_approve().count())
        count += _add_count(breakdown, "Rotes to Approve", len(self.rotes_to_approve()))
        count += _add_count(breakdown, "Freebies to Approve", self.freebies_to_approve().count())
        count += _add_count(breakdown, "XP Spend Requests", self.xp_spend_requests().count())
        count += _add_count(
            breakdown,
            "Character Images to Approve",
            self.character_images_to_approve().count(),
        )
        count += _add_count(
            breakdown,
            "Location Images to Approve",
            self.location_images_to_approve().count(),
        )
        count += _add_count(
            breakdown,
            "Item Images to Approve",
            self.item_images_to_approve().count(),
        )

        waiting = filter_scenes(
            Scene.objects.waiting_for_st().filter(
                chronicle__in=staffed_chronicles(self.profile.user)
            ),
            self.profile.user,
        )
        count += _add_count(breakdown, "Scenes Needing Attention", waiting.count())
        count += _add_count(breakdown, "Updated Journals", self.get_updated_journals().count())
        count += _add_count(
            breakdown,
            "Weekly XP to Approve",
            len(self.get_unfulfilled_weekly_xp_requests_to_approve()),
        )
        return count
