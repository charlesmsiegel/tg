"""Read audiences shared by private game detail and collection views."""

from django.db.models import Q

from characters.models.core import CharacterModel
from core.permissions import Permission, PermissionManager
from game.models import Chronicle, Scene, STRelationship


def readable_chronicles(user):
    if not user.is_authenticated:
        return Chronicle.objects.none()
    if user.is_staff or user.is_superuser:
        return Chronicle.objects.all()
    played = CharacterModel.objects.filter(owner=user).values("chronicle_id")
    staffed = STRelationship.objects.filter(user=user).values("chronicle_id")
    return Chronicle.objects.filter(
        Q(head_st=user)
        | Q(game_storytellers=user)
        | Q(pk__in=played)
        | Q(pk__in=staffed)
    ).distinct()


def staffed_chronicles(user):
    """Chronicles where a user has a full ST read role."""
    if not user.is_authenticated:
        return Chronicle.objects.none()
    if user.is_staff or user.is_superuser:
        return Chronicle.objects.all()
    return Chronicle.objects.filter(
        Q(head_st=user) | Q(game_storytellers=user) | Q(st_relationships__user=user)
    ).distinct()


def can_read_private_record(user, record):
    character = getattr(record, "character", None)
    if character is None and hasattr(record, "journal"):
        character = getattr(record.journal, "character", None)
    return bool(
        character
        and PermissionManager.user_has_permission(user, character, Permission.VIEW_FULL)
    )


def filter_private_records(queryset, user):
    if not user.is_authenticated:
        return queryset.none()
    if user.is_staff or user.is_superuser:
        return queryset
    return queryset.filter(
        Q(character__owner=user)
        | Q(character__chronicle_id__in=staffed_chronicles(user).values("pk"))
    ).distinct()


def filter_scenes(queryset, user):
    if user.is_authenticated and (user.is_staff or user.is_superuser):
        return queryset
    visible = Q(visibility=Scene.Visibility.PUBLIC)
    if user.is_authenticated:
        visible |= Q(
            visibility=Scene.Visibility.CHRONICLE,
            chronicle_id__in=readable_chronicles(user).values("pk"),
        )
        visible |= Q(visibility=Scene.Visibility.PARTICIPANTS) & (
            Q(chronicle_id__in=staffed_chronicles(user).values("pk"))
            | Q(characters__owner=user)
        )
    return queryset.filter(visible).distinct()


def can_view_scene(user, scene):
    return filter_scenes(type(scene).objects.filter(pk=scene.pk), user).exists()
