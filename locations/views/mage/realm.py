from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import ViewPermissionMixin, EditPermissionMixin
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
    fields = ["name", "description", "parent"]
    template_name = "locations/mage/realm/form.html"
    success_message = "Horizon Realm '{name}' created successfully!"
    error_message = "Failed to create horizon realm. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form


class RealmUpdateView(EditPermissionMixin, UpdateView):
    model = HorizonRealm
    fields = ["name", "description", "parent"]
    template_name = "locations/mage/realm/form.html"
    success_message = "Horizon Realm '{name}' updated successfully!"
    error_message = "Failed to update horizon realm. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form
