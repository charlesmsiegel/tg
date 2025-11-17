from characters.models.demon import Lore
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class LoreDetailView(DetailView):
    model = Lore
    template_name = "characters/demon/lore/detail.html"


class LoreCreateView(CreateView):
    model = Lore
    fields = [
        "name",
        "description",
        "property_name",
        "houses",
    ]
    template_name = "characters/demon/lore/form.html"


class LoreUpdateView(UpdateView):
    model = Lore
    fields = [
        "name",
        "description",
        "property_name",
        "houses",
    ]
    template_name = "characters/demon/lore/form.html"


class LoreListView(ListView):
    model = Lore
    ordering = ["name"]
    template_name = "characters/demon/lore/list.html"
