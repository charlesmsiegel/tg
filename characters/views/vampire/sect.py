from characters.models.vampire.sect import VampireSect
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class VampireSectDetailView(DetailView):
    model = VampireSect
    template_name = "characters/vampire/sect/detail.html"


class VampireSectCreateView(CreateView):
    model = VampireSect
    fields = [
        "name",
        "description",
        "philosophy",
    ]
    template_name = "characters/vampire/sect/form.html"


class VampireSectUpdateView(UpdateView):
    model = VampireSect
    fields = [
        "name",
        "description",
        "philosophy",
    ]
    template_name = "characters/vampire/sect/form.html"


class VampireSectListView(ListView):
    model = VampireSect
    ordering = ["name"]
    template_name = "characters/vampire/sect/list.html"
