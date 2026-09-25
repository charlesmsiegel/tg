"""Pre-dispatch access-policy adapter for project URL callbacks."""

from django.http import HttpResponse

from core.access_policy import PROJECT_PREFIXES, authorize_route


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_class = getattr(view_func, "view_class", None)
        target = view_class or view_func
        if not target.__module__.startswith(PROJECT_PREFIXES):
            return None
        pk = view_kwargs.get("pk")
        if pk is not None and (
            not str(pk).isascii() or not str(pk).isdecimal() or int(pk) < 1
        ):
            return HttpResponse("Not found", status=404, content_type="text/plain")
        if view_class is not None and view_class.__module__ == "game.views":
            denial = self._check_game_detail(request, view_class, view_kwargs)
            if denial is not None:
                return denial
        return authorize_route(request, target, view_args, view_kwargs)

    @staticmethod
    def _check_game_detail(request, view_class, kwargs):
        from game.models import (
            Chronicle,
            FreebieSpendingRecord,
            Journal,
            JournalEntry,
            Scene,
            StoryXPRequest,
            WeeklyXPRequest,
            XPSpendingRequest,
        )
        from game.security import (
            can_read_private_record,
            can_view_scene,
            readable_chronicles,
        )

        model = getattr(view_class, "model", None)
        if view_class.__name__ == "XPSpendingRequestApproveView":
            model = XPSpendingRequest
        elif view_class.__name__ == "WeeklyXPRequestApproveView":
            model = WeeklyXPRequest
        private = {
            Journal, JournalEntry, XPSpendingRequest, FreebieSpendingRecord,
            WeeklyXPRequest, StoryXPRequest,
        }
        if model not in private | {Chronicle, Scene} or "pk" not in kwargs:
            return None

        # A fixed response keeps existing hidden IDs indistinguishable from
        # missing IDs, including for anonymous callers and POST requests.
        hidden = HttpResponse("Not found", status=404, content_type="text/plain")
        pk = kwargs.get("pk")
        try:
            obj = model.objects.filter(pk=pk).first() if pk is not None else None
        except (ValueError, TypeError):
            obj = None
        if obj is None:
            return hidden
        if model in private and not can_read_private_record(request.user, obj):
            return hidden
        if model is Scene and not can_view_scene(request.user, obj):
            return hidden
        if model is Chronicle and not readable_chronicles(request.user).filter(pk=obj.pk).exists():
            return hidden
        return None
