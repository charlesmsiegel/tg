from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.hunter import Safehouse


class SafehouseDetailView(ViewPermissionMixin, DetailView):
    model = Safehouse
    template_name = "locations/hunter/safehouse/detail.html"


class SafehouseListView(ListView):
    model = Safehouse
    ordering = ["name"]
    template_name = "locations/hunter/safehouse/list.html"


class SafehouseCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Safehouse
    fields = [
        "name",
        "parent",
        "description",
        "size",
        "capacity",
        "security_level",
        "armory_level",
        "surveillance_level",
        "medical_facilities",
        "is_compromised",
        "is_mobile",
        "has_panic_room",
        "has_escape_routes",
        "has_dead_drop",
        "has_communications",
        "cover_story",
        "legal_owner",
    ]
    template_name = "locations/hunter/safehouse/form.html"
    success_message = "Safehouse '{name}' created successfully!"
    error_message = "Failed to create safehouse. Please correct the errors below."


class SafehouseUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Safehouse
    fields = [
        "name",
        "parent",
        "description",
        "size",
        "capacity",
        "security_level",
        "armory_level",
        "surveillance_level",
        "medical_facilities",
        "is_compromised",
        "is_mobile",
        "has_panic_room",
        "has_escape_routes",
        "has_dead_drop",
        "has_communications",
        "cover_story",
        "legal_owner",
    ]
    template_name = "locations/hunter/safehouse/form.html"
    success_message = "Safehouse '{name}' updated successfully!"
    error_message = "Failed to update safehouse. Please correct the errors below."
