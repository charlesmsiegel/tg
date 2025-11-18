from characters.forms.changeling.house_faction import HouseFactionForm
from characters.models.changeling.house_faction import HouseFaction
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class HouseFactionDetailView(DetailView):
    model = HouseFaction
    template_name = "characters/changeling/house_faction/detail.html"


class HouseFactionCreateView(CreateView):
    model = HouseFaction
    form_class = HouseFactionForm
    template_name = "characters/changeling/house_faction/form.html"


class HouseFactionUpdateView(UpdateView):
    model = HouseFaction
    form_class = HouseFactionForm
    template_name = "characters/changeling/house_faction/form.html"


class HouseFactionListView(ListView):
    model = HouseFaction
    ordering = ["name"]
    template_name = "characters/changeling/house_faction/list.html"
