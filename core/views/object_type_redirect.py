"""Navigate from a chosen object type to its create or list page (Step 5).

Choosing a type writes nothing, so it is a GET: no CSRF token, and the
browser's back button and bookmarks behave. The type is resolved only through
``resolve_object_type_url`` (seeded ``ObjectType`` rows and the item/location
registries), never from a route name in the request.
"""

from urllib.parse import urlencode

from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import redirect
from django.views import View

from core.create_redirects import resolve_object_type_url

# kind -> (ObjectType category, the form field that names the type)
KINDS = {
    "character": ("char", "char_type"),
    "group": ("char", "group_type"),
    "item": ("obj", "item_type"),
    "location": ("loc", "loc_type"),
}
ACTIONS = {"create", "list"}


class ObjectTypeRedirectView(View):
    http_method_names = ["get", "head"]

    def get(self, request, kind, action):
        if kind not in KINDS or action not in ACTIONS:
            raise Http404("Unknown selection")
        if action == "create" and not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        category, field = KINDS[kind]
        type_name = request.GET.get(field) or request.GET.get("type")
        gameline = request.GET.get("gameline") or None
        target = resolve_object_type_url(category, type_name, action, gameline)
        if kind == "location" and action == "create" and request.GET.get("chronicle"):
            target += "?" + urlencode({"chronicle": request.GET["chronicle"]})
        return redirect(target)
