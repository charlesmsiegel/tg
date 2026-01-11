from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import EditPermissionMixin, ViewPermissionMixin
from locations.forms.changeling.holding import HoldingForm
from locations.models.changeling import Holding


class HoldingDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Holding"""

    model = Holding
    template_name = "locations/changeling/holding/detail.html"


class HoldingListView(ListView):
    """List view for all Holdings"""

    model = Holding
    ordering = ["name"]
    template_name = "locations/changeling/holding/list.html"


class HoldingCreateView(LoginRequiredMixin, CreateView):
    """Create view for a new Holding"""

    model = Holding
    form_class = HoldingForm
    template_name = "locations/changeling/holding/form.html"


class HoldingUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Holding"""

    model = Holding
    form_class = HoldingForm
    template_name = "locations/changeling/holding/form.html"
