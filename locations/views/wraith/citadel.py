from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.wraith import Citadel


class CitadelDetailView(ViewPermissionMixin, DetailView):
    model = Citadel
    template_name = "locations/wraith/citadel/detail.html"


class CitadelCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Citadel
    fields = [
        "name",
        "description",
        "parent",
        "purpose",
        "defense_rating",
        "garrison_size",
        "commander",
        "controlling_faction",
        "has_soulforges",
        "has_prison",
        "has_gateway",
    ]
    template_name = "locations/wraith/citadel/form.html"
    success_message = "Citadel '{name}' created successfully!"
    error_message = "Failed to create citadel. Please correct the errors below."


class CitadelUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Citadel
    fields = [
        "name",
        "description",
        "parent",
        "purpose",
        "defense_rating",
        "garrison_size",
        "commander",
        "controlling_faction",
        "has_soulforges",
        "has_prison",
        "has_gateway",
    ]
    template_name = "locations/wraith/citadel/form.html"
    success_message = "Citadel '{name}' updated successfully!"
    error_message = "Failed to update citadel. Please correct the errors below."


class CitadelListView(ListView):
    model = Citadel
    ordering = ["name"]
    template_name = "locations/wraith/citadel/list.html"
