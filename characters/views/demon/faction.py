from characters.models.demon import DemonFaction
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class DemonFactionDetailView(DetailView):
    model = DemonFaction
    template_name = "characters/demon/faction/detail.html"


class DemonFactionCreateView(CreateView):
    model = DemonFaction
    fields = [
        "name",
        "description",
        "philosophy",
        "goal",
        "leadership",
        "tactics",
    ]
    template_name = "characters/demon/faction/form.html"


class DemonFactionUpdateView(UpdateView):
    model = DemonFaction
    fields = [
        "name",
        "description",
        "philosophy",
        "goal",
        "leadership",
        "tactics",
    ]
    template_name = "characters/demon/faction/form.html"


class DemonFactionListView(ListView):
    model = DemonFaction
    ordering = ["name"]
    template_name = "characters/demon/faction/list.html"
