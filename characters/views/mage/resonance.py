from django.views.generic import CreateView, UpdateView

from characters.models.mage import Resonance
from core.mixins import MessageMixin
from core.views import CachedDetailView, CachedListView


class ResonanceDetailView(CachedDetailView):
    model = Resonance
    template_name = "characters/mage/resonance/detail.html"


class ResonanceCreateView(MessageMixin, CreateView):
    model = Resonance
    fields = [
        "name",
        "correspondence",
        "life",
        "prime",
        "entropy",
        "matter",
        "spirit",
        "forces",
        "mind",
        "time",
    ]
    template_name = "characters/mage/resonance/form.html"
    success_message = "Resonance created successfully."
    error_message = "There was an error creating the Resonance."


class ResonanceUpdateView(MessageMixin, UpdateView):
    model = Resonance
    fields = [
        "name",
        "correspondence",
        "life",
        "prime",
        "entropy",
        "matter",
        "spirit",
        "forces",
        "mind",
        "time",
    ]
    template_name = "characters/mage/resonance/form.html"
    success_message = "Resonance updated successfully."
    error_message = "There was an error updating the Resonance."


class ResonanceListView(CachedListView):
    model = Resonance
    ordering = ["name"]
    template_name = "characters/mage/resonance/list.html"
