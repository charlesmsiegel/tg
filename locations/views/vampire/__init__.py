from locations.models.vampire import Domain, Elysium, Haven, Rack
from django.views.generic import CreateView, DetailView, ListView, UpdateView


# Haven Views
class HavenDetailView(DetailView):
    model = Haven
    template_name = "locations/vampire/haven/detail.html"


class HavenCreateView(CreateView):
    model = Haven
    fields = [
        "name",
        "description",
        "parent",
        "size",
        "security",
        "location",
        "has_guardian",
        "has_luxury",
        "is_hidden",
        "has_library",
        "has_workshop",
    ]
    template_name = "locations/vampire/haven/form.html"


class HavenUpdateView(UpdateView):
    model = Haven
    fields = [
        "name",
        "description",
        "parent",
        "size",
        "security",
        "location",
        "has_guardian",
        "has_luxury",
        "is_hidden",
        "has_library",
        "has_workshop",
    ]
    template_name = "locations/vampire/haven/form.html"


class HavenListView(ListView):
    model = Haven
    ordering = ["name"]
    template_name = "locations/vampire/haven/list.html"


# Domain Views
class DomainDetailView(DetailView):
    model = Domain
    template_name = "locations/vampire/domain/detail.html"


class DomainCreateView(CreateView):
    model = Domain
    fields = [
        "name",
        "description",
        "parent",
        "size",
        "population",
        "control",
        "is_elysium",
        "has_rack",
        "is_disputed",
        "domain_type",
    ]
    template_name = "locations/vampire/domain/form.html"


class DomainUpdateView(UpdateView):
    model = Domain
    fields = [
        "name",
        "description",
        "parent",
        "size",
        "population",
        "control",
        "is_elysium",
        "has_rack",
        "is_disputed",
        "domain_type",
    ]
    template_name = "locations/vampire/domain/form.html"


class DomainListView(ListView):
    model = Domain
    ordering = ["name"]
    template_name = "locations/vampire/domain/list.html"


# Elysium Views
class ElysiumDetailView(DetailView):
    model = Elysium
    template_name = "locations/vampire/elysium/detail.html"


class ElysiumCreateView(CreateView):
    model = Elysium
    fields = [
        "name",
        "description",
        "parent",
        "prestige",
        "keeper_name",
        "elysium_type",
        "is_protected",
        "allows_weapons",
        "has_blood_dolls",
        "has_art_collection",
        "has_library",
        "is_court",
    ]
    template_name = "locations/vampire/elysium/form.html"


class ElysiumUpdateView(UpdateView):
    model = Elysium
    fields = [
        "name",
        "description",
        "parent",
        "prestige",
        "keeper_name",
        "elysium_type",
        "is_protected",
        "allows_weapons",
        "has_blood_dolls",
        "has_art_collection",
        "has_library",
        "is_court",
    ]
    template_name = "locations/vampire/elysium/form.html"


class ElysiumListView(ListView):
    model = Elysium
    ordering = ["name"]
    template_name = "locations/vampire/elysium/list.html"


# Rack Views
class RackDetailView(DetailView):
    model = Rack
    template_name = "locations/vampire/rack/detail.html"


class RackCreateView(CreateView):
    model = Rack
    fields = [
        "name",
        "description",
        "parent",
        "quality",
        "population_density",
        "risk_level",
        "rack_type",
        "blood_quality",
        "is_protected",
        "is_exclusive",
        "is_contested",
        "masquerade_risk",
    ]
    template_name = "locations/vampire/rack/form.html"


class RackUpdateView(UpdateView):
    model = Rack
    fields = [
        "name",
        "description",
        "parent",
        "quality",
        "population_density",
        "risk_level",
        "rack_type",
        "blood_quality",
        "is_protected",
        "is_exclusive",
        "is_contested",
        "masquerade_risk",
    ]
    template_name = "locations/vampire/rack/form.html"


class RackListView(ListView):
    model = Rack
    ordering = ["name"]
    template_name = "locations/vampire/rack/list.html"
