from characters.models.core import Ability, Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class RoteDetailView(DetailView):
    model = Rote
    template_name = "characters/mage/rote/detail.html"


class RoteCreateView(CreateView):
    model = Rote
    fields = ["name", "description", "effect", "practice", "attribute", "ability"]
    template_name = "characters/mage/rote/form.html"


class RoteUpdateView(UpdateView):
    model = Rote
    fields = ["name", "description", "effect", "practice", "attribute", "ability"]
    template_name = "characters/mage/rote/form.html"


class RoteListView(ListView):
    model = Rote
    ordering = ["name"]
    template_name = "characters/mage/rote/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["practices"] = Practice.objects.all().order_by("name")
        context["attributes"] = Attribute.objects.all().order_by("name")
        context["abilities"] = Ability.objects.all().order_by("name")
        return context
