from characters.models.vampire.discipline import Discipline
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class DisciplineDetailView(DetailView):
    model = Discipline
    template_name = "characters/vampire/discipline/detail.html"


class DisciplineCreateView(CreateView):
    model = Discipline
    fields = [
        "name",
        "property_name",
    ]
    template_name = "characters/vampire/discipline/form.html"


class DisciplineUpdateView(UpdateView):
    model = Discipline
    fields = [
        "name",
        "property_name",
    ]
    template_name = "characters/vampire/discipline/form.html"


class DisciplineListView(ListView):
    model = Discipline
    ordering = ["name"]
    template_name = "characters/vampire/discipline/list.html"
