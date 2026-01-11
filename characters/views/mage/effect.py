from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.mage import Effect
from core.mixins import MessageMixin


class EffectDetailView(DetailView):
    model = Effect
    template_name = "characters/mage/effect/detail.html"


class EffectCreateView(MessageMixin, CreateView):
    model = Effect
    fields = [
        "name",
        "description",
        "correspondence",
        "time",
        "spirit",
        "matter",
        "life",
        "forces",
        "entropy",
        "mind",
        "prime",
    ]
    template_name = "characters/mage/effect/form.html"
    success_message = "Effect created successfully."
    error_message = "There was an error creating the Effect."


class EffectUpdateView(MessageMixin, UpdateView):
    model = Effect
    fields = [
        "name",
        "description",
        "correspondence",
        "time",
        "spirit",
        "matter",
        "life",
        "forces",
        "entropy",
        "mind",
        "prime",
    ]
    template_name = "characters/mage/effect/form.html"
    success_message = "Effect updated successfully."
    error_message = "There was an error updating the Effect."


class EffectListView(ListView):
    model = Effect
    ordering = ["name"]
    template_name = "characters/mage/effect/list.html"
