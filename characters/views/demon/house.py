from characters.models.demon import DemonHouse
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class DemonHouseDetailView(DetailView):
    model = DemonHouse
    template_name = "characters/demon/house/detail.html"


class DemonHouseCreateView(CreateView):
    model = DemonHouse
    fields = [
        "name",
        "description",
        "celestial_name",
        "starting_torment",
        "domain",
    ]
    template_name = "characters/demon/house/form.html"


class DemonHouseUpdateView(UpdateView):
    model = DemonHouse
    fields = [
        "name",
        "description",
        "celestial_name",
        "starting_torment",
        "domain",
    ]
    template_name = "characters/demon/house/form.html"


class DemonHouseListView(ListView):
    model = DemonHouse
    ordering = ["name"]
    template_name = "characters/demon/house/list.html"
