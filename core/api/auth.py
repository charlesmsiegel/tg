"""JSON responses over native Django form/session authentication protections."""

from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, JsonResponse
from django.views import View

from accounts.views import CustomLoginView
from core.api.session import session_state


class PrivateAuthResponseMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response["Cache-Control"] = "private, no-store"
        return response


class CSRFView(PrivateAuthResponseMixin, View):
    http_method_names = ["get", "head", "options"]

    def get(self, request):
        return JsonResponse(session_state(request))


class LoginView(PrivateAuthResponseMixin, CustomLoginView):
    # Keep inherited csrf_protect, sensitive_post_parameters, never_cache,
    # AuthenticationForm binding, login/session rotation and shared throttle.
    http_method_names = ["post", "options"]

    def post(self, request, *args, **kwargs):
        if request.content_type != "application/x-www-form-urlencoded":
            return JsonResponse({"error": "unsupported_media_type"}, status=415)
        allowed = {"username", "password", "csrfmiddlewaretoken"}
        if any(key not in allowed or len(values) != 1 for key, values in request.POST.lists()):
            return JsonResponse({"error": "invalid_credentials"}, status=400)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        # Native login needs a redirect response internally; the facade returns JSON.
        return "/"

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse(session_state(self.request))

    def form_invalid(self, form):
        return JsonResponse({"error": "invalid_credentials"}, status=400)

    def throttled_response(self):
        return JsonResponse({"error": "too_many_attempts"}, status=429)


class SessionLogoutView(PrivateAuthResponseMixin, LogoutView):
    http_method_names = ["post", "options"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return HttpResponse(status=204)

    def get_success_url(self):
        return "/"
