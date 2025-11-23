from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.changeling import Treasure


# Treasure Views
class TreasureDetailView(DetailView):
    model = Treasure
    template_name = "items/changeling/treasure/detail.html"


class TreasureCreateView(CreateView):
    model = Treasure
    fields = [
        "name",
        "description",
        "rating",
        "treasure_type",
        "creator",
        "creation_method",
        "permanence",
        "special_abilities",
        "glamour_storage",
        "glamour_affinity",
    ]
    template_name = "items/changeling/treasure/form.html"


class TreasureUpdateView(UpdateView):
    model = Treasure
    fields = [
        "name",
        "description",
        "rating",
        "treasure_type",
        "creator",
        "creation_method",
        "permanence",
        "special_abilities",
        "glamour_storage",
        "glamour_affinity",
    ]
    template_name = "items/changeling/treasure/form.html"


class TreasureListView(ListView):
    model = Treasure
    ordering = ["name"]
    template_name = "items/changeling/treasure/list.html"
