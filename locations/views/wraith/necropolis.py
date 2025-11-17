from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.views.approved_user_mixin import SpecialUserMixin
from locations.models.wraith.necropolis import Necropolis


class NecropolisDetailView(DetailView):
    model = Necropolis
    template_name = "locations/wraith/necropolis/detail.html"


class NecropolisCreateView(CreateView):
    model = Necropolis
    fields = [
        "name",
        "description",
        "parent",
        "region",
        "population",
        "deathlord",
    ]
    template_name = "locations/wraith/necropolis/form.html"


class NecropolisUpdateView(SpecialUserMixin, UpdateView):
    model = Necropolis
    fields = [
        "name",
        "description",
        "parent",
        "region",
        "population",
        "deathlord",
    ]
    template_name = "locations/wraith/necropolis/form.html"


class NecropolisListView(ListView):
    model = Necropolis
    ordering = ["name"]
    template_name = "locations/wraith/necropolis/list.html"
