from core.mixins import EditPermissionMixin, ViewPermissionMixin
from django.views.generic import DetailView, UpdateView
from locations.models.changeling import Holding


class HoldingDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Holding"""

    model = Holding
    template_name = "locations/changeling/holding/detail.html"


class HoldingUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Holding"""

    model = Holding
    fields = [
        "name",
        "description",
        "chronicle",
        "holding_type",
        "glamour_per_week",
    ]
    template_name = "locations/changeling/holding/form.html"
