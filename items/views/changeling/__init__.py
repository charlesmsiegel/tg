from django.views.generic import CreateView, DetailView, ListView, UpdateView

from items.models.changeling import Dross, Treasure


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


# Dross Views
class DrossDetailView(DetailView):
    model = Dross
    template_name = "items/changeling/dross/detail.html"


class DrossCreateView(CreateView):
    model = Dross
    fields = [
        "name",
        "description",
        "quality",
        "glamour_value",
        "physical_form",
        "color",
        "source",
        "is_stable",
        "decay_rate",
        "resonance",
        "special_effects",
        "restricted_to",
        "is_consumable",
        "recharge_method",
        "container_description",
        "estimated_value",
    ]
    template_name = "items/changeling/dross/form.html"


class DrossUpdateView(UpdateView):
    model = Dross
    fields = [
        "name",
        "description",
        "quality",
        "glamour_value",
        "physical_form",
        "color",
        "source",
        "is_stable",
        "decay_rate",
        "resonance",
        "special_effects",
        "restricted_to",
        "is_consumable",
        "recharge_method",
        "container_description",
        "estimated_value",
    ]
    template_name = "items/changeling/dross/form.html"


class DrossListView(ListView):
    model = Dross
    ordering = ["name"]
    template_name = "items/changeling/dross/list.html"
