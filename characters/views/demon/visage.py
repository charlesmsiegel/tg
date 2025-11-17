from characters.models.demon import Visage
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class VisageDetailView(DetailView):
    model = Visage
    template_name = "characters/demon/visage/detail.html"


class VisageCreateView(CreateView):
    model = Visage
    fields = [
        "name",
        "description",
        "house",
        "low_torment_traits",
        "high_torment_traits",
    ]
    template_name = "characters/demon/visage/form.html"


class VisageUpdateView(UpdateView):
    model = Visage
    fields = [
        "name",
        "description",
        "house",
        "low_torment_traits",
        "high_torment_traits",
    ]
    template_name = "characters/demon/visage/form.html"


class VisageListView(ListView):
    model = Visage
    ordering = ["name"]
    template_name = "characters/demon/visage/list.html"
