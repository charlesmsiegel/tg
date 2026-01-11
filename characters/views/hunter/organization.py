from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.hunter import HunterOrganization
from core.mixins import MessageMixin


class HunterOrganizationDetailView(DetailView):
    model = HunterOrganization
    template_name = "characters/hunter/organization/detail.html"


class HunterOrganizationCreateView(MessageMixin, CreateView):
    model = HunterOrganization
    fields = [
        "name",
        "organization_type",
        "philosophy",
        "goals",
        "resources",
        "members",
        "leader",
    ]
    template_name = "characters/hunter/organization/form.html"
    success_message = "Hunter Organization created successfully."
    error_message = "There was an error creating the Hunter Organization."


class HunterOrganizationUpdateView(MessageMixin, UpdateView):
    model = HunterOrganization
    fields = [
        "name",
        "organization_type",
        "philosophy",
        "goals",
        "resources",
        "members",
        "leader",
    ]
    template_name = "characters/hunter/organization/form.html"
    success_message = "Hunter Organization updated successfully."
    error_message = "There was an error updating the Hunter Organization."


class HunterOrganizationListView(ListView):
    model = HunterOrganization
    ordering = ["name"]
    template_name = "characters/hunter/organization/list.html"
