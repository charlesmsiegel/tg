from typing import Any

from django.views.generic import DetailView

from core.mixins import ViewPermissionMixin
from locations.models.vampire.haven import HavenMeritFlawRating

# Haven Views
from locations.registry import registry


class _HavenDetailView(ViewPermissionMixin, DetailView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["merits_and_flaws"] = HavenMeritFlawRating.objects.filter(
            haven=self.object
        ).order_by("mf__name")
        return context


HavenDetailView = registry.view("locations.Haven", "detail")


# Domain Views


# Elysium Views


# Rack Views


# TremereChantry Views


# Barrens Views


HavenListView = registry.view("locations.Haven", "list")
HavenCreateView = registry.view("locations.Haven", "create")
HavenUpdateView = registry.view("locations.Haven", "update")
DomainDetailView = registry.view("locations.Domain", "detail")
DomainListView = registry.view("locations.Domain", "list")
DomainCreateView = registry.view("locations.Domain", "create")
DomainUpdateView = registry.view("locations.Domain", "update")
ElysiumDetailView = registry.view("locations.Elysium", "detail")
ElysiumListView = registry.view("locations.Elysium", "list")
ElysiumCreateView = registry.view("locations.Elysium", "create")
ElysiumUpdateView = registry.view("locations.Elysium", "update")
RackDetailView = registry.view("locations.Rack", "detail")
RackListView = registry.view("locations.Rack", "list")
RackCreateView = registry.view("locations.Rack", "create")
RackUpdateView = registry.view("locations.Rack", "update")
TremereChantryDetailView = registry.view("locations.TremereChantry", "detail")
TremereChantryListView = registry.view("locations.TremereChantry", "list")
TremereChantryCreateView = registry.view("locations.TremereChantry", "create")
TremereChantryUpdateView = registry.view("locations.TremereChantry", "update")
BarrensDetailView = registry.view("locations.Barrens", "detail")
BarrensListView = registry.view("locations.Barrens", "list")
BarrensCreateView = registry.view("locations.Barrens", "create")
BarrensUpdateView = registry.view("locations.Barrens", "update")
