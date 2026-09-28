"""Read-side aggregation for game pages. Selectors never write."""

from bisect import bisect_left, bisect_right
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Max, OuterRef, Q, Subquery

from characters.models.core.character import Character
from core.services import ChronicleDataService
from game.models import Post, Scene, STRelationship, UserSceneReadStatus
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


# Scene posts ----------------------------------------------------------------

SCENE_POST_WINDOW = 100


def scene_storyteller_ids(scene, user_ids):
    """Which of ``user_ids`` may manage ``scene``'s chronicle and gameline.

    The same facts ``PermissionManager.can_manage_scope`` reads without a
    request (staff, superusers, the head ST, an ``STRelationship`` for this
    chronicle and gameline), for many users in one query.
    """
    user_ids = {pk for pk in user_ids if pk is not None}
    if not user_ids:
        return set()
    scope = Q(is_staff=True) | Q(is_superuser=True)
    chronicle = scene.chronicle
    if chronicle is not None:
        if chronicle.head_st_id is not None:
            scope |= Q(pk=chronicle.head_st_id)
        line = settings.GAMELINES.get(scene.gameline, {}).get("name")
        if line:
            scope |= Q(
                pk__in=STRelationship.objects.filter(
                    chronicle=chronicle, gameline__name=line
                ).values("user_id")
            )
    users = get_user_model().objects.filter(scope, pk__in=user_ids)
    return set(users.values_list("pk", flat=True))


def with_author_roles(scene, posts):
    """Set ``author_is_st`` on each post: its author manages this scene's scope."""
    posts = list(posts)
    owners = {post.character.owner_id for post in posts if post.character is not None}
    storytellers = scene_storyteller_ids(scene, owners)
    for post in posts:
        post.author_is_st = post.character is not None and post.character.owner_id in storytellers
    return posts


def scene_cast(scene):
    """The scene's characters with their owners joined, for the cover's cast list."""
    return list(scene.characters.select_related("owner").order_by("name"))


def scene_post_window(scene, *, before=None, limit=SCENE_POST_WINDOW):
    """The latest ``limit`` posts (or the ``limit`` before post id ``before``).

    Returns ``(posts, has_earlier)``; posts are oldest first, ready for
    ``_post.html``. Ids order posts: they follow ``datetime_created`` for every
    post the app creates, and they are what live clients compare.
    """
    queryset = Post.objects.for_scene_optimized(scene)
    if before is not None:
        queryset = queryset.filter(pk__lt=before)
    newest_first = list(queryset.order_by("-pk")[: limit + 1])
    has_earlier = len(newest_first) > limit
    return with_author_roles(scene, newest_first[:limit][::-1]), has_earlier


def scene_posts_after(scene, after, *, limit=SCENE_POST_WINDOW):
    """Posts after id ``after``, oldest first; ``(posts, has_more)`` past ``limit``."""
    posts = list(
        Post.objects.for_scene_optimized(scene).filter(pk__gt=after).order_by("pk")[: limit + 1]
    )
    return with_author_roles(scene, posts[:limit]), len(posts) > limit


def scene_post(scene, post_id):
    """One post of ``scene`` ready for ``_post.html``, or ``None``."""
    posts = with_author_roles(scene, Post.objects.for_scene_optimized(scene).filter(pk=post_id))
    return posts[0] if posts else None


# Read markers ---------------------------------------------------------------


def scene_read_marker(scene, user):
    """``(tracked, read, marker)``: ``user``'s read status for ``scene``, in one query.

    ``tracked`` is false when the user has no status row (they have never had a
    character in the scene); ``marker`` is the newest post id they have read.
    """
    rows = list(
        UserSceneReadStatus.objects.filter(scene=scene, user=user).values_list(
            "read", "last_read_post_id"
        )
    )
    markers = [marker for _read, marker in rows if marker is not None]
    return bool(rows), all(read for read, _marker in rows), max(markers, default=None)


def unread_divider(scene, posts, *, read, marker, has_earlier):
    """Where the "new" divider goes in a window of ``posts``: ``{"post_id", "count"}``.

    Posts after ``marker`` are new. Without a marker every post is new, unless
    the status says the scene is read (rows from before markers were kept).
    ``None`` when nothing in the window is new. When the whole window is new and
    older posts precede it, the count comes from the database (one query).
    """
    if marker is None and read:
        return None
    fresh = [post for post in posts if marker is None or post.pk > marker]
    if not fresh:
        return None
    count = len(fresh)
    if has_earlier and fresh[0] is posts[0]:
        unread = Post.objects.filter(scene=scene)
        if marker is not None:
            unread = unread.filter(pk__gt=marker)
        count = unread.count()
    return {"post_id": fresh[0].pk, "count": count}
