from core.mixins import EditPermissionMixin, MessageMixin, ViewPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.mummy.cult_temple import CultTemple
from locations.models.mummy.sanctuary import UndergroundSanctuary
from locations.models.mummy.tomb import Tomb


class TombDetailView(ViewPermissionMixin, DetailView):
    model = Tomb
    template_name = "locations/mummy/tomb/detail.html"


class TombCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Tomb
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "security",
        "sanctity",
        "era",
        "has_false_chambers",
        "has_hieroglyphic_wards",
        "has_treasure_cache",
        "has_sarcophagus",
        "has_cult_shrine",
        "has_underworld_portal",
        "ba_per_week",
        "guardian_description",
        "original_occupant",
        "discovered_date",
        "archaeological_status",
    ]
    template_name = "locations/mummy/tomb/form.html"
    success_message = "Tomb '{name}' created successfully!"
    error_message = "Failed to create tomb. Please correct the errors below."


class TombUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Tomb
    fields = [
        "name",
        "description",
        "contained_within",
        "size",
        "security",
        "sanctity",
        "era",
        "has_false_chambers",
        "has_hieroglyphic_wards",
        "has_treasure_cache",
        "has_sarcophagus",
        "has_cult_shrine",
        "has_underworld_portal",
        "ba_per_week",
        "duat_barrier",
        "guardian_description",
        "original_occupant",
        "discovered_date",
        "archaeological_status",
    ]
    template_name = "locations/mummy/tomb/form.html"
    success_message = "Tomb '{name}' updated successfully!"
    error_message = "Failed to update tomb. Please correct the errors below."


class TombListView(ListView):
    model = Tomb
    ordering = ["name"]
    template_name = "locations/mummy/tomb/list.html"


class CultTempleDetailView(ViewPermissionMixin, DetailView):
    model = CultTemple
    template_name = "locations/mummy/cult_temple/detail.html"


class CultTempleCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = CultTemple
    fields = [
        "name",
        "description",
        "contained_within",
        "cult_size",
        "public_cover",
        "cult_leader_name",
        "cult_wealth",
        "has_library",
        "has_ritual_chamber",
    ]
    template_name = "locations/mummy/cult_temple/form.html"
    success_message = "Cult Temple '{name}' created successfully!"
    error_message = "Failed to create cult temple. Please correct the errors below."


class CultTempleUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = CultTemple
    fields = [
        "name",
        "description",
        "contained_within",
        "cult_size",
        "public_cover",
        "cult_leader_name",
        "cult_wealth",
        "has_library",
        "has_ritual_chamber",
    ]
    template_name = "locations/mummy/cult_temple/form.html"
    success_message = "Cult Temple '{name}' updated successfully!"
    error_message = "Failed to update cult temple. Please correct the errors below."


class CultTempleListView(ListView):
    model = CultTemple
    ordering = ["name"]
    template_name = "locations/mummy/cult_temple/list.html"


class UndergroundSanctuaryDetailView(ViewPermissionMixin, DetailView):
    model = UndergroundSanctuary
    template_name = "locations/mummy/sanctuary/detail.html"


class UndergroundSanctuaryCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = UndergroundSanctuary
    fields = [
        "name",
        "description",
        "contained_within",
        "sanctuary_type",
        "concealment_rating",
    ]
    template_name = "locations/mummy/sanctuary/form.html"
    success_message = "Sanctuary '{name}' created successfully!"
    error_message = "Failed to create sanctuary. Please correct the errors below."


class UndergroundSanctuaryUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = UndergroundSanctuary
    fields = [
        "name",
        "description",
        "contained_within",
        "sanctuary_type",
        "concealment_rating",
    ]
    template_name = "locations/mummy/sanctuary/form.html"
    success_message = "Sanctuary '{name}' updated successfully!"
    error_message = "Failed to update sanctuary. Please correct the errors below."


class UndergroundSanctuaryListView(ListView):
    model = UndergroundSanctuary
    ordering = ["name"]
    template_name = "locations/mummy/sanctuary/list.html"
