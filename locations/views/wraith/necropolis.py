from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.views.approved_user_mixin import SpecialUserMixin
from core.views.message_mixin import MessageMixin
from locations.models.wraith.necropolis import Necropolis


class NecropolisDetailView(DetailView):
    model = Necropolis
    template_name = "locations/wraith/necropolis/detail.html"


class NecropolisCreateView(MessageMixin, CreateView):
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
    success_message = "Necropolis '{name}' created successfully!"
    error_message = "Failed to create necropolis. Please correct the errors below."


class NecropolisUpdateView(MessageMixin, SpecialUserMixin, UpdateView):
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
    success_message = "Necropolis '{name}' updated successfully!"
    error_message = "Failed to update necropolis. Please correct the errors below."


class NecropolisListView(ListView):
    model = Necropolis
    ordering = ["name"]
    template_name = "locations/wraith/necropolis/list.html"
