"""Validated navigation from an existing object type to its create/list route."""

from django.conf import settings
from django.http import Http404
from django.urls import NoReverseMatch, reverse

from game.models import ObjectType

APP_NAMES = {"char": "characters", "obj": "items", "loc": "locations"}


def resolve_object_type_url(category, type_name, action="create", gameline=None):
    """Resolve a seeded type without creating or trusting a route from POST data."""
    if category not in APP_NAMES or action not in {"create", "list"} or not type_name:
        raise Http404("Unknown object type")

    queryset = ObjectType.objects.filter(type=category, name=type_name)
    if gameline is not None:
        queryset = queryset.filter(gameline=gameline)
    matches = list(queryset.values_list("gameline", flat=True)[:2])
    if len(matches) != 1:
        raise Http404("Unknown or ambiguous object type")

    code = matches[0]
    config = settings.GAMELINES.get(code)
    if config is None:
        raise Http404("Unsupported gameline")
    namespace = "" if code == "wod" else f"{config['app_name']}:"
    route_name = f"{APP_NAMES[category]}:{namespace}{action}:{type_name}"
    try:
        return reverse(route_name)
    except NoReverseMatch as exc:
        raise Http404("Unsupported object type route") from exc
