from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.mage.sector import Sector


class SectorDetailView(DetailView):
    model = Sector
    template_name = "locations/mage/sector/detail.html"


class SectorListView(ListView):
    model = Sector
    ordering = ["name"]
    template_name = "locations/mage/sector/list.html"


class SectorCreateView(MessageMixin, CreateView):
    model = Sector
    fields = ["name", "description", "parent", "sector_class", "constraints"]
    template_name = "locations/mage/sector/form.html"
    success_message = "Sector '{name}' created successfully!"
    error_message = "Failed to create sector. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["constraints"].widget.attrs.update(
            {"placeholder": "Enter constraints here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form


class SectorUpdateView(MessageMixin, UpdateView):
    model = Sector
    fields = ["name", "description", "parent", "sector_class", "constraints"]
    template_name = "locations/mage/sector/form.html"
    success_message = "Sector '{name}' updated successfully!"
    error_message = "Failed to update sector. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        form.fields["constraints"].widget.attrs.update(
            {"placeholder": "Enter constraints here"}
        )
        form.fields["parent"].empty_label = "Parent Location"
        return form
