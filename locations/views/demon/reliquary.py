from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.demon.reliquary import Reliquary


class ReliquaryDetailView(ViewPermissionMixin, DetailView):
    model = Reliquary
    template_name = "locations/demon/reliquary/detail.html"


class ReliquaryListView(ListView):
    model = Reliquary
    ordering = ["name"]
    template_name = "locations/demon/reliquary/list.html"


class ReliquaryCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Reliquary
    fields = [
        "name",
        "parent",
        "description",
        "reliquary_type",
        "location_size",
        "max_health_levels",
        "current_health_levels",
        "soak_rating",
        "has_pervasiveness",
        "has_manifestation",
        "manifestation_range",
    ]
    template_name = "locations/demon/reliquary/form.html"
    success_message = "Reliquary '{name}' created successfully!"
    error_message = "Failed to create reliquary. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["parent"].empty_label = "Parent Location"
        return form


class ReliquaryUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Reliquary
    fields = [
        "name",
        "description",
        "parent",
        "reliquary_type",
        "location_size",
        "max_health_levels",
        "current_health_levels",
        "soak_rating",
        "has_pervasiveness",
        "has_manifestation",
        "manifestation_range",
    ]
    template_name = "locations/demon/reliquary/form.html"
    success_message = "Reliquary '{name}' updated successfully!"
    error_message = "Failed to update reliquary. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["parent"].empty_label = "Parent Location"
        return form
