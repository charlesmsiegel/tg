from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.views.approved_user_mixin import SpecialUserMixin
from locations.models.wraith.haunt import Haunt


class HauntDetailView(DetailView):
    model = Haunt
    template_name = "locations/wraith/haunt/detail.html"


class HauntCreateView(CreateView):
    model = Haunt
    fields = [
        "name",
        "description",
        "parent",
        "rank",
        "shroud_rating",
        "haunt_type",
        "haunt_size",
        "faith_resonance",
        "attracts_ghosts",
    ]
    template_name = "locations/wraith/haunt/form.html"


class HauntUpdateView(SpecialUserMixin, UpdateView):
    model = Haunt
    fields = [
        "name",
        "description",
        "parent",
        "rank",
        "shroud_rating",
        "haunt_type",
        "haunt_size",
        "faith_resonance",
        "attracts_ghosts",
    ]
    template_name = "locations/wraith/haunt/form.html"


class HauntListView(ListView):
    model = Haunt
    ordering = ["name"]
    template_name = "locations/wraith/haunt/list.html"
