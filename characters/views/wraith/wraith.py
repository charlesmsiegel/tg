from typing import Any

from characters.models.wraith.wraith import Wraith
from characters.views.core.human import HumanDetailView
from core.mixins import EditPermissionMixin, MessageMixin
from django.views.generic import CreateView, UpdateView


class WraithDetailView(HumanDetailView):
    model = Wraith
    template_name = "characters/wraith/wraith/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["arcanoi"] = self.object.get_arcanoi()
        context["dark_arcanoi"] = self.object.get_dark_arcanoi()
        return context


class WraithCreateView(MessageMixin, CreateView):
    model = Wraith
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "guild",
        "legion",
        "faction",
    ]
    template_name = "characters/wraith/wraith/form.html"
    success_message = "Wraith '{name}' created successfully!"
    error_message = "Failed to create wraith. Please correct the errors below."


class WraithUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Wraith
    fields = [
        "name",
        "nature",
        "demeanor",
        "concept",
        "chronicle",
        "image",
        "npc",
        "guild",
        "legion",
        "faction",
        "corpus",
        "pathos",
        "pathos_permanent",
        "angst",
        "angst_permanent",
        "willpower",
        "death_description",
        "age_at_death",
    ]
    template_name = "characters/wraith/wraith/form.html"
    success_message = "Wraith '{name}' updated successfully!"
    error_message = "Failed to update wraith. Please correct the errors below."
