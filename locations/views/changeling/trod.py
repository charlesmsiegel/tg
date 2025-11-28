from core.mixins import EditPermissionMixin, ViewPermissionMixin
from django.views.generic import DetailView, UpdateView
from locations.models.changeling import Trod


class TrodDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Trod"""

    model = Trod
    template_name = "locations/changeling/trod/detail.html"


class TrodUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Trod"""

    model = Trod
    fields = [
        "name",
        "description",
        "chronicle",
        "trod_type",
        "danger_level",
    ]
    template_name = "locations/changeling/trod/form.html"
