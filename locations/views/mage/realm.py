from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.mage.realm import HorizonRealm


class RealmDetailView(ViewPermissionMixin, DetailView):
    model = HorizonRealm
    template_name = "locations/mage/realm/detail.html"


class RealmListView(ListView):
    model = HorizonRealm
    ordering = ["name"]
    template_name = "locations/mage/realm/list.html"


class RealmCreateView(LoginRequiredMixin, CreateView):
    model = HorizonRealm
    fields = ["name", "description", "contained_within"]
    template_name = "locations/mage/realm/form.html"
    success_message = "Horizon Realm '{name}' created successfully!"
    error_message = "Failed to create horizon realm. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["contained_within"].help_text = "Select one or more parent locations"
        return form


class RealmUpdateView(EditPermissionMixin, UpdateView):
    model = HorizonRealm
    fields = ["name", "description", "contained_within"]
    template_name = "locations/mage/realm/form.html"
    success_message = "Horizon Realm '{name}' updated successfully!"
    error_message = "Failed to update horizon realm. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["contained_within"].help_text = "Select one or more parent locations"
        return form
