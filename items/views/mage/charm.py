from typing import Any

from django.views.generic import DetailView

from items.models.mage import WonderResonanceRating
from items.registry import registry


class _CharmDetailView(DetailView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(wonder=self.object).order_by(
            "resonance__name"
        )
        return context


CharmDetailView = registry.view("items.Charm", "detail")


CharmListView = registry.view("items.Charm", "list")
CharmCreateView = registry.view("items.Charm", "create")
CharmUpdateView = registry.view("items.Charm", "update")
