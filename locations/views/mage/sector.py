from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from locations.forms.mage.sector import SectorForm
from locations.models.mage.sector import Sector


class SectorDetailView(ViewPermissionMixin, DetailView):
    model = Sector
    template_name = "locations/mage/sector/detail.html"


class SectorListView(ListView):
    model = Sector
    ordering = ["name"]
    template_name = "locations/mage/sector/list.html"


class SectorCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Sector
    form_class = SectorForm
    template_name = "locations/mage/sector/form.html"
    success_message = "Sector '{name}' created successfully!"
    error_message = "Failed to create sector. Please correct the errors below."


class SectorUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Sector
    form_class = SectorForm
    template_name = "locations/mage/sector/form.html"
    success_message = "Sector '{name}' updated successfully!"
    error_message = "Failed to update sector. Please correct the errors below."
