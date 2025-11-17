from characters.models.demon import Pact
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class PactDetailView(DetailView):
    model = Pact
    template_name = "characters/demon/pact/detail.html"


class PactCreateView(CreateView):
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


class PactUpdateView(UpdateView):
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


class PactListView(ListView):
    model = Pact
    ordering = ["demon", "thrall"]
    template_name = "characters/demon/pact/list.html"
