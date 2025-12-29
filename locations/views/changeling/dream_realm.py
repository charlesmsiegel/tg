from core.mixins import EditPermissionMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.forms.changeling.dream_realm import DreamRealmForm
from locations.models.changeling import DreamRealm


class DreamRealmDetailView(ViewPermissionMixin, DetailView):
    """Detail view for a Dream Realm"""

    model = DreamRealm
    template_name = "locations/changeling/dream_realm/detail.html"


class DreamRealmListView(ListView):
    """List view for all Dream Realms"""

    model = DreamRealm
    ordering = ["name"]
    template_name = "locations/changeling/dream_realm/list.html"


class DreamRealmCreateView(LoginRequiredMixin, CreateView):
    """Create view for a new Dream Realm"""

    model = DreamRealm
    form_class = DreamRealmForm
    template_name = "locations/changeling/dream_realm/form.html"


class DreamRealmUpdateView(EditPermissionMixin, UpdateView):
    """Update view for an existing Dream Realm"""

    model = DreamRealm
    form_class = DreamRealmForm
    template_name = "locations/changeling/dream_realm/form.html"
