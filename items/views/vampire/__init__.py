from items.models.vampire import Bloodstone, VampireArtifact
from django.views.generic import CreateView, DetailView, ListView, UpdateView


# VampireArtifact Views
class VampireArtifactDetailView(DetailView):
    model = VampireArtifact
    template_name = "items/vampire/artifact/detail.html"


class VampireArtifactCreateView(CreateView):
    model = VampireArtifact
    fields = [
        "name",
        "description",
        "power_level",
        "background_cost",
        "is_cursed",
        "is_unique",
        "requires_blood",
        "powers",
        "history",
    ]
    template_name = "items/vampire/artifact/form.html"


class VampireArtifactUpdateView(UpdateView):
    model = VampireArtifact
    fields = [
        "name",
        "description",
        "power_level",
        "background_cost",
        "is_cursed",
        "is_unique",
        "requires_blood",
        "powers",
        "history",
    ]
    template_name = "items/vampire/artifact/form.html"


class VampireArtifactListView(ListView):
    model = VampireArtifact
    ordering = ["name"]
    template_name = "items/vampire/artifact/list.html"


# Bloodstone Views
class BloodstoneDetailView(DetailView):
    model = Bloodstone
    template_name = "items/vampire/bloodstone/detail.html"


class BloodstoneCreateView(CreateView):
    model = Bloodstone
    fields = [
        "name",
        "description",
        "blood_stored",
        "max_blood",
        "is_active",
        "created_by_generation",
        "stone_type",
    ]
    template_name = "items/vampire/bloodstone/form.html"


class BloodstoneUpdateView(UpdateView):
    model = Bloodstone
    fields = [
        "name",
        "description",
        "blood_stored",
        "max_blood",
        "is_active",
        "created_by_generation",
        "stone_type",
    ]
    template_name = "items/vampire/bloodstone/form.html"


class BloodstoneListView(ListView):
    model = Bloodstone
    ordering = ["name"]
    template_name = "items/vampire/bloodstone/list.html"
