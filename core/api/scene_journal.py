"""Read-only native scenes and journals; no commands, read markers or ST messages."""

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from characters.models.core import CharacterModel
from core.api.views import JSONReadView
from core.permissions import Permission, PermissionManager
from game.models import Journal, Scene
from game.security import can_view_scene, filter_private_records, filter_scenes

MAX_NATIVE_ID = 2**63 - 1
SCENE_FIELDS = (
    "id",
    "name",
    "chronicle_id",
    "gameline",
    "visibility",
    "date_played",
    "date_of_scene",
    "finished",
)
POST_FIELDS = ("id", "scene_id", "display_name", "message", "datetime_created")
ENTRY_FIELDS = ("id", "journal_id", "message", "date", "datetime_created")


def scene_projection(scene):
    return {key: getattr(scene, key) for key in SCENE_FIELDS} | {
        "projection": "tg-scene-v1",
        "complete": False,
    }


def post_projection(post):
    return {key: getattr(post, key) for key in POST_FIELDS}


def journal_projection(journal):
    return {
        "id": journal.pk,
        "character_id": journal.character_id,
        "projection": "tg-journal-v1",
        "complete": False,
    }


def entry_projection(entry):
    return {key: getattr(entry, key) for key in ENTRY_FIELDS}


def hidden_get(queryset, **lookup):
    """Never disclose a hidden object's model or a different missing-object error."""
    try:
        return get_object_or_404(queryset, **lookup)
    except Http404 as exc:
        raise NotFound("Not found.") from exc


class GameReadView(JSONReadView):
    query_keys = frozenset()

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if "pk" in kwargs and not 1 <= kwargs["pk"] <= MAX_NATIVE_ID:
            raise NotFound("Not found.")
        for key in request.query_params:
            if key not in self.query_keys:
                raise ValidationError({key: "Unsupported query parameter."})
            values = request.query_params.getlist(key)
            if len(values) != 1:
                raise ValidationError({key: "Supply exactly one value."})
            value = values[0]
            if (
                not value.isascii()
                or not value.isdecimal()
                or len(value) > 19
                or not 1 <= int(value) <= MAX_NATIVE_ID
            ):
                raise ValidationError({key: "Expected a positive native integer."})

    def visible_scenes(self):
        queryset = filter_scenes(Scene.objects.only(*SCENE_FIELDS), self.request.user)
        if "chronicle_id" in self.request.query_params:
            queryset = queryset.filter(chronicle_id=int(self.request.query_params["chronicle_id"]))
        return queryset

    def scene(self):
        scene = hidden_get(self.visible_scenes(), pk=self.kwargs["pk"])
        # Visibility or cast membership can change after the initial lookup.
        if not can_view_scene(self.request.user, scene):
            raise NotFound("Not found.")
        return scene

    def visible_journals(self):
        full_characters = PermissionManager.filter_full_view_characters_for_user(
            self.request.user, CharacterModel.objects.all()
        )
        queryset = filter_private_records(
            Journal.objects.filter(character_id__in=full_characters.values("pk")),
            self.request.user,
        ).only("id", "character_id")
        if "chronicle_id" in self.request.query_params:
            queryset = queryset.filter(
                character__chronicle_id=int(self.request.query_params["chronicle_id"])
            )
        return queryset

    def journal(self, **lookup):
        journal = hidden_get(self.visible_journals(), **lookup)
        # Recheck the journal-to-character link and current owner/ST scope, not
        # the character/roles captured before the record was fetched.
        if (
            not self.visible_journals()
            .filter(pk=journal.pk, character_id=journal.character_id)
            .exists()
        ):
            raise NotFound("Not found.")
        characters = PermissionManager.filter_full_view_characters_for_user(
            self.request.user,
            CharacterModel.objects.select_related("owner", "chronicle").with_polymorphic_ctype(),
        )
        character = hidden_get(characters, pk=journal.character_id)
        PermissionManager.invalidate_request_cache(self.request)
        if not PermissionManager.user_has_permission(
            self.request.user, character, Permission.VIEW_FULL, request=self.request
        ):
            raise NotFound("Not found.")
        return journal


class SceneListView(GameReadView):
    query_keys = frozenset({"page", "page_size", "chronicle_id"})

    def get(self, request):
        return self.page(
            self.visible_scenes().order_by("-date_of_scene", "-date_played", "-pk"),
            scene_projection,
        )


class SceneDetailView(GameReadView):
    def get(self, request, pk):
        return Response(scene_projection(self.scene()))


class ScenePostsView(GameReadView):
    query_keys = frozenset({"page", "page_size"})

    def get(self, request, pk):
        scene = self.scene()
        return self.page(scene.post_set.only(*POST_FIELDS).order_by("pk"), post_projection)


class JournalListView(GameReadView):
    query_keys = frozenset({"page", "page_size", "chronicle_id"})

    def get(self, request):
        return self.page(self.visible_journals().order_by("pk"), journal_projection)


class JournalDetailView(GameReadView):
    def get(self, request, pk):
        return Response(journal_projection(self.journal(pk=pk)))


class JournalEntriesView(GameReadView):
    query_keys = frozenset({"page", "page_size"})

    def get(self, request, pk):
        journal = self.journal(pk=pk)
        return self.page(
            journal.entries.only(*ENTRY_FIELDS).order_by("-date", "datetime_created", "pk"),
            entry_projection,
        )


class CharacterJournalView(GameReadView):
    def get(self, request, pk):
        return Response(journal_projection(self.journal(character_id=pk)))
