from typing import Any

from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.vampire import (
    Barrens,
    Domain,
    Elysium,
    Haven,
    Rack,
    TremereChantry,
)
from locations.models.vampire.haven import HavenMeritFlawRating


# Haven Views
class HavenDetailView(ViewPermissionMixin, DetailView):
    model = Haven
    template_name = "locations/vampire/haven/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["merits_and_flaws"] = HavenMeritFlawRating.objects.filter(
            haven=self.object
        ).order_by("mf__name")
        return context


class HavenCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Haven
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "security",
        "location",
        "has_guardian",
        "has_luxury",
        "is_hidden",
        "has_library",
        "has_workshop",
    ]
    template_name = "locations/vampire/haven/form.html"
    success_message = "Haven '{name}' created successfully!"
    error_message = "Failed to create haven. Please correct the errors below."


class HavenUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Haven
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "security",
        "location",
        "has_guardian",
        "has_luxury",
        "is_hidden",
        "has_library",
        "has_workshop",
    ]
    template_name = "locations/vampire/haven/form.html"
    success_message = "Haven '{name}' updated successfully!"
    error_message = "Failed to update haven. Please correct the errors below."


class HavenListView(ListView):
    model = Haven
    ordering = ["name"]
    template_name = "locations/vampire/haven/list.html"


# Domain Views
class DomainDetailView(ViewPermissionMixin, DetailView):
    model = Domain
    template_name = "locations/vampire/domain/detail.html"


class DomainCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Domain
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "population",
        "control",
        "is_elysium",
        "has_rack",
        "is_disputed",
        "domain_type",
    ]
    template_name = "locations/vampire/domain/form.html"
    success_message = "Domain '{name}' created successfully!"
    error_message = "Failed to create domain. Please correct the errors below."


class DomainUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Domain
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "population",
        "control",
        "is_elysium",
        "has_rack",
        "is_disputed",
        "domain_type",
    ]
    template_name = "locations/vampire/domain/form.html"
    success_message = "Domain '{name}' updated successfully!"
    error_message = "Failed to update domain. Please correct the errors below."


class DomainListView(ListView):
    model = Domain
    ordering = ["name"]
    template_name = "locations/vampire/domain/list.html"


# Elysium Views
class ElysiumDetailView(ViewPermissionMixin, DetailView):
    model = Elysium
    template_name = "locations/vampire/elysium/detail.html"


class ElysiumCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Elysium
    fields = [
        "name",
        "description",
        "contained_within",
        "prestige",
        "keeper_name",
        "elysium_type",
        "is_protected",
        "allows_weapons",
        "has_blood_dolls",
        "has_art_collection",
        "has_library",
        "is_court",
    ]
    template_name = "locations/vampire/elysium/form.html"
    success_message = "Elysium '{name}' created successfully!"
    error_message = "Failed to create elysium. Please correct the errors below."


class ElysiumUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Elysium
    fields = [
        "name",
        "description",
        "contained_within",
        "prestige",
        "keeper_name",
        "elysium_type",
        "is_protected",
        "allows_weapons",
        "has_blood_dolls",
        "has_art_collection",
        "has_library",
        "is_court",
    ]
    template_name = "locations/vampire/elysium/form.html"
    success_message = "Elysium '{name}' updated successfully!"
    error_message = "Failed to update elysium. Please correct the errors below."


class ElysiumListView(ListView):
    model = Elysium
    ordering = ["name"]
    template_name = "locations/vampire/elysium/list.html"


# Rack Views
class RackDetailView(ViewPermissionMixin, DetailView):
    model = Rack
    template_name = "locations/vampire/rack/detail.html"


class RackCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Rack
    fields = [
        "name",
        "description",
        "contained_within",
        "quality",
        "population_density",
        "risk_level",
        "rack_type",
        "blood_quality",
        "is_protected",
        "is_exclusive",
        "is_contested",
        "masquerade_risk",
    ]
    template_name = "locations/vampire/rack/form.html"
    success_message = "Rack '{name}' created successfully!"
    error_message = "Failed to create rack. Please correct the errors below."


class RackUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Rack
    fields = [
        "name",
        "description",
        "contained_within",
        "quality",
        "population_density",
        "risk_level",
        "rack_type",
        "blood_quality",
        "is_protected",
        "is_exclusive",
        "is_contested",
        "masquerade_risk",
    ]
    template_name = "locations/vampire/rack/form.html"
    success_message = "Rack '{name}' updated successfully!"
    error_message = "Failed to update rack. Please correct the errors below."


class RackListView(ListView):
    model = Rack
    ordering = ["name"]
    template_name = "locations/vampire/rack/list.html"


# TremereChantry Views
class TremereChantryDetailView(DetailView):
    model = TremereChantry
    template_name = "locations/vampire/chantry/detail.html"


class TremereChantryCreateView(CreateView):
    model = TremereChantry
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "security_level",
        "library_rating",
        "ritual_rooms",
        "blood_vault_capacity",
        "regent_name",
        "resident_count",
        "apprentice_count",
        "has_wards",
        "has_sanctum",
        "has_blood_forge",
        "has_scrying_chamber",
        "has_gargoyle_guardians",
        "pyramid_level",
        "reports_to",
    ]
    template_name = "locations/vampire/chantry/form.html"


class TremereChantryUpdateView(UpdateView):
    model = TremereChantry
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "security_level",
        "library_rating",
        "ritual_rooms",
        "blood_vault_capacity",
        "regent_name",
        "resident_count",
        "apprentice_count",
        "has_wards",
        "has_sanctum",
        "has_blood_forge",
        "has_scrying_chamber",
        "has_gargoyle_guardians",
        "pyramid_level",
        "reports_to",
    ]
    template_name = "locations/vampire/chantry/form.html"


class TremereChantryListView(ListView):
    model = TremereChantry
    ordering = ["name"]
    template_name = "locations/vampire/chantry/list.html"


# Barrens Views
class BarrensDetailView(DetailView):
    model = Barrens
    template_name = "locations/vampire/barrens/detail.html"


class BarrensCreateView(CreateView):
    model = Barrens
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "danger_level",
        "population_density",
        "is_contested",
        "is_anarch_territory",
        "is_sabbat_territory",
        "is_unclaimed",
        "controlling_faction",
        "has_feeding_grounds",
        "feeding_quality",
        "has_shelter",
        "has_resources",
        "masquerade_threat",
        "lupine_activity",
        "hunter_activity",
        "mortal_gang_activity",
        "barrens_type",
        "notable_locations",
    ]
    template_name = "locations/vampire/barrens/form.html"


class BarrensUpdateView(UpdateView):
    model = Barrens
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "danger_level",
        "population_density",
        "is_contested",
        "is_anarch_territory",
        "is_sabbat_territory",
        "is_unclaimed",
        "controlling_faction",
        "has_feeding_grounds",
        "feeding_quality",
        "has_shelter",
        "has_resources",
        "masquerade_threat",
        "lupine_activity",
        "hunter_activity",
        "mortal_gang_activity",
        "barrens_type",
        "notable_locations",
    ]
    template_name = "locations/vampire/barrens/form.html"


class BarrensListView(ListView):
    model = Barrens
    ordering = ["name"]
    template_name = "locations/vampire/barrens/list.html"
