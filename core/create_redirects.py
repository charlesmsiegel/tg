"""Validated navigation from an existing object type to its create/list route."""

from django.conf import settings
from django.http import Http404
from django.urls import NoReverseMatch, reverse

from game.models import ObjectType

APP_NAMES = {"char": "characters", "obj": "items", "loc": "locations"}

# Seeded character types whose routes drop the underscore from the type name.
CHARACTER_ROUTE_NAMES = {"dtf_human": "dtfhuman", "htr_human": "htrhuman", "mtr_human": "mtrhuman"}


def character_type_route_name(type_name, gameline, action="create"):
    """The route a seeded character type navigates to, or None for an unknown gameline."""
    config = settings.GAMELINES.get(gameline)
    if config is None:
        return None
    namespace = "" if gameline == "wod" else f"{config['app_name']}:"
    route_type = CHARACTER_ROUTE_NAMES.get(type_name, type_name)
    return f"{APP_NAMES['char']}:{namespace}{action}:{route_type}"


def character_type_has_route(type_name, gameline, action="create"):
    """Whether a seeded character type has the route its picker entry leads to."""
    route_name = character_type_route_name(type_name, gameline, action)
    if route_name is None:
        return False
    try:
        reverse(route_name)
    except NoReverseMatch:
        return False
    return True


def creatable_character_types(object_types):
    """The seeded character types among ``object_types`` that have a create route."""
    return [obj for obj in object_types if character_type_has_route(obj.name, obj.gameline)]


def resolve_object_type_url(category, type_name, action="create", gameline=None):
    """Resolve a seeded type without creating or trusting a route from POST data."""
    if category not in APP_NAMES or action not in {"create", "list"} or not type_name:
        raise Http404("Unknown object type")

    if category in {"obj", "loc"}:
        from core.model_registry import get_registry

        registry = get_registry(APP_NAMES[category])
        entry = registry.resolve(type_name, gameline)
        return registry.selection_url(entry, action)

    queryset = ObjectType.objects.filter(type=category, name=type_name)
    if gameline is not None:
        queryset = queryset.filter(gameline=gameline)
    matches = list(queryset.values_list("gameline", flat=True)[:2])
    if len(matches) != 1:
        raise Http404("Unknown or ambiguous object type")

    route_name = character_type_route_name(type_name, matches[0], action)
    if route_name is None:
        raise Http404("Unsupported gameline")
    try:
        return reverse(route_name)
    except NoReverseMatch as exc:
        raise Http404("Unsupported object type route") from exc
