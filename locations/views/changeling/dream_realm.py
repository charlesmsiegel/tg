from core.mixins import EditPermissionMixin, ViewPermissionMixin
from django.views.generic import DetailView, UpdateView
from locations.models.changeling import DreamRealm


class DreamRealmDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Dream Realm"""

    model = DreamRealm
    template_name = "locations/changeling/dream_realm/detail.html"


class DreamRealmUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Dream Realm"""

    model = DreamRealm
    fields = [
        "name",
        "description",
        "chronicle",
        "realm_type",
        "stability",
        "accessibility",
    ]
    template_name = "locations/changeling/dream_realm/form.html"
