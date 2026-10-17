"""Session-authenticated JSON reads and dedicated, CSRF-protected POST writes."""

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from characters.models.core import Character
from core.actions import ObjectActionView
from core.api.projections import character_detail, character_summary, chronicle_detail
from core.api.services import create_chronicle, update_description
from core.api.session import session_state
from core.permissions import Permission, PermissionManager
from game.security import readable_chronicles


class NativePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


class JSONReadView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    http_method_names = ["get", "head", "options"]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response["Cache-Control"] = "private, no-store"
        return response

    def page(self, queryset, project):
        paginator = NativePagination()
        rows = paginator.paginate_queryset(queryset, self.request, view=self)
        return paginator.get_paginated_response([project(row) for row in rows])

    def chronicle(self):
        return get_object_or_404(readable_chronicles(self.request.user), pk=self.kwargs["pk"])


class SessionView(JSONReadView):
    def get(self, request):
        return Response(session_state(request))


class ChronicleListView(JSONReadView):
    def get(self, request):
        return self.page(
            readable_chronicles(request.user).order_by("pk"),
            lambda row: {"id": row.pk, "name": row.name},
        )


class ChronicleDetailView(JSONReadView):
    def get(self, request, pk):
        return Response(chronicle_detail(self.chronicle()))


class AllowedObjectsView(JSONReadView):
    def get(self, request, pk):
        return self.page(
            self.chronicle().allowed_objects.order_by("pk"),
            lambda row: {
                "id": row.pk,
                "name": row.name,
                "type": row.type,
                "gameline": row.gameline,
            },
        )


class ChronicleCharactersView(JSONReadView):
    def get(self, request, pk):
        chronicle = self.chronicle()
        queryset = PermissionManager.filter_full_view_characters_for_user(
            request.user, Character.objects.filter(chronicle=chronicle)
        )
        return self.page(
            queryset.select_related("owner", "chronicle").with_polymorphic_ctype().order_by("pk"),
            character_summary,
        )


class CharacterDetailView(JSONReadView):
    def get(self, request, pk):
        queryset = PermissionManager.filter_full_view_characters_for_user(
            request.user, Character.objects.all()
        )
        character = get_object_or_404(
            queryset.select_related("owner", "chronicle").with_polymorphic_ctype(), pk=pk
        )
        if not PermissionManager.user_has_permission(
            request.user, character, Permission.VIEW_FULL, request=request
        ):
            raise Http404("Not found.")
        return Response(character_detail(character))


class CharacterUpdateView(ObjectActionView):
    model = Character
    permission = Permission.EDIT_LIMITED
    lock = True

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return JsonResponse(
                {"error": "Not found."}, status=404, headers={"Cache-Control": "private, no-store"}
            )
        except PermissionDenied:
            return JsonResponse(
                {"error": "Forbidden."}, status=403, headers={"Cache-Control": "private, no-store"}
            )

    def get_queryset(self):
        return super().get_queryset().select_related("owner", "chronicle").with_polymorphic_ctype()

    def perform(self, form):
        # ObjectActionView has now locked and reloaded the polymorphic row.
        # Owner/status/membership may have changed since its pre-lock check.
        PermissionManager.invalidate_request_cache(self.request)
        self.authorize()
        if self.request.content_type != "application/json":
            raise ValidationError("Content-Type must be application/json.")
        return update_description(self.object, self.request.body)

    def action_succeeded(self, result):
        return JsonResponse({"id": result.pk}, headers={"Cache-Control": "private, no-store"})

    def action_failed(self, error, form=None):
        return JsonResponse(
            {"error": error}, status=400, headers={"Cache-Control": "private, no-store"}
        )


class ChronicleCreateView(View):
    http_method_names = ["post"]

    def post(self, request):
        if request.content_type != "application/json":
            return JsonResponse({"error": "Content-Type must be application/json."}, status=400)
        try:
            chronicle = create_chronicle(request.user, request.body, request)
        except ValidationError as exc:
            return JsonResponse({"errors": exc.messages}, status=400)
        return JsonResponse(
            {"id": chronicle.pk}, status=201, headers={"Cache-Control": "private, no-store"}
        )
