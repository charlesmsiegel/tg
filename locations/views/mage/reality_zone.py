from django.views.generic import DetailView

from core.permissions import Permission, PermissionManager
from locations.models.mage.reality_zone import ZoneRating
from locations.registry import registry


class _RealityZoneDetailView(DetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["positive_practices"] = ZoneRating.objects.filter(zone=self.object, rating__gt=0)
        context["negative_practices"] = ZoneRating.objects.filter(zone=self.object, rating__lt=0)
        context["applied_locations"] = [
            location
            for location in self.object.get_applied_to()
            if PermissionManager.user_has_permission(
                self.request.user, location, Permission.VIEW_FULL, request=self.request
            )
        ]
        return context


RealityZoneDetailView = registry.view("locations.RealityZone", "detail")


RealityZoneListView = registry.view("locations.RealityZone", "list")
RealityZoneCreateView = registry.view("locations.RealityZone", "create")
RealityZoneUpdateView = registry.view("locations.RealityZone", "update")
