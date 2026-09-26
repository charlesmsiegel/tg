"""Class-based polymorphic dispatch, independent of legacy display type strings."""

from django.http import Http404

from core.access_policy import authorize_route
from core.model_registry import get_registry
from core.views.generic import DictView


class RegistryDetailView(DictView):
    registry_app = None
    protected_object = True

    @property
    def view_mapping(self):
        return get_registry(self.registry_app).detail_views

    def handle_request(self, request, *args, **kwargs):
        obj = self.get_object(kwargs["pk"])
        target = self.view_mapping.get(type(obj))
        if target is None:
            raise Http404("Unregistered object type")
        detail = get_registry(self.registry_app).view(type(obj), "detail")
        denial = authorize_route(request, detail, args, kwargs, subject=obj)
        if denial is not None:
            return denial
        # The registry wrapper authorizes ordinary detail views; workflow routers
        # retain their own scoped state/permission checks and receive this object.
        if hasattr(target, "registry_subject"):
            return target.as_view(registry_subject=obj)(request, *args, **kwargs)
        denial = authorize_route(request, target, args, kwargs, subject=obj)
        if denial is not None:
            return denial
        return target.as_view(resolved_object=obj)(request, *args, **kwargs)
