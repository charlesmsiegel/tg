from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.wraith import WraithArtifact, WraithRelic


# WraithRelic Views
class WraithRelicDetailView(DetailView):
    model = WraithRelic
    template_name = "items/wraith/relic/detail.html"


class WraithRelicCreateView(CreateView):
    model = WraithRelic
    fields = [
        "name",
        "description",
        "level",
        "rarity",
        "pathos_cost",
    ]
    template_name = "items/wraith/relic/form.html"


class WraithRelicUpdateView(UpdateView):
    model = WraithRelic
    fields = [
        "name",
        "description",
        "level",
        "rarity",
        "pathos_cost",
    ]
    template_name = "items/wraith/relic/form.html"


class WraithRelicListView(ListView):
    model = WraithRelic
    ordering = ["name"]
    template_name = "items/wraith/relic/list.html"


# WraithArtifact Views
class WraithArtifactDetailView(DetailView):
    model = WraithArtifact
    template_name = "items/wraith/artifact/detail.html"


class WraithArtifactCreateView(CreateView):
    model = WraithArtifact
    fields = [
        "name",
        "description",
        "level",
        "artifact_type",
        "material",
        "corpus",
        "pathos_cost",
    ]
    template_name = "items/wraith/artifact/form.html"


class WraithArtifactUpdateView(UpdateView):
    model = WraithArtifact
    fields = [
        "name",
        "description",
        "level",
        "artifact_type",
        "material",
        "corpus",
        "pathos_cost",
    ]
    template_name = "items/wraith/artifact/form.html"


class WraithArtifactListView(ListView):
    model = WraithArtifact
    ordering = ["name"]
    template_name = "items/wraith/artifact/list.html"
