from typing import Any

from django.views.generic import DetailView

from items.models.mage import WonderResonanceRating
from items.registry import registry


class _ArtifactDetailView(DetailView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = (
            WonderResonanceRating.objects.filter(wonder=self.object)
            .select_related("resonance")
            .order_by("resonance__name")
        )
        return context


ArtifactDetailView = registry.view("items.Artifact", "detail")


ArtifactListView = registry.view("items.Artifact", "list")
ArtifactCreateView = registry.view("items.Artifact", "create")
ArtifactUpdateView = registry.view("items.Artifact", "update")
