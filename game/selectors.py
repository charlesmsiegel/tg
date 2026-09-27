"""Read-side aggregation for game pages. Selectors never write."""

from bisect import bisect_left, bisect_right
from datetime import timedelta

from django.db.models import Max, OuterRef, Subquery

from characters.models.core.character import Character
from core.services import ChronicleDataService
from game.models import Post, Scene
from game.security import filter_scenes, staffed_chronicles
from items.models.core import ItemModel
from locations.models.core import LocationModel


def chronicle_overview(chronicle, user):
    """Everything the chronicle page lists, filtered to what ``user`` may read in full.

    Chronicle staff see every row. Other members see only their own
    characters and items and no location tree, because these tables expose
    owners, statuses and relationships; the object cards elsewhere remain
    public to chronicle members.
    """
    setting_elements = chronicle.common_knowledge_elements.all()
    top_locations = LocationModel.objects.top_level().filter(chronicle=chronicle).order_by("name")

    def characters(queryset):
        return (
            queryset.with_group_ordering()
            .filter(chronicle=chronicle)
            .select_related("owner", "owner__profile")
        )

    active = characters(Character.objects.active().player_characters())
    retired = characters(Character.objects.retired().player_characters())
    deceased = characters(Character.objects.deceased().player_characters())
    npcs = characters(Character.objects.active().npcs())
    items = ItemModel.objects.for_chronicle(chronicle).order_by("name")

    if not staffed_chronicles(user).filter(pk=chronicle.pk).exists():
        # Location rows recurse through children in the template, so a
        # filtered parent alone could still expose another owner's child.
        top_locations = top_locations.none()
        active = active.filter(owner=user)
        retired = retired.filter(owner=user)
        deceased = deceased.filter(owner=user)
        npcs = npcs.filter(owner=user)
        items = items.filter(owner=user)

    scenes = filter_scenes(Scene.objects.filter(chronicle=chronicle), user).order_by(
        "-date_of_scene"
    )
    active_scenes = scenes.filter(finished=False)
    completed_scenes = scenes.filter(finished=True)
    by_gameline = ChronicleDataService.group_characters_by_gameline
    group_scenes = ChronicleDataService.group_scenes_by_gameline

    return {
        "setting_elements_by_gameline": ChronicleDataService.group_by_gameline(
            setting_elements, gameline_attr="gameline"
        ),
        "character_list": active,
        "retired_characters": retired,
        "deceased_characters": deceased,
        "npc_characters": npcs,
        "active_by_gameline": by_gameline(active),
        "retired_by_gameline": by_gameline(retired),
        "deceased_by_gameline": by_gameline(deceased),
        "npc_by_gameline": by_gameline(npcs),
        "top_locations": top_locations,
        "locations_by_gameline": ChronicleDataService.group_locations_by_gameline(top_locations),
        "items": items,
        "items_by_gameline": ChronicleDataService.group_items_by_gameline(items),
        "all_scenes_by_gameline": group_scenes(scenes),
        "active_scenes_by_gameline": group_scenes(active_scenes),
        "completed_scenes_by_gameline": group_scenes(completed_scenes),
        "active_scenes": active_scenes,
    }


def count_dates_in_week(sorted_dates, end_date):
    """How many of ``sorted_dates`` fall in the week ending ``end_date``.

    A week spans ``end_date - 7 days`` through ``end_date``, both inclusive,
    matching ``Week.start_date``.
    """
    start_date = end_date - timedelta(days=7)
    return bisect_right(sorted_dates, end_date) - bisect_left(sorted_dates, start_date)


def annotate_week_scene_counts(weeks, user):
    """Set ``week.cached_scene_count``: finished scenes ``user`` may see, by last post."""
    latest_post = (
        Post.objects.filter(scene=OuterRef("pk"))
        .values("scene")
        .annotate(latest_dt=Max("datetime_created"))
        .values("latest_dt")
    )
    dates = sorted(
        latest.date()
        for latest in filter_scenes(Scene.objects.filter(finished=True), user)
        .annotate(latest_post_date=Subquery(latest_post))
        .values_list("latest_post_date", flat=True)
        if latest
    )
    for week in weeks:
        week.cached_scene_count = count_dates_in_week(dates, week.end_date)
    return weeks
