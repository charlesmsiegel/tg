from characters.models.hunter import Edge
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class EdgeDetailView(DetailView):
    model = Edge
    template_name = "characters/hunter/edge/detail.html"


class EdgeCreateView(MessageMixin, CreateView):
    model = Edge
    fields = [
        "name",
        "virtue",
        "level",
        "cost",
        "duration",
        "system",
        "description",
        "book",
    ]
    template_name = "characters/hunter/edge/form.html"
    success_message = "Edge created successfully."
    error_message = "There was an error creating the Edge."


class EdgeUpdateView(MessageMixin, UpdateView):
    model = Edge
    fields = [
        "name",
        "virtue",
        "level",
        "cost",
        "duration",
        "system",
        "description",
        "book",
    ]
    template_name = "characters/hunter/edge/form.html"
    success_message = "Edge updated successfully."
    error_message = "There was an error updating the Edge."


class EdgeListView(ListView):
    model = Edge
    ordering = ["virtue", "level", "name"]
    template_name = "characters/hunter/edge/list.html"
