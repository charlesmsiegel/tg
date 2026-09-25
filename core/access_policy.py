"""One fail-closed evaluator for declared URL and DictView targets."""

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse

from core.permissions import Permission, PermissionManager
from core.route_policy_manifest import VIEW_POLICIES

PROJECT_PREFIXES = (
    "accounts.",
    "characters.",
    "core.",
    "game.",
    "items.",
    "locations.",
    "widgets.",
)


def route_name(view):
    return f"{view.__module__}.{view.__name__}"


def route_policy(view):
    return VIEW_POLICIES.get(route_name(view))


def _object(model, kwargs):
    pk = kwargs.get("pk")
    if pk is None:
        raise Http404("Object not found")
    try:
        return model.objects.get(pk=pk)
    except (model.DoesNotExist, ValueError, TypeError) as exc:
        raise Http404("Object not found") from exc


def authorize_route(request, view, args=(), kwargs=None, subject=None):
    """Return a safe response or None; raise on denied actions.

    `subject` is the already resolved polymorphic object from a DictView. It
    prevents a mapped step with a child model from checking the wrong row.
    """
    kwargs = kwargs or {}
    policy = route_policy(view)
    if policy is None:
        raise PermissionDenied("View has no declared access policy")

    if policy in {"PUBLIC_READ", "PUBLIC_INDEX", "PUBLIC_CARD", "ROUTER"}:
        return None
    if policy == "WIDGET":
        if not request.user.is_authenticated:
            from django.http import JsonResponse

            return JsonResponse({"error": "Authentication required"}, status=401)
        return None
    if policy == "OBJECT_LIST":
        if not (
            request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        ) and request.method in {"GET", "HEAD"}:
            from core.views.public_object import render_public_object_list

            return render_public_object_list(request, view.model)
        return None
    if policy == "OBJECT_AJAX":
        if not request.user.is_authenticated:
            from django.http import JsonResponse

            return JsonResponse({"error": "Authentication required"}, status=401)
        object_id = request.GET.get("object")
        if object_id:
            if (
                len(object_id) > 20
                or not object_id.isascii()
                or not object_id.isdecimal()
                or int(object_id) < 1
            ):
                raise Http404("Object not found")
            from characters.models.core import CharacterModel

            subject = _object(CharacterModel, {"pk": object_id})
            if not PermissionManager.user_has_permission(
                request.user, subject, Permission.VIEW_FULL, request=request
            ):
                raise Http404("Object not found")
        return None
    if policy in {"LOGIN", "ACCOUNT", "GAME", "OBJECT_CREATE"}:
        if (
            policy == "GAME"
            and route_name(view) in {"game.views.SceneDetailView", "game.views.SceneListView"}
            and request.method in {"GET", "HEAD"}
        ):
            return None
        if not request.user.is_authenticated:
            return HttpResponse("Login required", status=401, content_type="text/plain")
        return None
    if policy == "STAFF_WRITE":
        if not request.user.is_authenticated:
            return HttpResponse("Login required", status=401, content_type="text/plain")
        if not (
            request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        ):
            raise PermissionDenied("Staff permission required")
        return None

    if policy == "CHARGEN_STEP":
        if subject is None:
            from characters.models.core import CharacterModel
            from locations.models.core import LocationModel

            model = LocationModel if view.__module__.startswith("locations.") else CharacterModel
            subject = _object(model, kwargs)
        if not PermissionManager.user_has_permission(
            request.user, subject, Permission.EDIT_FULL, request=request
        ) or getattr(subject, "status", None) not in {"Un", "Rev"}:
            raise Http404("Object not found")
        return None

    model = getattr(view, "model", None)
    if model is None:
        raise PermissionDenied("Policy requires a model")
    obj = subject if subject is not None else _object(model, kwargs)
    if policy == "OBJECT_DETAIL":
        if PermissionManager.user_has_permission(
            request.user, obj, Permission.VIEW_FULL, request=request
        ):
            return None
        if request.method not in {"GET", "HEAD"}:
            raise Http404("Object not found")
        from core.views.public_object import PublicObjectDetailView

        return PublicObjectDetailView.as_view(model_class=model)(request, *args, **kwargs)
    if policy in {"OBJECT_WRITE", "OBJECT_ACTION"}:
        from core.models import CharacterTemplate

        if (
            isinstance(obj, CharacterTemplate)
            and obj.is_official
            and not (
                PermissionManager.user_has_scoped_editor_role(request.user, obj, request=request)
            )
        ):
            raise PermissionDenied("Official templates require a scoped editor")
        if not PermissionManager.user_has_permission(
            request.user, obj, Permission.EDIT_FULL, request=request
        ):
            raise PermissionDenied("Cannot edit this object")
        if request.method in {"POST", "PUT", "PATCH"} and not (
            request.user.is_staff or request.user.is_superuser
        ):
            forbidden = {
                "owner",
                "chronicle",
                "gameline",
                "status",
                "npc",
                "xp",
                "freebies_approved",
                "approved",
                "approved_by",
            }
            submitted = forbidden.intersection(request.POST)
            if policy == "OBJECT_WRITE":
                form_class = getattr(view, "form_class", None)
                form_fields = set(getattr(form_class, "base_fields", {}))
                form_fields.update(getattr(view, "fields", ()) or ())
                submitted |= {
                    field
                    for field in {"npc", "freebies_approved"}
                    if field in form_fields
                    and field not in request.POST
                    and bool(getattr(obj, field, False))
                }
            for field in submitted:
                posted = request.POST.get(field, "")
                if field in {"owner", "chronicle", "approved_by"}:
                    current_id = getattr(obj, f"{field}_id", None)
                    current = "" if current_id is None else str(current_id)
                    unchanged = posted == current
                elif field in {"npc", "freebies_approved"}:
                    unchanged = (posted.lower() in {"1", "true", "on", "yes"}) == bool(
                        getattr(obj, field, False)
                    )
                else:
                    unchanged = posted == str(getattr(obj, field, ""))
                if not unchanged:
                    raise PermissionDenied(
                        "Approval and ownership fields require a dedicated action"
                    )
        return None
    raise PermissionDenied("Unknown access policy")
