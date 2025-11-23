from django.views.generic import CreateView, DetailView, ListView, UpdateView
from locations.models.demon import Bastion, Reliquary


# Bastion Views
class BastionDetailView(DetailView):
    model = Bastion
    template_name = "locations/demon/bastion/detail.html"


class BastionCreateView(CreateView):
    model = Bastion
    fields = [
        "name",
        "description",
        "parent",
        "ritual_strength",
        "warding_level",
        "consecration_date",
    ]
    template_name = "locations/demon/bastion/form.html"


class BastionUpdateView(UpdateView):
    model = Bastion
    fields = [
        "name",
        "description",
        "parent",
        "ritual_strength",
        "warding_level",
        "consecration_date",
    ]
    template_name = "locations/demon/bastion/form.html"


class BastionListView(ListView):
    model = Bastion
    ordering = ["name"]
    template_name = "locations/demon/bastion/list.html"


# Reliquary Views
class ReliquaryDetailView(DetailView):
    model = Reliquary
    template_name = "locations/demon/reliquary/detail.html"


class ReliquaryCreateView(CreateView):
    model = Reliquary
    fields = [
        "name",
        "description",
        "parent",
        "reliquary_type",
        "location_size",
        "max_health_levels",
        "current_health_levels",
        "soak_rating",
        "has_pervasiveness",
        "has_manifestation",
        "manifestation_range",
    ]
    template_name = "locations/demon/reliquary/form.html"


class ReliquaryUpdateView(UpdateView):
    model = Reliquary
    fields = [
        "name",
        "description",
        "parent",
        "reliquary_type",
        "location_size",
        "max_health_levels",
        "current_health_levels",
        "soak_rating",
        "has_pervasiveness",
        "has_manifestation",
        "manifestation_range",
    ]
    template_name = "locations/demon/reliquary/form.html"


class ReliquaryListView(ListView):
    model = Reliquary
    ordering = ["name"]
    template_name = "locations/demon/reliquary/list.html"
