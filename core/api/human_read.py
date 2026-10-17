"""Read-only exact Human profile plus native-public reference catalogs."""

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch
from django.urls import resolve, reverse
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from characters.models.core import (
    Archetype,
    Background,
    CharacterModel,
    Derangement,
    Human,
    MeritFlaw,
    Specialty,
)
from core.api.human_profile import (
    CATALOG_FIELDS,
    RELATION_LIMIT,
    ProfileError,
    catalog_projection,
    fingerprint,
    human_projection,
    manifest,
)
from core.api.scene_journal import GameReadView, hidden_get
from core.models import Book, Language, Number
from core.permissions import Permission, PermissionManager
from core.route_policy_manifest import VIEW_POLICIES
from game.models import ObjectType

CATALOG_ROUTES = {
    "archetypes": "characters:list:archetype",
    "merits-flaws": "characters:list:meritflaw",
    "specialties": "characters:list:specialty",
    "languages": "core:index_language",
    "derangements": "characters:list:derangement",
    "books": "core:index_book",
}

CATALOG_MODELS = {
    "archetypes": Archetype,
    "merits-flaws": MeritFlaw,
    "specialties": Specialty,
    "languages": Language,
    "derangements": Derangement,
    "books": Book,
}


def catalog_view(kind):
    # Resolve only these fixed native list routes. This reuses the actual routed
    # class without importing native view packages into the API dependency graph.
    route = CATALOG_ROUTES.get(kind)
    if route is None:
        raise NotFound("Not found.")
    native_class = getattr(resolve(reverse(route)).func, "view_class", None)
    if native_class is None or native_class.model is not CATALOG_MODELS[kind]:
        raise NotFound("Not found.")
    native_name = f"{native_class.__module__}.{native_class.__name__}"
    if (
        VIEW_POLICIES.get(native_name) != "PUBLIC_READ"
        or native_class.__dict__.get("access_policy", "PUBLIC_READ") != "PUBLIC_READ"
    ):
        raise NotFound("Not found.")
    return native_class


def authorized_character(request):
    queryset = PermissionManager.filter_full_view_characters_for_user(
        request.user,
        CharacterModel.objects.select_related("owner", "chronicle").with_polymorphic_ctype(),
    )
    character = hidden_get(queryset, pk=request.parser_context["kwargs"]["pk"])
    if not PermissionManager.user_has_permission(
        request.user, character, Permission.VIEW_FULL, request=request
    ):
        raise NotFound("Not found.")
    return character


def exact_projection(character):
    if type(character) is not Human:
        raise ProfileError("unsupported_type")
    return human_projection(character)


class HumanProfileManifestView(GameReadView):
    def get(self, request):
        return Response(manifest())


class HumanProfileView(GameReadView):
    def get(self, request, pk):
        with transaction.atomic():
            character = authorized_character(request)
            try:
                first = exact_projection(character)
            except ProfileError:
                # Type/size diagnostics also disclose object facts. Defer them
                # until the same fresh canonical authorization as normal data.
                first = None
            # An initial full-view grant never leases access across role/owner
            # changes. Reload actor flags and every public scalar/relation too.
            request.user = hidden_get(
                get_user_model().objects.filter(is_active=True), pk=request.user.pk
            )
            PermissionManager.invalidate_request_cache(request)
            second = exact_projection(authorized_character(request))
            if first != second:
                raise ProfileError("snapshot_changed", status=409)
            second["snapshot_token"] = fingerprint(request, second)
        return Response(second)


class HumanCatalogView(GameReadView):
    query_keys = frozenset({"page", "page_size"})

    def get(self, request, kind):
        if kind == "backgrounds":
            # Background extends plain Statistic, which has no ownership or
            # visibility metadata. Only its public definition facts are emitted.
            queryset = Background.objects.all()
        else:
            native_class = catalog_view(kind)
            native = native_class()
            native.setup(request._request)
            queryset = native.get_queryset()
            if queryset.model is not CATALOG_MODELS[kind]:
                raise NotFound("Not found.")
        queryset = queryset.only(*CATALOG_FIELDS[kind]).order_by("pk")
        if kind == "merits-flaws":
            queryset = queryset.prefetch_related(None).prefetch_related(
                Prefetch(
                    "ratings",
                    queryset=Number.objects.only("id", "value").order_by("pk")[
                        : RELATION_LIMIT + 1
                    ],
                    to_attr="_profile_ratings",
                ),
                Prefetch(
                    "allowed_types",
                    queryset=ObjectType.objects.only("id", "name", "type", "gameline").order_by(
                        "pk"
                    )[: RELATION_LIMIT + 1],
                    to_attr="_profile_allowed_types",
                ),
            )
        return self.page(queryset, lambda row: catalog_projection(kind, row))
