from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import EditPermissionMixin, ViewPermissionMixin
from locations.forms.changeling.trod import TrodForm
from locations.models.changeling import Trod


class TrodDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Trod"""

    model = Trod
    template_name = "locations/changeling/trod/detail.html"


class TrodListView(ListView):
    """List view for all Trods"""

    model = Trod
    ordering = ["name"]
    template_name = "locations/changeling/trod/list.html"


class TrodCreateView(LoginRequiredMixin, CreateView):
    """Create view for a new Trod"""

    model = Trod
    form_class = TrodForm
    template_name = "locations/changeling/trod/form.html"


class TrodUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Trod"""

    model = Trod
    form_class = TrodForm
    template_name = "locations/changeling/trod/form.html"
