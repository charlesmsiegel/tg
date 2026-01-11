from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.demon import Visage
from core.mixins import MessageMixin


class VisageDetailView(DetailView):
    model = Visage
    template_name = "characters/demon/visage/detail.html"


class VisageCreateView(MessageMixin, CreateView):
    model = Visage
    fields = [
        "name",
        "description",
        "house",
        "default_apocalyptic_form",
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
        "default_apocalyptic_form",
    ]
    template_name = "characters/demon/visage/form.html"
    success_message = "Visage updated successfully."
    error_message = "There was an error updating the Visage."


class VisageListView(ListView):
    model = Visage
    ordering = ["name"]
    template_name = "characters/demon/visage/list.html"
