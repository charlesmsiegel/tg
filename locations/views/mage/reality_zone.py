from django.views.generic import DetailView, ListView

from core.mixins import ViewPermissionMixin, VisibilityFilterMixin
from core.permissions import PermissionManager
from locations.models.mage.reality_zone import ZoneRating
from locations.registry import registry


class _RealityZoneDetailView(ViewPermissionMixin, DetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["positive_practices"] = ZoneRating.objects.filter(zone=self.object, rating__gt=0)
        context["negative_practices"] = ZoneRating.objects.filter(zone=self.object, rating__lt=0)
        context["applied_locations"] = [
            location
            for relation in self.object.get_location_relations()
            for location in PermissionManager.filter_full_view_locations_for_user(
                self.request.user,
                getattr(self.object, relation.get_accessor_name()).all().with_polymorphic_ctype(),
            )
        ]
        return context


RealityZoneDetailView = registry.view("locations.RealityZone", "detail")


class _RealityZoneListView(VisibilityFilterMixin, ListView):
    """Reference zones with linked player places use their full-view audience."""


RealityZoneListView = registry.view("locations.RealityZone", "list")
RealityZoneCreateView = registry.view("locations.RealityZone", "create")
RealityZoneUpdateView = registry.view("locations.RealityZone", "update")
