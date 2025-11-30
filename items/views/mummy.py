from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from items.models.mummy.relic import MummyRelic
from items.models.mummy.ushabti import Ushabti
from items.models.mummy.vessel import Vessel


class MummyRelicDetailView(DetailView):
    model = MummyRelic
    template_name = "items/mummy/relic/detail.html"


class MummyRelicCreateView(MessageMixin, CreateView):
    model = MummyRelic
    fields = [
        "name",
        "description",
        "rank",
        "relic_type",
        "era",
        "original_owner",
        "powers",
        "ba_cost",
        "associated_hekau",
        "requires_sekhem",
        "requires_ritual",
        "is_cursed",
        "is_unique",
        "is_sentient",
        "material",
        "hieroglyphic_inscription",
        "history",
        "current_location_notes",
    ]
    template_name = "items/mummy/relic/form.html"
    success_message = "Relic '{name}' created successfully!"
    error_message = "Failed to create relic. Please correct the errors below."


class MummyRelicUpdateView(MessageMixin, UpdateView):
    model = MummyRelic
    fields = [
        "name",
        "description",
        "rank",
        "relic_type",
        "era",
        "original_owner",
        "powers",
        "ba_cost",
        "associated_hekau",
        "requires_sekhem",
        "requires_ritual",
        "is_cursed",
        "is_unique",
        "is_sentient",
        "material",
        "hieroglyphic_inscription",
        "history",
        "current_location_notes",
    ]
    template_name = "items/mummy/relic/form.html"
    success_message = "Relic '{name}' updated successfully!"
    error_message = "Failed to update relic. Please correct the errors below."


class MummyRelicListView(ListView):
    model = MummyRelic
    ordering = ["name"]
    template_name = "items/mummy/relic/list.html"


class VesselDetailView(DetailView):
    model = Vessel
    template_name = "items/mummy/vessel/detail.html"


class VesselCreateView(MessageMixin, CreateView):
    model = Vessel
    fields = [
        "name",
        "description",
        "rank",
        "vessel_type",
        "transfer_rate",
        "efficiency",
        "is_portable",
        "requires_ritual",
        "is_attuned",
        "attuned_to",
        "material",
        "inscriptions",
    ]
    template_name = "items/mummy/vessel/form.html"
    success_message = "Vessel '{name}' created successfully!"
    error_message = "Failed to create vessel. Please correct the errors below."


class VesselUpdateView(MessageMixin, UpdateView):
    model = Vessel
    fields = [
        "name",
        "description",
        "rank",
        "current_ba",
        "vessel_type",
        "transfer_rate",
        "efficiency",
        "is_portable",
        "requires_ritual",
        "is_attuned",
        "attuned_to",
        "material",
        "inscriptions",
    ]
    template_name = "items/mummy/vessel/form.html"
    success_message = "Vessel '{name}' updated successfully!"
    error_message = "Failed to update vessel. Please correct the errors below."


class VesselListView(ListView):
    model = Vessel
    ordering = ["name"]
    template_name = "items/mummy/vessel/list.html"


class UshabtiDetailView(DetailView):
    model = Ushabti
    template_name = "items/mummy/ushabti/detail.html"


class UshabtiCreateView(MessageMixin, CreateView):
    model = Ushabti
    fields = [
        "name",
        "description",
        "rank",
        "purpose",
        "physical_rating",
        "mental_rating",
        "special_abilities",
        "material",
        "size_description",
        "appearance",
        "command_word",
        "obeys_only_creator",
        "creator",
    ]
    template_name = "items/mummy/ushabti/form.html"
    success_message = "Ushabti '{name}' created successfully!"
    error_message = "Failed to create ushabti. Please correct the errors below."


class UshabtiUpdateView(MessageMixin, UpdateView):
    model = Ushabti
    fields = [
        "name",
        "description",
        "rank",
        "is_currently_animated",
        "animation_duration_hours",
        "purpose",
        "physical_rating",
        "mental_rating",
        "special_abilities",
        "material",
        "size_description",
        "appearance",
        "command_word",
        "obeys_only_creator",
        "creator",
    ]
    template_name = "items/mummy/ushabti/form.html"
    success_message = "Ushabti '{name}' updated successfully!"
    error_message = "Failed to update ushabti. Please correct the errors below."


class UshabtiListView(ListView):
    model = Ushabti
    ordering = ["name"]
    template_name = "items/mummy/ushabti/list.html"
