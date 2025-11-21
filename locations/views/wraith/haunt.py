from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
from locations.models.wraith.haunt import Haunt


class HauntDetailView(DetailView):
    model = Haunt
    template_name = "locations/wraith/haunt/detail.html"


class HauntCreateView(MessageMixin, CreateView):
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
    success_message = "Haunt '{name}' created successfully!"
    error_message = "Failed to create haunt. Please correct the errors below."


class HauntUpdateView(MessageMixin, SpecialUserMixin, UpdateView):
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
    success_message = "Haunt '{name}' updated successfully!"
    error_message = "Failed to update haunt. Please correct the errors below."


class HauntListView(ListView):
    model = Haunt
    ordering = ["name"]
    template_name = "locations/wraith/haunt/list.html"
