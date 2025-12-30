from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, ListView, UpdateView
from locations.forms.mage.demesne import DemesneForm
from locations.models.mage.demesne import Demesne


class DemesneDetailView(ViewPermissionMixin, DetailView):
    model = Demesne
    template_name = "locations/mage/demesne/detail.html"


class DemesneListView(ListView):
    model = Demesne
    ordering = ["name"]
    template_name = "locations/mage/demesne/list.html"


class DemesneCreateView(LoginRequiredMixin, MessageMixin, FormView):
    form_class = DemesneForm
    template_name = "locations/mage/demesne/form.html"
    success_message = "Demesne '{name}' created successfully!"
    error_message = "Failed to create demesne. Please correct the errors below."

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class DemesneUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Demesne
    fields = ["name", "description", "contained_within", "size", "accessibility"]
    template_name = "locations/mage/demesne/form.html"
    success_message = "Demesne '{name}' updated successfully!"
    error_message = "Failed to update demesne. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        form.fields["contained_within"].help_text = "Select one or more parent locations"
        return form
