from characters.models.demon import Visage
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class VisageDetailView(DetailView):
    model = Visage
    template_name = "characters/demon/visage/detail.html"


class VisageCreateView(MessageMixin, CreateView):
    model = Visage
    fields = [
        "name",
        "description",
        "house",
        "low_torment_traits",
        "high_torment_traits",
    ]
    template_name = "characters/demon/visage/form.html"
    success_message = "Visage created successfully."
    error_message = "There was an error creating the Visage."


class VisageUpdateView(MessageMixin, UpdateView):
    model = Visage
    fields = [
        "name",
        "description",
        "house",
        "low_torment_traits",
        "high_torment_traits",
    ]
    template_name = "characters/demon/visage/form.html"
    success_message = "Visage updated successfully."
    error_message = "There was an error updating the Visage."


class VisageListView(ListView):
    model = Visage
    ordering = ["name"]
    template_name = "characters/demon/visage/list.html"
