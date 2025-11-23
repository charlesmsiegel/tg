from characters.models.demon import Pact
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class PactDetailView(DetailView):
    model = Pact
    template_name = "characters/demon/pact/detail.html"


class PactCreateView(MessageMixin, CreateView):
    model = Pact
    fields = [
        "demon",
        "thrall",
        "terms",
        "faith_payment",
        "enhancements",
        "active",
    ]
    template_name = "characters/demon/pact/form.html"
    success_message = "Pact created successfully."
    error_message = "There was an error creating the Pact."


class PactUpdateView(MessageMixin, UpdateView):
    model = Pact
    fields = [
        "demon",
        "thrall",
        "terms",
        "faith_payment",
        "enhancements",
        "active",
    ]
    template_name = "characters/demon/pact/form.html"
    success_message = "Pact updated successfully."
    error_message = "There was an error updating the Pact."


class PactListView(ListView):
    model = Pact
    ordering = ["demon", "thrall"]
    template_name = "characters/demon/pact/list.html"
